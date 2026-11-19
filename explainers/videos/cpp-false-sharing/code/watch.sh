#!/bin/bash
# Run the three benchmarks whenever the box is quiet; log with load average.
# Build first with explainers/samples.sh; binaries are in build/samples/<slug>/.
B="${B:-$(cd "$(dirname "$0")/../../../.." && pwd)/build/samples}"
L="${L:-$B/cpp-false-sharing/quiet.log}"
for i in $(seq 1 400); do
  la=$(cut -d' ' -f1 /proc/loadavg)
  if awk "BEGIN{exit !($la < 2.5)}"; then
    { echo "=== $(date +%T) load $la"; "$B/cpp-false-sharing/fs3"; "$B/cpp-false-sharing/fs" | head -3;
      "$B/cpp-no-alloc/pool" new; "$B/cpp-no-alloc/pool" pool; "$B/cpp-memory-order/cost"; echo "end load $(cut -d' ' -f1 /proc/loadavg)"; } >> "$L" 2>&1
    sleep 120
  else sleep 20; fi
done
