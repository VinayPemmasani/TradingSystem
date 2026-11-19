// The general version lives in its own translation unit, like a strategy library loaded by config.
#include "ai.hpp"
#include "ai_api.hpp"
namespace ai {
const Quoter& make_clamp(int edge, int lo, int hi) { static Clamp c(edge, lo, hi); return c; }
}  // namespace ai
