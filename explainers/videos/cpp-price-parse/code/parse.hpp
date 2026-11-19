#pragma once
// ASCII price -> Price(4): integer count of 1/10000 dollars. "123.4567" -> 1234567, "0.5" -> 5000.
// Accepts digits [ '.' digits ], at least one digit, at most 4 decimals. No sign, exponent,
// spaces, inf/nan. Returns nullopt on anything else or on overflow.
#include <bit>
#include <charconv>
#include <cstdint>
#include <cstring>
#include <optional>
#include <string_view>

inline constexpr std::uint64_t kMaxWhole = 1'000'000'000'000ULL;  // same cap as libs/fix
inline constexpr std::uint64_t kPow10[5] = {1, 10, 100, 1000, 10000};

// 1) Plain digit loop.
inline std::optional<std::uint64_t> parse_loop(std::string_view s) {
  const char* p = s.data();
  const char* e = p + s.size();
  std::uint64_t whole = 0;
  const char* w0 = p;
  for (; p < e && *p != '.'; ++p) {
    const unsigned d = unsigned(*p - '0');
    if (d > 9 || whole > kMaxWhole / 10) return std::nullopt;
    whole = whole * 10 + d;
  }
  if (whole > kMaxWhole) return std::nullopt;
  const bool has_whole = p != w0;
  std::uint64_t frac = 0;
  int n = 0;
  if (p < e) {  // *p == '.'
    for (++p; p < e; ++p, ++n) {
      const unsigned d = unsigned(*p - '0');
      if (d > 9 || n == 4) return std::nullopt;
      frac = frac * 10 + d;
    }
  }
  if (!has_whole && n == 0) return std::nullopt;  // "", ".",
  return whole * 10000 + frac * kPow10[4 - n];   // "0.5": 5 * 1000
}

// 2) std::from_chars for the integer part, short digit loop for the fraction.
inline std::optional<std::uint64_t> parse_fc(std::string_view s) {
  const char* p = s.data();
  const char* e = p + s.size();
  std::uint64_t whole = 0;
  const auto [q, ec] = std::from_chars(p, e, whole);
  if (ec == std::errc::result_out_of_range || whole > kMaxWhole) return std::nullopt;
  if (ec != std::errc{} && (q == e || *q != '.')) return std::nullopt;  // no digits, no '.'
  const bool has_whole = ec == std::errc{};
  p = q;
  if (p == e) return whole * 10000;
  if (*p != '.') return std::nullopt;
  const char* f = ++p;
  if (e - f > 4 || (e == f && !has_whole)) return std::nullopt;
  std::uint64_t frac = 0;
  for (; p < e; ++p) {
    const unsigned d = unsigned(*p - '0');
    if (d > 9) return std::nullopt;
    frac = frac * 10 + d;
  }
  return whole * 10000 + frac * kPow10[4 - (e - f)];
}

// 3) SWAR: 8 ASCII digits -> integer with three multiplies (little-endian).
static_assert(std::endian::native == std::endian::little);
inline bool all_digits8(std::uint64_t v) {
  return (((v & 0xF0F0F0F0F0F0F0F0ULL) |
           (((v + 0x0606060606060606ULL) & 0xF0F0F0F0F0F0F0F0ULL) >> 4)) ==
          0x3333333333333333ULL);
}
inline std::uint64_t swar8(std::uint64_t v) {
  v = (v & 0x0F0F0F0F0F0F0F0FULL) * 2561 >> 8;              // pairs of digits
  v = (v & 0x00FF00FF00FF00FFULL) * 6553601 >> 16;          // groups of four
  return (v & 0x0000FFFF0000FFFFULL) * 42949672960001ULL >> 32;  // all eight
}
// Prices below 10,000 dollars: right-align the whole part into bytes 0-3 and
// left-align the fraction into bytes 4-7 of "00000000"; one SWAR call gives Price(4).
inline std::optional<std::uint64_t> parse_swar(std::string_view s) {
  const std::size_t dot = s.find('.');
  const std::size_t w = dot == std::string_view::npos ? s.size() : dot;
  const std::size_t f = dot == std::string_view::npos ? 0 : s.size() - dot - 1;
  if (w > 4) return parse_fc(s);  // big prices: fallback
  if (f > 4 || (w == 0 && f == 0)) return std::nullopt;
  char buf[8] = {'0', '0', '0', '0', '0', '0', '0', '0'};
  std::memcpy(buf + 4 - w, s.data(), w);
  std::memcpy(buf + 4, s.data() + w + 1, f);
  std::uint64_t v;
  std::memcpy(&v, buf, 8);
  if (!all_digits8(v)) return std::nullopt;
  return swar8(v);
}
