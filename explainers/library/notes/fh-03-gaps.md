# fh-03-gaps: Gap detection, retransmission and stale books

Key facts and sources (lab repo /home/claude/ts-push):

- Sequencer state: `expected_` (next to deliver) and `high_` (one past highest seen); a gap is `expected_ < high_`. Messages ahead of a gap are copied into a preallocated window (slot = seq & mask, up to 64 bytes each). Source: `libs/mold/include/lab/mold/sequencer.hpp`.
- itch-fh defaults: window 1u << 18 = 262,144 messages, gap_delay 100 µs, timeout 20 ms, 10 retries without progress, then give up. Source: `libs/feed/include/lab/feed/receiver.hpp` (`ReceiverConfig`).
- Heartbeats (count 0) carry the next sequence number; requests are a bare 20-byte header (session, sequence, count) sent unicast. Source: `docs/specs/moldudp64-layout.md`, [MoldUDP64 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf).
- Real run shown on screen: `scripts/e2e-live-feed.sh` (default faults, rate 500k msg/s) on this shared, heavily loaded 4-vCPU box on 19 Nov 2026: 9 gaps opened, 9 given up, 663,863 messages lost, 656,674 window overflows, 93 unknown order references, test FAIL.

Unsure: the cause of the failure is the overload as far as I can tell (a no-fault run on the same box passed with matching digests, but its median receive-to-book was 24 ms, so the box itself was saturated). Notably every gap in both faulty runs ended "given up", none "filled"; I did not investigate whether that is purely load or something in the recovery path, and the video does not claim either. Venue recovery services are mentioned generically; no specific venue's snapshot mechanism is described.
