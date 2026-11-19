#pragma once
// First answer: keep the window in a std::deque and recompute everything on every trade.
#include <deque>
#include <optional>

#include "vwap.hpp"

class NaiveVwap {
 public:
  explicit NaiveVwap(std::int64_t window_ns) : window_{window_ns} {}
  void on_trade(const Trade& t) {
    w_.push_back(t);
    while (w_.front().ts <= t.ts - window_) w_.pop_front();
    unsigned __int128 pq = 0;
    std::uint64_t q = 0;
    std::uint32_t hi = 0, lo = UINT32_MAX;
    for (const Trade& x : w_) {  // O(trades in window), every time
      pq += static_cast<unsigned __int128>(x.px) * x.qty;
      q += x.qty;
      if (x.px > hi) hi = x.px;
      if (x.px < lo) lo = x.px;
    }
    vwap_ = q ? std::optional<std::uint64_t>(std::uint64_t((pq + q / 2) / q)) : std::nullopt;
    hi_ = hi;
    lo_ = lo;
  }
  std::optional<std::uint64_t> vwap() const { return vwap_; }
  std::uint32_t high() const { return hi_; }
  std::uint32_t low() const { return lo_; }
  std::size_t count() const { return w_.size(); }

 private:
  std::int64_t window_;
  std::deque<Trade> w_;
  std::optional<std::uint64_t> vwap_;
  std::uint32_t hi_ = 0, lo_ = 0;
};
