# ai-06-copies: how it was measured
- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`.
- `./test`: LEFT (ai.hpp), MIDDLE (mid.hpp: const& but still operator+/to_string) and RIGHT (fast.hpp) give identical
  accept/reject decisions and identical tag text for 20,000 orders.
- `./bench`: 400k orders per variant (4096 distinct, 8 accounts, 16 symbols, 1-3 fills, ~62% accepted), each call timed
  with rdtscp (timer overhead subtracted). Allocations counted by a replaced global operator new.
- Instruction counts: objdump of visible.cpp (instr.txt). Raw output of 5 runs: results.txt.
