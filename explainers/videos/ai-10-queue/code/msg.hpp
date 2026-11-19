#pragma once
#include <cstdint>
struct Tick { uint64_t tsc; uint64_t seq; int64_t px; uint32_t qty; uint32_t sym; };
static_assert(sizeof(Tick) == 32);
