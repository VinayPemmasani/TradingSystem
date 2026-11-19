// Both rings deliver the same sequence across two threads (small ring: full/empty paths).
#include <cstdio>
#include <thread>
#include "ai.hpp"
#include "fast.hpp"
template <class R> unsigned long long run(R& r, int n) {
  unsigned long long h = 1469598103934665603ull; bool ord = true;
  std::thread c([&] { long v; for (int i = 0; i < n; ++i) { while (!r.try_pop(v)) {} if (v != i) ord = false; h = (h ^ (unsigned long long)v) * 1099511628211ull; } });
  for (int i = 0; i < n; ++i) while (!r.try_push(i)) {}
  c.join(); return ord ? h : 0;
}
static RingSeq<long, 16> a; static RingAR<long, 16> b;
int main() { auto x = run(a, 2000000), y = run(b, 2000000); bool ok = x && x == y;
  printf("%s %llx %llx\n", ok ? "PASS" : "FAIL", x, y); return ok ? 0 : 1; }
