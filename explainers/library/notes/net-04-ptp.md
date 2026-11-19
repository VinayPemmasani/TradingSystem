# net-04-ptp: Hardware timestamps and PTP

Key facts and sources

- EU clock rules: for high-frequency algorithmic trading, maximum divergence from UTC 100 µs and timestamp granularity 1 µs or better. Commission Delegated Regulation (EU) 2017/574, Annex Table 2: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0574
- SO_TIMESTAMPING requests software and/or hardware stamps; the hardware stamp is returned in the ancillary data (ts[2]); transmit stamps come back via the socket error queue (MSG_ERRQUEUE). Linux kernel docs: https://www.kernel.org/doc/html/latest/networking/timestamping.html
- PTP Sync / Delay_Req / Delay_Resp exchange, offset = ((t2-t1)-(t4-t3))/2, delay = ((t2-t1)+(t4-t3))/2, symmetric-path assumption. IEEE 1588 overview (NIST): https://www.nist.gov/el/intelligent-systems-division-73500/ieee-1588 ; worked notes: https://people.cs.rutgers.edu/pxk/417/notes/ptp.html
- ptp4l uses hardware timestamping by default and supports boundary, ordinary and transparent clocks: https://linuxptp.nwtime.org/documentation/ptp4l/ ; phc2sys "synchronizes two or more clocks": https://linuxptp.nwtime.org/documentation/phc2sys/
- Lab: rdtsc/rdtscp stamps and TscClock::calibrate against CLOCK_MONOTONIC over 50 ms at startup (libs/core clock.hpp in /home/claude/ts-push).

The worked example (t1 = 1000, t2 = 1650, t3 = 2000, t4 = 2250 ns) is made-up numbers for illustration; it gives offset 200 ns and delay 450 ns.

Unsure / simplified

- The exact way a transparent clock reports residence time (the correctionField update rules in IEEE 1588-2019) is not described; I could not read the standard itself, so the video says only that transparent clocks "correct for the time each message spent inside them".
- The "few nanoseconds" cost of rdtsc is qualitative and depends on the CPU.
- One-step vs two-step clocks (Follow_Up) are left out.
