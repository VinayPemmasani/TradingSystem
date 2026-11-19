# cpp-live-optimize: how it was measured

A market data handler optimized live, one step at a time. Every version must print the same output.

- `common.hpp`: the feed message, a deterministic synthetic feed, rdtsc timing, percentiles, an allocation counter.
- `v0_naive.hpp` (step 0, the snippet handed over), `v1_ds.hpp` (index by locate code, flat array, hot fields in
  one line), `v1h_table.hpp` (no locate code: key on the 8 symbol bytes in an open-addressing table),
  `v2a_ilp.hpp` (four accumulators), `v2_pipe.hpp` (running sums, no divide), `v3_branch.hpp` (side as an index,
  one validation test), `v4_alloc.hpp` (fixed 32-slot window, no malloc). `all.hpp` includes them all.
- `queues.hpp`: part 2 hand-offs between a feed thread and a strategy thread (mutex+cv, packed ring, padded ring);
  `mt.cpp` also uses the lab's `lab::SpscRing` from `libs/core`.

Programs (built by `explainers/samples.sh` into `build/samples/cpp-live-optimize/`; by hand from this directory:
`g++ -std=c++20 -O2 -Wall -Wextra -pthread -I../../../../libs/core/include mt.cpp -o mt`):

- `test [messages]`: every version produces the same signals and the same final state.
- `bench [messages] [runs] [version]`: single-thread per-message latency (lfence;rdtsc around each call), pinned to
  CPU 2. Results: `results1.txt`, `bench1.out`.
- `ilp`: the 32-trade VWAP loop in L1, one accumulator vs four, dependent divide vs cross-multiply.
- `fs`: two threads bumping counters in one cache line vs their own lines (`fs.out`).
- `mt [messages] [gap_ns] [runs] [variant]`: feed thread (CPU 1) to strategy thread (CPU 2), one-way latency from the
  feed's rdtsc stamp. Results: `mt_main.out`, `mt_main2.out`, `mt1.out`, `mt2.out`, `mt_lat.out`, `mt_flat.out`
  (gap 0 = flat out). `tsan.out` is a short run under `-fsanitize=thread` (no races reported; timings meaningless).
- `run_all.sh [bindir]`: the measurement run for the video (`chrt -f 10`, needs root or `CAP_SYS_NICE`).

Assembly shown on screen: `asm.cpp` -> `asm.s`, `ilp.s`; `broken.cpp` (a plain `bool` hand-off, a data race) ->
`broken.s`; `fixed.cpp` (release/acquire) -> `fixed.s`; all `g++ -O2 -S`. `fixed_arm.cpp` -> `fixed_arm.s` is
`clang --target=aarch64-linux-gnu -O2 -S` (it uses `__atomic` builtins because no AArch64 libstdc++ headers are needed).

Box: shared 4-vCPU cloud VM (Xeon @ 2.10GHz), g++ 13.3, load average 11-22 from other jobs during the runs.
Treat the numbers as relative; rerun on pinned, idle cores for your own.
