#pragma once
// Middle ground (not on screen as RIGHT): same shared_ptr store, handlers take const&.
#include <memory>
#include "order.hpp"
namespace mid {
[[gnu::noinline]] void publish(const std::shared_ptr<Order>& o, Stats& s) { s.out += o->qty; }
[[gnu::noinline]] void route(const std::shared_ptr<Order>& o, Stats& s) { s.notional += o->px * o->qty; publish(o, s); }
[[gnu::noinline]] void risk(const std::shared_ptr<Order>& o, Stats& s) { if (o->qty <= s.max_qty) route(o, s); else ++s.rejects; }
[[gnu::noinline]] void on_msg(const std::shared_ptr<Order>& o, Stats& s) { if (o->px > 0) risk(o, s); }
}  // namespace mid
