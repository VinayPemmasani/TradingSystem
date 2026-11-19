# ai-01-hashmap: how it was measured

- `ai.hpp` (LEFT): `std::unordered_map<std::string, Quote>`, looked up by symbol string on every tick.
- `fast.hpp` (RIGHT): symbols interned to a small integer id once at startup (`SymbolIds`), then a flat
  open-addressing table (`FlatQuotes`, 32 B slots, linear probing, Fibonacci hash, power-of-two capacity, load <= 0.8).
- `test.cpp`: 100k random ticks applied to both; every symbol's quote compared (ASan+UBSan build). `./test`
- `bench.cpp`: g++ 13.3 `-O2 -std=c++20 -Wall -Wextra -DHZ_COUNT_NEW`, run `taskset -c 3 ./bench <N>`.
  N instruments (7-char symbols, fit SSO), 1M uniform random ticks, same sequence for both.
  * ns/tick back to back: 5 alternating runs, median (min-max).
  * one tick at a time: lfence+rdtsc / rdtscp around each call, p50/p99; timer overhead ~21 ns is printed and included.
  * heap bytes per instrument: replaced operator new counts bytes during build.
  * hot-path allocations: counted during all timed runs (0 for both).
- Box: shared 4-vCPU cloud VM (Xeon @ 2.1 GHz, 2 MB L2 per core). No perf counters available.

Results used in the video (3 runs at N=200000, 2 at N=1000): see bench.out and the write-up.
