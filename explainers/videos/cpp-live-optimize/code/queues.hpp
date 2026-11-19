// Part 2 handoffs between the feed thread and the strategy thread.
#pragma once
#include <atomic>
#include <condition_variable>
#include <mutex>
#include <queue>
#include "common.hpp"

// Step 5a: the obvious version. Lock, push, notify; the consumer sleeps when empty.
struct MutexQueue {
  std::mutex mu;
  std::condition_variable cv;
  std::queue<Msg> q;
  std::uint64_t pushed = 0, popped = 0;   // stats
  bool try_push(const Msg& m) {
    { std::lock_guard<std::mutex> g(mu); q.push(m); ++pushed; }
    cv.notify_one();
    return true;
  }
  void pop_wait(Msg& out) {
    std::unique_lock<std::mutex> g(mu);
    cv.wait(g, [&] { return !q.empty(); });
    out = q.front(); q.pop(); ++popped;
  }
};

// Step 5b: lock-free SPSC ring with acquire/release, everything packed together.
template <std::size_t N> struct alignas(64) RingPacked {   // head, tail, pushed, popped: bytes 0-31 of one line
  std::atomic<std::uint64_t> head{0};     // written by the feed thread
  std::atomic<std::uint64_t> tail{0};     // written by the strategy thread
  std::uint64_t pushed = 0, popped = 0;   // stats: one per thread, same line
  Msg slots[N];
  bool try_push(const Msg& m) {
    std::uint64_t h = head.load(std::memory_order_relaxed);
    if (h - tail.load(std::memory_order_acquire) == N) return false;
    slots[h % N] = m;
    head.store(h + 1, std::memory_order_release);
    ++pushed;
    return true;
  }
  bool try_pop(Msg& out) {
    std::uint64_t t = tail.load(std::memory_order_relaxed);
    if (t == head.load(std::memory_order_acquire)) return false;
    out = slots[t % N];
    tail.store(t + 1, std::memory_order_release);
    ++popped;
    return true;
  }
};

// Step 6a: same ring, each index and each counter on its own 64-byte line.
template <std::size_t N> struct RingPadded {
  alignas(64) std::atomic<std::uint64_t> head{0};
  alignas(64) std::atomic<std::uint64_t> tail{0};
  alignas(64) std::uint64_t pushed = 0;
  alignas(64) std::uint64_t popped = 0;
  alignas(64) Msg slots[N];
  bool try_push(const Msg& m) {
    std::uint64_t h = head.load(std::memory_order_relaxed);
    if (h - tail.load(std::memory_order_acquire) == N) return false;
    slots[h % N] = m;
    head.store(h + 1, std::memory_order_release);
    ++pushed;
    return true;
  }
  bool try_pop(Msg& out) {
    std::uint64_t t = tail.load(std::memory_order_relaxed);
    if (t == head.load(std::memory_order_acquire)) return false;
    out = slots[t % N];
    tail.store(t + 1, std::memory_order_release);
    ++popped;
    return true;
  }
};
