// MIDDLE (bench only): LEFT with const& and string_view, but still std::string + and to_string.
#pragma once
#include "order.hpp"
#include "fast.hpp"
namespace mid {
inline std::string make_tag(const Order& o) {
  return o.account + "-" + o.symbol + "-" + std::to_string(o.qty) + "@" + std::to_string(o.px);
}
inline bool on_order(const Order& o, const Limits& lim, std::string& tag) {
  if (o.qty > fast::limit_for(o.symbol, lim)) return false;
  tag = make_tag(o);
  return true;
}
}  // namespace mid
