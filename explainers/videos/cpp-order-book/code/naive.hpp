#pragma once
// The interview's first answer: a map of price -> list of orders per side,
// and a linear search over every order to cancel or execute by id.
#include <cstdint>
#include <functional>
#include <list>
#include <map>
#include <optional>
#include <unordered_map>

struct NOrder { std::uint64_t id; std::uint32_t qty; };

class NaiveBook {
 public:
  bool add(std::uint64_t id, bool buy, std::uint32_t price, std::uint32_t qty) {
    if (qty == 0 || find(id).first) return false;
    (buy ? bids_[price] : asks_[price]).push_back({id, qty});
    return true;
  }
  bool cancel(std::uint64_t id) {
    auto [m, it] = find(id);
    if (!m) return false;
    auto lvl = it.first;
    lvl->second.erase(it.second);
    if (lvl->second.empty()) m->erase(lvl);
    return true;
  }
  bool execute(std::uint64_t id, std::uint32_t qty) {
    auto [m, it] = find(id);
    if (!m || qty == 0 || qty > it.second->qty) return false;
    if (qty == it.second->qty) return cancel(id);
    it.second->qty -= qty;
    return true;
  }
  std::optional<std::uint32_t> best_bid() const {
    if (bids_.empty()) return std::nullopt;
    return bids_.rbegin()->first;
  }
  std::optional<std::uint32_t> best_ask() const {
    if (asks_.empty()) return std::nullopt;
    return asks_.begin()->first;
  }

 private:
  using Levels = std::map<std::uint32_t, std::list<NOrder>>;
  using Pos = std::pair<Levels::iterator, std::list<NOrder>::iterator>;
  std::pair<Levels*, Pos> find(std::uint64_t id) {  // O(number of live orders)
    for (Levels* m : {&bids_, &asks_})
      for (auto l = m->begin(); l != m->end(); ++l)
        for (auto o = l->second.begin(); o != l->second.end(); ++o)
          if (o->id == id) return {m, {l, o}};
    return {nullptr, {}};
  }
  Levels bids_, asks_;
};

// The usual second answer: same containers, plus a hash map id -> list iterator.
// Cancel becomes O(log L) for the level, but every add still allocates nodes.
class MapListBook {
 public:
  bool add(std::uint64_t id, bool buy, std::uint32_t price, std::uint32_t qty) {
    if (qty == 0 || where_.count(id)) return false;
    auto& lst = (buy ? bids_ : asks_)[price];
    lst.push_back({id, qty});
    where_.emplace(id, Where{buy, price, std::prev(lst.end())});
    return true;
  }
  bool cancel(std::uint64_t id) {
    auto w = where_.find(id);
    if (w == where_.end()) return false;
    Levels& m = w->second.buy ? bids_ : asks_;
    auto l = m.find(w->second.price);
    l->second.erase(w->second.it);
    if (l->second.empty()) m.erase(l);
    where_.erase(w);
    return true;
  }
  bool execute(std::uint64_t id, std::uint32_t qty) {
    auto w = where_.find(id);
    if (w == where_.end() || qty == 0 || qty > w->second.it->qty) return false;
    if (qty == w->second.it->qty) return cancel(id);
    w->second.it->qty -= qty;
    return true;
  }
  std::optional<std::uint32_t> best_bid() const {
    if (bids_.empty()) return std::nullopt;
    return bids_.rbegin()->first;
  }
  std::optional<std::uint32_t> best_ask() const {
    if (asks_.empty()) return std::nullopt;
    return asks_.begin()->first;
  }
  void reserve(std::size_t n) { where_.reserve(n); }

 private:
  using Levels = std::map<std::uint32_t, std::list<NOrder>>;
  struct Where { bool buy; std::uint32_t price; std::list<NOrder>::iterator it; };
  Levels bids_, asks_;
  std::unordered_map<std::uint64_t, Where> where_;
};
