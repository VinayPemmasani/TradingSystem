// Replaced global operator new/delete that count allocations (link into bench and test).
#include <cstdlib>
#include <new>
#include <cstdint>
extern std::uint64_t g_allocs_ext;
std::uint64_t g_allocs_ext = 0;
void* operator new(std::size_t n) { ++g_allocs_ext; if (void* p = std::malloc(n ? n : 1)) return p; throw std::bad_alloc(); }
void* operator new[](std::size_t n) { ++g_allocs_ext; if (void* p = std::malloc(n ? n : 1)) return p; throw std::bad_alloc(); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
