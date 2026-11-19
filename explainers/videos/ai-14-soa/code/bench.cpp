// g++ -O2 -std=c++20 -Wall -Wextra bench.cpp -o bench && taskset -c N ./bench [n_orders]
#include "variants.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
[[gnu::noinline]] std::int64_t k_aos(const std::vector<Order>& b, double px) { return bid_depth(b, px); }
[[gnu::noinline]] std::int64_t k_aos_bl(const std::vector<Order>& b, double px) { return var::bid_depth_aos_branchless(b, px); }
[[gnu::noinline]] std::int64_t k_hot(const std::vector<var::OrderHot>& h, double px) { return var::bid_depth_hot(h, px); }
[[gnu::noinline]] std::int64_t k_soa(const BookHot& b, double px) { return bid_depth(b, px); }
template <class F> static void run(const char* name, std::size_t bytes, F f, std::size_t n, std::int64_t ref) {
  std::vector<double> v;
  for (int r = 0; r < 21; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    std::int64_t s = f();
    auto t1 = std::chrono::steady_clock::now();
    if (s != ref) { std::printf("MISMATCH %s\n", name); std::exit(1); }
    v.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / n);
  }
  std::sort(v.begin(), v.end());
  std::printf("  %-18s %4zu B/elem  %8.1f MB  p50 %6.3f ns/elem  min %6.3f  max %6.3f\n", name, bytes,
              double(bytes) * n / 1e6, v[10], v[0], v[20]);
}
int main(int argc, char** argv) {
  const std::size_t n = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : (1u << 20);
  std::mt19937_64 rng(3);
  std::vector<Order> aos(n);
  std::vector<var::OrderHot> hot(n);
  BookHot soa; soa.px.resize(n); soa.qty.resize(n); soa.live_bid.resize(n);
  for (std::size_t i = 0; i < n; ++i) {
    Order& o = aos[i];
    o.symbol = "ESZ6"; o.account = "ACC-" + std::to_string(i % 1000);
    o.id = i; o.created = o.updated = std::chrono::system_clock::now();
    o.price = 5000.0 + double(rng() % 400) * 0.25;
    o.qty = 1 + std::int64_t(rng() % 50);
    o.side = Side(rng() & 1); o.active = rng() % 10 != 0; o.ioc = false; o.post_only = rng() & 1;
    const std::uint8_t lb = o.active && o.side == Side::Buy;
    hot[i] = {o.price, o.qty, lb};
    soa.px[i] = o.price; soa.qty[i] = o.qty; soa.live_bid[i] = lb;
  }
  const double px = 5050.0;
  const std::int64_t ref = bid_depth(aos, px);
  std::printf("n = %zu orders, sizeof(Order) = %zu, sizeof(OrderHot) = %zu, depth = %lld\n", n, sizeof(Order),
              sizeof(var::OrderHot), (long long)ref);
  run("AoS (general)", sizeof(Order), [&] { return k_aos(aos, px); }, n, ref);
  run("AoS, branchless", sizeof(Order), [&] { return k_aos_bl(aos, px); }, n, ref);
  run("hot/cold split", sizeof(var::OrderHot), [&] { return k_hot(hot, px); }, n, ref);
  run("SoA (hot path)", 8 + 8 + 1, [&] { return k_soa(soa, px); }, n, ref);
}
