# Pattern 10: The queue between two threads

**Rule:** on the hot path, hand messages over a bounded SPSC ring with a busy-polling consumer on its own core;
keep mutex + condition variable for threads without a latency budget.

## General version (ai.hpp)

```cpp
template <class T>
class BlockingQueue {
  std::mutex m_;
  std::condition_variable cv_;
  std::queue<T> q_;
 public:
  void push(const T& v) {
    { std::lock_guard lk(m_); q_.push(v); }
    cv_.notify_one();
  }
  T pop() {
    std::unique_lock lk(m_);
    cv_.wait(lk, [&] { return !q_.empty(); });
    T v = q_.front(); q_.pop();
    return v;
  }
};
```

## Hot-path version (fast.hpp)

```cpp
template <class T, size_t N>   // N: power of two, fixed at compile time
class SpscRing {
  alignas(64) std::atomic<size_t> head_{0};  // producer writes
  size_t cached_tail_ = 0;
  alignas(64) std::atomic<size_t> tail_{0};  // consumer writes
  size_t cached_head_ = 0;
  alignas(64) T buf_[N];
 public:
  bool try_push(const T& v) {
    size_t h = head_.load(relaxed);
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load(acquire);
      if (h - cached_tail_ == N) return false;  // full
    }
    buf_[h & (N - 1)] = v;
    head_.store(h + 1, release);
    return true;
  }
  bool try_pop(T& out) {
    size_t t = tail_.load(relaxed);
    if (t == cached_head_) {
      cached_head_ = head_.load(acquire);
      if (t == cached_head_) return false;      // empty
    }
    out = buf_[t & (N - 1)];
    tail_.store(t + 1, release);
    return true;
  }
  T pop() { T v; while (!try_pop(v)) _mm_pause(); return v; }  // busy-poll
};
```

## Why the general version is slower (machine level)

- The idle consumer sleeps in the kernel on a futex inside `condition_variable::wait`. Each hand-off to a
  sleeping consumer costs a `futex` wake syscall from the producer (`notify_one`), a scheduler wake-up, and a
  context switch (measured ~0.2 context switches per message: the consumer slept about every fifth message).
- On a VM, waking an idle vCPU also goes through the hypervisor, which pushed the median wake to ~5 us
  (and ~16 us with 10 us between messages, when the vCPU had longer to go idle).
- While the consumer is waking, later messages queue behind it, so the p99 includes queueing (32 us to 2.2 ms).
- Both sides take the same mutex: a locked read-modify-write each, and the mutex's cache line bounces between cores.
- `std::queue` is a `std::deque`: one 512-byte chunk allocation (and free) per 16 32-byte messages.
- Code: `push` 187 instructions + 14 call sites, `pop` 81 + 7 (g++ -O2); the ring's `try_push`/`try_pop`
  26 + 22 instructions, no calls. The ring's hand-off is just the slot and head lines moving between caches.

## Measured (shared 4-vCPU cloud VM, Xeon @ 2.10 GHz, g++ 13.3 -O2 -std=c++20)

One-way latency feed -> strategy (rdtsc stamped by the feed, read on receipt), one 32-byte message every ~2 us,
100k messages per run, feed pinned to CPU 1, strategy to CPU 0, both `chrt -f 10`. Median of 5 runs (min-max).
The VM was heavily loaded by other jobs.

| Metric | General (mutex + cv + std::queue) | Hot path (SPSC ring, spin) | Ratio |
| --- | --- | --- | --- |
| p50 one-way latency | 5,455 ns (5,314-6,830) | 216 ns (208-235) | 25x |
| p99 one-way latency | 1,161,949 ns (32,289-2,200,220) | 900 ns (344-12,848) | ~1,000x (very noisy) |
| context switches / msg (consumer) | 0.16-0.23 | 0 | |
| allocations / msg | 0.0625 (1 per 16) | 0 | |
| instructions push+pop (objdump) | 268 + 21 call sites | 48, 0 calls | |

Both queues deliver the same 1M messages in the same order (test.cpp, PASS). Method and raw runs:
`/tmp/claude-0/vx/ai-10-queue/code/` (README.md, runs.txt).

## When the general version is fine

Thread pools, background and housekeeping work, many producers, more threads than cores, and anything without
a latency budget: a sleeping consumer costs nothing while idle, while a spinning one burns a whole core all day
and needs an isolated, pinned core to be worth it. A bounded ring also forces a decision about "full"
(drop, block, or back-pressure), which the unbounded queue hides.

## Sources

- cppreference, `std::condition_variable`: https://en.cppreference.com/w/cpp/thread/condition_variable
- Linux `futex(2)` man page: https://man7.org/linux/man-pages/man2/futex.2.html
- Erik Rigtorp, "Optimizing a ring buffer for throughput" (cached indices): https://rigtorp.se/ringbuffer/
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (https://github.com/CppCon/CppCon2017)
- David Gross, "When Nanoseconds Matter: Ultrafast Trading Systems in C++", CppCon 2024 (https://github.com/CppCon/CppCon2024)
- Trading lab ring: `/home/claude/ts-push/libs/core/include/lab/core/spsc_ring.hpp`
