# md-07-opra: OPRA (172 s)

Key facts and sources
- Symbols are spread across lines 1 to 96 in the regular session. Every message is sent on two redundant multicast streams, with separate retransmission streams. Blocks are at most 1000 bytes and have a 21-byte header (version, size, feed and retransmission indicators, session, block sequence 4, message count, timestamp in seconds and nanoseconds, checksum). Integers are big-endian. The long quote 'k' is 43 bytes and the short quote 'q' is 29 bytes. Line Integrity messages arrive at least every 10 s and are not retransmitted. Source: [OPRA Binary Data Recipient Interface Specification v6.4c, 16 Nov 2026](https://cdn.opraplan.com/documents/OPRA_Pillar_Output_Specification.pdf).
- 12.322 billion total messages per day were projected for October 2025, for one stream. Taking both streams doubles that, plus 10% for retransmissions. Median latency is under 18 µs. Source: [OPRA Capacity Projections Update, Sept 2025](https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf). The year and the source appear on screen.
- 20 participant exchanges, with SIAC as the processor. Quote traffic is "the vast majority". Source: [OPRA FAQ](https://www.opraplan.com/faqs).
- Lab tie-in: the vendor `Server` conflates per subscription (`libs/vendor/include/lab/vendor/server.hpp`).

Worked example: the quote 2.15 / 2.20, 40 x 25 is illustrative.

Unsure / left out: peak messages per second (the table's column meanings were ambiguous), the denominator code letters, and any "largest feed in the world" claim.
