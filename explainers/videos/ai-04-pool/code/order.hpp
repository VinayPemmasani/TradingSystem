#pragma once
#include <array>
#include <cstdint>
struct Order {                                // 128 bytes
  std::uint64_t id, ts;
  std::int64_t px, qty;
  std::uint32_t acct, side;
  std::array<char, 24> symbol;
  std::array<std::uint64_t, 8> user;          // strategy tags etc.
};
static_assert(sizeof(Order) == 128);
struct NewMsg { std::uint64_t id, ts; std::int64_t px, qty; std::uint32_t acct, side; };
