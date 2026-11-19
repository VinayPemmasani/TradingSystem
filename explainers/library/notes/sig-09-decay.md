# sig-09-decay: Signal horizon and decay

Builds on sig-04 (half-life), sig-05 (lead decays) and the `signals` video (latency in backtests).

## Key facts and sources
- IC(h) = corr(s_t, m_{t+h} − m_t). Worked model, computed exactly (not simulated): s_t = 0.9 s_{t−1} + ε, r_{t+1} = 0.1 s_t + e, unit variances. IC = 0.10 at h = 1, peak 0.20 near h = 11, 0.13 at h = 50; half-life ln½ / ln 0.9 = 6.6 steps; 1 − 0.9^10 = 65% of the move done by 10 steps; 2 steps of latency leave 0.9² = 81%. My own model and arithmetic.
- Lagged cross-asset order flow imbalance improves short-horizon return forecasts, and the improvement decays rapidly with horizon. Cont, Cucuringu & Zhang, "Cross-impact of order flow imbalance in equity markets", Quantitative Finance 23(10), 1373-1393, 2023. https://ideas.repec.org/a/taf/quantf/v23y2023i10p1373-1393.html
- Markout example (+0.5, +0.4, +0.3, −0.2, −0.5 ¢ at fill, 1, 10, 100, 1,000 ms): illustrative mids, labelled as such.
- Lab: `research/lab_research/tca.py` (capture vs mid just before; markouts at 1, 10, 100, 1,000 ms); market maker requotes on book changes; pairs on 5-minute samples and trend on daily closes (`tools/quant-lab/main.cpp` header, `pairs.hpp`, `trend.hpp`).

## Unsure / left out
- No market IC values are quoted; real ICs are much smaller and noisier than the toy model.
