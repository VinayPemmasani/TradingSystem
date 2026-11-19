# strat-06-mean-rev: Short-term mean reversion (176.3 s)

Key facts and sources
- The contrarian rule is from Lehmann (1990) and Lo & MacKinlay (1990), as written in Khandani & Lo, eq. 1: ω_i,t = −(1/N)(R_i,t−1 − R_m,t−1), where R_m is the equal-weighted average return of all N stocks. The weights sum to zero, so the book is dollar neutral. Source: [Khandani & Lo, "What Happened to the Quants in August 2007?", J. Investment Management 5(2), 2007](https://web.mit.edu/Alo/www/Papers/august07.html).
- The simulated contrarian strategy's unleveraged daily returns were −1.16% (Aug 7), −2.83% (Aug 8) and −2.86% (Aug 9), then +5.92% (Aug 10, 2007). The paper attributes this to the rapid unwind of a large market-neutral portfolio, magnified by leverage and spread by stop-loss and de-leveraging rules. Same source.
- The worked example (N = 3, returns +4%, +1%, −2%, market +1%) is illustrative. The weights come out at −1%, 0% and +1% of capital.
- Lab tie-in: `pairs.hpp` is mean reversion on one spread. `execution.hpp` has `work_toward(target, position, open_buy, open_sell, max_child, lot)`, which turns a target into bounded child orders.
- The "temporary pressure" price path in the video is illustrative.

Unsure / left out: the paper's leverage multiples and the strategy's long-run return figures (no performance claims), and figures for turnover costs.
