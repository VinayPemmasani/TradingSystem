#pragma once
#include <cstdint>
#include <string>
#include <string_view>
#include <vector>
struct Fill { std::int64_t px; std::int32_t qty; };
struct Order {                 // 104 bytes on x86-64 libstdc++
  std::string account;         // e.g. "FIRM01-DESK07" (<= 16 chars, checked at entry)
  std::string symbol;          // e.g. "AAPL"          (<= 8 chars, checked at entry)
  std::int64_t px;             // fixed-point price
  std::int32_t qty;
  std::vector<Fill> fills;     // fills so far
};
struct Limits {
  struct Entry { std::string symbol; std::int32_t max_qty; };
  std::vector<Entry> entries;
};
