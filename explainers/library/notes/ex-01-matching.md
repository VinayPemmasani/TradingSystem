# ex-01-matching: Inside a matching engine

Topic 2, Exchanges and matching, video 1 of 10. About 3 minutes.

## Key facts and sources
- The single matching thread works as the sequencer. It gives each command the next sequence number, runs it through the engine, and then sends order responses to the gateway, ITCH messages to the publisher and the command to the journal. Commands are 64-byte structs on SPSC rings. Source: lab repo `exchange/simex/matcher.hpp` and `exchange/simex/messages.hpp`.
- Engine design: price-time priority on a single thread, deterministic and replayable from the journal. It reserves memory up front: `max_orders = 1u << 20` order slots and `levels_per_side = 512`. Each side is a sorted vector with the best price at the back. Each level is a doubly linked list whose head is the oldest order. Fills print at the resting level's price (`lv.price`). Source: `libs/match/include/lab/match/engine.hpp` (`EngineConfig`, `Book`, `Level`, `match_and_rest`).
- ITCH 5.0 Order Executed (E) is 31 bytes: an 11-byte header, then order reference 8, executed shares 4 and match number 8. OUCH 5.0 Order Executed is 36 bytes, with price, liquidity flag and match number. Source: lab `docs/specs/itch50-layout.md` and `docs/specs/ouch50-layout.md`, taken from Nasdaq's [ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf) and [OUCH 5.0](https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf) specifications.
- "Each fill becomes three messages" describes simex, where both sides are on OUCH sessions. A real venue sends each side a report on whatever protocol that side uses.

## Unsure / left out
- No latency numbers for the engine. `bench/bm_match.cpp` exists, but the shared VM was heavily loaded (load average about 18 on 4 vCPUs), so a measurement would not mean much.
- No claims about how particular real exchanges build their engines, such as replication or hot standby. I found no primary source this session.
- The worked example's prices and sizes are illustrative.
