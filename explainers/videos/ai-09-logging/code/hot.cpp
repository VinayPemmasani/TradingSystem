#include "ai.hpp"
#include "fast.hpp"
__attribute__((noinline)) void ai_call(Logger& l, const char* s, int64_t p, uint32_t q, uint64_t o) { l.fill(s, p, q, o); }
__attribute__((noinline)) void fast_call(LogRing<65536>& r, const char* s, int64_t p, uint32_t q, uint64_t o) { r.fill(s, p, q, o); }
