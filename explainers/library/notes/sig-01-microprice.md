# sig-01-microprice: Microprice

Builds on the `signals` video, which defined the size-weighted mid (there called the microprice).

## Key facts and sources
- Micro-price: P^micro = lim P^i, P^i = E[mid at the i-th mid change | book now] = M + Σ g_k(I, S), with g_1 = E[M_τ1 − M | I, S] and g_{i+1} = E[g_i(I_τ1, S_τ1) | I, S]; (M, I, S) Markov, dynamics independent of M. Toy cases: jumps independent of imbalance give M; imbalance as Brownian motion on [0,1], spread 1, gives M + I − 1/2 (the weighted mid). Estimation: bucket imbalance and spread, absorbing Markov chain, g_1 = (1 − Q)^-1 R_1 K, symmetrised data. Stoikov, Quantitative Finance 18(12), 1959-1966, 2018, https://doi.org/10.1080/14697688.2018.1489139 (abstract: https://ideas.repec.org/a/taf/quantf/v18y2018i12p1959-1966.html); slides: https://www.ma.imperial.ac.uk/~ajacquie/Gatheral60/Slides/Gatheral60%20-%20Stoikov.pdf
- "Martingale by construction"; weighted mid "noisy": summary in https://arxiv.org/abs/2507.09734.
- Weighted-mid example (50.00 x 900 / 50.01 x 100, then 50.02 x 2,700): my own numbers.
- Toy model: my own exact solve (value iteration, 160x160 grid; one-tick spread; events add a lot 45% or remove one 55%; empty queue moves mid half a tick, spread refills symmetrically). Top bucket (I 0.8-1.0): g = +0.455 ticks vs weighted mid +0.377. At I = 0.75: 3v1 0.305, 12v4 0.350, 30v10 0.401. Illustrative only.
- Lab: `firm/oms/include/lab/oms/messages.hpp` (TopOfBook sizes), `tools/itch-dump/main.cpp` (`--tob-csv`), `firm/strategy/include/lab/strategy/market_maker.hpp` (anchor). The table-lookup code is a sketch, not in the repo.

## Unsure / left out
- Read via abstract and slides, not the full text; the slide PDF extracted garbled, so its numeric example, exact symmetrisation and sample dates are not used.
