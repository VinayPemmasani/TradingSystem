// Step 4: memory. A fixed 32-slot window inside the state: no push_back, no strings, no malloc.
#pragma once
#include "common.hpp"
namespace v4 {
struct alignas(64) State {
  std::int64_t px[2] = {0, 0};
  std::int64_t pv = 0, vol = 0;
  std::uint64_t updates = 0;
  std::uint32_t n = 0;                     // trades seen
  std::int64_t win_pv[32] = {};            // price*qty of the last 32 trades
  std::uint32_t win_q[32] = {};
};
static_assert(sizeof(State) == 448);
struct Handler {
  State* st;                               // allocated and touched once, at startup
  std::uint64_t invalid = 0;
  Handler() : st(new State[kMaxLocate]) {}
  ~Handler() { delete[] st; }
  Handler(const Handler&) = delete;
  Handler& operator=(const Handler&) = delete;
  int on_msg(const Msg& m) {
    bool ok = (m.qty != 0) & (m.price > 0) & ((m.side == 'B') | (m.side == 'S'));
    if (!ok) [[unlikely]] { ++invalid; return 0; }
    State& s = st[m.locate];
    ++s.updates;
    if (m.type == 'Q') {
      s.px[m.side == 'S'] = m.price;
    } else {
      std::uint32_t k = s.n++ & 31;         // overwrite the oldest slot
      std::int64_t add = m.price * m.qty;
      s.pv += add - s.win_pv[k];           // slots start at 0: nothing to evict
      s.vol += std::int64_t(m.qty) - s.win_q[k];
      s.win_pv[k] = add; s.win_q[k] = m.qty;
    }
    std::int64_t bid = s.px[0], ask = s.px[1];
    std::int64_t lhs = 2 * ((bid + ask) * s.vol - 2 * s.pv);
    std::int64_t rhs = (ask - bid) * s.vol;
    int sig = (lhs > rhs) - (lhs < -rhs);
    bool live = (bid > 0) & (ask > bid) & (s.vol != 0);
    return live ? sig : 0;
  }
  std::uint64_t report() const { std::uint64_t h = invalid; for (int i = 0; i < kMaxLocate; ++i) if (st[i].updates) h += sym_digest(st[i].px[0], st[i].px[1], st[i].updates); return h; }
};
}  // namespace v4
