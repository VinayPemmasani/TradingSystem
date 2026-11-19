// For objdump: one out-of-line copy of each.
#include "ai.hpp"
#include "variants.hpp"
Stats f_general(const std::vector<Tick>& t, int b) { return scan(t, b); }
Stats f_hot(const Tick* t, std::size_t n, std::int64_t b) { return hot::scan(t, n, b); }
