#include <atomic>
#include <cstddef>
#include <cstdint>
inline constexpr std::size_t kCacheLine = 64;
template <typename T, std::size_t Capacity>
class SpscRing {
  // Producer-owned line.
  alignas(kCacheLine) std::atomic<std::uint64_t> head_{0};
  std::uint64_t cached_tail_{0};

  // Consumer-owned line.
  alignas(kCacheLine) std::atomic<std::uint64_t> tail_{0};
  std::uint64_t cached_head_{0};

  alignas(kCacheLine) T slots_[Capacity]{};
 public:
  static constexpr std::size_t off_tail() { return offsetof(SpscRing, tail_); }
  static constexpr std::size_t off_slots() { return offsetof(SpscRing, slots_); }
};
#include <cstdio>
int main(){ std::printf("tail_ at %zu, slots_ at %zu, sizeof %zu\n", SpscRing<long,1024>::off_tail(), SpscRing<long,1024>::off_slots(), sizeof(SpscRing<long,1024>)); }
