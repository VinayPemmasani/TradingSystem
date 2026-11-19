// Isolated pipelining check: the 32-trade VWAP loop with data hot in L1,
// one accumulator versus four; and the dependent divide versus cross-multiply.
#include <cstdio>
#include <pthread.h>
#include "common.hpp"
struct T { std::int64_t price; std::uint32_t qty; };
__attribute__((noinline)) double one_chain(const T* t) {
  double pv = 0;
  for (int i = 0; i < 32; ++i) pv += double(t[i].price) * t[i].qty;
  return pv;
}
__attribute__((noinline)) double four_chains(const T* t) {
  double p0 = 0, p1 = 0, p2 = 0, p3 = 0;
  for (int i = 0; i < 32; i += 4) {
    p0 += double(t[i].price) * t[i].qty;     p1 += double(t[i + 1].price) * t[i + 1].qty;
    p2 += double(t[i + 2].price) * t[i + 2].qty; p3 += double(t[i + 3].price) * t[i + 3].qty;
  }
  return (p0 + p1) + (p2 + p3);
}
// signal from the sums: two dependent divides
__attribute__((noinline)) int sig_div(double pv, std::int64_t vol, std::int64_t bid, std::int64_t ask) {
  double vwap = pv / double(vol);
  double mid = double(bid + ask) / 2.0;
  double edge = (mid - vwap) / double(ask - bid);
  return (edge > 0.25) - (edge < -0.25);
}
__attribute__((noinline)) int sig_mul(std::int64_t pv, std::int64_t vol, std::int64_t bid, std::int64_t ask) {
  std::int64_t lhs = 2 * ((bid + ask) * vol - 2 * pv), rhs = (ask - bid) * vol;
  return (lhs > rhs) - (lhs < -rhs);
}
int main() {
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(2, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s);
  double tpn = tsc_per_ns();
  T t[32]; Rng r{7};
  for (auto& x : t) { x.price = 1000000 + std::int64_t(r.below(1000)); x.qty = 1 + std::uint32_t(r.below(1000)); }
  const int N = 2000000;
  for (int rep = 0; rep < 3; ++rep) {
    double acc = 0;
    std::uint64_t a = __rdtsc();
    for (int i = 0; i < N; ++i) { acc += one_chain(t); t[i & 31].qty ^= 1; }
    std::uint64_t b = __rdtsc();
    for (int i = 0; i < N; ++i) { acc += four_chains(t); t[i & 31].qty ^= 1; }
    std::uint64_t c = __rdtsc();
    // dependent: each call's input depends on the previous result (latency, not throughput)
    std::int64_t vol = 16000, bid = 999900, ask = 1000100; double pv = 16000.0 * 1000000; int k = 0;
    for (int i = 0; i < N; ++i) { k = sig_div(pv + k, vol, bid, ask + (k & 1)); }
    std::uint64_t d = __rdtsc();
    std::int64_t ipv = 16000LL * 1000000; int j = 0;
    for (int i = 0; i < N; ++i) { j = sig_mul(ipv + j, vol, bid, ask + (j & 1)); }
    std::uint64_t e = __rdtsc();
    std::printf("loop: 1 chain %.1f ns (%.0f cyc)  4 chains %.1f ns (%.0f cyc)   signal: divide %.1f ns (%.0f cyc)  cross-mul %.1f ns (%.0f cyc)  [%g %d %d]\n",
      (b - a) / tpn / N, double(b - a) / N, (c - b) / tpn / N, double(c - b) / N,
      (d - c) / tpn / N, double(d - c) / N, (e - d) / tpn / N, double(e - d) / N, acc > 0 ? 1.0 : 0.0, k, j);
  }
}
