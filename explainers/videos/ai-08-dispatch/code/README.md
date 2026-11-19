# ai-08-dispatch: how it was measured
- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`.
  The box was heavily loaded by other jobs (load average 40+) during these runs; throughput numbers are best-of-15.
- The general version (ai.hpp) is compiled in its own TU (lib.cpp), as an engine calling a strategy chosen at run time.
  Two builds of lib.cpp:
  * `bench`: default -O2. Clamp is visible in lib.cpp, so g++ speculatively devirtualizes (compare the vtable slot
    with Clamp::quote, inline a guarded copy, fall back to `call *%rax`).
  * `bench_opaque`: lib.cpp built with `-fno-devirtualize-speculatively`, modelling a strategy defined in another
    TU or plugin, where the compiler cannot guess the target: a real indirect call per price.
- `./test`: virtual, std::function and template versions give identical quotes for 1,562 batches of 64 and for a
  100,000-tick serial chain.
- `./bench`: 256 ticks x 64 instruments per pass, 200 reps, best of 15 passes -> ns per quote. "serial" = a chain where
  each quote feeds the next (no vectorization possible). Allocations: 0 everywhere (the lambda fits std::function's
  local buffer).
- Vectorization: `-fopt-info-vec-optimized` reports "loop vectorized using 16 byte vectors" for fast::quote_all.
  Note: at -O2 (very-cheap cost model) g++ 13 only vectorized it with a fixed trip count (std::array<int, 64>) and
  with the strategy passed by value (by const& the output stores might alias its fields).
- Raw output: results.txt (5 runs of each build). Instruction counts: instr.txt.
