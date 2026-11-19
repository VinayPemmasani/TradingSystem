# ai-10-queue: how it was measured

ai.hpp: BlockingQueue = std::mutex + std::condition_variable + std::queue (unbounded, consumer sleeps).
fast.hpp: SpscRing<T,N> = bounded lock-free SPSC ring, cached opposite index, indices on separate 64 B lines,
consumer busy-polls with _mm_pause. msg.hpp: 32-byte Tick.
Build: g++ -O2 -std=c++20 -Wall -Wextra -pthread {bench,test,allocs}.cpp
test: 1M messages through each queue across two threads, same order and same hash -> PASS (ring of 64 to hit full/empty).

Latency: chrt -f 10 ./bench 100000 2000 5 1 0  (runs.txt)
  feed thread pinned to CPU 1, strategy thread pinned to CPU 0, both SCHED_FIFO 10.
  Feed sends one 32-byte message every ~2 us (busy-wait gap), stamping rdtsc in it; the strategy thread
  takes rdtsc on receipt; one-way latency = difference (invariant TSC, one socket). Includes queueing.
  Machine: shared 4-vCPU cloud VM (Xeon @ 2.10GHz), heavily loaded by other jobs (renders, TTS, benchmarks).
Results, median of 5 runs (min-max):
  mutex+cv : p50 5,455 ns (5,314-6,830)   p99 1,161,949 ns (32,289-2,200,220)   ~0.2 context switches/msg
  SPSC ring: p50   216 ns (208-235)       p99       900 ns (344-12,848)         0 context switches
The p99s are dominated by the VM: the consumer's wake-up (futex + scheduler + an idle vCPU woken by IPI
through the hypervisor) and, when it lags, a backlog of queued messages. Earlier probe runs gave the same p50s.
With a 10 us gap the mutex+cv p50 rose to ~16 us (deeper idle before each wake); ring p50 stayed ~235-265 ns.

Allocations per message (allocs.cpp, replaced operator new): std::queue (std::deque) 0.0625 = one 512-byte
chunk per 16 messages; ring 0.
Code size (objdump -dr of g++ -O2, padding excluded): push 187 instr + 14 call sites (lock, unlock,
notify_one, operator new, memmove, throws), pop 81 instr + 7 call sites (lock, unlock, cv::wait, delete);
ring try_push 26 instr, try_pop 22 instr, 0 calls.
