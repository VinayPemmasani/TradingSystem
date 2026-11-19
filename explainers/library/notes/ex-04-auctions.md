# ex-04-auctions: Opening and closing auctions

## Key facts and sources
- Nasdaq Opening Cross runs at 9:30 a.m. ET. NOII starts at 9:25 and comes every 10 seconds until 9:28, then every second. MOO orders must arrive before 9:28, and LOO orders until 9:29:30.
- Nasdaq Closing Cross runs at 4:00 p.m. ET. NOII starts at 3:50 and comes every 10 seconds until 3:55, then every second. MOC orders must arrive before 3:55, and LOC orders before 3:58.
- The cross price comes from three steps in order: maximize shares executed, minimize imbalance, minimize distance from the Nasdaq inside bid-ask midpoint.
- The Opening Cross sets the NOOP and the Closing Cross sets the NOCP. Unexecuted MOO, MOC, LOO, LOC and IO orders are cancelled after the cross. The crosses do not access other venues.
- All of the above comes from Nasdaq's Opening/Closing Cross FAQ (© 2025), https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf.
- ITCH 5.0 NOII (I) is 50 bytes: paired 8, imbalance 8, direction 1, stock 8, far 4, near 4, reference 4, cross type 1, price variation 1. Cross Trade (Q) carries the cross volume once. Source: lab `docs/specs/itch50-layout.md`.
- Lab: `Engine::indicative()` maximizes executable shares, then takes the smaller imbalance, then the price nearest the reference, then the lower price. `uncross()` fills every order at one price. simex publishes I, then Q, plus C non-printable executions. `noii_interval_s` defaults to 1. Sources: `libs/match/include/lab/match/engine.hpp`, `exchange/simex/matcher.cpp`, `exchange/simex/scenarios.hpp`.

## Unsure / left out
- No closing-auction volume share statistics. I found no primary figure this session.
- The worked book is illustrative. Its "reference" stands in for Nasdaq's inside midpoint.
- The open/close price-validation thresholds in the FAQ (for example, the greater of $0.50 or 10%) are not used in the video.
