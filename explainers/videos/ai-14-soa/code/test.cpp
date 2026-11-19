// g++ -O2 -std=c++20 -Wall -Wextra test.cpp -o test && ./test
#include "variants.hpp"
#include <cstdio>
#include <random>
int main() {
  std::mt19937_64 rng(9);
  for (int trial = 0; trial < 300; ++trial) {
    const std::size_t n = rng() % 5000;
    std::vector<Order> aos(n); std::vector<var::OrderHot> hot(n); BookHot soa;
    for (std::size_t i = 0; i < n; ++i) {
      Order& o = aos[i];
      o.price = 100.0 + double(rng() % 200) * 0.25; o.qty = std::int64_t(rng() % 100);
      o.side = Side(rng() & 1); o.active = rng() & 1;
      const std::uint8_t lb = o.active && o.side == Side::Buy;
      hot[i] = {o.price, o.qty, lb};
      soa.px.push_back(o.price); soa.qty.push_back(o.qty); soa.live_bid.push_back(lb);
    }
    const double px = 100.0 + double(rng() % 200) * 0.25;
    const auto a = bid_depth(aos, px);
    if (a != bid_depth(soa, px) || a != var::bid_depth_hot(hot, px) || a != var::bid_depth_aos_branchless(aos, px)) {
      std::puts("FAIL"); return 1; }
  }
  std::puts("PASS: 300 random books: AoS == AoS branchless == hot/cold == SoA");
}
