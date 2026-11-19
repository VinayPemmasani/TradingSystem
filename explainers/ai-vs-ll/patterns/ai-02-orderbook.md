# Pattern 02: Order book price levels

**Rule:** index price levels by integer tick in a flat array, keep a best cursor, and never allocate per level.

## General-purpose version (left)

```cpp
#pragma once
// LEFT: the general-purpose version. A price-level (market-by-price) book:
// one std::map per side, keyed by price. Correct for any price, any depth.
#include <cstdint>
#include <functional>
#include <map>
#include <optional>
#include <utility>

namespace ai {
struct Level { std::int64_t qty; };
using Top = std::optional<std::pair<double, std::int64_t>>;

class Book {
 public:
  void set(bool bid, double px, std::int64_t qty) {   // qty 0 = delete level
    if (bid) apply(bids_, px, qty); else apply(asks_, px, qty);
  }
  Top best_bid() const { return top(bids_); }
  Top best_ask() const { return top(asks_); }
 private:
  template <class M> static void apply(M& m, double px, std::int64_t qty) {
    if (qty == 0) m.erase(px);
    else m[px].qty = qty;                               // allocates a node if new
  }
  template <class M> static Top top(const M& m) {
    if (m.empty()) return std::nullopt;
    return std::make_pair(m.begin()->first, m.begin()->second.qty);
  }
  std::map<double, Level, std::greater<double>> bids_;  // best bid first
  std::map<double, Level> asks_;                        // best ask first
};
}  // namespace ai
```

## Hot-path version (right)

```cpp
#pragma once
// RIGHT: the hot-path version. Prices are integer ticks. Each side is a flat
// array of quantities indexed by (price - base), plus a cursor at the best level.
// Constraint stated up front: prices stay inside a known window (price bands).
#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace hp {
using Top = std::optional<std::pair<std::int64_t, std::int64_t>>;  // ticks, qty

class FlatBook {
 public:
  FlatBook(std::int64_t base, std::int32_t n)            // window [base, base+n)
      : base_(base), n_(n), bid_(std::size_t(n)), ask_(std::size_t(n)), bb_(-1), ba_(n) {}
  bool set(bool bid, std::int64_t px, std::int64_t qty) {  // qty 0 = delete level
    const std::int64_t i = px - base_;
    if (i < 0 || i >= n_) return false;                    // outside band: caller recenters
    const auto k = std::int32_t(i);
    if (bid) {
      bid_[std::size_t(k)] = qty;
      if (qty != 0 && k > bb_) bb_ = k;
      else if (qty == 0 && k == bb_) while (bb_ >= 0 && bid_[std::size_t(bb_)] == 0) --bb_;
    } else {
      ask_[std::size_t(k)] = qty;
      if (qty != 0 && k < ba_) ba_ = k;
      else if (qty == 0 && k == ba_) while (ba_ < n_ && ask_[std::size_t(ba_)] == 0) ++ba_;
    }
    return true;
  }
  Top best_bid() const { if (bb_ < 0) return std::nullopt; return std::make_pair(base_ + bb_, bid_[std::size_t(bb_)]); }
  Top best_ask() const { if (ba_ >= n_) return std::nullopt; return std::make_pair(base_ + ba_, ask_[std::size_t(ba_)]); }
 private:
  std::int64_t base_;
  std::int32_t n_;
  std::vector<std::int64_t> bid_, ask_;   // qty per tick; 0 = empty level
  std::int32_t bb_, ba_;                  // best bid / best ask index
};
}  // namespace hp
```

## Why the left is slower

- `std::map` is a red-black tree (libstdc++ `_Rb_tree`): finding a price walks root to leaf, ~9-10 dependent node loads for ~420 live levels; each load must finish before the next address is known.
- Each step compares doubles and branches left/right; the direction is data dependent, so the branch predictor misses often (a miss typically costs ~15-20 cycles on recent Intel/AMD cores).
- A new level allocates a node (`malloc`, 48 B node here) and a deleted level frees one: measured 0.33 allocations per message for a 1/3 add mix. Insert and erase may rebalance (recolour/rotate), writing several nodes.
- Here the whole book (~850 nodes) fits in the 2 MB L2, so the gap is pointer chasing, branches and allocation, not cache misses. A deeper or colder book would add misses.
- `double` keys only match if every price arrives bit-identical; the hot path uses integer ticks, which also removes that hazard.
- The flat version: index = px - base (one subtract, one store), cursor compare; delete-at-best scans adjacent slots (contiguous, same cache lines). Top-of-book read is one load in both (libstdc++ caches the leftmost node).

## Measured

Shared 4-vCPU cloud VM (Xeon @ 2.1 GHz, 2 MB L2/core, heavily loaded), g++ 13.3 -O2 -std=c++20, `taskset -c 3`. 1M level updates per run (1/3 add, 1/3 modify, 1/3 delete) near the touch, ~420 live levels/side; each message = set level + read best bid and ask. Medians of 5 runs.

| Metric | General (std::map) | Hot path (flat array + cursor) | Ratio |
| --- | --- | --- | --- |
| one message at a time, p50 (incl. ~22 ns timer) | 103 ns | 33 ns | 3.1x (≈7x net of timer) |
| one message at a time, p99 (incl. timer) | 204 ns | 59 ns | 3.5x |
| one message at a time, p99.9 (incl. timer) | 390 ns | 236 ns | 1.7x |
| back to back, ns/message (median 1k-msg batch) | 82 (81-83) | 11 (10.9-11.0) | 7.5x |
| allocations per message | 0.33 | 0 | - |
| top-of-book read alone | ~1.8 ns | ~1.8 ns | 1x |
| memory | 48 B node per live level (+ malloc header) | 2 x 4096 x 8 B = 64 KB fixed | - |

Method: `/tmp/claude-0/vx/ai-02-orderbook/code` (README). One-at-a-time = lfence+rdtsc / rdtscp. Allocations via replaced `operator new`. No perf counters on this VM, so branch misses are explained, not counted. Test: 5 seeds x 200k ops, top of book compared after every op.

## When the general version is fine

Prices that are unbounded or sparse, instruments with no fixed tick, multi-venue consolidated views with mixed ticks, analytics, replay tools and tests. The flat book needs its constraints stated: integer tick size, a known price band (with a recenter path when price leaves it), and no allocation per level.

## Sources

- cppreference, std::map: https://en.cppreference.com/w/cpp/container/map
- Intel 64 and IA-32 Architectures Optimization Reference Manual (branch misprediction cost): https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- David Gross, "When Nanoseconds Matter: Ultrafast Trading Systems in C++", CppCon 2024 (order book design): https://www.youtube.com/watch?v=sX2nF1fW7kI
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: https://www.youtube.com/watch?v=NH1Tta7purM
- Related lab video: /mnt/project-files/videos/explainers/cpp-order-book
- Video: /mnt/project-files/videos/explainers/ai-02-orderbook
