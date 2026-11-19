// g++ -O2 -std=c++20 -S asm.cpp  -> asm.s  (the side-by-side on screen)
#include <cstdint>
#include "ai.hpp"
#include "fast.hpp"
struct Quote { int64_t px; int64_t qty; };
template class RingSeq<Quote, 1024>;
template class RingAR<Quote, 1024>;
