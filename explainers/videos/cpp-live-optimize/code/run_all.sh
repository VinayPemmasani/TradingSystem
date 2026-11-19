#!/bin/sh
# All measurements for the video. Shared 4-vCPU KVM box; SCHED_FIFO, pinned.
# Run from the directory holding the built binaries (build/samples/<slug>), or pass it as $1.
cd "${1:-.}"
date; uptime
chrt -f 10 ./bench 2000000 7
chrt -f 10 ./ilp
chrt -f 10 ./fs
chrt -f 10 ./mt 200000 1000 11
uptime
