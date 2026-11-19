// Step 1 variant: no locate code on the wire. Key on the 8 symbol bytes as one
// uint64 in an open-addressing table (linear probing, power-of-two size).
#pragma once
#include <string>
#include <vector>
#include "common.hpp"
namespace v1h {
struct Trade { std::string symbol; std::int64_t price; std::uint32_t qty; };
struct alignas(64) State { std::int64_t bid = 0, ask = 0; std::vector<Trade> trades; std::uint64_t updates = 0; };
struct SymbolTable {                      // 1024 slots for 500 symbols: load factor < 0.5
  std::uint64_t keys[1024] = {};          // 0 = empty (a symbol is never 8 zero bytes)
  std::uint16_t ids[1024] = {};
  std::uint16_t count = 0;
  std::uint16_t find_or_add(const char* stock) {
    std::uint64_t k; std::memcpy(&k, stock, 8);
    std::size_t i = (k * 0x9E3779B97F4A7C15ull) >> 54;   // top 10 bits
    while (keys[i] != k) {
      if (keys[i] == 0) { keys[i] = k; ids[i] = count++; break; }
      i = (i + 1) & 1023;
    }
    return ids[i];
  }
};
struct Handler {
  SymbolTable table;
  std::vector<State> st = std::vector<State>(kMaxLocate);
  std::uint64_t invalid = 0;
  int on_msg(const Msg& m) {
    if (m.qty == 0) { ++invalid; return 0; }
    if (m.price <= 0) { ++invalid; return 0; }
    if (m.side != 'B' && m.side != 'S') { ++invalid; return 0; }
    State& s = st[table.find_or_add(m.stock)];
    ++s.updates;
    if (m.type == 'Q') {
      if (m.side == 'B') s.bid = m.price; else s.ask = m.price;
    } else {
      s.trades.push_back(Trade{std::string(m.stock, 8), m.price, m.qty});
    }
    if (s.bid <= 0 || s.ask <= s.bid || s.trades.empty()) return 0;
    double pv = 0; std::uint64_t vol = 0;
    std::size_t n = s.trades.size(), from = n > 32 ? n - 32 : 0;
    for (std::size_t i = from; i < n; ++i) { pv += double(s.trades[i].price) * s.trades[i].qty; vol += s.trades[i].qty; }
    double vwap = pv / double(vol);
    double mid = double(s.bid + s.ask) / 2.0;
    double edge = (mid - vwap) / double(s.ask - s.bid);
    if (edge > 0.25) return 1;
    if (edge < -0.25) return -1;
    return 0;
  }
  std::uint64_t report() const { std::uint64_t h = invalid; for (auto& s : st) if (s.updates) h += sym_digest(s.bid, s.ask, s.updates); return h; }
};
}  // namespace v1h
