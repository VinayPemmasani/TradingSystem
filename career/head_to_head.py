#!/usr/bin/env python3
"""Head to head: a quant dev/researcher against a veteran market data developer.

Both profiles work the same 82 issues the project has already built:

  * MD-413 (3 reports) and MD-414 (11 reports): the release incidents on the
    interview branches, the same ones the seven candidates worked;
  * MD-415: the 60 planted bugs of the bug bank (interview/md-415-bank);
  * PF: 8 research problems the paper fund run found (PR #28, results in
    /mnt/project-files/paperfund/results), with dollar figures taken from that run.

A profile is a skill level from 0 to 1 in nine areas. An issue has a difficulty
and weights over the areas. The chance a profile solves an issue is a logistic
curve of (weighted skill - difficulty); time to solve scales the time Priya, the
strongest replayed candidate, took on the same MD-415 bug. Value at stake is the
loss avoided (or gain made) over the paper fund's 463-session window.

The skill levels and incident dollar figures are assumptions, written out below
so anyone can change them; the paper fund dollar figures are measured. Run:

    python3 career/head_to_head.py            # writes career/results.json
"""

from __future__ import annotations

import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
AREAS = [
    "cpp",  # C++, memory, concurrency, low-latency engineering
    "protocols",  # feed and order-entry protocols, exchange rules
    "network",  # UDP/TCP, multicast, kernel and NIC tuning
    "data_quality",  # book integrity, reconciliation, vendor checks
    "trading_core",  # OMS, risk checks, matching
    "finance",  # PnL, positions, corporate actions, accounting
    "stats",  # statistics, hypothesis tests, overfitting, ML
    "portfolio",  # sizing, risk budgets, correlation, drawdown control
    "execution",  # costs, market impact, capacity, TCA
]

PROFILES = {
    "quant": {
        "label": "Quant dev/researcher",
        "blurb": "6 years at a systematic fund; Nasdaq, NYSE and CME only; strong statistics,"
        " Python and C++ to production standard, never run a feed handler at scale.",
        "skill": dict(cpp=0.60, protocols=0.45, network=0.40, data_quality=0.55,
                      trading_core=0.70, finance=0.85, stats=0.90, portfolio=0.85,
                      execution=0.75),
    },
    "mdev": {
        "label": "Market data veteran",
        "blurb": "15 years, 40-50 feeds across equities, futures, FX, options and fixed income;"
        " every production incident there is; no strategy or research experience.",
        "skill": dict(cpp=0.95, protocols=0.97, network=0.92, data_quality=0.95,
                      trading_core=0.65, finance=0.45, stats=0.25, portfolio=0.20,
                      execution=0.45),
    },
    "mdev_plus": {
        "label": "Market data veteran after the course",
        "blurb": "The same person after the 16-week course and a year applying it on the job.",
        "skill": dict(cpp=0.95, protocols=0.97, network=0.92, data_quality=0.95,
                      trading_core=0.75, finance=0.70, stats=0.62, portfolio=0.58,
                      execution=0.72),
    },
}

LEVEL_DIFFICULTY = {"easy": 0.30, "medium": 0.50, "hard": 0.70}
# Loss avoided when an MD-415 bug is found before it costs money; a silent bug
# (no existing check fails) runs longer in production, so it costs three times as much.
LEVEL_VALUE = {"easy": 50_000, "medium": 250_000, "hard": 1_000_000}
AREA_WEIGHTS = {
    "cpp": dict(cpp=0.7, data_quality=0.3),
    "md": dict(protocols=0.6, data_quality=0.4),
    "net": dict(network=0.7, cpp=0.3),
    "lat": dict(cpp=0.5, network=0.5),
    "trd": dict(trading_core=0.6, finance=0.2, cpp=0.2),
    "gw": dict(protocols=0.6, trading_core=0.4),
}

# MD-413 and MD-414 reports (INTERVIEW.md on interview/md-413-exercise and md-414-exercise).
INCIDENTS = [
    ("MD-413.1", "Full-day replay finds unknown order refs (OrderMap wrap)", "hard",
     dict(cpp=0.6, data_quality=0.4), 1_000_000, 95),
    ("MD-413.2", "EOD report prints 16.600 for 16.06", "easy",
     dict(data_quality=0.7, protocols=0.3), 200_000, 15),
    ("MD-413.3", "PnL off but reconciliation says clean", "medium",
     dict(finance=0.5, data_quality=0.5), 500_000, 40),
    ("MD-414.1", "Full-day replay never finishes", "medium",
     dict(cpp=0.7, data_quality=0.3), 300_000, 45),
    ("MD-414.2", "Volume high on auction days (non-printable executions)", "medium",
     dict(protocols=0.7, data_quality=0.3), 500_000, 30),
    ("MD-414.3", "$4.5M order passes a $100k notional limit", "medium",
     dict(trading_core=0.7, cpp=0.3), 10_000_000, 35),
    ("MD-414.4", "Order burst after the lunch lull gets throttled", "medium",
     dict(trading_core=0.6, protocols=0.4), 500_000, 30),
    ("MD-414.5", "Orders sent during LULD pause; phantom position limit", "hard",
     dict(protocols=0.5, trading_core=0.5), 1_000_000, 60),
    ("MD-414.6", "Fill rate down, replaces up 3x (queue position)", "medium",
     dict(protocols=0.4, trading_core=0.3, execution=0.3), 2_000_000, 40),
    ("MD-414.7", "FIRM01 self-trades despite self-match prevention", "hard",
     dict(trading_core=0.7, protocols=0.3), 2_000_000, 70),
    ("MD-414.8", "Report PnL disagrees with risk (marks)", "medium",
     dict(finance=0.6, data_quality=0.4), 300_000, 35),
    ("MD-414.9", "FIX client missing two execution reports after a blip", "hard",
     dict(protocols=0.7, network=0.3), 1_000_000, 60),
    ("MD-414.10", "simex fills disagree with the replayed book", "medium",
     dict(trading_core=0.6, data_quality=0.4), 500_000, 30),
    ("MD-414.11", "Latency report better but colo p99 worse", "hard",
     dict(cpp=0.5, network=0.3, stats=0.2), 1_000_000, 70),
]

