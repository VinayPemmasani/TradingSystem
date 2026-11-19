#include <cstdio>
#include "strat.hpp"
int run_virtual(const Strategy& s, const int* mids, int n);
int run_final(const Maker& s, const int* mids, int n);
int run_mixed(const Strategy* const* objs, const int* mids, int n);
int run_variant(const AnyStrategy* objs, const int* mids, int n);
int run_chosen(const AnyStrategy& chosen, const int* mids, int n);
struct Crtp; int run_crtp(const Crtp& c, const int* mids, int n);
struct Config { bool maker = true; };
AnyStrategy make_strategy(const Config& cfg);
int main() {
  int mids[3] = {100, 200, 300};
  Maker m; Taker t;
  const Strategy* objs[3] = {&m, &t, &m};
  AnyStrategy v[3] = {m, t, m};
  bool ok = run_virtual(m, mids, 3) == 594 && run_final(m, mids, 3) == 594 &&
            run_virtual(t, mids, 3) == 609 && run_mixed(objs, mids, 3) == 98 + 203 + 298 &&
            run_variant(v, mids, 3) == 599 && run_chosen(make_strategy({true}), mids, 3) == 594 &&
            run_chosen(make_strategy({false}), mids, 3) == 609 &&
            run_crtp(*reinterpret_cast<const Crtp*>(&mids[0]), mids, 3) == 594;
  std::puts(ok ? "screen test OK" : "screen test FAILED");
  return ok ? 0 : 1;
}
