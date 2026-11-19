#pragma once
#include <random>
#include <vector>
#include "book.hpp"
struct Tick { std::int64_t lo, hi; };
inline Book make_book() {
  Book b; b.depth = kMaxDepth;
  for (int i = 0; i < kMaxDepth; ++i) b.levels[i] = {100000 - i * 5, 100 + 7 * i, 1 + i % 4};
  return b;
}
// Bands 4..24 levels wide at a random offset: a typical "levels near my quote" query.
inline std::vector<Tick> make_ticks(int n) {
  std::mt19937_64 r(42); std::vector<Tick> t(n);
  for (auto& x : t) { int off = int(r() % 8), w = 4 + int(r() % 21);
    x.hi = 100000 - off * 5; x.lo = x.hi - (w - 1) * 5; }
  return t;
}
