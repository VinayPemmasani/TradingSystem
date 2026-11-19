#pragma once
// LEFT: the general-purpose version (on screen verbatim below the includes).
#include <chrono>
#include <cstdint>
#include <string>
#include <vector>
using std::int64_t; using std::uint64_t;
using sys_clock = std::chrono::system_clock;
enum class Side : std::uint8_t { Buy, Sell };
struct Order {                       // 112 bytes
  std::string symbol, account;       // 2 x 32
  uint64_t id;
  sys_clock::time_point created, updated;
  double price; int64_t qty;
  Side side; bool active, ioc, post_only;
};
int64_t bid_depth(const std::vector<Order>& book,
                  double px) {
  int64_t total = 0;
  for (const Order& o : book)
    if (o.active && o.side == Side::Buy &&
        o.price >= px) total += o.qty;
  return total;
}
static_assert(sizeof(Order) == 112);
