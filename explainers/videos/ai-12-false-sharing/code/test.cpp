// Same results for both layouts: counter totals and ring sums across two threads.
#include <cstdio>
#include <thread>
#include "ai.hpp"
#include "fast.hpp"
#include "ring_ops.hpp"
static RingPacked<long, 8> rp; static RingPadded<long, 8> rd;
template <class R> unsigned long long ring(R& r) { unsigned long long s = 0; long v;  // unsigned: the hash may wrap
  std::thread c([&] { for (int g = 0; g < 1000000;) if (pop<R, long, 8>(r, v)) { s = s * 31 + v; ++g; } });
  for (long i = 0; i < 1000000; ++i) while (!push<R, long, 8>(r, i)) {}
  c.join(); return s; }
int main() {
  CountersPacked p; CountersPadded d;
  std::thread a([&] { for (int i = 0; i < 1000000; ++i) { p.n[0].fetch_add(1); d.c[0].n.fetch_add(1); } });
  for (int i = 0; i < 2000000; ++i) { p.n[1].fetch_add(1); d.c[1].n.fetch_add(1); }
  a.join();
  unsigned long long x = ring(rp), y = ring(rd);
  bool ok = p.n[0] == d.c[0].n && p.n[1] == d.c[1].n && x == y;
  printf("%s counters %lu/%lu ring hash %llx %llx\n", ok ? "PASS" : "FAIL", (unsigned long)p.n[0], (unsigned long)p.n[1], x, y);
  return ok ? 0 : 1;
}
