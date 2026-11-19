// LEFT: the general-purpose version. Correct and idiomatic; allocates every call.
#pragma once
#include <vector>
#include "book.hpp"
namespace ai {
// Each tick: the levels priced inside [lo, hi]
std::vector<Level> levels_in_band(const Book& b,
                                  Px lo, Px hi) {
  std::vector<Level> out;
  for (int i = 0; i < b.depth; ++i) {
    const Level& l = b.levels[i];
    if (l.px >= lo && l.px <= hi)
      out.push_back(l);
  }
  return out;
}
}  // namespace ai
