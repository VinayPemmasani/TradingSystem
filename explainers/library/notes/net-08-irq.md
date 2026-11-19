# net-08-irq: Interrupts, coalescing and busy polling

Key facts and sources

- NAPI, busy polling, SO_BUSY_POLL and the net.core.busy_poll / busy_read sysctls: Linux kernel docs https://docs.kernel.org/networking/napi.html
- RSS (flows hashed onto receive queues, one interrupt per queue), IRQ affinity via /proc/irq/<n>/smp_affinity, and irqbalance: https://docs.kernel.org/networking/scaling.html
- Interrupt coalescing with ethtool -C: rx-usecs, rx-frames, adaptive-rx: https://man7.org/linux/man-pages/man8/ethtool.8.html
- AMD Onload user guide (UG1586): handling an interrupt and switching to the right thread costs on the order of a microsecond; EF_POLL_USEC sets how long Onload spins before blocking: https://docs.amd.com/r/en-US/ug1586-onload-user/Resources
- Lab core plan: CPU 2 feed receive, 3 book, 4 trading, 5 order entry, 6 to 7 simex, 0 to 1 housekeeping (docs/core-plan.md in /home/claude/ts-push). The feed receiver loops over a non-blocking recvmmsg and sleeps only when idle_sleep_us is set (libs/feed).
- Lab measurement: aeron-ping, 500,000 round trips of 64 bytes between two busy-polling processes on separate cores, p50 0.72 to 0.81 µs over four runs on a shared 4-vCPU container (docs/aeron.md).

Unsure / simplified

- "A core already spinning can start in nanoseconds" is qualitative; no source gives one number for it.
- The vendor microsecond figure is AMD's own and depends on the CPU and kernel.
- The lab figure is a shared-memory round trip, not a NIC receive path, and is labelled as such on screen.
