#pragma once
#include <random>
#include <vector>
#include "common.hpp"
inline Limits make_limits() { return {1000, 900000, 1100000}; }
// reject_per_10k: how many orders in 10,000 fail validation (half bad qty, half bad price).
inline std::vector<Order> make_orders(int n, int reject_per_10k, std::vector<char>* bad = nullptr) {
  std::mt19937_64 r(11); std::vector<Order> v(n); if (bad) bad->assign(n, 0);
  for (int i = 0; i < n; ++i) {
    Order& o = v[i]; o.id = 1000 + i; o.qty = 1 + int(r() % 1000); o.px = 900000 + std::int64_t(r() % 200001);
    if (int(r() % 10000) < reject_per_10k) { if (bad) (*bad)[i] = 1; if (r() & 1) o.qty = 1000 + 1 + int(r() % 500); else o.px = 1100001 + std::int64_t(r() % 1000); }
  }
  return v;
}
