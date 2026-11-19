# ai-05-vector: how it was measured
- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`.
- `./test`: LEFT, reserved-vector, and RIGHT return identical levels for 10,000 ticks.
- `./bench`: 400k calls per variant, each timed with rdtscp (timer overhead subtracted, TSC calibrated to ns
  against steady_clock). Book of 32 levels; each tick asks for a random band 4..24 levels wide.
  The timed region includes building the result, summing its qty, and (LEFT) freeing the vector.
- Allocations counted by a replaced global operator new (alloc_count.cpp).
- Instruction counts: `objdump -d` of visible.cpp (out-of-line copies).
- Raw output of 3 runs: results.txt
