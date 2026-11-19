// Step 2: no loop-carried chain at all (running sums), and no divide (cross-multiply).
#pragma once
#include <string>
#include <vector>
#include "common.hpp"
namespace v2 {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct alignas(64) State {
  std::int64_t bid = 0, ask = 0;
  std::int64_t pv = 0, vol = 0;          // running sums over the last 32 trades
  std::vector<Trade> trades;
  std::uint64_t updates = 0;
};
static_assert(sizeof(State) == 64);
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
      s.pv += m.price * m.qty; s.vol += m.qty;
      if (s.trades.size() > 32) {
        const Trade& old = s.trades[s.trades.size() - 33];
        s.pv -= old.price * old.qty; s.vol -= old.qty;
      }
    }
    if (s.bid <= 0 || s.ask <= s.bid || s.vol == 0) return 0;
    // edge > 1/4  <=>  2*((bid+ask)*vol - 2*pv) > (ask-bid)*vol   (vol, spread > 0)
    std::int64_t lhs = 2 * ((s.bid + s.ask) * s.vol - 2 * s.pv);
    std::int64_t rhs = (s.ask - s.bid) * s.vol;
    if (lhs > rhs) return 1;
    if (lhs < -rhs) return -1;
    return 0;
  }
  std::uint64_t report() const { std::uint64_t h = invalid; for (auto& s : st) if (s.updates) h += sym_digest(s.bid, s.ask, s.updates); return h; }
};
}  // namespace v2
