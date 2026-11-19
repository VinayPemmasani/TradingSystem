# md-05-cme-mdp3: CME MDP 3.0 (179 s)

Key facts and sources
- Each channel has incremental feeds A and B, and CME "strongly recommends" processing both. The market recovery feeds loop snapshots, and the instrument definitions arrive on their own loop. Sources: [MDP 3.0 Recovery Services](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457325847/MDP+3.0+-+Recovery+Services) and the [CME client wiki](https://cmegroupclientsite.atlassian.net/wiki/x/UoBIGw).
- The packet header is MsgSeqNum (uint32) followed by SendingTime (uint64, ns since the epoch). Each message has a 2-byte MsgSize and then the 8-byte SBE header. Everything is little-endian, and in CME's example the bytes A6 BB 0A 00 decode to 703398. Sources: [MDP 3.0 SBE Decoding Example](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457638169/MDP+3.0+-+SBE+Decoding+Example) and [Simple Binary Encoding](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457418645/MDP+3.0+-+Simple+Binary+Encoding).
- Template 46, MDIncrementalRefreshBook, has tags 60 and 5799, then a group of entries with tags 48, 83 RptSeq (per instrument), 270, 271, 346, 1023, 279 (0 new, 1 change, 2 delete) and 269 (0, 1, E, F). Source: [Incremental Refresh MBP and MBOFD](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457227795/MDP+3.0+-+Market+Data+Incremental+Refresh+-+MBP+and+MBOFD).
- In market by price, New shifts the levels below it down and Delete shifts them up. Book depth comes from tag 264 in the instrument definition. Source: [Market by Price, Multiple Depth Book](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457574047/MDP+3.0+-+Market+by+Price+-+Multiple+Depth+Book).
- To recover from a snapshot: tag 369 LastMsgSeqNumProcessed tells you which queued incrementals the snapshot already covers. Discard any with a sequence number below it, and skip entries whose RptSeq is at or below the snapshot's. Source: [Snapshot Full Recovery](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457736274/MDP+3.0+-+Market+Data+Snapshot+-+Full+Recovery).

Worked example: the five-deep bid ladder is illustrative.

Unsure / left out: the snapshot template ID (only vendor documentation gives it), typical book depths, and message rates.
