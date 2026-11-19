// Step 3: branches. Side becomes an index, validation one test, the signal arithmetic.
#pragma once
#include <string>
#include <vector>
#include "common.hpp"
namespace v3 {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct alignas(64) State {
  std::int64_t px[2] = {0, 0};           // px[0] bid, px[1] ask
  std::int64_t pv = 0, vol = 0;
  std::vector<Trade> trades;
  std::uint64_t updates = 0;
};
static_assert(sizeof(State) == 64);
struct Handler {
  std::vector<State> st = std::vector<State>(kMaxLocate);
  std::uint64_t invalid = 0;
  int on_msg(const Msg& m) {
    bool ok = (m.qty != 0) & (m.price > 0) & ((m.side == 'B') | (m.side == 'S'));
    if (!ok) [[unlikely]] { ++invalid; return 0; }
    State& s = st[m.locate];
    ++s.updates;
    if (m.type == 'Q') {
      s.px[m.side == 'S'] = m.price;       // no branch on side
    } else {
      s.trades.push_back(Trade{std::string(m.stock, 8), m.price, m.qty});
      s.pv += m.price * m.qty; s.vol += m.qty;
      if (s.trades.size() > 32) {
        const Trade& old = s.trades[s.trades.size() - 33];
        s.pv -= old.price * old.qty; s.vol -= old.qty;
      }
    }
    std::int64_t bid = s.px[0], ask = s.px[1];
    std::int64_t lhs = 2 * ((bid + ask) * s.vol - 2 * s.pv);
    std::int64_t rhs = (ask - bid) * s.vol;
    int sig = (lhs > rhs) - (lhs < -rhs);   // +1 / 0 / -1, no jumps
    bool live = (bid > 0) & (ask > bid) & (s.vol != 0);
    return live ? sig : 0;
  }
  std::uint64_t report() const { std::uint64_t h = invalid; for (auto& s : st) if (s.updates) h += sym_digest(s.px[0], s.px[1], s.updates); return h; }
};
}  // namespace v3
