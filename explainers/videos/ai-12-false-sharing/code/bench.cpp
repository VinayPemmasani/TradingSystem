// (1) two threads, each increments its own counter (fetch_add relaxed) 100M times.
// (2) SPSC ring, 20M 8-byte messages, packed vs padded indices.
// usage: chrt -f 10 ./bench <incs> <msgs> <runs>
#include <chrono>
#include <cstddef>
#include <functional>
#include <cstdio>
#include <cstdlib>
#include <pthread.h>
#include <thread>
#include "ai.hpp"
#include "fast.hpp"
#include "ring_ops.hpp"
static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
using clk = std::chrono::steady_clock;
static const int A = 1, B = 0;

template <class F> double two(F&& fa, F&& fb) {   // run fa on CPU A, fb on CPU B; wall ns
  pin(A);                                          // child inherits A, starts while main spins on B
  auto t0 = clk::now();
  std::thread t([&] { pin(A); fa(); });
  pin(B); fb(); t.join();
  return std::chrono::duration<double, std::nano>(clk::now() - t0).count();
}

static CountersPacked g_cp; static CountersPadded g_cd;
static RingPacked<uint64_t, 1024> g_rp; static RingPadded<uint64_t, 1024> g_rd;

template <class R> double ring(R& r, uint64_t n) {
  uint64_t sum = 0;
  double ns = two(std::function<void()>([&] { for (uint64_t i = 1; i <= n; ++i) while (!push<R, uint64_t, 1024>(r, i)) {} }),
                  std::function<void()>([&] { uint64_t v; for (uint64_t g = 0; g < n;) if (pop<R, uint64_t, 1024>(r, v)) { sum += v; ++g; } }));
  if (sum != n * (n + 1) / 2) std::puts("BAD SUM");
  return ns / n;
}

int main(int argc, char** argv) {
  uint64_t inc = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000, msgs = argc > 2 ? strtoull(argv[2], 0, 10) : 20000000;
  int runs = argc > 3 ? atoi(argv[3]) : 5;
  printf("sizeof CountersPacked %zu, CountersPadded %zu; &n[1]-&n[0] = %td bytes, &c[1]-&c[0] = %td bytes\n",
         sizeof(CountersPacked), sizeof(CountersPadded),
         (char*)&g_cp.n[1] - (char*)&g_cp.n[0], (char*)&g_cd.c[1] - (char*)&g_cd.c[0]);
  printf("RingPacked: head@%zu tail@%zu buf@%zu | RingPadded: head@%zu tail@%zu buf@%zu\n",
         offsetof(decltype(g_rp), head), offsetof(decltype(g_rp), tail), offsetof(decltype(g_rp), buf),
         offsetof(decltype(g_rd), head), offsetof(decltype(g_rd), tail), offsetof(decltype(g_rd), buf));
  for (int r = 0; r < runs; ++r) {
    double p = two(std::function<void()>([&] { for (uint64_t i = 0; i < inc; ++i) g_cp.n[0].fetch_add(1, std::memory_order_relaxed); }),
                   std::function<void()>([&] { for (uint64_t i = 0; i < inc; ++i) g_cp.n[1].fetch_add(1, std::memory_order_relaxed); })) / inc;
    double d = two(std::function<void()>([&] { for (uint64_t i = 0; i < inc; ++i) g_cd.c[0].n.fetch_add(1, std::memory_order_relaxed); }),
                   std::function<void()>([&] { for (uint64_t i = 0; i < inc; ++i) g_cd.c[1].n.fetch_add(1, std::memory_order_relaxed); })) / inc;
    double rp = ring(g_rp, msgs), rd = ring(g_rd, msgs);
    printf("run %d  counters ns/inc: packed %.2f padded %.2f | ring ns/msg: packed %.2f padded %.2f\n", r, p, d, rp, rd);
  }
  if (g_cp.n[0] != g_cd.c[0].n || g_cp.n[1] != g_cd.c[1].n) std::puts("COUNT MISMATCH");
}
