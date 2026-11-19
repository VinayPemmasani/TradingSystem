# Pattern 15: prices as integer ticks (fixed point)

**Rule:** integer ticks inside, decimal text only at the edges. Convert once at the feed boundary with the instrument's tick size; never compare, key, or sum money in `double`.

## General version (LEFT)
```cpp
struct Levels {
  double base;               // price of level 0
  std::vector<double> qty;   // one slot per tick
  double notional = 0;
};
constexpr double kTick = 0.01, kEps = 1e-9;
void apply(Levels& L, double px, double qty) {
  const double t = px / kTick;
  if (std::fabs(t - std::round(t)) > kEps)
    throw std::invalid_argument("off tick");
  const auto i = static_cast<std::size_t>(
      std::round((px - L.base) / kTick));
  L.qty[i] += qty;
  L.notional += px * qty;
}
```

## Hot-path version (RIGHT)
```cpp
// price in ticks of 0.01: 5012.25 -> 501225
using Ticks = int64_t;
struct Levels {
  Ticks base;                // price of level 0
  std::vector<int64_t> qty;  // one slot per tick
  int64_t notional = 0;      // ticks x qty, exact
};
// px: validated and converted once, at the edge
void apply(Levels& L, Ticks px, int64_t qty) {
  const auto i = std::size_t(px - L.base);
  L.qty[i] += qty;
  L.notional += px * qty;
}
```
The conversion from text to ticks is pattern 16 (a digit loop straight into `int64_t`, rejecting more than 2 decimals).

## Correctness (the main point) — measured with `demo.cpp`, g++ 13.3
| Expression | double | int64 ticks |
| --- | --- | --- |
| `0.1 + 0.2 == 0.3` | false (0.30000000000000004) | `10 + 20 == 30` true |
| `std::map` key: +100 @ 0.3, +50 @ 0.1+0.2 | 2 levels | 1 level, qty 150 |
| `100.00 + ten 0.01 steps == 100.10` | false (100.10000000000005) | true |
| `int64_t(0.29 / 0.01)` | 28 (0.29/0.01 = 28.999999999999996) | 29 |
| `std::round(1.005 * 100)` | 100, not 101 (1.005 is stored as 1.00499999999999989...) | no rounding: text "1.005" is 1005 ticks of 0.001, or rejected at a 0.01 tick |
| 1,000,000 fills of 3 lots @ 0.01 | 29999.9999996277 | 3,000,000 ticks = 30000.00 |
| benchmark notional after 335,872 updates | 84,539,714,399.649658 | 84,539,714,399.65 exactly (error $0.00034) |

## Why the left is slower
- Two `divsd` per update (division by 0.01 cannot be turned into an exact multiply); typically 13-15 cycles latency each on current x86.
- `std::round` (round half away from zero) has no single SSE instruction; g++ 13 at -O2 calls libm `round` twice per update, also with `-march=native`, and spills XMM registers around each call.
- Compiled loop: about 35 instructions per update including 2 calls, vs 10 for the integer loop (`sub`, `imul`, two adds to memory, loads, loop control).
- The off-tick check is most of the cost: without it the double version still needs one divide and one round call (4.5 ns).
- The floating-point notional is a 4-cycle-latency `addsd` chain; the integer one is a 1-cycle `add`.
- None of this is large per operation; the correctness issues are what make the double version wrong for prices.

## Measured
| Metric | General (double) | Hot path (int64 ticks) | Ratio |
| --- | --- | --- | --- |
| ns/update, p50 (min-max of 3 runs) | 13.2 (13.1-14.0) | 2.5 (2.52-2.55) | 5.2x |
| ns/update, double without the off-tick check | 4.5 (4.2-4.6) | 2.5 | 1.8x |
| instructions per update in the loop (objdump) | ~35 + 2 libm calls | 10 | ~3.5x |
| map levels for "0.3" and "0.1+0.2" | 2 | 1 | - |
| notional error after 335,872 updates | $0.00034 | 0 | - |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, pinned with `taskset` to the idlest core (load average 22-24 from other jobs). 8,192 updates into a 2,000-level book, 41 passes, p50; kernels `noinline` + `flatten` so `apply` is inlined into both. Test: 100 random books x 2000 updates give identical level quantities; an off-tick price throws. Code, demo, test, raw output, disassembly: `/tmp/claude-0/vx/ai-15-fixed-point/code/`.

## When the general version is fine
Analytics, risk, pricing models, signals, volatility and other statistics, where a relative error near 1e-16 is irrelevant and you never test prices for equality. Displaying prices. Not fine: matching, book keys, price comparisons, P&L and fee accounting, anything that must reconcile to the cent. Range check for ticks: `int64_t` holds about 9.2e18, so ticks x quantity sums need a worst-case check (or `__int128`) for very large notional. If a venue varies tick size by price band, use the smallest increment as the unit and keep the scale with the instrument.

## Sources
- cppreference, `std::round` (half away from zero) and floating-point types: https://en.cppreference.com/w/cpp/numeric/math/round , https://en.cppreference.com/w/cpp/language/types
- David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991): https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html
- Agner Fog, instruction tables (DIVSD latency per core): https://www.agner.org/optimize/instruction_tables.pdf
- Intel 64 and IA-32 Optimization Reference Manual: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- CME Group, tick sizes defined per contract in reference data (e.g. E-mini S&P 500 minimum tick 0.25 index points): https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.contractSpecs.html
- RESEARCH.md notes that none of the Gross/Cook/DE sources cover fixed point; present it as house practice backed by the measurements above.
