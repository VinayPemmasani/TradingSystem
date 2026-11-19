// RIGHT: the hot-path version. Borrows (const&, string_view), formats into a fixed buffer.
#pragma once
#include <algorithm>
#include <array>
#include <charconv>
#include "order.hpp"
namespace fast {
std::int32_t limit_for(std::string_view sym, const Limits& lim);
char* put(char* p, std::string_view s) {
  return std::copy(s.begin(), s.end(), p);
}
struct Tag { std::array<char, 64> b; int n = 0; };
bool on_order(const Order& o, const Limits& lim,
              Tag& tag) {
  if (o.qty > limit_for(o.symbol, lim))
    return false;
  char* p = tag.b.data(); char* e = p + 64;
  p = put(p, o.account); *p++ = '-';
  p = put(p, o.symbol);  *p++ = '-';
  p = std::to_chars(p, e, o.qty).ptr; *p++ = '@';
  p = std::to_chars(p, e, o.px).ptr;
  tag.n = int(p - tag.b.data());
  return true;
}
// (end of on-screen snippet)
// Constraint, checked at order entry: account <= 16 chars, symbol <= 8 chars.
// Worst case: 16 + 1 + 8 + 1 + 11 (int32) + 1 + 20 (int64) = 58 <= 64.
static_assert(16 + 1 + 8 + 1 + 11 + 1 + 20 <= 64);
std::int32_t limit_for(std::string_view sym, const Limits& lim) {
  for (const auto& e : lim.entries)
    if (e.symbol == sym) return e.max_qty;
  return 0;
}
}  // namespace fast
