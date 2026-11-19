// Per-message allocation vs a preallocated pool with a free list.
// Each message adds an order (64 bytes) and, once 100k are live, removes a random old one.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <random>
#include <vector>
#include <sys/resource.h>
#include <x86intrin.h>

struct Order { std::uint64_t id, price, qty, ts; Order* next; char pad[24]; };
static_assert(sizeof(Order) == 64);

template <class T>
class Pool {                                   // fixed capacity, intrusive free list
 public:
  explicit Pool(std::size_t n) : slots_(n) {   // allocates and touches every slot up front
    for (std::size_t i = 0; i + 1 < n; ++i) slots_[i].next = &slots_[i + 1];
    free_ = &slots_[0];
  }
  T* get() noexcept { T* p = free_; if (p) free_ = p->next; return p; }
  void put(T* p) noexcept { p->next = free_; free_ = p; }
 private:
  std::vector<T> slots_;
  T* free_ = nullptr;
};

static long f0, df;
static long faults() { rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_minflt; }
constexpr std::size_t kLive = 100'000, kMsgs = 2'000'000;

template <class Get, class Put>
std::vector<std::uint64_t> run(Get get, Put put) {
  std::vector<Order*> live(kLive);                 // harness memory: touched before timing
  std::vector<std::uint64_t> cyc(kMsgs);
  std::size_t n = 0;
  std::mt19937_64 rng(42);
  f0 = faults();
  for (std::size_t m = 0; m < kMsgs; ++m) {
    std::size_t victim = rng() % kLive;
    std::uint64_t t0 = __rdtsc();
    Order* o = get();
    o->id = m; o->price = 100; o->qty = 10; o->ts = t0;
    if (n < kLive) live[n++] = o;
    else { put(live[victim]); live[victim] = o; }
    cyc[m] = __rdtsc() - t0;
  }
  df = faults() - f0;
  for (Order* o : live) put(o);
  return cyc;
}

static double tsc_ghz() {
  auto c0 = std::chrono::steady_clock::now(); std::uint64_t t0 = __rdtsc();
  while (std::chrono::steady_clock::now() - c0 < std::chrono::milliseconds(200)) {}
  double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - c0).count();
  return (__rdtsc() - t0) / ns;
}

static void report(const char* name, std::vector<std::uint64_t> c, double ghz) {
  std::sort(c.begin(), c.end());
  auto q = [&](double p) { return c[std::size_t(p * (c.size() - 1))] / ghz; };
  std::printf("%-9s p50 %6.1f ns  p99 %7.1f ns  p99.9 %8.1f ns  max %10.1f ns  faults %ld\n", name, q(.5), q(.99), q(.999), c.back() / ghz, df);
}

int main(int argc, char** argv) {
  double ghz = tsc_ghz();
  bool pool_first = argc > 1 && !std::strcmp(argv[1], "pool");
  if (pool_first) {
    Pool<Order> pool(kLive + 1);
    report("pool", run([&] { return pool.get(); }, [&](Order* o) { pool.put(o); }), ghz);
  } else {
    report("new", run([] { return new Order; }, [](Order* o) { delete o; }), ghz);
  }
}
