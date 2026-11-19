# Pattern 03: shared_ptr through the handler chain

**Rule:** own once, borrow everywhere: one owner (a pool) for the session, plain references in handlers, and never copy a shared_ptr per message.

## General-purpose version (left)

```cpp
#pragma once
// LEFT: the general-purpose version. Orders are shared, so each one is a
// std::shared_ptr, and every handler takes it by value: clear ownership, no
// dangling pointers, whoever holds it last frees it.
#include <memory>
#include "order.hpp"

namespace ai {
[[gnu::noinline]] void publish(std::shared_ptr<Order> o, Stats& s) { s.out += o->qty; }
[[gnu::noinline]] void route(std::shared_ptr<Order> o, Stats& s) {
  s.notional += o->px * o->qty;
  publish(o, s);
}
[[gnu::noinline]] void risk(std::shared_ptr<Order> o, Stats& s) {
  if (o->qty <= s.max_qty) route(o, s); else ++s.rejects;
}
[[gnu::noinline]] void on_msg(std::shared_ptr<Order> o, Stats& s) {
  if (o->px > 0) risk(o, s);
}
}  // namespace ai
```

## Hot-path version (right)

```cpp
#pragma once
// RIGHT: the hot-path version. One owner: a pool of Orders that lives for the
// whole session. Handlers borrow a plain reference; the message carries an index.
#include <cstdint>
#include <vector>
#include "order.hpp"

namespace hp {
[[gnu::noinline]] void publish(const Order& o, Stats& s) { s.out += o.qty; }
[[gnu::noinline]] void route(const Order& o, Stats& s) {
  s.notional += o.px * o.qty;
  publish(o, s);
}
[[gnu::noinline]] void risk(const Order& o, Stats& s) {
  if (o.qty <= s.max_qty) route(o, s); else ++s.rejects;
}
[[gnu::noinline]] void on_msg(const Order& o, Stats& s) {
  if (o.px > 0) risk(o, s);
}
struct OrderPool {                        // the single owner
  std::vector<Order> slots;               // sized at startup
  Order& operator[](std::uint32_t i) { return slots[i]; }
};
}  // namespace hp
```

## Why the left is slower

- A `std::shared_ptr` copy increments the use count in the control block; destroying the copy decrements it (and checks for zero). Passing by value through 4 handlers = 4 copies + 4 destructions = 8 read-modify-writes per message.
- Once the process has started any thread (every trading system has), libstdc++ performs these as atomic RMWs (`lock xadd` / `lock add` on x86). Measured on this VM: ~16 ns per dependent locked add vs <1 ns for a plain add.
- A locked instruction is a full memory barrier on x86: it drains the store buffer and later loads cannot pass it, which limits overlap with surrounding work.
- Code bloat: the four handlers compiled to 237 instructions with 6 lock-prefixed ops (plus single-thread fast-path branches) vs 29 instructions and none for the reference version (static objdump count).
- In a multi-threaded system the control block's cache line also moves between cores whenever another thread copies the same pointer (not measured here: single-threaded benchmark, per the brief).
- If the process never starts a thread, libstdc++ (GCC 11+, via glibc's `__libc_single_threaded`) skips the atomics; even then the copies cost 3x the reference version here.

## Measured

Shared 4-vCPU cloud VM (Xeon @ 2.1 GHz, heavily loaded), g++ 13.3 -O2 -std=c++20 -pthread, `taskset -c 3`. 1,000 orders (in cache), 2M messages, 4 noinline handlers. Medians of 3 runs.

| Metric | General (shared_ptr by value) | Hot path (pool + const Order&) | Ratio |
| --- | --- | --- | --- |
| back to back, ns/message (thread started) | 71.8 | 5.0 | 14x |
| one message at a time p50 (incl. ~22 ns timer) | 106.7 ns | 27.6 ns | 3.9x (≈17x net of timer) |
| one message at a time p99 (incl. timer) | 180 ns | 40 ns | 4.5x |
| back to back, process never started a thread | 16.8 | 5.0 | 3.4x |
| shared_ptr by const& (thread started), back to back | 5.9 | 5.0 | 1.2x |
| refcount RMWs per message | 8 (atomic) | 0 | - |
| one dependent atomic RMW vs plain add | ~16 ns | <1 ns | - |
| handler-chain instructions (static) | 237 (6 lock ops) | 29 (0) | 8x |

Method: `/tmp/claude-0/vx/ai-03-shared-ptr/code` (README). Back to back = median of 1,000-message batches; one at a time = lfence+rdtsc / rdtscp. Test: 100k messages through all three variants with identical totals.

## When the general version is fine

When lifetime is genuinely shared and unpredictable: objects handed across threads, async callbacks, caches, session/config objects, and anything off the per-message path. Even there, pass `const std::shared_ptr<T>&` or `T&` to functions that do not keep the object, and move rather than copy when transferring ownership. The pool version requires a stated rule: one owner, nothing on the hot path frees an order, and a slot is reused only when its order is done.

## Sources

- cppreference, std::shared_ptr (control block, thread-safety of the count): https://en.cppreference.com/w/cpp/memory/shared_ptr
- libstdc++ shared_ptr atomic policy / __libc_single_threaded: https://gcc.gnu.org/onlinedocs/libstdc++/manual/memory.html#shared_ptr.thread
- Intel 64 and IA-32 SDM Vol. 3A, 9.1.2 locked atomic operations / ordering: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- Herb Sutter, GotW #91 "Smart Pointer Parameters": https://herbsutter.com/2013/06/05/gotw-91-solution-smart-pointer-parameters/
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: https://www.youtube.com/watch?v=NH1Tta7purM
- Video: /mnt/project-files/videos/explainers/ai-03-shared-ptr
