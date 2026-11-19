#include <cmath>
#include <cstdio>
#include <random>
#include <string>

#include "lab/fix/codec.hpp"
#include "parse.hpp"

static int fails = 0;
#define CHECK(x) do { if (!(x)) { std::printf("FAIL line %d: %s\n", __LINE__, #x); ++fails; } } while (0)

using P = std::optional<std::uint64_t> (*)(std::string_view);

int main() {
  const P fns[] = {parse_loop, parse_fc, parse_swar,
                   [](std::string_view s) { return lab::fix::parse_price(s); }};
  struct Case { const char* s; std::optional<std::uint64_t> want; };
  const Case cases[] = {
      {"123.4567", 1234567}, {"0.5", 5000}, {"100.25", 1002500}, {"100", 1000000},
      {"100.", 1000000}, {".5", 5000}, {"0", 0}, {"0.0001", 1}, {"0.29", 2900},
      {"9999.9999", 99999999}, {"10000.0001", 100000001}, {"007.10", 71000},
      {"429496.7295", 4294967295ULL}, {"1000000000000", 10000000000000000ULL},
      {"1000000000000.9999", 10000000000009999ULL},
      {"1000000000001", std::nullopt},           // over the cap
      {"99999999999999999999", std::nullopt},    // overflows uint64 itself
      {"", std::nullopt}, {".", std::nullopt}, {"1.23456", std::nullopt},
      {"-1.5", std::nullopt}, {"+1.5", std::nullopt}, {" 1.5", std::nullopt},
      {"1.5 ", std::nullopt}, {"1e3", std::nullopt}, {"inf", std::nullopt},
      {"nan", std::nullopt}, {"1.2.3", std::nullopt}, {"12a", std::nullopt},
      {"1..2", std::nullopt}, {"0x10", std::nullopt}, {"1,5", std::nullopt},
      {"/", std::nullopt}, {":", std::nullopt}, {"1.:", std::nullopt}, {"1./", std::nullopt},
  };
  for (const auto& c : cases)
    for (int k = 0; k < 4; ++k) {
      const auto got = fns[k](c.s);
      if (got != c.want) {
        std::printf("FAIL fn %d on \"%s\": got %lld want %lld\n", k, c.s,
                    got ? (long long)*got : -1LL, c.want ? (long long)*c.want : -1LL);
        ++fails;
      }
    }
  // SWAR primitive against a scalar loop on every 8-digit pattern sampled + all 8-byte edges
  std::mt19937_64 rng(1);
  for (int i = 0; i < 2'000'000; ++i) {
    char b[8];
    std::uint64_t want = 0;
    for (char& ch : b) { ch = char('0' + rng() % 10); want = want * 10 + std::uint64_t(ch - '0'); }
    std::uint64_t v;
    std::memcpy(&v, b, 8);
    CHECK(all_digits8(v));
    CHECK(swar8(v) == want);
    b[rng() % 8] = char(rng() % 256);  // corrupt one byte
    std::memcpy(&v, b, 8);
    bool digits = true;
    for (char ch : b) digits &= ch >= '0' && ch <= '9';
    CHECK(all_digits8(v) == digits);
    if (fails > 10) return 1;
  }
  // every single non-digit byte in every position is rejected
  for (int pos = 0; pos < 8; ++pos)
    for (int c = 0; c < 256; ++c) {
      char b[8] = {'1', '2', '3', '4', '5', '6', '7', '8'};
      b[pos] = char(c);
      std::uint64_t v;
      std::memcpy(&v, b, 8);
      CHECK(all_digits8(v) == (c >= '0' && c <= '9'));
    }
  // randomized: all parsers agree with each other and with the integer we formatted
  for (int i = 0; i < 2'000'000; ++i) {
    const std::uint64_t whole = rng() % 5 == 0 ? rng() % 1'000'000'000'000ULL : rng() % 20000;
    const int nd = int(rng() % 5);
    std::uint64_t frac = nd ? rng() % kPow10[nd] : 0;
    std::string s = std::to_string(whole);
    if (nd) { std::string f = std::to_string(frac); s += "." + std::string(nd - f.size(), '0') + f; }
    else if (rng() & 1) s += ".";
    const std::uint64_t want = whole * 10000 + frac * kPow10[4 - nd];
    for (int k = 0; k < 4; ++k) if (fns[k](s) != want) { std::printf("FAIL fn %d %s\n", k, s.c_str()); ++fails; }
    // random garbage strings: all must agree (accept/reject and value)
    std::string g;
    const int len = int(rng() % 10);
    static const char al[] = "0123456789..-+e x";
    for (int j = 0; j < len; ++j) g += al[rng() % (sizeof al - 1)];
    const auto r0 = fns[0](g);
    for (int k = 1; k < 4; ++k) if (fns[k](g) != r0) { std::printf("DIFF fn %d \"%s\"\n", k, g.c_str()); ++fails; }
    if (fails > 10) return 1;
  }
  // how often does truncating stod(s) * 10000 give the wrong Price(4)?
  int trunc_wrong = 0, round_wrong = 0;
  const int N = 1'000'000;
  for (int i = 0; i < N; ++i) {
    const std::uint64_t want = rng() % 10'000'000;  // 0.0000 .. 999.9999
    char s[32];
    std::snprintf(s, sizeof s, "%llu.%04llu", (unsigned long long)(want / 10000), (unsigned long long)(want % 10000));
    const double d = std::stod(s);
    trunc_wrong += std::uint64_t(d * 10000) != want;
    round_wrong += std::uint64_t(std::llround(d * 10000)) != want;
  }
  std::printf("stod*10000 truncated: %d of %d wrong; llround: %d wrong\n", trunc_wrong, N, round_wrong);
  std::printf("0.29 -> %llu, 1.15 -> %llu\n", (unsigned long long)(std::stod("0.29") * 10000),
              (unsigned long long)(std::stod("1.15") * 10000));
  std::printf(fails ? "%d FAILED\n" : "all tests passed\n", fails);
  return fails != 0;
}
