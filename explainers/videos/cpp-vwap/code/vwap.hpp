#pragma once
// VWAP over the last `window` nanoseconds of exchange time, O(1) amortized per trade.
// Prices are Price(4) (1/10000 dollars); timestamps are exchange nanoseconds
// (ITCH: since midnight). A trade at time t stays in the window while t > now - window.
#include <cstdint>
#include <optional>
#include <vector>

struct Trade {
  std::int64_t ts;     // exchange timestamp, ns
  std::uint32_t px;    // Price(4)
  std::uint32_t qty;   // shares
};

// Fixed-capacity ring; capacity is a power of two, indexes wrap with a mask.
template <class T>
class Ring {
 public:
  explicit Ring(std::size_t cap_pow2) : buf_(cap_pow2), mask_(cap_pow2 - 1) {}
  bool full() const { return tail_ - head_ == buf_.size(); }
  bool empty() const { return tail_ == head_; }
  std::size_t size() const { return std::size_t(tail_ - head_); }
  T& front() { return buf_[head_ & mask_]; }
  T& back() { return buf_[(tail_ - 1) & mask_]; }
  void push_back(const T& t) { buf_[tail_++ & mask_] = t; }
  void pop_front() { ++head_; }
  void pop_back() { --tail_; }

 private:
  std::vector<T> buf_;
  std::uint64_t mask_, head_ = 0, tail_ = 0;
};

class SlidingVwap {
 public:
  SlidingVwap(std::int64_t window_ns, std::size_t cap_pow2)
      : window_{window_ns}, ring_{cap_pow2}, maxq_{cap_pow2}, minq_{cap_pow2} {}

  // Returns false (and changes nothing) if time went backwards or the ring is full.
  bool on_trade(const Trade& t) {
    if (t.ts < last_ts_) return false;
    evict(t.ts);
    if (ring_.full()) return false;  // size the ring for the busiest window
    last_ts_ = t.ts;
    ring_.push_back(t);
    pq_ += static_cast<unsigned __int128>(t.px) * t.qty;  // up to 2^64 per trade
    q_ += t.qty;
    while (!maxq_.empty() && maxq_.back().px <= t.px) maxq_.pop_back();
    maxq_.push_back(t);
    while (!minq_.empty() && minq_.back().px >= t.px) minq_.pop_back();
    minq_.push_back(t);
    return true;
  }

  // Drop trades at or before now - window (also call it on a timer when no trades arrive).
  void evict(std::int64_t now) {
    const std::int64_t cut = now - window_;
    while (!ring_.empty() && ring_.front().ts <= cut) {
      const Trade& o = ring_.front();
      pq_ -= static_cast<unsigned __int128>(o.px) * o.qty;
      q_ -= o.qty;
      ring_.pop_front();
    }
    while (!maxq_.empty() && maxq_.front().ts <= cut) maxq_.pop_front();
    while (!minq_.empty() && minq_.front().ts <= cut) minq_.pop_front();
  }

  // VWAP in Price(4), rounded half up; nullopt for an empty window.
  std::optional<std::uint64_t> vwap() const {
    if (q_ == 0) return std::nullopt;
    return static_cast<std::uint64_t>((pq_ + q_ / 2) / q_);
  }
  std::optional<std::uint32_t> high() { return maxq_.empty() ? std::nullopt : std::optional{maxq_.front().px}; }
  std::optional<std::uint32_t> low() { return minq_.empty() ? std::nullopt : std::optional{minq_.front().px}; }
  std::size_t count() const { return ring_.size(); }
  std::uint64_t volume() const { return q_; }

 private:
  std::int64_t window_;
  std::int64_t last_ts_ = INT64_MIN;
  Ring<Trade> ring_, maxq_, minq_;
  unsigned __int128 pq_ = 0;  // sum of px * qty
  std::uint64_t q_ = 0;       // sum of qty
};
