"""Equity ratings instead of trading: a fair value, a trend read and a MiroFish news read per stock.

    fair value  = latest annual EPS (as filed) x the median P/E of the profitable names that day
    upside      = fair value / price - 1
    composite   = 0.5 * value z-score + 0.3 * trend z-score + 0.2 * news z-score
    rating      = Buy (top third of composite), Hold, Sell (bottom third); loss-makers get no
                  fair value and are rated on trend and news only

``evaluate`` checks whether the ratings meant anything: at each month end it rates every stock
with data known that day, then measures the next month's return of Buy minus Sell names and the
rank correlation (IC) between composite and next-month return. An IC near zero means the
ratings are decoration.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .data import BENCHMARK, Fundamentals, Market


def _z(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    sd = s.std()
    return (s - s.mean()) / sd if sd and np.isfinite(sd) else s * 0.0


def rate(market: Market, fund: Fundamentals, i: int, news_score: dict[str, float] | None = None,
         lookback: int = 120) -> pd.DataFrame:
    d = market.sessions[i]
    px = market.close.iloc[i]
    eps = fund.eps_asof(d)
    tickers = [t for t in market.tickers if np.isfinite(px.get(t, np.nan))]
    pe = pd.Series({t: px[t] / eps[t] for t in tickers if t in eps and eps[t] > 0})
    med_pe = float(pe.median()) if len(pe) else float("nan")
    rows = []
    for t in tickers:
        e = eps.get(t)
        fv = e * med_pe if e is not None and e > 0 and np.isfinite(med_pe) else np.nan
        mom = px[t] / market.close[t].iloc[max(0, i - lookback)] - 1 if i >= 20 else np.nan
        rows.append({"ticker": t, "price": px[t], "eps": e, "fair_value": fv,
                     "upside": fv / px[t] - 1 if np.isfinite(fv) else np.nan,
                     "trend": mom, "news": (news_score or {}).get(t, 0.0)})
    df = pd.DataFrame(rows).set_index("ticker")
    v = _z(df["upside"].clip(-1, 2)).fillna(0.0)
    df["composite"] = 0.5 * v + 0.3 * _z(df["trend"]).fillna(0.0) + 0.2 * _z(df["news"]).fillna(0.0)
    q1, q2 = df["composite"].quantile([1 / 3, 2 / 3])
    df["rating"] = np.where(df["composite"] >= q2, "Buy", np.where(df["composite"] <= q1, "Sell", "Hold"))
    df.attrs["median_pe"] = med_pe
    return df.sort_values("composite", ascending=False)


def evaluate(market: Market, fund: Fundamentals, start: int = 60) -> dict:
    ends = [i for i in range(start, len(market.sessions) - 21)
            if market.sessions[i].month != market.sessions[i + 1].month]
    spreads, ics, hits = [], [], []
    for i in ends:
        r = rate(market, fund, i)
        fwd = market.close.iloc[i + 21] / market.close.iloc[i] - 1
        r = r.join(fwd.rename("fwd")).dropna(subset=["fwd"])
        buy, sell = r[r.rating == "Buy"]["fwd"].mean(), r[r.rating == "Sell"]["fwd"].mean()
        spreads.append(buy - sell)
        ics.append(r["composite"].rank().corr(r["fwd"].rank()))
        hits.append(float(buy > r["fwd"].mean()))
    s, ic = pd.Series(spreads), pd.Series(ics)
    return {"months": len(ends), "buy_minus_sell_monthly_mean": float(s.mean()),
            "buy_minus_sell_t_stat": float(s.mean() / s.std() * math.sqrt(len(s))) if s.std() > 0 else 0.0,
            "mean_rank_ic": float(ic.mean()), "ic_positive_months": float((ic > 0).mean()),
            "buy_beat_universe_months": float(np.mean(hits)), "benchmark": BENCHMARK}
