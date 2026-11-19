# Running the explainer samples on your own PC

Every video with a `code/` directory (`cpp-*`, `ai-*`, `cpp-live-optimize`) ships the C++ shown on screen with
its tests and benchmarks. This page gets them, and the lab itself, building and running on your machine.

The samples use Linux and x86-64 facilities: `rdtsc`/`rdtscp` for timing, `pthread_setaffinity_np` to pin
threads, and `taskset`/`chrt` to pin and prioritise processes. So the main path is **Windows 11 + WSL2 with
Ubuntu 24.04** on an Intel or AMD PC. Native Linux on x86-64 works the same way. macOS and ARM machines are
covered at the end.

Steps marked **(Windows)** run in PowerShell on Windows. Everything else runs in the Ubuntu shell, and was run
on an Ubuntu 24.04 x86-64 box (g++ 13.3, cmake 3.28, ninja 1.11) while writing this page.

## 1. Set up WSL2 (Windows 11)

**(Windows)** In an administrator PowerShell, then reboot if asked:

```powershell
wsl --install -d Ubuntu-24.04
```

Open "Ubuntu 24.04" from the Start menu and create your Linux user. Optional but recommended for benchmarks:
copy `scripts/wslconfig.example` from the repo (after step 3) to `%UserProfile%\.wslconfig`, set `processors=`
to how many cores WSL may use, and run **(Windows)** `wsl --shutdown` to apply it.

On native Ubuntu 24.04, skip this step.

## 2. Install the tools

```bash
sudo apt-get update
sudo apt-get install -y git build-essential g++ cmake ninja-build python3 \
  libgtest-dev libbenchmark-dev zlib1g-dev util-linux
g++ --version    # 13 or newer (Ubuntu 24.04 ships 13.3)
```

`util-linux` provides `taskset` and `chrt` (normally already installed). Optional: `clang` for the AArch64
assembly listings in two samples, and `linux-tools-generic` for `perf` (perf counters are usually not
available inside WSL2 or cloud VMs).

## 3. Get the code

Clone into your Linux home directory, not under `/mnt/c`: builds through the Windows drive are much slower.

```bash
cd ~
git clone https://github.com/VinayPemmasani/TradingSystem.git
cd TradingSystem
```

The rest of this page runs from this directory.

## 4. Build and test the lab (optional for the samples)

The samples do not need the lab built; they only use a few of its headers. To build the whole lab with its
CMake presets (`CMakePresets.json`):

```bash
cmake --preset release
cmake --build --preset release
ctest --preset release
./build/release/tools/lab-check/lab-check     # checks the machine: cores, TSC, huge pages, multicast
```

`ctest` should end with `100% tests passed`. `lab-check` prints `WARN` lines with a fix for each (huge pages,
loopback multicast, core count); they matter for the lab's feeds, not for the samples.

Configuring downloads the Aeron client from GitHub, so it needs network access. On WSL2,
`scripts/wsl-setup.sh` does all of the above plus the lab's machine settings (loopback multicast, huge pages)
in one go; see the top-level README.md. `asan` and `tsan` presets exist too (`cmake --preset asan`, and so on).

## 5. Build and run every sample

```bash
explainers/samples.sh
```

This builds every `explainers/videos/*/code` directory with `g++ -std=c++20 -O2 -Wall -Wextra -pthread` into
`build/samples/<slug>/` (outside the source tree, ignored by git), then runs each test. Every `.cpp` with a
`main()` becomes a program named after the file; every other `.cpp` is compiled to assembly (`.s`), which is how
the videos show compiler output. The end of the output looks like:

```
== summary: 26 samples, 0 build failures, 0 with warnings, 23 tests, 0 failed
```

Options:

```bash
explainers/samples.sh --bench                    # also run every bench* program (takes several minutes)
explainers/samples.sh --sanitize                 # also build and run ASan+UBSan (and TSan) copies of each test
explainers/samples.sh ai-10-queue cpp-vwap       # only these videos
CXX=clang++ explainers/samples.sh                # another compiler
```

Each program's output is saved next to it, for example `build/samples/ai-01-hashmap/bench.log`, and compiler
messages in `build/samples/<slug>/build.log`.

## 6. Run one sample by hand

Each `code/README.md` says how that sample was built and run for its video. For example, the quote-cache sample:

```bash
cd explainers/videos/ai-01-hashmap/code
g++ -std=c++20 -O2 -Wall -Wextra -DHZ_COUNT_NEW bench.cpp -o /tmp/hz-bench
g++ -std=c++20 -O2 -Wall -Wextra test.cpp -o /tmp/hz-test
/tmp/hz-test
taskset -c 3 /tmp/hz-bench 200000
```

Writing the binaries outside the source tree (here `/tmp`) keeps `git status` clean.

