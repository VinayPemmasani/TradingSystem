// ai-01: unordered_map<string,Quote> per tick vs flat open-addressing table keyed by interned id.
// Build: g++ -O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW bench.cpp -o bench
// Run:   taskset -c 3 ./bench <instruments>
#include <cstring>
#include <random>
#include <string>
#include "harness.hpp"
#include "ai.hpp"
#include "fast.hpp"

struct AiTick { std::string sym; double bid, ask; std::uint64_t ts; };
struct HpTick { std::uint32_t id; double bid, ask; std::uint64_t ts; };

__attribute__((noinline)) void ai_tick(ai::QuoteCache& c, const AiTick& t) { c.on_tick(t.sym, t.bid, t.ask, t.ts); }
__attribute__((noinline)) void hp_tick(hp::FlatQuotes& c, const HpTick& t) { c.on_tick(t.id, t.bid, t.ask, t.ts); }

static std::string symbol(std::size_t i) { char b[32]; std::snprintf(b, sizeof b, "S%06zu", i); return b; }  // 7 chars: fits SSO

int main(int argc, char** argv) {
  const std::size_t N = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 200000;
  const std::size_t T = 1'000'000, RUNS = 5;
  const double ghz = hz::tsc_ghz();
  std::vector<std::string> names(N);
  for (std::size_t i = 0; i < N; ++i) names[i] = symbol(i);

  // ---- startup: build both
  ai::QuoteCache left;
  std::uint64_t n0 = hz::g_news, b0 = hz::g_bytes;
  for (auto& s : names) left.on_tick(s, 0, 0, 0);
  const double ai_allocs = double(hz::g_news - n0) / double(N), ai_bytes = double(hz::g_bytes - b0) / double(N);

  hp::SymbolIds ids; std::uint32_t cap = 1; while (cap < N + N / 4) cap <<= 1;  // load <= 0.8
  n0 = hz::g_news; b0 = hz::g_bytes;
  hp::FlatQuotes right(cap);
  const double hp_bytes = double(hz::g_bytes - b0) / double(N);
  std::vector<std::uint32_t> id_of(N);
  for (std::size_t i = 0; i < N; ++i) { id_of[i] = ids.intern(names[i]); right.insert(id_of[i]); }

  // ---- tick stream: uniform random instruments (same sequence for both)
  std::mt19937_64 rng(7);
  std::vector<AiTick> at(T); std::vector<HpTick> ht(T);
  for (std::size_t k = 0; k < T; ++k) {
    std::size_t i = rng() % N; double px = 100.0 + double(k % 100) * 0.01;
    at[k] = {names[i], px, px + 0.01, k}; ht[k] = {id_of[i], px, px + 0.01, k};
  }
  // ---- throughput: ns per tick, RUNS runs each, alternating
  std::vector<double> tai, thp; std::uint64_t hot_news = 0;
  for (std::size_t r = 0; r < RUNS; ++r) {
    std::uint64_t a0 = hz::g_news, t0 = __rdtsc();
    for (auto& t : at) ai_tick(left, t);
    std::uint64_t t1 = __rdtsc(); hot_news += hz::g_news - a0; tai.push_back(double(t1 - t0) / ghz / double(T));
    a0 = hz::g_news; t0 = __rdtsc();
    for (auto& t : ht) hp_tick(right, t);
    t1 = __rdtsc(); hot_news += hz::g_news - a0; thp.push_back(double(t1 - t0) / ghz / double(T));
  }
  // ---- per-tick latency: lfence+rdtsc / rdtscp around each call (includes timer overhead, reported)
  std::vector<std::uint64_t> la(T), lh(T), l0(T); unsigned aux;
  auto stamp = [&] { _mm_lfence(); return __rdtsc(); };
  for (std::size_t k = 0; k < T; ++k) { std::uint64_t t0 = stamp(); l0[k] = __rdtscp(&aux) - t0; }
  for (std::size_t k = 0; k < T; ++k) { std::uint64_t t0 = stamp(); ai_tick(left, at[k]); la[k] = __rdtscp(&aux) - t0; }
  for (std::size_t k = 0; k < T; ++k) { std::uint64_t t0 = stamp(); hp_tick(right, ht[k]); lh[k] = __rdtscp(&aux) - t0; }
  // ---- same results?
  bool same = true;
  for (std::size_t i = 0; i < N; ++i) {
    const ai::Quote* a = left.find(names[i]); const hp::Quote* b = right.find(id_of[i]);
    same &= a && b && a->bid == b->bid && a->ask == b->ask && a->ts == b->ts;
  }
  auto mm = [](std::vector<double> v) { std::sort(v.begin(), v.end()); return std::make_tuple(v[v.size() / 2], v.front(), v.back()); };
  auto [am, al, ah] = mm(tai); auto [hm, hl, hh] = mm(thp);
  std::printf("timer overhead p50 %.1f ns\n", hz::pct(l0, .5) / ghz);
  std::printf("N=%zu ticks=%zu runs=%zu  same=%s  hot-path allocs=%llu\n", N, T, RUNS, same ? "yes" : "NO", (unsigned long long)hot_news);
  std::printf("map   ns/tick median %6.1f (min %.1f max %.1f)  p50 %6.1f p99 %6.1f ns  heap %5.1f B/entry, %.1f allocs/entry\n",
              am, al, ah, hz::pct(la, .5) / ghz, hz::pct(la, .99) / ghz, ai_bytes, ai_allocs);
  std::printf("flat  ns/tick median %6.1f (min %.1f max %.1f)  p50 %6.1f p99 %6.1f ns  heap %5.1f B/entry (cap %u)\n",
              hm, hl, hh, hz::pct(lh, .5) / ghz, hz::pct(lh, .99) / ghz, hp_bytes, cap);
}
