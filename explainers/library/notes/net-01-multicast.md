# net-01-multicast: Multicast and IGMP for market data

Key facts and sources

- Host group (class D) addresses run 224.0.0.0 to 239.255.255.255; an IP group maps to Ethernet by putting its low-order 23 bits into 01-00-5E-00-00-00, so with 28 significant bits several groups (32) share one MAC. RFC 1112 sections 4 and 6.4: https://www.rfc-editor.org/rfc/rfc1112.txt
- 239.0.0.0 to 239.255.255.255 is the administratively scoped range. RFC 2365 section 4: https://www.rfc-editor.org/rfc/rfc2365.txt
- IGMPv3: IP protocol 2, TTL 1, Router Alert; reports to 224.0.0.22; general queries to 224.0.0.1; defaults Robustness 2, Query Interval 125 s, Query Response Interval 10 s, so Group Membership Interval 260 s; INCLUDE/EXCLUDE source filter modes. RFC 3376 sections 2, 4, 8: https://www.rfc-editor.org/rfc/rfc3376.txt
- IGMP snooping: forward by group-based port membership tables and always to router ports; use a membership timeout; non-IGMP 224.0.0.X goes to all ports. RFC 4541: https://www.rfc-editor.org/rfc/rfc4541.txt
- Lab: `UdpSocket::receiver` binds the group address (not INADDR_ANY), sets SO_RCVBUF (default 16 << 20), joins with IP_ADD_MEMBERSHIP on the given interface (libs/net/src/udp.cpp). `scripts/wsl-setup.sh` runs `ip route replace 239.0.0.0/8 dev lo`; simex publishes on 239.1.1.2:31001 (exchange/simex/main.cpp).

Unsure / simplified

- "Lose the querier and snooping switches can age out your port" is the RFC 4541 membership-timeout behaviour; exact ageing varies by switch vendor and configuration, so the video gives no number.
- The unicast-vs-multicast picture is schematic (6 subscribers); no exchange's subscriber count is claimed.
- No specific exchange multicast group or channel numbers are shown.
