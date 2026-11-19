# sig-05-lead-lag: Lead-lag, futures lead cash

Builds on the `signals` video (futures as a leading signal) and sig-04 (returns, decay).

## Key facts and sources
- S&P 500 and MMI futures returns lead stock index returns by about 5 minutes on average (occasionally 10+), with weaker feedback the other way, after purging bid/ask and infrequent-trading effects. Stoll & Whaley, "The dynamics of stock index and stock index futures returns", JFQA 25(4), 441-468, 1990. https://ideas.repec.org/a/cup/jfinqa/v25y1990i04p441-468_00.html
- Most price discovery for the S&P 500 and Nasdaq-100 takes place in the E-mini futures. Hasbrouck, "Intraday price formation in U.S. equity index markets", Journal of Finance 58(6), 2375-2400, 2003. https://ideas.repec.org/a/bla/jfinan/v58y2003i6p2375-2400.html
- ES vs SPY, 2011: return correlation 0.0073 (1 ms), 0.0923 (10 ms), 0.6879 (1 s), 0.9798 (1 min); median arbitrage duration 97 ms (2005) to 7 ms (2011). Budish, Cramton & Shim, "The high-frequency trading arms race", QJE 2015. https://conference.nber.org/conf_papers/f69665.pdf
- Simulation (20,000 steps, c = 0.1f + 0.3f(−1) + 0.6f(−2) + noise): ρ(k) peaks 0.71 at lag 2; regression recovers 0.30 and 0.60. My own.
- Lab: `exchange/agents/main.cpp` `--strip NAME=A+B` (strip value = sum of legs); `tools/itch-dump`.

## Unsure / left out
- Epps effect: not named; sources I found were inconsistent on direction.
- The 0.6-point fair-value move is from my simulation's weights, not any market.
