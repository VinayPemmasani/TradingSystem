# Pattern 01: Quote lookup by symbol

**Rule:** intern strings at the edge (startup or the feed handler); key hot tables by a small integer.

## General-purpose version (left)

```cpp
#pragma once
// LEFT: the general-purpose version. Correct, idiomatic, and what you get
// when the prompt says "cache the latest quote per symbol".
#include <cstdint>
#include <string>
#include <unordered_map>

namespace ai {
struct Quote { double bid, ask; std::uint64_t ts; };

class QuoteCache {
 public:
  void on_tick(const std::string& sym, double bid,
               double ask, std::uint64_t ts) {
    quotes_[sym] = Quote{bid, ask, ts};   // hash string, walk bucket
  }
  const Quote* find(const std::string& sym) const {
    auto it = quotes_.find(sym);
    return it == quotes_.end() ? nullptr : &it->second;
  }
 private:
  std::unordered_map<std::string, Quote> quotes_;
};
}  // namespace ai
```

## Hot-path version (right)

```cpp
#pragma once
// RIGHT: the hot-path version. Symbols are interned to a small integer id once,
// at startup; the hot path carries the id and does one probe into a flat table.
#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>

namespace hp {
struct Quote { double bid, ask; std::uint64_t ts; };

class FlatQuotes {                       // open addressing, linear probing
 public:
  explicit FlatQuotes(std::uint32_t cap_pow2)   // sized once; never grows
      : slot_(std::make_unique<Slot[]>(cap_pow2)), mask_(cap_pow2 - 1) {}
  Quote* insert(std::uint32_t id) {      // startup only; id 0 is reserved
    std::uint32_t i = home(id);
    while (slot_[i].id != 0 && slot_[i].id != id) i = (i + 1) & mask_;
    slot_[i].id = id;
    return &slot_[i].q;
  }
  Quote* find(std::uint32_t id) {        // hot path
    for (std::uint32_t i = home(id);; i = (i + 1) & mask_) {
      if (slot_[i].id == id) return &slot_[i].q;
      if (slot_[i].id == 0) return nullptr;
    }
  }
  void on_tick(std::uint32_t id, double bid, double ask, std::uint64_t ts) {
    if (Quote* q = find(id)) *q = Quote{bid, ask, ts};
  }
 private:
  struct Slot { std::uint32_t id = 0; Quote q{}; };   // 32 bytes, 2 per line
  std::uint32_t home(std::uint32_t id) const {
    return (id * 0x9E3779B1u) & mask_;   // Fibonacci hash spreads ids
  }
  std::unique_ptr<Slot[]> slot_;
  std::uint32_t mask_;
};

// Startup: give every symbol an id once. Feeds often send one already
// (e.g. ITCH "stock locate"); then this map is only for reference data.
class SymbolIds {
 public:
  std::uint32_t intern(const std::string& s) {
    auto [it, fresh] = ids_.try_emplace(s, next_);
    if (fresh) ++next_;
    return it->second;
  }
 private:
  std::unordered_map<std::string, std::uint32_t> ids_;
  std::uint32_t next_ = 1;
};
}  // namespace hp
```

## Why the left is slower

- Every tick hashes the symbol string: libstdc++ `std::hash<std::string>` runs a byte loop (`_Hash_bytes`) over the key.
- The hash is reduced modulo a prime bucket count (libstdc++ prime rehash policy), which is an integer division on each lookup.
- The bucket array holds a pointer; the entry lives in a separately allocated heap node (one `malloc` per symbol, measured 1.0 allocation and ~100 B per entry incl. buckets). Bucket load and node load are dependent: the second cannot start until the first returns.
- With 200k instruments the nodes take ~20 MB, ten times the 2 MB per-core L2, so those dependent loads tend to miss.
- Symbols longer than 15 chars (libstdc++ SSO limit), e.g. 21-char OCC option symbols, add a third pointer to the key's heap buffer.
- The flat table does a multiply and mask, then one load of a 32 B slot whose id and quote share a cache line. Its 8 MB array also exceeds L2, but a lookup is usually a single miss.

## Measured

Shared 4-vCPU cloud VM (Xeon @ 2.1 GHz, 2 MB L2/core), g++ 13.3 -O2 -std=c++20, `taskset -c 3`. 200,000 instruments (7-char symbols, fit SSO), 1M uniform random ticks, same sequence for both. Six runs at N=200k; two at N=1000.

| Metric | General (unordered_map) | Hot path (flat table) | Ratio |
| --- | --- | --- | --- |
| ns/tick back to back, median of 6 (range) | 77 (70-105) | 9.8 (9.5-11.1) | ~8x |
| one tick at a time, p50 (incl. ~21 ns timer) | 265 ns | 61 ns | ~4.3x |
| one tick at a time, p99 (incl. ~21 ns timer) | 711 ns | 279 ns | ~2.5x |
| 1,000 instruments (all in cache), ns/tick | 30 | 5 | ~6x |
| heap bytes per instrument | 100 B | 42 B (32 B slot / load 0.76) | 2.4x |
| hot-path allocations per tick | 0 | 0 | - |

Method: `bench.cpp` in `/tmp/claude-0/vx/ai-01-hashmap/code` (README there). Back-to-back = total TSC time / ticks over 5 alternating runs; one-at-a-time = lfence+rdtsc / rdtscp around each call. Bytes and allocations counted with a replaced `operator new`. No perf counters on this VM, so cache behaviour is inferred from the in-cache vs out-of-cache comparison, not counted. Test: `test.cpp` (ASan/UBSan) applies 100k random ticks to both and compares every quote.

## When the general version is fine

Reference data, configuration, startup, tools, tests, anything not on the per-tick path, or when the key set is unknown and unbounded. The map is correct and grows on demand; the flat table needs the constraints stated: instruments known at startup, small ids, fixed capacity. If ids are dense (0..N), a plain array indexed by id is simpler still.

## Sources

- libstdc++ unordered_map / hashtable implementation: https://gcc.gnu.org/onlinedocs/libstdc++/manual/unordered_associative.html
- cppreference, std::unordered_map: https://en.cppreference.com/w/cpp/container/unordered_map
- Nasdaq TotalView-ITCH 5.0 spec (Stock Locate field): https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: https://www.youtube.com/watch?v=NH1Tta7purM
- David Gross, "When Nanoseconds Matter", CppCon 2024: https://www.youtube.com/watch?v=sX2nF1fW7kI
- Video: /mnt/project-files/videos/explainers/ai-01-hashmap
