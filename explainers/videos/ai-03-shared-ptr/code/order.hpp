#pragma once
#include <cstdint>
struct Order { std::uint64_t id; std::int64_t px, qty; std::uint32_t acct; std::uint32_t flags; };
struct Stats { std::int64_t max_qty = 10'000, notional = 0, out = 0, rejects = 0; };
