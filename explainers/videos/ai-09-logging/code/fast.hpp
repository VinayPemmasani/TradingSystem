// RIGHT: the hot thread copies a fixed-size binary record into an SPSC ring
// (about 10 stores and one release store). A background thread formats and
// writes. No lock, no formatting, no syscall on the hot path.
#pragma once
#include <atomic>
#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <x86intrin.h>

struct Rec {                    // 48 bytes, trivially copyable
  uint64_t tsc;
  const char* fmt;              // string literal: only the pointer is copied
  const char* sym;              // must outlive the logger (literal / static)
  int64_t px; uint64_t oid; uint32_t qty;
};
static_assert(sizeof(Rec) == 48);
inline constexpr const char* kFillFmt =
    "fill oid=%" PRIu64 " sym=%s px=%" PRId64 " qty=%u";
inline constexpr auto relaxed = std::memory_order_relaxed;
inline constexpr auto acquire = std::memory_order_acquire;
inline constexpr auto release = std::memory_order_release;

template <size_t N>
class LogRing {
  static_assert((N & (N - 1)) == 0);
  alignas(64) std::atomic<uint64_t> head_{0};
  uint64_t cached_tail_ = 0;
  alignas(64) std::atomic<uint64_t> tail_{0};
  alignas(64) Rec buf_[N];
 public:
  uint64_t dropped = 0;
  // hot thread
  void fill(const char* sym, int64_t px, uint32_t qty, uint64_t oid) {
    uint64_t h = head_.load(relaxed);
    if (h - cached_tail_ == N) {
      cached_tail_ = tail_.load(acquire);
      if (h - cached_tail_ == N)
        { ++dropped; return; }  // never block
    }
    buf_[h & (N - 1)] =
        Rec{__rdtsc(), kFillFmt, sym, px, oid, qty};
    head_.store(h + 1, release);  // publish
  }
  // background thread: returns records written
  size_t drain(FILE* f, double ns_per_tick, uint64_t tsc0, uint64_t wall0) {
    uint64_t t = tail_.load(std::memory_order_relaxed);
    const uint64_t h = head_.load(std::memory_order_acquire);
    size_t n = 0;
    for (; t != h; ++t, ++n) {
      const Rec& r = buf_[t & (N - 1)];
      fprintf(f, "%" PRIu64 " ", wall0 + uint64_t((r.tsc - tsc0) * ns_per_tick));
      fprintf(f, r.fmt, r.oid, r.sym, r.px, r.qty);
      fputc('\n', f);
    }
    tail_.store(t, std::memory_order_release);
    if (n) fflush(f);
    return n;
  }
};
