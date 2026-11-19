#pragma once
// RIGHT: the hot-path version (on screen verbatim below the includes).
#include <cstddef>
#include <cstdint>
#include <vector>
using std::int64_t; using std::uint8_t; using std::size_t;
// hot fields: one array each.
// cold fields live elsewhere, same index.
struct BookHot {
  std::vector<double>   px;
  std::vector<int64_t>  qty;
  std::vector<uint8_t>  live_bid;  // active && Buy
};
int64_t bid_depth(const BookHot& b, double px) {
  int64_t total = 0;
  for (size_t i = 0; i < b.px.size(); ++i) {
    const int64_t take =
        b.live_bid[i] & (b.px[i] >= px);
    total += b.qty[i] & -take;   // 0 or all ones
  }
  return total;
}
