"""Markdown summary of an arena run."""


def _m(x):
    return f"${x / 1e6:,.0f}m" if abs(x) >= 1e6 else f"${x / 1e3:,.0f}k"


def markdown(res):
    y = res["years"]
    lines = [f"# Arena: {len(res['funds'])} funds, one exchange, {y} simulated years",
             "",
             f"Simulation only; rival funds are archetypes, not real firms. Main history = the most "
             f"typical of {res['paths']} (seed {res['main_seed']}). Running costs are estimates.",
             "",
             "| Fund | Capital | Trading PnL | Running costs | Net | Ann. return | Sharpe | Max DD | "
             "P(net > 0) | P(beat market) |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for f in sorted(res["funds"], key=lambda f: -f["net"]):
        mc = res["mc"][f["key"]]
        lines.append(f"| {f['name']} | {_m(f['capital'])} | {_m(f['trading_pnl'])} | {_m(f['opex'])} | "
                     f"**{_m(f['net'])}** | {f['ann']:+.1%} | {f['sharpe']:.2f} | {f['max_dd']:.1%} | "
                     f"{mc['p_net_positive']:.0%} | {mc['p_beat_market']:.0%} |")
    m = res["market"]
    lines.append(f"| Market (buy and hold) | | | | | {m['ann']:+.1%} | {m['sharpe']:.2f} | {m['max_dd']:.1%} | | |")
    eb = res["lob"]["exec_bps"]
    lines += ["", f"Execution cost per dollar traded (calm / choppy / crisis): marketable "
              f"{eb[0][0]:.2f} / {eb[0][1]:.2f} / {eb[0][2]:.2f} bp; lead-aware passive "
              f"{eb[1][0]:.2f} / {eb[1][1]:.2f} / {eb[1][2]:.2f} bp."]
    return "\n".join(lines) + "\n"
