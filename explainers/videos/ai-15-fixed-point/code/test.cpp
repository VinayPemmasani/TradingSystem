// g++ -O2 -std=c++20 -Wall -Wextra test.cpp -o test && ./test
// Same level quantities from both versions on random on-grid updates; off-grid prices are rejected by the
// general version, and cannot be represented in the hot one (the edge parser rejects them, see ai-16).
#include "ai.hpp"
#include "fast.hpp"
#include <cstdio>
#include <random>
int main() {
  std::mt19937_64 rng(2);
  for (int trial = 0; trial < 100; ++trial) {
    const std::size_t levels = 1 + rng() % 5000;
    const hot::Ticks base = 1 + std::int64_t(rng() % 1000000);
    Levels Ld{double(base) / 100.0, std::vector<double>(levels)};
    hot::Levels Li{base, std::vector<std::int64_t>(levels)};
    for (int k = 0; k < 2000; ++k) {
      const hot::Ticks t = base + std::int64_t(rng() % levels);
      const std::int64_t q = 1 + std::int64_t(rng() % 1000);
      apply(Ld, double(t) / 100.0, double(q));
      hot::apply(Li, t, q);
    }
    for (std::size_t i = 0; i < levels; ++i)
      if (std::int64_t(Ld.qty[i]) != Li.qty[i]) { std::printf("FAIL trial %d level %zu\n", trial, i); return 1; }
  }
  bool threw = false; Levels L{100.0, std::vector<double>(10)};
  try { apply(L, 100.005, 1); } catch (const std::invalid_argument&) { threw = true; }
  if (!threw) { std::puts("FAIL: off-tick accepted"); return 1; }
  std::puts("PASS: 100 random books x 2000 updates, same level quantities; off-tick price rejected");
}
