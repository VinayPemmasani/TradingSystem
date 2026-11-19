#pragma once
// Order book with O(1) add / cancel / execute, keyed by order id (ITCH order reference).
// Pool of order slots + open-addressing id->slot map + intrusive FIFO per price level
// + flat array of levels indexed by tick offset, with best-price tracking.
#include <cstdint>
#include <optional>
#include <vector>

enum class Side : std::uint8_t { Buy = 0, Sell = 1 };
inline constexpr std::uint32_t NIL = ~0u;

struct Order {               // one pool slot
  std::uint64_t id;
  std::uint32_t price, qty;  // Price(4), shares
  std::uint32_t prev, next;  // intrusive FIFO links: slot indexes
  Side side;
};

struct Level {
  std::uint32_t head = NIL, tail = NIL;  // oldest ... newest
  std::uint64_t qty = 0;
};

// id -> slot. Linear probing, backward-shift erase (no tombstones). Fixed size.
class IdMap {
 public:
  explicit IdMap(std::size_t max_live) {
    std::size_t c = 16;
    while (c < max_live * 2) c <<= 1;
    keys_.assign(c, kEmpty);
    vals_.assign(c, NIL);
    mask_ = c - 1;
  }
  std::uint32_t find(std::uint64_t k) const {
    for (std::size_t i = home(k);; i = (i + 1) & mask_) {
      if (keys_[i] == k) return vals_[i];
      if (keys_[i] == kEmpty) return NIL;
    }
  }
  bool insert(std::uint64_t k, std::uint32_t v) {
    std::size_t i = home(k);
    for (; keys_[i] != kEmpty; i = (i + 1) & mask_)
      if (keys_[i] == k) return false;
    keys_[i] = k;
    vals_[i] = v;
    return true;
  }
  void erase(std::uint64_t k) {
    std::size_t i = home(k);
    while (keys_[i] != k) {
      if (keys_[i] == kEmpty) return;
      i = (i + 1) & mask_;
    }
    for (std::size_t j = i;;) {
      j = (j + 1) & mask_;
      if (keys_[j] == kEmpty) break;
      const std::size_t h = home(keys_[j]);
      const bool stays = (i <= j) ? (i < h && h <= j) : (i < h || h <= j);
      if (stays) continue;
      keys_[i] = keys_[j];
      vals_[i] = vals_[j];
      i = j;
    }
    keys_[i] = kEmpty;
  }

 private:
  static constexpr std::uint64_t kEmpty = ~0ULL;
  std::size_t home(std::uint64_t k) const { return (k * 0x9E3779B97F4A7C15ULL >> 32) & mask_; }
  std::vector<std::uint64_t> keys_;
  std::vector<std::uint32_t> vals_;
  std::size_t mask_ = 0;
};

class Book {
 public:
  // Levels cover prices base, base+tick, ..., base+(nlevels-1)*tick.
  Book(std::uint32_t base, std::uint32_t tick, std::uint32_t nlevels, std::uint32_t max_orders)
      : base_{base}, tick_{tick}, n_{nlevels}, pool_(max_orders), ids_{max_orders} {
    for (std::uint32_t i = max_orders; i-- > 0;) free_.push_back(i);
    lv_[0].assign(nlevels, Level{});
    lv_[1].assign(nlevels, Level{});
    best_[0] = -1;                          // best bid: highest live index
    best_[1] = static_cast<std::int64_t>(nlevels);  // best ask: lowest live index
  }

  bool add(std::uint64_t id, Side s, std::uint32_t price, std::uint32_t qty) {
    const std::int64_t i = index(price);
    if (i < 0 || qty == 0 || free_.empty()) return false;
    const std::uint32_t slot = free_.back();
    if (!ids_.insert(id, slot)) return false;  // duplicate id
    free_.pop_back();
    Order& o = pool_[slot];
    o = Order{id, price, qty, NIL, NIL, s};
    Level& L = lv_[int(s)][i];
    o.prev = L.tail;  // append at the back of the FIFO
    if (L.tail != NIL) pool_[L.tail].next = slot;
    else               L.head = slot;
    L.tail = slot;
    L.qty += qty;
    if (s == Side::Buy ? i > best_[0] : i < best_[1]) best_[int(s)] = i;
    return true;
  }

  bool cancel(std::uint64_t id) {
    const std::uint32_t slot = ids_.find(id);
    if (slot == NIL) return false;
    remove(slot);
    return true;
  }

  // Execute `qty` shares of order `id` (ITCH E). Partial fills keep queue position.
  bool execute(std::uint64_t id, std::uint32_t qty) {
    const std::uint32_t slot = ids_.find(id);
    if (slot == NIL || qty == 0 || qty > pool_[slot].qty) return false;
    Order& o = pool_[slot];
    if (qty == o.qty) { remove(slot); return true; }
    o.qty -= qty;
    lv_[int(o.side)][index(o.price)].qty -= qty;
    return true;
  }

  std::optional<std::uint32_t> best_bid() const {
    if (best_[0] < 0) return std::nullopt;
    return price_of(best_[0]);
  }
  std::optional<std::uint32_t> best_ask() const {
    if (best_[1] >= std::int64_t(n_)) return std::nullopt;
    return price_of(best_[1]);
  }
  std::uint64_t qty_at(Side s, std::uint32_t price) const {
    const std::int64_t i = index(price);
    return i < 0 ? 0 : lv_[int(s)][i].qty;
  }
  // Id of the oldest order at the best level of side s (first to trade), or 0.
  std::uint64_t front(Side s) const {
    const std::int64_t b = best_[int(s)];
    if (b < 0 || b >= std::int64_t(n_)) return 0;
    return pool_[lv_[int(s)][b].head].id;
  }
  std::size_t live() const { return pool_.size() - free_.size(); }

 private:
  std::int64_t index(std::uint32_t price) const {
    if (price < base_ || (price - base_) % tick_ != 0) return -1;
    const std::uint32_t i = (price - base_) / tick_;
    return i < n_ ? std::int64_t(i) : -1;
  }
  std::uint32_t price_of(std::int64_t i) const { return base_ + std::uint32_t(i) * tick_; }

  void remove(std::uint32_t slot) {
    Order& o = pool_[slot];
    const int s = int(o.side);
    const std::int64_t i = index(o.price);
    Level& L = lv_[s][i];
    if (o.prev != NIL) pool_[o.prev].next = o.next;
    else               L.head = o.next;
    if (o.next != NIL) pool_[o.next].prev = o.prev;
    else               L.tail = o.prev;
    L.qty -= o.qty;
    if (L.head == NIL && i == best_[s]) {  // best level emptied: walk to the next live one
      if (s == 0) { while (best_[0] >= 0 && lv_[0][best_[0]].head == NIL) --best_[0]; }
      else { while (best_[1] < std::int64_t(n_) && lv_[1][best_[1]].head == NIL) ++best_[1]; }
    }
    ids_.erase(o.id);
    free_.push_back(slot);
  }

  std::uint32_t base_, tick_, n_;
  std::vector<Order> pool_;
  std::vector<std::uint32_t> free_;
  IdMap ids_;
  std::vector<Level> lv_[2];
  std::int64_t best_[2];
};
