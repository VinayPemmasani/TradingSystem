# strat-05-trend: Trend following and CTAs (185.4 s)

Key facts and sources
- The time series momentum rule: for each of 58 liquid futures (equity indices, currencies, commodities, bonds), go long for one month if the past 12-month return is positive and short if it is negative. Returns persist for 1 to 12 months and partly reverse over longer horizons. The authors call this "consistent with sentiment theories of initial under-reaction and delayed over-reaction". Source: [Moskowitz, Ooi & Pedersen, "Time Series Momentum", JFE 104(2), 2012](https://fairmodel.econ.yale.edu/ec439/jpde.pdf), also on [SSRN 2089463](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463).
- Sizing: each position is 40% / σ_ex-ante. σ² is 261 × an EWMA of squared daily returns, with a centre of mass of 60 days (eq. 1). Same source. The 20% and 80% volatility examples are illustrative.
- CTA (commodity trading advisor) definition: [NFA, who has to register as a CTA](https://www.nfa.futures.org/registration-membership/who-has-to-register/cta.html).
- Lab tie-in: `firm/strategy/include/lab/strategy/trend.hpp` uses a 20/50-day SMA crossover on $1M notional, rounded to lots of 100. On real QQQ daily bars for 2019 in quant-real, closes went from 154.88 to 212.61. The run started the year short, flipped 5 times, ended at -$20,135 with a max drawdown of -$202,700, and whipsawed in May and August. The video labels this a lab backtest, not a performance claim.
- The whipsaw, reversal and trend paths in the video are illustrative.

Unsure / left out: the paper's Sharpe ratios and return figures (no performance claims), CTA industry size, and roll and margin cost figures.
