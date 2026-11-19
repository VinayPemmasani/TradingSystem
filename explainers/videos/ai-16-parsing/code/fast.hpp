#pragma once
// RIGHT: the hot-path version (on screen verbatim, minus the header).
#include <algorithm>
#include <charconv>
#include <cstdint>
#include <string_view>
namespace hot {
using std::int64_t;
struct Quote { std::string_view sym; int64_t px; int64_t qty; };  // px in ticks of 0.01
// "ESZ6,5012.25,17" -> {"ESZ6", 501225, 17}. No allocation, no locale, no exceptions.
// Strict: price is digits with an optional '.' and at most 2 decimals.
bool parse(std::string_view s, Quote& q) {
  const char *p = s.data(), *e = p + s.size();
  const char* c = std::find(p, e, ',');
  const char* f = std::find(c + (c < e), e, ',');
  if (f == e || f-c < 2 || f-c > 17) return false;
  q.sym = std::string_view(p, c - p);
  int64_t t = 0; int nf = -1;   // nf: decimals
  for (++c; c < f; ++c) {
    if (*c == '.' && nf < 0) { nf = 0; continue; }
    const unsigned d = unsigned(*c - '0');
    if (d > 9 || nf == 2) return false;
    t = t * 10 + d; nf += nf >= 0;
  }
  q.px = t * (nf <= 0 ? 100 : nf == 1 ? 10 : 1);
  auto [r, ec] = std::from_chars(f + 1, e, q.qty);
  return ec == std::errc{} && r == e; }
}  // namespace hot
