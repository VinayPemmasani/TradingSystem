// Two threads: feed (CPU 1) stamps each message with rdtsc and hands it over;
// strategy (CPU 2) runs the step-4 handler. Latency = strategy done - feed stamp.
// usage: mt [messages] [gap_ns] [runs] [variant]
#include <cstddef>
#include <cstdio>
#include <memory>
#include <string>
#include <thread>
#include <pthread.h>
#include "lab/core/spsc_ring.hpp"
#include "queues.hpp"
#include "v4_alloc.hpp"

constexpr std::size_t kRing = 1024;
struct alignas(64) Stat { std::uint64_t n = 0; };
struct LabRing {                       // step 6b: the lab's SpscRing (cached indices)
  lab::SpscRing<Msg, kRing> r;
  Stat pushed, popped;
  bool try_push(const Msg& m) { bool ok = r.try_push(m); pushed.n += ok; return ok; }
  bool try_pop(Msg& m) { bool ok = r.try_pop(m); popped.n += ok; return ok; }
};

static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
static double TPN;
static std::uint64_t g_expect = 0;

template <class Q> void pop_one(Q& q, Msg& m) {
  if constexpr (requires { q.pop_wait(m); }) q.pop_wait(m);
  else while (!q.try_pop(m)) {}
}

struct Res { std::vector<Pct> ps; std::vector<double> wall; };

template <class Q> void run_once(const char* name, const std::vector<Msg>& feed, double gap_ns, Res& res, bool keep) {
  static std::vector<std::uint32_t> lat; lat.resize(feed.size());
  std::this_thread::sleep_for(std::chrono::milliseconds(1200));  // let the RT budget refill
  auto q = std::make_unique<Q>();
  v4::Handler h;
  std::uint64_t sig = 0x1234;
  const std::uint64_t gap = std::uint64_t(gap_ns * TPN);
  pin(1);                                      // feeder inherits CPU 1; we move to CPU 2
  std::thread feeder([&] {
    std::uint64_t next = __rdtsc() + 1000000;
    for (const Msg& src : feed) {
      if (gap) { while (__rdtsc() < next) {} next += gap; }
      Msg m = src; m.ts = __rdtsc();
      while (!q->try_push(m)) {}
    }
  });
  pin(2);
  std::uint64_t t0 = __rdtsc();
  Msg m;
  for (std::size_t i = 0; i < feed.size(); ++i) {
    pop_one(*q, m);
    int s = h.on_msg(m);
    std::uint64_t done = tsc_end();
    lat[i] = std::uint32_t(std::min<std::uint64_t>(done - m.ts, 0xffffffffu));
    sig = mix(sig, std::uint64_t(s + 2));
  }
  std::uint64_t t1 = __rdtsc();
  feeder.join();
  if (sig != g_expect) std::printf("  %s: OUTPUT MISMATCH %llx\n", name, (unsigned long long)sig);
  if (!keep) return;
  res.ps.push_back(percentiles(lat, TPN));
  res.wall.push_back((t1 - t0) / TPN / feed.size());
}

void print(const char* name, double gap_ns, Res& res) {
  auto med = [&](auto f) { std::vector<double> v; for (auto& p : res.ps) v.push_back(f(p)); std::sort(v.begin(), v.end()); return v; };
  auto p50 = med([](const Pct& p) { return p.p50; }), p99 = med([](const Pct& p) { return p.p99; });
  auto p999 = med([](const Pct& p) { return p.p999; });
  auto w = res.wall; std::sort(w.begin(), w.end());
  std::size_t k = p50.size() / 2;
  std::printf("%-12s gap %5.0f  p50 %8.1f ns [%7.1f-%7.1f]  p99 %9.1f ns [%8.1f-%8.1f]  p99.9 %9.1f   wall %.1f ns/msg [%.1f-%.1f]\n",
              name, gap_ns, p50[k], p50.front(), p50.back(), p99[k], p99.front(), p99.back(), p999[k], w[k], w.front(), w.back());
}

int main(int argc, char** argv) {
  setvbuf(stdout, nullptr, _IONBF, 0);
  std::size_t n = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 1000000;
  double gap = argc > 2 ? std::atof(argv[2]) : 1000;
  int runs = argc > 3 ? std::atoi(argv[3]) : 3;
  std::string only = argc > 4 ? argv[4] : "";
  pin(2);
  TPN = tsc_per_ns();
  auto feed = make_feed(n);
  { v4::Handler h; std::uint64_t sig = 0x1234; for (auto& m : feed) sig = mix(sig, std::uint64_t(h.on_msg(m) + 2)); g_expect = sig; }
  std::printf("%zu msgs, one every %.0f ns (0 = flat out), %d runs, median [min-max]\n", n, gap, runs);
  auto want = [&](const char* v) { return only.empty() || only.find(v) != std::string::npos; };
  Res a, b, c, d;                              // runs interleaved, so slow spells hit every variant
  for (int r = 0; r <= runs; ++r) {
    if (want("mutex")) run_once<MutexQueue>("mutex+cv", feed, gap, a, r > 0);
    if (want("packed")) run_once<RingPacked<kRing>>("ring packed", feed, gap, b, r > 0);
    if (want("padded")) run_once<RingPadded<kRing>>("ring padded", feed, gap, c, r > 0);
    if (want("lab")) run_once<LabRing>("lab SpscRing", feed, gap, d, r > 0);
  }
  if (want("mutex")) print("mutex+cv", gap, a);
  if (want("packed")) print("ring packed", gap, b);
  if (want("padded")) print("ring padded", gap, c);
  if (want("lab")) print("lab SpscRing", gap, d);
}
static_assert(offsetof(RingPacked<kRing>, popped) + 8 <= 64, "packed counters share the first line");
static_assert(alignof(RingPacked<kRing>) == 64);
