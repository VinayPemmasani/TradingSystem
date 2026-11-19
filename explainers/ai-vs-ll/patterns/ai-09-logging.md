# Pattern 09: Logging on the hot path

**Rule:** on the hot path, log data, not text. Copy a small binary record into a ring and format it on another core.

## General version (ai.hpp)

```cpp
class Logger {
  std::mutex mu_;
  std::ofstream out_;
 public:
  explicit Logger(const char* path) : out_(path) {}
  void fill(const char* sym, int64_t px, uint32_t qty, uint64_t oid) {
    auto ns = std::chrono::system_clock::now().time_since_epoch().count();
    std::lock_guard lock(mu_);
    out_ << ns << " fill oid=" << oid << " sym=" << sym
         << " px=" << px << " qty=" << qty << std::endl;
  }
};
```

## Hot-path version (fast.hpp, producer side)

```cpp
struct Rec {                    // 48 bytes, trivially copyable
  uint64_t tsc;
  const char* fmt;              // string literal: only the pointer is copied
  const char* sym;              // must outlive the logger (literal / static)
  int64_t px; uint64_t oid; uint32_t qty;
};
static_assert(sizeof(Rec) == 48);

void fill(const char* sym, int64_t px, uint32_t qty, uint64_t oid) {
  uint64_t h = head_.load(relaxed);
  if (h - cached_tail_ == N) {
    cached_tail_ = tail_.load(acquire);
    if (h - cached_tail_ == N)
      { ++dropped; return; }  // never block
  }
  buf_[h & (N - 1)] =
      Rec{__rdtsc(), kFillFmt, sym, px, oid, qty};
  head_.store(h + 1, release);  // publish
}
// A background thread pinned to another core drains the ring, converts TSC ticks to wall time,
// fprintf()s the stored format with the raw args, and writes in 64 KB chunks.
```

## Why the general version is slower (machine level)

- `std::endl` is `'\n'` plus `flush()`: the filebuf hands every line to the kernel with one `write()` syscall
  on the calling thread (strace: ~20,000 writes for 20,000 calls).
- The mutex is an atomic read-modify-write on every call, and a `futex()` syscall (sleep/wake) when contended.
- Each `operator<<` is an out-of-line call into libstdc++; integers go through the stream's locale `num_put`
  facet, strings through `strlen` + `__ostream_insert`. g++ -O2: `Logger::fill` is 106 instructions with
  21 call sites into the library; the ring's `fill` is 30 instructions (25 on the common path) and 0 calls.
- The `write()` copies into the page cache inside the kernel; its tail latency depends on the filesystem
  and the VM, which is why the general p99 is ~16x the ring's.
- The ring's own ~115 ns is mostly coherence: the writer core has read the head/slot lines, so each new
  store needs the line back (an RFO). With no consumer running, the same call measured ~42 ns incl. timer.
- Formatting is not free on the other side either: it just moves to a core with no latency budget.

## Measured (shared 4-vCPU cloud VM, Intel Xeon @ 2.10 GHz, g++ 13.3 -O2 -std=c++20)

Hot-thread cost per log call; 100k calls, ~1 us of busy work between calls, hot thread pinned to CPU 1,
writer thread to CPU 0, file sink on the VM disk; rdtscp timing (~21 ns timer overhead included);
median of 5 runs (min-max). Another benchmark was running on CPU 2.

| Metric | General (`std::endl`) | General (`'\n'`) | Hot path (ring) | Ratio endl / ring |
| --- | --- | --- | --- | --- |
| p50 | 625 ns (617-641) | 261 ns (251-268) | 115 ns (91-119) | 5.4x |
| p99 | 2,180 ns (2,164-2,340) | 1,233 ns (1,136-1,461) | 137 ns (109-151) | 15.9x |
| write() syscalls on the hot thread | 1 per call | ~1 per 126 calls | 0 | |
| allocations per call | 0 | 0 | 0 | |
| instructions in the call (objdump) | 106 + 21 lib calls | same | 30, 0 calls | |

`/dev/null` sink: endl p50 445 ns (418-461), p99 1,022 ns (703-1,090); ring p50 122 ns (102-135),
p99 143 ns (119-226). First run's ring p99.9 (~2 us) is first-touch page faults of the 3 MB ring: prefault it.
Both versions write identical lines after the timestamp (test.cpp, 500 lines, PASS).
Method and raw runs: `/tmp/claude-0/vx/ai-09-logging/code/` (README.md, runs_file.txt, runs_null.txt).

## When the general version is fine

Startup, config errors, shutdown, tools and scripts, and any thread with no latency budget. Swapping
`std::endl` for `'\n'` alone already removed most syscalls (2.4x at p50). The ring version has real costs:
records can be dropped when the ring is full, string arguments must be literals or outlive the logger,
lines appear on disk later, and a crash can lose what is still in the ring.

## Sources

- cppreference, `std::endl` (inserts a newline and flushes): https://en.cppreference.com/w/cpp/io/manip/endl
- S. Yang, S. J. Park, J. Ousterhout, "NanoLog: A Nanosecond Scale Logging System", USENIX ATC 2018:
  https://www.usenix.org/conference/atc18/presentation/yang-stephen
- Carl Cook, "When a Microsecond Is an Eternity: High Performance Trading Systems in C++", CppCon 2017
  (slides: https://github.com/CppCon/CppCon2017)
- David Gross, "When Nanoseconds Matter: Ultrafast Trading Systems in C++", CppCon 2024
  (slides: https://github.com/CppCon/CppCon2024)
- Trading lab async logger: `/home/claude/ts-push/libs/core/include/lab/core/log.hpp` (LogChannel + AsyncLogger)
