# Pattern 08: dispatch the compiler cannot see through

**Rule:** fix the strategy type at build time (template, CRTP, or choose once at startup and run a specialised loop) so the call inlines; keep virtual/std::function for plugins, tests and once-per-tick calls.

## General version (LEFT)
```cpp
struct Quoter {          // pluggable strategy
  virtual ~Quoter() = default;
  virtual int quote(int mid) const = 0;
};
void quote_all(const Quoter& q, const Prices& mid,
               Prices& out) {
  for (int i = 0; i < kN; ++i)
    out[i] = q.quote(mid[i]);  // indirect call
}
struct Clamp : Quoter {
  int edge, lo, hi;
  Clamp(int e, int l, int h)
      : edge(e), lo(l), hi(h) {}
  int quote(int mid) const override {
    return std::clamp(mid - edge, lo, hi);
  }
};
// callback flavour
using QuoteFn = std::function<int(int)>;
```

## Hot-path version (RIGHT)
```cpp
struct Clamp {           // no base, no vtable
  int edge, lo, hi;
  int quote(int mid) const {
    return std::clamp(mid - edge, lo, hi);
  }
};
template <class Q>       // type fixed at build
void quote_all(Q q, const Prices& mid,
               Prices& out) {
  for (int i = 0; i < kN; ++i)
    out[i] = q.quote(mid[i]);  // inlined, SIMD
}
```

## Why the left is slower
- A virtual call is: load the vptr, load the slot, `call *%rax`, then `ret`. With one strategy the target never changes, so the indirect-branch predictor gets it right and the call itself costs only a few cycles.
- The real cost is lost inlining: across an opaque call the compiler must make one call per element, in order, keep values in callee-saved registers, and cannot constant-fold, hoist or vectorize.
- With the type known, `quote` inlines and g++ -O2 vectorizes the 64-price loop with SSE2 (4 x int32 per instruction; min/max emulated with compare + mask).
- g++ speculative devirtualization: when the only implementation is visible in the TU, g++ compares the loaded function pointer against `Clamp::quote` and runs an inlined guarded copy. That removes the call but keeps the per-element check, so it is still scalar: 0.85 ns vs 0.27 ns.
- `std::function` adds one more indirection (its invoker) and can never be speculated here: ~3 ns per call.
- When the work is a serial dependency chain (each quote feeds the next), nothing can vectorize and a predicted indirect call hides in the chain's latency: virtual and template measured the same within noise.

## Measured
| Metric (ns per quote) | General | Hot path (template) | Ratio |
| --- | --- | --- | --- |
| 64-price batch, std::function | 2.7-4.3 | 0.26-0.27 | ~10-16x |
| 64-price batch, virtual, strategy in another TU (no speculation) | 1.8-3.0 | 0.26-0.27 | ~7-11x |
| 64-price batch, virtual, g++ speculates | 0.82-0.85 | 0.26-0.27 | ~3.1x |
| serial chain (each quote feeds the next), virtual | 3.6-7.7 | 5.1-8.0 | no measurable difference |
| allocations | 0 | 0 | - |
| instructions (objdump) | quote_all: 26 (opaque) / 40 (speculative) + 9 in Clamp::quote | quote_all: 28 (vectorized, 4 per step) | - |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz, heavily loaded at the time), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`; 256 ticks x 64 instruments per pass, best of 15 passes, 5 runs per build; ranges are min-max over runs. Code, test, raw results: `/tmp/claude-0/vx/ai-08-dispatch/code/`.

## When the general version is fine
Plugins and strategies loaded at run time, test doubles, anything called once per tick around real work, and code where the per-call work is a serial dependency chain anyway. A monomorphic, predicted virtual call costs a nanosecond or two; it matters when it sits inside a tight loop whose body the compiler could otherwise inline and vectorize.

## Sources
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: virtuals "(and even simple branches) can be expensive"; resolve the type at compile time with templates. https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- David Gross, "When Nanoseconds Matter", CppCon 2024: "std::function may allocate"; prefer lambdas / inplace_function. https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- GCC docs, `-fdevirtualize-speculatively` and `-ftree-loop-vectorize` / `-fvect-cost-model` (very-cheap at -O2): https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
- cppreference: `std::function` https://en.cppreference.com/w/cpp/utility/functional/function , CRTP https://en.cppreference.com/w/cpp/language/crtp
- Related lab video: cpp-static-dispatch (vtables, final, variant).
