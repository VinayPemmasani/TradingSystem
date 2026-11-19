# Pattern 11: Memory order (seq_cst everywhere vs acquire/release)

**Rule:** on x86 a seq_cst store is a full barrier (`xchg`). When each index has one writer and you only pass
messages, publish with release and read with acquire.

## General version (ai.hpp, RingSeq)

```cpp
bool try_push(const T& v) {
  size_t h = head_.load();                 // seq_cst
  if (h - cached_tail_ == N) {
    cached_tail_ = tail_.load();           // seq_cst
    if (h - cached_tail_ == N) return false;
  }
  buf_[h & (N - 1)] = v;
  head_.store(h + 1);                      // seq_cst store: xchg on x86
  return true;
}
// try_pop: same shape, ends in tail_.store(t + 1)
```

## Hot-path version (fast.hpp, RingAR)

```cpp
bool try_push(const T& v) {
  size_t h = head_.load(relaxed);          // we own head_
  if (h - cached_tail_ == N) {
    cached_tail_ = tail_.load(acquire);    // pairs with pop's release
    if (h - cached_tail_ == N) return false;
  }
  buf_[h & (N - 1)] = v;
  head_.store(h + 1, release);             // slot write happens-before the consumer's read
  return true;
}
// try_pop: tail_ relaxed, head_ acquire, tail_.store(t + 1, release)
```

Generated code (g++ 13.3 -O2 -S; identical except one instruction):

```asm
# RingSeq::try_push                      # RingAR::try_push
movaps %xmm0, 128(%rdx,%rdi)  # slot     movaps %xmm0, 128(%rdx,%rdi)
xchgq  (%rdi), %rax           # head_    movq   %rax, (%rdi)
```

## Why the general version is slower (machine level)

- x86-TSO keeps load-load, store-store and load-store order; the only reordering is a later load passing an
  earlier store that is still in the core's store buffer. seq_cst has to forbid exactly that.
- So seq_cst loads are plain `mov` (same as acquire and relaxed), and the cost lands on stores: GCC and clang emit
  `xchg`, which has an implicit `lock` prefix and acts as a full barrier: the store buffer must drain before
  the core continues.
- A release store is a plain `mov` that retires into the store buffer, and the core keeps going.
- In the two-thread ring the slot store usually misses (the line was last read by the other core), so the
  `xchg` waits for that RFO round trip each message; that is where 48 -> 164 ns/msg comes from.
- Release/acquire are not "nothing": they forbid the compiler from sinking the slot write below the release
  store or hoisting the slot read above the acquire load. Relaxed would allow that, and would be a bug here.
- On AArch64 (clang 18), release and seq_cst stores are both `stlr` and acquire/seq_cst loads `ldar`
  (`ldapr` for acquire with -march=armv8.3-a); relaxed is `str`/`ldr`. The seq_cst-vs-release gap is an x86 story.

## Measured (shared 4-vCPU cloud VM, Xeon @ 2.10 GHz, g++ 13.3 -O2 -std=c++20, chrt -f 10, pinned)

Median of 5 runs (min-max). The VM was loaded by other jobs.

| Metric | General (seq_cst) | Hot path (acq/rel) | Ratio |
| --- | --- | --- | --- |
| one-thread publish loop (write 16 B slot + publish index), ns/op, 100M | 11.6 (11.58-11.83) | 2.53 (2.49-3.07) | 4.6x |
| two-thread ring, 20M 16 B msgs, ns/msg | 164 (45.6-168) | 48.1 (45.3-51.2) | 3.4x |
| index store instruction | `xchgq` | `movq` | |
| instructions in try_push / try_pop | 22 / 19 | 22 / 18 | |

The seq_cst two-thread result was bimodal: four runs at 161-168 ns, one at 45.6 ns (as fast as acq/rel), so the
gap depends on how the two threads' timing lines up. Both rings deliver the same 2M values in order (test.cpp, PASS).
Method, asm and raw runs: `/tmp/claude-0/vx/ai-11-memory-order/code/` (README.md, asm.s, arm.s, runs.txt).

## When the general version is fine

When you are not sure which ordering a protocol needs; on cold paths; and in protocols that need a single total
order across several variables, such as Dekker/Peterson-style flags ("store mine, then load yours"), where
acquire/release is not enough. seq_cst loads cost nothing extra on x86, so the default is harmless for readers.

## Sources

- cppreference, `std::memory_order`: https://en.cppreference.com/w/cpp/atomic/memory_order
- C/C++11 mappings to processors (x86 seq_cst store = xchg or mov+mfence; ARMv8 stlr/ldar):
  https://www.cl.cam.ac.uk/~pes20/cpp/cpp0xmappings.html
- P. Sewell et al., "x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors", CACM 2010:
  https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf
- Intel 64 and IA-32 Architectures Software Developer's Manual, Vol. 3A, chapter "Multiple-Processor Management", section "Memory Ordering" (locked
  instructions, XCHG implicit lock)
- David Gross, "When Nanoseconds Matter", CppCon 2024 (https://github.com/CppCon/CppCon2024)
