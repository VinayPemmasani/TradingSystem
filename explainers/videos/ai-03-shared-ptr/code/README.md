# ai-03-shared-ptr: how it was measured

- `ai.hpp` (LEFT): 4 handlers (on_msg -> risk -> route -> publish), each takes `std::shared_ptr<Order>` by value
  and forwards it by copy: 4 copies + 4 destructions = 8 refcount read-modify-writes per message.
- `mid.hpp`: same chain taking `const std::shared_ptr<Order>&` (minimal fix, for comparison).
- `fast.hpp` (RIGHT): one owner (`OrderPool`, a vector sized at startup); handlers take `const Order&`.
- All handlers `[[gnu::noinline]]` to model a chain across translation units, same work on both sides.
- `test.cpp`: 100k random messages through all three; totals identical; use_count back to 1 after each (ASan+UBSan).
- `bench.cpp`: g++ 13.3 `-O2 -std=c++20 -Wall -Wextra -pthread`, `taskset -c 3 ./bench threads|single`, 3 runs each.
  1,000 orders (in cache), 2M messages picking random orders.
  * `threads`: starts and joins one std::thread first. libstdc++ then uses atomic (lock-prefixed) refcounts;
    `single`: process never starts a thread, so libstdc++ (__libc_single_threaded) uses plain increments.
  * back to back: median of 1,000-message batches; one at a time: lfence+rdtsc / rdtscp (~22 ns timer overhead included).
  * atomic RMW cost: 20M dependent `fetch_add(acq_rel)` on one counter vs a plain volatile add.
  * instruction counts: objdump of the four ai:: vs hp:: handler functions (static count; `lock` = lock-prefixed).
- Box: shared 4-vCPU cloud VM, heavily loaded (load average 30-50). No perf counters.
