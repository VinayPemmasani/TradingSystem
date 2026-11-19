// RIGHT: the hot-path version. The strategy type is fixed at compile time, so quote() inlines.
#pragma once
#include <algorithm>
#include "prices.hpp"
namespace fast {
struct Clamp {           // no base, no vtable
  int edge, lo, hi;
  int quote(int mid) const {
    return std::clamp(mid - edge, lo, hi);
  }
};
template <class Q>       // type fixed at build
void quote_all(Q q, const Prices& mid,
               Prices& out) {
  for (int i = 0; i < kN; ++i)
    out[i] = q.quote(mid[i]);  // inlined, SIMD
}
// (end of on-screen snippet)
template <class Q>
int run_serial(Q q, const int* mid, int n) {
  int acc = 0;
  for (int i = 0; i < n; ++i) acc = q.quote(mid[i] ^ (acc & 7));
  return acc;
}
}  // namespace fast
