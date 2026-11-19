#pragma once
// RIGHT: the hot-path version. One owner: a pool of Orders that lives for the
// whole session. Handlers borrow a plain reference; the message carries an index.
#include <cstdint>
#include <vector>
#include "order.hpp"

namespace hp {
[[gnu::noinline]] void publish(const Order& o, Stats& s) { s.out += o.qty; }
[[gnu::noinline]] void route(const Order& o, Stats& s) {
  s.notional += o.px * o.qty;
  publish(o, s);
}
[[gnu::noinline]] void risk(const Order& o, Stats& s) {
  if (o.qty <= s.max_qty) route(o, s); else ++s.rejects;
}
[[gnu::noinline]] void on_msg(const Order& o, Stats& s) {
  if (o.px > 0) risk(o, s);
}
struct OrderPool {                        // the single owner
  std::vector<Order> slots;               // sized at startup
  Order& operator[](std::uint32_t i) { return slots[i]; }
};
}  // namespace hp
