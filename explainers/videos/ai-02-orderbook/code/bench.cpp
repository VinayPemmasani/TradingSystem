// ai-02: std::map<double, Level> per side vs flat tick-indexed arrays with best cursors.
// Build: g++ -O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW bench.cpp -o bench ; Run: taskset -c 3 ./bench
#include "harness.hpp"
#include "ai.hpp"
#include "fast.hpp"
#include "ops.hpp"

static std::int64_t sink = 0;
__attribute__((noinline)) void ai_msg(ai::Book& b, const Op& o) {
  b.set(o.bid, o.px, o.qty);
  auto x = b.best_bid(), y = b.best_ask();
  sink += (x ? x->second : 0) + (y ? y->second : 0);
}
__attribute__((noinline)) void hp_msg(hp::FlatBook& b, const Op& o) {
  b.set(o.bid, o.ticks, o.qty);
  auto x = b.best_bid(), y = b.best_ask();
  sink += (x ? x->second : 0) + (y ? y->second : 0);
}
__attribute__((noinline)) std::int64_t ai_top(const ai::Book& b) { auto x = b.best_bid(), y = b.best_ask(); return (x ? x->second : 0) + (y ? y->second : 0); }
__attribute__((noinline)) std::int64_t hp_top(const hp::FlatBook& b) { auto x = b.best_bid(), y = b.best_ask(); return (x ? x->second : 0) + (y ? y->second : 0); }

int main() {
  const std::int64_t base = 1'000'000; const std::int32_t win = 4096;
  const std::size_t W = 200'000, T = 1'000'000, RUNS = 5;
  const double ghz = hz::tsc_ghz();
  Mix mix; auto all = make_ops(W + T * RUNS + T, base, win, 11, mix);
  ai::Book a; hp::FlatBook b(base, win);
  for (std::size_t k = 0; k < W; ++k) { ai_msg(a, all[k]); hp_msg(b, all[k]); }   // warm: build depth
  std::size_t pos = W;
  std::vector<double> ta, tb; std::uint64_t na = 0, nb = 0;
  for (std::size_t r = 0; r < RUNS; ++r, pos += T) {        // same ops into both, books stay identical
    std::uint64_t n0 = hz::g_news;
    double x = hz::batch_median(T, 1000, ghz, [&](std::size_t k) { ai_msg(a, all[pos + k]); });
    na += hz::g_news - n0; ta.push_back(x);
    n0 = hz::g_news;
    x = hz::batch_median(T, 1000, ghz, [&](std::size_t k) { hp_msg(b, all[pos + k]); });
    nb += hz::g_news - n0; tb.push_back(x);
  }
  // one message at a time (lfence/rdtscp), then top-of-book reads alone
  std::vector<std::uint64_t> la(T), lb(T), l0(T); unsigned aux;
  auto stamp = [] { _mm_lfence(); return __rdtsc(); };
  for (std::size_t k = 0; k < T; ++k) { auto t0 = stamp(); l0[k] = __rdtscp(&aux) - t0; }
  for (std::size_t k = 0; k < T; ++k) { auto t0 = stamp(); ai_msg(a, all[pos + k]); la[k] = __rdtscp(&aux) - t0; }   // same aged heap,
  for (std::size_t k = 0; k < T; ++k) { auto t0 = stamp(); hp_msg(b, all[pos + k]); lb[k] = __rdtscp(&aux) - t0; }   // no copies
  std::int64_t s = 0; std::uint64_t t0 = __rdtsc();
  for (std::size_t k = 0; k < T; ++k) { s += ai_top(a); asm volatile("" ::: "memory"); }
  double rta = double(__rdtsc() - t0) / ghz / double(T); t0 = __rdtsc();
  for (std::size_t k = 0; k < T; ++k) { s += hp_top(b); asm volatile("" ::: "memory"); }
  double rtb = double(__rdtsc() - t0) / ghz / double(T);
  auto x = a.best_bid(); auto y = b.best_bid();
  bool same = x && y && x->first == double(y->first) * 0.01 && x->second == y->second;
  auto med = [](std::vector<double> v) { std::sort(v.begin(), v.end()); return v[v.size() / 2]; };
  auto mn = [](const std::vector<double>& v) { return *std::min_element(v.begin(), v.end()); };
  auto mx = [](const std::vector<double>& v) { return *std::max_element(v.begin(), v.end()); };
  double ov = hz::pct(l0, .5) / ghz;
  std::printf("ops: add %.0f%% modify %.0f%% cancel %.0f%%; each op = set level + read best bid & ask; same=%s sink=%lld\n",
              100.0 * mix.add / all.size(), 100.0 * mix.mod / all.size(), 100.0 * mix.del / all.size(), same ? "yes" : "NO", (long long)(sink + s) % 7);
  std::printf("timer overhead p50 %.1f ns\n", ov);
  std::printf("map   b2b ns/msg %6.1f (min %.1f max %.1f)  p50 %6.1f p99 %6.1f p99.9 %7.1f ns  allocs/msg %.3f  top-read %.2f ns\n",
              med(ta), mn(ta), mx(ta), hz::pct(la, .5) / ghz, hz::pct(la, .99) / ghz, hz::pct(la, .999) / ghz, double(na) / double(T * RUNS), rta);
  std::printf("flat  b2b ns/msg %6.1f (min %.1f max %.1f)  p50 %6.1f p99 %6.1f p99.9 %7.1f ns  allocs/msg %.3f  top-read %.2f ns\n",
              med(tb), mn(tb), mx(tb), hz::pct(lb, .5) / ghz, hz::pct(lb, .99) / ghz, hz::pct(lb, .999) / ghz, double(nb) / double(T * RUNS), rtb);
  std::printf("live levels at end: bid %zu ask %zu\n", mix.live_bid, mix.live_ask);
  std::printf("memory: flat arrays %zu KB total; map node %zu B each\n", std::size_t(2 * win * 8 / 1024), sizeof(std::_Rb_tree_node<std::pair<const double, ai::Level>>));
}
