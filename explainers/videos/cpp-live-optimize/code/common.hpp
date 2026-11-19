// Shared pieces for the cpp-live-optimize video: the feed message, a
// deterministic synthetic feed, rdtsc timing, percentiles, an allocation counter.
#pragma once
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <new>
#include <vector>
#include <x86intrin.h>

// One market-data message, ITCH-flavoured: a stock locate code (ITCH carries
// one in every message) plus the 8-byte space-padded symbol. Price is an
// integer in 1/10000 dollars, as in ITCH Price(4).
struct Msg {
  char type;          // 'Q' quote update, 'T' trade
  char side;          // 'B' bid / 'S' ask  (anything else is invalid)
  std::uint16_t locate;
  std::uint32_t qty;
  std::int64_t price;
  char stock[8];
  std::uint64_t ts;   // stamped by the feed thread in the two-thread runs
};
static_assert(sizeof(Msg) == 32);

constexpr int kSymbols = 500;
constexpr int kMaxLocate = 512;

struct Rng {
  std::uint64_t s;
  std::uint64_t next() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
  std::uint64_t below(std::uint64_t n) { return next() % n; }
};

inline std::vector<Msg> make_feed(std::size_t n, std::uint64_t seed = 0x9E3779B97F4A7C15ull) {
  Rng r{seed};
  struct Sym { char name[8]; std::int64_t mid; };
  std::vector<Sym> syms(kSymbols + 1);
  for (int i = 1; i <= kSymbols; ++i) {
    std::memset(syms[i].name, ' ', 8);
    for (bool dup = true; dup;) {                         // unique 2..4 letter names
      std::memset(syms[i].name, ' ', 8);
      int len = 2 + int(r.below(3));
      for (int k = 0; k < len; ++k) syms[i].name[k] = char('A' + r.below(26));
      dup = false;
      for (int j = 1; j < i; ++j) dup |= std::memcmp(syms[j].name, syms[i].name, 8) == 0;
    }
    syms[i].mid = (20 + std::int64_t(r.below(480))) * 10000;   // $20..$500
  }
  std::vector<Msg> v(n);
  for (auto& m : v) {
    int loc = 1 + int(r.below(kSymbols));
    Sym& s = syms[loc];
    s.mid += (std::int64_t(r.below(5)) - 2) * 100;      // random walk in cents
    if (s.mid < 10000) s.mid = 10000;
    m = Msg{};
    m.locate = std::uint16_t(loc);
    std::memcpy(m.stock, s.name, 8);
    m.type = r.below(10) < 7 ? 'Q' : 'T';
    m.side = r.below(2) ? 'B' : 'S';
    m.qty = 1 + std::uint32_t(r.below(1000));
    std::int64_t off = (1 + std::int64_t(r.below(3))) * 100;
    if (m.type == 'Q') m.price = m.side == 'B' ? s.mid - off : s.mid + off;
    else m.price = s.mid + (std::int64_t(r.below(5)) - 2) * 100;
    std::uint64_t bad = r.below(1000);                   // ~1% invalid
    if (bad < 4) m.qty = 0;
    else if (bad < 7) m.price = 0;
    else if (bad < 10) m.side = 'X';
  }
  return v;
}

// ---- timing
inline std::uint64_t tsc_begin() { _mm_lfence(); std::uint64_t t = __rdtsc(); _mm_lfence(); return t; }
inline std::uint64_t tsc_end() { unsigned a; std::uint64_t t = __rdtscp(&a); _mm_lfence(); return t; }

inline double tsc_per_ns() {
  using clk = std::chrono::steady_clock;
  auto c0 = clk::now(); std::uint64_t t0 = __rdtsc();
  while (clk::now() - c0 < std::chrono::milliseconds(200)) {}
  auto c1 = clk::now(); std::uint64_t t1 = __rdtsc();
  return double(t1 - t0) / std::chrono::duration<double, std::nano>(c1 - c0).count();
}

struct Pct { double p50, p99, p999, max; };
inline Pct percentiles(std::vector<std::uint32_t>& c, double tpn) {
  std::sort(c.begin(), c.end());
  auto at = [&](double q) { return c[std::size_t(q * double(c.size() - 1))] / tpn; };
  return {at(0.50), at(0.99), at(0.999), c.back() / tpn};
}

// ---- allocation counter (counts every operator new in the process)
inline std::atomic<std::uint64_t> g_allocs{0};
inline bool g_count_allocs = false;

inline std::uint64_t mix(std::uint64_t h, std::uint64_t v) { return (h ^ v) * 0x100000001B3ull + (h >> 29); }
// order-independent digest of one symbol's final state
inline std::uint64_t sym_digest(std::int64_t bid, std::int64_t ask, std::uint64_t updates) {
  return mix(mix(mix(0xcbf29ce484222325ull, std::uint64_t(bid)), std::uint64_t(ask)), updates);
}
