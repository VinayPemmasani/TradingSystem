// aeron-driver: the Aeron C media driver with the lab's settings, as its own
// process. itch-fh and every trader connect to it through its directory.
//
//   aeron-driver                                  /dev/shm/aeron-lab, 4 MiB IPC terms, busy-spin
//   aeron-driver --dir /dev/shm/aeron-x --term-length 1048576 --cpu 3 --idle backoff
//
// Runs until Ctrl-C or SIGTERM. The driver creates the log buffers and runs
// flow control; it is not on the IPC data path (see docs/aeron.md).

#include <chrono>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <string>
#include <thread>

#include "lab/aeron/aeron.hpp"
#include "lab/core/affinity.hpp"

namespace {

std::sig_atomic_t volatile g_stop = 0;
extern "C" void on_signal(int) { g_stop = 1; }

}  // namespace

int main(int argc, char** argv) {
  lab::aeron::DriverOptions opts;
  int cpu = -1;
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    if (i + 1 >= argc) {
      std::fprintf(stderr, "aeron-driver: %s needs a value\n", a.c_str());
      return 2;
    }
    const char* v = argv[++i];
    if (a == "--dir") {
      opts.dir = v;
    } else if (a == "--term-length") {
      opts.ipc_term_length = std::strtoull(v, nullptr, 10);
    } else if (a == "--cpu") {
      cpu = std::atoi(v);
    } else if (a == "--idle") {
      opts.spin = std::string{v} == "spin";
    } else {
      std::fprintf(stderr,
                   "usage: aeron-driver [--dir DIR] [--term-length BYTES] [--cpu N]"
                   " [--idle spin|backoff]\n");
      return 2;
    }
  }
  // The driver thread inherits this thread's affinity.
  if (cpu >= 0) {
    if (auto ec = lab::pin_this_thread(cpu)) {
      std::fprintf(stderr, "aeron-driver: cannot pin to cpu %d: %s\n", cpu, ec.message().c_str());
    }
  }
  std::signal(SIGINT, on_signal);
  std::signal(SIGTERM, on_signal);
  try {
    lab::aeron::Driver driver{opts};
    std::fprintf(stderr, "aeron-driver: running in %s, IPC term %zu bytes, %s\n",
                 driver.dir().c_str(), opts.ipc_term_length, opts.spin ? "busy-spin" : "backoff");
    while (g_stop == 0) std::this_thread::sleep_for(std::chrono::milliseconds{50});
  } catch (const std::exception& e) {
    std::fprintf(stderr, "aeron-driver: %s\n", e.what());
    return 2;
  }
  return 0;
}
