// Hot-thread cost per log call: general Logger (ostream + mutex + endl) vs
// binary record into an SPSC ring drained by a background thread.
// usage: bench <path> <calls> <runs>      (path: a file or /dev/null)
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <pthread.h>
#include <sched.h>
#include <thread>
#include <vector>
#include "ai.hpp"
#include "fast.hpp"

static thread_local uint64_t t_allocs = 0;
void* operator new(size_t n) { ++t_allocs; if (void* p = malloc(n)) return p; throw std::bad_alloc(); }
void operator delete(void* p) noexcept { free(p); }
void operator delete(void* p, size_t) noexcept { free(p); }

static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
static double g_ns_per_tick;
static void calibrate() {
  auto c0 = std::chrono::steady_clock::now(); uint64_t t0 = __rdtsc();
  while (std::chrono::steady_clock::now() - c0 < std::chrono::milliseconds(100)) {}
  auto c1 = std::chrono::steady_clock::now(); uint64_t t1 = __rdtsc();
  g_ns_per_tick = std::chrono::duration<double, std::nano>(c1 - c0).count() / double(t1 - t0);
}
static inline uint64_t stamp() { unsigned a; return __rdtscp(&a); }
static void gap(uint64_t ticks) { uint64_t e = __rdtsc() + ticks; while (__rdtsc() < e) {} }

// Same as Logger but '\n' (buffered) instead of std::endl: no flush per line.
class LoggerNL {
  std::mutex mu_; std::ofstream out_;
 public:
  explicit LoggerNL(const char* p) : out_(p) {}
  void fill(const char* sym, int64_t px, uint32_t qty, uint64_t oid) {
    auto ns = std::chrono::system_clock::now().time_since_epoch().count();
    std::lock_guard lock(mu_);
    out_ << ns << " fill oid=" << oid << " sym=" << sym << " px=" << px << " qty=" << qty << '\n';
  }
};

static const char* kSyms[4] = {"AAPL", "MSFT", "NVDA", "AMZN"};
struct Res { double p50, p99, p999; double allocs; };

template <class L> Res run_hot(L& lg, int n) {
  std::vector<uint64_t> d(n);
  const uint64_t spacing = uint64_t(1000 / g_ns_per_tick);  // ~1 us of "work" between calls
  t_allocs = 0;
  for (int i = 0; i < n; ++i) {
    gap(spacing);
    uint64_t t0 = stamp();
    lg.fill(kSyms[i & 3], 1'893'400 + (i % 97), 100 + (i % 7), 9'000'000 + i);
    d[i] = stamp() - t0;
  }
  Res r; double a = double(t_allocs) / n;
  std::sort(d.begin(), d.end());
  r.p50 = d[n / 2] * g_ns_per_tick; r.p99 = d[n * 99 / 100] * g_ns_per_tick; r.p999 = d[n * 999 / 1000] * g_ns_per_tick; r.allocs = a;
  return r;
}

static Res empty_timer(int n) {
  struct Nop { void fill(const char*, int64_t, uint32_t, uint64_t) { asm volatile("" ::: "memory"); } } nop;
  return run_hot(nop, n);
}

static LogRing<1 << 16> g_ring;
static Res run_fast(const char* path, int n, uint64_t* written, uint64_t* dropped) {
  FILE* f = fopen(path, "w"); setvbuf(f, nullptr, _IOFBF, 1 << 16);
  std::atomic<bool> stop{false};
  uint64_t tsc0 = __rdtsc(), wall0 = std::chrono::system_clock::now().time_since_epoch().count();
  *written = 0;
  std::thread bg([&] { pin(0); while (!stop.load(std::memory_order_acquire)) { if (!(*written += g_ring.drain(f, g_ns_per_tick, tsc0, wall0))) std::this_thread::sleep_for(std::chrono::microseconds(50)); }
                       *written += g_ring.drain(f, g_ns_per_tick, tsc0, wall0); });
  g_ring.dropped = 0;
  Res r = run_hot(g_ring, n);
  stop.store(true, std::memory_order_release); bg.join(); fclose(f);
  *dropped = g_ring.dropped;
  return r;
}

int main(int argc, char** argv) {
  const char* path = argc > 1 ? argv[1] : "/dev/null";
  int n = argc > 2 ? atoi(argv[2]) : 200000, runs = argc > 3 ? atoi(argv[3]) : 5;
  pin(1); calibrate();
  Res e = empty_timer(n);
  printf("sink=%s calls=%d  timer overhead p50 %.1f ns (included below)\n", path, n, e.p50);
  for (int k = 0; k < runs; ++k) {
    Res a, b, c; uint64_t w, dr;
    { Logger lg(path); a = run_hot(lg, n); }
    { LoggerNL lg(path); b = run_hot(lg, n); }
    c = run_fast(path, n, &w, &dr);
    printf("run %d  endl: p50 %7.1f p99 %8.1f p99.9 %8.1f alloc/call %.2f | '\\n': p50 %6.1f p99 %7.1f p99.9 %8.1f | ring: p50 %5.1f p99 %6.1f p99.9 %6.1f alloc/call %.2f written %lu dropped %lu\n",
           k, a.p50, a.p99, a.p999, a.allocs, b.p50, b.p99, b.p999, c.p50, c.p99, c.p999, c.allocs, (unsigned long)w, (unsigned long)dr);
  }
}
