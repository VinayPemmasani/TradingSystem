#include <cassert>
#include <cstdio>
#include "ai.hpp"
#include "fast.hpp"
#include "inputs.hpp"
int main() {
  Book b = make_book(); auto ticks = make_ticks(10000);
  fast::Band band; std::vector<Level> vec; vec.reserve(kMaxDepth);
  for (auto t : ticks) {
    auto a = ai::levels_in_band(b, t.lo, t.hi);
    fast::levels_in_band(b, t.lo, t.hi, band);
    fast::levels_in_band(b, t.lo, t.hi, vec);
    if (int(a.size()) != band.n || a.size() != vec.size()) { std::puts("FAIL size"); return 1; }
    for (int i = 0; i < band.n; ++i)
      if (a[i].px != band.v[i].px || a[i].qty != band.v[i].qty || a[i].px != vec[i].px) { std::puts("FAIL elem"); return 1; }
  }
  std::puts("PASS: all three return identical levels for 10000 ticks");
}
