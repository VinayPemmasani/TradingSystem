# net-09-capture: Packet capture, taps and wire-to-wire latency

Key facts and sources

- SPAN oversubscription: when the source ports carry more than the destination port can, packets drop at the destination's egress buffer. Cisco SPAN guide: https://www.cisco.com/c/en/us/td/docs/dcn/hyperfabric/software/cisco-nexus-hyperfabric-configure-span.html
- Taps vs SPAN: SPAN traffic is low priority in the switch; passive taps pass every packet in order. Gigamon white paper: https://www.gigamon.com/content/dam/resource-library/english/white-paper/wp-tap-vs-span.pdf
- pcap format: 24-byte file header with SnapLen; magic 0xA1B2C3D4 means microsecond timestamps, 0xA1B23C4D nanosecond; 16-byte record header (seconds, fraction, captured length, original length). IETF draft: https://www.ietf.org/archive/id/draft-ietf-opsawg-pcap-04.html
- Lab: the feed receiver stamps each batch with rdtsc; the stamp is carried in Aeron's reserved_value field (docs/aeron.md); LatencyHistogram prints count, min, p50, p90, p99, p99.9, p99.99 and max (libs/core/include/lab/core/histogram.hpp); scripts/wsl-setup.sh installs tcpdump and tshark (/home/claude/ts-push).

The 4.1 µs wire-to-wire example is an illustration, not a measurement.

Unsure / simplified

- Real capture appliances also do hardware timestamping on ingress and may use PTP-disciplined clocks; product details are left out.
- "Storage fills fast at line rate" is qualitative.
- Matching an order to its trigger packet needs application knowledge (for example a client order ID derived from the triggering sequence number); this is shown only schematically.
