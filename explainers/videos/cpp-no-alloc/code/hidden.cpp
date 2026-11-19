// Counts malloc calls made by innocent-looking C++ (glibc: wrap malloc via __libc_malloc).
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <memory>
#include <memory_resource>
#include <stdexcept>
#include <string>
#include <vector>
extern "C" void* __libc_malloc(std::size_t);
static long g_mallocs = 0;
extern "C" void* malloc(std::size_t n) { ++g_mallocs; return __libc_malloc(n); }

template <class F> long count(F f) { long before = g_mallocs; f(); return g_mallocs - before; }

struct Order { long id, price, qty; };
int main() {
  long a = 1, b = 2, c = 3;
  std::printf("function, 8-byte capture : %ld\n", count([&] { std::function<long()> f = [a] { return a; }; (void)f(); }));
  std::printf("function, 16-byte capture: %ld\n", count([&] { std::function<long()> f = [a, b] { return a + b; }; (void)f(); }));
  std::printf("function, 24-byte capture: %ld\n", count([&] { std::function<long()> f = [a, b, c] { return a + b + c; }; (void)f(); }));
  std::printf("string 15 chars          : %ld\n", count([] { std::string s(15, 'x'); (void)s; }));
  std::printf("string 16 chars          : %ld\n", count([] { std::string s(16, 'x'); (void)s; }));
  std::printf("throw/catch              : %ld\n", count([] { try { throw std::runtime_error("x"); } catch (...) {} }));
  std::printf("throw/catch int          : %ld\n", count([] { try { throw 1; } catch (...) {} }));
  std::printf("make_shared<Order>       : %ld\n", count([] { auto p = std::make_shared<Order>(); (void)p; }));
  std::printf("shared_ptr copy          : %ld\n", count([] {}));
  auto sp = std::make_shared<Order>();
  std::printf("shared_ptr copy (real)   : %ld\n", count([&] { auto q = sp; (void)q; }));
  std::vector<Order> v; v.reserve(1000);
  std::printf("push_back under reserve  : %ld\n", count([&] { for (int i = 0; i < 1000; ++i) v.push_back({i, 0, 0}); }));
  std::printf("push_back past capacity  : %ld\n", count([&] { v.push_back({0, 0, 0}); }));
  alignas(16) static char buf[64 * 1024];
  std::pmr::monotonic_buffer_resource arena{buf, sizeof buf, std::pmr::null_memory_resource()};
  std::printf("pmr vector, 100 fills    : %ld\n", count([&] { std::pmr::vector<Order> fills{&arena}; fills.reserve(100); for (int i = 0; i < 100; ++i) fills.push_back({i, 0, 0}); }));
}
