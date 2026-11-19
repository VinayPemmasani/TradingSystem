// Throughput: one producer thread, one consumer thread, pinned to different cores.
// Round trip: ping-pong over two queues, median and p99 of 200k round trips.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <pthread.h>
#include <sched.h>
#include <thread>
#include <vector>
#include "mutex_queue.hpp"
#include "ring.hpp"
#include "ring_simple.hpp"

static bool g_pin = true;
static void pin(int cpu) {
  if (!g_pin) return;
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s);
  pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}
using clk = std::chrono::steady_clock;
constexpr int P = 1, C = 2;

template <class Q> double throughput(std::uint64_t n) {
  static Q q;
  std::uint64_t sum = 0;
  auto t0 = clk::now();
  std::thread prod([&] { pin(P); for (std::uint64_t i = 1; i <= n; ++i) while (!q.try_push(i)) {} });
  pin(C);
  std::uint64_t v;
  for (std::uint64_t got = 0; got < n;) if (q.try_pop(v)) { sum += v; ++got; }
  prod.join();
  auto t1 = clk::now();
  if (sum != n * (n + 1) / 2) std::puts("BAD SUM");
  return std::chrono::duration<double, std::nano>(t1 - t0).count() / n;
}

template <class Q> void roundtrip(const char* name, int n) {
  static Q a, b;
  std::thread echo([&] { pin(P); std::uint64_t v; for (int i = 0; i < n; ++i) { while (!a.try_pop(v)) {} while (!b.try_push(v)) {} } });
  pin(C);
  std::vector<double> rt(n);
  std::uint64_t v;
  for (int i = 0; i < n; ++i) {
    auto t0 = clk::now();
    while (!a.try_push(i)) {}
    while (!b.try_pop(v)) {}
    rt[i] = std::chrono::duration<double, std::nano>(clk::now() - t0).count();
  }
  echo.join();
  std::sort(rt.begin(), rt.end());
  std::printf("  round trip %-12s median %6.0f ns  p99 %7.0f ns\n", name, rt[n / 2], rt[n * 99 / 100]);
}

int main(int argc, char** argv) {
  setvbuf(stdout, nullptr, _IONBF, 0);
  g_pin = getenv("NOPIN") == nullptr;
  const std::uint64_t n = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 20000000;
  for (int r = 0; r < 3; ++r) {
    double m = throughput<MutexQueue<std::uint64_t, 1024>>(n / 10);
    double s = throughput<RingNoCache<std::uint64_t, 1024>>(n);
    double c = throughput<Ring<std::uint64_t, 1024>>(n);
    std::printf("run %d  ns/msg: mutex %.1f  ring(no cache) %.1f  ring(cached) %.1f\n", r, m, s, c);
  }
  roundtrip<MutexQueue<std::uint64_t, 1024>>("mutex", 200000);
  roundtrip<Ring<std::uint64_t, 1024>>("ring", 200000);
}
