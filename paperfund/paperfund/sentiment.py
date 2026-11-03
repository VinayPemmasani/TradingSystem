"""MiroFish signals for the fund: the sentiment forum, the trader swarm and the decision rule.

This reuses ``mirofish/mirofish_trader`` unchanged. Each session, after the
close, the day's news (and Reddit posts) go through the forum and aggregator;
every ticker with a signal gets a swarm forecast anchored on today's observed
move; ``decide`` fuses them into an alpha and a target weight.

``delay`` shifts every item later by that many sessions. With a large delay the
news no longer lines up with the prices, so it is the placebo test: whatever
the sentiment sleeve earns then is luck or market drift, not news.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from . import data  # noqa: F401  (puts mirofish on sys.path)
from mirofish_trader.config import Config as MFConfig  # noqa: E402
from mirofish_trader.decision import decide  # noqa: E402
from mirofish_trader.ingest.news import bucket_by_session  # noqa: E402
from mirofish_trader.models import NewsItem  # noqa: E402
from mirofish_trader.pipeline import FORWARD_SESSIONS, Pipeline, busday  # noqa: E402

NY = ZoneInfo("America/New_York")
OPEN = time(9, 30)

# Press-release feeds are mostly noise for trading: promotions, third-party releases that name a
# big company to borrow its attention, ETF launches and law-firm adverts. ``clean`` drops those;
# ``events`` keeps only items about results, guidance, deals, regulation and other hard events.
_SPAM = re.compile(r"thinking about (buying|trading)|\betf(s)?\b|investors? (are )?reminded|"
                   r"shareholder (alert|deadline)|class action|securities (fraud|action)|"
                   r"lawsuit filed|deadline|weeklypay|research highlights|should you buy|"
                   r"buybacks|dow jones (industrial|sustainability)|index (review|rebalanc)", re.I)
_EVENT = re.compile(r"results|earnings|revenue|guidance|outlook|forecast|quarter|dividend|"
                    r"buyback|repurchase|acqui|merger|to buy|deal|agreement|approv|fda|recall|"
                    r"investigation|antitrust|tariff|export|layoff|job cuts|ceo|resign|appoint|"
                    r"downgrade|upgrade|price target|record", re.I)


def filter_news(items: list[NewsItem], mode: str) -> list[NewsItem]:
    if mode == "all":
        return items
    out = [i for i in items if not _SPAM.search(i.headline)]
    if mode == "events":
        out = [i for i in out if _EVENT.search(i.headline)]
    return out


@dataclass
class Signal:
    ticker: str
    alpha: float  # fused sentiment + swarm view, roughly -1..1
    target_weight: float  # MiroFish's own sizing, fraction of capital
    horizon: int
    premarket: bool  # first item for the ticker arrived before today's open


class MiroFishSignals:
    def __init__(self, news: list[NewsItem], market, delay: int = 0, mf_cfg: MFConfig | None = None,
                 swarm_seeds: int | None = None, news_filter: str = "all"):
        news = filter_news(news, news_filter)
        self.cfg = mf_cfg or MFConfig()
        if swarm_seeds:
            self.cfg.swarm.seeds = swarm_seeds
        self.pipe = Pipeline(self.cfg)
        self.mf_market = market.to_mirofish()
        sessions = market.sessions
        raw = bucket_by_session(news, sessions)
        pos = {d: i for i, d in enumerate(sessions)}
        self.buckets: dict[date, list[NewsItem]] = {}
        for d, items in raw.items():
            j = pos[d] + delay
            if 0 <= j < len(sessions):
                self.buckets.setdefault(sessions[j], []).extend(items)
        self.delay = delay
        self.items_used = sum(len(v) for v in self.buckets.values())

    def warm(self, d: date) -> None:
        """Learn buzz baselines and novelty memory without trading."""
        items = self.buckets.get(d, [])
        self.pipe.aggregator.aggregate(d, [a for it in items for a in self.pipe.forum.assess(it)])

    def signals(self, d: date) -> dict[str, Signal]:
        pipe, mkt = self.pipe, self.mf_market
        pipe.calibrator.mature(d, mkt.forward_idio)
        items = self.buckets.get(d, [])
        assessments = [a for it in items for a in pipe.forum.assess(it)]
        sigs = pipe.aggregator.aggregate(d, assessments)
        out = {}
        for t, sig in sigs.items():
            if mkt.px_close(t, d) is None:
                continue
            fc = pipe.swarm.run(sig, observed_move=mkt.idio_return(t, d))
            feats = (fc.continuation, fc.gap)
            fc.calibrated_return = pipe.calibrator.apply(feats)
            start = busday(d, 1)
            pipe.calibrator.add_forecast(start, busday(start, FORWARD_SESSIONS - 1), t, feats)
            dec = decide(sig, fc, mkt.daily_vol(t, d), self.cfg.decision)
            first = min((a.item.ts for a in sig.direct_items), default=None)
            pre = bool(first and (first.astimezone(NY).date() < d or first.astimezone(NY).time() < OPEN))
            out[t] = Signal(t, dec.alpha, dec.target_weight, max(1, sig.horizon_days), pre)
        return out


def combine_news(*lists: list[NewsItem]) -> list[NewsItem]:
    seen, out = set(), []
    for lst in lists:
        for it in lst:
            if it.id not in seen:
                seen.add(it.id)
                out.append(it)
    return sorted(out, key=lambda i: i.ts)


def stamp(d: date, hh: int, mm: int) -> datetime:
    return datetime.combine(d, time(hh, mm), NY)
