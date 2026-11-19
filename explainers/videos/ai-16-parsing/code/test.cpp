// g++ -O2 -std=c++20 -Wall -Wextra test.cpp -o test && ./test
#include "fast.hpp"
#include "variants.hpp"
#include <cmath>
#include <cstdio>
#include <random>
int main() {
  std::mt19937_64 rng(5);
  const char* syms[] = {"ESZ6", "NQZ6", "CLF7", "AAPL", "MSFT", "X"};
  for (int i = 0; i < 200000; ++i) {
    const long ticks = long(rng() % 100000000);  // up to 999,999.99
    const int dec = int(rng() % 3);              // 0, 1 or 2 decimals written
    char buf[64];
    long whole = ticks / 100, frac = ticks % 100;
    int n;
    if (dec == 0) { frac = 0; n = std::snprintf(buf, sizeof buf, "%s,%ld,%d", syms[i % 6], whole, int(rng() % 1000)); }
    else if (dec == 1) { frac = frac / 10 * 10; n = std::snprintf(buf, sizeof buf, "%s,%ld.%ld,%d", syms[i % 6], whole, frac / 10, int(rng() % 1000)); }
    else n = std::snprintf(buf, sizeof buf, "%s,%ld.%02ld,%d", syms[i % 6], whole, frac, int(rng() % 1000));
    const std::string line(buf, n);
    const Quote a = parse(line);
    const Quote r = var::parse_regex(line);
    hot::Quote b{};
    if (!hot::parse(line, b)) { std::printf("FAIL reject %s\n", buf); return 1; }
    if (a.sym != b.sym || std::llround(a.px * 100) != b.px || a.qty != b.qty || b.px != whole * 100 + frac ||
        r.sym != a.sym || r.px != a.px || r.qty != a.qty) { std::printf("FAIL %s\n", buf); return 1; }
  }
  // Inputs every version rejects (general: throws; hot: returns false).
  const char* bad[] = {"ESZ6,abc,1", "ESZ6,,1", "ESZ6", "ESZ6,5012.25", "ESZ6,5012.25,", "ESZ6,5012.25,x"};
  for (const char* s : bad) {
    bool threw = false; try { parse(s); } catch (const std::exception&) { threw = true; }
    hot::Quote b{};
    if (!threw || hot::parse(s, b)) { std::printf("FAIL bad-input %s (threw %d)\n", s, threw); return 1; }
  }
  // Strict by design: the hot parser rejects what the feed spec forbids; stod accepts these.
  const char* strict[] = {"ESZ6,5012.255,1", "ESZ6,5.0e3,1", "ESZ6, 5012.25,1"};
  for (const char* s : strict) { hot::Quote b{}; if (hot::parse(s, b)) { std::printf("FAIL strict %s\n", s); return 1; } }
  std::puts("PASS: 200,000 random lines: stringstream == regex == hot (px as ticks); 6 bad lines rejected by both; 3 off-spec lines rejected by hot");
}
