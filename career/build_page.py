#!/usr/bin/env python3
"""Fill career/web/index.html with career/results.json and the paper fund equity curve.

    python3 career/head_to_head.py
    python3 career/build_page.py --equity PATH/TO/baseline_5bn/equity.csv --out OUT.html
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--equity", required=True, help="paper fund baseline_5bn/equity.csv")
    ap.add_argument("--out", default=str(HERE / "dist" / "index.html"))
    args = ap.parse_args()

    res = json.loads((HERE / "results.json").read_text())
    rows = [r for r in csv.DictReader(open(args.equity)) if r["date"] >= "2024-12-26"]  # run start
    cols = ["fund", "benchmark", "fundamental", "systematic_trend", "stat_arb"]
    equity = {"date": [r["date"] for r in rows]}
    for c in cols:
        equity[c] = [round(float(r[c]) / 1e6, 2) for r in rows]  # $M

    keep = ("id", "group", "area", "title", "level", "value", "silent", "note", "scales")
    issues = []
    for r in res["issues"]:
        row = {k: r[k] for k in keep if k in r}
        for p in res["profiles"]:
            row[p] = [r[p]["p"], r[p]["minutes"]]
        issues.append(row)
    data = {
        "profiles": {k: {"label": v["label"], "blurb": v["blurb"], "skill": v["skill"]}
                     for k, v in res["profiles"].items()},
        "issues": issues,
        "groups": res["groups"],
        "sweep": res["sweep"],
        "mc": res["monte_carlo"],
        "equity": equity,
    }
    html = (HERE / "web" / "index.html").read_text()
    html = html.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {out} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
