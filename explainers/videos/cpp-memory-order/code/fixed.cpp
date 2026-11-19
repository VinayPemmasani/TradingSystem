#include <atomic>
struct Msg { long price; int qty; };
Msg msg;
std::atomic<bool> ready{false};

void publish(long p, int q) {    // thread 1
  msg.price = p;
  msg.qty = q;
  ready.store(true, std::memory_order_release);
}
long consume() {                 // thread 2
  while (!ready.load(std::memory_order_acquire)) {}
  return msg.price;
}
