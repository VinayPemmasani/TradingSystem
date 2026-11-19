# sig-02-imbalance: Order book imbalance

Builds on the `signals` video (I = Qb/(Qb+Qa)) and sig-01 (toy queue model).

## Key facts and sources
- Queue imbalance ρ = (Qb − Qa)/(Qb + Qa) at the best quotes; logistic regression of next mid-move direction on imbalance; LOBSTER Nasdaq data, 10 liquid stocks, 2014; statistically significant for all stocks; improvement "considerable" for large-tick stocks, "moderate" for small-tick. Gould & Bonart, "Queue imbalance as a one-tick-ahead price predictor in a limit order book" (arXiv 1512.03492, 2015). https://arxiv.org/abs/1512.03492
- Imbalance predicts the sign of the next market order and the next price move; strategies using it earn more, mostly by reducing adverse selection; 11 Nasdaq stocks, 2014 (first half fit, second half out of sample). Cartea, Donnelly & Jaimungal, "Enhancing trading strategies with order book signals", Applied Mathematical Finance 25(1), 1-35, 2018. https://ideas.repec.org/a/taf/apmtfi/v25y2018i1p1-35.html
- Worked example (slope ≈ 4.0, ρ = 0.5 gives 0.88): my own logistic fit to the sig-01 toy model, not market data.
- Lab: `firm/oms/include/lab/oms/messages.hpp` (TopOfBook, 2 levels per side); `firm/strategy/.../market_maker.hpp` (`others()` removes own price, not own size); `research/lab_research/backtest.py` (`quote()`). The lean-a-tick rule is a sketch, not in the repo.

## Unsure / left out
- Gould & Bonart's exact accuracy/improvement percentages are not quoted; only the qualitative large-tick vs small-tick contrast.
- No claim about profit size from CDJ beyond the direction of the effect.
