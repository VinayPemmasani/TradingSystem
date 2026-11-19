# Pattern 16: parsing a price/qty text feed

**Rule:** parse the bytes you were promised, straight into the type you will use: no allocation, no locale, integer ticks, reject anything off spec, errors as values.

## General version (LEFT)
```cpp
struct Quote {
  std::string sym; double px; int qty; };
// "ESZ6,5012.25,17" -> {"ESZ6", 5012.25, 17}
Quote parse(const std::string& line) {
  std::stringstream ss(line);
  std::string sym, px, qty;
  std::getline(ss, sym, ',');
  std::getline(ss, px, ',');
  std::getline(ss, qty, ',');
  return {sym, std::stod(px), std::stoi(qty)};
}
```
The other common general answer, also measured:
```cpp
static const std::regex re(
    R"(([A-Z0-9]+),(\d+(?:\.\d{1,2})?),(-?\d+))");
std::smatch m;
if (!std::regex_match(line, m, re)) throw ...;
return {m[1].str(), std::stod(m[2].str()),
        std::stoi(m[3].str())};
```

## Hot-path version (RIGHT)
```cpp
bool parse(std::string_view s, Quote& q) {
  const char *p = s.data(), *e = p + s.size();
  const char* c = std::find(p, e, ',');
  const char* f = std::find(c + (c < e), e, ',');
  if (f == e || f-c < 2 || f-c > 17) return false;
  q.sym = std::string_view(p, c - p);
  int64_t t = 0; int nf = -1;   // nf: decimals
  for (++c; c < f; ++c) {
    if (*c == '.' && nf < 0) { nf = 0; continue; }
    const unsigned d = unsigned(*c - '0');
    if (d > 9 || nf == 2) return false;
    t = t * 10 + d; nf += nf >= 0;
  }
  q.px = t * (nf <= 0 ? 100 : nf == 1 ? 10 : 1);
  auto [r, ec] = std::from_chars(f + 1, e, q.qty);
  return ec == std::errc{} && r == e; }
```
Here `Quote` is `{ std::string_view sym; int64_t px; /* ticks of 0.01 */ int64_t qty; }`; the symbol view points into the receive buffer, so the buffer must outlive it. The 16-char price limit keeps `t * 100` far below `INT64_MAX`.

## Why the left is slower
- `std::stringstream` construction sets up a `basic_stringbuf` and `basic_ios`, each holding a copy of the global `std::locale` (atomic reference counts), then copies the line into its own `std::string`.
- That copy allocates when the line exceeds libstdc++'s 15-character small-string buffer: 0.80 allocations per line on this feed (lines of 14-16 chars).
- `getline` copies each field into a `std::string`; `std::stod` calls `strtod`, which follows the C locale's decimal point and also handles exponents, hex floats, inf/nan and leading spaces: generality the feed spec never uses.
- Errors are exceptions (`std::invalid_argument`), which cost microseconds when thrown on the hot thread.
- `std::regex_match` in libstdc++ runs a backtracking executor and allocated 3.00 times per line here; it was also the most sensitive to box load.
- The result is a `double`, so the problems of pattern 15 start at the parser.
- Right side: two `std::find` calls, one digit loop that produces ticks directly, `std::from_chars` (no locale, no allocation, no exceptions), zero copies.

## Measured
| Metric | General (stringstream) | std::regex | from_chars, double px | Hot path | General / hot |
| --- | --- | --- | --- | --- | --- |
| ns/line, p50 (range of 3 runs) | 301 (294-306) | 736 at load 13; 1,720-1,770 at load 30; 3,450 at load 49 (best 730-740 throughout) | 27.4 (26.4-28.0) | 19.2 (19.2-19.5) | 15.7x |
| ns/field (3 fields per line) | 100 | 245-1,150 | 9.1 | 6.4 | 15.7x |
| heap allocations per line | 0.80 | 3.00 | 0 | 0 | - |
| CPU at 1 M lines/s | ~30% of a core | 74-345% (more than one core) | ~2.7% | ~1.9% | - |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), g++ 13.3 / libstdc++ `-O2 -std=c++20 -Wall -Wextra`, pinned with `taskset` to the idlest core; the box was heavily loaded by other jobs (load average 13-30). 4,096 lines like `ESZ6,5083.42,229`, 31 passes, p50 per line; allocations counted with a replaced global `operator new`. Test: 200,000 random lines, all versions agree (hot `px` equals the exact tick value); malformed lines rejected by both; off-spec lines (`5012.255`, `5.0e3`, leading space) rejected by the hot parser only. Code, test, raw output: `/tmp/claude-0/vx/ai-16-parsing/code/`. Related, earlier video: `cpp-price-parse` (single price field, stod/strtod/stringstream vs digit loop / from_chars / SWAR).

## When the general version is fine
Config files, command-line arguments, CSV reports, test fixtures, admin tools: rare, varied, human-written input where a good error message matters more than nanoseconds, and where accepting `1e3` or a leading space is a feature. On a feed handler the format is fixed by the venue specification, so state those constraints (no allocation, integer ticks, reject off-spec, errors as values) and the parser becomes small and fast.

## Sources
- cppreference, `std::from_chars` (locale-independent, non-allocating, non-throwing): https://en.cppreference.com/w/cpp/utility/from_chars
- cppreference, `std::stod` (calls `std::strtod`) and `std::strtod` (locale, exponents, hex, inf/nan): https://en.cppreference.com/w/cpp/string/basic_string/stof , https://en.cppreference.com/w/cpp/string/byte/strtof
- cppreference, `std::basic_stringstream` and `std::regex_match`: https://en.cppreference.com/w/cpp/io/basic_stringstream , https://en.cppreference.com/w/cpp/regex/regex_match
- David Gross, "When Nanoseconds Matter", CppCon 2024 (zero copy: work directly on the buffer): https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (no allocation and no exceptions on the hot path): https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- RESEARCH.md notes that parsing beyond zero copy is not covered by the Gross/Cook/DE sources; the rest is house practice backed by the measurements above.
