#!/bin/bash
# 5 rounds x {1M, 8M} orders, each pinned to the idlest core at launch
# Run from the directory holding the built binaries (build/samples/<slug>), or pass it as $1.
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "${1:-.}"
for r in 1 2 3 4 5; do for n in 1048576 8388608; do c=$("$HERE"/idlecpu.sh); echo "== round $r cpu $c load $(cut -d' ' -f1 /proc/loadavg)"; taskset -c $c ./bench $n; done; done