# Paper fund research problems. Dollar figures come from the paper fund run
# (baseline_5bn/summary.json, scenarios/scenarios.txt, tuning/tuning.txt).
RESEARCH = [
    ("PF.1", "Real news does no better than placebo news: there is no edge", "hard",
     dict(stats=0.8, finance=0.2), 437_646_685, 240,
     "Fund -$437.6M with real news, -$443.3M with news shifted 20 days. Spotting this before"
     " launch avoids the whole loss."),
    ("PF.2", "Tuned on the past: in-sample Sharpe +0.43 became -2.81 out of sample", "hard",
     dict(stats=0.9, portfolio=0.1), 247_800_000, 180,
     "Dropping the loss makers after seeing results looks like +$247.8M. It is hindsight;"
     " allocating on it repeats the loss."),
    ("PF.3", "Fundamental sleeve fell 37% with no risk budget", "medium",
     dict(portfolio=0.8, finance=0.2), 206_600_000, 120,
     "Sleeve lost $331.6M; a 10% drawdown stop and vol targeting cap it near $125M."),
    ("PF.4", "Costs of $184.7M on $91bn traded", "medium",
     dict(execution=0.7, stats=0.3), 74_000_000, 120,
     "Lower turnover and better execution cut about 40% of costs."),
    ("PF.5", "Half the news move is gone before the daily fill: should we go faster?", "hard",
     dict(stats=0.6, data_quality=0.2, protocols=0.2), 65_460_000, 90,
     "Running the same signal on real-time news lost $65.5M more. Speed only pays once the"
     " signal works; the right call is not to build it yet."),
    ("PF.6", "HFT sleeve is not co-located: -9.18% that becomes +11.02%", "medium",
     dict(cpp=0.3, network=0.4, protocols=0.3), 20_200_000, 160,
     "The co-located scenario turns the $100M sleeve from -$9.2M to +$11.0M."),
    ("PF.7", "Trend sleeve is too big for its capacity", "medium",
     dict(execution=0.6, stats=0.4), 50_000_000, 90,
     "Trend makes +3.15% at $10M and -0.18% at $1.5bn; right-sizing is worth about $50M."),
    ("PF.8", "Find a real, tradable edge (Sharpe 1 at 5% vol)", "hard",
     dict(stats=0.6, portfolio=0.2, execution=0.1, data_quality=0.1), 458_000_000, 2400,
     "Sharpe 1 at 5% vol on $5bn for 463 sessions. Most researchers never find one."),
]
# PF.8 is harder than its level says: finding alpha is rare even for good researchers.
EXTRA_DIFFICULTY = {"PF.8": 0.22}
# Issues whose value does not grow with fund size (fixed cost or capacity-limited).
FIXED_VALUE = {"PF.6"}

SLOPE = 9.0
CAPITAL = 5_000_000_000


def build_issues() -> list[dict]:
    issues = []
    for i in INCIDENTS:
        iid, title, level, w, value, minutes = i
        issues.append(dict(id=iid, group="incident", title=title, level=level, weights=w,
                           value=value, base_min=minutes, scales=False, note=""))
    for b in json.loads((HERE / "md415_bugs.json").read_text()):
        value = LEVEL_VALUE[b["level"]] * (3 if b["silent"] else 1)
        issues.append(dict(id=b["id"], group="bugbank", area=b["area"], title=b["title"],
                           level=b["level"], weights=AREA_WEIGHTS[b["area"]], value=value,
                           base_min=b["priya_min"], scales=False, silent=b["silent"], note=""))
    for r in RESEARCH:
        iid, title, level, w, value, minutes, note = r
        issues.append(dict(id=iid, group="research", title=title, level=level, weights=w,
                           value=value, base_min=minutes, scales=iid not in FIXED_VALUE,
                           note=note))
    return issues


def skill_on(profile: dict, weights: dict) -> float:
    return sum(profile["skill"][a] * w for a, w in weights.items()) / sum(weights.values())


