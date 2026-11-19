# ai-04-pool: how it was measured

- `ai.hpp` (LEFT): `std::make_unique<Order>` per new order, `std::vector<std::unique_ptr<Order>>` of live orders;
  cancel moves the last into the gap (old order freed by unique_ptr).
- `fast.hpp` (RIGHT): `Pool<Order>`: one array of slots allocated and written at startup (pages faulted in), an
  intrusive free list (union of object and next pointer); acquire pops, release pushes; empty pool -> reject.
  The live index vector is also touched at startup.
- `order.hpp`: 128-byte Order; both sides write the full object (value-initialized) per new order.
- `test.cpp`: 300k random new/cancel messages into both, all live orders compared in order; full pool rejects (ASan+UBSan).
- `bench.cpp`: g++ 13.3 `-O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW`; fresh process per variant:
  `taskset -c 3 ./bench new`, `taskset -c 3 ./bench pool`, alternated, 3 runs each.
  50k live orders at start; 2M messages; live target ramps 50k -> 150k -> 50k every 400k messages (bursts).
  * per message: lfence+rdtsc / rdtscp; p50/p99/p99.9 (timer overhead ~22 ns included and printed).
  * allocations per message: replaced operator new during the timed loop.
  * page faults: getrusage minor+major during the timed loop.
  * p99.99 and max are dominated by scheduler preemption on this loaded VM (both variants ~15-35 us / ~20 ms), so not used.
- Box: shared 4-vCPU cloud VM (load average ~50 during runs), Xeon @ 2.1 GHz. No perf counters.
