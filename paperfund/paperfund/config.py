"""Every tunable of the Paper Fund in one place.

Defaults are chosen before looking at any real-data result and are not tuned
on it. ``scenarios.robustness`` reports how much the result moves when they do.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path


@dataclass
class CostConfig:
    """Institutional US equity costs. Square-root impact as in Almgren et al. (2005)."""

    commission_bps: float = 0.3  # broker commission plus exchange/clearing fees
    half_spread_bps: float = 1.0  # large-cap half spread; widened for thin names in costs.py
    impact_coef: float = 0.7  # Y in  cost = Y * sigma_daily * sqrt(shares / ADV)
    max_participation: float = 0.10  # never trade more than this share of a day's volume
    borrow_bps_per_year: float = 30.0  # general-collateral stock borrow for shorts
    retail_fx_bps: float = 0.0  # e.g. 15 for a GBP account on Trading 212 buying US stock


@dataclass
class TrendConfig:
    lookback: int = 60  # sessions of momentum
    vol_window: int = 20
    target_vol: float = 0.10  # annualised sleeve volatility target
    rebalance_every: int = 5  # sessions
    max_weight: float = 0.15


@dataclass
class PairsConfig:
    pairs: list[tuple[str, str]] = field(default_factory=lambda: [
        ("GOOGL", "GOOG"), ("KO", "PEP"), ("V", "MA"), ("XOM", "CVX"), ("AMD", "NVDA"),
        ("AMGN", "GILD"), ("MSFT", "AAPL"), ("QCOM", "AVGO"),
    ])
    window: int = 60
    entry_z: float = 2.0
    exit_z: float = 0.5
    stop_z: float = 4.0
    max_hold: int = 20


@dataclass
class FundamentalConfig:
    rebalance_every: int = 21  # monthly
    quantile: float = 0.33  # long the cheapest third, short the dearest third
    report_lag_days: int = 1  # a report is usable the session after it is published
    exclude_negative_eps: bool = False  # leave loss-makers out instead of shorting them as "dearest"


@dataclass
class HFTConfig:
    """Market making, modelled from daily bars (not backtested at tick level).

    The tick-level version is ``tools/quant-real`` on a Nasdaq ITCH day; these
    numbers are the knobs that version measures.
    """

    volume_share: float = 0.005  # share of each name's daily volume we trade as a maker
    capture_half_spread_frac: float = 1.0  # of the half spread earned per share traded
    rebate_bps: float = 0.2  # maker rebate net of take fees (Nasdaq tier pricing)
    adverse_selection: float = 0.9  # share of the spread lost to informed flow on a normal day
    trend_penalty: float = 0.5  # extra loss per unit of |return|/vol (inventory run over)
    capital_cap: float = 100e6  # what a market maker can actually deploy in these names


@dataclass
class SentimentConfig:
    enabled: bool = True
    overlay: float = 0.25  # tilt on other sleeves: weight *= 1 + overlay * agreement
    sleeve_gross: float = 1.0
    news_delay_sessions: int = 0  # placebo / delay tests shift news by this many sessions
    realtime: bool = False  # upper bound: fill at the price before the news
    news_filter: str = "all"  # all | clean | events (see sentiment.filter_news)
    entry_threshold: float = 0.12  # MiroFish decision entry threshold


@dataclass
class FundConfig:
    capital: float = 5e9
    allocation: dict[str, float] = field(default_factory=lambda: {
        "systematic_trend": 0.30, "stat_arb": 0.25, "fundamental": 0.25,
        "mirofish_sentiment": 0.18, "hft_market_making": 0.02,
    })
    warmup: int = 60
    costs: CostConfig = field(default_factory=CostConfig)
    trend: TrendConfig = field(default_factory=TrendConfig)
    pairs: PairsConfig = field(default_factory=PairsConfig)
    fundamental: FundamentalConfig = field(default_factory=FundamentalConfig)
    hft: HFTConfig = field(default_factory=HFTConfig)
    sentiment: SentimentConfig = field(default_factory=SentimentConfig)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def load(cls, path: str | Path | None) -> "FundConfig":
        cfg = cls()
        if path:
            _merge(cfg, json.loads(Path(path).read_text()))
        return cfg


def _merge(obj, overrides: dict) -> None:
    names = {f.name for f in fields(obj)}
    for k, v in overrides.items():
        if k not in names:
            raise KeyError(f"unknown setting {type(obj).__name__}.{k}")
        cur = getattr(obj, k)
        if is_dataclass(cur) and isinstance(v, dict):
            _merge(cur, v)
        else:
            setattr(obj, k, v)
