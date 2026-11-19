// RIGHT: the same ring with the orderings the protocol needs. Each index has
// one writer: its owner reads it relaxed; the other side reads it with acquire;
// the owner publishes with release (a plain mov on x86).
#pragma once
#include <atomic>
#include <cstddef>

inline constexpr auto relaxed = std::memory_order_relaxed;
inline constexpr auto acquire = std::memory_order_acquire;
inline constexpr auto release = std::memory_order_release;

template <class T, size_t N>
class RingAR {
  alignas(64) std::atomic<size_t> head_{0};
  size_t cached_tail_ = 0;
  alignas(64) std::atomic<size_t> tail_{0};
  size_t cached_head_ = 0;
  alignas(64) T buf_[N];
 public:
  bool try_push(const T& v) {
    size_t h = head_.load(relaxed);          // we own head_
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load(acquire);    // pairs with pop's release
      if (h - cached_tail_ == N) return false;
    }
    buf_[h & (N - 1)] = v;
    head_.store(h + 1, release);             // slot write happens-before
    return true;
  }
  bool try_pop(T& out) {
    size_t t = tail_.load(relaxed);          // we own tail_
    if (t == cached_head_) {
      cached_head_ = head_.load(acquire);    // pairs with push's release
      if (t == cached_head_) return false;
    }
    out = buf_[t & (N - 1)];
    tail_.store(t + 1, release);             // slot read done, free it
    return true;
  }
};
