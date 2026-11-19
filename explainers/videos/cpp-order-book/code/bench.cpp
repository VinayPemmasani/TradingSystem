// ns per operation on a pre-generated ITCH-like stream: adds near the touch,
// cancels of random live orders, executes. Steady state of LIVE resting orders.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

#include "book.hpp"
#include "lab/book/order_book.hpp"
#include "lab/book/order_map.hpp"
#include "naive.hpp"

struct Op { char type; bool buy; std::uint64_t id; std::uint32_t price, qty; };

std::vector<Op> make_ops(std::size_t live_target, std::size_t n, std::uint64_t seed) {
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> off(0.0, 8.0);  // ticks from the touch
  std::vector<Op> ops;
  std::vector<std::pair<std::uint64_t, std::uint32_t>> live;  // id, qty
  std::uint64_t next = 1;
  const std::uint32_t mid = 1'000'000, T = 100;
  auto add = [&] {
    const bool buy = rng() & 1;
    int d = std::abs(int(off(rng)));
    if (d > 400) d = 400;
    const std::uint32_t px = buy ? mid - T - d * T : mid + d * T;
    const std::uint32_t q = 100 * (1 + std::uint32_t(rng() % 5));
    ops.push_back({'A', buy, next, px, q});
    live.push_back({next++, q});
  };
  while (live.size() < live_target) add();
  const std::size_t warm = ops.size();
  while (ops.size() - warm < n) {
    const unsigned r = unsigned(rng() % 100);
    const bool grow = live.size() + 50 < live_target ? true
                      : live.size() > live_target + 50 ? false : r < 50;
    if (grow || live.empty()) { add(); continue; }
    const std::size_t k = rng() % live.size();
    auto& [id, q] = live[k];
    if (r % 10 < 8) {  // cancel (delete)
      ops.push_back({'X', false, id, 0, 0});
      live[k] = live.back(); live.pop_back();
    } else {  // execute 100 shares
      ops.push_back({'E', false, id, 0, 100});
      if ((q -= 100) == 0) { live[k] = live.back(); live.pop_back(); }
    }
  }
  return ops;
}

struct Good {
  Book b{1'000'000 - 600 * 100, 100, 1200, 1u << 20};
  void add(const Op& o) { b.add(o.id, o.buy ? Side::Buy : Side::Sell, o.price, o.qty); }
  void cancel(const Op& o) { b.cancel(o.id); }
  void exec(const Op& o) { b.execute(o.id, o.qty); }
  std::uint64_t best() { return b.best_bid().value_or(0) + b.best_ask().value_or(0); }
};
struct Naive {
  NaiveBook b;
  void add(const Op& o) { b.add(o.id, o.buy, o.price, o.qty); }
  void cancel(const Op& o) { b.cancel(o.id); }
  void exec(const Op& o) { b.execute(o.id, o.qty); }
  std::uint64_t best() { return b.best_bid().value_or(0) + b.best_ask().value_or(0); }
};
struct MapList {
  MapListBook b;
  MapList() { b.reserve(1u << 20); }
  void add(const Op& o) { b.add(o.id, o.buy, o.price, o.qty); }
  void cancel(const Op& o) { b.cancel(o.id); }
  void exec(const Op& o) { b.execute(o.id, o.qty); }
  std::uint64_t best() { return b.best_bid().value_or(0) + b.best_ask().value_or(0); }
};
struct Lab {  // libs/book: OrderMap + L2 BookSide (no per-order queues)
  lab::book::OrderMap m{1u << 20};
  lab::book::OrderBook ob;
  void add(const Op& o) {
    const auto s = o.buy ? lab::book::Side::kBuy : lab::book::Side::kSell;
    if (m.insert(o.id, {o.price, o.qty, 0, s})) ob.side(s).add(o.price, o.qty);
  }
  void reduce(std::uint64_t id, std::uint32_t q, bool all) {
    auto* x = m.find(id);
    if (!x) return;
    if (all) q = x->shares;
    const bool gone = q == x->shares;
    ob.side(x->side).reduce(x->price, q, gone);
    if (gone) m.erase_found(x); else x->shares -= q;
  }
  void cancel(const Op& o) { reduce(o.id, 0, true); }
  void exec(const Op& o) { reduce(o.id, o.qty, false); }
  std::uint64_t best() {
    auto* b = ob.bids().best(); auto* a = ob.asks().best();
    return (b ? b->price : 0) + (a ? a->price : 0);
  }
};

template <class B>
double run(const std::vector<Op>& ops, std::size_t warm, std::uint64_t& sink) {
  B* b = new B;
  for (std::size_t i = 0; i < warm; ++i) b->add(ops[i]);
  const auto t0 = std::chrono::steady_clock::now();
  for (std::size_t i = warm; i < ops.size(); ++i) {
    const Op& o = ops[i];
    if (o.type == 'A') b->add(o); else if (o.type == 'X') b->cancel(o); else b->exec(o);
    sink += b->best();  // best bid/ask read after every message
  }
  const auto t1 = std::chrono::steady_clock::now();
  delete b;
  return std::chrono::duration<double, std::nano>(t1 - t0).count() / double(ops.size() - warm);
}

template <class B>
void report(const char* name, std::size_t live, std::size_t n, int reps) {
  std::vector<double> r;
  std::uint64_t sink = 0;
  for (int i = 0; i < reps; ++i) {
    auto ops = make_ops(live, n, 7 + i);
    r.push_back(run<B>(ops, live, sink));
  }
  std::sort(r.begin(), r.end());
  std::printf("%-8s live=%6zu  median %9.1f ns/op  min %9.1f  max %9.1f  (sink %llu)\n", name, live,
              r[r.size() / 2], r[0], r.back(), (unsigned long long)(sink & 1));
}

int main(int argc, char** argv) {
  const std::size_t live = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 10'000;
  const int reps = 7;
  report<Good>("pool", live, 2'000'000, reps);
  report<Lab>("lab-L2", live, 2'000'000, reps);
  report<MapList>("map+hash", live, 2'000'000, reps);
  report<Naive>("naive", live, live >= 10'000 ? 20'000 : 200'000, reps);
}
