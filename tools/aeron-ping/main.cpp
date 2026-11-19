// aeron-ping: round-trip latency between two processes, over Aeron IPC or over
// the lab's own shared-memory SpscRing, so the two can be compared on one box.
//
//   aeron-ping                                    Aeron IPC, embedded driver, 200k round trips
//   aeron-ping --transport shm                    lab::SpscRing pair in /dev/shm
//   aeron-ping --ping-cpu 2 --pong-cpu 3 --driver-cpu 4 --messages 1000000
//   aeron-ping --driver external --dir /dev/shm/aeron-lab   use a running aeron-driver
//
// The process forks a pong child first; nothing else exists yet, so the fork
// copies no threads or locks. The parent then starts the media driver (unless
// --driver external) and both sides connect. Each round trip: ping stamps
// rdtsc into a 64-byte message and publishes it on stream 1101; pong copies it
// back on stream 1102; ping records rdtscp minus the stamp in a
// LatencyHistogram. Both hot loops busy-poll and never allocate.

#include <sys/wait.h>
#include <unistd.h>

#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <memory>
#include <optional>
#include <string>
#include <thread>

#include "lab/aeron/aeron.hpp"
#include "lab/core/affinity.hpp"
#include "lab/core/clock.hpp"
#include "lab/core/histogram.hpp"
#include "lab/core/shm.hpp"
#include "lab/core/spsc_ring.hpp"

namespace {

struct alignas(64) Ping {
  std::uint64_t seq;
  std::uint64_t sent_tsc;
  std::uint8_t pad[48];
};
static_assert(sizeof(Ping) == 64);

struct Options {
  std::string transport = "aeron";  // aeron | shm
  std::string driver = "embedded";  // embedded | external
  std::string dir;                  // Aeron directory; empty: a private one per run
  std::string channel = "aeron:ipc";
  std::uint64_t messages = 200'000;
  std::uint64_t warmup = 20'000;
  int ping_cpu = -1, pong_cpu = -1, driver_cpu = -1;
};

void usage() {
  std::fprintf(
      stderr,
      "usage: aeron-ping [--transport aeron|shm] [--driver embedded|external] [--dir DIR]\n"
      "                  [--channel URI] [--messages N] [--warmup N]\n"
      "                  [--ping-cpu N] [--pong-cpu N] [--driver-cpu N]\n");
}

bool parse(int argc, char** argv, Options& o) {
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    if (i + 1 >= argc) return false;
    const char* v = argv[++i];
    if (a == "--transport")
      o.transport = v;
    else if (a == "--driver")
      o.driver = v;
    else if (a == "--dir")
      o.dir = v;
    else if (a == "--channel")
      o.channel = v;
    else if (a == "--messages")
      o.messages = std::strtoull(v, nullptr, 10);
    else if (a == "--warmup")
      o.warmup = std::strtoull(v, nullptr, 10);
    else if (a == "--ping-cpu")
      o.ping_cpu = std::atoi(v);
    else if (a == "--pong-cpu")
      o.pong_cpu = std::atoi(v);
    else if (a == "--driver-cpu")
      o.driver_cpu = std::atoi(v);
    else
      return false;
  }
  return (o.transport == "aeron" || o.transport == "shm") &&
         (o.driver == "embedded" || o.driver == "external");
}

void pin(int cpu, const char* who) {
  if (cpu < 0) return;
  if (auto ec = lab::pin_this_thread(cpu)) {
    std::fprintf(stderr, "aeron-ping: cannot pin %s to cpu %d: %s\n", who, cpu,
                 ec.message().c_str());
  }
}

// ---- Aeron IPC ----

// The child connects as soon as the parent's driver is up.
std::unique_ptr<lab::aeron::Client> connect_with_retry(const std::string& dir) {
  const auto end = std::chrono::steady_clock::now() + std::chrono::seconds{10};
  for (;;) {
    try {
      return std::make_unique<lab::aeron::Client>(lab::aeron::ClientOptions{.dir = dir});
    } catch (const std::exception&) {
      if (std::chrono::steady_clock::now() > end) throw;
      std::this_thread::sleep_for(std::chrono::milliseconds{20});
    }
  }
}

int aeron_pong(const Options& o, const std::string& dir) {
  pin(o.pong_cpu, "pong");
  auto client = connect_with_retry(dir);
  lab::aeron::Subscription in{*client, o.channel, lab::aeron::kPingStream};
  lab::aeron::Publication out{*client, o.channel, lab::aeron::kPongStream};
  const std::uint64_t total = o.warmup + o.messages;
  std::uint64_t echoed = 0;
  auto echo = [&](const lab::aeron::Message& m) {
    while (out.offer(m.data) != lab::aeron::Offer::kOk) {
    }
    ++echoed;
  };
  while (echoed < total) in.poll(echo, 16);
  // Let ping read the last reply before this publication closes.
  std::this_thread::sleep_for(std::chrono::milliseconds{100});
  return 0;
}

