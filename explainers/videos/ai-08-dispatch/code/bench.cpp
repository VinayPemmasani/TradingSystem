#include "bench.hpp"
#include "ai_api.hpp"
#include "fast.hpp"
#include <random>
constexpr int B = 256, REPS = 200;   // 256 ticks x 64 instruments per pass
volatile int sink;
template <class F> double best_ns(F f, int calls) {
  double best = 1e18;
  for (int pass = 0; pass < 15; ++pass) {
    auto t0 = tsc(); for (int r = 0; r < REPS; ++r) f(); auto t1 = tsc();
    best = std::min(best, double(t1 - t0) / REPS / calls);
  }
  return best;
}
int main() {
  double tpn = tsc_per_ns();
  std::mt19937 r(5); std::vector<Prices> mid(B); std::vector<int> flat(B * kN); Prices out{};
  for (auto& p : mid) for (auto& m : p) m = 99000 + int(r() % 2000);
  for (int i = 0; i < B * kN; ++i) flat[i] = mid[i / kN][i % kN];
  const ai::Quoter& qa = ai::make_clamp(3, 99500, 100500);
  fast::Clamp qf{3, 99500, 100500};
  ai::QuoteFn fn = [qf](int m) { return qf.quote(m); };
  std::uint64_t a0 = g_allocs;
  auto batch = [&](auto&& call) { return best_ns([&] { for (int t = 0; t < B; ++t) { call(mid[t]); sink = out[t & (kN - 1)]; } }, B * kN) / tpn; };
  double v  = batch([&](const Prices& m) { ai::quote_all(qa, m, out); });
  double sf = batch([&](const Prices& m) { ai::quote_all(fn, m, out); });
  double t  = batch([&](const Prices& m) { fast::quote_all(qf, m, out); });
  double vs = best_ns([&] { sink = ai::run_serial(qa, flat.data(), B * kN); }, B * kN) / tpn;
  double ts = best_ns([&] { sink = fast::run_serial(qf, flat.data(), B * kN); }, B * kN) / tpn;
  std::printf("batch: virtual %.3f  std::function %.3f  template %.3f ns/call   serial: virtual %.3f  template %.3f ns/call   allocs %llu\n",
              v, sf, t, vs, ts, (unsigned long long)(g_allocs - a0));
}
