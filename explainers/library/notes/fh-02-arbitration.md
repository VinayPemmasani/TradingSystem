# fh-02-arbitration: Arbitrating A and B multicast in code

Key facts and sources:

- CME MDP 3.0: "All packets are sent through both UDP Feed A and UDP Feed B" and "UDP Feed A and UDP Feed B should be used for arbitration." Source: [CME MDP 3.0 – Dissemination](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457222936/MDP+3.0+-+Dissemination).
- The lab's feed has a single line (no A/B code exists in the repo). Its MoldUDP64 sequencer's `accept()` delivers `seq == expected_`, counts `seq < expected_` as a duplicate, and holds anything above; held duplicates are also dropped. Source: `libs/mold/include/lab/mold/sequencer.hpp` (lab repo /home/claude/ts-push).
- The sequencer rejects packets from a different MoldUDP64 session (`wrong_session`), so both lines must carry the same session for one sequencer to arbitrate them. Same file.
- The fault injector sends duplicates on purpose (`FaultConfig::duplicate`). Source: `libs/mold/include/lab/mold/fault_injector.hpp`.

Illustrative: the worked example (A loses 1003 and 1005, B loses 1002, B 40 µs behind) is invented; the hold-then-release timing follows the sequencer's rules exactly.

Unsure / left out: I did not state which other venues besides CME publish A/B lines, how far apart lines typically run, or whether every venue's A and B packets are byte-identical; I could not verify these from a primary source this session. Protocol layouts are left to the md-* videos.
