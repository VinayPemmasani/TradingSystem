#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <sstream>
#include <string>
#include <vector>

#include "lab/fix/codec.hpp"
#include "parse.hpp"

// 1M realistic prices: 1..999 dollars, 0, 2 or 4 decimals, a few sub-dollar.
static std::vector<std::string_view> make(std::string& store) {
  std::mt19937_64 rng(3);
  std::vector<std::pair<std::size_t, std::size_t>> pos;
  for (int i = 0; i < 1'000'000; ++i) {
    char b[32];
    const unsigned w = rng() % 10 == 0 ? 0 : 1 + unsigned(rng() % 999);
    const unsigned k = unsigned(rng() % 3);
    int n = k == 0 ? std::snprintf(b, 32, "%u", w)
          : k == 1 ? std::snprintf(b, 32, "%u.%02u", w, unsigned(rng() % 100))
                   : std::snprintf(b, 32, "%u.%04u", w, unsigned(rng() % 10000));
    if (w == 0 && k == 0) n = std::snprintf(b, 32, "0.5");
    pos.push_back({store.size(), std::size_t(n)});
    store.append(b, std::size_t(n));
    store.push_back('\0');  // strtod needs a terminator
  }
  std::vector<std::string_view> v;
  for (auto [p, n] : pos) v.emplace_back(store.data() + p, n);
  return v;
}

template <class F>
void bench(const char* name, const std::vector<std::string_view>& in, F f, int reps = 7) {
  std::vector<double> r;
  std::uint64_t sink = 0;
  for (int k = 0; k < reps; ++k) {
    const auto t0 = std::chrono::steady_clock::now();
    for (auto s : in) sink += f(s);
    const auto t1 = std::chrono::steady_clock::now();
    r.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / double(in.size()));
  }
  std::sort(r.begin(), r.end());
  std::printf("%-14s median %7.2f ns  min %7.2f  max %7.2f   (%llu)\n", name, r[r.size() / 2], r[0],
              r.back(), (unsigned long long)(sink % 7));
}

void main_bench() {
  std::string store;
  store.reserve(16'000'000);
  const auto in = make(store);
  bench("stod", in, [](std::string_view s) { return std::uint64_t(std::llround(std::stod(std::string(s)) * 10000)); }, 3);
  bench("strtod", in, [](std::string_view s) { return std::uint64_t(std::llround(std::strtod(s.data(), nullptr) * 10000)); }, 3);
  bench("stringstream", in, [](std::string_view s) {
    std::istringstream ss{std::string(s)}; double d = 0; ss >> d; return std::uint64_t(std::llround(d * 10000)); }, 3);
  bench("digit loop", in, [](std::string_view s) { return parse_loop(s).value_or(0); });
  bench("from_chars", in, [](std::string_view s) { return parse_fc(s).value_or(0); });
  bench("swar", in, [](std::string_view s) { return parse_swar(s).value_or(0); });
  bench("lab fix", in, [](std::string_view s) { return lab::fix::parse_price(s).value_or(0); });
}
int main(){ std::string store; store.reserve(16'000'000); auto in = make(store); int bad=0;
 for (auto s: in){ auto a=parse_loop(s); auto d=std::llround(std::strtod(s.data(),nullptr)*10000); if(!a || (long long)*a!=d){ if(bad<5) std::printf("[%.*s] %lld %lld\n",(int)s.size(),s.data(), a?(long long)*a:-1LL, d); ++bad;} } std::printf("bad %d\n",bad);}
