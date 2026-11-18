// itch-fh: the firm's ITCH 5.0 feed handler. Joins a MoldUDP64 feed, recovers
// lost packets from the re-request server, and rebuilds every order book live.
//
//   itch-fh                                         239.1.1.1:30001, re-requests to 127.0.0.1:30002
//   itch-fh --rx-cpu 2 --book-cpu 3 --symbol AAPL
//   itch-fh --group 127.0.0.1:30001                 unicast feed (CI, or no loopback multicast)
//   itch-fh --aeron aeron:ipc                       also republish the feed over Aeron IPC
//
// Two threads, joined by lock-free rings (see lab/feed/receiver.hpp):
//
//   rx thread    recvmmsg on the feed and on the re-request socket, timestamps
//                each packet with rdtsc, pushes it to the packet ring; sends
//                retransmission requests. All syscalls happen here.
//   book thread  MoldUDP64 sequencing (gaps, duplicates, reordering), ITCH
//                decode and book updates. No syscalls or locks on the message
//                path.
//
// With --aeron, the book thread also republishes every ITCH message, in
// sequence and with gaps already filled, on an Aeron exclusive publication
// (stream 1001 by default) through the media driver in --aeron-dir; any number
// of trader processes subscribe with `trader --md-aeron aeron:ipc`. Each
// frame's reserved value carries the message's rx timestamp (rdtsc) so a
// subscriber on the same machine can measure feed handler to trader latency.
// See docs/aeron.md.
//
// Runs until End of Session with every message delivered, then prints feed and
// book reports. Exits 0 when nothing was lost and every integrity check is
// zero, 1 otherwise, 2 on usage or setup errors, 3 if the feed went silent or
// was interrupted before End of Session.

#include <atomic>
#include <chrono>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include "lab/aeron/aeron.hpp"
#include "lab/book/book_builder.hpp"
#include "lab/book/report.hpp"
#include "lab/core/affinity.hpp"
#include "lab/core/clock.hpp"
#include "lab/core/histogram.hpp"
#include "lab/feed/receiver.hpp"

namespace {

struct Options {
  lab::feed::ReceiverConfig feed;
  int book_cpu = -1;
  double idle_seconds = 10;  // after the first packet, give up if the feed is silent this long
  std::string symbol;
  std::size_t depth = 10;
  std::size_t top = 10;
  std::vector<lab::book::StripDef> strips;
  std::string aeron_channel;  // empty: no Aeron output
  std::string aeron_dir;      // empty: lab::aeron::default_dir()
  std::int32_t aeron_stream = lab::aeron::kItchStream;
  double aeron_wait_seconds = 10;  // wait this long for a first subscriber before joining the feed
};

void usage() {
  std::fprintf(stderr,
               "usage: itch-fh [--group IP:PORT] [--iface IP] [--retrans IP:PORT]\n"
               "               [--rx-cpu N] [--book-cpu N] [--gap-delay-us N] [--timeout-ms N]\n"
               "               [--retries N] [--idle-seconds S] [--symbol SYM] [--depth N]\n"
               "               [--top N] [--strip NAME=A+B]...\n"
               "               [--aeron CHANNEL] [--aeron-dir DIR] [--aeron-stream N]\n"
               "               [--aeron-wait-seconds S]\n");
}

bool parse(int argc, char** argv, Options& o) {
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    if (i + 1 >= argc) return false;
    const char* v = argv[++i];
    if (a == "--group")
      o.feed.group = v;
    else if (a == "--iface")
      o.feed.iface = v;
    else if (a == "--retrans")
      o.feed.retrans = v;
    else if (a == "--rx-cpu")
      o.feed.rx_cpu = std::atoi(v);
    else if (a == "--book-cpu")
      o.book_cpu = std::atoi(v);
    else if (a == "--gap-delay-us")
      o.feed.gap_delay_us = std::strtoull(v, nullptr, 10);
    else if (a == "--timeout-ms")
      o.feed.timeout_ms = std::strtoull(v, nullptr, 10);
    else if (a == "--retries")
      o.feed.retries = static_cast<std::uint32_t>(std::strtoul(v, nullptr, 10));
    else if (a == "--idle-seconds")
      o.idle_seconds = std::strtod(v, nullptr);
    else if (a == "--symbol")
      o.symbol = v;
    else if (a == "--depth")
      o.depth = std::strtoul(v, nullptr, 10);
    else if (a == "--top")
      o.top = std::strtoul(v, nullptr, 10);
    else if (a == "--aeron")
      o.aeron_channel = v;
    else if (a == "--aeron-dir")
      o.aeron_dir = v;
    else if (a == "--aeron-stream")
      o.aeron_stream = static_cast<std::int32_t>(std::atoi(v));
    else if (a == "--aeron-wait-seconds")
      o.aeron_wait_seconds = std::strtod(v, nullptr);
    else if (a == "--strip") {
      const auto d = lab::book::parse_strip(v);
      if (!d) return false;
      o.strips.push_back(*d);
    } else
      return false;
  }
  return true;
}

