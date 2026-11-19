// Out-of-line copies of both functions, for counting instructions with objdump.
#include "ai.hpp"
#include "fast.hpp"
std::vector<Level> left(const Book& b, std::int64_t lo, std::int64_t hi) { return ai::levels_in_band(b, lo, hi); }
void right(const Book& b, std::int64_t lo, std::int64_t hi, fast::Band& o) { fast::levels_in_band(b, lo, hi, o); }
