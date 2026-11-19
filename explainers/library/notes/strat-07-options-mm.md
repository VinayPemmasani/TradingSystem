# strat-07-options-mm: Options market making and delta hedging (184.1 s)

Key facts and sources
- Black-Scholes pricing and delta. Source: [Black & Scholes, "The Pricing of Options and Corporate Liabilities", J. Political Economy 81(3), 1973](https://www.journals.uchicago.edu/doi/10.1086/260062).
- The gamma term of the delta-hedged P&L: dΠ ≈ ½ Γ S² (σ²_realized − σ²_implied) dt. Source: [arXiv 2504.15626, eq. 2.8](https://arxiv.org/abs/2504.15626).
- Worked example, computed with Black-Scholes: a 30-day ATM call with S = K = 100, implied vol 20% and zero rates. Price ≈ 2.29, delta ≈ 0.51, gamma ≈ 0.07, one-day breakeven move ≈ S·σ·√(1/252) ≈ $1.26. A hedged long call makes ≈ +8¢ on a $2 day and ≈ −5¢ on a 50¢ day (theta). The 100-call / 5,100-share hedge is illustrative.
- OPRA projected about 12.3 billion messages a day for October 2025 (12.322 billion, one stream). Source: [OPRA Capacity Projections Update, Sept 2025](https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf).
- Lab tie-in: the lab has no options. Its market maker leans quotes by share inventory. The Nasdaq ITCH day 2019-01-30 had 368,366,634 messages (quant-real script.log). The `target = -book_delta_shares` line is labelled as a sketch, and `work_toward` is real (`execution.hpp`).

Unsure / left out: OPRA peak message rates, market-maker spread and volume shares, and exchange fee levels.
