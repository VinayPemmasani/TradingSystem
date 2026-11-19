# net-07-nagle: Nagle, delayed ACK and TCP_NODELAY

Key facts and sources

- Nagle, RFC 896 (6 January 1984), "Congestion Control in IP/TCP Internetworks": a one-byte keystroke becomes a 41-byte packet (40 bytes of headers), 4000% overhead; fix: while unacknowledged data is outstanding, hold new small data until an ACK arrives or a full segment builds up. https://www.rfc-editor.org/rfc/rfc896.txt
- RFC 1122 section 4.2.3.2: a TCP SHOULD implement delayed ACK, the delay MUST be less than 0.5 s, and in a stream of full-sized segments there SHOULD be an ACK for at least every second segment. Section 4.2.3.4: TCP SHOULD implement Nagle and MUST allow an application to disable it. https://datatracker.ietf.org/doc/html/rfc1122#section-4.2.3.2
- Linux delayed ACK bounds: TCP_DELACK_MIN = HZ/25 (40 ms), TCP_DELACK_MAX = HZ/5 (200 ms), include/net/tcp.h: https://raw.githubusercontent.com/torvalds/linux/master/include/net/tcp.h
- tcp(7): TCP_NODELAY disables Nagle so segments are sent as soon as possible; TCP_QUICKACK "is not permanent". https://man7.org/linux/man-pages/man7/tcp.7.html
- TCP header minimum 20 bytes (RFC 9293), plus 20 for IPv4: https://www.rfc-editor.org/rfc/rfc9293.txt
- Lab: TcpStream calls set_nodelay in its constructor; send queues what the kernel will not take into out_, and flush drains it (libs/net/src/tcp.cpp in /home/claude/ts-push).

Unsure / simplified

- The collision scene is schematic: the actual stall depends on the peer's delayed-ACK timer state and on whether it has data to send back.
- "Tens of milliseconds" is a range from the Linux bounds above, not a measurement.
