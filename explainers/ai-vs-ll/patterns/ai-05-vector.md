# Pattern 05: a fresh vector every tick

**Rule:** size the buffer once (bounded capacity), reuse it every tick; never return a fresh `std::vector` from a hot function.

## General version (LEFT)
```cpp
// Each tick: the levels priced inside [lo, hi]
std::vector<Level> levels_in_band(const Book& b,
                                  Px lo, Px hi) {
  std::vector<Level> out;
  for (int i = 0; i < b.depth; ++i) {
    const Level& l = b.levels[i];
    if (l.px >= lo && l.px <= hi)
      out.push_back(l);
  }
  return out;
}
```

## Hot-path version (RIGHT)
```cpp
struct Band {                      // caller owns it
  std::array<Level, kMaxDepth> v;  // depth <= 32
  int n = 0;
};
inline void levels_in_band(const Book& b, Px lo,
                           Px hi, Band& out) {
  int n = 0;
  for (int i = 0; i < b.depth; ++i) {
    const Level& l = b.levels[i];
    if (l.px >= lo && l.px <= hi)
      out.v[n++] = l;   // n <= depth <= 32
  }
  out.n = n;
}
```
Alternative with the same cost: a `std::vector<Level>` that is `reserve(kMaxDepth)`-ed once at startup and `clear()`-ed per tick (clear keeps capacity).

## Why the left is slower
- Without `reserve`, libstdc++ grows capacity by doubling (1, 2, 4, 8, 16, ...). Each growth is a `malloc` of the new block, a copy of every existing element, and a `free` of the old block.
- A band of 14 levels costs 5 mallocs, 4 frees and 15 element copies inside the call, plus one more `free` when the caller drops the returned vector. Averaged over the benchmark's 4-24 level bands: 5.08 allocations per call.
- glibc's per-thread cache (tcache) makes each small malloc/free cheap when it hits: the measured gap works out to about 18 ns per growth step. But the cost is not fixed: a tcache miss goes to an arena (with a lock), and a growing heap means `brk`/`mmap` system calls and first-touch page faults, which show up in p99/p99.9.
- Each new block is fresh memory, so the copies touch new cache lines every tick instead of the same 512 bytes that stay in L1.
- Code bloat: the general function compiles to 136 instructions (with the inlined `_M_realloc_insert` growth path) plus a cold clone, vs 29 for the hot-path one.
- The hot-path version relies on a stated constraint: book depth <= 32, so the result can never exceed 32 and `out.v[n++]` needs no overflow branch.

## Measured
| Metric | General (fresh vector) | Hot path (array + size) | Ratio |
| --- | --- | --- | --- |
| allocations per call | 5.08 | 0 | - |
| p50 ns/call | 144 (142-187) | 53 (48-74) | 2.7x |
| p99 ns/call | 257 (196-293) | 84 (76-114) | 3.1x |
| p99.9 ns/call | 420 (340-495) | 102 (91-164) | 4.1x |
| instructions in function (objdump) | 136 (+8 cold) | 29 | 4.7x |
| reserved vector + clear (p50 / p99) | - | 51 / 84 | - |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`. 400k calls per variant, each timed with rdtscp (timer overhead subtracted), book of 32 levels, random band 4-24 levels wide per tick; timed region includes building, summing and (LEFT) freeing the result. Allocations counted by a replaced global `operator new`. Median of 5 runs, (min-max) in brackets. Code, test and raw results: `/tmp/claude-0/vx/ai-05-vector/code/`.

## When the general version is fine
Startup, config loading, tools and tests, cold paths, or any place where the size is genuinely unbounded and the call is rare. There, returning a vector by value is clearer and the allocator cost is invisible.

## Sources
- cppreference, `std::vector::push_back` (reallocation, amortized constant) and `std::vector::clear` (capacity unchanged): https://en.cppreference.com/w/cpp/container/vector/push_back , https://en.cppreference.com/w/cpp/container/vector/clear
- glibc malloc internals (tcache, arenas): https://sourceware.org/glibc/wiki/MallocInternals
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: "Allocations are costly", use a pool of preallocated objects. Slides: https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- David Gross, "When Nanoseconds Matter: Ultrafast Trading Systems in C++", CppCon 2024 ("Most of the time, you don't want node containers"). Slides: https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- "From NIC to p99": pre-allocate at startup, avoid dynamic containers on the hot path. https://deepengineering.substack.com/p/from-nic-to-p99-engineering-low-latency
