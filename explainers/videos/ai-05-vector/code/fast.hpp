// RIGHT: the hot-path version. Caller owns a fixed-capacity buffer; never allocates.
#pragma once
#include <vector>
#include "book.hpp"
namespace fast {
struct Band {                      // caller owns it
  std::array<Level, kMaxDepth> v;  // depth <= 32
  int n = 0;
};
inline void levels_in_band(const Book& b, Px lo,
                           Px hi, Band& out) {
  int n = 0;
  for (int i = 0; i < b.depth; ++i) {
    const Level& l = b.levels[i];
    if (l.px >= lo && l.px <= hi)
      out.v[n++] = l;   // n <= depth <= 32
  }
  out.n = n;
}
// Middle ground: a std::vector reserved once at startup, clear()-ed per call.
inline void levels_in_band(const Book& b, Px lo, Px hi,
                           std::vector<Level>& out) {
  out.clear();  // keeps capacity: no allocation while size <= capacity
  for (int i = 0; i < b.depth; ++i) {
    const Level& l = b.levels[i];
    if (l.px >= lo && l.px <= hi) out.push_back(l);
  }
}
}  // namespace fast
