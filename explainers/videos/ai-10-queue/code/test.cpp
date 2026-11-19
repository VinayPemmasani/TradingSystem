// Both queues deliver the same messages in the same order (two threads, 1M msgs).
#include <cstdio>
#include <thread>
#include "ai.hpp"
#include "fast.hpp"
#include "msg.hpp"
template <class Q> unsigned long long check(Q& q, int n) {
  unsigned long long h = 1469598103934665603ull; bool order = true;
  std::thread c([&] { for (int i = 0; i < n; ++i) { Tick t = q.pop(); if (t.seq != (uint64_t)i) order = false;
                      h = (h ^ (t.seq * 31 + (uint64_t)t.px)) * 1099511628211ull; } });
  for (int i = 0; i < n; ++i) { Tick t{0, (uint64_t)i, 1000 + i % 77, 1, 2};
    if constexpr (requires { q.try_push(t); }) { while (!q.try_push(t)) {} } else q.push(t); }
  c.join();
  return order ? h : 0;
}
static SpscRing<Tick, 64> ring;   // small ring: exercises full and empty
int main() {
  BlockingQueue<Tick> bq;
  auto a = check(bq, 1000000), b = check(ring, 1000000);
  bool ok = a && a == b;
  printf("%s: hash %llx vs %llx\n", ok ? "PASS" : "FAIL", a, b);
  return ok ? 0 : 1;
}
