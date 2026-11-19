#pragma once
// Two extra variants, measured for honesty.
#include "fast.hpp"
namespace var {
// (a) lookup table: side indexes a 2-entry array. Repeated sides chain through
//     store-to-load forwarding.
inline Stats scan_lut(const Tick* t, std::size_t n, std::int32_t big) {
  std::int64_t vol[2] = {0, 0}, nb[2] = {0, 0}, bad = 0;
  for (std::size_t i = 0; i < n; ++i) {
    if (t[i].qty <= 0) [[unlikely]] { hot::on_bad(t[i]); ++bad; continue; }
    const unsigned s = static_cast<unsigned>(t[i].side);
    vol[s] += t[i].qty;
    nb[s] += t[i].qty >= big;
  }
  return {vol[0], vol[1], nb[0], nb[1], bad};
}
// (b) keep the if/else on side, but move the rare path out of line and
//     accumulate in locals. Isolates "branchy" from "rare path inline".
inline Stats scan_branchy_cold(const Tick* t, std::size_t n, std::int32_t big) {
  std::int64_t bv = 0, sv = 0, bb = 0, sb = 0, bad = 0;
  for (std::size_t i = 0; i < n; ++i) {
    const std::int32_t q = t[i].qty;
    if (q <= 0) [[unlikely]] { hot::on_bad(t[i]); ++bad; continue; }
    if (t[i].side == Side::Buy) { bv += q; if (q >= big) ++bb; }
    else                        { sv += q; if (q >= big) ++sb; }
  }
  return {bv, sv, bb, sb, bad};
}
}  // namespace var
