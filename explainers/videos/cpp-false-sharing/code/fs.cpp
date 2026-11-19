// Two threads, each incrementing its own counter. Packed: both on one line. Padded: one line each.
#include <atomic>
#include <chrono>
#include <cstdio>
#include <new>
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
static_assert(sizeof(Packed) == 16);
static_assert(sizeof(Padded) == 128);

constexpr long N = 100'000'000;

static void pin(int cpu) {
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s);
  pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}

template <class C>
double run(C& c) {
  auto t0 = std::chrono::steady_clock::now();
  std::thread x([&] { pin(1); for (long i = 0; i < N; ++i) c.a.fetch_add(1, std::memory_order_relaxed); });
  std::thread y([&] { pin(2); for (long i = 0; i < N; ++i) c.b.fetch_add(1, std::memory_order_relaxed); });
  x.join(); y.join();
  return std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
  for (int r = 0; r < 5; ++r) {
    alignas(64) Packed p; alignas(64) Padded q;
    double tp = run(p), tq = run(q);
    std::printf("packed %.3f s (%.2f ns/inc)  padded %.3f s (%.2f ns/inc)  x%.1f\n",
                tp, tp * 1e9 / N, tq, tq * 1e9 / N, tp / tq);
  }
#ifdef __cpp_lib_hardware_interference_size
  std::printf("hardware_destructive_interference_size = %zu\n", std::hardware_destructive_interference_size);
#else
  std::printf("no __cpp_lib_hardware_interference_size\n");
#endif
}
