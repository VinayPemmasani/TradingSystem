#include <cstdio>
#include <cstring>
#include "ai.hpp"
#include "fast.hpp"
#include "inputs.hpp"
int main() {
  auto ord = make_orders(100000, 300);
  ai::Gateway A{make_limits(), {}}; fast::Gateway F{make_limits(), {}};
  for (const auto& o : ord) {
    bool a = A.on_order(o), f = F.on_order(o);
    if (a != f || std::strcmp(A.out_.last_reason, F.out_.last_reason) != 0) { std::printf("FAIL at %llu: %s | %s\n", (unsigned long long)o.id, A.out_.last_reason, F.out_.last_reason); return 1; }
  }
  if (A.out_.sent != F.out_.sent || A.out_.rejected != F.out_.rejected || A.out_.ids != F.out_.ids) { std::puts("FAIL totals"); return 1; }
  std::printf("PASS: same accept/reject and reason text for 100000 orders (%llu rejected, last: \"%s\")\n", (unsigned long long)A.out_.rejected, A.out_.last_reason);
}
