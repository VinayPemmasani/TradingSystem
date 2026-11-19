#pragma once
#include <atomic>
#include <cstddef>
using std::size_t;
inline constexpr auto relaxed = std::memory_order_relaxed;
inline constexpr auto acquire = std::memory_order_acquire;
inline constexpr auto release = std::memory_order_release;

template <class T, size_t N>
class Ring {
  static_assert(N >= 2 && (N & (N - 1)) == 0, "power of two");
  static constexpr size_t kMask = N - 1;

  alignas(64) std::atomic<size_t> head_{0};  // producer writes
  size_t cached_tail_ = 0;                    // producer's copy
  alignas(64) std::atomic<size_t> tail_{0};  // consumer writes
  size_t cached_head_ = 0;                    // consumer's copy
  alignas(64) T buf_[N];

 public:
  bool try_push(const T& v) {
    const size_t h = head_.load(relaxed);
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load(acquire);
      if (h - cached_tail_ == N) return false;  // full
    }
    buf_[h & kMask] = v;
    head_.store(h + 1, release);  // publish the slot
    return true;
  }

  bool try_pop(T& out) {
    const size_t t = tail_.load(relaxed);
    if (t == cached_head_) {
      cached_head_ = head_.load(acquire);
      if (t == cached_head_) return false;  // empty
    }
    out = buf_[t & kMask];
    tail_.store(t + 1, release);  // free the slot
    return true;
  }
};
