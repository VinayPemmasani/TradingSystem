#include <cstdio>
#include <cstdlib>
#include <map>
#include <random>
#include <vector>

#include "book.hpp"
#include "naive.hpp"

static int fails = 0;
#define CHECK(x) do { if (!(x)) { std::printf("FAIL line %d: %s\n", __LINE__, #x); ++fails; } } while (0)

int main() {
  constexpr std::uint32_t T = 100;  // one cent in Price(4)
  {  // empty book, rejects
    Book b(1'000'000, T, 1000, 4);
    CHECK(!b.best_bid() && !b.best_ask());
    CHECK(!b.add(1, Side::Buy, 999'900, 10));       // below the band
    CHECK(!b.add(1, Side::Buy, 1'000'050, 10));     // off the tick grid
    CHECK(!b.add(1, Side::Buy, 1'000'000 + 1000 * T, 10));  // just past the top
    CHECK(b.add(1, Side::Buy, 1'000'000 + 999 * T, 10));    // top level ok
    CHECK(b.add(9, Side::Buy, 1'000'000, 10));              // bottom level ok
    CHECK(!b.add(2, Side::Buy, 1'000'100, 0));      // zero qty
    CHECK(!b.add(1, Side::Sell, 1'000'100, 5));     // duplicate id
    CHECK(!b.cancel(77));                           // unknown id
    CHECK(b.cancel(1) && !b.cancel(1));             // cancel twice
    CHECK(b.best_bid() == 1'000'000u);
    CHECK(b.cancel(9) && !b.best_bid());
  }
  {  // FIFO: cancel in the middle, head, tail
    Book b(1'000'000, T, 1000, 8);
    b.add(1, Side::Sell, 1'010'000, 100);
    b.add(2, Side::Sell, 1'010'000, 200);
    b.add(3, Side::Sell, 1'010'000, 300);
    CHECK(b.front(Side::Sell) == 1 && b.qty_at(Side::Sell, 1'010'000) == 600);
    CHECK(b.cancel(2));
    CHECK(b.front(Side::Sell) == 1 && b.qty_at(Side::Sell, 1'010'000) == 400);
    CHECK(b.cancel(1));
    CHECK(b.front(Side::Sell) == 3);
    b.add(4, Side::Sell, 1'010'000, 50);
    CHECK(b.cancel(4) && b.front(Side::Sell) == 3);  // tail removal
    CHECK(b.cancel(3) && !b.best_ask() && b.qty_at(Side::Sell, 1'010'000) == 0);
  }
  {  // execute: partial keeps priority, full removes, over-execution rejected
    Book b(1'000'000, T, 1000, 8);
    b.add(1, Side::Buy, 1'005'000, 100);
    b.add(2, Side::Buy, 1'005'000, 100);
    CHECK(b.execute(1, 40) && b.front(Side::Buy) == 1);
    CHECK(b.qty_at(Side::Buy, 1'005'000) == 160);
    CHECK(!b.execute(1, 61) && !b.execute(1, 0) && !b.execute(5, 1));
    CHECK(b.execute(1, 60) && b.front(Side::Buy) == 2);
  }
  {  // best price walks to the next live level when the best empties
    Book b(1'000'000, T, 1000, 8);
    b.add(1, Side::Buy, 1'000'500, 1);
    b.add(2, Side::Buy, 1'003'000, 1);
    b.add(3, Side::Sell, 1'004'000, 1);
    b.add(4, Side::Sell, 1'009'900, 1);
    CHECK(b.best_bid() == 1'003'000u && b.best_ask() == 1'004'000u);
    b.cancel(2); b.cancel(3);
    CHECK(b.best_bid() == 1'000'500u && b.best_ask() == 1'009'900u);
    b.cancel(1); b.cancel(4);
    CHECK(!b.best_bid() && !b.best_ask());
  }
  {  // pool full, slot and id reuse
    Book b(1'000'000, T, 10, 2);
    CHECK(b.add(1, Side::Buy, 1'000'000, 1) && b.add(2, Side::Buy, 1'000'000, 1));
    CHECK(!b.add(3, Side::Buy, 1'000'000, 1));
    CHECK(b.cancel(1) && b.add(3, Side::Buy, 1'000'100, 1));  // freed slot reused
    CHECK(!b.add(4, Side::Sell, 1'000'200, 1));
    CHECK(b.cancel(2) && b.add(1, Side::Sell, 1'000'200, 1));  // id 1 reusable once gone
    CHECK(b.live() == 2 && b.best_bid() == 1'000'100u && b.best_ask() == 1'000'200u);
  }
  {  // randomized: good book vs naive and map+list books, plus an aggregate model
    std::mt19937_64 rng(42);
    Book b(1'000'000, T, 400, 200'000);
    NaiveBook nb;
    MapListBook mb;
    std::map<std::uint32_t, std::uint64_t> agg[2];
    std::vector<std::uint64_t> live;
    std::map<std::uint64_t, std::pair<int, std::uint32_t>> info;  // id -> side, price
    std::map<std::uint64_t, std::uint32_t> qty;
    std::uint64_t next = 1;
    for (int step = 0; step < 200'000; ++step) {
      const int op = int(rng() % 10) - 1;  // 40% adds keeps the live set bounded
      if (op < 3 || live.empty()) {
        const bool buy = rng() & 1;
        const std::uint32_t px = 1'000'000 + std::uint32_t(rng() % 400) * T;
        const std::uint32_t q = 1 + std::uint32_t(rng() % 500);
        const std::uint64_t id = (rng() % 50 == 0 && !live.empty()) ? live[rng() % live.size()] : next++;
        const bool ok = b.add(id, buy ? Side::Buy : Side::Sell, px, q);
        CHECK(ok == nb.add(id, buy, px, q));
        CHECK(ok == mb.add(id, buy, px, q));
        if (ok) { live.push_back(id); info[id] = {buy ? 0 : 1, px}; qty[id] = q; agg[buy ? 0 : 1][px] += q; }
      } else {
        const std::size_t k = rng() % live.size();
        const std::uint64_t id = (rng() % 20 == 0) ? next + 1'000'000 : live[k];
        if (op < 8) {
          const bool ok = b.cancel(id);
          CHECK(ok == nb.cancel(id));
          CHECK(ok == mb.cancel(id));
          if (ok) { auto [s, px] = info[id]; agg[s][px] -= qty[id]; if (!agg[s][px]) agg[s].erase(px);
                    live[k] = live.back(); live.pop_back(); qty.erase(id); }
        } else {
          const std::uint32_t q = 1 + std::uint32_t(rng() % 300);
          const bool ok = b.execute(id, q);
          CHECK(ok == nb.execute(id, q));
          CHECK(ok == mb.execute(id, q));
          if (ok) { auto [s, px] = info[id]; agg[s][px] -= q; if (!agg[s][px]) agg[s].erase(px);
                    qty[id] -= q; if (!qty[id]) { qty.erase(id); live[k] = live.back(); live.pop_back(); } }
        }
      }
      CHECK(b.best_bid() == nb.best_bid() && b.best_ask() == nb.best_ask());
      CHECK(b.best_bid() == mb.best_bid() && b.best_ask() == mb.best_ask());
      if (step % 1000 == 0)
        for (int s = 0; s < 2; ++s)
          for (std::uint32_t i = 0; i < 400; ++i) {
            const std::uint32_t px = 1'000'000 + i * T;
            const auto it = agg[s].find(px);
            CHECK(b.qty_at(Side(s), px) == (it == agg[s].end() ? 0 : it->second));
          }
      if (fails > 10) return 1;
    }
    CHECK(b.live() == live.size());
  }
  std::printf(fails ? "%d FAILED\n" : "all tests passed\n", fails);
  return fails != 0;
}
