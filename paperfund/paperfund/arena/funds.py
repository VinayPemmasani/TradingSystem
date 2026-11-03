"""The funds in the arena: what each one trades, how fast it is, what it costs to run, and the
risk rules it lives by. Archetypes, not real firms. Running costs are estimates."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

YEAR = 252


@dataclass
class Sleeve:
    strategy: str          # value | reversal | trend | news | market
    alloc: float           # share of fund capital
    target_vol: float      # annual volatility target for this sleeve
    max_lev: float = 8.0
    universe: int = 600    # names traded (for market impact)
    adv: float = 300e6     # average daily dollar volume per name


@dataclass
class FundSpec:
    key: str
    name: str
    style: str
    capital: float
    opex: float                    # running cost per year, dollars (estimate)
    fees: str                      # prop | 2/20 | passthrough
    latency: str
    sleeves: list = field(default_factory=list)
    strat_kw: dict = field(default_factory=dict)
    execution: str = "marketable"  # marketable | passive
    micro: dict = field(default_factory=dict)   # lob firm -> (stock-equivalents, venue)
    risk: dict = field(default_factory=dict)
    edge: str = ""
    start_day: int = 0             # days spent building before the first trade
    discovery: dict = field(default_factory=dict)  # signal strength -> probability (new funds)
    color: str = ""


def cast():
    return [
        FundSpec("apex_hft", "Apex HFT", "Colocated market maker", 500e6, 150e6, "prop",
                 "3 µs (FPGA, colocated)", micro={"apex_hft": (400, "main")},
                 risk={"rules": "inventory limit per name, kill switch, no overnight risk"},
                 edge="Fastest quote refresh: first in every new queue, rarely left stale."),
        FundSpec("sniper_arb", "Sniper Arb", "Latency arbitrage", 150e6, 45e6, "prop",
                 "2 µs (microwave + FPGA)", micro={"sniper_arb": (300, "main")},
                 risk={"rules": "hedges every fill at once on another venue; position near zero"},
                 edge="Reads the leading venue first and takes stale quotes before they are pulled."),
        FundSpec("tier2_mm", "Tier-2 Market Maker", "Market maker, second tier", 300e6, 30e6, "prop",
                 "60 µs (software, colocated)", micro={"tier2_mm": (300, "main")},
                 risk={"rules": "inventory limit, wider quotes when losing"},
                 edge="Same strategy as Apex, 20x slower: behind in the queue and often picked off."),
        FundSpec("pod_shop", "Pod Shop", "Multi-manager pods", 20e9, 0.8e9, "passthrough",
                 "~1 ms (broker algos)",
                 sleeves=[Sleeve("value", 0.50, 0.05, universe=4000, adv=150e6),
                          Sleeve("news", 0.20, 0.05, universe=4000, adv=150e6),
                          Sleeve("trend", 0.30, 0.06, universe=80, adv=5e9)],
                 strat_kw={"value_noise": 0.1, "news_q": 0.62},
                 risk={"pod_stop": (-0.05, -0.075), "rules": "pod down 5%: risk halved; down 7.5%: pod cut and replaced"},
                 edge="Many independent pods and strict stops; huge size means heavy market impact."),
        FundSpec("cta_trend", "Trend CTA", "Trend following futures", 5e9, 50e6, "2/20",
                 "seconds (daily rebalancing)",
                 sleeves=[Sleeve("trend", 1.0, 0.12, universe=50, adv=5e9)],
                 risk={"rules": "volatility targeting, no stops; size follows realised volatility"},
                 edge="Rides long trends in five markets; loses in choppy years, shines in crises."),
        FundSpec("value_ls", "Value Long/Short", "Fundamental long/short equity", 3e9, 40e6, "2/20",
                 "days", sleeves=[Sleeve("value", 1.0, 0.08)],
                 risk={"rules": "gross and net limits, holds through drawdowns"},
                 edge="A good estimate of fair value; patient enough to wait for prices to converge."),
        FundSpec("big_bet", "Big Bet Capital", "Concentrated, highly levered", 2e9, 25e6, "2/20",
                 "days", sleeves=[Sleeve("value", 0.8, 0.30, max_lev=25), Sleeve("market", 0.2, 0.18, max_lev=2)],
                 strat_kw={"concentrated": True},
                 risk={"margin_call": -0.40, "rules": "no stops; prime broker liquidates at -40% from peak"},
                 edge="Same insight as Value L/S, ten names and 4x the risk: high reward until margin call."),
        FundSpec("mirofish_fund", "MiroFish Fund (as built)", "Your paper fund from PR #28", 5e9, 60e6, "2/20",
                 "~2 ms (broker DMA), signals at close, fills next open",
                 sleeves=[Sleeve("trend", 0.30, 0.10, universe=50, adv=5e9),
                          Sleeve("reversal", 0.25, 0.05, universe=100, adv=2e9),
                          Sleeve("value", 0.25, 0.08, universe=100, adv=2e9),
                          Sleeve("news", 0.18, 0.04, universe=100, adv=2e9)],
                 strat_kw={"value_noise": 1.5, "reversal_capture": 0.4, "news_q": 0.5, "reversal_hold": 5},
                 micro={"mirofish_fund": (50, "main")},
                 risk={"rules": "per-sleeve vol targets, participation cap; no drawdown stop"},
                 edge="Five sleeves at $5bn with retail-grade data and speed; news read is a coin flip."),
        FundSpec("your_md_fund", "Your Market-Data Fund", "Small fund built on feed expertise", 25e6, 2.4e6, "prop",
                 "25 µs (own feed handlers, one colocated rack)",
                 sleeves=[Sleeve("reversal", 1.0, 0.08, universe=600, adv=300e6)],
                 execution="passive", micro={"your_md_fund": (8, "niche")}, start_day=126,
                 strat_kw={"strength": 0.5}, discovery={0.0: 0.35, 0.5: 0.40, 1.0: 0.25},
                 risk={"daily_stop": -0.02, "dd_halve": -0.08,
                       "rules": "daily loss limit 2%, risk halved at -8%, inventory caps, no news bets"},
                 edge="Fastest firm on a less contested venue, and lead-aware passive execution that "
                      "keeps the spread instead of paying it."),
        FundSpec("your_md_race", "Your Fund, racing HFTs", "Same team, market making on the main venue",
                 25e6, 2.4e6, "prop", "25 µs (8x slower than Apex)",
                 micro={"your_md_fund": (8, "main")}, start_day=126,
                 risk={"rules": "inventory caps; same team and budget as Your Market-Data Fund"},
                 edge="None: third in every race against firms that spend 60x more on speed."),
    ]


def impact(traded, sleeve: Sleeve, vol_d):
    """Square-root market impact as a fraction of dollars traded."""
    per_name = traded / sleeve.universe
    return 0.7 * vol_d * np.sqrt(np.maximum(per_name, 0) / sleeve.adv)


def run_fund(spec: FundSpec, units: dict, reg, micro_pnl, exec_bps):
    """Daily accounting. units: strategy -> (u, turnover). micro_pnl: daily dollars from the order
    book. exec_bps: (marketable, passive) cost per dollar traded in basis points, per regime.
    Returns a dict of daily series."""
    days = len(reg)
    eq = np.zeros(days + 1)
    eq[0] = spec.capital
    gross = np.zeros(days)
    costs = np.zeros(days)
    sleeve_pnl = {s.strategy: np.zeros(days) for s in spec.sleeves}
    lev_hist = {s.strategy: np.ones(days) for s in spec.sleeves}
    mult = {s.strategy: 1.0 for s in spec.sleeves}
    s_hwm = {s.strategy: 0.0 for s in spec.sleeves}
    s_cum = {s.strategy: 0.0 for s in spec.sleeves}
    cut_until = {s.strategy: -1 for s in spec.sleeves}
    events = []
    closed = None
    hwm = spec.capital
    halt_tomorrow = False
    vol_d = np.array([0.016, 0.02, 0.035])
    for d in range(days):
        if d < spec.start_day:
            eq[d + 1] = eq[d]
            continue
        if closed is not None:
            eq[d + 1] = eq[d]
            continue
        cap = eq[d]
        day_g = day_c = 0.0
        if halt_tomorrow:
            halt_tomorrow = False
        else:
            for s in spec.sleeves:
                u, tau = units[s.strategy]
                lo = max(0, d - 60)
                hist = u[lo:d] if d - lo >= 20 else u[:60]
                rv = hist.std() * np.sqrt(YEAR) + 1e-9
                lev = min(s.target_vol / rv, s.max_lev) * mult[s.strategy]
                if d < cut_until[s.strategy]:
                    lev = 0.0
                lev_hist[s.strategy][d] = lev
                book = cap * s.alloc * lev
                g = book * u[d]
                traded = book * tau[d]
                bps = exec_bps[1 if spec.execution == "passive" else 0][reg[d]]
                if s.strategy == "trend":
                    bps = 0.5  # futures: about a quarter of a tick
                imp = impact(traded, s, vol_d[reg[d]]) * (0.5 if spec.execution == "passive" else 1.0)
                c = traded * (bps * 1e-4 + imp)
                day_g += g
                day_c += c
                sleeve_pnl[s.strategy][d] = g - c
                # pod rules
                if "pod_stop" in spec.risk:
                    half, cut = spec.risk["pod_stop"]
                    s_cum[s.strategy] += (g - c) / (spec.capital * s.alloc)
                    s_hwm[s.strategy] = max(s_hwm[s.strategy], s_cum[s.strategy])
                    dd = s_cum[s.strategy] - s_hwm[s.strategy]
                    if dd <= cut and d >= cut_until[s.strategy]:
                        cut_until[s.strategy] = d + 20
                        s_hwm[s.strategy] = s_cum[s.strategy]
                        mult[s.strategy] = 1.0
                        events.append((d, f"{s.strategy} pod cut at {dd:.1%}"))
                    elif dd <= half and mult[s.strategy] == 1.0:
                        mult[s.strategy] = 0.5
                        events.append((d, f"{s.strategy} pod risk halved at {dd:.1%}"))
                    elif dd > half / 2:
                        mult[s.strategy] = 1.0
        mp = micro_pnl[d] if micro_pnl is not None else 0.0
        gross[d] = day_g + mp
        costs[d] = day_c
        eq[d + 1] = cap + day_g - day_c + mp
        hwm = max(hwm, eq[d + 1])
        dd = eq[d + 1] / hwm - 1
        if "margin_call" in spec.risk and dd <= spec.risk["margin_call"]:
            fire = eq[d + 1] * 0.08  # forced selling into a falling market
            eq[d + 1] -= fire
            costs[d] += fire
            closed = d
            events.append((d, f"margin call at {dd:.0%}: forced liquidation, fund closed"))
        if "daily_stop" in spec.risk and (eq[d + 1] / cap - 1) <= spec.risk["daily_stop"]:
            halt_tomorrow = True
            events.append((d, "daily loss limit hit: flat for a day"))
        if "dd_halve" in spec.risk:
            for s in spec.sleeves:
                mult[s.strategy] = 0.5 if dd <= spec.risk["dd_halve"] else 1.0
    return {"equity": eq, "gross": gross, "costs": costs, "sleeves": sleeve_pnl,
            "events": events, "closed": closed, "lev": lev_hist}


def fees_and_net(spec: FundSpec, res, years):
    """Running costs and, for outside-capital funds, fees. Net PnL = trading PnL - running costs."""
    pnl = res["equity"][-1] - res["equity"][0]
    opex = spec.opex * years if res["closed"] is None else spec.opex * (res["closed"] + 1) / YEAR
    if spec.fees == "prop":
        fees = 0.0
    else:
        eq = res["equity"]
        days = len(eq) - 1
        fees = 0.0
        hwm = eq[0]
        mgmt = 0.02 if spec.fees == "2/20" else spec.opex / spec.capital
        for y in range(int(np.ceil(days / YEAR))):
            a, b = y * YEAR, min((y + 1) * YEAR, days)
            fees += mgmt * eq[a] * (b - a) / YEAR
            if eq[b] > hwm:
                fees += 0.2 * (eq[b] - hwm)
                hwm = eq[b]
    return {"trading_pnl": pnl, "opex": opex, "net": pnl - opex, "fees": fees,
            "investor_pnl": pnl - fees if spec.fees != "prop" else None}
