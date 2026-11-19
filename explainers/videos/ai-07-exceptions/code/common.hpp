#pragma once
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <string_view>
struct Order { std::uint64_t id; std::int64_t px; std::int32_t qty; };
struct Limits { std::int32_t max_qty; std::int64_t px_lo, px_hi; };
// Stand-in for the outbound path: both versions call the same send/reject.
struct Out {
  std::uint64_t sent = 0, rejected = 0, ids = 0;
  char last_reason[64] = {};
  void send(const Order& o) { ++sent; ids += o.id; }
  void reject(const Order& o, std::string_view why) {
    ++rejected; ids += o.id * 31;
    std::size_t n = std::min<std::size_t>(why.size(), 63);
    std::memcpy(last_reason, why.data(), n); last_reason[n] = 0;
  }
};