std::atomic<bool> g_interrupted{false};

extern "C" void on_signal(int) { g_interrupted.store(true, std::memory_order_relaxed); }

struct BookThread {
  lab::LatencyHistogram rx_to_book;  // ticks from rx timestamp to the message's book update
  lab::aeron::Publication* aeron = nullptr;
  std::uint64_t aeron_published = 0;
  std::uint64_t aeron_retries = 0;  // offers refused as back-pressured or admin action
  std::uint64_t aeron_dropped = 0;  // no subscriber connected
  bool aeron_closed = false;
  std::atomic<bool> stop{false};
  std::atomic<bool> finished{false};
};

// Hands one message to Aeron. A slow subscriber back-pressures this thread
// (and so the packet ring behind it) rather than losing messages.
void publish(BookThread& t, std::span<const std::byte> msg, std::uint64_t rx_tsc) {
  for (;;) {
    switch (t.aeron->offer(msg, static_cast<std::int64_t>(rx_tsc))) {
      case lab::aeron::Offer::kOk:
        ++t.aeron_published;
        return;
      case lab::aeron::Offer::kBackPressured:
      case lab::aeron::Offer::kAdminAction:
        ++t.aeron_retries;
        continue;
      case lab::aeron::Offer::kNotConnected:
        ++t.aeron_dropped;
        return;
      default:
        t.aeron_closed = true;
        return;
    }
  }
}

