"""A synthetic market for tests and the offline demo: MiroFish's synthetic Nasdaq year plus
GOOG (cointegrated with GOOGL), eight NYSE names and a flat EPS table.

Its news has a planted price reaction, so the sentiment sleeve *should* make money
here. Synthetic results prove the plumbing, never an edge.
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from . import data
from mirofish_trader.ingest.synthetic import generate


def world(days: int = 260, seed: int = 42):
    w = generate(days=days, seed=seed)
    bars = w.bars.copy()
    rng = np.random.default_rng(seed + 1)
    g = bars[bars["ticker"] == "GOOGL"].copy()
    noise = np.exp(np.cumsum(rng.normal(0, 0.002, len(g))) * 0.3)
    for c in ("open", "high", "low", "close"):
        g[c] = g[c].to_numpy() * 0.995 * noise
    g["ticker"] = "GOOG"
    extra = [g]
    q = bars[bars["ticker"] == data.BENCHMARK].sort_values("date")
    qr = q["close"].pct_change().fillna(0).to_numpy()
    for k, t in enumerate(sorted(data.NYSE)):
        r = 0.6 * qr + rng.normal(0, 0.012, len(q))
        c = 80.0 * (1 + k / 4) * np.cumprod(1 + r)
        o = c / (1 + r) * (1 + rng.normal(0, 0.002, len(q)))
        extra.append(pd.DataFrame({"date": q["date"].to_numpy(), "ticker": t, "open": o,
                                   "high": np.maximum(o, c) * 1.004, "low": np.minimum(o, c) * 0.996,
                                   "close": c, "volume": rng.integers(5_000_000, 15_000_000, len(q))}))
    bars = pd.concat([bars] + extra, ignore_index=True)
    tickers = sorted(set(bars["ticker"]) - {data.BENCHMARK})
    eps = pd.DataFrame({"ticker": tickers, "available": date(2000, 1, 1),
                        "eps_ttm": rng.uniform(1, 12, len(tickers))})
    return bars, w.news, eps