int aeron_ping(const Options& o, const std::string& dir, lab::LatencyHistogram& rtt) {
  pin(o.ping_cpu, "ping");
  auto client = connect_with_retry(dir);
  lab::aeron::Publication out{*client, o.channel, lab::aeron::kPingStream};
  lab::aeron::Subscription in{*client, o.channel, lab::aeron::kPongStream};
  const auto end = std::chrono::steady_clock::now() + std::chrono::seconds{10};
  while (!out.connected() || !in.connected()) {
    if (std::chrono::steady_clock::now() > end) {
      std::fprintf(stderr, "aeron-ping: pong never connected\n");
      return 1;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds{1});
  }
  Ping p{};
  bool got = false;
  auto on_pong = [&](const lab::aeron::Message& m) {
    Ping r;
    std::memcpy(&r, m.data.data(), sizeof r);
    if (r.seq == p.seq) got = true;
  };
  for (std::uint64_t i = 0; i < o.warmup + o.messages; ++i) {
    p.seq = i;
    p.sent_tsc = lab::rdtsc();
    while (out.offer(p) != lab::aeron::Offer::kOk) {
    }
    got = false;
    while (!got) in.poll(on_pong, 1);
    if (i >= o.warmup) rtt.record(lab::rdtscp() - p.sent_tsc);
  }
  return 0;
}

// ---- lab::SpscRing in shared memory ----

struct RingPair {
  lab::SpscRing<Ping, 1024> to_pong;
  lab::SpscRing<Ping, 1024> to_ping;
};

int shm_pong(const Options& o, const std::string& name) {
  pin(o.pong_cpu, "pong");
  std::optional<lab::ShmRegion> region;
  const auto end = std::chrono::steady_clock::now() + std::chrono::seconds{10};
  while (!region) {
    try {
      region.emplace(lab::ShmRegion::open(name));
    } catch (const std::exception&) {
      if (std::chrono::steady_clock::now() > end) throw;
      std::this_thread::sleep_for(std::chrono::milliseconds{5});
    }
  }
  auto* rings = lab::attach_shared<RingPair>(*region, std::chrono::seconds{10});
  const std::uint64_t total = o.warmup + o.messages;
  Ping p;
  for (std::uint64_t n = 0; n < total;) {
    if (rings->to_pong.try_pop(p)) {
      while (!rings->to_ping.try_push(p)) {
      }
      ++n;
    }
  }
  return 0;
}

int shm_ping(const Options& o, const std::string& name, lab::LatencyHistogram& rtt) {
  pin(o.ping_cpu, "ping");
  auto region = lab::ShmRegion::create(name, lab::shared_size<RingPair>());
  auto* rings = lab::create_shared<RingPair>(region);
  Ping p{}, r{};
  for (std::uint64_t i = 0; i < o.warmup + o.messages; ++i) {
    p.seq = i;
    p.sent_tsc = lab::rdtsc();
    while (!rings->to_pong.try_push(p)) {
    }
    while (!rings->to_ping.try_pop(r) || r.seq != i) {
    }
    if (i >= o.warmup) rtt.record(lab::rdtscp() - p.sent_tsc);
  }
  lab::ShmRegion::unlink(name);
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  Options o;
  if (!parse(argc, argv, o)) {
    usage();
    return 2;
  }
  std::string dir = o.dir;
  if (dir.empty()) {
    dir = o.driver == "embedded" ? "/dev/shm/aeron-ping-" + std::to_string(::getpid())
                                 : lab::aeron::default_dir();
  }
  const std::string shm_name = "/lab-ping-" + std::to_string(::getpid());

  // Fork before any thread or mapping exists.
  const pid_t child = ::fork();
  if (child < 0) {
    std::perror("aeron-ping: fork");
    return 2;
  }
  if (child == 0) {
    try {
      std::_Exit(o.transport == "aeron" ? aeron_pong(o, dir) : shm_pong(o, shm_name));
    } catch (const std::exception& e) {
      std::fprintf(stderr, "aeron-ping (pong): %s\n", e.what());
      std::_Exit(2);
    }
  }

  const auto clock = lab::TscClock::calibrate();
  auto rtt = std::make_unique<lab::LatencyHistogram>();
  int rc = 0;
  int status = 0;
  bool reaped = false;
  try {
    if (o.transport == "aeron") {
      std::unique_ptr<lab::aeron::Driver> driver;
      if (o.driver == "embedded") {
        // The driver thread is the one created here; pin the creator so the
        // driver inherits the cpu, then move this thread to the ping cpu.
        if (o.driver_cpu >= 0) pin(o.driver_cpu, "driver");
        driver = std::make_unique<lab::aeron::Driver>(lab::aeron::DriverOptions{.dir = dir});
      }
      rc = aeron_ping(o, dir, *rtt);
      // Keep the driver up until pong has read its last message and exited.
      ::waitpid(child, &status, 0);
      reaped = true;
    } else {
      rc = shm_ping(o, shm_name, *rtt);
    }
  } catch (const std::exception& e) {
    std::fprintf(stderr, "aeron-ping: %s\n", e.what());
    rc = 2;
  }
  if (!reaped) ::waitpid(child, &status, 0);
  if (rc != 0) return rc;
  if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
    std::fprintf(stderr, "aeron-ping: pong process failed\n");
    return 1;
  }

  const double to_ns = 1.0 / clock.ticks_per_ns();
  std::printf("Transport    %s%s, %llu round trips of %zu bytes (after %llu warm-up)\n",
              o.transport == "aeron" ? "Aeron IPC " : "lab::SpscRing in /dev/shm",
              o.transport == "aeron" ? o.channel.c_str() : "",
              static_cast<unsigned long long>(o.messages), sizeof(Ping),
              static_cast<unsigned long long>(o.warmup));
  rtt->print(stdout, "Round trip", to_ns);
  std::printf("One way p50  %.0f ns (half the round trip)\n",
              static_cast<double>(rtt->percentile(50)) * to_ns / 2);
  return 0;
}
