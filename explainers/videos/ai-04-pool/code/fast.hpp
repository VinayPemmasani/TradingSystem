#pragma once
// RIGHT: the hot-path version. A fixed-size pool, allocated and touched at
// startup; a free list of slot pointers. acquire/release are two pointer moves.
#include <cstddef>
#include <cstring>
#include <memory>
#include <vector>
#include "order.hpp"

namespace hp {
template <class T>
class Pool {
 public:
  explicit Pool(std::size_t n) : slots_(std::make_unique<Slot[]>(n)) {
    std::memset(static_cast<void*>(slots_.get()), 0, n * sizeof(Slot));   // fault pages in now
    for (std::size_t i = 0; i < n; ++i) slots_[i].next = i + 1 < n ? &slots_[i + 1] : nullptr;
    free_ = &slots_[0];
  }
  T* acquire() noexcept {
    Slot* s = free_;
    if (!s) return nullptr;                      // full: caller rejects
    free_ = s->next;
    return &s->obj;
  }
  void release(T* p) noexcept {
    Slot* s = reinterpret_cast<Slot*>(p);
    s->next = free_; free_ = s;
  }
 private:
  union Slot { T obj; Slot* next; };
  std::unique_ptr<Slot[]> slots_;
  Slot* free_;
};

class Orders {
 public:
  explicit Orders(std::size_t max_live) : pool_(max_live) {
    live_.resize(max_live); live_.clear();       // touch the index pages at startup too
  }
  bool on_new(const NewMsg& m) {
    Order* o = pool_.acquire();
    if (!o) return false;                        // full: reject, never malloc
    *o = Order{m.id, m.ts, m.px, m.qty, m.acct, m.side, {}, {}};
    live_.push_back(o);
    return true;
  }
  void on_cancel(std::size_t k) {
    pool_.release(live_[k]);
    live_[k] = live_.back();
    live_.pop_back();
  }
  std::size_t size() const { return live_.size(); }
  const Order& at(std::size_t k) const { return *live_[k]; }
 private:
  Pool<Order> pool_;
  std::vector<Order*> live_;
};
}  // namespace hp
