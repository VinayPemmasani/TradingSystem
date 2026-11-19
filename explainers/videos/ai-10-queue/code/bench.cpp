// One-way latency feed thread -> strategy thread. The feed stamps rdtsc into the
// message; the strategy reads rdtsc when it gets it (invariant TSC, same socket).
// usage: bench <msgs> <gap_ns> <runs>   (run under chrt -f 10)
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <pthread.h>
#include <sys/resource.h>
#include <thread>
#include <vector>
#include <x86intrin.h>
#include "ai.hpp"
#include "fast.hpp"
#include "msg.hpp"

static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
static double g_nspt;
static void calibrate() {
  auto c0 = std::chrono::steady_clock::now(); uint64_t t0 = __rdtsc();
  while (std::chrono::steady_clock::now() - c0 < std::chrono::milliseconds(100)) {}
  auto c1 = std::chrono::steady_clock::now(); uint64_t t1 = __rdtsc();
  g_nspt = std::chrono::duration<double, std::nano>(c1 - c0).count() / double(t1 - t0);
}
static int FEED = 1, STRAT = 0;

struct Out { double p50, p99, p999; bool ok; double csw; };
template <class Q> Out run(Q& q, int n, uint64_t gap_ticks) {
  std::vector<uint64_t> lat(n);
  bool ok = true; double csw = 0;
  std::thread strat([&] {
    pin(STRAT);
    rusage r0; getrusage(RUSAGE_THREAD, &r0);
    for (int i = 0; i < n; ++i) {
      Tick t = q.pop();
      lat[i] = __rdtsc() - t.tsc;
      if (t.seq != uint64_t(i)) ok = false;
    }
    rusage r1; getrusage(RUSAGE_THREAD, &r1);
    csw = double((r1.ru_nvcsw + r1.ru_nivcsw) - (r0.ru_nvcsw + r0.ru_nivcsw)) / n;
  });
  pin(FEED);
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  for (int i = 0; i < n; ++i) {
    uint64_t e = __rdtsc() + gap_ticks; while (__rdtsc() < e) {}
    Tick t{__rdtsc(), uint64_t(i), 1'893'400 + i % 50, 100, 7};
    if constexpr (requires { q.try_push(t); }) { while (!q.try_push(t)) _mm_pause(); }
    else q.push(t);
  }
  strat.join();
  std::sort(lat.begin(), lat.end());
  return {lat[n / 2] * g_nspt, lat[size_t(n) * 99 / 100] * g_nspt, lat[size_t(n) * 999 / 1000] * g_nspt, ok, csw};
}

static SpscRing<Tick, 1024> g_ring;
int main(int argc, char** argv) {
  int n = argc > 1 ? atoi(argv[1]) : 200000;
  double gap = argc > 2 ? atof(argv[2]) : 2000;
  int runs = argc > 3 ? atoi(argv[3]) : 5;
  if (argc > 5) { FEED = atoi(argv[4]); STRAT = atoi(argv[5]); }
  calibrate();
  uint64_t gt = uint64_t(gap / g_nspt);
  printf("msgs=%d gap=%.0f ns feed cpu %d strat cpu %d\n", n, gap, FEED, STRAT);
  for (int r = 0; r < runs; ++r) {
    BlockingQueue<Tick> bq;
    Out a = run(bq, n, gt);
    Out b = run(g_ring, n, gt);
    printf("run %d  mutex+cv: p50 %7.0f p99 %8.0f p99.9 %8.0f %s ctxsw/msg %.2f | spsc: p50 %5.0f p99 %6.0f p99.9 %6.0f %s ctxsw/msg %.4f\n",
           r, a.p50, a.p99, a.p999, a.ok ? "ok" : "BAD", a.csw, b.p50, b.p99, b.p999, b.ok ? "ok" : "BAD", b.csw);
  }
}
