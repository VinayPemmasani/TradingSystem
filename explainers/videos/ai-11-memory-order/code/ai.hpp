// LEFT: SPSC ring written with default std::atomic operations: every load
// and store is memory_order_seq_cst. Correct, and the strongest ordering.
#pragma once
#include <atomic>
#include <cstddef>

template <class T, size_t N>
class RingSeq {
  alignas(64) std::atomic<size_t> head_{0};
  size_t cached_tail_ = 0;
  alignas(64) std::atomic<size_t> tail_{0};
  size_t cached_head_ = 0;
  alignas(64) T buf_[N];
 public:
  bool try_push(const T& v) {
    size_t h = head_.load();
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load();
      if (h - cached_tail_ == N) return false;
    }
    buf_[h & (N - 1)] = v;
    head_.store(h + 1);            // seq_cst store: xchg on x86
    return true;
  }
  bool try_pop(T& out) {
    size_t t = tail_.load();
    if (t == cached_head_) {
      cached_head_ = head_.load();
      if (t == cached_head_) return false;
    }
    out = buf_[t & (N - 1)];
    tail_.store(t + 1);            // seq_cst store: xchg on x86
    return true;
  }
};
