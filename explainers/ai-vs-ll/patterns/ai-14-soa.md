# Pattern 14: hot fields, cold fields (struct of arrays)

**Rule:** lay data out by how the hot loop reads it, not by what it is called: split the scanned fields into their own arrays (or a small hot struct) and keep the rest in a cold store at the same index.

## General version (LEFT)
```cpp
struct Order {                       // 112 bytes
  std::string symbol, account;       // 2 x 32
  uint64_t id;
  sys_clock::time_point created, updated;
  double price; int64_t qty;
  Side side; bool active, ioc, post_only;
};
int64_t bid_depth(const std::vector<Order>& book,
                  double px) {
  int64_t total = 0;
  for (const Order& o : book)
    if (o.active && o.side == Side::Buy &&
        o.price >= px) total += o.qty;
  return total;
}
```
(`sys_clock` = `std::chrono::system_clock`; `Side` is a `uint8_t` enum.)

## Hot-path version (RIGHT)
```cpp
// hot fields: one array each.
// cold fields live elsewhere, same index.
struct BookHot {
  std::vector<double>   px;
  std::vector<int64_t>  qty;
  std::vector<uint8_t>  live_bid;  // active && Buy
};
int64_t bid_depth(const BookHot& b, double px) {
  int64_t total = 0;
  for (size_t i = 0; i < b.px.size(); ++i) {
    const int64_t take =
        b.live_bid[i] & (b.px[i] >= px);
    total += b.qty[i] & -take;   // 0 or all ones
  }
  return total;
}
```
Middle option measured too: a 24-byte `struct OrderHot { double px; int64_t qty; uint8_t live_bid; }` in its own vector (hot/cold split).

## Why the left is slower
- The scan needs 18 bytes per order (price 8, qty 8, side 1, active 1) out of 112 (`offsetof`: price at 88, qty 96, side 104, active 105).
- The core moves whole 64-byte cache lines. With a 112-byte stride the hot bytes of 4 orders fall in 5 of the 7 lines they span: 80 bytes of lines read per order, and the sequential prefetcher streams the remaining lines too.
- 1 M orders = 117 MB per scan, far beyond the 2 MiB L2. Measured, the fat-struct scan runs at the same speed at 1 M as at 8 M orders (DRAM-like), while the 18 MB of hot arrays at 1 M run 3.7x faster than at 8 M: they stay in cache, the structs do not.
- Cold bytes (strings, timestamps, unused flags) occupy cache and bandwidth that the next lines need.
- The branchy filter adds mispredicts on a random book; giving the fat struct the same branchless body (variant measured) only moves it from 24 to 17 ns/order, so the layout is the main cost.
- Right side: 17 bytes per order, all used; the filter is a mask (`qty & -take`), with no data-dependent jump. Note: written as `take ? qty : 0`, g++ 13 emitted a branch again; check the assembly.
- Bookkeeping cost: `live_bid` (a precomputed hot predicate) must be updated on every fill, cancel and state change; all arrays share one index.

## Measured
ns per order, p50 of 21 scans, median of 5 runs (range of the 5 p50s in brackets).

| Metric | General (AoS, branchy) | AoS, branchless body | Hot/cold split (24 B) | Hot path (SoA) | General / SoA |
| --- | --- | --- | --- | --- | --- |
| bytes per order in memory | 112 | 112 | 24 | 17 | 6.6x |
| bytes of cache lines the loop reads per order | 80 (+ prefetched rest) | 80 | 24 | 17 | 4.7-6.6x |
| 1 M orders (117 MB vs 18 MB), ns/order | 24.3 (18.5-24.7) | 17.0 (14.4-20.3) | 1.13 (1.07-1.15) | 0.77 (0.76-0.77) | 32x |
| 8 M orders (940 MB vs 143 MB), ns/order | 23.6 (19.1-27.7) | 20.6 (16.2-21.6) | 5.97 (4.7-6.5) | 2.83 (1.95-3.08) | 8.3x (7.3x vs branchless AoS) |

Method: measured on a shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz, L1d 48 KiB, L2 2 MiB, L3 260 MiB shared), g++ 13.3 `-O2 -std=c++20 -Wall -Wextra`, each run pinned with `taskset` to the idlest core; the box was heavily loaded by other jobs (load average 14-17), which mostly widens the AoS ranges. Random book: price 5000.00-5099.75 in 0.25 steps, 90% active, side 50/50, query at 5050.00. Test: 300 random books, all four kernels agree. Code, test, raw output: `/tmp/claude-0/vx/ai-14-soa/code/`.

## When the general version is fine
Whenever the code touches the whole order: new order, amend, fill report, audit, persistence, the UI, and any per-order (not per-scan) work. One rich struct is simpler and keeps invariants in one place. Small books that fit in L1/L2 shrink the gap too. Split only the fields a hot loop scans across many records, and keep a single index authoritative.

## Sources
- Carl Cook, "When a Microsecond Is an Eternity", CppCon 2017 (keep data that is used together in as few cache lines as possible; don't trample the cache): https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
- "From NIC to p99": prefetch and cache-align structs: https://deepengineering.substack.com/p/from-nic-to-p99-engineering-low-latency
- David Gross, "When Nanoseconds Matter", CppCon 2024 (understand the problem by looking at data; containers and layout): https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf
- Intel 64 and IA-32 Architectures Optimization Reference Manual (cache lines, hardware prefetchers): https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- Ulrich Drepper, "What Every Programmer Should Know About Memory" (2007): https://people.freebsd.org/~lstewart/articles/cpumemory.pdf
