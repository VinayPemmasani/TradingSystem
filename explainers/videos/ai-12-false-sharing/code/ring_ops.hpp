// The same SPSC push/pop (cached indices, acquire/release) for both layouts,
// so only the layout differs.
#pragma once
#include <atomic>
#include <cstddef>
template <class R, class T, size_t N> inline bool push(R& r, const T& v) {
  size_t h = r.head.load(std::memory_order_relaxed);
  if (h - r.cached_tail == N) {
    r.cached_tail = r.tail.load(std::memory_order_acquire);
    if (h - r.cached_tail == N) return false;
  }
  r.buf[h & (N - 1)] = v;
  r.head.store(h + 1, std::memory_order_release);
  return true;
}
template <class R, class T, size_t N> inline bool pop(R& r, T& out) {
  size_t t = r.tail.load(std::memory_order_relaxed);
  if (t == r.cached_head) {
    r.cached_head = r.head.load(std::memory_order_acquire);
    if (t == r.cached_head) return false;
  }
  out = r.buf[t & (N - 1)];
  r.tail.store(t + 1, std::memory_order_release);
  return true;
}
