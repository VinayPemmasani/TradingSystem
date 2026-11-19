#include <atomic>

std::atomic<int> flag;
int data;

void store_relaxed() { flag.store(1, std::memory_order_relaxed); }
void store_release() { flag.store(1, std::memory_order_release); }
void store_seq_cst() { flag.store(1, std::memory_order_seq_cst); }
int  load_acquire()  { return flag.load(std::memory_order_acquire); }
void fetch_add_relaxed() { flag.fetch_add(1, std::memory_order_relaxed); }
