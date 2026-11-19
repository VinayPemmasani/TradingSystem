#!/usr/bin/env bash
# End-to-end check of Aeron IPC market data: one feed handler, two traders.
#
#   simex --UDP--> itch-fh --Aeron IPC (aeron:ipc, stream 1001)--> trader A, trader B
#                                                                     |  OUCH
#   simex <-----------------------------------------------------------+
#
# aeron-driver runs the media driver in a private directory. Both traders
# subscribe first; itch-fh waits for a subscriber, joins simex's MoldUDP64
# feed, rebuilds the books and republishes every ITCH message on Aeron.
# ouch-client adds noise orders so the traders' quotes trade. Passes when:
#   - itch-fh lost nothing, its books are clean, and it published every
#     message it received;
#   - each trader read exactly that many messages through End of Messages and
#     its own trading checks pass;
#   - ouch-client and simex pass their checks.
#
#   scripts/e2e-aeron.sh [BUILD_DIR]
set -euo pipefail

build=${1:-build/release}
md=${MD:-127.0.0.1:31501}
retrans_port=${RETRANS_PORT:-31502}
rate=${RATE:-100000}
orders=${ORDERS:-10000}
order_rate=${ORDER_RATE:-2000}
duration=${DURATION:-15}
tools=$build/tools
work=$(mktemp -d)
aeron_dir=/dev/shm/aeron-e2e-$$
cleanup() {
  for pid in ${a_pid:-} ${b_pid:-} ${fh_pid:-} ${simex_pid:-} ${driver_pid:-}; do
    kill "$pid" 2>/dev/null || true
  done
  [[ -n "${KEEP:-}" ]] && cp -r "$work" "$KEEP" || true
  rm -rf "$work" "$aeron_dir"
}
trap cleanup EXIT

day=$work/synth.itch50.gz
"$tools/itch-gen/itch-gen" "$day" --symbols 500 --messages 1000000 > /dev/null

echo "== aeron-driver in $aeron_dir"
"$tools/aeron-driver/aeron-driver" --dir "$aeron_dir" --idle backoff > "$work/driver.out" 2>&1 &
driver_pid=$!
for _ in $(seq 100); do [[ -e "$aeron_dir/cnc.dat" ]] && break; sleep 0.05; done

echo "== trader A and trader B on Aeron, itch-fh on $md, simex at $rate msgs/s"
"$build/firm/trader/trader" --md-aeron aeron:ipc --aeron-dir "$aeron_dir" --account FIRM01:lab \
  --symbols SYM0001,SYM0002,SYM0003 --duration "$duration" > "$work/trader-a.out" 2>&1 &
a_pid=$!
"$build/firm/trader/trader" --md-aeron aeron:ipc --aeron-dir "$aeron_dir" --account FIRM04:lab \
  --symbols SYM0003,SYM0004,SYM0005 --duration "$duration" > "$work/trader-b.out" 2>&1 &
b_pid=$!
sleep 0.5
"$tools/itch-fh/itch-fh" --group "$md" --retrans "127.0.0.1:$retrans_port" --aeron aeron:ipc \
  --aeron-dir "$aeron_dir" > "$work/fh.out" 2>&1 &
fh_pid=$!
sleep 0.3
"$build/exchange/simex/simex" --replay "$day" --rate "$rate" --md-dest "$md" \
  --md-retrans-port "$retrans_port" --linger 2 \
  --accounts FIRM01:lab,FIRM02:lab,FIRM03:lab,FIRM04:lab > "$work/simex.out" 2>&1 &
simex_pid=$!

client_status=0
"$tools/ouch-client/ouch-client" --accounts FIRM02:lab,FIRM03:lab --reference "$day" \
  --symbols SYM0001,SYM0002,SYM0003,SYM0004,SYM0005 --orders "$orders" --rate "$order_rate" \
  --max-lots "${MAX_LOTS:-20}" --ioc 0.5 --wait-eos > "$work/client.out" 2>&1 || client_status=$?
fh_status=0; wait "$fh_pid" || fh_status=$?; fh_pid=
a_status=0; wait "$a_pid" || a_status=$?; a_pid=
b_status=0; wait "$b_pid" || b_status=$?; b_pid=
simex_status=0; wait "$simex_pid" || simex_status=$?; simex_pid=

for f in fh trader-a trader-b client simex; do
  echo "== $f"
  cat "$work/$f.out"
done

fail=0
[[ $fh_status -eq 0 ]] || { echo "FAIL: itch-fh exited $fh_status" >&2; fail=1; }
[[ $a_status -eq 0 ]] || { echo "FAIL: trader A exited $a_status" >&2; fail=1; }
[[ $b_status -eq 0 ]] || { echo "FAIL: trader B exited $b_status" >&2; fail=1; }
[[ $client_status -eq 0 ]] || { echo "FAIL: ouch-client exited $client_status" >&2; fail=1; }
[[ $simex_status -eq 0 ]] || { echo "FAIL: simex exited $simex_status" >&2; fail=1; }

published=$(awk '/^Aeron / {print $2}' "$work/fh.out")
dropped=$(awk '/^Aeron / {for (i = 1; i < NF; i++) if ($(i + 1) == "dropped") print $i}' "$work/fh.out")
for t in a b; do
  got=$(awk '/^Market data/ {print $3}' "$work/trader-$t.out")
  [[ -n "$got" && "$got" == "$published" ]] ||
    { echo "FAIL: trader $t read ${got:-0} messages, itch-fh published ${published:-0}" >&2; fail=1; }
  grep -q "through End of Messages" "$work/trader-$t.out" ||
    { echo "FAIL: trader $t stopped before End of Messages" >&2; fail=1; }
done
[[ "${dropped:-1}" == "0" ]] || { echo "FAIL: itch-fh dropped ${dropped:-?} messages" >&2; fail=1; }
[[ $fail -eq 0 ]] || exit 1
echo "PASS: itch-fh published $published ITCH messages over Aeron IPC; both traders read all of them"
