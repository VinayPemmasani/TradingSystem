// (1) publish loop, one thread: write a 16-byte slot, publish the index.
//     seq_cst store (xchg) vs release store (mov). ns per publish.
// (2) two threads through the SPSC ring: RingSeq (all seq_cst) vs RingAR. ns per message.
// usage: bench <publish_iters> <ring_msgs> <runs>     (run under chrt -f 10)
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <pthread.h>
#include <thread>
#include "ai.hpp"
#include "fast.hpp"

struct Quote { int64_t px; int64_t qty; };
static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
using clk = std::chrono::steady_clock;
static double ns_since(clk::time_point t0) { return std::chrono::duration<double, std::nano>(clk::now() - t0).count(); }

alignas(64) static std::atomic<uint64_t> g_head{0};
alignas(64) static Quote g_slot[1024];

__attribute__((noinline)) static void pub_seq(uint64_t n) {
  for (uint64_t i = 0; i < n; ++i) {
    uint64_t h = g_head.load();
    g_slot[h & 1023] = Quote{int64_t(i), 100};
    g_head.store(h + 1);
  }
}
__attribute__((noinline)) static void pub_rel(uint64_t n) {
  for (uint64_t i = 0; i < n; ++i) {
    uint64_t h = g_head.load(std::memory_order_relaxed);
    g_slot[h & 1023] = Quote{int64_t(i), 100};
    g_head.store(h + 1, std::memory_order_release);
  }
}

template <class R> double two_threads(R& r, uint64_t n) {
  int64_t sum = 0;
  pin(1);                       // child inherits CPU 1, so it can start while main spins on CPU 0
  auto t0 = clk::now();
  std::thread prod([&] { pin(1); for (uint64_t i = 1; i <= n; ++i) while (!r.try_push(Quote{int64_t(i), 1})) {} });
  pin(0);
  Quote q;
  for (uint64_t got = 0; got < n;) if (r.try_pop(q)) { sum += q.px; ++got; }
  prod.join();
  double ns = ns_since(t0) / n;
  if (sum != int64_t(n * (n + 1) / 2)) std::puts("BAD SUM");
  return ns;
}

static RingSeq<Quote, 1024> g_rs;
static RingAR<Quote, 1024> g_ra;
int main(int argc, char** argv) {
  uint64_t pn = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000;
  uint64_t rn = argc > 2 ? strtoull(argv[2], 0, 10) : 20000000;
  int runs = argc > 3 ? atoi(argv[3]) : 5;
  pin(0);
  for (int r = 0; r < runs; ++r) {
    auto t0 = clk::now(); pub_seq(pn); double s = ns_since(t0) / pn;
    t0 = clk::now(); pub_rel(pn); double a = ns_since(t0) / pn;
    double rs = rn ? two_threads(g_rs, rn) : 0, ra = rn ? two_threads(g_ra, rn) : 0;
    printf("run %d  publish loop ns/op: seq_cst %.2f  release %.2f  | 2-thread ring ns/msg: seq_cst %.2f  acq/rel %.2f\n", r, s, a, rs, ra);
  }
}
