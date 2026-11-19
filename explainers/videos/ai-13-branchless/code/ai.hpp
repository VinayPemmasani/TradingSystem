#pragma once
// LEFT: the general-purpose version (on screen verbatim).
#include "common.hpp"
#include <cstdio>
Stats scan(const std::vector<Tick>& v, int big) {
  Stats s;
  for (const Tick& t : v) {
    if (t.qty <= 0) {
      std::fprintf(stderr, "bad qty %d\n", t.qty);
      ++s.bad; continue;
    }
    if (t.side == Side::Buy) {
      s.buy_vol += t.qty;
      if (t.qty >= big) ++s.big_buys;
    } else {
      s.sell_vol += t.qty;
      if (t.qty >= big) ++s.big_sells;
    }
  }
  return s; }
