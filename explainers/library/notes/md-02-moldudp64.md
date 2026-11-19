# md-02-moldudp64: MoldUDP64, sequenced UDP and re-requests (182 s)

Key facts and sources
- Downstream packet header is 20 bytes: Session 10 (alphanumeric), Sequence Number 8 (number of the first message in the packet), Message Count 2. Each message block is a 2-byte length followed by the message data. All integers are big-endian. Source: lab spec `docs/specs/moldudp64-layout.md`, taken from the [Nasdaq MoldUDP64 Protocol Specification V1.00](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf).
- Message Count 0 is a heartbeat, sent about once a second when the feed is idle, and it carries the next expected sequence number. Message Count 0xFFFF is End of Session. Source: the same spec.
- A re-request is a 20-byte packet (session, sequence, count) sent to the re-request server. The server answers with an ordinary packet over unicast holding what fits, and the receiver asks again for the rest. The server keeps only a bounded window of recent messages. Source: the same spec.
- Nasdaq offers TotalView-ITCH over MoldUDP64 ([ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf)).
- Lab tie-in: the defaults in `libs/feed/include/lab/feed/receiver.hpp` are gap_delay_us 100, timeout_ms 20, retries 10 and window 1<<18 (262,144 messages). After the last retry a gap's messages are counted as lost (`libs/mold/.../sequencer.hpp`). `scripts/e2e-live-feed.sh` injects drops, bursts, duplicates and reordering, and checks that `itch-fh`'s book digest equals `itch-dump`'s (`CLAUDE.md`).

Worked example: sequence 1001, count 3, with A (36 bytes), D (19) and E (31) = 86 bytes of messages plus 3 × 2 length bytes = 112 bytes of payload. The numbers are illustrative.

Unsure / left out: no figures for Nasdaq's real re-request window size or rate limits, because the spec does not give them.
