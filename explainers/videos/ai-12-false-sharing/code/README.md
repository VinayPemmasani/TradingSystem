# ai-12-false-sharing: how it was measured

ai.hpp: CountersPacked (std::array<std::atomic<uint64_t>,2>, 16 B, one line) and RingPacked (head, cached_tail,
tail, cached_head adjacent: offsets 0/8/16/24, buf at 32). fast.hpp: CountersPadded (alignas(64) per counter,
128 B, static_assert) and RingPadded (head@0, tail@64, buf@128). ring_ops.hpp: one push/pop (cached indices,
acquire/release) used for both rings, so only the layout differs.
Build: g++ -O2 -std=c++20 -Wall -Wextra -pthread {bench,test}.cpp. test: counters and ring give identical results (PASS).
Run: chrt -f 10 ./bench 100000000 20000000 5  (runs.txt). Thread A pinned to CPU 1, thread B to CPU 0, SCHED_FIFO 10.
 (1) each thread does 100M fetch_add(1, relaxed) on its own counter; ns per increment = wall / 100M.
 (2) SPSC ring, 1024 slots, 20M uint64 messages producer CPU 1 -> consumer CPU 0; ns per message.
Machine: shared 4-vCPU cloud VM (Xeon @ 2.10GHz), load average ~45-55 from other jobs during the runs.
Median of 5 runs (min-max):
 counters: packed 31.8 ns/inc (28.5-36.1)   padded 7.1 ns/inc (6.7-8.0)   4.5x
 ring    : packed 98.3 ns/msg (69.1-112.4)  padded 60.0 ns/msg (42.6-75.9) 1.6x
The ring numbers are much slower than on an idle box (the earlier cpp-spsc-ring video measured ~10 ns/msg for a
padded cached ring): treat them as relative. std::hardware_destructive_interference_size = 64 here (g++ 13.3);
used in a header, g++ warns [-Winterference-size] that it can vary with -mtune/-mcpu.
