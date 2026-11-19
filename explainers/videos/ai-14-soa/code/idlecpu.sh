#!/bin/bash
# prints the idlest CPU (1..3) over a 0.5 s window, from /proc/stat
read_idle() { awk '/^cpu[0-9]/{print $1, $5+$6, $2+$3+$4+$5+$6+$7+$8}' /proc/stat; }
a=$(read_idle); sleep 0.5; b=$(read_idle)
paste <(echo "$a") <(echo "$b") | awk '$1!="cpu0"{busy=1-($5-$2)/($6-$3+1e-9); print busy, substr($1,4)}' | sort -n | head -1 | cut -d' ' -f2
