#pragma once
// LEFT: the general-purpose version. Each new order is its own heap object;
// unique_ptr makes ownership and cleanup automatic.
#include <memory>
#include <vector>
#include "order.hpp"

namespace ai {
class Orders {
 public:
  explicit Orders(std::size_t max_live) { live_.reserve(max_live); }
  void on_new(const NewMsg& m) {
    auto o = std::make_unique<Order>(            // malloc per message
        Order{m.id, m.ts, m.px, m.qty, m.acct, m.side, {}, {}});
    live_.push_back(std::move(o));
  }
  void on_cancel(std::size_t k) {                // k: index of a live order
    live_[k] = std::move(live_.back());          // old order freed here
    live_.pop_back();
  }
  std::size_t size() const { return live_.size(); }
  const Order& at(std::size_t k) const { return *live_[k]; }
 private:
  std::vector<std::unique_ptr<Order>> live_;
};
}  // namespace ai
