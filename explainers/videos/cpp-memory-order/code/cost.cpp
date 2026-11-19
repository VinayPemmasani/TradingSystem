// Cost of a release store (plain mov) vs a seq_cst store (xchg) in a tight loop, one thread.
#include <atomic>
#include <chrono>
#include <cstdio>

std::atomic<long> flag;
long data[64];

template <std::memory_order MO>
__attribute__((noinline)) double run(long n) {
  auto t0 = std::chrono::steady_clock::now();
  for (long i = 0; i < n; ++i) {
    data[i & 63] = i;          // the payload
    flag.store(i, MO);         // publish
  }
  return std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / n;
}

int main() {
  constexpr long N = 100'000'000;
  double best_rel = 1e9, best_sc = 1e9;
  for (int r = 0; r < 7; ++r) {
    double a = run<std::memory_order_release>(N), b = run<std::memory_order_seq_cst>(N);
    if (a < best_rel) best_rel = a;
    if (b < best_sc) best_sc = b;
  }
  std::printf("release %.2f ns/iter   seq_cst %.2f ns/iter\n", best_rel, best_sc);
}