Samples that use the lab's headers (`cpp-memory-order/ring.cpp`, `cpp-order-book`, `cpp-price-parse`,
`cpp-live-optimize/mt.cpp`) need include paths relative to the code directory:

```bash
cd explainers/videos/cpp-live-optimize/code
g++ -std=c++20 -O2 -Wall -Wextra -pthread -I../../../../libs/core/include mt.cpp -o /tmp/mt
cd ../../cpp-order-book/code
g++ -std=c++20 -O2 -Wall -Wextra -I../../../../libs/core/include -I../../../../libs/book/include \
  bench.cpp -o /tmp/book-bench
```

A few samples need more than one file or a flag; `samples.sh` knows them (see `recipe()` in it):

| Sample | Extra |
| --- | --- |
| `ai-01-hashmap`, `ai-02-orderbook`, `ai-04-pool` bench | `-DHZ_COUNT_NEW` (counts allocations) |
| `ai-05-vector`, `ai-06-copies`, `ai-07-exceptions` bench and test | link `alloc_count.cpp` |
| `ai-08-dispatch` bench and test | link `alloc_count.cpp lib.cpp`; the `_opaque` builds compile `lib.cpp` with `-fno-devirtualize-speculatively` |
| `cpp-static-dispatch` bench and test | link `calls.cpp` |
| `cpp-false-sharing` | `--param destructive-interference-size=64` (otherwise g++ warns, which the video discusses) |
| `ai-11-memory-order/arm.c`, `cpp-live-optimize/fixed_arm.cpp` | AArch64 assembly only: `clang --target=aarch64-linux-gnu -O2 -S` |

## 7. Getting stable numbers

The benchmark numbers in the videos come from a **shared, heavily loaded 4-vCPU cloud VM** (load average often
15 to 50 from other jobs), and the videos say so. Your numbers will differ, usually for the better: compare the
two sides of each sample (general vs hot path, before vs after), not the absolute values.

To make runs repeatable:

- Close other programs, and plug a laptop in (power saving changes clock speed).
- Pin a single-threaded benchmark to one core with `taskset`:
  ```bash
  taskset -c 3 build/samples/ai-01-hashmap/bench
  ```
  Some benchmarks pin their own threads (for example `ai-10-queue` uses CPUs 0 and 1, `cpp-live-optimize` uses
  CPUs 1 and 2), so they need at least 4 cores; check the top of each `bench.cpp`.
- Give two-thread benchmarks real-time priority with `chrt`, as their READMEs do. This needs root:
  ```bash
  cd build/samples/ai-10-queue
  sudo chrt -f 10 ./bench 100000 2000 5 1 0
  ```
- Repeat runs and look at the median and the spread, as the READMEs do; one run proves little.
- WSL2 is a VM: Windows still schedules its cores, so pinning inside WSL2 helps but does not isolate a core.
  For the cleanest numbers use native Linux with `isolcpus` or `cset shield`.
- `perf stat` (cache misses, branch misses) works on native Linux; inside WSL2 and most cloud VMs the hardware
  counters are not exposed. None of the samples need it.

`ai-14-soa/code/runall.sh` and `cpp-live-optimize/code/run_all.sh` repeat the video's measurement runs; pass the
build directory: `explainers/videos/ai-14-soa/code/runall.sh build/samples/ai-14-soa`.

## 8. macOS and ARM

Most samples time with `rdtsc` from `<x86intrin.h>`, and several pin threads with
`pthread_setaffinity_np`, which exists only on Linux. So most of them **do not build on macOS**, and the `rdtsc` ones do not build
on ARM Linux (Raspberry Pi, AWS Graviton, Apple Silicon under Linux). Options (not tested here):

- Use any x86-64 Linux machine: a PC with WSL2, a Linux PC, or a small x86 cloud VM (for example an AWS
  `c7i.xlarge`, which is also the closest match to the box the videos were measured on).
- On an Apple Silicon Mac, Docker or UTM with an `linux/amd64` Ubuntu 24.04 image runs everything under
  emulation: the builds and tests work, but timings are meaningless.
- To port a sample to ARM, replace the `rdtsc` timer with `std::chrono::steady_clock` (or the `cntvct_el0`
  counter) and drop the affinity calls. The data-structure and layout lessons carry over; the ns figures do not.

## 9. Re-rendering a video (optional)

The videos themselves are not in git. To render one from its sources (`script.json`, `scenes.html`, ...), follow
[README.md](README.md#rendering) and `engine/GUIDE.md`. You need Node with Playwright (Chromium), ffmpeg, Python
with `kokoro-onnx`, and the voice model (`kokoro-v1.0.onnx` and `voices-v1.0.bin`, about 340 MB, from the
github.com/thewh1teagle/kokoro-onnx releases). The engine scripts have the scratch paths they were written with
at the top; change them to your directories first. Rendering one three-minute video takes several minutes of CPU.
This step was not re-tested for this page.
