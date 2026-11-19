# fh-10-replay: Testing with pcap replay

Key facts and sources:

- pcap savefile: 24-byte file header; 16-byte per-packet header (timestamp seconds, timestamp micro- or nanoseconds, captured length, original length). Source: [pcap-savefile(5)](https://www.mankier.com/5/pcap-savefile).
- The lab does not use pcap (`*.pcap` is git-ignored); it replays Nasdaq gzip BinaryFILE day files with `itch-replay` as MoldUDP64 (rate default 1M msg/s, `--rate 0` unlimited, `--speed` by ITCH timestamps; heartbeats, End of Session, re-request server). Source: `tools/itch-replay/main.cpp`, `libs/feed/include/lab/feed/publisher.hpp`, `docs/specs/itch50-layout.md` (lab repo /home/claude/ts-push).
- Seeded fault injector (drop, burst, duplicate, reorder; xorshift64*). Source: `libs/mold/include/lab/mold/fault_injector.hpp`.
- Oracle: itch-dump vs itch-fh book digest (FNV-1a over levels, trading state, volume, live order count). Source: `scripts/e2e-live-feed.sh`, `libs/book/src/book_builder.cpp`. Run after feed/sequencing/book changes (CLAUDE.md); CI runs it (README).
- My runs, 19 Nov 2026, shared heavily loaded 4-vCPU box, synthetic day: no faults at 50k msg/s → PASS, 1,000,406 messages, digest 0f90093c8381dcfd both; default faults at 25k msg/s → 40 gaps given up, 291,049 lost, 440 unknown order references, live digest f1fc5eb1df292a54, FAIL.

Unsure: why every gap was given up rather than filled on this box (see fh-03 note). The video says only what the report says.
