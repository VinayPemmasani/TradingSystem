#pragma once
// LEFT: the general-purpose version. A price-level (market-by-price) book:
// one std::map per side, keyed by price. Correct for any price, any depth.
#include <cstdint>
#include <functional>
#include <map>
#include <optional>
#include <utility>

namespace ai {
struct Level { std::int64_t qty; };
using Top = std::optional<std::pair<double, std::int64_t>>;

class Book {
 public:
  void set(bool bid, double px, std::int64_t qty) {   // qty 0 = delete level
    if (bid) apply(bids_, px, qty); else apply(asks_, px, qty);
  }
  Top best_bid() const { return top(bids_); }
  Top best_ask() const { return top(asks_); }
 private:
  template <class M> static void apply(M& m, double px, std::int64_t qty) {
    if (qty == 0) m.erase(px);
    else m[px].qty = qty;                               // allocates a node if new
  }
  template <class M> static Top top(const M& m) {
    if (m.empty()) return std::nullopt;
    return std::make_pair(m.begin()->first, m.begin()->second.qty);
  }
  std::map<double, Level, std::greater<double>> bids_;  // best bid first
  std::map<double, Level> asks_;                        // best ask first
};
}  // namespace ai
