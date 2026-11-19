// Step 0: the snippet the interviewer hands you.
#pragma once
#include <map>
#include <string>
#include <vector>
#include "common.hpp"
namespace v0 {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct State {
  std::string symbol;
  std::int64_t bid = 0, ask = 0;
  std::vector<Trade> trades;          // every trade, kept forever
  std::uint64_t updates = 0;
};
struct Handler {
  std::map<std::string, State> book;
  std::uint64_t invalid = 0;

  int on_msg(const Msg& m) {
    if (m.qty == 0) { ++invalid; return 0; }
    if (m.price <= 0) { ++invalid; return 0; }
    if (m.side != 'B' && m.side != 'S') { ++invalid; return 0; }
    std::string sym(m.stock, 8);
    State& s = book[sym];
    s.symbol = sym;
    ++s.updates;
    if (m.type == 'Q') {
      if (m.side == 'B') s.bid = m.price; else s.ask = m.price;
    } else {
      s.trades.push_back(Trade{sym, m.price, m.qty});
    }
    if (s.bid <= 0 || s.ask <= s.bid || s.trades.empty()) return 0;
    double pv = 0; std::uint64_t vol = 0;               // VWAP of the last 32 trades
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
    for (auto& [k, s] : book) h += sym_digest(s.bid, s.ask, s.updates);
    return h;
  }
};
}  // namespace v0
