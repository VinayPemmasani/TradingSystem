#pragma once
// LEFT: the general-purpose version (on screen verbatim below the includes).
#include <cmath>
#include <cstddef>
#include <stdexcept>
#include <vector>
struct Levels {
  double base;               // price of level 0
  std::vector<double> qty;   // one slot per tick
  double notional = 0;
};
constexpr double kTick = 0.01, kEps = 1e-9;
void apply(Levels& L, double px, double qty) {
  const double t = px / kTick;
  if (std::fabs(t - std::round(t)) > kEps)
    throw std::invalid_argument("off tick");
  const auto i = static_cast<std::size_t>(
      std::round((px - L.base) / kTick));
  L.qty[i] += qty;
  L.notional += px * qty;
}
