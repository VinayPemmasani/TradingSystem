// On-screen snippets for cpp-no-alloc, compiled together.
#include <cstddef>
#include <cstdint>
#include <memory_resource>
#include <vector>

template <class T>
class Pool {                                   // fixed capacity, intrusive free list
 public:
  explicit Pool(std::size_t n) : slots_(n) {   // allocates and touches every slot up front
    for (std::size_t i = 0; i + 1 < n; ++i) slots_[i].next = &slots_[i + 1];
    free_ = &slots_[0];
  }
  T* get() noexcept { T* p = free_; if (p) free_ = p->next; return p; }
  void put(T* p) noexcept { p->next = free_; free_ = p; }
 private:
  std::vector<T> slots_;
  T* free_ = nullptr;
};

struct Order { std::uint64_t id, price, qty, ts; Order* next; char pad[24]; };
struct Fill { std::uint64_t order, qty, price; };

int main() {
  Pool<Order> pool(100'001);
  Order* o = pool.get(); pool.put(o);

  alignas(16) static char buf[64 * 1024];                  // owned, faulted in at startup
  std::pmr::monotonic_buffer_resource arena{
      buf, sizeof buf, std::pmr::null_memory_resource()};  // never falls back to malloc
  {
    std::pmr::vector<Fill> fills{&arena};                  // scratch for one batch
    fills.reserve(64);
    fills.push_back({1, 100, 101250});
  }
  arena.release();                                         // free everything at once

  std::vector<Order> v;
  v.reserve(1000);                // startup: one allocation
  for (int i = 0; i < 1000; ++i)
    v.push_back(Order{});         // hot path: no allocation
}
