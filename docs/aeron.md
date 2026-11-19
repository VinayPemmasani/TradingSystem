# Aeron IPC in the lab

The lab builds the real [Aeron](https://github.com/real-logic/aeron) C client and C media
driver (release 1.47.7, fetched by `cmake/Aeron.cmake`; 1.48 and later need CMake 3.30, and
Ubuntu 24.04 ships 3.28). `libs/aeron` wraps them in a few C++ classes. The facts below come
from Aeron's own sources, named in each section, at that release.

## Why

`itch-fh` joins simex's MoldUDP64 feed, recovers lost packets and rebuilds every book. Before
this change, every `trader` process did all of that again on its own copy of the UDP feed. With
`itch-fh --aeron aeron:ipc`, the feed handler does it once and republishes the gap-free ITCH
stream through shared memory. Any number of `trader --md-aeron aeron:ipc` processes read it
with no syscalls on the data path.

```
simex --MoldUDP64--> itch-fh --aeron:ipc stream 1001--> trader A
                                                     \-> trader B      (each OUCH back to simex)
```

## The pieces

| Piece | What it is |
| --- | --- |
| Media driver | `aeron-driver` (or `lab::aeron::Driver` inside a process). It creates log buffers, links publishers to subscribers and runs flow control. It is not on the IPC data path. |
| Aeron directory | `/dev/shm/aeron-lab` by default. `cnc.dat` holds the to-driver ring buffer (client commands), the to-clients broadcast buffer (driver replies) and the counters, including every subscriber's position. |
| Log buffer | `<dir>/publications/<id>.logbuffer`, one per publication, mapped by the publisher and by every subscriber. |
| Client | `lab::aeron::Client`: maps `cnc.dat` and runs Aeron's client conductor thread, which handles commands, not data. |

Setup: the client writes ADD_PUBLICATION to the to-driver ring, and the driver creates the log
and answers on the broadcast buffer with its file name. A subscriber sends ADD_SUBSCRIPTION and
is told about the image (the same file), which it maps. From then on both processes share those
pages.

## Log buffer (`aeron_logbuffer_descriptor.h`)

The log buffer holds three term partitions and then a metadata page. The metadata page holds
`term_tail_counters[3]`, `active_term_count`, the initial term id, the term length and a
default frame header. The lab's terms are 4 MiB (`DriverOptions::ipc_term_length`). The smallest
allowed is 64 KiB, and Aeron's IPC default is 64 MiB. The raw tail of a term is
`term_id << 32 | term_offset`.

## Frame header (`protocol/aeron_udp_protocol.h`)

Every message is one frame: a 32-byte header, then the payload. Frames are padded to 32-byte
alignment. All fields are little-endian, unlike the lab's exchange protocols.

| Offset | Size | Field | Notes |
| --- | --- | --- | --- |
| 0 | 4 | frame_length | header + payload, before alignment; negative while the frame is being written |
| 4 | 1 | version | |
| 5 | 1 | flags | 0x80 begin, 0x40 end; 0xC0 for a message in one frame |
| 6 | 2 | type | 0x01 data, 0x00 padding |
| 8 | 4 | term_offset | |
| 12 | 4 | session_id | identifies the publication |
| 16 | 4 | stream_id | the lab's ITCH feed is 1001 |
| 20 | 4 | term_id | |
| 24 | 8 | reserved_value | `itch-fh` puts the packet's rdtsc receive time here |

A 36-byte ITCH Add Order becomes a 68-byte frame and takes 96 bytes of the log. A 64-byte
`aeron-ping` message also takes 96 bytes.

## Publish (`aeron_exclusive_publication.c`)

`itch-fh` uses an exclusive publication, which allows only one writer thread. That writer moves
the tail with a release store rather than an atomic add (a shared publication uses get-and-add
on the raw tail). Each append does the following:

1. Write `frame_length = -length` (release), then the other header fields and the payload.
2. Store `frame_length = +length` with release ordering. That store commits the frame.

There is no lock and no syscall. If the frame does not fit in the rest of the term, a padding
frame fills the term and the next term (`term_count % 3`) becomes active. The offer that hits
this returns ADMIN_ACTION, and the caller retries.

## Poll

Each subscriber keeps a position. `aeron_subscription_poll` reads `frame_length` there with
acquire ordering. A positive length means a whole frame is ready, and the handler gets a
pointer straight into the shared pages, so nothing is copied. The position then advances by
the aligned length and is published to the subscriber's position counter. Subscribers read
the same bytes independently.

## Flow control (`aeron_ipc_publication.c`)

The driver's conductor reads every subscriber position and sets the publisher's limit to the
slowest position plus the term window (half a term, `aeron_producer_window_length`). It also
zeroes the partition the slowest reader has left behind. Past the limit, `offer` returns
BACK_PRESSURED (-2). With no subscriber it returns NOT_CONNECTED (-1). `itch-fh` retries on
back pressure, so a slow trader slows the feed handler instead of losing messages. The report
counts these retries, and `tests/aeron` checks the limit.

## Using it

```
build/release/tools/aeron-driver/aeron-driver &                     # /dev/shm/aeron-lab
build/release/firm/trader/trader --md-aeron aeron:ipc --account FIRM01:lab --symbols SYM0001 &
build/release/tools/itch-fh/itch-fh --aeron aeron:ipc               # waits for a subscriber
build/release/tools/aeron-ping/aeron-ping --ping-cpu 2 --pong-cpu 3 --driver-cpu 4
build/release/tools/aeron-ping/aeron-ping --transport shm --ping-cpu 2 --pong-cpu 3
```

A subscriber that joins late starts at the live position. It would miss the stock directory, so
start the traders first. `itch-fh` waits up to `--aeron-wait-seconds` (default 10) for the first
one. Traders stop at the ITCH End of Messages event, or when the publisher goes away.

`scripts/e2e-aeron.sh` runs the whole chain with two traders. It checks that each trader reads
exactly the messages `itch-fh` published, through End of Messages, and that every trading
check passes.

## Measured (shared 4-vCPU cloud container, so tails are noisy)

`aeron-ping` timed 500,000 round trips of 64 bytes between two processes, pinned to separate
cores, with both sides busy-polling:

| Transport | Round trip p50 | p99 | p99.9 |
| --- | --- | --- | --- |
| Aeron IPC (embedded driver) | 0.72–0.81 µs | 1.4–2.2 µs | 13–23 µs |
| `lab::SpscRing` in `/dev/shm` | 0.76–0.98 µs | 0.93–1.3 µs | 9.5–18 µs |

The ranges are four runs. When the two processes landed on one physical core, the ring
reached 76 ns, so placement matters more than the transport here. Aeron's reader touches one
cache line per message (the frame), while the ring's reader also reads the producer's index
line, which is why the medians are close. Aeron also adds back pressure, many subscribers,
term rotation and a standard frame format.

In `e2e-aeron.sh`, nine busy-polling threads ran on 4 vCPUs. The fastest message took 0.9–2 µs
from `itch-fh`'s packet receive to the trader's md thread. The median was 9–11 ms, almost all of
it queueing that was already present before Aeron: `itch-fh`'s own receive-to-book median was
7 ms in the same run. Rerun on pinned, isolated cores (see `docs/core-plan.md`) for real tails.

## Sanitizers

Aeron's C code is built without sanitizer flags and does its atomics in inline assembly. That
means ThreadSanitizer cannot see the ordering inside it. `libs/aeron` therefore suppresses
reports whose stack is in Aeron's sources (`__tsan_default_suppressions`). Races in lab code
are still reported. CI runs `e2e-aeron.sh` under release and ASan. Under TSan the two traders
cannot keep up, so there `tests/aeron` covers the Aeron path.
