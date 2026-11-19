#include <cstdio>
#include "ai.hpp"
#include "fast.hpp"
#include "mid.hpp"
#include "inputs.hpp"
int main() {
  Limits lim = make_limits(); auto ord = make_orders(20000);
  int pass = 0;
  for (const auto& o : ord) {
    std::string a, m; fast::Tag t;
    bool ra = ai::on_order(o, lim, a), rm = mid::on_order(o, lim, m), rf = fast::on_order(o, lim, t);
    if (ra != rf || ra != rm) { std::puts("FAIL result"); return 1; }
    if (ra) { ++pass; if (a != std::string_view(t.b.data(), t.n) || a != m) { std::printf("FAIL tag %s\n", a.c_str()); return 1; } }
  }
  std::printf("PASS: identical accept/reject and tags for 20000 orders (%d accepted), e.g. tag of first accepted order computed\n", pass);
}
