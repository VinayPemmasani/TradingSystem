"""The Paper Fund: pretend capital, real prices, every sleeve on one ledger.

Timeline for each session ``d`` (index ``i``):

1. Open of ``d``: yesterday's orders fill at the open. Orders from all sleeves
   are netted per ticker first (sleeves trading against each other cross
   internally for free, as a real multi-strategy fund would), the net is capped
   at ``max_participation`` of 20-day average volume, and costs come from
   ``costs.cost_fraction`` on the net shares, shared out by each sleeve's size.
2. Close of ``d``: positions are marked, short borrow is charged, the HFT
   sleeve books its modelled day.
3. After the close: every sleeve computes targets from data up to ``d``; the
   difference to what it holds becomes tomorrow's orders.

With ``sentiment.realtime`` the MiroFish sleeve instead fills on day ``d`` at
the price before the news (yesterday's close for news that came out before the
open, today's open otherwise). That is an upper bound on what faster data
could add, not a backtest: the signal still uses today's close.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import costs as C
from .config import FundConfig
from .data import BENCHMARK, Fundamentals, Market, listing
from .strategies import Ctx, Fundamental, PairsStatArb, Sentiment, Trend, overlay

SENT = "mirofish_sentiment"
HFT = "hft_market_making"


@dataclass
class Sleeve:
    name: str
    capital: float
    cash: float
    pos: dict[str, float] = field(default_factory=dict)
    strategy: object = None

    def equity(self, px: pd.Series) -> float:
        return self.cash + sum(q * px[t] for t, q in self.pos.items() if q)


@dataclass
class Result:
    cfg: FundConfig
    equity: pd.DataFrame  # date x sleeve (plus "fund", "benchmark")
    pnl: pd.DataFrame  # long: date, sleeve, ticker, exchange, pnl, cost, traded
    notes: list[str]
    stats: dict

    def by(self, *keys: str) -> pd.DataFrame:
        return self.pnl.groupby(list(keys))[["pnl", "cost", "traded"]].sum()


def hft_pnl(market: Market, i: int, tickers: list[str], capital: float, cfg,
            costs_cfg) -> dict[str, float]:
    """One day of modelled market making per ticker (see config.HFTConfig)."""
    scale = min(1.0, capital / cfg.capital_cap) if cfg.capital_cap > 0 else 0.0
    out = {}
    px, vol, r = market.close.iloc[i], market.volume.iloc[i], market.returns.iloc[i]
    sig = market.vol20.iloc[i - 1] if i > 0 else market.vol20.iloc[i]
    adv = market.adv20.iloc[i - 1] if i > 0 else market.adv20.iloc[i]
    for t in tickers:
        p, v, ret, s, a = px.get(t), vol.get(t), r.get(t), sig.get(t), adv.get(t)
        if not all(np.isfinite(x) for x in (p, v, ret, s, a)) or s <= 0:
            continue
        hs = C.half_spread_bps(p, a, costs_cfg)
        edge_bps = (hs * cfg.capture_half_spread_frac * (1 - cfg.adverse_selection) + cfg.rebate_bps
                    - cfg.trend_penalty * hs * abs(ret) / s)
        out[t] = scale * cfg.volume_share * v * p * edge_bps / 1e4
    return out


class PaperFund:
    def __init__(self, market: Market, cfg: FundConfig | None = None, signals=None,
                 fundamentals: Fundamentals | None = None, tickers: list[str] | None = None):
        self.m, self.cfg = market, cfg or FundConfig()
        self.signals, self.fund = signals, fundamentals
        self.tickers = [t for t in (tickers or market.tickers) if t in market.close]
        alloc = {k: v for k, v in self.cfg.allocation.items() if v > 0}
        if not self.cfg.sentiment.enabled:
            alloc.pop(SENT, None)
        tot = sum(alloc.values())
        self.alloc = {k: v / tot for k, v in alloc.items()}
        strat = {
            "systematic_trend": lambda: Trend(self.cfg.trend, self.tickers),
            "stat_arb": lambda: PairsStatArb(self.cfg.pairs, set(self.tickers)),
            "fundamental": lambda: Fundamental(self.cfg.fundamental, self.tickers),
            SENT: lambda: Sentiment(self.cfg.sentiment),
            HFT: lambda: None,
        }
        self.sleeves = {k: Sleeve(k, w * self.cfg.capital, w * self.cfg.capital, strategy=strat[k]())
                        for k, w in self.alloc.items()}
        self.notes: list[str] = []
        self.max_participation = 0.0
        if "fundamental" in self.sleeves and fundamentals is None:
            self.notes.append("fundamental sleeve held cash: no fundamentals file was given")
        if SENT in self.sleeves and signals is None:
            self.notes.append("MiroFish sleeve held cash: no news was given")

    # ------------------------------------------------------------------
    def run(self) -> Result:
        m, cfg = self.m, self.cfg
        close_ff = m.close.ffill()
        rows: list[tuple] = []
        eq_rows = []
        pending: dict[str, dict[str, float]] = {}
        crossed = 0.0
        unfilled = 0.0
        participation_hits = 0
        for i, d in enumerate(m.sessions):
            px_c = close_ff.iloc[i]
            px_prev = close_ff.iloc[i - 1] if i > 0 else px_c
            px_o = m.open.iloc[i]
            day: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])

            # 1. mark yesterday's positions to today's close
            for s in self.sleeves.values():
                for t, q in s.pos.items():
                    if q and np.isfinite(px_c[t]) and np.isfinite(px_prev[t]):
                        day[(s.name, t)][0] += q * (px_c[t] - px_prev[t])

            # 2. fill yesterday's orders at today's open
            if pending:
                c, u, h = self._execute(pending, i, px_o, px_c, day)
                crossed += c
                unfilled += u
                participation_hits += h
                pending = {}

            # 3. borrow and HFT
            for s in self.sleeves.values():
                for t, q in s.pos.items():
                    if q < 0 and np.isfinite(px_c[t]):
                        fee = -q * px_c[t] * cfg.costs.borrow_bps_per_year / 1e4 / 252
                        s.cash -= fee
                        day[(s.name, t)][0] -= fee
                        day[(s.name, t)][1] += fee
            if HFT in self.sleeves and i >= cfg.warmup:
                s = self.sleeves[HFT]
                for t, p in hft_pnl(m, i, self.tickers, s.capital, cfg.hft, cfg.costs).items():
                    s.cash += p
                    day[(HFT, t)][0] += p

            # 4. signals and targets after the close
            sigs = {}
            if self.signals is not None and i < len(m.sessions) - 1:
                if i < cfg.warmup:
                    self.signals.warm(d)
                else:
                    sigs = self.signals.signals(d)
            if i >= cfg.warmup and i < len(m.sessions) - 1:
                ctx = Ctx(m, i, sigs, self.fund)
                for s in self.sleeves.values():
                    if s.strategy is None:
                        continue
                    w = s.strategy.targets(ctx)
                    if s.name != SENT and cfg.sentiment.enabled:
                        w = overlay(w, sigs, cfg.sentiment.overlay)
                    if w is None:
                        continue
                    eq = s.equity(px_c)
                    orders = {}
                    for t in set(w) | set(s.pos):
                        p = px_c.get(t)
                        if p is None or not np.isfinite(p) or p <= 0:
                            continue
                        want = w.get(t, 0.0) * eq / p
                        dq = want - s.pos.get(t, 0.0)
                        if abs(dq * p) > 1e-6 * max(eq, 1.0) and abs(dq) >= 1:
                            orders[t] = dq
                    if s.name == SENT and cfg.sentiment.realtime and orders:
                        self._realtime_fill(s, orders, sigs, i, px_c, px_prev, px_o, day)
                    elif orders:
                        pending[s.name] = orders
            elif i == len(m.sessions) - 1:
                pass  # positions stay marked at the last close

            for (sl, t), (p, cst, trd) in day.items():
                if p or cst or trd:
                    rows.append((d, sl, t, listing(t) if t != BENCHMARK else "NASDAQ", p, cst, trd))
            eq_rows.append({"date": d, **{k: s.equity(px_c) for k, s in self.sleeves.items()}})

        eq = pd.DataFrame(eq_rows).set_index("date")
        eq["fund"] = eq.sum(axis=1)
        b = close_ff[BENCHMARK]
        eq["benchmark"] = cfg.capital * b / b.iloc[cfg.warmup] if len(b) > cfg.warmup else np.nan
        pnl = pd.DataFrame(rows, columns=["date", "sleeve", "ticker", "exchange", "pnl", "cost", "traded"])
        stats = {"internally_crossed_notional": crossed, "unfilled_notional": unfilled,
                 "participation_cap_hits": participation_hits,
                 "max_participation_used": self.max_participation}
        return Result(cfg, eq, pnl, self.notes, stats)

    # ------------------------------------------------------------------
    def _execute(self, pending, i, px_o, px_c, day):
        m, cc = self.m, self.cfg.costs
        adv = m.adv20.iloc[i - 1]
        sig = m.vol20.iloc[i - 1]
        per_t: dict[str, dict[str, float]] = defaultdict(dict)
        for sl, orders in pending.items():
            for t, q in orders.items():
                per_t[t][sl] = q
        crossed = unfilled = 0.0
        hits = 0
        for t, by_sleeve in per_t.items():
            p = px_o.get(t)
            if p is None or not np.isfinite(p) or p <= 0:
                continue
            net = sum(by_sleeve.values())
            gross = sum(abs(q) for q in by_sleeve.values())
            a = adv.get(t, np.nan)
            a = a if np.isfinite(a) else 0.0
            cap = C.fill_cap(a, cc)
            ratio = 1.0
            if abs(net) > cap:
                ratio = cap / abs(net) if abs(net) > 0 else 1.0
                hits += 1
            exec_net = abs(net) * ratio
            if a > 0:
                self.max_participation = max(self.max_participation, exec_net / a)
            s_ = sig.get(t, np.nan)
            frac = C.cost_fraction(exec_net, p, a, s_ if np.isfinite(s_) else 0.02, cc)
            cost_total = exec_net * p * frac
            crossed += (gross - abs(net)) * p
            unfilled += abs(net) * (1 - ratio) * p
            for sl, q in by_sleeve.items():
                fq = q * ratio
                s = self.sleeves[sl]
                share = abs(fq) / (gross * ratio) if gross > 0 and ratio > 0 else 0.0
                cst = cost_total * share
                s.cash -= fq * p + cst
                s.pos[t] = s.pos.get(t, 0.0) + fq
                pc = px_c.get(t)
                if pc is not None and np.isfinite(pc):
                    day[(sl, t)][0] += fq * (pc - p)
                day[(sl, t)][0] -= cst
                day[(sl, t)][1] += cst
                day[(sl, t)][2] += abs(fq) * p
        return crossed, unfilled, hits

    def _realtime_fill(self, s, orders, sigs, i, px_c, px_prev, px_o, day):
        """Upper bound for faster news: fill at the pre-news price on the signal day itself."""
        m, cc = self.m, self.cfg.costs
        adv, sig = m.adv20.iloc[i - 1], m.vol20.iloc[i - 1]
        for t, q in orders.items():
            sg = sigs.get(t)
            p = (px_prev.get(t) if sg is not None and sg.premarket else px_o.get(t)) if sg else None
            if p is None or not np.isfinite(p):
                p = px_c[t]  # no new news for this name: an ordinary exit at today's close
            a = adv.get(t, 0.0)
            a = a if np.isfinite(a) else 0.0
            fq = math.copysign(min(abs(q), C.fill_cap(a, cc)), q)
            s_ = sig.get(t, np.nan)
            cst = abs(fq) * p * C.cost_fraction(abs(fq), p, a, s_ if np.isfinite(s_) else 0.02, cc)
            s.cash -= fq * p + cst
            s.pos[t] = s.pos.get(t, 0.0) + fq
            day[(s.name, t)][0] += fq * (px_c[t] - p) - cst
            day[(s.name, t)][1] += cst
            day[(s.name, t)][2] += abs(fq) * p
