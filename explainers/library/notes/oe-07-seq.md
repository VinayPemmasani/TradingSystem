# oe-07-seq: Sequence numbers, resends and gap fill

Key facts and sources
- FIX session rules: MsgSeqNum (34) persists across reconnects unless Logon carries ResetSeqNumFlag (141) Y; higher than expected: ResendRequest (2) from the expected number with EndSeqNo (16) 0 = to the end, and nothing later is processed until the gap is filled; lower with PossDupFlag (43) Y: ignored; lower without: Logout and disconnect. Resends carry PossDupFlag Y and OrigSendingTime (122); SequenceReset-GapFill (35=4, 123=Y, 36 NewSeqNo) covers session messages. Heartbeat after HeartBtInt (108) seconds without traffic; TestRequest after HeartBtInt plus grace, disconnect if unanswered; lab default 30 s (`libs/fix/include/lab/fix/session.hpp`). SoupBinTCP Login Accepted carries the next Sequence Number (`docs/specs/soupbintcp-layout.md`). Source: lab spec `docs/specs/fix44-subset.md`; [OnixS FIXT 1.1 Message Recovery](https://www.onixs.biz/fix-dictionary/FIXT1.1/section_message_recovery.html) (session messages never resent: Logon, Logout, ResendRequest, Heartbeat, TestRequest, SequenceReset; a sender may gap fill over application messages it chooses not to retransmit, such as aged orders; lower without PossDup: "strongly recommended that the session be terminated").
- SoupBinTCP: sequenced data carries no number; re-login with the next number replays. Source: lab spec `docs/specs/soupbintcp-layout.md`.
- Lab: `libs/fix/include/lab/fix/session.hpp` (store 32 MB / 2^20 messages, gap fill beyond; a too-high message is not processed and comes back in the resend); `tools/fix-client --reconnect-at N` drops the TCP connection without Logout and checks every report arrives by resend.

Worked example (illustrative): expected 41, 44 arrives; GapFill 41 to 42, 42 resent, GapFill 43 to 44, 44 resent.

Unsure / left out: the FIX Trading Community session spec PDF itself was not fetched; rules were checked against the OnixS FIXT 1.1 pages and the lab spec.
