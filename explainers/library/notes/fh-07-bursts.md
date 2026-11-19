# fh-07-bursts: Surviving the open: bursts and microbursts

Key facts and sources (lab repo /home/claude/ts-push):

- Socket receive buffer requested: `rcvbuf_bytes = 16 << 20` (16 MiB). The kernel may cap this; the video says "asks for". Source: `libs/net/include/lab/net/udp.hpp`.
- Packet ring `SpscRing<RxPacket, 4096>`, `sizeof(RxPacket) == 1536` → 6 MiB; held window 1u << 18 messages; `ring_full`, `window_overflow` counters (window overflow messages are "asked for again once the gap ahead of it fills"). Source: `libs/feed/include/lab/feed/receiver.hpp`, `libs/mold/include/lab/mold/sequencer.hpp`.
- Aeron: three terms of 4 MiB; back pressure beyond the slowest reader plus half a term; itch-fh retries on back pressure. Source: `docs/aeron.md`.
- recvmmsg batch of 32; vendor conflation per subscription. Source: `libs/feed/src/receiver.cpp`, `libs/vendor/include/lab/vendor/server.hpp`.
- Measured overload: the same 19 Nov 2026 run as fh-03 (shared 4-vCPU box, load average above 40): receive-to-book p50 8.49 ms, p90 32.95 ms, p99 41.68 ms; 656,674 window overflows. docs/aeron.md separately notes overloaded medians were "almost all of it queueing".

Unsure / left out: no exchange message-rate statistics (e.g. peak messages per second at the open) are given, because I did not verify one from a primary source this session; the title-card rate chart is labelled illustrative. Whether the kernel actually granted 16 MiB on this box was not checked.
