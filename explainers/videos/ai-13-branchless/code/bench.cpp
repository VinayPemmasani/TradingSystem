// g++ -O2 -std=c++20 -Wall -Wextra bench.cpp -o bench && taskset -c 2 ./bench 2>/dev/null
#include "ai.hpp"
#include "variants.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>
// noinline wrappers: the timed code is exactly what objdump shows for these symbols.
[[gnu::noinline]] Stats k_general(const std::vector<Tick>& t, int b) { return scan(t, b); }
[[gnu::noinline]] Stats k_hot(const Tick* t, std::size_t n, std::int64_t b) { return hot::scan(t, n, b); }
[[gnu::noinline]] Stats k_bc(const Tick* t, std::size_t n, std::int32_t b) { return var::scan_branchy_cold(t, n, b); }
[[gnu::noinline]] Stats k_lut(const Tick* t, std::size_t n, std::int32_t b) { return var::scan_lut(t, n, b); }
template <class F> static void run(const char* name, F f, std::size_t n, const Stats& ref) {
  std::vector<double> v;
  for (int r = 0; r < 101; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    Stats s = f();
    auto t1 = std::chrono::steady_clock::now();
    if (!(s == ref)) { std::printf("MISMATCH %s\n", name); std::exit(1); }
    v.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / n);
  }
  std::sort(v.begin(), v.end());
  std::printf("  %-13s p50 %6.3f ns/tick  min %6.3f  p99 %6.3f\n", name, v[50], v[0], v[99]);
}
int main() {
  const std::size_t n = 16384;  // 256 KiB of ticks: L2-resident, so we time the core, not DRAM
  const std::int32_t big = 500;
  std::mt19937_64 rng(42);
  struct Mode { const char* name; int kind; };
  for (Mode m : {Mode{"predictable: sides in runs of 256, 1% big", 0},
                 Mode{"in between: side repeats 80%, 10% big", 1},
                 Mode{"unpredictable: random side, 50% big", 2}}) {
    std::vector<Tick> t(n);
    Side side = Side::Buy;
    for (std::size_t i = 0; i < n; ++i) {
      if (m.kind == 0) side = Side((i / 256) & 1);
      if (m.kind == 1 && rng() % 100 >= 80) side = Side(1 - int(side));
      if (m.kind == 2) side = Side(rng() & 1);
      const int pbig = m.kind == 0 ? 1 : m.kind == 1 ? 10 : 50;
      const std::int32_t q = int(rng() % 100) < pbig ? 500 + int(rng() % 1000) : 1 + int(rng() % 499);
      t[i] = {10000 + std::int64_t(rng() % 50), q, side};
    }
    const Stats ref = scan(t, big);
    std::printf("%s\n", m.name);
    run("general", [&] { return k_general(t, big); }, n, ref);
    run("branchless", [&] { return k_hot(t.data(), n, big); }, n, ref);
    run("branchy+cold", [&] { return k_bc(t.data(), n, big); }, n, ref);
    run("lut", [&] { return k_lut(t.data(), n, big); }, n, ref);
  }
}
