# ai-09-logging: how it was measured

Files: ai.hpp (LEFT: std::ofstream + std::mutex + std::endl on the caller), fast.hpp (RIGHT: 48-byte
binary record into an SPSC ring, background thread formats with fprintf and writes), bench.cpp, test.cpp.

Build: g++ -O2 -std=c++20 -Wall -Wextra -pthread bench.cpp -o bench   (and test.cpp -o test; ./test -> PASS,
both loggers write identical lines after the timestamp field).

Run: ./bench <sink> 100000 5   with sink = a file on the VM's disk (runs_file.txt) and /dev/null (runs_null.txt).
Hot thread pinned to CPU 1, background writer pinned to CPU 0. ~1 us of busy "work" between log calls.
Each call timed with rdtscp pairs (timer overhead ~21 ns, INCLUDED in all numbers). TSC calibrated vs steady_clock.
Machine: shared 4-vCPU cloud VM (Intel Xeon @ 2.10GHz), another benchmark running on CPU 2 at the time.

Results, file sink, median of 5 runs (min-max):
  endl  (flush per line): p50 625 ns (617-641)  p99 2180 ns (2164-2340)
  '\n'  (buffered)      : p50 261 ns (251-268)  p99 1233 ns (1136-1461)
  ring  (binary record) : p50 115 ns (91-119)   p99  137 ns (109-151)
/dev/null sink: endl p50 445 (418-461) p99 1022 (703-1090); ring p50 122 (102-135) p99 143 (119-226).
Without a consumer thread the ring call is ~42 ns incl. timer: most of the ring's ~115 ns is the
cache-line transfer of the slot/head lines the writer core touched (cross-core RFO on this VM).
First run's ring p99.9 ~2 us = first-touch page faults of the 3 MB ring (prefault in real code).

Syscalls (strace -f -c, 20k calls each): ~20,000 write() calls for endl = 1 per log call on the hot thread;
'\n' ~1 per 126 calls (8 KB filebuf); ring 0 on the hot thread (background thread writes 64 KB chunks).
Allocations per call: 0 for all (replaced operator new).
Code size (objdump of g++ -O2): Logger::fill 106 instructions (incl. exception cleanup pads) + 21 call sites into the library (PLT32 relocations: mutex lock/unlock,
system_clock::now, 9 inserts (4 literals, sym, 4 integers) + endl as put and flush, plus error-path throws); LogRing::fill 30 instructions (25 on the not-full path incl. ret), 0 calls. Padding nops and endbr64 excluded.
