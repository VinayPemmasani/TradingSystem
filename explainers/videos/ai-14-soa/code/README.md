# ai-14-soa: how it was measured

- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz, L1d 48 KiB, L2 2 MiB per core, L3 260 MiB shared), g++ 13.3,
  -O2 -std=c++20 -Wall -Wextra. The box was heavily loaded by other jobs (load average 14-17) during the runs.
- `ai.hpp` = LEFT (vector of 112-byte Order, branchy filter), `fast.hpp` = RIGHT (struct of arrays: px, qty, live_bid),
  `variants.hpp` = hot/cold split (24-byte OrderHot) and "AoS with the same branchless body" (isolates layout from branches).
- Field offsets in Order: symbol 0, account 32, id 64, created 72, updated 80, price 88, qty 96, side 104, active 105,
  ioc 106, post_only 107, size 112. Hot bytes: price, qty, side, active = 18. With a 112-byte stride, the hot range
  [88,106) of 4 consecutive orders falls in 5 of the 7 cache lines they span (80 bytes of lines per order).
- `test.cpp`: 300 random books, all four kernels return the same depth. `./test` -> PASS.
- `bench.cpp N`: N orders, 21 timed scans per kernel (noinline), ns/order p50/min/max. `runall.sh`: 5 rounds x
  {1,048,576; 8,388,608} orders, each launch pinned to the idlest core (`idlecpu.sh`). Output: bench.out.
- First RIGHT draft used `total += take ? qty : 0`; g++ turned it back into a branch (objdump `je`), which mispredicts
  on random books. The shipped version uses `qty & -take`, which compiles without a data-dependent jump.
