# ms-10-volume: Intraday volume curves and the close

## Key facts and sources
- Admati & Pfleiderer, "A theory of intraday patterns: volume and price variability", RFS 1(1) 3–40, 1988. https://gsb.stanford.edu/faculty-research/publications/theory-intraday-patterns-volume-price-variability
- NYSE (Aug 29, 2024): closing auctions 9.44% of total US equity notional value traded in Q2 2024, a record. https://nyse.com/data-insights/nyse-closing-auction-price-discovery-opportunities-reach-new-highs
- Nasdaq (June 26, 2026): Russell reconstitution Closing Cross 4,594,880,616 shares, $334.027bn, 1.630 s; 2025: 2,506,428,416 shares. https://nasdaqinc.gcs-web.com/node/110641
- Lab: tools/quant-lab/main.cpp fund_mkt/fund_us arrays of 13 half-hour buckets; kEventsPerMinute constant → flat profile; simex --close-at/--close-auction, NOII imbalance, ITCH I/Q cross type C (docs/scenarios.md).

## Worked numbers (mine)
- Made-up profile (% per half hour): 12, 8, 7, 6, 5.5, 5, 5, 5, 5.5, 6, 6.5, 7.5, 11.5 + close 9.5 = 100 → VWAP schedule for 100,000 shares.

## Unsure / left out
- No real intraday volume curve on screen: market data APIs available here gave daily bars only, so the U-shape is labelled illustrative. Closing share of share volume (vs notional) not stated.

Duration: 177.7 s.
