// (1) Dependent random loads: ns per load vs working-set size.
// (2) Summing 1M ints: std::vector vs std::list vs std::map.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <list>
#include <map>
#include <numeric>
#include <random>
#include <vector>

struct alignas(64) Node { Node* next; };

double chase_ns(std::size_t bytes) {
  std::size_t n = bytes / sizeof(Node);
  std::vector<Node> nodes(n);
  std::vector<std::size_t> order(n);
  std::iota(order.begin(), order.end(), 0);
  std::shuffle(order.begin() + 1, order.end(), std::mt19937_64(1));
  for (std::size_t i = 0; i < n; ++i) nodes[order[i]].next = &nodes[order[(i + 1) % n]];
  Node* p = &nodes[0];
  const std::size_t steps = 20'000'000;
  for (std::size_t i = 0; i < n; ++i) p = p->next;  // warm
  double best = 1e30;
  for (int r = 0; r < 3; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < steps; ++i) p = p->next;
    auto t1 = std::chrono::steady_clock::now();
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / steps);
  }
  if (p == nullptr) std::puts("");
  return best;
}

template <class F> double ns_per(F f, std::size_t n, long& out) {
  double best = 1e30;
  for (int r = 0; r < 9; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    out = f();
    auto t1 = std::chrono::steady_clock::now();
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / n);
  }
  return best;
}

int main() {
  for (std::size_t kb : {16, 32, 256, 1024, 4096, 32768, 262144, 1048576})
    std::printf("working set %8zu KB: %6.2f ns/load\n", kb, chase_ns(kb * 1024));

  const std::size_t n = 1 << 20;
  std::vector<int> vals(n);
  std::mt19937 rng(3);
  for (auto& x : vals) x = rng() % 1000;
  std::vector<int> vec(vals);
  // Build the list and map in random key order so nodes scatter like a long-running heap.
  std::list<int> lst;
  std::map<int, int> mp;
  std::vector<int> keys(n); std::iota(keys.begin(), keys.end(), 0);
  std::shuffle(keys.begin(), keys.end(), rng);
  std::vector<std::list<int>::iterator> its;
  for (std::size_t i = 0; i < n; ++i) { lst.push_back(vals[i]); mp.emplace(keys[i], vals[keys[i]]); }
  // shuffle list node order by splicing
  std::list<int> l2;
  { std::vector<std::list<int>::iterator> v; for (auto it = lst.begin(); it != lst.end(); ++it) v.push_back(it);
    std::shuffle(v.begin(), v.end(), rng); for (auto it : v) l2.splice(l2.end(), lst, it); }
  long a, b, c, d;
  double tv = ns_per([&] { long s = 0; for (int x : vec) s += x; return s; }, n, a);
  double tl = ns_per([&] { long s = 0; for (int x : l2) s += x; return s; }, n, b);
  double tm = ns_per([&] { long s = 0; for (auto& [k, v] : mp) s += v; return s; }, n, c);
  if (a != b || a != c) { std::puts("MISMATCH"); return 1; }
  std::printf("sum 1M ints: vector %.2f  list %.2f  map %.2f ns/elem\n", tv, tl, tm);
}
