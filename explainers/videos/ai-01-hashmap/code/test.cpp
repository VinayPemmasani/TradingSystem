// Same observable results: random ticks applied to both, then every symbol compared.
#include <cassert>
#include <cstdio>
#include <random>
#include "ai.hpp"
#include "fast.hpp"
int main() {
  ai::QuoteCache a; hp::FlatQuotes b(1024); hp::SymbolIds ids;
  std::vector<std::string> names; std::vector<std::uint32_t> id;
  for (int i = 0; i < 500; ++i) { names.push_back("SYM" + std::to_string(i * 7919)); id.push_back(ids.intern(names.back())); b.insert(id.back()); }
  assert(ids.intern(names[3]) == id[3]);                      // interning is stable
  std::mt19937 rng(1);
  for (int k = 0; k < 100000; ++k) {
    int i = int(rng() % 500); double px = double(rng() % 10000) / 100;
    a.on_tick(names[i], px, px + 0.01, std::uint64_t(k)); b.on_tick(id[i], px, px + 0.01, std::uint64_t(k));
  }
  int seen = 0;
  for (int i = 0; i < 500; ++i) {
    const ai::Quote* x = a.find(names[i]); const hp::Quote* y = b.find(id[i]);
    assert((x == nullptr) == false && y);
    assert(x->bid == y->bid && x->ask == y->ask && x->ts == y->ts); ++seen;
  }
  assert(a.find("NOPE") == nullptr && b.find(999999) == nullptr);
  std::printf("test ok: %d symbols identical\n", seen);
}
