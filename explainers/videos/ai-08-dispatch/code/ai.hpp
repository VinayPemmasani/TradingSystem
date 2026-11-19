// LEFT: the general-purpose version. A strategy interface (or a std::function callback) called per price.
#pragma once
#include <algorithm>
#include <functional>
#include "prices.hpp"
namespace ai {
struct Quoter {          // pluggable strategy
  virtual ~Quoter() = default;
  virtual int quote(int mid) const = 0;
};
void quote_all(const Quoter& q, const Prices& mid,
               Prices& out) {
  for (int i = 0; i < kN; ++i)
    out[i] = q.quote(mid[i]);  // indirect call
}
// (end of on-screen snippet 1)
struct Clamp : Quoter {
  int edge, lo, hi;
  Clamp(int e, int l, int h)
      : edge(e), lo(l), hi(h) {}
  int quote(int mid) const override {
    return std::clamp(mid - edge, lo, hi);
  }
};
// (end of on-screen snippet 2)
using QuoteFn = std::function<int(int)>;  // the callback flavour of the same idea
void quote_all(const QuoteFn& f, const Prices& mid, Prices& out) {
  for (int i = 0; i < kN; ++i) out[i] = f(mid[i]);
}
// Serial flavour: each tick's quote feeds the next, so nothing can vectorize.
int run_serial(const Quoter& q, const int* mid, int n) {
  int acc = 0;
  for (int i = 0; i < n; ++i) acc = q.quote(mid[i] ^ (acc & 7));
  return acc;
}
}  // namespace ai
