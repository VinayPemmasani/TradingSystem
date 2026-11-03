"""Inputs: daily bars, listing exchanges, fundamentals, news and Reddit posts.

Prices CSV (long): ``date,ticker,open,high,low,close,volume``; must include QQQ.
Fundamentals CSV: ``ticker,available,eps_ttm`` where ``available`` is the date
the number was public (the filing or earnings release date), never the
fiscal period end, so the fundamental sleeve cannot see a report early.
News and Reddit JSONL: one item per line, ``{"ts", "source", "headline", ...}``;
Reddit items use ``"source": "reddit"`` and get Reddit's low credibility weight.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

_MIROFISH = Path(__file__).resolve().parents[2] / "mirofish"
if str(_MIROFISH) not in sys.path:
    sys.path.insert(0, str(_MIROFISH))

from mirofish_trader import universe as mf_universe  # noqa: E402
from mirofish_trader.ingest.news import load_jsonl  # noqa: E402,F401
from mirofish_trader.models import NewsItem  # noqa: E402,F401

BENCHMARK = "QQQ"

# Listing exchange and sector for every name the fund trades. The MiroFish universe is all
# Nasdaq-listed; the NYSE names are there so "per exchange" means something and so the
# classic NYSE pairs (KO/PEP, V/MA, XOM/CVX) can trade.
NYSE = {"JPM": "banks", "XOM": "energy", "CVX": "energy", "KO": "staples", "V": "payments",
        "MA": "payments", "WMT": "retail", "JNJ": "pharma"}
EXTRA_NASDAQ = {"GOOG": "internet"}


def listing(ticker: str) -> str:
    return "NYSE" if ticker in NYSE else "NASDAQ"


def sector(ticker: str) -> str:
    if ticker in NYSE:
        return NYSE[ticker]
    if ticker in EXTRA_NASDAQ:
        return EXTRA_NASDAQ[ticker]
    c = mf_universe.get(ticker)
    return c.sector if c else "other"


def default_universe() -> list[str]:
    return sorted(set(mf_universe.tickers()) | set(EXTRA_NASDAQ) | set(NYSE))


class Market:
    """Wide frames of daily bars with as-of helpers. Nothing here looks past ``d``."""

    def __init__(self, bars: pd.DataFrame):
        bars = bars.copy()
        bars["date"] = pd.to_datetime(bars["date"]).dt.date
        bars["ticker"] = bars["ticker"].str.upper()
        bars = bars.drop_duplicates(["date", "ticker"], keep="last")
        self.bars = bars.sort_values(["date", "ticker"]).reset_index(drop=True)
        piv = {c: bars.pivot(index="date", columns="ticker", values=c).sort_index()
               for c in ("open", "high", "low", "close", "volume")}
        self.open, self.high, self.low = piv["open"], piv["high"], piv["low"]
        self.close, self.volume = piv["close"], piv["volume"]
        if BENCHMARK not in self.close:
            raise ValueError(f"price data has no {BENCHMARK} benchmark")
        self.sessions: list[date] = list(self.close.index)
        self.pos = {d: i for i, d in enumerate(self.sessions)}
        self.returns = self.close.pct_change(fill_method=None)
        self.vol20 = self.returns.rolling(20, min_periods=10).std().shift(0)
        self.adv20 = self.volume.rolling(20, min_periods=5).mean()

    @classmethod
    def from_csv(cls, path: str | Path) -> "Market":
        return cls(pd.read_csv(path))

    @property
    def tickers(self) -> list[str]:
        return [t for t in self.close.columns if t != BENCHMARK]

    def to_mirofish(self):
        from mirofish_trader.ingest.prices import MarketData
        return MarketData(self.bars[["date", "ticker", "open", "high", "low", "close", "volume"]])


@dataclass
class Fundamentals:
    table: pd.DataFrame  # ticker, available (date), eps_ttm

    @classmethod
    def from_csv(cls, path: str | Path) -> "Fundamentals":
        t = pd.read_csv(path)
        t["available"] = pd.to_datetime(t["available"]).dt.date
        t["ticker"] = t["ticker"].str.upper()
        return cls(t.sort_values(["ticker", "available"]).reset_index(drop=True))

    def eps_asof(self, d: date, lag_days: int = 1) -> dict[str, float]:
        cutoff = np.datetime64(d) - np.timedelta64(lag_days, "D")
        known = self.table[pd.to_datetime(self.table["available"]).values <= cutoff]
        return known.groupby("ticker")["eps_ttm"].last().to_dict()
