# sig-04-ewma: EWMA, VWAP and online features

Builds on the `signals` video (time-decayed α = 1 − e^(−Δt/τ)); the sliding-window VWAP lives in the cpp-vwap video.

## Key facts and sources
- EWMA m ← m + α(x − m); half-life in updates h = ln½ / ln(1 − α). pandas `ewm`: span N gives α = 2/(N+1); halflife h gives α = 1 − exp(−ln2/h). https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
- Exponentially weighted variance recurrence (diff, incr, mean += incr, var = (1 − α)(var + diff·incr)). Tony Finch, "Incremental calculation of weighted mean and variance", 2009. https://fanf2.user.srcf.net/hermes/doc/antiforgery/stats.tex
- Worked Finch example (α = 0.25, prints 50.00, 50.02, 50.01, 50.05: z = 5.6 before update, 1.6 after) and VWAP example (300@50.00, 100@50.04, 600@50.02 → 50.016; mid 50.05 is +6.8 bps): my own arithmetic.
- τ = h / ln2: 1 s half-life → τ = 1.44 s; Δt = 0.5 s gives α = 1 − e^(−0.5/1.44) ≈ 0.29 (old mean keeps √½ ≈ 71%). My own arithmetic.
- Lab: `exchange/agents/main.cpp` (fast/slow EWMA α 0.3 / 0.03 → half-lives 1.94 / 22.8 trades); `firm/strategy/.../trend.hpp` (SMA 20 / 50; span-matched α 0.095 / 0.039); `firm/strategy/.../pairs.hpp` (156-sample window, running sum and sum of squares).

## Unsure / left out
- RiskMetrics' 0.94 decay factor is not quoted (no primary source read).
- "Span-matched" α for an SMA is the usual centre-of-mass match, not an exact equivalence.
