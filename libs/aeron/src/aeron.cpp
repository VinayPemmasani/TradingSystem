#include "lab/aeron/aeron.hpp"

#include <chrono>
#include <stdexcept>
#include <thread>

extern "C" {
#include "aeronmd.h"
}

namespace lab::aeron {
namespace {

[[noreturn]] void fail(const std::string& what) {
  throw std::runtime_error("aeron: " + what + ": " + aeron_errmsg());
}

// Polls an async add until it completes, fails, or times out.
template <typename T, typename Async, typename Poll>
T* await_add(Async* async, Poll poll, std::uint64_t timeout_ms, const std::string& what) {
  const auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds{timeout_ms};
  for (;;) {
    T* out = nullptr;
    const int r = poll(&out, async);
    if (r == 1) return out;
    if (r < 0) fail(what);
    if (std::chrono::steady_clock::now() > deadline) {
      throw std::runtime_error("aeron: " + what + ": timed out waiting for the media driver");
    }
    std::this_thread::sleep_for(std::chrono::milliseconds{1});
  }
}

}  // namespace

std::string default_dir() { return "/dev/shm/aeron-lab"; }

Driver::Driver(const DriverOptions& opts) : dir_{opts.dir.empty() ? default_dir() : opts.dir} {
  if (aeron_driver_context_init(&ctx_) < 0) fail("driver context");
  aeron_driver_context_set_dir(ctx_, dir_.c_str());
  aeron_driver_context_set_dir_delete_on_start(ctx_, opts.delete_dir_on_start);
  aeron_driver_context_set_dir_delete_on_shutdown(ctx_, true);
  aeron_driver_context_set_threading_mode(ctx_, AERON_THREADING_MODE_SHARED);
  aeron_driver_context_set_ipc_term_buffer_length(ctx_, opts.ipc_term_length);
  // Map the whole log now so no page is faulted in on the hot path.
  aeron_driver_context_set_term_buffer_sparse_file(ctx_, false);
  aeron_driver_context_set_shared_idle_strategy(ctx_, opts.spin ? "spin" : "backoff");
  if (aeron_driver_init(&driver_, ctx_) < 0) {
    aeron_driver_context_close(ctx_);
    fail("driver init in " + dir_);
  }
  if (aeron_driver_start(driver_, false) < 0) {
    aeron_driver_close(driver_);
    aeron_driver_context_close(ctx_);
    fail("driver start");
  }
}

Driver::~Driver() {
  aeron_driver_close(driver_);
  aeron_driver_context_close(ctx_);
}

Client::Client(const ClientOptions& opts) {
  const std::string dir = opts.dir.empty() ? default_dir() : opts.dir;
  if (aeron_context_init(&ctx_) < 0) fail("client context");
  aeron_context_set_dir(ctx_, dir.c_str());
  aeron_context_set_driver_timeout_ms(ctx_, opts.driver_timeout_ms);
  if (aeron_init(&aeron_, ctx_) < 0) {
    aeron_context_close(ctx_);
    fail("connect to the media driver in " + dir);
  }
  if (aeron_start(aeron_) < 0) {
    aeron_close(aeron_);
    aeron_context_close(ctx_);
    fail("client start");
  }
}

Client::~Client() {
  aeron_close(aeron_);
  aeron_context_close(ctx_);
}

Publication::Publication(Client& client, const std::string& channel, std::int32_t stream,
                         std::uint64_t timeout_ms) {
  aeron_async_add_exclusive_publication_t* async = nullptr;
  if (aeron_async_add_exclusive_publication(&async, client.get(), channel.c_str(), stream) < 0) {
    fail("add publication " + channel);
  }
  pub_ = await_add<aeron_exclusive_publication_t>(async, aeron_async_add_exclusive_publication_poll,
                                                  timeout_ms, "add publication " + channel);
}

Publication::~Publication() { aeron_exclusive_publication_close(pub_, nullptr, nullptr); }

Subscription::Subscription(Client& client, const std::string& channel, std::int32_t stream,
                           std::uint64_t timeout_ms) {
  aeron_async_add_subscription_t* async = nullptr;
  if (aeron_async_add_subscription(&async, client.get(), channel.c_str(), stream, nullptr, nullptr,
                                   nullptr, nullptr) < 0) {
    fail("add subscription " + channel);
  }
  sub_ = await_add<aeron_subscription_t>(async, aeron_async_add_subscription_poll, timeout_ms,
                                         "add subscription " + channel);
}

Subscription::~Subscription() { aeron_subscription_close(sub_, nullptr, nullptr); }

}  // namespace lab::aeron

#if defined(__SANITIZE_THREAD__)
#define LAB_AERON_TSAN 1
#elif defined(__has_feature)
#if __has_feature(thread_sanitizer)
#define LAB_AERON_TSAN 1
#endif
#endif

#if defined(LAB_AERON_TSAN)
// Aeron's C code is built without -fsanitize=thread and does its atomics in
// inline assembly (aeron_atomic64_gcc_x86_64.h), so ThreadSanitizer cannot see
// the barriers that order its threads and reports races inside Aeron. Those
// reports are suppressed; races in lab code are still reported.
extern "C" const char* __tsan_default_suppressions() { return "race:_deps/aeron-src/\n"; }
#endif
