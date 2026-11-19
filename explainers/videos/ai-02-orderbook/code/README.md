# ai-02-orderbook: how it was measured

- `ai.hpp` (LEFT): market-by-price book, `std::map<double, Level>` per side (bids with `std::greater<>`), qty 0 erases.
- `fast.hpp` (RIGHT): integer-tick prices, flat `std::vector<int64_t>` of qty per tick per side over a fixed window
  [base, base+n), best-bid / best-ask cursor; deleting the best scans to the next non-empty slot; out-of-window rejected.
- `ops.hpp`: shared op stream. Distance from mid ~ geometric (mean ~7 ticks), mid random-walks; if the level exists
  50% modify / 50% delete, else add. ~1/3 each; ~420 live levels per side in steady state.
- `test.cpp`: 5 seeds x 200k ops, best bid/ask compared after every op (ASan+UBSan). `./test`
- `bench.cpp`: g++ 13.3 `-O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW`, `taskset -c 3 ./bench`, 5 runs.
  Warm 200k ops, then per message = set level + read best bid & ask.
  * back to back: median of 1,000-message batches (robust to preemption on the shared box), 5 x 1M messages.
  * one at a time: lfence+rdtsc / rdtscp per message on the same (aged) books, p50/p99/p99.9; ~22 ns timer overhead included.
  * allocations per message: replaced operator new. Top-of-book read alone: 1M reads.
- Box: shared 4-vCPU cloud VM (load average 20-38 during runs), Xeon @ 2.1 GHz, 2 MB L2/core. No perf counters.
