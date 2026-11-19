# oe-08-throttles: Throttles and message rate limits

Key facts and sources
- CME Globex messaging controls (production, per iLink session, fixed three-second interval starting with the first message): New Order, Cancel/Replace and similar: reject at 1,500 messages (average 500/s), terminate at 2,250 (average 750/s); Cancel and Order Mass Action: reject at 3,000, terminate at 4,500. Past the reject threshold, messages get Business Message Reject 35=j 380=8 for the rest of the interval; at terminate, the session is terminated (ErrorCodes 9). Source: [CME client systems wiki, Messaging Controls](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457317540/Messaging+Controls), read 19 Nov 2026.
- Lab: token bucket in `firm/risk/include/lab/risk/risk.hpp`, 2,000 orders/s, burst 100, refilled from rdtsc ticks (tokens per tick computed once in the constructor; refill multiplies elapsed ticks, adds, caps at burst); last of the risk checks; new orders and replaces spend tokens, cancels are never checked; `firm/trader/trading.cpp` prints blocks per reason.

Worked example: fixed-window edge case (1,500 + 1,500 across a window boundary) is arithmetic, not a CME statement.  150 orders at once with a full bucket of 100: 100 pass, 50 blocked; at 2 tokens/ms the bucket holds 50 after 25 ms.

Unsure / left out: the CME page lives in a space named EPICSANDBOX on CME's client wiki; values may change, so the video labels them "read Nov 2026". Other venues' throttles were not checked. The risk-block printout on screen is illustrative.
