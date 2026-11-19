# Pattern 13: branches on market data

**Rule:** branchless for unpredictable data, out of line for rare paths, and let a measurement on recorded data decide; on predictable data the branchy loop can win.

## General version (LEFT)
```cpp
Stats scan(const std::vector<Tick>& v, int big) {
  Stats s;
  for (const Tick& t : v) {
    if (t.qty <= 0) {
      std::fprintf(stderr, "bad qty %d\n", t.qty);
      ++s.bad; continue;
    }
    if (t.side == Side::Buy) {
      s.buy_vol += t.qty;
      if (t.qty >= big) ++s.big_buys;
    } else {
      s.sell_vol += t.qty;
      if (t.qty >= big) ++s.big_sells;
    }
  }
  return s; }
```

## Hot-path version (RIGHT)
```cpp
[[gnu::cold, gnu::noinline]]
void on_bad(const Tick& t);  // logs; never inlined
Stats scan(const Tick* t, size_t n, int64_t big) {
  int64_t vol = 0, sv = 0, nb = 0, sb = 0, bad = 0;
  for (size_t i = 0; i < n; ++i) {
    const int64_t q = t[i].qty;
    if (q <= 0) [[unlikely]] {
      on_bad(t[i]); ++bad; continue; }
    const int64_t sell = -int64_t(t[i].side);
    const int64_t b = q >= big;
    vol += q;   sv += q & sell;
    nb  += b;   sb += b & sell;
  }
  return {vol - sv, sv, nb - sb, sb, bad};
}
```
`Tick` is `{int64_t px; int32_t qty; Side side;}` (16 bytes), `Side` is a `uint8_t` enum with Buy = 0, Sell = 1.

## Why the left is slower (on unpredictable data)
- The loop has two data-dependent conditional jumps per tick (side, then size vs threshold; confirmed in `objdump`). With a random aggressor side the predictor is wrong about half the time on the side jump.
- Each mispredict discards the speculatively executed work and refetches: typically 15-20 cycles on current x86 cores. Measured here: about 6 ns/tick extra on random input.
- Quieter cost: the totals live in the returned struct (caller memory, via the hidden return pointer) and the inline error path calls `fprintf`, which g++ must treat as opaque. So g++ keeps the four totals in memory: every update is a read-modify-write (`add %rax,0x0(%rbp)`), creating store-to-load chains. That alone makes the left 2.1 ns/tick even on perfectly predictable data.
- The right side turns decisions into values: side becomes a 0 / all-ones mask, size-over-threshold becomes 0/1 (`setle`), and every tick does the same adds. Buy totals are recovered at the end as total minus sell. 15 instructions per tick, no data-dependent jump.
- The rare path stays a branch, marked `[[unlikely]]`, and its body moves to a `[[gnu::cold, gnu::noinline]]` function (placed in `.text.unlikely`), so the hot loop keeps its accumulators in registers and its code compact.
- Branchless is not free: it always executes all the work. When the branch is predictable, the branchy loop executes fewer instructions and wins (see the table).
- A lookup table indexed by side (`vol[side] += q`) avoids the jump but chains each add through a store and a reload when the same side repeats; it was the slowest on long runs.

## Measured
ns/tick, p50 of 101 passes, median of 3 runs (min of runs in brackets where it matters).

| Input | General (LEFT) | Branchless (RIGHT) | Branches + cold path | Lookup table | General / RIGHT |
| --- | --- | --- | --- | --- | --- |
| random side, 50% big | 7.2 (6.6 min) | 1.04 | 4.9 | 1.33 | 6.9x |
| side repeats 80%, 10% big | 2.4 | 1.04 | 2.1 | 1.5 | 2.3x |
| sides in runs of 256, 1% big | 2.1 | 1.00 | **0.77** | 2.3 | 2.1x (but branchy+cold beats RIGHT by 1.3x) |

| Bloat metric | General | Hot path |
| --- | --- | --- |
| data-dependent conditional jumps per tick | 2 | 0 |
| hot-loop instructions per tick (objdump) | 10-11 executed, 4 of them memory RMW | 15, all register |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz, L1d 48 KiB, L2 2 MiB), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, pinned with `taskset` to the idlest core. 16,384 ticks (256 KiB, L2-resident) per pass; each kernel behind a `noinline` wrapper so the timed code is what `objdump` shows. Test: 500 random batches including bad ticks, all four variants return identical results. Caveat: branchy loops are sensitive to code layout; an inlined build measured the branchy+cold loop at 1.5 ns/tick on the predictable input. Code, test, raw output, disassembly: `/tmp/claude-0/vx/ai-13-branchless/code/`.

## When the general version is fine
Startup, config parsing, tooling, reports, and any loop that is not on the latency path. Also on hot paths whose branches are genuinely predictable: there, keep the branches, just move the rare path out of line and keep accumulators local. Real order flow sits between the cases above (aggressor side is autocorrelated), so measure with recorded data before rewriting, and read the assembly: g++ often emits `setcc`/`cmov` for simple conditional adds on its own.

## Sources
- David Gross, "When Nanoseconds Matter", CppCon 2024 (branchless binary search, CMOV; error handling out of line): https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (branches can be expensive; keep error handling out of the hot path): https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- cppreference, `[[likely]]` / `[[unlikely]]` (C++20): https://en.cppreference.com/w/cpp/language/attributes/likely
- GCC function attributes, `cold` and `noinline`: https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html
- Intel 64 and IA-32 Architectures Optimization Reference Manual (branch prediction, misprediction cost): https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- Agner Fog, "The microarchitecture of Intel, AMD and VIA CPUs" (misprediction penalties per core): https://www.agner.org/optimize/microarchitecture.pdf
