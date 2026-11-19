// Sorted vs unsorted data, branchy vs branchless sum.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

__attribute__((noinline)) long sum_branchy(const std::uint8_t* v, std::size_t n) {
  long sum = 0;
  for (std::size_t i = 0; i < n; ++i) {
    if (v[i] >= 128) sum += v[i];
    asm volatile("" ::: "memory");  // keep the loop scalar and the branch a branch
  }
  return sum;
}

__attribute__((noinline)) long sum_branchless(const std::uint8_t* v, std::size_t n) {
  long sum = 0;
  for (std::size_t i = 0; i < n; ++i) {
    long x = v[i];
    long mask = -static_cast<long>(x >= 128);  // all ones or zero
    sum += x & mask;
    asm volatile("" ::: "memory");
  }
  return sum;
}

template <class F> double ns_per(F f, const std::vector<std::uint8_t>& v, long& out) {
  double best = 1e30;
  for (int r = 0; r < 15; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    long s = 0;
    for (int k = 0; k < 20; ++k) s += f(v.data(), v.size());
    auto t1 = std::chrono::steady_clock::now();
    out = s;
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / (20.0 * v.size()));
  }
  return best;
}

int main() {
  std::vector<std::uint8_t> v(1 << 16);
  std::mt19937 rng(42);
  for (auto& x : v) x = rng() & 0xff;
  auto s = v;
  std::sort(s.begin(), s.end());
  long a, b, c, d;
  double ub = ns_per(sum_branchy, v, a), sb = ns_per(sum_branchy, s, b);
  double ul = ns_per(sum_branchless, v, c), sl = ns_per(sum_branchless, s, d);
  if (a != b || a != c || a != d) { std::puts("MISMATCH"); return 1; }
  std::printf("branchy    unsorted %.2f ns/elem  sorted %.2f ns/elem\n", ub, sb);
  std::printf("branchless unsorted %.2f ns/elem  sorted %.2f ns/elem\n", ul, sl);
  std::printf("mispredict cost est: %.1f ns (half the elements mispredict)\n", (ub - sb) / 0.5);
}
