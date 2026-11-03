"""A daily world for the slower funds: a stock universe and four macro markets, with known
sources of return so each strategy's edge (or lack of one) is explicit. Simulation only.

Stock return = beta * market + change in mispricing M (slow, mean-reverting: what value funds
trade) + change in flow pressure S (fast, mean-reverting: what reversal / stat arb trades)
+ news jumps (70% on the day, 30% drifts over the next five days: what news funds trade)
+ noise. Market regimes: 0 calm bull, 1 choppy, 2 crisis. Crowding events push every crowded
value / reversal book the wrong way for four days, then half of it comes back (August 2007).
"""

from __future__ import annotations

import numpy as np

REG_DRIFT = np.array([0.0006, 0.0000, -0.0022])
REG_VOL = np.array([0.008, 0.011, 0.027])
REG_P = np.array([[0.993, 0.006, 0.001],
                  [0.008, 0.986, 0.006],
                  [0.012, 0.028, 0.960]])
YEAR = 252


def regimes(days, rng):
    r = np.zeros(days, dtype=int)
    for d in range(1, days):
        r[d] = rng.choice(3, p=REG_P[r[d - 1]])
    return r


def simulate(days, rng, n=60, crowding_rate=0.25):
    reg = regimes(days, rng)
    mkt = REG_DRIFT[reg] + REG_VOL[reg] * rng.standard_normal(days)
    # four macro markets (bonds, commodities, currencies, rates) with persistent trends
    macro = np.zeros((days, 4))
    s = rng.choice([-1, 1], 4)
    for d in range(days):
        flip = rng.random(4) < 1 / 220
        s = np.where(flip, -s, s)
        crisis = reg[d] == 2
        drift = 0.00045 * s + np.array([0.0006, 0, 0, 0.0004]) * crisis
        macro[d] = drift + 0.0065 * (1 + crisis) * rng.standard_normal(4)
    beta = rng.uniform(0.7, 1.3, n)
    idio = 0.012
    M = np.zeros((days + 1, n))
    S = np.zeros((days + 1, n))
    M[0] = rng.normal(0, 0.013, n)
    for d in range(days):
        M[d + 1] = 0.985 * M[d] + rng.normal(0, 0.0019, n)
        S[d + 1] = 0.4 * S[d] + rng.normal(0, 0.0038, n)
    dM = np.diff(M, axis=0)
    dS = np.diff(S, axis=0)
    news_hit = rng.random((days, n)) < 0.02
    J = np.where(news_hit, rng.normal(0, 0.04, (days, n)), 0.0)
    drift = np.zeros((days + 6, n))
    for k in range(1, 6):
        drift[k:days + k] += 0.06 * J
    r = beta * mkt[:, None] + dM + dS + 0.7 * J + drift[:days] + idio * rng.standard_normal((days, n))
    # crowding events
    events = []
    n_ev = rng.poisson(crowding_rate * days / YEAR)
    for d0 in sorted(rng.integers(60, max(61, days - 20), n_ev)):
        z = -M[d0] + 0.5 * (-S[d0])
        z = (z - z.mean()) / (z.std() + 1e-12)
        for k in range(4):
            r[d0 + k] -= 0.006 * z
        for k in range(4, 14):
            r[d0 + k] += 0.006 * z * 4 * 0.5 / 10
        events.append(int(d0))
    return {"reg": reg, "mkt": mkt, "macro": macro, "r": r, "M": M[1:], "S": S[1:], "dS": dS,
            "J": J, "beta": beta, "crowd": events}


def _norm(w):
    g = np.abs(w).sum(axis=-1, keepdims=True)
    return np.divide(w, g, out=np.zeros_like(w), where=g > 0)


def _demean(x):
    return x - x.mean(axis=-1, keepdims=True)


def unit_returns(w, r):
    """w[d] decided at close d, earns r[d+1]. Returns per-day return and turnover."""
    u = np.zeros(len(r))
    u[1:] = (w[:-1] * r[1:]).sum(axis=1)
    tau = np.zeros(len(r))
    tau[1:] = np.abs(np.diff(w, axis=0)).sum(axis=1)
    tau[0] = np.abs(w[0]).sum()
    return u, tau


def hold(w, every):
    out = w.copy()
    for d in range(len(w)):
        if d % every:
            out[d] = out[d - 1]
    return out


def strategies(world, rng, value_noise=0.4, reversal_capture=1.0, news_q=0.5, concentrated=False,
               reversal_hold=1, strength=1.0):
    """Unit (gross 1) strategy books and their daily returns. Each returns (u, turnover)."""
    r, M, beta = world["r"], world["M"], world["beta"]
    days, n = r.shape
    resid = r - beta * world["mkt"][:, None]
    out = {}
    # value: a noisy view of the mispricing, weekly
    Mhat = M + rng.normal(0, value_noise * 0.013, M.shape) * 1.0
    noise_persist = np.zeros_like(Mhat)
    e = rng.normal(0, value_noise * 0.013, n)
    for d in range(days):  # analyst errors persist; they are not fresh every day
        e = 0.98 * e + np.sqrt(1 - 0.98 ** 2) * rng.normal(0, value_noise * 0.013, n)
        noise_persist[d] = e
    Mhat = M + noise_persist
    sig = _demean(-Mhat)
    if concentrated:
        cut = np.quantile(sig, [0.1, 0.9], axis=1)
        sig = np.where((sig <= cut[0][:, None]) | (sig >= cut[1][:, None]), sig, 0.0)
    w = hold(_norm(sig), 5)
    out["value"] = unit_returns(w, r)
    # short-term reversal on residual returns, daily; capture < 1 for fills at the next open
    w = _norm(_demean(-resid))
    if strength < 1.0:
        # a weaker signal than the true one: part of each day's book is random picks, with the
        # same turnover, so the edge shrinks but the trading costs do not
        junk = _norm(_demean(rng.standard_normal(w.shape)))
        w = _norm(strength * w + (1 - strength) * junk)
    w = hold(w, reversal_hold)
    u, tau = unit_returns(w, r)
    lost = np.zeros(days)
    lost[1:] = (w[:-1] * world["dS"][1:]).sum(axis=1) * (1 - reversal_capture)
    out["reversal"] = (u - lost, tau)
    # trend on the equity market and four macro markets, 126-day sign, inverse-vol weights
    assets = np.column_stack([world["mkt"], world["macro"]])
    cum = np.cumsum(assets, axis=0)
    w = np.zeros_like(assets)
    for d in range(126, days):
        mom = cum[d] - cum[d - 126]
        vol = assets[d - 60:d].std(axis=0) + 1e-9
        w[d] = np.sign(mom) / vol
    w = hold(_norm(w), 5)
    out["trend"] = unit_returns(w, assets)
    # news: trade the five-day drift after news; q is the chance the read is the right way
    J = world["J"]
    w = np.zeros_like(r)
    for d in range(days):
        hit = J[d] != 0
        if hit.any():
            right = rng.random(n) < news_q
            sgn = np.where(right, np.sign(J[d]), -np.sign(J[d]))
            for k in range(0, 5):
                if d + k < days:
                    w[d + k] += np.where(hit, sgn, 0.0)
    out["news"] = unit_returns(_norm(w), r)
    out["market"] = (world["mkt"].copy(), np.zeros(days))
    return out
