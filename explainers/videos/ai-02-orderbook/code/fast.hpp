#pragma once
// RIGHT: the hot-path version. Prices are integer ticks. Each side is a flat
// array of quantities indexed by (price - base), plus a cursor at the best level.
// Constraint stated up front: prices stay inside a known window (price bands).
#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace hp {
using Top = std::optional<std::pair<std::int64_t, std::int64_t>>;  // ticks, qty

class FlatBook {
 public:
  FlatBook(std::int64_t base, std::int32_t n)            // window [base, base+n)
      : base_(base), n_(n), bid_(std::size_t(n)), ask_(std::size_t(n)), bb_(-1), ba_(n) {}
  bool set(bool bid, std::int64_t px, std::int64_t qty) {  // qty 0 = delete level
    const std::int64_t i = px - base_;
    if (i < 0 || i >= n_) return false;                    // outside band: caller recenters
    const auto k = std::int32_t(i);
    if (bid) {
      bid_[std::size_t(k)] = qty;
      if (qty != 0 && k > bb_) bb_ = k;
      else if (qty == 0 && k == bb_) while (bb_ >= 0 && bid_[std::size_t(bb_)] == 0) --bb_;
    } else {
      ask_[std::size_t(k)] = qty;
      if (qty != 0 && k < ba_) ba_ = k;
      else if (qty == 0 && k == ba_) while (ba_ < n_ && ask_[std::size_t(ba_)] == 0) ++ba_;
    }
    return true;
  }
  Top best_bid() const { if (bb_ < 0) return std::nullopt; return std::make_pair(base_ + bb_, bid_[std::size_t(bb_)]); }
  Top best_ask() const { if (ba_ >= n_) return std::nullopt; return std::make_pair(base_ + ba_, ask_[std::size_t(ba_)]); }
 private:
  std::int64_t base_;
  std::int32_t n_;
  std::vector<std::int64_t> bid_, ask_;   // qty per tick; 0 = empty level
  std::int32_t bb_, ba_;                  // best bid / best ask index
};
}  // namespace hp
