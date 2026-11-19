// Keep the values >= 128: branchy vs branchless, on unsorted and sorted input.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

using u8 = std::uint8_t;

__attribute__((noinline)) std::size_t keep_branchy(const u8* in, std::size_t n, u8* out) {
  std::size_t k = 0;
  for (std::size_t i = 0; i < n; ++i)
    if (in[i] >= 128) out[k++] = in[i];
  return k;
}

__attribute__((noinline)) std::size_t keep_branchless(const u8* in, std::size_t n, u8* out) {
  std::size_t k = 0;
  for (std::size_t i = 0; i < n; ++i) {
    out[k] = in[i];          // always store
    k += (in[i] >= 128);     // advance only if kept
  }
  return k;
}

template <class F> double ns_per(F f, const std::vector<u8>& v, std::vector<u8>& o, std::size_t& k) {
  double best = 1e30;
  for (int r = 0; r < 21; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    for (int j = 0; j < 20; ++j) k = f(v.data(), v.size(), o.data());
    auto t1 = std::chrono::steady_clock::now();
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / (20.0 * v.size()));
  }
  return best;
}

int main() {
  std::vector<u8> v(1 << 16), o(1 << 16);
  std::mt19937 rng(42);
  for (auto& x : v) x = rng() & 0xff;
  auto s = v;
  std::sort(s.begin(), s.end());
  std::size_t a, b, c, d;
  double ub = ns_per(keep_branchy, v, o, a), sb = ns_per(keep_branchy, s, o, b);
  double ul = ns_per(keep_branchless, v, o, c), sl = ns_per(keep_branchless, s, o, d);
  if (a != b || a != c || a != d) { std::puts("MISMATCH"); return 1; }
  // check contents match
  std::vector<u8> o1(v.size()), o2(v.size());
  keep_branchy(v.data(), v.size(), o1.data()); keep_branchless(v.data(), v.size(), o2.data());
  if (!std::equal(o1.begin(), o1.begin() + a, o2.begin())) { std::puts("MISMATCH2"); return 1; }
  std::printf("kept %zu of %zu\n", a, v.size());
  std::printf("branchy    unsorted %.2f  sorted %.2f ns/elem\n", ub, sb);
  std::printf("branchless unsorted %.2f  sorted %.2f ns/elem\n", ul, sl);
  std::printf("per mispredict ~ %.1f ns\n", (ub - sb) / 0.5);
}
