#pragma once
#include <atomic>
#include <new>

constexpr std::size_t kLine = std::hardware_destructive_interference_size;

struct Counters {
  alignas(kLine) std::atomic<long> a{0};
  alignas(kLine) std::atomic<long> b{0};
};
