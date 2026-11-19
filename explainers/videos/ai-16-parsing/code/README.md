# ai-16-parsing: how it was measured

- Box: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 / libstdc++, -O2 -std=c++20 -Wall -Wextra.
- `ai.hpp` = LEFT (stringstream + getline + stod/stoi), `variants.hpp` = std::regex version and a from_chars version
  that still produces a double price, `fast.hpp` = RIGHT (find commas, digit loop into int64 ticks of 0.01,
  std::from_chars for qty; string_view symbol; returns bool).
- `alloc_count.hpp`: replaced global operator new counting allocations (harness only).
- `test.cpp`: 200,000 random lines with 0, 1 or 2 decimals; stringstream, regex and hot agree (hot px == llround(px*100)
  == exact ticks). 6 malformed lines are rejected by both (throw / false). 3 off-spec lines ("5012.255", "5.0e3",
  " 5012.25") are rejected by hot only (stod accepts them). Known difference: a price of just "." parses as 0 in hot
  and throws in stod.
- `bench.cpp`: 4,096 lines like "ESZ6,5083.42,229" (14-16 chars), 31 passes, ns/line p50/min/max, allocations per line;
  3 runs pinned to the idlest core (bench.out). Lines of 16 chars exceed libstdc++'s 15-char SSO buffer, so the
  stringstream's copy of the line allocates for ~80% of lines (qty 100-500).
- The box was heavily loaded (load average 13-30, other jobs' TTS and renders); regex p50 moved from ~740 ns
  (load 13) to ~1,720-1,770 ns (load 30) while its min stayed ~730; the other three were stable.
- Later sample at load average 49: regex p50 3,447 ns/line, min 741.
