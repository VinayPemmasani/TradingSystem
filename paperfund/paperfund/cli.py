"""python -m paperfund {demo,run,scenarios}"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from . import report
from .config import FundConfig
from .data import Fundamentals, Market, load_jsonl
from .engine import PaperFund
from .scenarios import make_signals, mirofish_tuning, run_all
from .sentiment import combine_news


def _inputs(a):
    if a.cmd == "demo":
        from . import synthetic
        bars, news, eps = synthetic.world(a.days)
        return Market(bars), news, Fundamentals(eps.assign(available=pd.to_datetime(eps["available"]).dt.date))
    m = Market.from_csv(a.prices)
    news = combine_news(*(load_jsonl(p) for p in (a.news or []) + (a.reddit or [])))
    f = Fundamentals.from_csv(a.fundamentals) if a.fundamentals else None
    return m, news, f


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="paperfund", description="$5B paper fund. Simulation only.")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("demo", "run", "scenarios", "tune"):
        s = sub.add_parser(name)
        s.add_argument("--out", default=f"out/{name}")
        s.add_argument("--config")
        s.add_argument("--capital", type=float)
        s.add_argument("--seeds", type=int, default=4, help="swarm seeds per signal (MiroFish uses 16)")
        if name == "demo":
            s.add_argument("--days", type=int, default=320)
        else:
            s.add_argument("--prices", required=True)
            s.add_argument("--news", nargs="*")
            s.add_argument("--reddit", nargs="*")
            s.add_argument("--fundamentals")
        if name == "scenarios":
            s.add_argument("--only", nargs="*")
            s.add_argument("--no-robustness", action="store_true")
    ar = sub.add_parser("arena", help="rival archetype funds on one simulated exchange")
    ar.add_argument("--out", default="out/arena")
    ar.add_argument("--years", type=int, default=5)
    ar.add_argument("--paths", type=int, default=200)
    ar.add_argument("--lob-days", type=int, default=40, help="order-book days simulated per regime")
    ar.add_argument("--seed", type=int, default=11)
    a = p.parse_args(argv)
    if a.cmd == "arena":
        from .arena import report as arena_report
        from .arena.run import run as arena_run
        res = arena_run(a.out, a.years, a.paths, a.lob_days, a.seed)
        print(arena_report.markdown(res))
        Path(a.out, "arena.md").write_text(arena_report.markdown(res))
        return 0
    cfg = FundConfig.load(a.config)
    if a.capital:
        cfg.capital = a.capital
    market, news, fund = _inputs(a)
    out = Path(a.out)
    if a.cmd == "tune":
        res = mirofish_tuning(market, news, cfg, a.seeds)
        out.mkdir(parents=True, exist_ok=True)
        (out / "tuning.json").write_text(json.dumps(res, indent=2, default=float))
        print(f"split at {res['split']}")
        for r in res["grid"]:
            print(f"{r['filter']:7s} entry {r['entry']:.2f} {'placebo' if r['placebo'] else 'real   '} "
                  f"in-sample sharpe {r['in_sample_sharpe']:+.2f}  out-of-sample {r['out_of_sample_sharpe']:+.2f}")
        b = res["chosen_in_sample"]
        print(f"chosen on in-sample: {b['filter']} entry {b['entry']} -> out-of-sample sharpe "
              f"{b['out_of_sample_sharpe']:+.2f}")
        return 0
    if a.cmd == "scenarios":
        res = run_all(market, news, fund, cfg, a.seeds, a.only, not a.no_robustness)
        out.mkdir(parents=True, exist_ok=True)
        (out / "scenarios.json").write_text(json.dumps(res, indent=2, default=float))
        for k, s in res.items():
            f = s["fund"]
            print(f"{k:28s} fund {f['pnl'] / 1e6:12,.1f}m  ret {f['return']:+7.2%}  sharpe {f['sharpe']:5.2f}  "
                  + "  ".join(f"{n[:10]} {v['return']:+.2%}" for n, v in s["sleeves"].items()))
        return 0
    sig = make_signals(market, news, cfg, a.seeds)
    res = PaperFund(market, cfg, sig, fund).run()
    s = report.write(res, out, "Paper Fund demo (synthetic market)" if a.cmd == "demo" else "Paper Fund run")
    print(report.markdown(s))
    return 0
