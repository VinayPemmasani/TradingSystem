#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>
#include "strat.hpp"

int run_virtual(const Strategy& s, const int* mids, int n);
int run_final(const Maker& s, const int* mids, int n);
template <Quoter S> int run_static(const S& s, const int* mids, int n);
extern template int run_static<Maker>(const Maker&, const int*, int);
int run_mixed(const Strategy* const* objs, const int* mids, int n);
int run_variant(const AnyStrategy* objs, const int* mids, int n);
int run_chosen(const AnyStrategy& chosen, const int* mids, int n);

template <class F> double ns_per(F f, int n, long& out) {
  double best = 1e30;
  for (int r = 0; r < 31; ++r) {
    auto t0 = std::chrono::steady_clock::now();
    long s = 0;
    for (int k = 0; k < 20; ++k) s += f();
    auto t1 = std::chrono::steady_clock::now();
    out = s;
    best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / (20.0 * n));
  }
  return best;
}

int main() {
  const int n = 1 << 16;
  std::mt19937 rng(11);
  std::vector<int> mids(n);
  for (auto& m : mids) m = 1'000'000 + int(rng() % 1000);
  Maker mk; Taker tk;
  std::vector<const Strategy*> one(n, &mk), mixed(n), grouped(n);
  std::vector<AnyStrategy> vmix(n), vone(n, Maker{});
  for (int i = 0; i < n; ++i) {
    bool t = rng() & 1;
    mixed[i] = t ? static_cast<const Strategy*>(&tk) : &mk;
    vmix[i] = t ? AnyStrategy{tk} : AnyStrategy{mk};
  }
  grouped = mixed;
  std::stable_sort(grouped.begin(), grouped.end(), [&](auto a, auto b) { return a == &mk && b != &mk; });
  AnyStrategy chosen = Maker{};
  long a, b, c, d, e, f, g, h, x;
  double t_virt = ns_per([&] { return run_virtual(mk, mids.data(), n); }, n, a);
  double t_fin = ns_per([&] { return run_final(mk, mids.data(), n); }, n, b);
  double t_sta = ns_per([&] { return run_static(mk, mids.data(), n); }, n, c);
  double t_one = ns_per([&] { return run_mixed(one.data(), mids.data(), n); }, n, d);
  double t_mix = ns_per([&] { return run_mixed(mixed.data(), mids.data(), n); }, n, e);
  double t_grp = ns_per([&] { return run_mixed(grouped.data(), mids.data(), n); }, n, x);
  double t_var = ns_per([&] { return run_variant(vmix.data(), mids.data(), n); }, n, f);
  double t_vone = ns_per([&] { return run_variant(vone.data(), mids.data(), n); }, n, h);
  double t_cho = ns_per([&] { return run_chosen(chosen, mids.data(), n); }, n, g);
  bool ok = a == b && b == c && c == d && c == g && c == h && e == f;
  std::printf("%s\n", ok ? "results agree" : "MISMATCH");
  std::printf("virtual, one object           %.2f ns/call\n", t_virt);
  std::printf("virtual via ptr array, 1 type %.2f\n", t_one);
  std::printf("virtual, 2 types grouped      %.2f\n", t_grp);
  std::printf("virtual, 2 types random       %.2f\n", t_mix);
  std::printf("final (devirtualized, inline) %.2f\n", t_fin);
  std::printf("template + concept            %.2f\n", t_sta);
  std::printf("variant visit, random         %.2f\n", t_var);
  std::printf("variant visit, one type       %.2f\n", t_vone);
  std::printf("visit once, then static loop  %.2f\n", t_cho);
  return ok ? 0 : 1;
}
