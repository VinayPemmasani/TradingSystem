#include "bench.hpp"
#include "ai.hpp"
#include "fast.hpp"
#include "inputs.hpp"
constexpr int N = 400000;
volatile std::int64_t sink;
template <class F> void run(const char* name, F f, double tpn, double ovh) {
  auto ticks = make_ticks(4096);
  std::vector<std::uint64_t> lat(N);
  for (int i = 0; i < 20000; ++i) sink = f(ticks[i & 4095]);  // warm
  std::uint64_t a0 = g_allocs;
  for (int i = 0; i < N; ++i) {
    auto t0 = tsc(); std::int64_t s = f(ticks[i & 4095]); auto t1 = tsc();
    sink = s; lat[i] = t1 - t0;
  }
  double apc = double(g_allocs - a0) / N;
  Pct p = pct(lat, tpn, ovh);
  std::printf("%-22s p50 %6.1f ns  p99 %6.1f ns  p99.9 %7.1f ns  mean %6.1f ns  allocs/call %.2f\n",
              name, p.p50, p.p99, p.p999, p.mean, apc);
}
int main() {
  double tpn = tsc_per_ns(), ovh = timer_overhead();
  Book b = make_book();
  fast::Band band; std::vector<Level> vec; vec.reserve(kMaxDepth);
  auto sum = [](auto& v, int n) { std::int64_t s = 0; for (int i = 0; i < n; ++i) s += v[i].qty; return s; };
  run("ai: fresh vector", [&](Tick t) { auto v = ai::levels_in_band(b, t.lo, t.hi); return sum(v, int(v.size())); }, tpn, ovh);
  run("reserved vector+clear", [&](Tick t) { fast::levels_in_band(b, t.lo, t.hi, vec); return sum(vec, int(vec.size())); }, tpn, ovh);
  run("fast: array+size", [&](Tick t) { fast::levels_in_band(b, t.lo, t.hi, band); return sum(band.v, band.n); }, tpn, ovh);
}
