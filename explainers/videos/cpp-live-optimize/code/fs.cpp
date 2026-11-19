// MESI ping-pong in isolation: two threads each bump their own counter.
// packed: both counters in one 64-byte line; padded: alignas(64) each.
// Also checks the TSC is in step across the two cores (ping-pong, one-way both ways).
#include <algorithm>
#include <cstdio>
#include <thread>
#include <vector>
#include <pthread.h>
#include "common.hpp"
static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
struct Packed { std::atomic<std::uint64_t> a{0}, b{0}; };
struct Padded { alignas(64) std::atomic<std::uint64_t> a{0}; alignas(64) std::atomic<std::uint64_t> b{0}; };
template <class S> double bump(std::uint64_t n, double tpn) {
  static S s; s.a = 0; s.b = 0;
  std::atomic<int> go{0};
  pin(1);
  std::thread t([&] { go.fetch_add(1); while (go.load() < 2) {}
    for (std::uint64_t i = 0; i < n; ++i) s.a.fetch_add(1, std::memory_order_relaxed); });
  pin(2);
  go.fetch_add(1); while (go.load() < 2) {}
  std::uint64_t t0 = __rdtsc();
  for (std::uint64_t i = 0; i < n; ++i) s.b.fetch_add(1, std::memory_order_relaxed);   // a stats counter
  std::uint64_t t1 = __rdtsc();
  t.join();
  return (t1 - t0) / tpn / n;
}
int main() {
  double tpn = tsc_per_ns();
  for (int r = 0; r < 7; ++r) {
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    double p = bump<Packed>(5000000, tpn);
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    double q = bump<Padded>(5000000, tpn);
    std::printf("ns per increment: same line %.1f   own lines %.1f\n", p, q);
  }
  // TSC step check
  alignas(64) static std::atomic<std::uint64_t> ping{0};
  alignas(64) static std::atomic<std::uint64_t> pong{0};
  const int N = 200000; std::vector<std::int64_t> ab(N), ba(N);
  pin(1);
  std::thread t([&] { for (int i = 1; i <= N; ++i) { std::uint64_t v; while ((v = ping.load(std::memory_order_acquire)) == 0) {}
      ab[i - 1] = std::int64_t(__rdtsc() - v); ping.store(0, std::memory_order_relaxed); pong.store(__rdtsc(), std::memory_order_release); } });
  pin(2);
  for (int i = 1; i <= N; ++i) { ping.store(__rdtsc(), std::memory_order_release); std::uint64_t v; while ((v = pong.load(std::memory_order_acquire)) == 0) {}
    ba[i - 1] = std::int64_t(__rdtsc() - v); pong.store(0, std::memory_order_relaxed); }
  t.join();
  std::sort(ab.begin(), ab.end()); std::sort(ba.begin(), ba.end());
  std::printf("one-way median: cpu2->cpu1 %.0f ns   cpu1->cpu2 %.0f ns  (equal => TSCs in step)\n", ab[N / 2] / tpn, ba[N / 2] / tpn);
}
