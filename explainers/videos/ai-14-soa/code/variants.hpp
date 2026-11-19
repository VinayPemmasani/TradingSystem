#pragma once
#include "ai.hpp"
#include "fast.hpp"
namespace var {
// Hot/cold split: the three hot fields packed in one 24-byte struct.
struct OrderHot { double px; std::int64_t qty; std::uint8_t live_bid; };
inline std::int64_t bid_depth_hot(const std::vector<OrderHot>& h, double px) {
  std::int64_t total = 0;
  for (const OrderHot& o : h) { const std::int64_t take = o.live_bid & (o.px >= px); total += o.qty & -take; }
  return total;
}
// Fat AoS with the same branchless body as the right side: isolates layout from branches.
inline std::int64_t bid_depth_aos_branchless(const std::vector<Order>& book, double px) {
  std::int64_t total = 0;
  for (const Order& o : book) {
    const std::int64_t take = o.active & (o.side == Side::Buy) & (o.price >= px);
    total += o.qty & -take;
  }
  return total;
}
}  // namespace var
