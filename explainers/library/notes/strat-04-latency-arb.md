# strat-04-latency-arb: Latency arbitrage (182.2 s)

Key facts and sources
- The ES/SPY correlation of equal-weighted midpoint returns (median, 2011) falls with the interval: 0.0073 at 1 ms, 0.0923 at 10 ms, 0.4622 at 100 ms, 0.6879 at 1 s, 0.9057 at 10 s and 0.9798 at 1 min. Source: [Budish, Cramton & Shim, "The High-Frequency Trading Arms Race", QJE 130(4), 2015](https://academic.oup.com/qje/article/130/4/1547/1916146), working version [NBER conference PDF](https://conference.nber.org/conf_papers/f69665.pdf).
- The median duration of an ES-SPY arbitrage opportunity fell from 97 ms in 2005 to 7 ms in 2011. Same source.
- The Chicago to New York round trip was about 16 ms on fibre before, 13 ms on the newer fibre route, and 10, then 9, then 8.5 ms on microwave. Light needs about 4 ms each way. Same source.
- In the model, a stale quote is sniped by N fast traders and each wins with probability 1/N. The expected sniping cost is built into the spread, and the proposed fix is frequent batch auctions. The "every 100 ms" interval is only an example. Same source.
- Lab tie-in: `firm/trader/order_entry.cpp` records tick_to_wire with `lab::rdtsc()` after `sock_.send`. The rx thread stamps each packet with rdtsc. The lab has no cross-venue sniper, and the video says so.

Unsure / left out: the paper's dollar estimates of arbitrage profits (I could not re-check the exact figures and units), exchange fee levels, and any figures for current link latencies.
