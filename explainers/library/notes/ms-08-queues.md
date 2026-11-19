# ms-08-queues: Queue dynamics at a price level

## Key facts and sources
- Moallemi & Yuan, "A model for queue position valuation in a limit order book" (Dec 2016, rev. Jun 2017): static (spread vs adverse selection, adverse selection rises with queue position) + dynamic value; for some large-tick stocks queue value can be the same order of magnitude as the bid-ask spread; BAC (Aug 2013 Nasdaq ITCH) front vs average-queue value gap ≈ 0.21–0.26 ticks. https://drupalgsb-test.paas.cc.columbia.edu/sites/default/files-efs/pubfiles/25461/queue-value-2016.pdf
- Lab: libs/match/include/lab/match/engine.hpp (price-time; a replace loses time priority); firm/strategy/.../market_maker.hpp hold_ticks = 1 ("every replace goes to the back of the queue"); ITCH A/E/X/D carry order references.
- Imbalance link: sig-02 (Gould & Bonart).

## Worked numbers (mine)
- Bid 30.00 holds 5,000; join 100; 1,500 traded + 2,000 cancelled ahead → 1,500 ahead, 400 behind; sweep 2,000 = 1,500 + 100 + 400; bid → 29.99.

## Unsure / left out
- "Changing price or adding size usually sends you to the back" is general exchange practice, hedged with "usually"; per-exchange rules not cited. Pro-rata markets not covered.

Duration: 166.6 s.
