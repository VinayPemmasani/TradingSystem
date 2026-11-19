# fh-09-timestamps: Timestamping and measuring feed latency

Key facts and sources:

- ITCH timestamp: 6 bytes at offset 5, nanoseconds since midnight. Source: [Nasdaq TotalView-ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).
- The rx thread reads `rdtsc()` once after each `batch.receive()` (recvmmsg) and stamps every datagram of that batch with it. Source: `libs/feed/src/receiver.cpp` (lab repo /home/claude/ts-push).
- `rdtsc` "a few ns, no syscall"; `rdtscp` waits for earlier instructions; `TscClock::calibrate` brackets `mono_ns()` with two rdtsc reads over a 50 ms window ("better than 0.01% accuracy on an invariant TSC"). Source: `libs/core/include/lab/core/clock.hpp`, `clock.cpp`.
- Ticks travel in `RxPacket::rx_tsc`, `TopOfBook::rx_tsc`, `OrderRequest::tick_tsc/decide_tsc`, and the Aeron frame's reserved value. Source: `receiver.hpp`, `firm/oms/.../messages.hpp`, `docs/aeron.md`.
- `LatencyHistogram`: values below 64 exact, 32 sub-buckets per power of two, within ~3%, prints p50/p90/p99/p99.9/p99.99/max. Source: `libs/core/include/lab/core/histogram.hpp`.
- WSL2/VM caveat: compare latency as relative changes between builds. Source: `docs/core-plan.md`.

Left out: PTP and hardware timestamping detail (network topic, net-04); no claim about NIC timestamp precision.
