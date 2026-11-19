# ai-07-exceptions: how it was measured
- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`.
- `./test`: LEFT (throw/catch) and RIGHT (enum code, [[unlikely]], cold out-of-line reject) make the same accept/reject
  decisions and write the same reason text for 100,000 orders with 3% rejects.
- `./bench`: 400k orders, at 0% and 1% rejects (half bad qty, half bad price). Per order: rdtscp timing (overhead
  subtracted) for p50/p99/p99.9, and separately the latency of the rejected orders only. "loop" = whole 400k loop
  timed without per-call timers, best of 7 passes, divided by N (ns/order, includes rejects).
  50k warm-up orders first (with rejects), so the unwinder's caches are warm.
- Allocations: replaced global operator new (does not see __cxa_allocate_exception, which uses malloc directly).
- Instruction counts: objdump of visible.cpp (instr.txt). Raw output of 5 runs: results.txt.
