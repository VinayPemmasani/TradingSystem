// Same observable results from all three chains; refcount returns to 1 after each message.
#include <cassert>
#include <cstdio>
#include <random>
#include "ai.hpp"
#include "mid.hpp"
#include "fast.hpp"
int main() {
  std::mt19937 rng(9); std::vector<std::shared_ptr<Order>> store; hp::OrderPool pool;
  for (std::uint64_t i = 0; i < 300; ++i) {
    Order o{i, std::int64_t(rng() % 200) - 20, std::int64_t(1 + rng() % 12000), 0, 0};   // some px <= 0, some qty > max
    store.push_back(std::make_shared<Order>(o)); pool.slots.push_back(o);
  }
  Stats a, m, h;
  for (int k = 0; k < 100000; ++k) {
    std::uint32_t i = rng() % 300;
    ai::on_msg(store[i], a); mid::on_msg(store[i], m); hp::on_msg(pool[i], h);
    assert(store[i].use_count() == 1);
  }
  assert(a.out == h.out && a.notional == h.notional && a.rejects == h.rejects);
  assert(m.out == h.out && m.notional == h.notional && m.rejects == h.rejects);
  std::printf("test ok: out %lld notional %lld rejects %lld identical\n", (long long)h.out, (long long)h.notional, (long long)h.rejects);
}
