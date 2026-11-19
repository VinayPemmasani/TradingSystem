# sig-07-queue: Queue position and fill probability

Builds on the `signals` video (queue position from order-level data) and sig-02 (queue imbalance).

## Key facts and sources
- Queue position has value; for some large-tick stocks it can be of the same order of magnitude as the bid-ask spread. Moallemi & Yuan, "A model for queue position valuation in a limit order book", 2016. https://drupalgsb-test.paas.cc.columbia.edu/sites/default/files-efs/pubfiles/25461/queue-value-2016.pdf
- Order book as queues with random limit orders, market orders and cancellations; computes conditional probabilities such as an order at the bid executing before the ask moves. Cont, Stoikov & Talreja, "A stochastic model for order book dynamics", Operations Research 58(3), 549-563, 2010. https://ideas.repec.org/a/inm/oropre/v58y2010i3p549-563.html
- Worked example: 600 back in a 1,000-share bid; 200 trade, level shows 700, so 100 cancelled; pro rata 60 of them ahead; ahead = 600 − 200 − 60 = 340 (moved up 260); at 50 shares/s about 7 s. My own numbers, using the backtest's pro-rata rule.
- Lab: `research/lab_research/backtest.py` (`_Side.update()`: traded shares come off the front, other shrinkage removed pro rata; fill when traded > ahead); `firm/strategy/.../market_maker.hpp` (`hold_ticks`, replace only if the quote moves more than hold_ticks ticks); `research/README.md` (sweep `--hold-ticks 0 1 2`).

## Unsure / left out
- No fill probabilities or queue values from either paper are quoted as numbers.
- The pro-rata cancel rule is the backtest's assumption, flagged on screen as a guess.
