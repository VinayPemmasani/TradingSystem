#pragma once
// The step before cached indices: each side reads the other's index every time.
#include "ring.hpp"

template <class T, size_t N>
class RingNoCache {
  static_assert(N >= 2 && (N & (N - 1)) == 0, "power of two");
  static constexpr size_t kMask = N - 1;

  alignas(64) std::atomic<size_t> head_{0};  // producer writes
  alignas(64) std::atomic<size_t> tail_{0};  // consumer writes
  alignas(64) T buf_[N];

 public:
  bool try_push(const T& v) {
    const size_t h = head_.load(relaxed);
    if (h - tail_.load(acquire) == N) return false;  // full
    buf_[h & kMask] = v;
    head_.store(h + 1, release);  // publish the slot
    return true;
  }

  bool try_pop(T& out) {
    const size_t t = tail_.load(relaxed);
    if (t == head_.load(acquire)) return false;  // empty
    out = buf_[t & kMask];
    tail_.store(t + 1, release);  // free the slot
    return true;
  }
};
