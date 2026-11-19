// RIGHT: bounded lock-free SPSC ring. One writer per index, cached copies of
// the other side's index, indices on separate cache lines. The consumer
// busy-polls on its own core.
#pragma once
#include <atomic>
#include <cstddef>
#include <immintrin.h>

inline constexpr auto relaxed = std::memory_order_relaxed;
inline constexpr auto acquire = std::memory_order_acquire;
inline constexpr auto release = std::memory_order_release;

template <class T, size_t N>   // N: power of two, fixed at compile time
class SpscRing {
  static_assert((N & (N - 1)) == 0);
  alignas(64) std::atomic<size_t> head_{0};  // producer writes
  size_t cached_tail_ = 0;
  alignas(64) std::atomic<size_t> tail_{0};  // consumer writes
  size_t cached_head_ = 0;
  alignas(64) T buf_[N];
 public:
  bool try_push(const T& v) {
    size_t h = head_.load(relaxed);
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load(acquire);
      if (h - cached_tail_ == N) return false;  // full
    }
    buf_[h & (N - 1)] = v;
    head_.store(h + 1, release);
    return true;
  }
  bool try_pop(T& out) {
    size_t t = tail_.load(relaxed);
    if (t == cached_head_) {
      cached_head_ = head_.load(acquire);
      if (t == cached_head_) return false;      // empty
    }
    out = buf_[t & (N - 1)];
    tail_.store(t + 1, release);
    return true;
  }
  T pop() {                                     // busy-poll
    T v;
    while (!try_pop(v)) _mm_pause();
    return v;
  }
};
