#include "bench.hpp"
#include "ai.hpp"
#include "fast.hpp"
#include "mid.hpp"
#include "inputs.hpp"
constexpr int N = 400000;
volatile std::int64_t sink;
template <class F> void run(const char* name, F f, double tpn, double ovh) {
  auto ord = make_orders(4096);
  std::vector<std::uint64_t> lat(N);
  for (int i = 0; i < 20000; ++i) sink = f(ord[i & 4095]);
  std::uint64_t a0 = g_allocs;
  for (int i = 0; i < N; ++i) { auto t0 = tsc(); std::int64_t s = f(ord[i & 4095]); auto t1 = tsc(); sink = s; lat[i] = t1 - t0; }
  double apc = double(g_allocs - a0) / N;
  Pct p = pct(lat, tpn, ovh);
  std::printf("%-26s p50 %6.1f ns  p99 %6.1f ns  p99.9 %7.1f ns  mean %6.1f ns  allocs/msg %.2f\n", name, p.p50, p.p99, p.p999, p.mean, apc);
}
int main() {
  double tpn = tsc_per_ns(), ovh = timer_overhead();
  Limits lim = make_limits();
  std::string s; fast::Tag t;
  run("ai: by value + operator+", [&](const Order& o) { return ai::on_order(o, lim, s) ? std::int64_t(s.size()) : 0; }, tpn, ovh);
  run("const& + operator+", [&](const Order& o) { return mid::on_order(o, lim, s) ? std::int64_t(s.size()) : 0; }, tpn, ovh);
  run("fast: const& + to_chars", [&](const Order& o) { return fast::on_order(o, lim, t) ? std::int64_t(t.n) : 0; }, tpn, ovh);
}
