#!/usr/bin/env bash
# Build every explainer code sample (explainers/videos/*/code), run its tests,
# and optionally its benchmarks.
#
#   explainers/samples.sh                 build all samples, run every test
#   explainers/samples.sh --bench         ... then run every bench* binary too
#   explainers/samples.sh --sanitize      ... also build and run ASan+UBSan (and TSan for
#                                         threaded tests) copies of every test
#   explainers/samples.sh ai-10-queue cpp-vwap   only these slugs
#
# Binaries and logs go to build/samples/<slug>/ (outside the source tree, ignored by git).
# Environment: CXX (default g++), CC_ARM (default clang, for the AArch64 asm listings),
# JOBS (parallel slugs, default nproc), BUILD (default <repo>/build/samples).
#
# Each .cpp with a main() becomes its own program. Every other .cpp is compiled to
# assembly (-S), which is how the videos show compiler output. Per-slug extras (extra
# translation units, defines) follow each code/README.md and are listed in recipe().
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
BUILD="${BUILD:-$ROOT/build/samples}"
CXX="${CXX:-g++}"
CC_ARM="${CC_ARM:-clang}"
JOBS="${JOBS:-$(nproc 2>/dev/null || echo 2)}"
CXXFLAGS="-std=c++20 -O2 -Wall -Wextra -pthread"
INCLUDES="-I$ROOT/libs/core/include -I$ROOT/libs/book/include -I$ROOT/libs/fix/include"
TEST_TIMEOUT="${TEST_TIMEOUT:-600}"
BENCH_TIMEOUT="${BENCH_TIMEOUT:-900}"

RUN_BENCH=0; SANITIZE=0; ONLY=()
for a in "$@"; do
  case "$a" in
    --bench) RUN_BENCH=1 ;;
    --sanitize) SANITIZE=1 ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    -*) echo "unknown option $a" >&2; exit 2 ;;
    *) ONLY+=("$a") ;;
  esac
done

# recipe <slug> <program>: prints "extra-sources|extra-flags" for one program.
recipe() {
  local slug=$1 prog=$2 src="" flags=""
  case "$slug:$prog" in
    ai-01-hashmap:bench|ai-02-orderbook:bench|ai-04-pool:bench) flags="-DHZ_COUNT_NEW" ;;
    ai-05-vector:bench|ai-05-vector:test|ai-06-copies:bench|ai-06-copies:test|\
    ai-07-exceptions:bench|ai-07-exceptions:test) src="alloc_count.cpp" ;;
    ai-08-dispatch:bench|ai-08-dispatch:test) src="alloc_count.cpp lib.cpp" ;;
    cpp-static-dispatch:bench|cpp-static-dispatch:test) src="calls.cpp" ;;
  esac
  case "$slug" in
    # These files use std::hardware_destructive_interference_size on purpose; pin it to
    # 64 as g++ suggests, so the build is warning-free and the value is stable.
    cpp-false-sharing) flags="$flags --param destructive-interference-size=64" ;;
  esac
  echo "$src|$flags"
}

# Translation units that are linked into a program, not compiled on their own.
is_linked_tu() {
  case "$1:$2" in
    ai-0[5678]-*:alloc_count.cpp|ai-08-dispatch:lib.cpp|cpp-static-dispatch:calls.cpp) return 0 ;;
  esac
  return 1
}

has_main() { grep -qE '^[[:space:]]*int[[:space:]]+main[[:space:]]*\(' "$1"; }

# compile <log> <cmd...>: runs a compile, records warnings and errors in <log>.
compile() {
  local log=$1; shift
  local out
  out=$("$@" 2>&1); local rc=$?
  if [ -n "$out" ]; then printf '$ %s\n%s\n' "$*" "$out" >> "$log"; fi
  if [ $rc -ne 0 ]; then echo "ERROR" >> "$log.status"; return 1; fi
  if printf '%s' "$out" | grep -q 'warning:'; then echo "WARN" >> "$log.status"; fi
  return 0
}

