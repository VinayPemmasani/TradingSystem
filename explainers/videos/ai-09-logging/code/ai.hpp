// LEFT: the general-purpose logger. Correct, thread-safe, and every line is
// on disk when log() returns -- all of it paid on the calling (hot) thread.
#pragma once
#include <chrono>
#include <cstdint>
#include <fstream>
#include <mutex>

class Logger {
  std::mutex mu_;
  std::ofstream out_;
 public:
  explicit Logger(const char* path) : out_(path) {}
  void fill(const char* sym, int64_t px, uint32_t qty, uint64_t oid) {
    auto ns = std::chrono::system_clock::now().time_since_epoch().count();
    std::lock_guard lock(mu_);
    out_ << ns << " fill oid=" << oid << " sym=" << sym
         << " px=" << px << " qty=" << qty << std::endl;
  }
};
