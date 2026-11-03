"""Run the arena: an order-book library per regime, one five-year main history, and many
alternate histories. Writes arena.json for the page. Simulation only."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from . import lob, world
from .funds import YEAR, cast, fees_and_net, run_fund

PRICE = 100.0  # dollars per share in the order book


def lob_library(days_per_regime, rng, record=True):
    """Simulate order-book days in each regime. Returns per-firm daily PnL samples, execution
    costs (marketable vs passive, bps), race and queue statistics, and recorded episodes."""
    lib = {r: defaultdict(list) for r in range(3)}
    niche = {r: defaultdict(list) for r in range(3)}
    exec_m = {r: [] for r in range(3)}
    exec_p = {r: [] for r in range(3)}
    fill_vol = defaultdict(float)
    front = defaultdict(float)
    transfer = defaultdict(float)
    picked = defaultdict(float)
    maker_vol = defaultdict(float)
    episodes = None
    for r in range(3):
        for i in range(days_per_regime):
            rec = 40 if (record and r == 1 and i == 0) else 0
            sim, pnl = lob.simulate_day(r, rng, flow={"slow_funds": (120, 1)},
                                        passive={"your_exec": 20000}, record_jumps=rec)
            if rec:
                episodes = sim.log
            for k, v in pnl.items():
                if v is not None:
                    lib[r][k].append(v)
            c, _ = lob.exec_cost(sim, "slow_funds", 1)
            exec_m[r].append(c)
            c, _ = lob.exec_cost(sim, "your_exec", 1)
            exec_p[r].append(c)
            for maker, taker, n, rank, g in lob.markouts(sim):
                fill_vol[maker] += n
                front[maker] += n * (rank == 0)
                transfer[(maker, taker)] += g
                if taker in ("sniper_arb", "informed"):
                    picked[maker] += n
                maker_vol[maker] += n
            for (t, maker, taker, s, price, n, rank) in sim.fills:
                fill_vol["taker:" + taker] += n
            sim2, pnl2 = lob.simulate_day(r, rng, niche=True)
            for k, v in pnl2.items():
                if v is not None:
                    niche[r][k].append(v)
    n_days = 3 * days_per_regime
    to_bps = 100.0 / PRICE  # ticks per share -> bps of $100
    stats = {
        "exec_bps": [[float(np.mean(exec_m[r])) * to_bps for r in range(3)],
                     [float(np.mean(exec_p[r])) * to_bps for r in range(3)]],
        "makers": {m: {"shares_per_day": fill_vol[m] / n_days,
                       "front_of_queue": front[m] / max(fill_vol[m], 1),
                       "picked_off": picked[m] / max(maker_vol[m], 1)}
                   for m in maker_vol if m != "background"},
        "takers": {k[6:]: v / n_days for k, v in fill_vol.items() if k.startswith("taker:")},
        "transfer": [[a, b, v / n_days] for (a, b), v in transfer.items()],
        "pnl_by_regime": {r: {k: [float(np.mean(v)), float(np.std(v))] for k, v in lib[r].items()}
                          for r in range(3)},
        "niche_by_regime": {r: {k: [float(np.mean(v)), float(np.std(v))] for k, v in niche[r].items()}
                            for r in range(3)},
    }
    return lib, niche, stats, episodes


def micro_series(spec, reg, lib, niche, rng):
    if not spec.micro:
        return None
    out = np.zeros(len(reg))
    for firm, (mult, venue) in spec.micro.items():
        src = lib if venue == "main" else niche
        for d, r in enumerate(reg):
            samples = src[r][firm]
            out[d] += mult * samples[rng.integers(len(samples))]
    return out


def metrics(eq):
    r = eq[1:] / eq[:-1] - 1
    r = r[np.isfinite(r)]
    years = len(r) / YEAR
    total = eq[-1] / eq[0] - 1
    ann = (1 + total) ** (1 / years) - 1 if total > -1 else -1.0
    vol = r.std() * np.sqrt(YEAR)
    down = r[r < 0].std() * np.sqrt(YEAR) if (r < 0).any() else 1e-9
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    # longest time under water
    under = longest = 0
    for x in dd:
        under = under + 1 if x < 0 else 0
        longest = max(longest, under)
    mean = r.mean() * YEAR
    return {"total": total, "ann": ann, "vol": vol, "sharpe": mean / vol if vol > 0 else 0.0,
            "sortino": mean / down, "max_dd": float(dd.min()), "worst_day": float(r.min()),
            "var99": float(-np.quantile(r, 0.01)), "skew": float(((r - r.mean()) ** 3).mean() / (r.std() ** 3 + 1e-18)),
            "losing_days": float((r < 0).mean()), "longest_dd_days": int(longest)}


def one_history(seed, days, lib, niche, exec_bps, draw_discovery=False):
    """One alternate history. With draw_discovery, a new fund's signal strength is drawn from its
    discovery odds (most new strategies turn out weaker than the backtest)."""
    rng = np.random.default_rng(seed)
    w = world.simulate(days, rng)
    units_cache = {}
    out = {}
    for spec in cast():
        kw = dict(spec.strat_kw)
        if draw_discovery and spec.discovery:
            levels = list(spec.discovery)
            kw["strength"] = float(rng.choice(levels, p=list(spec.discovery.values())))
        key = json.dumps(kw, sort_keys=True)
        if key not in units_cache:
            units_cache[key] = world.strategies(w, np.random.default_rng(seed * 7 + 1), **kw)
        micro = micro_series(spec, w["reg"], lib, niche, rng)
        res = run_fund(spec, units_cache[key], w["reg"], micro, exec_bps)
        if micro is not None:
            micro[:spec.start_day] = 0.0
        res["micro"] = micro
        res["strength"] = kw.get("strength")
        out[spec.key] = res
    mkt_eq = 5e9 * np.concatenate([[1], np.cumprod(1 + w["mkt"])])
    return w, out, mkt_eq


def run(out_dir, years=5, paths=200, lob_days=40, seed=11):
    rng = np.random.default_rng(seed)
    lib, niche, lstats, episodes = lob_library(lob_days, rng)
    exec_bps = lstats["exec_bps"]
    days = years * YEAR
    specs = {s.key: s for s in cast()}
    # alternate histories
    mc = defaultdict(lambda: defaultdict(list))
    path_rets = []
    for p in range(paths):
        wp, res, meq = one_history(1000 + p, days, lib, niche, exec_bps, draw_discovery=True)
        mret = meq[-1] / meq[0] - 1
        for k, r in res.items():
            spec = specs[k]
            eq = r["equity"]
            f = fees_and_net(spec, r, years)
            mc[k]["ret"].append(eq[-1] / eq[0] - 1)
            mc[k]["net"].append(f["net"])
            mc[k]["beat_mkt"].append(eq[-1] / eq[0] - 1 > mret)
            mc[k]["blowup"].append(r["closed"] is not None or eq.min() / spec.capital < 0.5)
            yr = eq[::YEAR]
            # first year in which cumulative trading PnL covers cumulative running costs
            be = None
            for y in range(1, len(yr)):
                if yr[y] - spec.capital >= spec.opex * y:
                    be = y
                    break
            mc[k]["breakeven_year"].append(be)
            if r["strength"] is not None:
                mc[k]["by_strength"].append((r["strength"], eq[-1] / eq[0] - 1, f["net"]))
            if len(eq) > 3 * YEAR:
                m3 = metrics(eq[:3 * YEAR + 1])
                mc[k]["sharpe3"].append(m3["sharpe"])
        mc["market"]["ret"].append(mret)
        path_rets.append([res[k]["equity"][-1] / specs[k].capital - 1 for k in res] + [mret])
    # the main history shown on the page is the most typical one: closest to the median
    # outcome of every fund and the market across all histories (rank distance)
    P = np.array(path_rets)
    ranks = P.argsort(axis=0).argsort(axis=0) / (len(P) - 1)
    best = int(np.abs(ranks - 0.5).mean(axis=1).argmin())
    main_seed = 1000 + best
    w, main, mkt_eq = one_history(main_seed, days, lib, niche, exec_bps, draw_discovery=True)
    table = []
    curves = {}
    step = 5
    for k, res in main.items():
        spec = specs[k]
        m = metrics(res["equity"])
        f = fees_and_net(spec, res, years)
        sleeves = {s: float(v.sum()) for s, v in res["sleeves"].items()}
        if res["micro"] is not None:
            sleeves["order_book"] = float(res["micro"].sum())
        table.append({"key": k, "name": spec.name, "style": spec.style, "capital": spec.capital,
                      "latency": spec.latency, "edge": spec.edge, "risk_rules": spec.risk.get("rules", ""),
                      "costs": float(res["costs"].sum()), "sleeves": sleeves, "events": res["events"][:12],
                      "n_events": len(res["events"]), "closed_day": res["closed"],
                      "signal_strength": res["strength"], **m, **f})
        curves[k] = (res["equity"][::step] / spec.capital).round(4).tolist()
    mm = metrics(mkt_eq)
    curves["market"] = (mkt_eq[::step] / mkt_eq[0]).round(4).tolist()
    # correlation of daily returns
    keys = list(main) + ["market"]
    R = []
    for k in keys:
        eq = main[k]["equity"] if k != "market" else mkt_eq
        R.append(eq[1:] / eq[:-1] - 1)
    corr = np.corrcoef(np.array(R)).round(2).tolist()
    mcs = {}
    for k, v in mc.items():
        ret = np.array(v["ret"])
        d = {"p5": float(np.quantile(ret, 0.05)), "p50": float(np.median(ret)),
             "p95": float(np.quantile(ret, 0.95)), "p_positive": float((ret > 0).mean()),
             "hist": np.histogram(np.clip(ret, -1, 3), bins=40, range=(-1, 3))[0].tolist()}
        if k != "market":
            net = np.array(v["net"])
            be = [x for x in v["breakeven_year"] if x is not None]
            d.update({"p_beat_market": float(np.mean(v["beat_mkt"])),
                      "p_blowup": float(np.mean(v["blowup"])),
                      "net_p50": float(np.median(net)), "p_net_positive": float((net > 0).mean()),
                      "p_breakeven_5y": len(be) / paths,
                      "breakeven_years": np.bincount(be, minlength=years + 1).tolist() if be else [],
                      "p_sharpe3_above_1": float((np.array(v["sharpe3"]) > 1).mean())})
            if v["by_strength"]:
                bs = defaultdict(list)
                for st, rt, nt in v["by_strength"]:
                    bs[st].append((rt, nt))
                d["by_strength"] = {str(st): {"n": len(x), "ret_p50": float(np.median([a for a, _ in x])),
                                              "net_p50": float(np.median([b for _, b in x])),
                                              "p_net_positive": float(np.mean([b > 0 for _, b in x]))}
                                    for st, x in sorted(bs.items())}
        mcs[k] = d
    ep = select_episodes(episodes)
    out = {"years": years, "paths": paths, "main_seed": main_seed, "lob_days": 3 * lob_days, "step_days": step,
           "regimes": w["reg"][::step].tolist(), "crowding_days": w["crowd"],
           "market": mm, "funds": table, "curves": curves, "corr_keys": keys, "corr": corr,
           "lob": lstats, "episodes": ep, "mc": mcs,
           "micro_multipliers": {k: s.micro for k, s in specs.items() if s.micro},
           "regime_share": np.bincount(w["reg"], minlength=3).tolist()}
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "arena.json").write_text(json.dumps(out, default=_js))
    return out


def _js(x):
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, tuple):
        return list(x)
    raise TypeError(type(x))


def select_episodes(log, n=3):
    """Cut the recorded log into per-jump windows and keep the most instructive ones: a stale
    quote picked off, a quote pulled in time, and a queue race after a jump."""
    if not log:
        return []
    windows = []
    cur = None
    for e in log:
        if e["kind"] in ("lead", "jump") and (cur is None or e["t"] - cur["t0"] > 4000):
            cur = {"t0": e["t"], "events": []}
            windows.append(cur)
        if cur is not None:
            cur["events"].append(e)
    picked = []
    def has(win, pred):
        return any(pred(e) for e in win["events"])
    snipe = [w for w in windows if has(w, lambda e: e["kind"] == "trade" and e["who"] == "sniper_arb"
                                       and any(f[0] in ("tier2_mm", "mirofish_fund", "your_md_fund") for f in e["detail"]["fills"]))]
    saved = [w for w in windows if has(w, lambda e: e["kind"] == "pull" and e["who"] == "your_md_fund")
             and has(w, lambda e: e["kind"] == "jump")]
    race = [w for w in windows if has(w, lambda e: e["kind"] == "trade" and e["who"] in ("retail", "slow_funds", "informed"))
            and has(w, lambda e: e["kind"] == "jump")]
    for tag, lst in (("picked_off", snipe), ("pulled_in_time", saved), ("queue_race", race)):
        if lst:
            w = max(lst, key=lambda w: len(w["events"]))
            t0 = w["events"][0]["t"]
            evs = [dict(e, t=round(e["t"] - t0, 1)) for e in w["events"][:60]]
            picked.append({"tag": tag, "events": evs})
    return picked
