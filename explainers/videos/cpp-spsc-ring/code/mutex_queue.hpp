#pragma once
#include <array>
#include <cstddef>
#include <mutex>
using std::size_t;

template <class T, size_t N>
class MutexQueue {
  std::mutex m_;
  std::array<T, N> buf_{};
  size_t head_ = 0, tail_ = 0;
 public:
  bool try_push(const T& v) {
    std::lock_guard lock(m_);
    if (head_ - tail_ == N) return false;  // full
    buf_[head_++ % N] = v;
    return true;
  }
  bool try_pop(T& out) {
    std::lock_guard lock(m_);
    if (head_ == tail_) return false;      // empty
    out = buf_[tail_++ % N];
    return true;
  }
};
