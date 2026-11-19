# fh-08-fanout: Fanning out to strategies: shared memory rings

Key facts and sources (lab repo /home/claude/ts-push):

- `SpscRing`: power-of-two capacity, mask indexing, head and tail on separate 64-byte cache lines (`kCacheLine = 64`), each side caches the other's index, `try_claim`/`commit` and `front`/`pop` zero-copy APIs, release store on commit and acquire load on the other side, slots zeroed at construction to prefault. Source: `libs/core/include/lab/core/spsc_ring.hpp`, `compiler.hpp`.
- Shared memory: `ShmRegion` (populate, huge pages, mlock options), `create_shared`/`attach_shared` with a magic/size/align/ready header; no pointers allowed. Source: `libs/core/include/lab/core/shm.hpp`.
- Aeron IPC republish from itch-fh, stream 1001, flow control at slowest reader + half a term, BACK_PRESSURED. Source: `docs/aeron.md`.
- Measured (docs/aeron.md, shared 4-vCPU cloud container, 500,000 round trips of 64 B, 4 runs): Aeron IPC p50 0.72–0.81 µs, p99 1.4–2.2 µs, p99.9 13–23 µs; SpscRing in /dev/shm p50 0.76–0.98 µs, p99 0.93–1.3 µs, p99.9 9.5–18 µs; 76 ns when both processes were on one physical core.
- The trader's md thread spins on a full TopRing and counts `ring_full_spins`. Source: `firm/trader/main.cpp`.

Unsure: I did not re-run aeron-ping (the box was heavily loaded); all numbers are quoted from the lab's doc with its stated conditions.
