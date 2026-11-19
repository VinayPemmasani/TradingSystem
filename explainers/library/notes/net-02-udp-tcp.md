# net-02-udp-tcp: UDP vs TCP in trading

Key facts and sources

- UDP header is 4 x 16-bit fields (source port, destination port, length, checksum) = 8 bytes; "delivery and duplicate protection are not guaranteed". RFC 768: https://www.rfc-editor.org/rfc/rfc768.txt
- TCP provides "a reliable, in-order, byte-stream service"; header is a multiple of 32 bits with a 20-byte minimum (Data Offset 5); three-way handshake. RFC 9293 sections 2.2, 3.1, 3.4.1: https://www.rfc-editor.org/rfc/rfc9293.txt
- RTO: initial 1 s, SHOULD round up to 1 s minimum, doubles on expiry (RFC 6298: https://www.rfc-editor.org/rfc/rfc6298.txt). Linux uses TCP_RTO_MIN = HZ/5 = 200 ms (include/net/tcp.h: https://raw.githubusercontent.com/torvalds/linux/master/include/net/tcp.h), so "at least 200 ms on Linux" when the timer fires.
- MoldUDP64: 20-byte header (Session 10, Sequence Number 8, Message Count 2); heartbeat = count 0 about once a second carrying the next sequence number; 20-byte unicast re-request. Lab docs/specs/moldudp64-layout.md, from Nasdaq MoldUDP64 v1.00: https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf
- SoupBinTCP: 2-byte length + 1-byte type; login with Requested Sequence Number; heartbeats after 1 s idle. Lab docs/specs/soupbintcp-layout.md (Nasdaq SoupBinTCP 3.00).
- Lab: RxPacket::kMaxLen = 1472 (1500 MTU - 20 IP - 8 UDP), ReceiverConfig gap_delay_us 100, timeout_ms 20, retries 10 (libs/feed/include/lab/feed/receiver.hpp); TcpStream sets TCP_NODELAY and queues unsent bytes (libs/net/src/tcp.cpp).

Unsure / simplified

- "Fast retransmit costs at least a round trip" is stated qualitatively; no Linux fast-retransmit timing is given.
- The 6-packet loss scene is schematic.
