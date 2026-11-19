#pragma once
// Shared bench helpers: TSC clock, allocation counter (replaced operator new), percentiles.
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <vector>
#include <x86intrin.h>

namespace hz {
inline std::uint64_t g_news = 0, g_bytes = 0;  // counted by the replaced operator new below
inline double tsc_ghz() {
  auto c0 = std::chrono::steady_clock::now(); std::uint64_t t0 = __rdtsc();
  while (std::chrono::steady_clock::now() - c0 < std::chrono::milliseconds(100)) {}
  double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - c0).count();
  return double(__rdtsc() - t0) / ns;
}
inline double pct(std::vector<std::uint64_t>& v, double p) {
  std::sort(v.begin(), v.end());
  return double(v[std::size_t(p * double(v.size() - 1))]);
}
// Back-to-back cost robust to preemption on a shared box: time batches of B calls,
// return the median batch's ns per call. f(k) handles item k.
template <class F> inline double batch_median(std::size_t n, std::size_t B, double ghz, F&& f) {
  std::vector<double> v; v.reserve(n / B + 1);
  for (std::size_t k = 0; k + B <= n; k += B) {
    std::uint64_t t0 = __rdtsc();
    for (std::size_t j = k; j < k + B; ++j) f(j);
    v.push_back(double(__rdtsc() - t0) / ghz / double(B));
  }
  std::sort(v.begin(), v.end());
  return v[v.size() / 2];
}
template <class T> inline void keep(const T& x) { asm volatile("" : : "g"(&x) : "memory"); }
}  // namespace hz

#ifdef HZ_COUNT_NEW
__attribute__((noinline)) void* operator new(std::size_t n) {
  ++hz::g_news; hz::g_bytes += n;
  if (void* p = std::malloc(n ? n : 1)) return p;
  throw std::bad_alloc();
}
__attribute__((noinline)) void operator delete(void* p) noexcept { std::free(p); }
__attribute__((noinline)) void operator delete(void* p, std::size_t) noexcept { std::free(p); }
#endif
