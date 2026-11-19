#!/bin/bash
# Run the three benchmarks whenever the box is quiet; log with load average.
L=/tmp/claude-0/vx/cpp-false-sharing/code/quiet.log
for i in $(seq 1 400); do
  la=$(cut -d' ' -f1 /proc/loadavg)
  if awk "BEGIN{exit !($la < 2.5)}"; then
    { echo "=== $(date +%T) load $la"; /tmp/claude-0/vx/cpp-false-sharing/code/fs3; /tmp/claude-0/vx/cpp-false-sharing/code/fs | head -3;
      /tmp/claude-0/vx/cpp-no-alloc/code/pool new; /tmp/claude-0/vx/cpp-no-alloc/code/pool pool; /tmp/claude-0/vx/cpp-memory-order/code/cost; echo "end load $(cut -d' ' -f1 /proc/loadavg)"; } >> $L 2>&1
    sleep 120
  else sleep 20; fi
done
