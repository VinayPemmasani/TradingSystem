#include "lab/core/spsc_ring.hpp"
int main(){ static lab::SpscRing<long,1024> r; r.try_push(1); long x; return r.try_pop(x) ? 0 : 1; }
