#pragma once
#include "ai.hpp"
#include <regex>
namespace var {
// The other common general-purpose answer: a regex.
inline Quote parse_regex(const std::string& line) {
  static const std::regex re(R"(([A-Z0-9]+),(\d+(?:\.\d{1,2})?),(-?\d+))");
  std::smatch m;
  if (!std::regex_match(line, m, re)) throw std::invalid_argument("bad line");
  return {m[1].str(), std::stod(m[2].str()), std::stoi(m[3].str())};
}
// std::from_chars for both numbers (C++17 floating from_chars, GCC 11+), still a double price.
inline bool parse_fc_double(std::string_view s, std::string_view& sym, double& px, long& qty) {
  const char *p = s.data(), *e = p + s.size();
  const char* c = std::find(p, e, ',');
  if (c == e) return false;
  sym = std::string_view(p, c - p);
  auto [r1, e1] = std::from_chars(c + 1, e, px);
  if (e1 != std::errc{} || r1 == e || *r1 != ',') return false;
  auto [r2, e2] = std::from_chars(r1 + 1, e, qty);
  return e2 == std::errc{} && r2 == e;
}
}  // namespace var
