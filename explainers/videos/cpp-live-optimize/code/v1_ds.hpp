// Step 1: data structures. Index by the locate code, flat array, hot fields in one line.
#pragma once
#include <string>
#include <vector>
#include "common.hpp"
namespace v1 {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct alignas(64) State {             // hot: one cache line
  std::int64_t bid = 0, ask = 0;
  std::vector<Trade> trades;
  std::uint64_t updates = 0;
};
static_assert(sizeof(State) == 64);
struct Handler {
  std::vector<State> st = std::vector<State>(kMaxLocate);
  std::vector<std::string> names = std::vector<std::string>(kMaxLocate);  // cold
  std::uint64_t invalid = 0;

  int on_msg(const Msg& m) {
    if (m.qty == 0) { ++invalid; return 0; }
    if (m.price <= 0) { ++invalid; return 0; }
    if (m.side != 'B' && m.side != 'S') { ++invalid; return 0; }
    State& s = st[m.locate];
    ++s.updates;
    if (m.type == 'Q') {
      if (m.side == 'B') s.bid = m.price; else s.ask = m.price;
    } else {
      s.trades.push_back(Trade{std::string(m.stock, 8), m.price, m.qty});
    }
    if (s.bid <= 0 || s.ask <= s.bid || s.trades.empty()) return 0;
    double pv = 0; std::uint64_t vol = 0;
    std::size_t n = s.trades.size(), from = n > 32 ? n - 32 : 0;
    for (std::size_t i = from; i < n; ++i) {
      pv += double(s.trades[i].price) * s.trades[i].qty;
      vol += s.trades[i].qty;
    }
    double vwap = pv / double(vol);
    double mid = double(s.bid + s.ask) / 2.0;
    double edge = (mid - vwap) / double(s.ask - s.bid);
    if (edge > 0.25) return 1;
    if (edge < -0.25) return -1;
    return 0;
  }
  std::uint64_t report() const {
    std::uint64_t h = invalid;
    for (auto& s : st) if (s.updates) h += sym_digest(s.bid, s.ask, s.updates);
    return h;
  }
};
}  // namespace v1
