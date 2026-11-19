#pragma once
#include <cstdint>
#include <vector>
enum class Side : std::uint8_t { Buy = 0, Sell = 1 };
struct Tick { std::int64_t px; std::int32_t qty; Side side; };
struct Stats { std::int64_t buy_vol = 0, sell_vol = 0; std::int64_t big_buys = 0, big_sells = 0; std::int64_t bad = 0;
  bool operator==(const Stats&) const = default; };
