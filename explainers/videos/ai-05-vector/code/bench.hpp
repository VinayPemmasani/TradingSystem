// Shared bench helpers: rdtsc timing calibrated to ns, an allocation counter, percentiles.
#pragma once
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <vector>
#include <x86intrin.h>

extern std::uint64_t g_allocs_ext;  // counted by the replaced operator new in alloc_count.cpp
#define g_allocs g_allocs_ext

inline std::uint64_t tsc() { unsigned a; return __rdtscp(&a); }

inline double tsc_per_ns() {
  using C = std::chrono::steady_clock;
  auto t0 = C::now(); auto c0 = tsc();
  while (C::now() - t0 < std::chrono::milliseconds(100)) {}
  auto c1 = tsc(); auto t1 = C::now();
  return double(c1 - c0) / std::chrono::duration<double, std::nano>(t1 - t0).count();
}

struct Pct { double p50, p99, p999, mean; };
inline Pct pct(std::vector<std::uint64_t>& v, double tpn, double overhead_ticks) {
  std::sort(v.begin(), v.end());
  auto at = [&](double q) { double x = (double(v[std::size_t(q * (v.size() - 1))]) - overhead_ticks) / tpn; return x < 0 ? 0 : x; };
  double s = 0; for (auto x : v) s += double(x); 
  return {at(0.50), at(0.99), at(0.999), (s / v.size() - overhead_ticks) / tpn};
}
// Timer overhead: median of back-to-back reads.
inline double timer_overhead() {
  std::vector<std::uint64_t> v(100000);
  for (auto& x : v) { auto a = tsc(); auto b = tsc(); x = b - a; }
  std::sort(v.begin(), v.end()); return double(v[v.size() / 2]);
}
