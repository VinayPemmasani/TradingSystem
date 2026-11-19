// Correctness: what double prices do. g++ -O2 -std=c++20 -Wall -Wextra demo.cpp -o demo && ./demo
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <map>
int main() {
  std::printf("0.1 + 0.2 == 0.3 ? %s   (0.1 + 0.2 = %.17g)\n", 0.1 + 0.2 == 0.3 ? "true" : "false", 0.1 + 0.2);
  std::map<double, std::int64_t> book;
  book[0.3] += 100; book[0.1 + 0.2] += 50;
  std::printf("map<double,qty>: add 100 @ 0.3, add 50 @ 0.1+0.2 -> %zu levels\n", book.size());
  std::map<std::int64_t, std::int64_t> tb;
  tb[30] += 100; tb[10 + 20] += 50;
  std::printf("map<ticks,qty>:  add 100 @ 30,  add 50 @ 10+20   -> %zu level, qty %lld\n", tb.size(), (long long)tb[30]);
  double p = 100.0; for (int i = 0; i < 10; ++i) p += 0.01;
  std::printf("100.00 + ten 0.01 steps == 100.10 ? %s  (%.17g)\n", p == 100.10 ? "true" : "false", p);
  std::printf("int64_t(0.29 / 0.01) = %lld   (0.29/0.01 = %.17g)\n", (long long)(0.29 / 0.01), 0.29 / 0.01);
  std::printf("int64_t(1.15 / 0.05) = %lld   (1.15/0.05 = %.17g)\n", (long long)(1.15 / 0.05), 1.15 / 0.05);
  std::printf("std::round(1.005 * 100) = %.0f  (1.005 is stored as %.17g)\n", std::round(1.005 * 100), 1.005);
  std::printf("std::round(2.675 * 100) = %.0f  (2.675 is stored as %.17g)\n", std::round(2.675 * 100), 2.675);
  // Accumulated notional drift
  double nd = 0; std::int64_t ni = 0;
  for (int i = 0; i < 1000000; ++i) { nd += 0.01 * 3; ni += 1 * 3; }
  std::printf("1,000,000 fills of 3 @ 0.01: double %.10f  vs ticks %lld x 0.01 = %lld.%02lld\n", nd, (long long)ni,
              (long long)(ni / 100), (long long)(ni % 100));
}
