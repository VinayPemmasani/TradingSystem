# ai-15-fixed-point: how it was measured

- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3, -O2 -std=c++20 -Wall -Wextra, load average 22-24
  from other jobs during the runs.
- `ai.hpp` = LEFT (double prices, off-tick check with epsilon, std::round to find the level, double notional),
  `fast.hpp` = RIGHT (int64 ticks of 0.01, level = px - base, int64 notional).
- `demo.cpp` -> demo.out: the correctness cases shown in the video (0.1+0.2, map<double> with two "0.3" levels,
  100 + ten 0.01 steps, int64_t(0.29/0.01) = 28, std::round(1.005*100) = 100, a million 0.03 adds).
- `test.cpp`: 100 random books x 2000 on-grid updates, identical level quantities; an off-tick price is rejected.
- `bench.cpp`: 8,192 updates into a 2,000-level book, kernels `noinline` + `flatten` (so `apply` is inlined in both),
  41 passes, ns/update p50/min/max, 3 runs pinned to the idlest core (bench.out). Also a decomposition variant
  without the off-tick check. Notional after all 41 x 8192 = 335,872 updates compared against the exact tick sum.
- `bench.s`: objdump. Double loop: 2 x `divsd`, 2 x `call round@plt` (std::round is half-away-from-zero, which SSE4.1
  `roundsd` cannot do in one instruction, so g++ calls libm even with -march=native), register spills around the
  calls; about 35 instructions per update. Int loop: 10 instructions (sub, add to memory, imul, add to memory, ...).
