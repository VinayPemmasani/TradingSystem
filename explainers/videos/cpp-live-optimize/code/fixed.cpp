// Step 5: the same mailbox with acquire/release.
#include "common.hpp"
Msg slot;
std::atomic<bool> ready{false};
void publish(const Msg& m) {     // feed thread
  slot = m;
  ready.store(true, std::memory_order_release);
}
std::int64_t consume() {         // strategy thread
  while (!ready.load(std::memory_order_acquire)) {}
  ready.store(false, std::memory_order_relaxed);
  return slot.price;
}
