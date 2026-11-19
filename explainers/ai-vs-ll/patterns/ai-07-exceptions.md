# Pattern 07: exceptions for rejected orders

**Rule:** throw for the exceptional; return codes for the expected. At a gateway, rejects are expected traffic: return a reject code, mark the reject branch `[[unlikely]]`, and keep the reject handling cold and out of line.

## General version (LEFT)
```cpp
void Gateway::validate(const Order& o) const {
  if (o.qty <= 0 || o.qty > lim_.max_qty)
    throw std::runtime_error(
        "bad qty " + std::to_string(o.qty));
  if (o.px < lim_.px_lo || o.px > lim_.px_hi)
    throw std::runtime_error(
        "px outside band " + std::to_string(o.px));
}
bool Gateway::on_order(const Order& o) {
  try { validate(o); }
  catch (const std::exception& e) {
    out_.reject(o, e.what()); return false;
  }
  out_.send(o);
  return true;
}
```

## Hot-path version (RIGHT)
```cpp
enum class Rej : std::uint8_t { None, Qty, Px };
// in struct Gateway:  [[gnu::cold, gnu::noinline]] void reject(const Order& o, Rej r);
inline Rej Gateway::check(const Order& o) const {
  if (o.qty <= 0 || o.qty > lim_.max_qty)
    [[unlikely]] return Rej::Qty;
  if (o.px < lim_.px_lo || o.px > lim_.px_hi)
    [[unlikely]] return Rej::Px;
  return Rej::None;
}
bool Gateway::on_order(const Order& o) {
  if (Rej r = check(o); r != Rej::None)
    [[unlikely]] { reject(o, r); return false; }
  out_.send(o);
  return true;
}
void Gateway::reject(const Order& o, Rej r) {
  char buf[64];
  int n = r == Rej::Qty ? std::snprintf(buf, sizeof buf, "bad qty %d", o.qty)
                        : std::snprintf(buf, sizeof buf, "px outside band %lld", (long long)o.px);
  out_.reject(o, std::string_view(buf, std::size_t(n)));
}
```

## Why the left is slower (on the reject path)
- Table-based ("zero-cost") EH: when nothing throws, the try/catch adds no instructions to the happy path; the unwind information lives in `.eh_frame` / `.gcc_except_table`. g++ also moves the throw sites into `.text.unlikely` by itself. So the happy path is near-equal (3.2 vs 2.7 ns/order measured).
- A throw is a slow, general mechanism: build the message (`std::to_string` + `operator+`), `std::runtime_error` copies it into a heap-allocated string, `__cxa_allocate_exception` mallocs the exception object, then `_Unwind_RaiseException` runs a two-phase unwind (phase 1 searches frames via the unwind tables and the personality routine for a matching handler; phase 2 walks them again running cleanups) before landing in the catch.
- Measured: about 1.5 us per rejected order (Cook quotes "at least 1.5us" for exceptions used as control flow), with 1.5 `operator new` calls per reject on top of the malloc'd exception object.
- At a 1% reject rate the general version's p99 is set entirely by rejects: 1.4 us vs 61 ns.
- Code: hot instructions `ai::on_order` (19) + `ai::validate` (30, not inlined) = 49 vs 28 for `fast::on_order`, whose accept path is 16 instructions from entry to `ret` with no call. Cold code: 113 instructions + `to_string`/`operator+` helpers vs a 44-instruction cold `reject`.
- C++23 `std::expected<T, E>` is the standard vocabulary type for the same idea.

## Measured
| Metric | General (throw/catch) | Hot path (reject code) | Ratio |
| --- | --- | --- | --- |
| 0% rejects, ns/order (whole loop) | 3.2 (3.0-3.6) | 2.7 (2.7-2.7) | 1.2x |
| 0% rejects, p50 per call (timer-limited) | 4.8 | 2.9 | - |
| 1% rejects, ns/order (whole loop) | 40 (30-50) | 2.9 (2.9-2.9) | 14x |
| 1% rejects, p99 per order | 1,391 ns (1,388-1,398) | 61 ns (60-99) | 23x |
| one reject, p50 | 1,503 ns (1,502-1,526) | 69 ns (66-127) | 22x |
| one reject, p99 | 4,777 ns | 269 ns | 18x |
| allocations per reject | 1.5 operator new + exception object (malloc) | 0 | - |
| hot instructions (objdump) | 49 | 28 (accept path 16) | 1.75x |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`. 400k orders, rejects half bad-qty and half bad-price; 50k warm-up orders (with rejects) so the unwinder caches are warm. Per-order rdtscp timing (overhead subtracted) for percentiles; "whole loop" is the full 400k loop timed without per-call timers, best of 7. Median of 5 runs (min-max). The reject path of the hot version includes `snprintf` of the same reason text. Code, test, raw results: `/tmp/claude-0/vx/ai-07-exceptions/code/`.

## When the general version is fine
Truly exceptional failures: a lost exchange session, a corrupt config at startup, a broken invariant, out of memory. Exceptions keep that code clean and cannot be silently ignored, and on the happy path they cost close to nothing. They are the wrong tool only when the "error" is routine traffic on the hot path.

## Sources
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: exceptions are "zero cost if they don't throw"; used for control flow they cost "at least 1.5us". https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- David Gross, "When Nanoseconds Matter", CppCon 2024: keep error handling out of line, in a cold path. https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- Itanium C++ ABI: Exception Handling (two-phase unwind, `__cxa_allocate_exception`, `__cxa_throw`): https://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html
- cppreference: `[[likely]]/[[unlikely]]` https://en.cppreference.com/w/cpp/language/attributes/likely , `std::expected` https://en.cppreference.com/w/cpp/utility/expected
- GCC function attributes `cold`, `noinline`: https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html
