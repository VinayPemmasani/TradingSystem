#include <cstdint>
#include <cstdio>
#include <thread>
#include "mutex_queue.hpp"
#include "ring.hpp"
#include "ring_simple.hpp"

template <class Q> bool check(const char* name, std::uint64_t n) {
  static Q q;
  std::thread prod([&] {
    for (std::uint64_t i = 1; i <= n; ++i)
      while (!q.try_push(i)) {}
  });
  std::uint64_t expect = 1, v;
  bool ok = true;
  while (expect <= n) {
    if (!q.try_pop(v)) continue;
    if (v != expect) { ok = false; break; }
    ++expect;
  }
  prod.join();
  ok = ok && !q.try_pop(v);  // drained
  std::printf("%-12s %s: %llu values, in order, none lost\n", name, ok ? "ok" : "FAILED",
              (unsigned long long)(expect - 1));
  return ok;
}

int main(int argc, char** argv) {
  std::uint64_t n = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 10'000'000;
  // Small capacity on purpose: the ring wraps and fills constantly.
  bool ok = check<Ring<std::uint64_t, 8>>("Ring", n) &
            check<RingNoCache<std::uint64_t, 8>>("RingNoCache", n) &
            check<MutexQueue<std::uint64_t, 8>>("MutexQueue", n / 10);
  // single-thread edge cases
  Ring<int, 4> r; int x;
  for (int i = 0; i < 4; ++i) ok &= r.try_push(i);
  ok &= !r.try_push(9);                      // full at N
  ok &= r.try_pop(x) && x == 0 && r.try_push(4);
  for (int i = 1; i <= 4; ++i) ok &= r.try_pop(x) && x == i;
  ok &= !r.try_pop(x);                       // empty
  std::puts(ok ? "all tests passed" : "TESTS FAILED");
  return ok ? 0 : 1;
}
