// What a caller of the general version sees: an interface, chosen at run time (e.g. from config).
#pragma once
#include <functional>
#include "prices.hpp"
namespace ai {
struct Quoter;
using QuoteFn = std::function<int(int)>;
const Quoter& make_clamp(int edge, int lo, int hi);   // factory, defined in lib.cpp
void quote_all(const Quoter& q, const Prices& mid, Prices& out);
void quote_all(const QuoteFn& f, const Prices& mid, Prices& out);
int run_serial(const Quoter& q, const int* mid, int n);
}  // namespace ai
