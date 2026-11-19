// LEFT: the general-purpose version. Correct; copies its arguments and builds strings with +.
#pragma once
#include "order.hpp"
namespace ai {
std::int32_t limit_for(std::string sym,
                       const Limits& lim);
std::string make_tag(Order o) {
  return o.account + "-" + o.symbol + "-" +
         std::to_string(o.qty) + "@" +
         std::to_string(o.px);
}
bool on_order(Order o, const Limits& lim,
              std::string& tag) {
  if (o.qty > limit_for(o.symbol, lim))
    return false;
  tag = make_tag(o);
  return true;
}
// (end of on-screen snippet)
std::int32_t limit_for(std::string sym, const Limits& lim) {
  for (const auto& e : lim.entries)
    if (e.symbol == sym) return e.max_qty;
  return 0;
}
}  // namespace ai