void book_loop(const Options& opt, lab::feed::FeedReceiver& rx, lab::book::BookBuilder& books,
               BookThread& t) {
  lab::set_thread_name("fh-book");
  if (opt.book_cpu >= 0) {
    if (auto ec = lab::pin_this_thread(opt.book_cpu)) {
      std::fprintf(stderr, "itch-fh: cannot pin book thread to cpu %d: %s\n", opt.book_cpu,
                   ec.message().c_str());
    }
  }
  auto deliver = [&](std::uint64_t, std::span<const std::byte> msg, std::uint64_t rx_tsc) {
    books.apply(msg);
    t.rx_to_book.record(lab::rdtscp() - rx_tsc);
    if (t.aeron != nullptr && !t.aeron_closed) publish(t, msg, rx_tsc);
  };
  while (!t.stop.load(std::memory_order_relaxed)) {
    rx.poll(deliver);
    if (rx.finished()) {
      t.finished.store(true, std::memory_order_release);
      return;
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  Options opt;
  if (!parse(argc, argv, opt)) {
    usage();
    return 2;
  }

  // Everything is allocated and faulted in here, before the threads start.
  auto books = std::make_unique<lab::book::BookBuilder>();
  auto bt = std::make_unique<BookThread>();
  std::unique_ptr<lab::feed::FeedReceiver> rx;
  try {
    rx = std::make_unique<lab::feed::FeedReceiver>(opt.feed);
  } catch (const std::exception& e) {
    std::fprintf(stderr, "itch-fh: %s\n", e.what());
    return 2;
  }
  std::fprintf(stderr, "itch-fh: listening on %s\n", rx->describe().c_str());

  std::unique_ptr<lab::aeron::Client> aeron;
  std::unique_ptr<lab::aeron::Publication> aeron_pub;
  if (!opt.aeron_channel.empty()) {
    try {
      aeron = std::make_unique<lab::aeron::Client>(lab::aeron::ClientOptions{.dir = opt.aeron_dir});
      aeron_pub =
          std::make_unique<lab::aeron::Publication>(*aeron, opt.aeron_channel, opt.aeron_stream);
    } catch (const std::exception& e) {
      std::fprintf(stderr, "itch-fh: %s\n", e.what());
      return 2;
    }
    // Subscribers that join later start at the live position and would miss
    // the stock directory, so wait for the first one before taking the feed.
    const auto until =
        std::chrono::steady_clock::now() + std::chrono::duration<double>(opt.aeron_wait_seconds);
    while (!aeron_pub->connected() && std::chrono::steady_clock::now() < until) {
      std::this_thread::sleep_for(std::chrono::milliseconds{5});
    }
    std::fprintf(stderr, "itch-fh: publishing on %s stream %d (%s)\n", opt.aeron_channel.c_str(),
                 opt.aeron_stream, aeron_pub->connected() ? "subscribed" : "no subscriber yet");
    bt->aeron = aeron_pub.get();
  }

  const auto wall_start = std::chrono::steady_clock::now();
  rx->start();
  std::thread bk{book_loop, std::cref(opt), std::ref(*rx), std::ref(*books), std::ref(*bt)};

  // Main thread: wait for End of Session, Ctrl-C, or a feed gone silent.
  std::signal(SIGINT, on_signal);
  std::signal(SIGTERM, on_signal);
  bool timed_out = false;
  std::uint64_t last_rx = 0;
  auto last_change = std::chrono::steady_clock::now();
  while (!bt->finished.load(std::memory_order_acquire) &&
         !g_interrupted.load(std::memory_order_relaxed)) {
    std::this_thread::sleep_for(std::chrono::milliseconds{50});
    const auto now = std::chrono::steady_clock::now();
    const std::uint64_t rx_now = rx->packets_received();
    if (rx_now != last_rx) {
      last_rx = rx_now;
      last_change = now;
    } else if (last_rx != 0 &&
               std::chrono::duration<double>(now - last_change).count() > opt.idle_seconds) {
      timed_out = true;
      break;
    }
  }
  bt->stop.store(true, std::memory_order_relaxed);
  bk.join();
  rx->stop();
  const double secs =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - wall_start).count();

  const auto& b = *books;
  rx->print_report(stdout);
  bt->rx_to_book.print(stdout, "Rx to book", 1.0 / rx->clock().ticks_per_ns());
  std::printf("Elapsed      %.2f s, last feed time %s\n", secs,
              lab::book::format_feed_time(b.last_timestamp()).c_str());
  std::printf("Live orders  %zu\n", b.orders().size());
  std::printf("Book digest  %016llx\n", static_cast<unsigned long long>(b.digest()));
  if (aeron_pub) {
    std::printf(
        "Aeron        %llu messages published on %s stream %d, %llu bytes; %llu retries,"
        " %llu dropped with no subscriber\n",
        static_cast<unsigned long long>(bt->aeron_published), opt.aeron_channel.c_str(),
        opt.aeron_stream, static_cast<unsigned long long>(aeron_pub->position()),
        static_cast<unsigned long long>(bt->aeron_retries),
        static_cast<unsigned long long>(bt->aeron_dropped));
  }
  lab::book::print_message_types(stdout, b);
  lab::book::print_integrity(stdout, b.checks());
  lab::book::print_top(stdout, b, opt.top);
  lab::book::print_scenarios(stdout, b);
  lab::book::print_implied(stdout, b, opt.strips, 5);
  if (!opt.symbol.empty()) {
    if (const auto l = b.find_locate(opt.symbol))
      lab::book::print_book(stdout, b, l, opt.depth);
    else
      std::printf("\nSymbol %s not found in the stock directory\n", opt.symbol.c_str());
  }

  if (g_interrupted.load()) {
    std::fprintf(stderr, "itch-fh: interrupted before End of Session\n");
    return 3;
  }
  if (timed_out) {
    std::fprintf(stderr, "itch-fh: feed silent for %.0f s before End of Session\n",
                 opt.idle_seconds);
    return 3;
  }
  const bool clean = rx->sequencer().stats().lost == 0 && b.checks().error_count() == 0;
  return clean ? 0 : 1;
}
