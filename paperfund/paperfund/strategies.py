"""The four strategy families as daily sleeves, plus MiroFish sentiment as a fifth.

Every sleeve sees only data up to and including the close of session ``i`` and
returns target weights as fractions of its own capital (negative = short), or
``None`` to keep what it holds. The engine fills at the next session's open.

- ``Trend``        systematic time-series momentum (the daily cousin of firm/strategy/trend.hpp)
- ``PairsStatArb`` z-score pairs on rolling hedge ratios (firm/strategy/pairs.hpp)
- ``Fundamental``  earnings-yield value, long cheap / short dear (firm/strategy/thesis.hpp)
- ``Sentiment``    MiroFish target weights, held for the signal's horizon
- HFT market making is modelled in ``engine.hft_pnl``; it holds no overnight positions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .config import FundamentalConfig, PairsConfig, SentimentConfig, TrendConfig
from .data import BENCHMARK, Fundamentals, Market


@dataclass
class Ctx:
    market: Market
    i: int
    signals: dict = field(default_factory=dict)  # ticker -> sentiment.Signal for this session
    fundamentals: Fundamentals | None = None

    @property
    def d(self):
        return self.market.sessions[self.i]


class Trend:
    name = "systematic_trend"

    def __init__(self, cfg: TrendConfig, tickers: list[str], rho: float = 0.3):
        self.cfg, self.tickers, self.rho = cfg, tickers + [BENCHMARK], rho
        self.last = -10**9

    def targets(self, ctx: Ctx):
        c, i = self.cfg, ctx.i
        if i - self.last < c.rebalance_every or i < c.lookback:
            return None
        self.last = i
        close, vol = ctx.market.close, ctx.market.vol20
        mom = close.iloc[i] / close.iloc[i - c.lookback] - 1.0
        v = vol.iloc[i]
        live = [t for t in self.tickers if t in close and np.isfinite(mom.get(t, np.nan))
                and np.isfinite(v.get(t, np.nan)) and v[t] > 0]
        n = len(live)
        if not n:
            return {}
        tv = c.target_vol / math.sqrt(252) / math.sqrt(n + n * (n - 1) * self.rho)
        return {t: float(np.clip(np.sign(mom[t]) * tv / v[t], -c.max_weight, c.max_weight))
                for t in live}


class PairsStatArb:
    name = "stat_arb"

    def __init__(self, cfg: PairsConfig, available: set[str]):
        self.cfg = cfg
        self.pairs = [(a, b) for a, b in cfg.pairs if a in available and b in available]
        self.state: dict[tuple[str, str], tuple[int, int]] = {}  # pair -> (side, entry index)

    def zscore(self, market: Market, a: str, b: str, i: int) -> float | None:
        w = self.cfg.window
        if i < w:
            return None
        la = np.log(market.close[a].iloc[i - w + 1:i + 1].to_numpy(float))
        lb = np.log(market.close[b].iloc[i - w + 1:i + 1].to_numpy(float))
        if not (np.all(np.isfinite(la)) and np.all(np.isfinite(lb))):
            return None
        beta = np.polyfit(lb, la, 1)[0]
        s = la - beta * lb
        sd = s.std()
        return float((s[-1] - s.mean()) / sd) if sd > 0 else None

    def targets(self, ctx: Ctx):
        c = self.cfg
        n = max(len(self.pairs), 1)
        out: dict[str, float] = {}
        for a, b in self.pairs:
            z = self.zscore(ctx.market, a, b, ctx.i)
            side, since = self.state.get((a, b), (0, ctx.i))
            if z is not None:
                if side == 0 and abs(z) > c.entry_z:
                    side, since = (-1 if z > 0 else 1), ctx.i
                elif side != 0 and (abs(z) < c.exit_z or abs(z) > c.stop_z
                                    or ctx.i - since >= c.max_hold):
                    side = 0
            self.state[(a, b)] = (side, since)
            # side +1 = long the spread: long a, short b
            out[a] = out.get(a, 0.0) + side * 0.5 / n
            out[b] = out.get(b, 0.0) - side * 0.5 / n
        return out


class Fundamental:
    name = "fundamental"

    def __init__(self, cfg: FundamentalConfig, tickers: list[str]):
        self.cfg, self.tickers = cfg, tickers
        self.last = -10**9

    def targets(self, ctx: Ctx):
        if ctx.fundamentals is None:
            return {}
        if ctx.i - self.last < self.cfg.rebalance_every:
            return None
        self.last = ctx.i
        eps = ctx.fundamentals.eps_asof(ctx.d, self.cfg.report_lag_days)
        px = ctx.market.close.iloc[ctx.i]
        ey = {t: eps[t] / px[t] for t in self.tickers
              if t in eps and t in px and np.isfinite(px[t]) and px[t] > 0
              and not (self.cfg.exclude_negative_eps and eps[t] <= 0)}
        if len(ey) < 6:
            return {}
        ranked = sorted(ey, key=ey.get)  # dearest (lowest earnings yield) first
        k = max(1, int(len(ranked) * self.cfg.quantile))
        out = {t: -0.5 / k for t in ranked[:k]}
        out.update({t: 0.5 / k for t in ranked[-k:]})
        return out


class Sentiment:
    name = "mirofish_sentiment"

    def __init__(self, cfg: SentimentConfig):
        self.cfg = cfg
        self.book: dict[str, tuple[float, int]] = {}  # ticker -> (weight, last index to hold)

    def targets(self, ctx: Ctx):
        for t, s in ctx.signals.items():
            if s.target_weight != 0.0:
                self.book[t] = (s.target_weight, ctx.i + s.horizon - 1)
            elif t in self.book and np.sign(s.alpha) != np.sign(self.book[t][0]):
                del self.book[t]  # fresh news against the position: get out
        self.book = {t: v for t, v in self.book.items() if v[1] >= ctx.i}
        w = {t: v[0] for t, v in self.book.items()}
        gross = sum(abs(x) for x in w.values())
        if gross > self.cfg.sleeve_gross:
            w = {t: x * self.cfg.sleeve_gross / gross for t, x in w.items()}
        return w


def overlay(weights: dict[str, float] | None, signals: dict, strength: float):
    """Tilt a sleeve's weights toward MiroFish: size up where news agrees, down where it disagrees."""
    if not weights or not signals or strength <= 0:
        return weights
    out = {}
    for t, w in weights.items():
        s = signals.get(t)
        if s is None or w == 0.0:
            out[t] = w
            continue
        agree = math.tanh(s.alpha) * (1 if w > 0 else -1)
        out[t] = w * max(0.0, 1.0 + strength * agree)
    return out
