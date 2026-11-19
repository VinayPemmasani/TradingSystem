// Step 2a: same work, four independent accumulators (shorter dependency chain).
#pragma once
#include <string>
#include <vector>
#include "common.hpp"
namespace v2a {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct alignas(64) State { std::int64_t bid = 0, ask = 0; std::vector<Trade> trades; std::uint64_t updates = 0; };
struct Handler {
  std::vector<State> st = std::vector<State>(kMaxLocate);
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
    double p0 = 0, p1 = 0, p2 = 0, p3 = 0; std::uint64_t vol = 0;
    std::size_t n = s.trades.size(), i = n > 32 ? n - 32 : 0;
    const Trade* t = s.trades.data();
    for (; i + 4 <= n; i += 4) {               // four chains run side by side
      p0 += double(t[i].price) * t[i].qty;
      p1 += double(t[i + 1].price) * t[i + 1].qty;
      p2 += double(t[i + 2].price) * t[i + 2].qty;
      p3 += double(t[i + 3].price) * t[i + 3].qty;
      vol += t[i].qty + t[i + 1].qty + t[i + 2].qty + t[i + 3].qty;
    }
    for (; i < n; ++i) { p0 += double(t[i].price) * t[i].qty; vol += t[i].qty; }
    double pv = (p0 + p1) + (p2 + p3);          // exact: integer-valued doubles < 2^53
    double vwap = pv / double(vol);
    double mid = double(s.bid + s.ask) / 2.0;
    double edge = (mid - vwap) / double(s.ask - s.bid);
    if (edge > 0.25) return 1;
    if (edge < -0.25) return -1;
    return 0;
  }
  std::uint64_t report() const { std::uint64_t h = invalid; for (auto& s : st) if (s.updates) h += sym_digest(s.bid, s.ask, s.updates); return h; }
};
}  // namespace v2a
