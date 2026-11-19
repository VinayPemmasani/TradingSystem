#include <cstdio>
#include <random>

#include "naive.hpp"
#include "vwap.hpp"

static int fails = 0;
#define CHECK(x) do { if (!(x)) { std::printf("FAIL line %d: %s\n", __LINE__, #x); ++fails; } } while (0)

int main() {
  constexpr std::int64_t S = 1'000'000'000;  // 1 s in ns
  {  // empty, single trade, rounding
    SlidingVwap v(5 * S, 16);
    CHECK(!v.vwap() && !v.high() && !v.low());
    CHECK(v.on_trade({10 * S, 1'000'000, 100}));
    CHECK(v.vwap() == 1'000'000u && v.high() == 1'000'000u && v.low() == 1'000'000u);
    CHECK(v.on_trade({10 * S, 1'000'001, 100}));  // same timestamp is fine
    CHECK(v.vwap() == 1'000'001u);                // 1000000.5 rounds half up
    CHECK(v.on_trade({10 * S, 1'000'003, 200}));  // (100*0 + 100*1 + 200*3)/400 = 1.75 -> 2
    CHECK(v.vwap() == 1'000'002u);
  }
  {  // window boundary: t stays while t > now - window
    SlidingVwap v(5 * S, 16);
    v.on_trade({0, 2'000'000, 10});
    v.on_trade({1, 1'000'000, 10});
    v.on_trade({5 * S - 1, 1'000'000, 10});
    CHECK(v.count() == 3);
    v.on_trade({5 * S, 1'000'000, 10});  // trade at 0 is exactly window old: out
    CHECK(v.count() == 3 && v.high() == 1'000'000u && v.vwap() == 1'000'000u);
    v.evict(5 * S + 1);                   // trade at 1 out
    CHECK(v.count() == 2);
    v.evict(100 * S);
    CHECK(v.count() == 0 && !v.vwap() && !v.high());
  }
  {  // time going backwards is rejected
    SlidingVwap v(S, 16);
    CHECK(v.on_trade({100, 1, 1}));
    CHECK(!v.on_trade({99, 5, 5}) && v.count() == 1 && v.vwap() == 1u);
  }
  {  // full ring rejects instead of silently dropping a live trade
    SlidingVwap v(S, 4);
    for (int i = 0; i < 4; ++i) CHECK(v.on_trade({i, 100, 1}));
    CHECK(!v.on_trade({4, 100, 1}));
    CHECK(v.on_trade({S, 100, 1}));  // trade 0 expired: room again
  }
  {  // overflow: max price x max qty, many times
    SlidingVwap v(S, 1024);
    std::uint64_t naive64 = 0;
    for (int i = 0; i < 1000; ++i) {
      v.on_trade({i, UINT32_MAX, UINT32_MAX});
      naive64 += std::uint64_t(UINT32_MAX) * UINT32_MAX;  // one fits; the second wraps
    }
    CHECK(v.vwap() == std::uint64_t(UINT32_MAX));
    CHECK(v.volume() == 1000ULL * UINT32_MAX);
    std::printf("uint64 sum after 1000 max trades wrapped to %llu\n", (unsigned long long)naive64);
  }
  {  // monotonic deques: equal prices, expiry of the max
    SlidingVwap v(10, 16);
    v.on_trade({0, 50, 1});
    v.on_trade({1, 70, 1});
    v.on_trade({2, 70, 1});
    v.on_trade({3, 60, 1});
    CHECK(v.high() == 70u && v.low() == 50u);
    v.evict(10);  // t=0 gone
    CHECK(v.high() == 70u && v.low() == 60u);
    v.evict(12);  // both 70s gone
    CHECK(v.high() == 60u && v.low() == 60u);
  }
  {  // randomized against the naive recompute
    std::mt19937_64 rng(9);
    const std::int64_t W = 1'000'000;  // 1 ms window
    SlidingVwap v(W, 1 << 12);
    NaiveVwap n(W);
    std::int64_t t = 0;
    for (int i = 0; i < 300'000; ++i) {
      t += std::int64_t(rng() % 1000);  // 0..999 ns gaps, bursts of equal timestamps
      if (rng() % 100 == 0) t += W;     // occasional quiet spell empties the window
      const Trade tr{t, std::uint32_t(rng() % 3 ? 1'000'000 + rng() % 500 : rng()),
                     std::uint32_t(rng() % 4 ? 1 + rng() % 1000 : rng())};
      CHECK(v.on_trade(tr));
      n.on_trade(tr);
      CHECK(v.count() == n.count());
      CHECK(v.vwap() == n.vwap());
      CHECK(v.high() == n.high() && v.low() == n.low());
      if (fails > 10) return 1;
    }
  }
  std::printf(fails ? "%d FAILED\n" : "all tests passed\n", fails);
  return fails != 0;
}
