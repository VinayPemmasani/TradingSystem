#pragma once

// Aeron IPC for the lab: a thin C++ layer over the official Aeron C client and
// C media driver (https://github.com/real-logic/aeron, see docs/aeron.md).
//
// Aeron IPC moves messages between processes on one machine through a log
// buffer file in shared memory (/dev/shm/<dir>/publications/*.logbuffer). A
// publisher appends frames to the log; every subscriber reads them in place
// and advances its own position counter. The media driver is not on the data
// path: it creates the log, and its conductor sets the publisher's limit from
// the slowest subscriber's position (flow control).
//
//   Driver        runs the C media driver on a thread inside this process
//   Client        connects to a driver through its CnC file (cnc.dat)
//   Publication   exclusive publication: one writer thread, no atomics on append
//   Subscription  reads every image (publisher) on a channel and stream
//
// Setup (constructors) allocates, maps files and throws std::runtime_error.
// offer() and poll() are the hot path: no allocation, locks, syscalls or
// exceptions. Neither is thread-safe; give each its own thread.

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <span>
#include <string>
#include <type_traits>

extern "C" {
#include "aeronc.h"

// From aeronmd.h (the driver API), which only aeron.cpp includes.
typedef struct aeron_driver_context_stct aeron_driver_context_t;
typedef struct aeron_driver_stct aeron_driver_t;
}

namespace lab::aeron {

// Default stream ids used by the lab.
inline constexpr std::int32_t kItchStream = 1001;  // ITCH messages from itch-fh
inline constexpr std::int32_t kPingStream = 1101;  // aeron-ping requests
inline constexpr std::int32_t kPongStream = 1102;  // aeron-ping replies

// The Aeron directory the lab uses when none is given: /dev/shm/aeron-lab.
std::string default_dir();

struct DriverOptions {
  std::string dir;                        // empty: default_dir()
  std::size_t ipc_term_length = 4 << 20;  // bytes per term (x3 per log); power of two
  bool spin = true;                       // busy-spin the driver thread (lowest latency)
  bool delete_dir_on_start = true;
};

// The media driver, running in this process on its own thread (SHARED
// threading mode: one agent does conductor, sender and receiver work).
class Driver {
 public:
  explicit Driver(const DriverOptions& opts);
  ~Driver();
  Driver(const Driver&) = delete;
  Driver& operator=(const Driver&) = delete;

  const std::string& dir() const noexcept { return dir_; }

 private:
  std::string dir_;
  aeron_driver_context_t* ctx_ = nullptr;
  aeron_driver_t* driver_ = nullptr;
};

struct ClientOptions {
  std::string dir;  // empty: default_dir()
  std::uint64_t driver_timeout_ms = 10'000;
};

// A connection to a media driver. Runs the client conductor on a background
// thread (it services the CnC command and broadcast buffers, not the data).
class Client {
 public:
  explicit Client(const ClientOptions& opts);
  ~Client();
  Client(const Client&) = delete;
  Client& operator=(const Client&) = delete;

  aeron_t* get() const noexcept { return aeron_; }

 private:
  aeron_context_t* ctx_ = nullptr;
  aeron_t* aeron_ = nullptr;
};

// Results of Publication::offer() that are not a position.
enum class Offer : std::int8_t {
  kOk,
  kNotConnected,
  kBackPressured,
  kAdminAction,
  kClosed,
  kError
};

class Publication {
 public:
  // Blocks until the driver has created the log buffer (or throws after
  // `timeout_ms`). Channel is usually "aeron:ipc" or "aeron:ipc?term-length=1m".
  Publication(Client& client, const std::string& channel, std::int32_t stream,
              std::uint64_t timeout_ms = 10'000);
  ~Publication();
  Publication(const Publication&) = delete;
  Publication& operator=(const Publication&) = delete;

  // Appends one message. `reserved` goes in the frame header's 64-bit reserved
  // value field (the lab puts the feed handler's rdtsc receive time there).
  // kBackPressured and kAdminAction are transient: retry.
  Offer offer(std::span<const std::byte> msg, std::int64_t reserved = 0) noexcept {
    std::int64_t r = reserved;
    const std::int64_t pos = aeron_exclusive_publication_offer(
        pub_, reinterpret_cast<const std::uint8_t*>(msg.data()), msg.size(), &supply_reserved, &r);
    return pos > 0 ? Offer::kOk : to_offer(pos);
  }

  template <typename T>
  Offer offer(const T& msg, std::int64_t reserved = 0) noexcept {
    static_assert(std::is_trivially_copyable_v<T>, "messages are copied byte for byte");
    return offer(std::span<const std::byte>{reinterpret_cast<const std::byte*>(&msg), sizeof(T)},
                 reserved);
  }

  // True once at least one subscriber has an image of this publication.
  bool connected() const noexcept { return aeron_exclusive_publication_is_connected(pub_); }
  // Bytes appended so far (the stream position).
  std::int64_t position() const noexcept { return aeron_exclusive_publication_position(pub_); }
  // How far the publisher may write before it is back-pressured: the slowest
  // subscriber's position plus the term window, set by the driver.
  std::int64_t limit() const noexcept { return aeron_exclusive_publication_position_limit(pub_); }

 private:
  static std::int64_t supply_reserved(void* clientd, std::uint8_t*, std::size_t) {
    return *static_cast<const std::int64_t*>(clientd);
  }
  static Offer to_offer(std::int64_t r) noexcept {
    switch (r) {
      case AERON_PUBLICATION_NOT_CONNECTED:
        return Offer::kNotConnected;
      case AERON_PUBLICATION_BACK_PRESSURED:
        return Offer::kBackPressured;
      case AERON_PUBLICATION_ADMIN_ACTION:
        return Offer::kAdminAction;
      case AERON_PUBLICATION_CLOSED:
        return Offer::kClosed;
      default:
        return Offer::kError;
    }
  }

  aeron_exclusive_publication_t* pub_ = nullptr;
};

// One delivered message: the payload and the parts of its frame header the
// lab uses.
struct Message {
  std::span<const std::byte> data;
  std::int64_t reserved;  // the publisher's reserved value
  std::int64_t position;  // stream position just after this message
  std::int32_t session_id;
};

class Subscription {
 public:
  // Blocks until the driver has registered the subscription.
  Subscription(Client& client, const std::string& channel, std::int32_t stream,
               std::uint64_t timeout_ms = 10'000);
  ~Subscription();
  Subscription(const Subscription&) = delete;
  Subscription& operator=(const Subscription&) = delete;

  // Calls f(const Message&) for up to `limit` messages; returns how many.
  // The span points into the log buffer and is only valid inside f.
  template <typename F>
  int poll(F&& f, int limit = 64) noexcept {
    auto handler = [](void* clientd, const std::uint8_t* buffer, std::size_t length,
                      aeron_header_t* header) {
      aeron_header_values_t v;
      aeron_header_values(header, &v);
      const Message m{{reinterpret_cast<const std::byte*>(buffer), length},
                      v.frame.reserved_value,
                      aeron_header_position(header),
                      v.frame.session_id};
      (*static_cast<std::remove_reference_t<F>*>(clientd))(m);
    };
    return aeron_subscription_poll(sub_, handler, &f, static_cast<std::size_t>(limit));
  }

  // Publishers currently connected (one image each).
  int images() const noexcept { return aeron_subscription_image_count(sub_); }
  bool connected() const noexcept { return aeron_subscription_is_connected(sub_); }

 private:
  aeron_subscription_t* sub_ = nullptr;
};

}  // namespace lab::aeron
