# fh-01-anatomy: Anatomy of a feed handler

Key facts and where they come from (lab repo paths are in /home/claude/ts-push):

- itch-fh runs two threads: an rx thread that makes every syscall (recvmmsg on the feed and re-request sockets, rdtsc stamp, push to a ring, send retransmission requests) and a book thread that sequences, decodes ITCH and updates books with no syscalls, locks or allocation. Source: `tools/itch-fh/main.cpp` header comment, `libs/feed/include/lab/feed/receiver.hpp`.
- Default pinning: rx thread on CPU 2, book thread on CPU 3. Source: `docs/core-plan.md`.
- recvmmsg batch of 32 datagrams; packet ring `SpscRing<RxPacket, 4096>`; `RxPacket` is 1536 bytes (1472-byte max UDP payload in a 1500-byte MTU). Source: `libs/feed/src/receiver.cpp`, `receiver.hpp`.
- A full packet ring drops the packet and counts `ring_full`; it is then recovered like any lost packet. Source: `receiver.hpp` (`RxStats::ring_full`), `docs/core-plan.md`.
- Everything is allocated and faulted in before threads start; exit code 0 only when nothing was lost and every integrity check is zero. Source: `tools/itch-fh/main.cpp`.
- ITCH Add Order is 36 bytes; Price(4) has 4 implied decimals; timestamp is nanoseconds since midnight. Source: `docs/specs/itch50-layout.md`, [Nasdaq TotalView-ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).
- The trader's market data thread pushes a 64-byte `TopOfBook` (static_assert) to the trading thread. Source: `firm/oms/include/lab/oms/messages.hpp`, `firm/trader/main.cpp`.

Unsure / illustrative: the packet in the worked example (sequence 1000, locate 13, reference 7001234, AAPL at 182.50, the level sizes) is invented to show the flow; only its layout is real. No latency numbers are given, because this shared box was heavily loaded.
