// Two threads, each owns one counter (single writer, like a ring index).
// Packed: both counters share a 64-byte line. Padded: alignas(64) puts each on its own line.
#include <atomic>
#include <chrono>
#include <cstdio>
#include <pthread.h>
#include <thread>

struct Packed {
  std::atomic<long> a{0};
  std::atomic<long> b{0};
};
struct Padded {
  alignas(64) std::atomic<long> a{0};
  alignas(64) std::atomic<long> b{0};
};
static_assert(sizeof(Packed) == 16 && sizeof(Padded) == 128);

constexpr long N = 200'000'000;

static void pin(int cpu) {
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s);
  pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}
static void bump(std::atomic<long>& c, int cpu) {
  pin(cpu);
  for (long i = 0; i < N; ++i) c.store(c.load(std::memory_order_relaxed) + 1, std::memory_order_relaxed);
}
template <class C>
double run(C& c) {
  auto t0 = std::chrono::steady_clock::now();
  std::thread x(bump, std::ref(c.a), 1), y(bump, std::ref(c.b), 2);
  x.join(); y.join();
  return std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count() * 1e9 / N;
}
int main() {
  for (int r = 0; r < 7; ++r) {
    alignas(64) static Packed p; alignas(64) static Padded q;
    p.a = p.b = q.a = q.b = 0;
    double tp = run(p), tq = run(q);
    std::printf("packed %6.2f ns/inc   padded %5.2f ns/inc   x%.1f\n", tp, tq, tp / tq);
  }
}
