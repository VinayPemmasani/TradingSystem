// 8-digit fixed-width fields ("01234567"): SWAR vs digit loop.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>
#include "parse.hpp"
int main() {
  std::mt19937_64 rng(5);
  std::vector<char> buf(8'000'000);
  for (auto& c : buf) c = char('0' + rng() % 10);
  auto run = [&](const char* name, auto f) {
    std::vector<double> r; std::uint64_t sink = 0;
    for (int k = 0; k < 21; ++k) {
      auto t0 = std::chrono::steady_clock::now();
      for (std::size_t i = 0; i < buf.size(); i += 8) sink += f(buf.data() + i);
      auto t1 = std::chrono::steady_clock::now();
      r.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / (buf.size() / 8));
    }
    std::sort(r.begin(), r.end());
    std::printf("%-10s median %6.2f ns  min %6.2f  (%llu)\n", name, r[10], r[0], (unsigned long long)(sink % 7));
  };
  run("loop8", [](const char* p) { std::uint64_t v = 0; for (int i = 0; i < 8; ++i) { unsigned d = unsigned(p[i] - '0'); if (d > 9) return std::uint64_t(0); v = v * 10 + d; } return v; });
  run("swar8", [](const char* p) { std::uint64_t v; std::memcpy(&v, p, 8); return all_digits8(v) ? swar8(v) : 0; });
}
