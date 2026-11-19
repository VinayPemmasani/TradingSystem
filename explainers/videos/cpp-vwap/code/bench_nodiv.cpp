#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

#include "naive.hpp"
#include "vwap.hpp"

// Poisson trade arrivals with mean gap `gap_ns`; window 1 s.
static std::vector<Trade> make(std::size_t n, std::int64_t gap_ns, std::uint64_t seed) {
  std::mt19937_64 rng(seed);
  std::exponential_distribution<double> gap(1.0 / double(gap_ns));
  std::vector<Trade> v;
  std::int64_t t = 0;
  std::uint32_t px = 1'000'000;
  for (std::size_t i = 0; i < n; ++i) {
    t += std::int64_t(gap(rng));
    px = std::uint32_t(std::int64_t(px) + std::int64_t(rng() % 21) - 10);
    v.push_back({t, px, std::uint32_t(100 * (1 + rng() % 10))});
  }
  return v;
}

template <class F>
void bench(const char* name, std::size_t n, std::int64_t gap, int reps, F make_and_run) {
  std::vector<double> r;
  std::uint64_t sink = 0;
  for (int k = 0; k < reps; ++k) {
    const auto tr = make(n, gap, 11 + k);
    r.push_back(make_and_run(tr, sink));
  }
  std::sort(r.begin(), r.end());
  std::printf("%-12s gap %6lld ns  median %9.1f ns/trade  min %9.1f  max %9.1f  (%llu)\n", name,
              (long long)gap, r[r.size() / 2], r[0], r.back(), (unsigned long long)(sink % 7));
}

int main() {
  constexpr std::int64_t W = 1'000'000'000;
  for (std::int64_t gap : {1'000'000LL, 100'000LL}) {  // ~1,000 and ~10,000 trades in the window
    bench("ring+sums", 2'000'000, gap, 7, [&](const std::vector<Trade>& tr, std::uint64_t& sink) {
      SlidingVwap v(W, 1 << 15);
      const auto t0 = std::chrono::steady_clock::now();
      for (const Trade& t : tr) { v.on_trade(t); sink += v.count(); }
      const auto t1 = std::chrono::steady_clock::now();
      return std::chrono::duration<double, std::nano>(t1 - t0).count() / double(tr.size());
    });
    bench("naive deque", gap == 100'000 ? 50'000 : 200'000, gap, 5,
          [&](const std::vector<Trade>& tr, std::uint64_t& sink) {
      NaiveVwap v(W);
      // warm the window so every measured trade sees a full window
      const std::size_t warm = std::size_t(W / gap) + 100;
      for (std::size_t i = 0; i < warm; ++i) v.on_trade(tr[i]);
      const auto t0 = std::chrono::steady_clock::now();
      for (std::size_t i = warm; i < tr.size(); ++i) { v.on_trade(tr[i]); sink += *v.vwap() + v.high() + v.low(); }
      const auto t1 = std::chrono::steady_clock::now();
      return std::chrono::duration<double, std::nano>(t1 - t0).count() / double(tr.size() - warm);
    });
  }
}
