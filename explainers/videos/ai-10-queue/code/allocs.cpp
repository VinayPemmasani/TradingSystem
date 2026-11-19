// Allocations per message, steady state (single thread push then pop, 1M msgs).
#include <cstdio>
#include <cstdlib>
#include <new>
#include "ai.hpp"
#include "fast.hpp"
#include "msg.hpp"
static unsigned long long g_n = 0;
void* operator new(size_t n) { ++g_n; if (void* p = malloc(n)) return p; throw std::bad_alloc(); }
void operator delete(void* p) noexcept { free(p); }
void operator delete(void* p, size_t) noexcept { free(p); }
static SpscRing<Tick, 1024> ring;
int main() {
  BlockingQueue<Tick> q; const int n = 1000000;
  for (int i = 0; i < 100; ++i) { q.push(Tick{}); q.pop(); }
  g_n = 0;
  for (int i = 0; i < n; ++i) { q.push(Tick{0, (uint64_t)i, 0, 0, 0}); (void)q.pop(); }
  printf("BlockingQueue: %.4f allocations per message\n", double(g_n) / n);
  g_n = 0;
  for (int i = 0; i < n; ++i) { ring.try_push(Tick{0, (uint64_t)i, 0, 0, 0}); (void)ring.pop(); }
  printf("SpscRing: %.4f allocations per message\n", double(g_n) / n);
}
