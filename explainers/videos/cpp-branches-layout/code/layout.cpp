// AoS vs hot/cold split vs SoA: sum price*qty over 1M orders.
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

struct Order {              // 64 bytes: one cache line
  std::uint32_t price, qty; // hot
  std::uint64_t id, ts_in, ts_ack;
  char account[16], symbol[8], pad[8];  // cold
};
static_assert(sizeof(Order) == 64);

struct Hot { std::uint32_t price, qty; };          // 8 bytes
struct Cold { std::uint64_t id, ts_in, ts_ack; char account[16], symbol[8], pad[8]; };

__attribute__((noinline)) std::uint64_t notional_aos(const Order* o, std::size_t n) {
  std::uint64_t s = 0;
  for (std::size_t i = 0; i < n; ++i) s += std::uint64_t(o[i].price) * o[i].qty;
  return s;
}
__attribute__((noinline)) std::uint64_t notional_hot(const Hot* h, std::size_t n) {
  std::uint64_t s = 0;
  for (std::size_t i = 0; i < n; ++i) s += std::uint64_t(h[i].price) * h[i].qty;
  return s;
}
__attribute__((noinline)) std::uint64_t notional_soa(const std::uint32_t* p, const std::uint32_t* q, std::size_t n) {
  std::uint64_t s = 0;
  for (std::size_t i = 0; i < n; ++i) s += std::uint64_t(p[i]) * q[i];
  return s;
}

template <class F> double ns_per(F f, std::size_t n, std::uint64_t& out) {
  double best = 1e30;
  for (int r = 0; r < 15; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    out = f();
    auto t1 = std::chrono::steady_clock::now();
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / n);
  }
  return best;
}

int main() {
  const std::size_t n = 1 << 20;
  std::vector<Order> aos(n); std::vector<Hot> hot(n); std::vector<Cold> cold(n);
  std::vector<std::uint32_t> px(n), qty(n);
  std::mt19937 rng(7);
  for (std::size_t i = 0; i < n; ++i) {
    std::uint32_t p = 1000000 + rng() % 10000, q = 100 * (1 + rng() % 10);
    aos[i].price = p; aos[i].qty = q; aos[i].id = i;
    hot[i] = {p, q}; cold[i].id = i; px[i] = p; qty[i] = q;
  }
  std::uint64_t a, b, c;
  double ta = ns_per([&] { return notional_aos(aos.data(), n); }, n, a);
  double tb = ns_per([&] { return notional_hot(hot.data(), n); }, n, b);
  double tc = ns_per([&] { return notional_soa(px.data(), qty.data(), n); }, n, c);
  if (a != b || a != c) { std::puts("MISMATCH"); return 1; }
  std::printf("AoS 64B    %.2f ns/order  (%zu MB)\n", ta, n * 64 >> 20);
  std::printf("hot 8B     %.2f ns/order  (%zu MB)\n", tb, n * 8 >> 20);
  std::printf("SoA        %.2f ns/order  (%zu MB)\n", tc, n * 8 >> 20);
}
