// False sharing on two counters. Each pinned thread does N relaxed fetch_adds on its own
// counter, timed in chunks of 10,000 with rdtsc; the median chunk filters out preemption.
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <pthread.h>
#include <thread>
#include <vector>
#include <x86intrin.h>

struct Packed {                       // a and b share one 64-byte line
  std::atomic<long> a{0};
  std::atomic<long> b{0};
};
struct Padded {                       // each counter starts its own line
  alignas(64) std::atomic<long> a{0};
  alignas(64) std::atomic<long> b{0};
};
static_assert(sizeof(Packed) == 16 && sizeof(Padded) == 128);

constexpr long kChunk = 10'000, kChunks = 10'000;   // 100 million increments per thread

static void pin(int cpu) {
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s);
  pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}
static void bump(std::atomic<long>& c, int cpu, std::atomic<int>& go, std::vector<std::uint64_t>& t) {
  pin(cpu); go.fetch_add(1); while (go.load() < 2) {}
  for (long k = 0; k < kChunks; ++k) {
    std::uint64_t t0 = __rdtsc();
    for (long i = 0; i < kChunk; ++i) c.fetch_add(1, std::memory_order_relaxed);
    t[k] = __rdtsc() - t0;
  }
}
template <class C>
double run(C& c, double ghz) {       // median ns per increment over both threads' chunks
  std::vector<std::uint64_t> ta(kChunks), tb(kChunks);
  std::atomic<int> go{0};
  std::thread x(bump, std::ref(c.a), 1, std::ref(go), std::ref(ta));
  std::thread y(bump, std::ref(c.b), 2, std::ref(go), std::ref(tb));
  x.join(); y.join();
  ta.insert(ta.end(), tb.begin(), tb.end());
  std::nth_element(ta.begin(), ta.begin() + ta.size() / 2, ta.end());
  return ta[ta.size() / 2] / ghz / kChunk;
}
static double tsc_ghz() {
  auto c0 = std::chrono::steady_clock::now(); std::uint64_t t0 = __rdtsc();
  while (std::chrono::steady_clock::now() - c0 < std::chrono::milliseconds(200)) {}
  return (__rdtsc() - t0) / std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - c0).count();
}
int main() {             // run as: chrt -f 10 ./fs3 (real-time, so both threads run together)
  pin(0);
  double ghz = tsc_ghz();
  for (int r = 0; r < 5; ++r) {
    alignas(64) static Packed p; alignas(64) static Padded q;
    double tp = run(p, ghz), tq = run(q, ghz);
    std::printf("packed %5.2f ns/inc   padded %5.2f ns/inc   x%.1f\n", tp, tq, tp / tq);
    std::fflush(stdout);
  }
}
