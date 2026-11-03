"""What-ifs that answer "why does it (not) work": each one changes one thing.

- ``baseline``            the fund as configured
- ``no_sentiment``        MiroFish off: no sentiment sleeve, no overlay
- ``placebo_news``        news shifted 20 sessions late, so it no longer matches prices
- ``realtime_news``       MiroFish fills at the pre-news price (upper bound for faster data)
- ``hft_colocated``       market making with half the adverse selection (what speed buys)
- ``capacity_*``          the same fund at $10k (retail, Trading 212-style FX fee), $10m, $500m, $5bn
- ``robustness``          neighbouring parameter values; a real edge should not hinge on one
"""

from __future__ import annotations

import copy
from dataclasses import replace

from .config import FundConfig
from .engine import PaperFund  # noqa: F401
from .report import summary
from .sentiment import MiroFishSignals


def make_signals(market, news, cfg: FundConfig, seeds: int | None):
    if not news or not cfg.sentiment.enabled:
        return None
    from mirofish_trader.config import Config as MFConfig
    mf = MFConfig()
    mf.decision.entry_threshold = cfg.sentiment.entry_threshold
    return MiroFishSignals(news, market, delay=cfg.sentiment.news_delay_sessions, swarm_seeds=seeds,
                           mf_cfg=mf, news_filter=cfg.sentiment.news_filter)


def _run(market, news, fundamentals, cfg: FundConfig, seeds: int | None):
    return PaperFund(market, cfg, make_signals(market, news, cfg, seeds), fundamentals).run()


def variants(base: FundConfig) -> dict[str, FundConfig]:
    v = {"baseline": copy.deepcopy(base)}
    c = copy.deepcopy(base); c.sentiment.enabled = False; v["no_sentiment"] = c
    c = copy.deepcopy(base); c.sentiment.news_delay_sessions = 20; v["placebo_news"] = c
    c = copy.deepcopy(base); c.sentiment.realtime = True; v["realtime_news"] = c
    c = copy.deepcopy(base); c.hft.adverse_selection = base.hft.adverse_selection - 0.45
    v["hft_colocated"] = c
    for name, cap, fx in (("capacity_10k_retail", 1e4, 15.0), ("capacity_10m", 1e7, 0.0),
                          ("capacity_500m", 5e8, 0.0), ("capacity_5bn", 5e9, 0.0)):
        c = copy.deepcopy(base); c.capital = cap; c.costs.retail_fx_bps = fx
        if cap <= 1e4:
            c.costs.commission_bps = 0.0  # zero-commission app
            c.costs.half_spread_bps = 2.0
        v[name] = c
    return v


def robustness(base: FundConfig) -> dict[str, FundConfig]:
    v = {}
    for lb in (20, 60, 120, 250):
        c = copy.deepcopy(base); c.trend.lookback = lb; v[f"trend_lookback_{lb}"] = c
    for z in (1.5, 2.0, 2.5):
        c = copy.deepcopy(base); c.pairs.entry_z = z; v[f"pairs_entry_z_{z}"] = c
    for th in (0.06, 0.24):
        c = copy.deepcopy(base); c.sentiment.entry_threshold = th; v[f"mirofish_entry_{th}"] = c
    c = copy.deepcopy(base); c.fundamental.exclude_negative_eps = True
    v["fundamental_ex_loss_makers (chosen after seeing results)"] = c
    return v


def mirofish_tuning(market, news, base: FundConfig, seeds: int | None = 4) -> dict:
    """Tune MiroFish on the first half, judge it on the second half (walk-forward, one split).

    Runs the sentiment sleeve alone so nothing else blurs it. A setting that only shines
    in-sample is overfitting; the out-of-sample column is the one to believe.
    """
    import math
    sessions = market.sessions
    mid = sessions[len(sessions) // 2]
    rows = []
    for filt in ("all", "clean", "events"):
        for th in (0.06, 0.12, 0.24):
            for delay in (0, 20):
                c = copy.deepcopy(base)
                c.allocation = {"mirofish_sentiment": 1.0}
                c.sentiment.news_filter, c.sentiment.entry_threshold = filt, th
                c.sentiment.news_delay_sessions = delay
                eq = _run(market, news, None, c, seeds).equity["mirofish_sentiment"].iloc[c.warmup:]
                r = eq.diff().dropna() / c.capital
                ins, oos = r[r.index < mid], r[r.index >= mid]
                sh = lambda x: float(x.mean() / x.std() * math.sqrt(252)) if x.std() > 0 else 0.0
                rows.append({"filter": filt, "entry": th, "placebo": bool(delay),
                             "in_sample_sharpe": sh(ins), "out_of_sample_sharpe": sh(oos),
                             "in_sample_return": float(ins.sum()), "out_of_sample_return": float(oos.sum())})
    real = [x for x in rows if not x["placebo"]]
    best = max(real, key=lambda x: x["in_sample_sharpe"])
    return {"split": str(mid), "grid": rows, "chosen_in_sample": best}


def run_all(market, news, fundamentals, base: FundConfig, seeds: int | None = 4,
            which: list[str] | None = None, robust: bool = True) -> dict[str, dict]:
    out = {}
    todo = variants(base)
    if robust:
        todo.update(robustness(base))
    for name, cfg in todo.items():
        if which and name not in which:
            continue
        res = _run(market, news, fundamentals, cfg, seeds)
        out[name] = summary(res)
    return out


def news_timing_study(market, news, news_filter: str = "events") -> dict:
    """How much of a news move is gone before a daily system can trade? Uses a perfect-direction
    oracle, so it is the ceiling on what faster data alone could add, not a strategy.

    For every (ticker, release date d) with the release stamped after the close of d:
      realtime capture = |close(d) -> close(d+3)|: the whole move, entering right after the
                         release (at the close of d; after-hours prices are not in daily bars,
                         so this flatters real time)
      daily capture    = the same direction call entered at open(d+2) and held to close(d+3),
                         which is what this fund's daily loop can reach (signal at the close of
                         d+1, fill at the next open)
    """
    import numpy as np
    from mirofish_trader.ingest.news import bucket_by_session
    from .sentiment import filter_news
    from . import data as D
    items = filter_news(news, news_filter)
    sessions = market.sessions
    pos = {d: i for i, d in enumerate(sessions)}
    c, o = market.close, market.open
    rt, dl, n = [], [], 0
    for d, its in bucket_by_session(items, sessions).items():
        i = pos[d]  # news after the close of i-1 lands on session i
        if i < 1 or i + 2 >= len(sessions):
            continue
        tickers = {t for it in its for t in it.tickers if t in c.columns and t != D.BENCHMARK}
        for t in tickers:
            a, b, x = c[t].iloc[i - 1], c[t].iloc[i + 2], o[t].iloc[i + 1]
            if not all(np.isfinite(v) for v in (a, b, x)):
                continue
            full = b / a - 1
            rt.append(abs(full))
            dl.append(np.sign(full) * (b / x - 1))  # same direction call, later entry
            n += 1
    return {"events": n, "filter": news_filter,
            "mean_abs_move_realtime_bps": float(np.mean(rt) * 1e4) if rt else 0.0,
            "mean_abs_move_daily_bps": float(np.mean(dl) * 1e4) if dl else 0.0,
            "share_gone_before_daily_fill": float(1 - np.mean(dl) / np.mean(rt)) if rt else 0.0}
