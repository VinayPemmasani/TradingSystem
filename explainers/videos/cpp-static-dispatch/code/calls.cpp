// The loops, in their own translation unit so nothing is devirtualized by accident.
// Every snippet here is shown on screen verbatim.
#include "strat.hpp"

int run_virtual(const Strategy& s, const int* mids, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i) sum += s.quote(mids[i]);
  return sum;
}

int run_final(const Maker& s, const int* mids, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i) sum += s.quote(mids[i]);
  return sum;
}

template <Quoter S>
int run_static(const S& s, const int* mids, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i) sum += s.quote(mids[i]);
  return sum;
}
template int run_static<Maker>(const Maker&, const int*, int);

int run_mixed(const Strategy* const* objs, const int* mids, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i) sum += objs[i]->quote(mids[i]);
  return sum;
}

int run_variant(const AnyStrategy* objs,
                const int* mids, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i)
    sum += std::visit([&](const auto& s) {
      return s.quote(mids[i]); }, objs[i]);
  return sum;
}

int run_chosen(const AnyStrategy& chosen,
               const int* mids, int n) {
  return std::visit([&](const auto& s) {
    return run_static(s, mids, n);  // monomorphic
  }, chosen);
}

// CRTP: static dispatch through a base class.
template <class D>
struct Base {
  int quote(int mid) const {
    return static_cast<const D*>(this)->impl(mid);
  }
};
struct Crtp : Base<Crtp> {
  int impl(int mid) const { return mid - 2; }
};
int run_crtp(const Crtp& c, const int* mids, int n) { return run_static(c, mids, n); }

// At startup.
struct Config { bool maker = true; };
AnyStrategy make_strategy(const Config& cfg) {
  AnyStrategy chosen = cfg.maker ? AnyStrategy{Maker{}}
                                 : AnyStrategy{Taker{}};
  return chosen;
}
