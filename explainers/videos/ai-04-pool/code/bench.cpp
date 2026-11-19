// ai-04: make_unique per message vs a preallocated pool with a free list.
// Each message is a new order or a cancel of a random live order. The live count swings
// between 50k and 150k (bursts), so the heap grows and shrinks like a real session.
// Build: g++ -O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW bench.cpp -o bench
// Run (fresh process per variant): taskset -c 3 ./bench new ; taskset -c 3 ./bench pool
#include <cstring>
#include <random>
#include <sys/resource.h>
#include "harness.hpp"
#include "ai.hpp"
#include "fast.hpp"

static long faults() { rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_minflt + r.ru_majflt; }
struct Msg { bool is_new; NewMsg m; std::uint32_t pick; };

template <class Book> int run(const char* name, double ghz) {
  const std::size_t LO = 50'000, HI = 150'000, MAX = HI + 1024, T = 2'000'000, PERIOD = 400'000;
  Book book(MAX);
  std::mt19937_64 rng(5);
  std::uint64_t id = 0;
  auto mk = [&] { ++id; return NewMsg{id, id * 3, std::int64_t(10000 + rng() % 500), std::int64_t(1 + rng() % 900), std::uint32_t(rng() % 16), std::uint32_t(rng() & 1)}; };
  for (std::size_t k = 0; k < LO; ++k) book.on_new(mk());          // startup state
  // pre-build the message stream (harness memory, touched before timing)
  std::vector<Msg> msgs(T);
  std::size_t live = LO;
  for (std::size_t k = 0; k < T; ++k) {
    std::size_t phase = k % PERIOD;                                   // ramp up, then down
    std::size_t target = phase < PERIOD / 2 ? LO + (HI - LO) * phase / (PERIOD / 2) : HI - (HI - LO) * (phase - PERIOD / 2) / (PERIOD / 2);
    bool is_new = live < target ? (rng() % 4 != 0) : (rng() % 4 == 0);
    if (live == 0) is_new = true;
    msgs[k] = {is_new, mk(), std::uint32_t(rng() % (live ? live : 1))};
    live += is_new ? 1 : -1;
  }
  std::vector<std::uint64_t> lat(T);
  unsigned aux;
  auto stamp = [] { _mm_lfence(); return __rdtsc(); };
  std::vector<std::uint64_t> ov(100000);
  for (auto& x : ov) { auto t0 = stamp(); x = __rdtscp(&aux) - t0; }
  const std::uint64_t n0 = hz::g_news; const long f0 = faults();
  for (std::size_t k = 0; k < T; ++k) {
    const Msg& m = msgs[k];
    auto t0 = stamp();
    if (m.is_new) book.on_new(m.m); else book.on_cancel(m.pick);
    lat[k] = __rdtscp(&aux) - t0;
  }
  const long df = faults() - f0; const std::uint64_t dn = hz::g_news - n0;
  std::uint64_t chk = 0; for (std::size_t k = 0; k < book.size(); ++k) chk = chk * 31 + book.at(k).id;
  const double p50 = hz::pct(lat, .5) / ghz, p99 = hz::pct(lat, .99) / ghz, p999 = hz::pct(lat, .999) / ghz;
  const double p9999 = hz::pct(lat, .9999) / ghz, mx = double(lat.back()) / ghz, tov = hz::pct(ov, .5) / ghz;
  std::printf("%-5s p50 %6.1f  p99 %7.1f  p99.9 %8.1f  p99.99 %8.1f  max %9.1f ns  allocs/msg %.3f  page faults %ld  live %zu  chk %llx  (timer %.1f ns)\n",
              name, p50, p99, p999, p9999, mx, double(dn) / double(T), df, book.size(), (unsigned long long)chk, tov);
  return 0;
}

int main(int argc, char** argv) {
  const double ghz = hz::tsc_ghz();
  if (argc > 1 && !std::strcmp(argv[1], "pool")) return run<hp::Orders>("pool", ghz);
  return run<ai::Orders>("new", ghz);
}
