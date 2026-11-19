#pragma once
#include <array>
inline constexpr int kN = 64;             // instruments quoted every tick (fixed at startup)
using Prices = std::array<int, kN>;
