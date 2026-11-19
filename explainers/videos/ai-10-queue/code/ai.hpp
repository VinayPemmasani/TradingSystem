// LEFT: the general-purpose thread-safe queue. Correct, unbounded, and the
// consumer sleeps when there is nothing to do.
#pragma once
#include <condition_variable>
#include <mutex>
#include <queue>

template <class T>
class BlockingQueue {
  std::mutex m_;
  std::condition_variable cv_;
  std::queue<T> q_;
 public:
  void push(const T& v) {
    { std::lock_guard lk(m_); q_.push(v); }
    cv_.notify_one();
  }
  T pop() {
    std::unique_lock lk(m_);
    cv_.wait(lk, [&] { return !q_.empty(); });
    T v = q_.front(); q_.pop();
    return v;
  }
};
