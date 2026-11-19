// LEFT: natural layout. Per-thread counters side by side in one array, and a
// ring whose producer and consumer indices sit next to each other.
#pragma once
#include <array>
#include <atomic>
#include <cstddef>
#include <cstdint>

struct CountersPacked {                       // 2 x 8 bytes: one cache line
  std::array<std::atomic<uint64_t>, 2> n{};   // n[0]: thread A, n[1]: thread B
};

template <class T, size_t N>
struct RingPacked {
  std::atomic<size_t> head{0};   // producer writes
  size_t cached_tail = 0;        // producer's copy of tail
  std::atomic<size_t> tail{0};   // consumer writes
  size_t cached_head = 0;        // consumer's copy of head
  T buf[N];                      // first slots share the line too
};
