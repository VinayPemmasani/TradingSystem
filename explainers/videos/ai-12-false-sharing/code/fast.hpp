// RIGHT: every field written by a different thread starts its own 64-byte line.
// 64 is fixed (not std::hardware_destructive_interference_size, which GCC warns
// can change with -mtune/-mcpu and would change the layout).
#pragma once
#include <array>
#include <atomic>
#include <cstddef>
#include <cstdint>

inline constexpr size_t kLine = 64;

struct alignas(kLine) PaddedCounter {
  std::atomic<uint64_t> n{0};
};
struct CountersPadded {
  std::array<PaddedCounter, 2> c;   // c[0], c[1]: separate lines
};
static_assert(sizeof(CountersPadded) == 2 * kLine);

template <class T, size_t N>
struct RingPadded {
  alignas(kLine) std::atomic<size_t> head{0};   // producer's line
  size_t cached_tail = 0;
  alignas(kLine) std::atomic<size_t> tail{0};   // consumer's line
  size_t cached_head = 0;
  alignas(kLine) T buf[N];                      // slots from line 3
};
