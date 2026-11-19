// ai-03: shared_ptr<Order> by value through a 4-handler chain vs plain references into a pool.
// Build: g++ -O2 -std=c++20 -Wall -Wextra -pthread bench.cpp -o bench
// Run:   taskset -c 3 ./bench threads   (a helper thread was started once, like any real app)
//        taskset -c 3 ./bench single    (process never starts a thread)
#include <cstring>
#include <random>
#include <thread>
#include "harness.hpp"
#include "ai.hpp"
#include "mid.hpp"
#include "fast.hpp"

int main(int argc, char** argv) {
  const bool threads = !(argc > 1 && !std::strcmp(argv[1], "single"));
  if (threads) std::thread([] {}).join();   // after this, libstdc++ uses atomic refcounts
  const std::size_t N = 1000, T = 2'000'000, RUNS = 5;
  const double ghz = hz::tsc_ghz();
  std::vector<std::shared_ptr<Order>> store(N);
  hp::OrderPool pool{std::vector<Order>(N)};
  std::mt19937_64 rng(3);
  for (std::size_t i = 0; i < N; ++i) {
    Order o{i, std::int64_t(10000 + rng() % 100), std::int64_t(1 + rng() % 12000), std::uint32_t(i % 7), 0};
    store[i] = std::make_shared<Order>(o); pool.slots[i] = o;
  }
  std::vector<std::uint32_t> msg(T);
  for (auto& m : msg) m = std::uint32_t(rng() % N);
  Stats sa, sm, sh;
  std::vector<double> ta, tm, th;
  for (std::size_t r = 0; r < RUNS; ++r) {
    ta.push_back(hz::batch_median(T, 1000, ghz, [&](std::size_t k) { ai::on_msg(store[msg[k]], sa); }));
    tm.push_back(hz::batch_median(T, 1000, ghz, [&](std::size_t k) { mid::on_msg(store[msg[k]], sm); }));
    th.push_back(hz::batch_median(T, 1000, ghz, [&](std::size_t k) { hp::on_msg(pool[msg[k]], sh); }));
  }
  // one message at a time
  std::vector<std::uint64_t> la(T / 4), lh(T / 4), l0(T / 4); unsigned aux;
  auto stamp = [] { _mm_lfence(); return __rdtsc(); };
  for (std::size_t k = 0; k < la.size(); ++k) { auto t0 = stamp(); l0[k] = __rdtscp(&aux) - t0; }
  for (std::size_t k = 0; k < la.size(); ++k) { auto t0 = stamp(); ai::on_msg(store[msg[k]], sa); la[k] = __rdtscp(&aux) - t0; }
  for (std::size_t k = 0; k < lh.size(); ++k) { auto t0 = stamp(); hp::on_msg(pool[msg[k]], sh); lh[k] = __rdtscp(&aux) - t0; }
  // raw cost of one atomic RMW vs a plain add (dependent chain on one counter)
  std::atomic<long> ac{0}; volatile long pc = 0; const std::size_t K = 20'000'000;
  std::uint64_t t0 = __rdtsc();
  for (std::size_t k = 0; k < K; ++k) ac.fetch_add(1, std::memory_order_acq_rel);
  double ns_atomic = double(__rdtsc() - t0) / ghz / double(K);
  t0 = __rdtsc();
  for (std::size_t k = 0; k < K; ++k) pc = pc + 1;
  double ns_plain = double(__rdtsc() - t0) / ghz / double(K);

  bool same = sa.out == sh.out && sa.notional == sh.notional && sa.rejects == sh.rejects;
  auto med = [](std::vector<double> v) { std::sort(v.begin(), v.end()); return v[v.size() / 2]; };
  auto mn = [](const std::vector<double>& v) { return *std::min_element(v.begin(), v.end()); };
  auto mx = [](const std::vector<double>& v) { return *std::max_element(v.begin(), v.end()); };
  std::printf("mode=%s orders=%zu msgs=%zu x %zu runs  same=%s  use_count(store[0])=%ld\n", threads ? "threads" : "single", N, T, RUNS, same ? "yes" : "NO", store[0].use_count());
  std::printf("shared_ptr by value  b2b ns/msg %5.1f (min %.1f max %.1f)  p50 %5.1f p99 %5.1f ns\n", med(ta), mn(ta), mx(ta), hz::pct(la, .5) / ghz, hz::pct(la, .99) / ghz);
  std::printf("shared_ptr by const& b2b ns/msg %5.1f (min %.1f max %.1f)\n", med(tm), mn(tm), mx(tm));
  std::printf("pool + Order&        b2b ns/msg %5.1f (min %.1f max %.1f)  p50 %5.1f p99 %5.1f ns\n", med(th), mn(th), mx(th), hz::pct(lh, .5) / ghz, hz::pct(lh, .99) / ghz);
  std::printf("timer overhead p50 %.1f ns; lock xadd (dependent) %.2f ns, plain add via memory %.2f ns\n", hz::pct(l0, .5) / ghz, ns_atomic, ns_plain);
}