build_slug() {
  local slug=$1 code="$HERE/videos/$1/code" out="$BUILD/$1"
  mkdir -p "$out"; rm -f "$out/build.log" "$out/build.log.status"
  local log="$out/build.log" f base r src flags extra
  for f in "$code"/*.cpp; do
    [ -f "$f" ] || continue
    base=$(basename "$f" .cpp)
    is_linked_tu "$slug" "$base.cpp" && continue
    r=$(recipe "$slug" "$base"); src=${r%%|*}; flags=${r#*|}
    if has_main "$f"; then
      extra=""; for s in $src; do extra="$extra $code/$s"; done
      compile "$log" $CXX $CXXFLAGS $flags $INCLUDES "$f" $extra -o "$out/$base"
      if [ "$slug:$base" = "ai-08-dispatch:bench" ] || [ "$slug:$base" = "ai-08-dispatch:test" ]; then
        # The "opaque" build: lib.cpp without speculative devirtualization (see README).
        compile "$log" $CXX $CXXFLAGS $INCLUDES -fno-devirtualize-speculatively -c "$code/lib.cpp" -o "$out/lib_opaque.o" &&
        compile "$log" $CXX $CXXFLAGS $flags $INCLUDES "$f" "$code/alloc_count.cpp" "$out/lib_opaque.o" -o "$out/${base}_opaque"
      fi
      if [ $SANITIZE = 1 ] && [ "$base" = test ]; then
        compile "$log" $CXX $CXXFLAGS -g -fsanitize=address,undefined -fno-sanitize-recover=all -Wno-maybe-uninitialized $flags $INCLUDES "$f" $extra -o "$out/test_asan"
        # -Wno-maybe-uninitialized: g++ 13 reports false positives inside libstdc++ (std::regex)
        # when sanitizers change inlining.
        if grep -qE 'std::thread|pthread_create' "$f"; then
          compile "$log" $CXX $CXXFLAGS -g -fsanitize=thread -Wno-maybe-uninitialized $flags $INCLUDES "$f" $extra -o "$out/test_tsan"
        fi
      fi
    else
      compile "$log" $CXX $CXXFLAGS $flags $INCLUDES -S "$f" -o "$out/$base.s"
    fi
  done
  # AArch64 listings (ai-11 arm.c, cpp-live-optimize fixed_arm.cpp) need clang's cross target.
  for f in "$code"/arm.c "$code"/*_arm.cpp; do
    [ -f "$f" ] || continue
    base=$(basename "${f%.*}")
    if command -v "$CC_ARM" >/dev/null 2>&1; then
      compile "$log" "$CC_ARM" --target=aarch64-linux-gnu -O2 -S "$f" -o "$out/$base.aarch64.s"
    else
      echo "skip $base: $CC_ARM not found (AArch64 asm only)" >> "$log"
    fi
  done
  if grep -q ERROR "$log.status" 2>/dev/null; then echo "$slug BUILD-FAIL"
  elif grep -q WARN "$log.status" 2>/dev/null; then echo "$slug WARN"
  else echo "$slug OK"; fi
}
export -f build_slug recipe is_linked_tu has_main compile
export HERE BUILD CXX CC_ARM CXXFLAGS INCLUDES SANITIZE

slugs=()
if [ ${#ONLY[@]} -gt 0 ]; then slugs=("${ONLY[@]}")
else for d in "$HERE"/videos/*/code; do s=${d%/code}; slugs+=("$(basename "$s")"); done; fi
for s in "${slugs[@]}"; do
  [ -d "$HERE/videos/$s/code" ] || { echo "no code dir for $s" >&2; exit 2; }
done

echo "== building ${#slugs[@]} samples into $BUILD ($JOBS at a time, $($CXX --version | head -1))"
mkdir -p "$BUILD"
results=$(printf '%s\n' "${slugs[@]}" | xargs -P "$JOBS" -I{} bash -c 'build_slug "$1"' _ {})
printf '%s\n' "$results" | sort | sed 's/^/   /'
fail=0; warn=0
for s in $(printf '%s\n' "$results" | awk '$2!="OK"{print $1}'); do
  echo "---- $s/build.log"; cat "$BUILD/$s/build.log"
done
fail=$(printf '%s\n' "$results" | grep -c 'BUILD-FAIL')
warn=$(printf '%s\n' "$results" | grep -c ' WARN')

run_one() {  # run_one <slug> <binary> <timeout> [args]
  local slug=$1 bin=$2 t=$3; shift 3
  local dir="$BUILD/$slug" log="$BUILD/$slug/$bin.log"
  [ -x "$dir/$bin" ] || return 0
  ( cd "$dir" && timeout "$t" "./$bin" "$@" ) > "$log" 2>&1; local rc=$?
  local last; last=$(grep -v '^\s*$' "$log" | tail -1 | cut -c1-90)
  if [ $rc -eq 0 ]; then printf '   %-24s %-14s ok    %s\n' "$slug" "$bin" "$last"
  else printf '   %-24s %-14s FAIL (exit %d, log %s)\n' "$slug" "$bin" "$rc" "$log"; return 1; fi
}

echo "== tests"
tfail=0; tcount=0
for s in "${slugs[@]}"; do
  bins="test test_opaque"; [ $SANITIZE = 1 ] && bins="$bins test_asan test_tsan"
  for b in $bins; do
    [ -x "$BUILD/$s/$b" ] || continue
    tcount=$((tcount+1))
    run_one "$s" "$b" "$TEST_TIMEOUT" || tfail=$((tfail+1))
  done
done

bfail=0
if [ $RUN_BENCH = 1 ]; then
  echo "== benchmarks (default arguments; numbers depend on your machine and its load)"
  for s in "${slugs[@]}"; do
    for p in "$BUILD/$s"/bench*; do
      [ -x "$p" ] && [ -f "$p" ] || continue
      case "$p" in *.log|*.s|*.o) continue ;; esac
      run_one "$s" "$(basename "$p")" "$BENCH_TIMEOUT" || bfail=$((bfail+1))
    done
  done
  echo "   full output: $BUILD/<slug>/bench*.log"
fi

echo "== summary: ${#slugs[@]} samples, $fail build failures, $warn with warnings, $tcount tests, $tfail failed$( [ $RUN_BENCH = 1 ] && echo ", $bfail benchmarks failed")"
[ $fail -eq 0 ] && [ $tfail -eq 0 ] && [ $bfail -eq 0 ]
