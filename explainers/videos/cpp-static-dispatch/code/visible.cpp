#include "strat.hpp"
int f(int x) {
  Taker m; Strategy& s = m;
  return s.quote(x);  // direct
}
