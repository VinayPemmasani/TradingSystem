# Pattern 12: False sharing

**Rule:** one writer per cache line. Put fields that different threads write on separate 64-byte lines.

## General version (ai.hpp)

```cpp
struct CountersPacked {
  std::array<std::atomic<uint64_t>, 2> n{};   // n[0]: thread A, n[1]: thread B
};

template <class T, size_t N>
struct RingPacked {
  std::atomic<size_t> head{0};   // producer
  size_t cached_tail = 0;        // producer
  std::atomic<size_t> tail{0};   // consumer
  size_t cached_head = 0;        // consumer
  T buf[N];
};
```

## Hot-path version (fast.hpp)

```cpp
inline constexpr size_t kLine = 64;
struct alignas(kLine) PaddedCounter {
  std::atomic<uint64_t> n{0};
};
struct CountersPadded {
  std::array<PaddedCounter, 2> c;
};
static_assert(sizeof(CountersPadded) == 2 * kLine);
template <class T, size_t N>
struct RingPadded {
  alignas(kLine) std::atomic<size_t> head{0};
  size_t cached_tail = 0;
  alignas(kLine) std::atomic<size_t> tail{0};
  size_t cached_head = 0;
  alignas(kLine) T buf[N];
};
```

## Why the general version is slower (machine level)

- Caches transfer and track whole 64-byte lines (64 on this box: `coherency_line_size`, and
  `std::hardware_destructive_interference_size` in g++ 13.3).
- To write, a core needs the line in Modified/Exclusive state, so the other core's copy is invalidated (MESI).
- With n[0] and n[1] in one line, each thread's write steals the line from the other: every increment becomes a
  cross-core transfer even though the threads share no data.
- In the packed ring, the producer writes head and cached_tail in the same line where the consumer writes tail and
  cached_head; every push invalidates the consumer's line and every pop the producer's. Even the cached copies,
  meant to avoid touching the other side's line, now live in it. The first slots share that line too.
- Padding cannot remove true sharing: in any SPSC ring the consumer must read head and the producer tail, which is
  why the ring gains 1.6x while the counters gain 4.5x.

## Measured (shared 4-vCPU cloud VM, Xeon @ 2.10 GHz, g++ 13.3 -O2 -std=c++20)

Two threads pinned to CPU 1 and CPU 0, `chrt -f 10`; median of 5 runs (min-max). The VM was heavily loaded.

| Metric | General (packed) | Hot path (padded) | Ratio |
| --- | --- | --- | --- |
| counters: 100M relaxed fetch_add per thread, ns/increment | 31.8 (28.5-36.1) | 7.1 (6.7-8.0) | 4.5x |
| SPSC ring: 20M 8-byte messages, ns/message | 98.3 (69.1-112.4) | 60.0 (42.6-75.9) | 1.6x |
| bytes: two counters | 16 | 128 | 8x the memory |
| bytes: ring header before buf | 32 | 128 | |

Both layouts give identical counter totals and ring output (test.cpp, PASS). Method and raw runs:
`/tmp/claude-0/vx/ai-12-false-sharing/code/` (README.md, runs.txt).

## When the general version is fine

Data written by a single thread, read-mostly or read-only data, and large arrays: dense is better there because
more of it fits in cache, and padding just wastes lines. Pad only fields written by different threads at a high
rate on different cores. Prefer a fixed 64 (as the lab does) over `std::hardware_destructive_interference_size`
in headers and shared-memory structs: g++ warns that its value can change with -mtune/-mcpu, which would change
the layout. Some code pads to 128 because Intel's L2 spatial prefetcher fetches 128-byte-aligned line pairs.

## Sources

- cppreference, `std::hardware_destructive_interference_size`:
  https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size
- GCC `-Winterference-size`: https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html
- Intel 64 and IA-32 Architectures Optimization Reference Manual (spatial prefetcher; false sharing)
- Trading lab: `/home/claude/ts-push/libs/core/include/lab/core/compiler.hpp` (kCacheLine = 64) and `spsc_ring.hpp`
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (https://github.com/CppCon/CppCon2017)
