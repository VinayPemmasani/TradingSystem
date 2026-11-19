// Every snippet shown on screen in cpp-memory-order that is not a whole file.
#include <atomic>
#include <cstddef>
#include <cstdint>
struct Msg { long price; int qty; };
Msg msg;
std::atomic<bool> ready{false};
long fixed_consume() {
  while (!ready.load(std::memory_order_acquire)) {}
  return msg.price;
}
void fixed_publish() { ready.store(true, std::memory_order_release); }
struct Stats { std::atomic<std::uint64_t> msgs{0}; } stats;
void count() { stats.msgs.fetch_add(1, std::memory_order_relaxed); }

template <typename T, std::size_t Capacity>
struct Ring {                       // the trimmed SpscRing body shown in the ring scene
  static constexpr std::uint64_t kMask = Capacity - 1;
  alignas(64) std::atomic<std::uint64_t> head_{0};
  std::uint64_t cached_tail_{0};
  alignas(64) std::atomic<std::uint64_t> tail_{0};
  std::uint64_t cached_head_{0};
  alignas(64) T slots_[Capacity]{};
  bool push(const T& value) {
    // producer
    const std::uint64_t head = head_.load(std::memory_order_relaxed);
    if (head - cached_tail_ == Capacity)
      cached_tail_ = tail_.load(std::memory_order_acquire);
    if (head - cached_tail_ == Capacity) return false;
    slots_[head & kMask] = value;
    head_.store(head + 1, std::memory_order_release);
    return true;
  }
  bool pop(T& out) {
    // consumer
    const std::uint64_t tail = tail_.load(std::memory_order_relaxed);
    if (tail == cached_head_)
      cached_head_ = head_.load(std::memory_order_acquire);
    if (tail == cached_head_) return false;
    out = slots_[tail & kMask];
    tail_.store(tail + 1, std::memory_order_release);
    return true;
  }
};
int main() { Ring<long, 8> r; long x; r.push(1); count(); fixed_publish(); return r.pop(x) && fixed_consume() == 0 ? 0 : 1; }
