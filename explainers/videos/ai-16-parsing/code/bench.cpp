// g++ -O2 -std=c++20 -Wall -Wextra bench.cpp -o bench && taskset -c N ./bench
#include "alloc_count.hpp"
#include "fast.hpp"
#include "variants.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <random>
#include <vector>
static std::vector<std::string> lines;
[[gnu::noinline]] long k_ss() { long s = 0; for (auto& l : lines) { Quote q = parse(l); s += std::llround(q.px * 100) + q.qty + long(q.sym.size()); } return s; }
[[gnu::noinline]] long k_re() { long s = 0; for (auto& l : lines) { Quote q = var::parse_regex(l); s += std::llround(q.px * 100) + q.qty + long(q.sym.size()); } return s; }
[[gnu::noinline]] long k_fcd() { long s = 0; for (auto& l : lines) { std::string_view y; double p; long qn; if (!var::parse_fc_double(l, y, p, qn)) return -1; s += std::llround(p * 100) + qn + long(y.size()); } return s; }
[[gnu::noinline]] long k_hot() { long s = 0; for (auto& l : lines) { hot::Quote q; if (!hot::parse(l, q)) return -1; s += q.px + q.qty + long(q.sym.size()); } return s; }
template <class F> void run(const char* name, F f, long ref) {
  std::vector<double> v; unsigned long allocs = 0;
  for (int r = 0; r < 31; ++r) {
    const unsigned long a0 = g_allocs;
    auto t0 = std::chrono::steady_clock::now(); long s = f(); auto t1 = std::chrono::steady_clock::now();
    allocs = g_allocs - a0;
    if (s != ref) { std::printf("MISMATCH %s\n", name); std::exit(1); }
    v.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / lines.size());
  }
  std::sort(v.begin(), v.end());
  std::printf("  %-28s p50 %7.1f ns/line = %6.1f ns/field  min %7.1f  max %7.1f  allocs/line %.2f\n", name, v[15], v[15] / 3,
              v[0], v[30], double(allocs) / lines.size());
}
int main() {
  std::mt19937_64 rng(5);
  const char* syms[] = {"ESZ6", "NQZ6", "CLF7", "ZNH7"};
  for (int i = 0; i < 4096; ++i) {
    char buf[64];
    const long t = 500000 + long(rng() % 20000);
    const int n = std::snprintf(buf, sizeof buf, "%s,%ld.%02ld,%d", syms[i % 4], t / 100, t % 100, 1 + int(rng() % 500));
    lines.emplace_back(buf, n);
  }
  const long ref = k_hot();
  std::printf("%zu lines like \"%s\", 3 fields each\n", lines.size(), lines[0].c_str());
  run("stringstream+getline+stod", k_ss, ref);
  run("std::regex + stod/stoi", k_re, ref);
  run("from_chars (double px)", k_fcd, ref);
  run("hot: digit loop + from_chars", k_hot, ref);
}
