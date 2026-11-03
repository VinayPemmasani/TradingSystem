"""Turn a Result into numbers people can check: per strategy, per day, per exchange."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .engine import Result


def series_stats(eq: pd.Series, capital: float) -> dict:
    eq = eq.dropna()
    if len(eq) < 2 or capital <= 0:
        return {"pnl": 0.0, "return": 0.0, "ann_return": 0.0, "ann_vol": 0.0, "sharpe": 0.0,
                "max_drawdown": 0.0, "up_days": 0.0}
    r = eq.diff().dropna() / capital  # daily PnL as a share of allocated capital
    days = len(r)
    ann_ret = r.mean() * 252
    ann_vol = r.std() * math.sqrt(252)
    path = 1.0 + (eq - eq.iloc[0]) / capital
    dd = (path / path.cummax() - 1.0).min()
    return {"pnl": float(eq.iloc[-1] - eq.iloc[0]), "return": float((eq.iloc[-1] - eq.iloc[0]) / capital),
            "ann_return": float(ann_ret), "ann_vol": float(ann_vol),
            "sharpe": float(ann_ret / ann_vol) if ann_vol > 0 else 0.0,
            "max_drawdown": float(dd), "up_days": float((r > 0).mean()), "days": days}


def summary(res: Result) -> dict:
    w = res.cfg.warmup
    eq = res.equity.iloc[w:]
    caps = {k: res.cfg.capital * v for k, v in _alloc(res).items()}
    out = {"capital": res.cfg.capital, "start": str(eq.index[0]), "end": str(eq.index[-1]),
           "sessions": len(eq), "sleeves": {}, "notes": res.notes, "stats": res.stats}
    pnl = res.pnl[pd.to_datetime(res.pnl["date"]) >= pd.Timestamp(eq.index[0])]
    for k, cap in caps.items():
        st = series_stats(eq[k], cap)
        sub = pnl[pnl["sleeve"] == k]
        st.update({"capital": cap, "costs": float(sub["cost"].sum()),
                   "traded": float(sub["traded"].sum())})
        out["sleeves"][k] = st
    out["fund"] = series_stats(eq["fund"], res.cfg.capital)
    out["fund"]["costs"] = float(pnl["cost"].sum())
    out["benchmark_qqq"] = series_stats(eq["benchmark"], res.cfg.capital)
    out["by_exchange"] = {ex: float(v) for ex, v in pnl.groupby("exchange")["pnl"].sum().items()}
    out["by_sleeve_exchange"] = {f"{s}|{ex}": float(v) for (s, ex), v in
                                 pnl.groupby(["sleeve", "exchange"])["pnl"].sum().items()}
    return out


def _alloc(res: Result) -> dict[str, float]:
    cols = [c for c in res.equity.columns if c not in ("fund", "benchmark")]
    first = res.equity.iloc[0]
    tot = sum(first[c] for c in cols)
    return {c: first[c] / tot for c in cols}


def daily_table(res: Result) -> pd.DataFrame:
    eq = res.equity.iloc[res.cfg.warmup - 1:] if res.cfg.warmup > 0 else res.equity
    d = eq.drop(columns=["benchmark"]).diff().iloc[1:]
    d.columns = [f"{c}_pnl" for c in d.columns]
    d["fund_equity"] = eq["fund"].iloc[1:]
    ex = res.pnl.pivot_table(index="date", columns="exchange", values="pnl", aggfunc="sum").fillna(0.0)
    ex.columns = [f"{c}_pnl" for c in ex.columns]
    return d.join(ex, how="left").fillna(0.0)


def _money(x: float) -> str:
    sign = "-" if x < 0 else ""
    x = abs(x)
    for unit, div in (("bn", 1e9), ("m", 1e6), ("k", 1e3)):
        if x >= div:
            return f"{sign}${x / div:,.2f}{unit}"
    return f"{sign}${x:,.0f}"


def markdown(s: dict, title: str = "Paper Fund run") -> str:
    lines = [f"# {title}", "",
             f"{_money(s['capital'])} of pretend capital, {s['start']} to {s['end']} "
             f"({s['sessions']} sessions). Simulation only; no order was sent anywhere.", "",
             "| Sleeve | Capital | PnL | Return | Ann. return | Sharpe | Max DD | Costs |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for k, v in s["sleeves"].items():
        lines.append(f"| {k} | {_money(v['capital'])} | {_money(v['pnl'])} | {v['return']:+.2%} | "
                     f"{v['ann_return']:+.2%} | {v['sharpe']:.2f} | {v['max_drawdown']:.1%} | "
                     f"{_money(v['costs'])} |")
    f, b = s["fund"], s["benchmark_qqq"]
    lines += [f"| **Fund** | {_money(s['capital'])} | **{_money(f['pnl'])}** | {f['return']:+.2%} | "
              f"{f['ann_return']:+.2%} | {f['sharpe']:.2f} | {f['max_drawdown']:.1%} | {_money(f['costs'])} |",
              f"| QQQ buy and hold | {_money(s['capital'])} | {_money(b['pnl'])} | {b['return']:+.2%} | "
              f"{b['ann_return']:+.2%} | {b['sharpe']:.2f} | {b['max_drawdown']:.1%} | |", "",
              "PnL by listing exchange: " + ", ".join(f"{k} {_money(v)}" for k, v in s["by_exchange"].items()),
              ""]
    st = s["stats"]
    lines.append(f"Internally crossed between sleeves: {_money(st['internally_crossed_notional'])}; "
                 f"left unfilled by the {st['participation_cap_hits']} participation-cap hits: "
                 f"{_money(st['unfilled_notional'])}.")
    for n in s["notes"]:
        lines.append(f"- Note: {n}")
    return "\n".join(lines) + "\n"


def write(res: Result, out: str | Path, title: str = "Paper Fund run") -> dict:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    s = summary(res)
    (out / "summary.json").write_text(json.dumps(s, indent=2, default=float))
    (out / "report.md").write_text(markdown(s, title))
    daily_table(res).to_csv(out / "daily_pnl.csv", float_format="%.2f")
    res.equity.to_csv(out / "equity.csv", float_format="%.2f")
    res.by("sleeve", "exchange").to_csv(out / "pnl_by_sleeve_exchange.csv", float_format="%.2f")
    res.by("sleeve", "ticker").to_csv(out / "pnl_by_sleeve_ticker.csv", float_format="%.2f")
    return s


def nan_safe(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else x
