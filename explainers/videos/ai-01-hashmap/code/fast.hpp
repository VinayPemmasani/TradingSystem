#pragma once
// RIGHT: the hot-path version. Symbols are interned to a small integer id once,
// at startup; the hot path carries the id and does one probe into a flat table.
#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>

namespace hp {
struct Quote { double bid, ask; std::uint64_t ts; };

class FlatQuotes {                       // open addressing, linear probing
 public:
  explicit FlatQuotes(std::uint32_t cap_pow2)   // sized once; never grows
      : slot_(std::make_unique<Slot[]>(cap_pow2)), mask_(cap_pow2 - 1) {}
  Quote* insert(std::uint32_t id) {      // startup only; id 0 is reserved
    std::uint32_t i = home(id);
    while (slot_[i].id != 0 && slot_[i].id != id) i = (i + 1) & mask_;
    slot_[i].id = id;
    return &slot_[i].q;
  }
  Quote* find(std::uint32_t id) {        // hot path
    for (std::uint32_t i = home(id);; i = (i + 1) & mask_) {
      if (slot_[i].id == id) return &slot_[i].q;
      if (slot_[i].id == 0) return nullptr;
    }
  }
  void on_tick(std::uint32_t id, double bid, double ask, std::uint64_t ts) {
    if (Quote* q = find(id)) *q = Quote{bid, ask, ts};
  }
 private:
  struct Slot { std::uint32_t id = 0; Quote q{}; };   // 32 bytes, 2 per line
  std::uint32_t home(std::uint32_t id) const {
    return (id * 0x9E3779B1u) & mask_;   // Fibonacci hash spreads ids
  }
  std::unique_ptr<Slot[]> slot_;
  std::uint32_t mask_;
};

// Startup: give every symbol an id once. Feeds often send one already
// (e.g. ITCH "stock locate"); then this map is only for reference data.
class SymbolIds {
 public:
  std::uint32_t intern(const std::string& s) {
    auto [it, fresh] = ids_.try_emplace(s, next_);
    if (fresh) ++next_;
    return it->second;
  }
 private:
  std::unordered_map<std::string, std::uint32_t> ids_;
  std::uint32_t next_ = 1;
};
}  // namespace hp