def p_solve(profile: dict, issue: dict) -> float:
    d = LEVEL_DIFFICULTY[issue["level"]] + EXTRA_DIFFICULTY.get(issue["id"], 0.0)
    return 1.0 / (1.0 + math.exp(-SLOPE * (skill_on(profile, issue["weights"]) - d)))


def minutes(profile: dict, issue: dict) -> float:
    # Priya's replays sit at about 0.9 skill; time grows with the square of the shortfall.
    s = max(skill_on(profile, issue["weights"]), 0.05)
    return issue["base_min"] * (0.9 / s) ** 2


def value_at(issue: dict, capital: float) -> float:
    return issue["value"] * (capital / CAPITAL if issue["scales"] else 1.0)


def main() -> None:
    issues = build_issues()
    rng = random.Random(413)
    out = {"profiles": PROFILES, "areas": AREAS, "issues": [], "groups": {}, "sweep": [],
           "monte_carlo": {}}

    for iss in issues:
        row = {k: v for k, v in iss.items() if k != "weights"}
        row["weights"] = iss["weights"]
        for key, prof in PROFILES.items():
            p = p_solve(prof, iss)
            row[key] = dict(skill=round(skill_on(prof, iss["weights"]), 3), p=round(p, 3),
                            minutes=round(minutes(prof, iss)),
                            ev=round(p * iss["value"]))
        out["issues"].append(row)

    for group in ("incident", "bugbank", "research"):
        g = [r for r in out["issues"] if r["group"] == group]
        out["groups"][group] = {
            key: dict(expected_solved=round(sum(r[key]["p"] for r in g), 1),
                      count=len(g),
                      hours=round(sum(r[key]["minutes"] for r in g) / 60, 1),
                      ev=round(sum(r[key]["ev"] for r in g)),
                      at_stake=sum(r["value"] for r in g))
            for key in PROFILES
        }
        team = sum(max(r["quant"]["p"], r["mdev"]["p"]) * r["value"] for r in g)
        out["groups"][group]["team"] = dict(ev=round(team))

    # Capital sweep: where does each profile bring more value?
    for cap in (25e6, 50e6, 100e6, 250e6, 500e6, 1e9, 2e9, 5e9, 10e9, 20e9):
        row = {"capital": cap}
        for key, prof in PROFILES.items():
            row[key] = round(sum(p_solve(prof, i) * value_at(i, cap) for i in issues))
        row["team"] = round(sum(max(p_solve(PROFILES["quant"], i), p_solve(PROFILES["mdev"], i))
                                * value_at(i, cap) for i in issues))
        out["sweep"].append(row)

    # Monte Carlo: each issue solved or not, 20,000 times, to show the spread of outcomes.
    trials = 20_000
    for key, prof in PROFILES.items():
        ps = [(p_solve(prof, i), i["value"], i["group"]) for i in issues]
        totals, infra, research = [], [], []
        for _ in range(trials):
            t_inf = t_res = 0.0
            for p, v, g in ps:
                if rng.random() < p:
                    if g == "research":
                        t_res += v
                    else:
                        t_inf += v
            infra.append(t_inf)
            research.append(t_res)
            totals.append(t_inf + t_res)
        totals.sort()
        q = lambda xs, f: round(sorted(xs)[int(f * (len(xs) - 1))])
        bins = [0] * 30
        top = 1.6e9
        for t in totals:
            bins[min(int(t / top * 30), 29)] += 1
        out["monte_carlo"][key] = dict(
            mean=round(statistics.fmean(totals)), p10=q(totals, 0.10), p50=q(totals, 0.50),
            p90=q(totals, 0.90), infra_mean=round(statistics.fmean(infra)),
            infra_sd=round(statistics.pstdev(infra)),
            research_mean=round(statistics.fmean(research)),
            research_sd=round(statistics.pstdev(research)),
            hist=bins, hist_top=top)
    # Share of trials where the quant beats the veteran on total value.
    out["notes"] = [
        "Skill levels and incident dollar values are assumptions; paper fund dollar values are"
        " measured from PR #28's run.",
        "Value is loss avoided or gain made over the paper fund's 463 sessions at $5bn.",
    ]
    (HERE / "results.json").write_text(json.dumps(out, indent=1))

    for group, g in out["groups"].items():
        print(f"{group:9s}", "  ".join(
            f"{k}: solved {v['expected_solved']}/{v['count']} {v['hours']}h ${v['ev']/1e6:,.1f}M"
            for k, v in g.items() if k != "team"), f" team ${g['team']['ev']/1e6:,.1f}M")
    for row in out["sweep"]:
        print(f"capital ${row['capital']/1e6:>8,.0f}M  quant ${row['quant']/1e6:7.1f}M"
              f"  mdev ${row['mdev']/1e6:7.1f}M  mdev+ ${row['mdev_plus']/1e6:7.1f}M"
              f"  team ${row['team']/1e6:7.1f}M")
    for k, v in out["monte_carlo"].items():
        print(k, {x: v[x] for x in ("mean", "p10", "p50", "p90", "infra_mean", "research_mean")})


if __name__ == "__main__":
    main()
