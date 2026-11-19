#include "bench.hpp"
#include "ai.hpp"
#include "fast.hpp"
#include "inputs.hpp"
constexpr int N = 400000;
volatile std::uint64_t sink;
template <class G> void run(const char* name, int rej, double tpn, double ovh) {
  std::vector<char> bad; auto ord = make_orders(N, rej, &bad);
  G g{make_limits(), {}};
  for (int i = 0; i < 50000; ++i) sink = g.on_order(ord[i]);  // warm, includes rejects so the unwinder is warm
  std::vector<std::uint64_t> lat(N), lat_bad;
  std::uint64_t a0 = g_allocs, allocs_bad = 0;
  for (int i = 0; i < N; ++i) {
    std::uint64_t ab = g_allocs;
    auto t0 = tsc(); bool ok = g.on_order(ord[i]); auto t1 = tsc();
    sink = ok; lat[i] = t1 - t0;
    if (bad[i]) { lat_bad.push_back(t1 - t0); allocs_bad += g_allocs - ab; }
  }
  double apo = double(g_allocs - a0) / N;
  // Throughput: whole loop timed, no per-call timer; best of 7 passes.
  double best = 1e18;
  for (int rep = 0; rep < 7; ++rep) {
    G h{make_limits(), {}}; auto t0 = tsc();
    for (int i = 0; i < N; ++i) h.on_order(ord[i]);
    auto t1 = tsc(); sink = h.out_.ids; best = std::min(best, double(t1 - t0) / tpn / N);
  }
  Pct p = pct(lat, tpn, ovh);
  std::printf("%-12s rej %4.1f%%  p50 %6.1f ns  p99 %7.1f ns  p99.9 %7.1f ns  loop %5.2f ns/order  allocs/order %.3f",
              name, rej / 100.0, p.p50, p.p99, p.p999, best, apo);
  if (!lat_bad.empty()) { Pct b = pct(lat_bad, tpn, ovh); std::printf("  reject-p50 %7.1f ns  reject-p99 %7.1f ns  allocs/reject %.2f", b.p50, b.p99, double(allocs_bad) / lat_bad.size()); }
  std::printf("\n");
}
int main() {
  double tpn = tsc_per_ns(), ovh = timer_overhead();
  run<ai::Gateway>("ai: throw", 0, tpn, ovh);
  run<fast::Gateway>("fast: code", 0, tpn, ovh);
  run<ai::Gateway>("ai: throw", 100, tpn, ovh);
  run<fast::Gateway>("fast: code", 100, tpn, ovh);
}
