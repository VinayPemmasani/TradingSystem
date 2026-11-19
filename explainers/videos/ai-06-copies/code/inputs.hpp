#pragma once
#include <random>
#include "order.hpp"
inline Limits make_limits() {
  const char* s[] = {"AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","AVGO","JPM","V","XOM","UNH","LLY","WMT","MA","ORCL"};
  Limits l; for (int i = 0; i < 16; ++i) l.entries.push_back({s[i], 500 + 100 * i}); return l;
}
inline std::vector<Order> make_orders(int n) {
  const char* acc[] = {"FIRM01-DESK07","FIRM01-DESK02","FIRM02-ARB","FIRM03-MM-EU","FIRM01-DESK11","FIRM04-OPT","FIRM02-HEDGE","FIRM05-MM-US"};
  Limits l = make_limits(); std::mt19937_64 r(7); std::vector<Order> v(n);
  for (auto& o : v) {
    o.account = acc[r() % 8]; o.symbol = l.entries[r() % 16].symbol;
    o.px = 1000000 + std::int64_t(r() % 9000000); o.qty = 1 + int(r() % 2000);  // ~2/3 pass the limit
    int nf = 1 + int(r() % 3); for (int k = 0; k < nf; ++k) o.fills.push_back({o.px, 10});
  }
  return v;
}
