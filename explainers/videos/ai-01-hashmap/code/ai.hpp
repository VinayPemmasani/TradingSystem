#pragma once
// LEFT: the general-purpose version. Correct, idiomatic, and what you get
// when the prompt says "cache the latest quote per symbol".
#include <cstdint>
#include <string>
#include <unordered_map>

namespace ai {
struct Quote { double bid, ask; std::uint64_t ts; };

class QuoteCache {
 public:
  void on_tick(const std::string& sym, double bid,
               double ask, std::uint64_t ts) {
    quotes_[sym] = Quote{bid, ask, ts};   // hash string, walk bucket
  }
  const Quote* find(const std::string& sym) const {
    auto it = quotes_.find(sym);
    return it == quotes_.end() ? nullptr : &it->second;
  }
 private:
  std::unordered_map<std::string, Quote> quotes_;
};
}  // namespace ai
