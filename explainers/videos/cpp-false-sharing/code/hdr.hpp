#include <new>
struct S { alignas(std::hardware_destructive_interference_size) int a; };
