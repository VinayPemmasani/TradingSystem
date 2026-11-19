#pragma once
// RIGHT: the hot-path version (on screen verbatim, minus this header).
#include "common.hpp"
#include <cstddef>
#include <cstdio>
namespace hot {
using std::int64_t; using std::size_t;
[[gnu::cold, gnu::noinline]]
inline void on_bad(const Tick& t) { std::fprintf(stderr, "bad qty %d\n", t.qty); }
inline Stats scan(const Tick* t, size_t n, int64_t big) {
  int64_t vol = 0, sv = 0, nb = 0, sb = 0, bad = 0;
  for (size_t i = 0; i < n; ++i) {
    const int64_t q = t[i].qty;
    if (q <= 0) [[unlikely]] {
      on_bad(t[i]); ++bad; continue; }
    const int64_t sell = -int64_t(t[i].side);
    const int64_t b = q >= big;
    vol += q;   sv += q & sell;
    nb  += b;   sb += b & sell;
  }
  return {vol - sv, sv, nb - sb, sb, bad};
}
}  // namespace hot
