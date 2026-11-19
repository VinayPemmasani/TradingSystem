// Single-thread per-message latency: lfence;rdtsc around each on_msg call.
// usage: bench [messages] [runs] [version]
#include <cstdio>
#include <memory>
#include <pthread.h>
#include <sched.h>
#include "all.hpp"

// Count every allocation. GCC 13 flags free() inside a replaced operator delete as
// "mismatched" (a known false positive for replacement allocators).
#pragma GCC diagnostic ignored "-Wmismatched-new-delete"
void* operator new(std::size_t n) {
  if (g_count_allocs) g_allocs.fetch_add(1, std::memory_order_relaxed);
  if (void* p = std::malloc(n ? n : 1)) return p;
  throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

struct Empty { int on_msg(const Msg&) { return 0; } std::uint64_t report() const { return 0; } };

static double TPN;
template <class H> void bench(const char* name, const std::vector<Msg>& feed, int runs) {
  std::vector<std::uint32_t> c(feed.size());
  std::vector<Pct> ps;
  std::uint64_t allocs = 0, sink = 0;
  { auto w = std::make_unique<H>(); for (const Msg& m : feed) sink += std::uint64_t(w->on_msg(m) + 1); }  // warm-up pass
  for (int r = 0; r < runs; ++r) {
    auto h = std::make_unique<H>();
    g_allocs = 0; g_count_allocs = true;
    for (std::size_t i = 0; i < feed.size(); ++i) {
      std::uint64_t t0 = tsc_begin();
      int s = h->on_msg(feed[i]);
      std::uint64_t t1 = tsc_end();
      c[i] = std::uint32_t(t1 - t0);
      sink += std::uint64_t(s + 1);
    }
    g_count_allocs = false; allocs = g_allocs;
    ps.push_back(percentiles(c, TPN));
  }
  auto med = [&](auto f) { std::vector<double> v; for (auto& p : ps) v.push_back(f(p)); std::sort(v.begin(), v.end()); return v; };
  auto p50 = med([](const Pct& p) { return p.p50; }), p99 = med([](const Pct& p) { return p.p99; });
  auto p999 = med([](const Pct& p) { return p.p999; }), mx = med([](const Pct& p) { return p.max; });
  std::size_t k = ps.size() / 2;
  std::printf("%-10s p50 %6.1f ns [%5.1f-%5.1f]  p99 %7.1f ns [%6.1f-%6.1f]  p99.9 %8.1f  max %9.0f  allocs/run %8llu  (sink %llu)\n",
              name, p50[k], p50.front(), p50.back(), p99[k], p99.front(), p99.back(), p999[k], mx[k],
              (unsigned long long)allocs, (unsigned long long)(sink & 1));
}
int main(int argc, char** argv) {
  setvbuf(stdout, nullptr, _IONBF, 0);
  std::size_t n = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 2000000;
  int runs = argc > 2 ? std::atoi(argv[2]) : 7;
  std::string only = argc > 3 ? argv[3] : "";
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(2, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s);
  TPN = tsc_per_ns();
  std::printf("tsc %.4f ticks/ns, %zu msgs, %d runs, median [min-max] over runs\n", TPN, n, runs);
  auto feed = make_feed(n);
  auto want = [&](const char* v) { return only.empty() || only == v; };
  if (want("e")) bench<Empty>("timer", feed, runs);
  if (want("0")) bench<v0::Handler>("v0 naive", feed, runs);
  if (want("1")) bench<v1::Handler>("v1 ds", feed, runs);
  if (want("1h")) bench<v1h::Handler>("v1h table", feed, runs);
  if (want("2a")) bench<v2a::Handler>("v2a ilp", feed, runs);
  if (want("2")) bench<v2::Handler>("v2 pipe", feed, runs);
  if (want("3")) bench<v3::Handler>("v3 branch", feed, runs);
  if (want("4")) bench<v4::Handler>("v4 alloc", feed, runs);
}
