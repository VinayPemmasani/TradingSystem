// False sharing, measured under load. Two threads pinned to CPUs 1 and 2 each do relaxed
// fetch_adds on their own counter in chunks of 2,000, logging each chunk's rdtsc start and end.
// The analysis keeps only chunks during which the other thread was also running.
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <pthread.h>
#include <thread>
#include <vector>
#include <x86intrin.h>

struct Packed {
  std::atomic<long> a{0};
  std::atomic<long> b{0};
};
struct Padded {
  alignas(64) std::atomic<long> a{0};
  alignas(64) std::atomic<long> b{0};
};
static_assert(sizeof(Packed) == 16 && sizeof(Padded) == 128);

constexpr long kChunk = 2'000, kChunks = 50'000;   // 100 million increments per thread

static void pin(int cpu) {
  cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s);
  pthread_setaffinity_np(pthread_self(), sizeof s, &s);
}
static void bump(std::atomic<long>& c, int cpu, std::atomic<int>& go, std::uint64_t* t) {
  pin(cpu); go.fetch_add(1); while (go.load() < 2) {}
  for (long k = 0; k < kChunks; ++k) {
    std::uint64_t t0 = __rdtsc();
    for (long i = 0; i < kChunk; ++i) c.fetch_add(1, std::memory_order_relaxed);
    t[2 * k] = t0; t[2 * k + 1] = __rdtsc();
  }
}
template <class C>
void run(C& c, const char* name) {
  std::vector<std::uint64_t> ta(2 * kChunks), tb(2 * kChunks);
  std::atomic<int> go{0};
  std::thread x(bump, std::ref(c.a), 1, std::ref(go), ta.data());
  std::thread y(bump, std::ref(c.b), 2, std::ref(go), tb.data());
  x.join(); y.join();
  char fn[64]; std::snprintf(fn, sizeof fn, "chunks_%s.bin", name);
  FILE* f = std::fopen(fn, "wb");
  std::fwrite(ta.data(), 8, ta.size(), f); std::fwrite(tb.data(), 8, tb.size(), f); std::fclose(f);
}
int main() {
  alignas(64) static Packed p; alignas(64) static Padded q;
  run(p, "packed"); run(q, "padded");
}
