// Same observable results: identical op stream into both books; top of book compared after every op.
#include <cassert>
#include <cstdio>
#include "ai.hpp"
#include "fast.hpp"
#include "ops.hpp"
int main() {
  const std::int64_t base = 1'000'000; const std::int32_t win = 4096;
  for (std::uint64_t seed = 1; seed <= 5; ++seed) {
    Mix mix; auto ops = make_ops(200000, base, win, seed, mix);
    ai::Book a; hp::FlatBook b(base, win);
    for (auto& o : ops) {
      a.set(o.bid, o.px, o.qty);
      bool ok = b.set(o.bid, o.ticks, o.qty); assert(ok);
      ai::Top x = a.best_bid(); hp::Top y = b.best_bid();
      assert(x.has_value() == y.has_value());
      if (x) assert(x->first == double(y->first) * 0.01 && x->second == y->second);
      x = a.best_ask(); y = b.best_ask();
      assert(x.has_value() == y.has_value());
      if (x) assert(x->first == double(y->first) * 0.01 && x->second == y->second);
    }
    std::printf("seed %llu: %zu ops (add %zu, modify %zu, cancel %zu) identical top of book\n",
                (unsigned long long)seed, ops.size(), mix.add, mix.mod, mix.del);
  }
  hp::FlatBook b(base, win);
  assert(!b.set(true, base - 1, 100) && !b.set(false, base + win, 100));   // outside band rejected
  assert(!b.best_bid() && !b.best_ask());
  std::puts("test ok");
}
