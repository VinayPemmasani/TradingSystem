# md-09-ab-lines: A/B line arbitration (178 s)

Key facts and sources
- CME "strongly recommends" processing both the A and B incremental feeds ([CME MDP 3.0 Recovery Services](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457325847/MDP+3.0+-+Recovery+Services)). CME also offers TCP recovery and the market recovery snapshot loop (same page).
- OPRA sends every message on two redundant streams ([OPRA Binary Data Recipient Interface Specification v6.4c](https://cdn.opraplan.com/documents/OPRA_Pillar_Output_Specification.pdf)).
- On Cboe, the A and B feeds have identical content, but their framing may differ, so arbitrate by unit and sequence. Recovery is through the spin server ([Cboe Multicast PITCH spec](https://cdn.cboe.com/resources/techspec/technical-specifications-cboe-titanium-u-s-equitiesoptions-multicast-pitch-specification.pdf)).
- MoldUDP64 re-requests are covered in video 02 ([Nasdaq MoldUDP64 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf)).
- Lab tie-in: the `libs/mold` sequencer drops duplicates, holds messages ahead of a gap in a preallocated window, and waits gap_delay_us 100 before the first request (`libs/feed/include/lab/feed/receiver.hpp`). The lab runs one line.

Worked example: A loses 102 and B loses 104. The run is illustrative. "First copy wins, so the merged feed is as fast as the faster line" follows from the algorithm; it is not a measurement.

Unsure / left out: whether Nasdaq itself publishes A/B lines (not verified), and any loss-rate statistics.
