// g++ -O2 -std=c++20 -Wall -Wextra bench.cpp -o bench && taskset -c N ./bench
#include "ai.hpp"
#include "fast.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
[[gnu::noinline, gnu::flatten]] void k_dbl(Levels& L, const double* px, const double* q, std::size_t n) {
  for (std::size_t i = 0; i < n; ++i) apply(L, px[i], q[i]);
}
// decomposition: same double book, no off-tick check (one divide, one round)
[[gnu::noinline]] void k_dbl_nocheck(Levels& L, const double* px, const double* q, std::size_t n) {
  for (std::size_t i = 0; i < n; ++i) {
    const auto j = static_cast<std::size_t>(std::round((px[i] - L.base) / kTick));
    L.qty[j] += q[i]; L.notional += px[i] * q[i];
  }
}
[[gnu::noinline, gnu::flatten]] void k_int(hot::Levels& L, const hot::Ticks* px, const std::int64_t* q, std::size_t n) {
  for (std::size_t i = 0; i < n; ++i) hot::apply(L, px[i], q[i]);
}
template <class F> static double run(F f, std::size_t n, std::vector<double>& v) {
  for (int r = 0; r < 41; ++r) {
    auto t0 = std::chrono::steady_clock::now(); f(); auto t1 = std::chrono::steady_clock::now();
    v.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / n);
  }
  std::sort(v.begin(), v.end()); return v[20];
}
int main() {
  const std::size_t n = 8192, levels = 2000;  // 8192 updates (128 KiB of inputs), 2000-level book
  std::mt19937_64 rng(11);
  std::vector<double> pxd(n), qd(n); std::vector<hot::Ticks> pxt(n); std::vector<std::int64_t> qt(n);
  const hot::Ticks base = 500000;  // 5000.00
  for (std::size_t i = 0; i < n; ++i) {
    const hot::Ticks t = base + hot::Ticks(rng() % levels);
    const std::int64_t q = 1 + std::int64_t(rng() % 100);
    pxt[i] = t; qt[i] = q;
    pxd[i] = double(t) / 100.0;  // what a double feed would carry: nearest double to t/100
    qd[i] = double(q);
  }
  Levels Ld{5000.0, std::vector<double>(levels + 1)};
  hot::Levels Li{base, std::vector<std::int64_t>(levels + 1)};
  std::vector<double> vd, vi, vn;
  Levels Ln{5000.0, std::vector<double>(levels + 1)};
  const double tn = run([&] { k_dbl_nocheck(Ln, pxd.data(), qd.data(), n); }, n, vn);
  const double td = run([&] { k_dbl(Ld, pxd.data(), qd.data(), n); }, n, vd);
  const double ti = run([&] { k_int(Li, pxt.data(), qt.data(), n); }, n, vi);
  // same level quantities?
  for (std::size_t i = 0; i <= levels; ++i)
    if (std::int64_t(Ld.qty[i]) != Li.qty[i]) { std::printf("MISMATCH level %zu\n", i); return 1; }
  std::printf("double + round + eps : p50 %6.3f ns/update  min %6.3f  max %6.3f\n", td, vd.front(), vd.back());
  std::printf("double, no eps check  : p50 %6.3f ns/update  min %6.3f  max %6.3f\n", tn, vn.front(), vn.back());
  std::printf("int64 ticks          : p50 %6.3f ns/update  min %6.3f  max %6.3f\n", ti, vi.front(), vi.back());
  std::printf("notional: double %.6f  vs ticks %lld (/100 = %.2f)\n", Ld.notional, (long long)Li.notional, Li.notional / 100.0);
}
