#include <cstdio>
#include <random>
#include <vector>
#include "ai_api.hpp"
#include "fast.hpp"
int main() {
  std::mt19937 r(5); const int n = 100000; std::vector<int> mid(n);
  for (auto& m : mid) m = 99000 + int(r() % 2000);
  const ai::Quoter& qa = ai::make_clamp(3, 99500, 100500); fast::Clamp qf{3, 99500, 100500};
  ai::QuoteFn fn = [qf](int m) { return qf.quote(m); };
  for (int b = 0; b + kN <= n; b += kN) {
    Prices in, a, f, c; for (int i = 0; i < kN; ++i) in[i] = mid[b + i];
    ai::quote_all(qa, in, a); fast::quote_all(qf, in, f); ai::quote_all(fn, in, c);
    if (a != f || a != c) { std::puts("FAIL batch"); return 1; }
  }
  if (ai::run_serial(qa, mid.data(), n) != fast::run_serial(qf, mid.data(), n)) { std::puts("FAIL serial"); return 1; }
  std::puts("PASS: virtual, std::function and template give identical quotes (1562 batches of 64, and a 100000-tick serial chain)");
}
