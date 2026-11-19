# Pattern 04: One malloc per message vs a preallocated pool

**Rule:** allocate (and touch) at startup; recycle on the hot path through a fixed-size pool with a free list.

## General-purpose version (left)

```cpp
#pragma once
// LEFT: the general-purpose version. Each new order is its own heap object;
// unique_ptr makes ownership and cleanup automatic.
#include <memory>
#include <vector>
#include "order.hpp"

namespace ai {
class Orders {
 public:
  explicit Orders(std::size_t max_live) { live_.reserve(max_live); }
  void on_new(const NewMsg& m) {
    auto o = std::make_unique<Order>(            // malloc per message
        Order{m.id, m.ts, m.px, m.qty, m.acct, m.side, {}, {}});
    live_.push_back(std::move(o));
  }
  void on_cancel(std::size_t k) {                // k: index of a live order
    live_[k] = std::move(live_.back());          // old order freed here
    live_.pop_back();
  }
  std::size_t size() const { return live_.size(); }
  const Order& at(std::size_t k) const { return *live_[k]; }
 private:
  std::vector<std::unique_ptr<Order>> live_;
};
}  // namespace ai
```

## Hot-path version (right)

```cpp
#pragma once
// RIGHT: the hot-path version. A fixed-size pool, allocated and touched at
// startup; a free list of slot pointers. acquire/release are two pointer moves.
#include <cstddef>
#include <cstring>
#include <memory>
#include <vector>
#include "order.hpp"

namespace hp {
template <class T>
class Pool {
 public:
  explicit Pool(std::size_t n) : slots_(std::make_unique<Slot[]>(n)) {
    std::memset(static_cast<void*>(slots_.get()), 0, n * sizeof(Slot));   // fault pages in now
    for (std::size_t i = 0; i < n; ++i) slots_[i].next = i + 1 < n ? &slots_[i + 1] : nullptr;
    free_ = &slots_[0];
  }
  T* acquire() noexcept {
    Slot* s = free_;
    if (!s) return nullptr;                      // full: caller rejects
    free_ = s->next;
    return &s->obj;
  }
  void release(T* p) noexcept {
    Slot* s = reinterpret_cast<Slot*>(p);
    s->next = free_; free_ = s;
  }
 private:
  union Slot { T obj; Slot* next; };
  std::unique_ptr<Slot[]> slots_;
  Slot* free_;
};

class Orders {
 public:
  explicit Orders(std::size_t max_live) : pool_(max_live) {
    live_.resize(max_live); live_.clear();       // touch the index pages at startup too
  }
  bool on_new(const NewMsg& m) {
    Order* o = pool_.acquire();
    if (!o) return false;                        // full: reject, never malloc
    *o = Order{m.id, m.ts, m.px, m.qty, m.acct, m.side, {}, {}};
    live_.push_back(o);
    return true;
  }
  void on_cancel(std::size_t k) {
    pool_.release(live_[k]);
    live_[k] = live_.back();
    live_.pop_back();
  }
  std::size_t size() const { return live_.size(); }
  const Order& at(std::size_t k) const { return *live_[k]; }
 private:
  Pool<Order> pool_;
  std::vector<Order*> live_;
};
}  // namespace hp
```

## Why the left is slower

- Every new order calls `malloc` (via `operator new`) and every cancel calls `free`: measured 0.5 allocations per message for a 50/50 new/cancel mix.
- glibc malloc's cost is not fixed: most calls hit the per-thread cache (tcache) and are fast, but misses walk bins, split and merge neighbouring chunks, which is slower and data dependent.
- Freed chunks scatter across the heap, so a new order lands in whatever hole fits, often a cold cache line; chunk headers next to the object are read and written too.
- When the live count surges, the heap grows (brk, or mmap for large requests) and each new 4 KB page faults on first touch, inside the message handler: 3,708 page faults while timing, which is where the p99.9 spike (4.6 us) comes from. glibc may later trim free memory at the top of the heap back to the kernel, so a later surge can fault again.
- The pool allocates the maximum once, writes every byte at startup (pages mapped before trading), and acquire/release are two pointer moves with no lock and no system call. The constraint is explicit: when the pool is empty the order is rejected.

## Measured

Shared 4-vCPU cloud VM (Xeon @ 2.1 GHz, load average ~50), g++ 13.3 -O2 -std=c++20, `taskset -c 3`, fresh process per variant. 2M messages (new order or cancel of a random live order), live count ramping 50k -> 150k -> 50k every 400k messages, 128 B orders. Medians of 3 runs.

| Metric | General (make_unique) | Hot path (pool + free list) | Ratio |
| --- | --- | --- | --- |
| p50 per message (incl. ~22 ns timer) | 177 ns | 65 ns | 2.7x |
| p99 | 858 ns | 335 ns | 2.6x |
| p99.9 | 4.56 us (4.39-4.91) | 445 ns (435-469) | 10x |
| allocations per message | 0.5 | 0 | - |
| page faults while timing | 3,708 | 0 | - |

Both sides also take cache misses from picking a random live order to cancel (the same in both). p99.99 and max were dominated by scheduler preemption on this loaded VM for both variants and are not reported. Method: `/tmp/claude-0/vx/ai-04-pool/code` (README). Test: 300k random new/cancel messages, all live orders identical; full pool rejects.

## When the general version is fine

Startup, configuration, cold paths, tools and tests, and objects whose count you cannot bound. A pool needs a stated maximum live count, memory reserved for the whole session, and a defined behaviour when full (reject, or a slow path off the hot thread). State those constraints, then measure the tail (p99, p99.9), not just the median.

## Sources

- glibc malloc internals (tcache, bins, trimming): https://sourceware.org/glibc/wiki/MallocInternals
- mallopt M_TRIM_THRESHOLD: https://man7.org/linux/man-pages/man3/mallopt.3.html
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (no allocation on the hot path): https://www.youtube.com/watch?v=NH1Tta7purM
- David Gross, "When Nanoseconds Matter", CppCon 2024: https://www.youtube.com/watch?v=sX2nF1fW7kI
- Related lab video: /mnt/project-files/videos/explainers/cpp-no-alloc
- Video: /mnt/project-files/videos/explainers/ai-04-pool
