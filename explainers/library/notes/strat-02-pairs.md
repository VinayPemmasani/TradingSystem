# strat-02-pairs: Statistical arbitrage, pairs

Key facts and sources
- The textbook rule: a 12-month formation period on normalised total-return prices (dividends reinvested); each stock is paired with the partner that minimises the sum of squared deviations; the pairs trade for the next 6 months; a pair opens when prices diverge by more than two formation-period standard deviations and closes at the next crossing or at the end of the period. Gatev, Goetzmann & Rouwenhorst, "Pairs Trading: Performance of a Relative-Value Arbitrage Rule", Review of Financial Studies 19(3), 797–827, 2006: https://econpapers.repec.org/RePEc:oup:rfinst:v:19:y:2006:i:3:p:797-827 (NBER w7032 abstract: https://nber.org/papers/w7032). Rule details checked against Skiena's lecture summary https://www3.cs.stonybrook.edu/~skiena/691/lectures/lecture23.pdf and Alpha Architect's summary, not the full RFS text.
- Lab rules (log price ratio, rolling z-score, entry 2.0, exit 0.3 or a zero cross, stop 4.0 with re-arm below 0.3, equal-dollar legs in round lots): /home/claude/ts-push/firm/strategy/include/lab/strategy/pairs.hpp.
- 2019 sample run: GOOGL/GOOG on Nasdaq ITCH 2019-01-30, 1-minute samples, 60-sample window, $300k per leg; 10 round trips, 3 wins, P&L −$1,632.36: /mnt/project-files/quant-real/quant-real.json (pairs) and script.log. A lab replay of one day; not a performance claim.

Unsure / left out
- The paper's return figures are left out on purpose (no performance claims).
- The price paths in the formation, trading and risk scenes are illustrative and seeded, not real data.
- Crowding is mentioned in general terms only. The August 2007 quant unwind (Khandani & Lo) is saved for strat-06.
