// Same observable results: identical message stream into both; live orders compared in order.
#include <cassert>
#include <cstdio>
#include <random>
#include "ai.hpp"
#include "fast.hpp"
int main() {
  ai::Orders a(5000); hp::Orders b(5000); std::mt19937 rng(2);
  for (std::uint64_t k = 1; k <= 300000; ++k) {
    if (a.size() < 4000 && (a.size() == 0 || rng() % 5 < 3)) {
      NewMsg m{k, k, std::int64_t(rng() % 1000), std::int64_t(1 + rng() % 50), 1, std::uint32_t(rng() & 1)};
      a.on_new(m); bool ok = b.on_new(m); assert(ok);
    } else { std::size_t i = rng() % a.size(); a.on_cancel(i); b.on_cancel(i); }
    assert(a.size() == b.size());
  }
  for (std::size_t i = 0; i < a.size(); ++i) {
    const Order &x = a.at(i), &y = b.at(i);
    assert(x.id == y.id && x.px == y.px && x.qty == y.qty && x.side == y.side && x.symbol == y.symbol && x.user == y.user);
  }
  hp::Orders full(2); NewMsg m{1, 1, 1, 1, 1, 1};
  assert(full.on_new(m) && full.on_new(m) && !full.on_new(m));   // pool full: rejected, no malloc
  std::printf("test ok: %zu live orders identical\n", a.size());
}
