#pragma once
// LEFT: the general-purpose version. Orders are shared, so each one is a
// std::shared_ptr, and every handler takes it by value: clear ownership, no
// dangling pointers, whoever holds it last frees it.
#include <memory>
#include "order.hpp"

namespace ai {
[[gnu::noinline]] void publish(std::shared_ptr<Order> o, Stats& s) { s.out += o->qty; }
[[gnu::noinline]] void route(std::shared_ptr<Order> o, Stats& s) {
  s.notional += o->px * o->qty;
  publish(o, s);
}
[[gnu::noinline]] void risk(std::shared_ptr<Order> o, Stats& s) {
  if (o->qty <= s.max_qty) route(o, s); else ++s.rejects;
}
[[gnu::noinline]] void on_msg(std::shared_ptr<Order> o, Stats& s) {
  if (o->px > 0) risk(o, s);
}
}  // namespace ai
