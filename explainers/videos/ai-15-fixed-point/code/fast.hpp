#pragma once
// RIGHT: the hot-path version (on screen verbatim below the includes).
#include <cstddef>
#include <cstdint>
#include <vector>
namespace hot {
using std::int64_t;
// price in ticks of 0.01: 5012.25 -> 501225
using Ticks = int64_t;
struct Levels {
  Ticks base;                // price of level 0
  std::vector<int64_t> qty;  // one slot per tick
  int64_t notional = 0;      // ticks x qty, exact
};
// px: validated and converted once, at the edge
void apply(Levels& L, Ticks px, int64_t qty) {
  const auto i = std::size_t(px - L.base);
  L.qty[i] += qty;
  L.notional += px * qty;
}
}  // namespace hot
