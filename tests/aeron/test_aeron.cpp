#include <gtest/gtest.h>
#include <unistd.h>

#include <chrono>
#include <cstdint>
#include <string>
#include <thread>

#include "lab/aeron/aeron.hpp"

namespace {

struct Tick {
  std::uint64_t seq;
  std::uint32_t price;
  std::uint32_t qty;
};
static_assert(sizeof(Tick) == 16);

std::string test_dir() { return "/dev/shm/aeron-lab-test-" + std::to_string(::getpid()); }

class AeronIpc : public ::testing::Test {
 protected:
  // The smallest term Aeron allows, so a test can fill the window quickly.
  lab::aeron::Driver driver{{.dir = test_dir(), .ipc_term_length = 64 * 1024, .spin = false}};
  lab::aeron::Client client{{.dir = test_dir()}};
};

template <typename Pred>
bool eventually(Pred p) {
  const auto end = std::chrono::steady_clock::now() + std::chrono::seconds{5};
  while (std::chrono::steady_clock::now() < end) {
    if (p()) return true;
    std::this_thread::sleep_for(std::chrono::milliseconds{1});
  }
  return false;
}

TEST_F(AeronIpc, NoSubscriberMeansNotConnected) {
  lab::aeron::Publication pub{client, "aeron:ipc", 7};
  EXPECT_FALSE(pub.connected());
  EXPECT_EQ(pub.offer(Tick{1, 100, 10}), lab::aeron::Offer::kNotConnected);
}

TEST_F(AeronIpc, DeliversInOrderWithReservedValue) {
  lab::aeron::Subscription sub{client, "aeron:ipc", 8};
  lab::aeron::Publication pub{client, "aeron:ipc", 8};
  ASSERT_TRUE(eventually([&] { return pub.connected() && sub.images() == 1; }));

  constexpr std::uint64_t kCount = 20'000;  // several terms: exercises term rotation
  std::uint64_t sent = 0, received = 0;
  bool in_order = true;
  auto on_msg = [&](const lab::aeron::Message& m) {
    ASSERT_EQ(m.data.size(), sizeof(Tick));
    Tick t;
    std::memcpy(&t, m.data.data(), sizeof t);
    in_order = in_order && t.seq == received && m.reserved == static_cast<std::int64_t>(t.seq * 3);
    ++received;
  };
  const auto end = std::chrono::steady_clock::now() + std::chrono::seconds{10};
  while (received < kCount && std::chrono::steady_clock::now() < end) {
    if (sent < kCount) {
      const auto r = pub.offer(Tick{sent, 100, 10}, static_cast<std::int64_t>(sent * 3));
      if (r == lab::aeron::Offer::kOk) ++sent;
    }
    sub.poll(on_msg, 16);
  }
  EXPECT_EQ(received, kCount);
  EXPECT_TRUE(in_order);
  // 16-byte payload + 32-byte header = 48, aligned to 64 bytes per frame.
  EXPECT_EQ(pub.position(), static_cast<std::int64_t>(kCount * 64));
}

TEST_F(AeronIpc, SlowSubscriberBackPressuresThePublisher) {
  lab::aeron::Subscription sub{client, "aeron:ipc", 9};
  lab::aeron::Publication pub{client, "aeron:ipc", 9};
  ASSERT_TRUE(eventually([&] { return pub.connected(); }));

  // Nobody polls: the publisher may run at most a term window (half a term)
  // ahead of the subscriber before offers are refused.
  std::uint64_t accepted = 0;
  lab::aeron::Offer last = lab::aeron::Offer::kOk;
  for (int i = 0; i < 100'000; ++i) {
    last = pub.offer(Tick{accepted, 1, 1});
    if (last != lab::aeron::Offer::kOk) break;
    ++accepted;
  }
  EXPECT_EQ(last, lab::aeron::Offer::kBackPressured);
  EXPECT_LE(pub.position(), pub.limit());
  EXPECT_LE(pub.position(), 32 * 1024 + 64);

  // Draining the subscriber lets the driver raise the limit again.
  std::uint64_t drained = 0;
  ASSERT_TRUE(eventually([&] {
    drained += static_cast<std::uint64_t>(sub.poll([](const lab::aeron::Message&) {}, 1024));
    return drained == accepted;
  }));
  EXPECT_TRUE(
      eventually([&] { return pub.offer(Tick{accepted, 1, 1}) == lab::aeron::Offer::kOk; }));
}

}  // namespace
