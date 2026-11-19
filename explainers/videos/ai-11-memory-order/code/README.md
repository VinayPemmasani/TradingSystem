# ai-11-memory-order: how it was measured

ai.hpp: RingSeq = SPSC ring with default (seq_cst) atomic loads/stores everywhere.
fast.hpp: RingAR = identical ring, relaxed load of own index, acquire load of the other side's, release store.
asm: g++ 13.3 -O2 -std=c++20 -S asm.cpp -> asm.s. The ONLY difference in try_push and try_pop is the index
store: `xchgq %rax,(%rdi)` (seq_cst) vs `movq %rax,(%rdi)` (release). seq_cst and acquire loads are both plain movq.
arm.c / arm.s: clang 18 --target=aarch64-linux-gnu -O2: seq_cst and release stores are both `stlr`, seq_cst and
acquire loads both `ldar` (with -march=armv8.3-a the acquire load becomes `ldapr`); relaxed = plain str/ldr.
x86 (clang): seq_cst store xchgq, release/relaxed store movq, all loads movq.

test.cpp: 2M values through each ring (16 slots) on two threads: same order, same hash -> PASS.

bench.cpp, run as: chrt -f 10 ./bench 100000000 20000000 5   (runs.txt)
 (1) publish loop, one thread pinned to CPU 0: write a 16-byte slot, publish the index; 100M iterations.
 (2) two threads (producer CPU 1, consumer CPU 0, SCHED_FIFO 10) through the 1024-slot ring; 20M 16-byte msgs.
Machine: shared 4-vCPU cloud VM (Xeon @ 2.10GHz), loaded by other jobs.
Median of 5 runs (min-max):
 publish loop : seq_cst 11.6 ns/op (11.58-11.83)   release 2.53 ns/op (2.49-3.07)   4.6x
 2-thread ring: seq_cst 164 ns/msg (45.6-168)      acq/rel 48.1 ns/msg (45.3-51.2)  3.4x
The seq_cst two-thread result is bimodal: 4 runs at 161-168 ns, one run at 45.6 (same as acq/rel).
Why: xchg has an implicit lock prefix = full barrier. The core may not continue until its store buffer has
drained, including the slot store, which in the two-thread case usually misses (the line sits in the other
core's cache). A release store is a plain mov that retires into the store buffer, and the core keeps going.
