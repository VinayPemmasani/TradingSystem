#pragma once
// Shared op stream: level updates (add / modify / cancel) clustered near the touch.
#include <cstdint>
#include <map>
#include <random>
#include <vector>
struct Op { bool bid; std::int64_t ticks; double px; std::int64_t qty; };
struct Mix { std::size_t add = 0, mod = 0, del = 0, live_bid = 0, live_ask = 0; };
inline std::vector<Op> make_ops(std::size_t n, std::int64_t base, std::int32_t win, std::uint64_t seed, Mix& mix) {
  std::mt19937_64 rng(seed);
  std::geometric_distribution<int> dist(0.12);              // distance from mid, mean ~7 ticks
  std::map<std::int64_t, std::int64_t> live[2];
  std::int64_t mid = base + win / 2;
  std::vector<Op> ops; ops.reserve(n);
  for (std::size_t k = 0; k < n; ++k) {
    if (k % 64 == 0) { mid += (rng() & 1) ? 1 : -1; if (mid < base + win / 4) mid += 2; if (mid > base + 3 * win / 4) mid -= 2; }
    bool bid = rng() & 1;
    int d = std::min(dist(rng), win / 4 - 2);
    std::int64_t t = bid ? mid - 1 - d : mid + 1 + d;
    auto& m = live[bid];
    std::int64_t q;
    auto it = m.find(t);
    if (it == m.end()) { q = 100 * std::int64_t(1 + rng() % 20); m[t] = q; ++mix.add; }
    else if (rng() & 1) { q = 100 * std::int64_t(1 + rng() % 20); it->second = q; ++mix.mod; }
    else { q = 0; m.erase(it); ++mix.del; }
    ops.push_back({bid, t, double(t) * 0.01, q});
  }
  mix.live_bid = live[1].size(); mix.live_ask = live[0].size();
  return ops;
}
