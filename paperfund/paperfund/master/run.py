"""One pass over every model in the project, scored with the same tests.

Three test benches, kept apart because they are different worlds:

- real:  the $5bn paper fund on real daily prices and news (paperfund run + scenarios + tune)
- lab:   the C++ Quant Research Lab on the simulated exchange, many seeds (tools/quant-lab)
- arena: ten archetype funds on one simulated exchange (paperfund arena)

Usage:
  python3 -m paperfund master --real RESULTS_DIR --qlab-bin build/release/tools/quant-lab/quant-lab \
      --arena out/arena/arena.json --out out/master
RESULTS_DIR holds baseline_5bn/, scenarios/, tuning/ and ratings/ from earlier runs.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

from . import stats

SLEEVES = ["systematic_trend", "stat_arb", "fundamental", "mirofish_sentiment", "hft_market_making"]
LAB = {"mm": "Market making (HFT)", "pairs": "Stat arb pairs", "trend": "Trend", "fund": "Fundamental"}


def _returns(real: Path):
    eq = pd.read_csv(real / "baseline_5bn" / "equity.csv", parse_dates=["date"]).set_index("date")
    pnl = pd.read_csv(real / "baseline_5bn" / "daily_pnl.csv", parse_dates=["date"]).set_index("date")
    prev = eq.shift(1).reindex(pnl.index)
    r = pd.DataFrame({s: pnl[f"{s}_pnl"] / prev[s] for s in SLEEVES})
    r["fund"] = pnl["fund_pnl"] / prev["fund"]
    r["qqq"] = eq["benchmark"].pct_change().reindex(pnl.index)
    return r.iloc[1:].fillna(0.0), eq


def _walk_forward(r: pd.DataFrame, lookback=60, every=21):
    """Combine the sleeves using only the past: inverse-volatility weights, monthly."""
    x = r[SLEEVES].to_numpy()
    w = np.full(len(SLEEVES), 1 / len(SLEEVES))
    out = np.zeros(len(x))
    hist = []
    for t in range(len(x)):
        if t >= lookback and t % every == 0:
            vol = x[t - lookback:t].std(axis=0) + 1e-6
            w = (1 / vol) / (1 / vol).sum()
            hist.append({"date": str(r.index[t].date()), "w": [round(float(v), 4) for v in w]})
        out[t] = x[t] @ w
    # scale to the fund's own volatility so the comparison is like for like
    return out * (r["fund"].std() / out.std()), hist


def real_bench(real: Path) -> dict:
    r, eq = _returns(real)
    scen = json.loads((real / "scenarios" / "scenarios.json").read_text())
    tune = json.loads((real / "tuning" / "tuning.json").read_text())
    timing = json.loads((real / "ratings" / "ratings_and_timing.json").read_text())
    base = scen["baseline"]
    fund_trials = [s["fund"]["sharpe"] for s in scen.values()]
    cards = {}
    for s in SLEEVES + ["fund"]:
        trials = [v["sleeves"][s]["sharpe"] for v in scen.values() if s in v.get("sleeves", {})] \
            if s != "fund" else fund_trials
        if s == "mirofish_sentiment":
            trials += [g["in_sample_sharpe"] for g in tune["grid"]]
        cards[s] = stats.scorecard(r[s].to_numpy(), r["qqq"].to_numpy(), trials)
        if s != "fund":
            sl = base["sleeves"][s]
            cards[s].update(pnl=sl["pnl"], costs=sl["costs"], capital=sl["capital"],
                            gross_pnl=sl["pnl"] + sl["costs"], traded=sl["traded"])
    f = base["fund"]
    cards["fund"].update(pnl=f["pnl"], costs=f["costs"], capital=base["capital"], gross_pnl=f["pnl"] + f["costs"])
    cards["qqq"] = stats.scorecard(r["qqq"].to_numpy())
    wf, wf_hist = _walk_forward(r)
    best = max(SLEEVES, key=lambda s: r[s].mean() / (r[s].std() + 1e-12))
    combos = {
        "as_built": stats.scorecard(r["fund"].to_numpy(), r["qqq"].to_numpy(), fund_trials),
        "walk_forward_inverse_vol": stats.scorecard(wf, r["qqq"].to_numpy(), fund_trials),
        "hindsight_best_sleeve": {**stats.scorecard(r[best].to_numpy(), r["qqq"].to_numpy(),
                                                    fund_trials + [cards[s]["sharpe"] for s in SLEEVES]),
                                  "sleeve": best},
    }
    corr = r[SLEEVES + ["qqq"]].corr().round(3)
    sc = {k: {"fund_return": v["fund"]["return"], "fund_sharpe": v["fund"]["sharpe"],
              "sleeves": {n: {"return": x["return"], "sharpe": x["sharpe"]} for n, x in v["sleeves"].items()}}
          for k, v in scen.items()}
    placebo = {k: scen[k]["sleeves"].get("mirofish_sentiment", {}).get("return")
               for k in ("baseline", "placebo_news", "realtime_news")}
    capacity = {k.replace("capacity_", ""): {"return": scen[k]["fund"]["return"],
                                             "sleeves": {n: x["return"] for n, x in scen[k]["sleeves"].items()}}
                for k in scen if k.startswith("capacity_")}
    iso = [g["in_sample_sharpe"] for g in tune["grid"] if not g["placebo"]]
    oos = [g["out_of_sample_sharpe"] for g in tune["grid"] if not g["placebo"]]
    curve = eq.loc[eq.index >= r.index[0] - pd.Timedelta(days=1)]
    step = max(1, len(curve) // 240)
    curve = curve.iloc[::step]
    return {
        "start": base["start"], "end": base["end"], "sessions": base["sessions"], "capital": base["capital"],
        "cards": cards, "combos": combos, "walk_forward_weights": wf_hist[-1] if wf_hist else None,
        "corr": {"keys": list(corr.columns), "m": corr.to_numpy().tolist()},
        "scenarios": sc, "placebo": placebo, "capacity": capacity,
        "tuning": {"split": tune["split"], "chosen": tune["chosen_in_sample"],
                   "is_oos_corr": float(np.corrcoef(iso, oos)[0, 1]), "grid": tune["grid"]},
        "timing": timing,
        "by_exchange": base["by_exchange"],
        "curve": {"dates": [str(d.date()) for d in curve.index],
                  **{c: [round(v / curve[c].iloc[0], 5) for v in curve[c]] for c in SLEEVES + ["fund", "benchmark"]}},
    }


def lab_bench(qlab_bin: str | None, seeds: int, days: int, cache: Path) -> dict:
    cache.mkdir(parents=True, exist_ok=True)
    runs = []
    for s in range(1, seeds + 1):
        p = cache / f"seed{s}.json"
        if not p.exists():
            if not qlab_bin:
                raise SystemExit(f"{p} missing and no --qlab-bin given")
            subprocess.run([qlab_bin, "--days", str(days), "--seed", str(s), "--out", str(p)],
                           check=True, stdout=subprocess.DEVNULL)
        d = json.loads(p.read_text())
        runs.append(d)
    out = {"seeds": seeds, "days": runs[0]["meta"]["days"], "strategies": {}, "integrity": {
        "integrity_errors": sum(d["meta"]["integrity_errors"] for d in runs),
        "book_mismatches": sum(d["meta"]["book_mismatches"] for d in runs),
        "oms_inconsistent": sum(d["meta"]["oms_inconsistent"] for d in runs),
        "messages": sum(d["meta"]["messages"] for d in runs)}}
    for k, name in LAB.items():
        pnls = [d[k]["summary"]["pnl"] for d in runs]
        shs = [d[k]["summary"]["sharpe"] for d in runs]
        wins = sum(p > 0 for p in pnls)
        out["strategies"][k] = {
            "name": name, "pnl": pnls, "sharpe": shs, "wins": wins,
            "median_pnl": float(np.median(pnls)), "p_luck": stats.sign_test_p(wins, len(pnls)),
            "curves": [d[k]["summary"]["daily"][::3] for d in runs],
            "fills": int(np.mean([d[k]["summary"]["fills"] for d in runs])),
        }
    return out


def arena_bench(path: Path) -> dict:
    a = json.loads(path.read_text())
    funds = [{k: f[k] for k in ("key", "name", "style", "capital", "latency", "edge", "trading_pnl", "opex", "net",
                                "ann", "sharpe", "max_dd")} | {"p_net_positive": a["mc"][f["key"]]["p_net_positive"],
                                                               "p_beat_market": a["mc"][f["key"]]["p_beat_market"]}
             for f in a["funds"]]
    return {"years": a["years"], "paths": a["paths"], "main_seed": a["main_seed"], "funds": funds,
            "market": a["market"], "curves": {k: v[::2] for k, v in a["curves"].items()}}


def run(real: Path, qlab_bin: str | None, arena: Path, out: Path, seeds=20, days=252) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    res = {"real": real_bench(real), "lab": lab_bench(qlab_bin, seeds, days, out / "quant-lab"),
           "arena": arena_bench(arena)}
    (out / "master.json").write_text(json.dumps(res, default=float))
    (out / "master.md").write_text(markdown(res))
    return res


def _pct(x):
    return f"{x:+.1%}"


def markdown(res: dict) -> str:
    r = res["real"]
    L = [f"# Master scorecard", "",
         f"## Bench A: real prices, $5bn paper fund ({r['start']} to {r['end']}, {r['sessions']} sessions)", "",
         "| Sleeve | Ann. return | Sharpe | 95% CI | t | P(SR>0) | Deflated SR prob | Beta to QQQ | Alpha t | Costs |",
         "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|"]
    for k in SLEEVES + ["fund", "qqq"]:
        c = r["cards"][k]
        L.append(f"| {k} | {_pct(c['ann_return'])} | {c['sharpe']:.2f} | {c['sharpe_ci95'][0]:.2f} to "
                 f"{c['sharpe_ci95'][1]:.2f} | {c['t_stat']:.2f} | {c['psr']:.0%} | "
                 f"{c['dsr']:.0%} | {c.get('beta', 1):.2f} | {c.get('alpha_t', 0):.2f} | "
                 f"{'$%.0fm' % (c['costs'] / 1e6) if 'costs' in c else ''} |" if 'dsr' in c else
                 f"| {k} | {_pct(c['ann_return'])} | {c['sharpe']:.2f} | {c['sharpe_ci95'][0]:.2f} to "
                 f"{c['sharpe_ci95'][1]:.2f} | {c['t_stat']:.2f} | {c['psr']:.0%} | | 1.00 | | |")
    L += ["", "Combining the sleeves:", ""]
    for k, c in r["combos"].items():
        L.append(f"- {k}: ann {_pct(c['ann_return'])}, Sharpe {c['sharpe']:.2f}, deflated SR prob {c['dsr']:.0%}"
                 + (f" ({c['sleeve']}, chosen after seeing results)" if "sleeve" in c else ""))
    p = r["placebo"]
    L += ["", f"MiroFish sleeve: real news {_pct(p['baseline'])}, placebo (shifted) news {_pct(p['placebo_news'])}, "
          f"real-time fills {_pct(p['realtime_news'])}.",
          f"Tuning: in-sample vs out-of-sample Sharpe correlation {r['tuning']['is_oos_corr']:+.2f}; the setting chosen "
          f"in-sample scored {r['tuning']['chosen']['out_of_sample_sharpe']:+.2f} out of sample.", "",
          f"## Bench B: Quant Research Lab, {res['lab']['seeds']} simulated years on the C++ exchange", "",
          f"Books rebuilt from {res['lab']['integrity']['messages']:,} ITCH messages: "
          f"{res['lab']['integrity']['integrity_errors']} integrity errors, "
          f"{res['lab']['integrity']['book_mismatches']} book mismatches.", "",
          "| Strategy | Years profitable | Median PnL | Median Sharpe | P(luck) |", "|---|---:|---:|---:|---:|"]
    for k, s in res["lab"]["strategies"].items():
        L.append(f"| {s['name']} | {s['wins']}/{len(s['pnl'])} | ${s['median_pnl']:,.0f} | "
                 f"{np.median(s['sharpe']):.2f} | {s['p_luck']:.4f} |")
    a = res["arena"]
    L += ["", f"## Bench C: Fund Arena, {a['years']} years, {a['paths']} alternate histories", "",
          "| Fund | Net | Sharpe | P(net>0) |", "|---|---:|---:|---:|"]
    for f in sorted(a["funds"], key=lambda f: -f["net"]):
        L.append(f"| {f['name']} | ${f['net'] / 1e6:,.0f}m | {f['sharpe']:.2f} | {f['p_net_positive']:.0%} |")
    return "\n".join(L) + "\n"
