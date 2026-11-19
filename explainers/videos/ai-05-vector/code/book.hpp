#pragma once
#include <array>
#include <cstdint>
using Px = std::int64_t;
inline constexpr int kMaxDepth = 32;
struct Level { Px px; std::int32_t qty; std::int32_t orders; };  // 16 bytes
struct Book { std::array<Level, kMaxDepth> levels; int depth = 0; };  // depth <= kMaxDepth
