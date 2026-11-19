# Pattern 06: copies you did not ask for

**Rule:** on the hot path, borrow (`const&`, `std::string_view`, `std::span`) and format into memory you already own; pass by value only when the callee keeps the copy.

## General version (LEFT)
```cpp
std::int32_t limit_for(std::string sym,
                       const Limits& lim);
std::string make_tag(Order o) {
  return o.account + "-" + o.symbol + "-" +
         std::to_string(o.qty) + "@" +
         std::to_string(o.px);
}
bool on_order(Order o, const Limits& lim,
              std::string& tag) {
  if (o.qty > limit_for(o.symbol, lim))
    return false;
  tag = make_tag(o);
  return true;
}
```

## Hot-path version (RIGHT)
```cpp
std::int32_t limit_for(std::string_view sym, const Limits& lim);
char* put(char* p, std::string_view s) {
  return std::copy(s.begin(), s.end(), p);
}
struct Tag { std::array<char, 64> b; int n = 0; };
bool on_order(const Order& o, const Limits& lim,
              Tag& tag) {
  if (o.qty > limit_for(o.symbol, lim))
    return false;
  char* p = tag.b.data(); char* e = p + 64;
  p = put(p, o.account); *p++ = '-';
  p = put(p, o.symbol);  *p++ = '-';
  p = std::to_chars(p, e, o.qty).ptr; *p++ = '@';
  p = std::to_chars(p, e, o.px).ptr;
  tag.n = int(p - tag.b.data());
  return true;
}
// Constraint, checked at order entry: account <= 16 chars, symbol <= 8 chars -> at most 58 of 64 bytes used.
```

## Why the left is slower
- `on_order(Order o)` copies the whole 104-byte `Order` per message; `make_tag(Order o)` copies it again for every accepted order. Short strings (<= 15 chars) are stored inline (SSO), so they copy without allocating, but the `std::vector<Fill>` inside the order owns heap memory: each copy is a `malloc` + element copy, and each destructor a `free`.
- `limit_for(std::string sym)` copies the symbol (inline here, but still a copy and a destructor).
- `a + "-" + b + ...` builds temporaries; the ~30-char tag exceeds the 15-char SSO buffer, so it allocates, and sometimes reallocates as it grows past capacity 30. `tag = make_tag(o)` then frees the caller's previous buffer.
- Average: 2.3 `operator new` calls per message (1 for the on_order copy, 0.62 for the make_tag copy, ~0.7 for the tag string).
- Code bloat: `ai::on_order` + `ai::make_tag` compile to 307 + 769 instructions (plus cold clones and shared `operator+`/`to_string` helpers) vs 220 for `fast::on_order`.
- The fix keeps the same data structures: `const Order&` (no copy), `std::string_view` (pointer + length, no copy), `std::to_chars` (writes digits in place, never allocates, no locale), and a 64-byte caller-owned buffer sized from stated bounds.

## Measured
| Metric | General (by value + operator+) | const& + operator+ | Hot path (const& + to_chars) | Ratio general/hot |
| --- | --- | --- | --- | --- |
| allocations per message | 2.3 | 0.7 | 0 | - |
| p50 ns/message | 162 (158-163) | 102 (98-103) | 52 (50-65) | 3.1x |
| p99 ns/message | 248 (245-303) | 183 (169-196) | 100 (98-138) | 2.5x |
| p99.9 ns/message | 433 (430-538) | 303 (273-333) | 152 (138-246) | 2.8x |
| instructions (objdump) | 1,076 (on_order + make_tag) | - | 220 | 4.9x |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, `taskset -c 3`; 400k orders per variant, each timed with rdtscp (overhead subtracted); allocations via a replaced global `operator new`; median of 5 runs, (min-max). Code, test, raw results: `/tmp/claude-0/vx/ai-06-copies/code/`.

## When the general version is fine
Pass by value is the right signature when the callee stores the object (sink arguments: take by value, then `std::move`). `std::string` is right when the text must outlive the call (a log record handed to another thread, a config value). Startup, admin and tooling code can use `operator+` freely.

## Sources
- cppreference: `std::basic_string_view` (https://en.cppreference.com/w/cpp/string/basic_string_view), `std::span` (https://en.cppreference.com/w/cpp/container/span), `std::to_chars` (https://en.cppreference.com/w/cpp/utility/to_chars: non-allocating, locale-independent).
- Tran et al., "Characterizing the Quality Profile of AI-Generated C++ in Production", arXiv 2608.06640 (2026): Copy & Allocation Overhead findings rate ratio 1.39 AI vs human, half of it `runtime-missing-move`; observational. https://arxiv.org/abs/2608.06640
- David Gross, "When Nanoseconds Matter", CppCon 2024: zero copy, serialise directly into the queue buffer. https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017: "Allocations are costly". https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
