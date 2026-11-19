# ai-13-branchless: how it was measured

- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz, L1d 48 KiB, L2 2 MiB per core), g++ 13.3, -O2 -std=c++20 -Wall -Wextra.
- `ai.hpp` = LEFT (general), `fast.hpp` = RIGHT (hot path, namespace hot), `variants.hpp` = lookup-table and
  "branchy + cold path out of line" variants, measured for comparison.
- `test.cpp`: 500 random batches incl. bad ticks; all four return identical Stats. `./test 2>/dev/null` -> PASS.
- `bench.cpp`: 16,384 ticks (256 KiB, L2-resident), each kernel behind a noinline wrapper, 101 timed passes,
  ns/tick p50 / min / p99. Three inputs: sides in runs of 256 + 1% big; side repeats 80% + 10% big; random side + 50% big.
  Run: `taskset -c $(./idlecpu.sh) ./bench 2>/dev/null` three times (bench.out).
- `bench.s`: objdump of the bench binary. General loop: two data-dependent jumps per tick (side, size) and the totals
  live in memory (`add %rax,0x0(%rbp)`), because the inline fprintf call is opaque. Hot loop: 15 instructions,
  only the never-taken bad-tick jump and the loop jump.
- Caveat seen while measuring: branchy loops are sensitive to code layout; an inlined build of branchy+cold measured
  1.5 ns/tick on the predictable input instead of 0.77. Reported numbers are from the noinline build.
