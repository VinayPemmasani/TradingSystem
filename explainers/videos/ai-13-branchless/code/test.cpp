// g++ -O2 -std=c++20 -Wall -Wextra test.cpp -o test && ./test 2>/dev/null
#include "ai.hpp"
#include "variants.hpp"
#include <cstdio>
#include <random>
int main() {
  std::mt19937 rng(1);
  for (int trial = 0; trial < 500; ++trial) {
    std::vector<Tick> t(rng() % 3000);
    for (auto& x : t) x = {std::int64_t(rng() % 1000), int(rng() % 2000) - (rng() % 500 == 0 ? 2000 : 0), Side(rng() & 1)};
    const int big = int(rng() % 1500);
    const Stats a = scan(t, big);
    if (!(a == hot::scan(t.data(), t.size(), big)) || !(a == var::scan_lut(t.data(), t.size(), big)) ||
        !(a == var::scan_branchy_cold(t.data(), t.size(), big))) { std::puts("FAIL"); return 1; }
  }
  std::puts("PASS: 500 random trials (incl. bad ticks): general == hot == lut == branchy+cold");
}
