# net-03-bypass: Kernel bypass with Onload, ef_vi and DPDK

Key facts and sources

- Onload: user-level TCP/UDP stack, binary compatible with BSD-sockets apps, launched with the `onload` prefix (Xilinx/onload README: https://github.com/Xilinx/onload). It intercepts libc calls via LD_PRELOAD and will not accelerate statically linked apps; it gives each app a protected virtual NIC (VNIC); kernel transitions cost "the equivalent of hundreds or thousands of instructions"; responding to an interrupt and switching threads can take "on the order of a microsecond"; EF_POLL_USEC sets the spin time before blocking; tcpdump/wireshark do not capture accelerated packets (onload_tcpdump does). AMD Onload User Guide UG1586 v1.5: https://docs.amd.com/r/en-US/ug1586-onload-user/Resources
- "ef_vi is a network layer 2 API"; TCPDirect is available for SFN8000, X2 and X3 adapters (UG1586).
- Vendor figures (UG1586, X2 Low Latency Quickstart: Dell R230, Xeon E3-1240 v6, X2522-25G back to back, RHEL 7.4): 1/2 RTT median for a 32-byte message at 25 Gb: ef_vi 750 ns, TCPDirect UDP 783 ns, Onload UDP 1022 ns (sfnt-pingpong) / 1034 ns (netperf), kernel UDP 2658 ns. Shown as "Onload about 1,030". https://docs.amd.com/r/en-US/ug1586-onload-user/Latency-Test-Results
- DPDK: PMDs "access Rx and Tx descriptors directly in a polling mode without relying on interrupts" (https://doc.dpdk.org/guides/prog_guide/ethdev/ethdev.html); the port is unbound from its kernel driver and bound to vfio-pci, after which Linux cannot use it (https://doc.dpdk.org/guides/linux_gsg/linux_drivers.html).
- Onload can also run over AF_XDP, with less acceleration than ef_vi (Onload README).
- Lab: rx thread does every syscall, BatchReceiver of 32 per recvmmsg (libs/feed/src/receiver.cpp); book thread reads an SPSC ring (docs/core-plan.md); Aeron IPC has no syscalls on the data path (docs/aeron.md).

Unsure / simplified

- The DPDK loop on screen is pseudo-code (`rx_burst`), not the exact rte_eth_rx_burst signature.
- Bifurcated-driver NICs that keep a kernel interface under DPDK are not covered.
