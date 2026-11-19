# md-08-feed-depth: Level 1, 2 and 3 (169 s)

Key facts and sources
- Order-by-order feeds: ITCH reports adds, executions, cancels and deletes by order reference number ([Nasdaq ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf)). Cboe PITCH does the same ([Cboe PITCH spec](https://cdn.cboe.com/resources/techspec/technical-specifications-cboe-titanium-u-s-equitiesoptions-multicast-pitch-specification.pdf)). CME also offers market by order (MBOFD) ([CME MDP 3.0 incremental refresh](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457227795/MDP+3.0+-+Market+Data+Incremental+Refresh+-+MBP+and+MBOFD)).
- Price-level feeds: CME market by price carries size (271) and order count (346) per level, to a fixed depth set by tag 264 ([CME MBP Multiple Depth Book](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457574047/MDP+3.0+-+Market+by+Price+-+Multiple+Depth+Book)).
- Consolidated top of book: in the US the SIPs publish the NBBO and last sale ([SEC release 2020-311](https://www.sec.gov/news/press-release/2020-311); [UTP plan overview](https://utpplan.com/PageParts/Overview.html)).
- Lab tie-in: `libs/book` BookBuilder keeps an order store and price-level sides. The vendor `Consolidator` builds Level 1 records (bid, ask, sizes, last trade, status) from those books (`libs/vendor`, `CLAUDE.md`). The claim that the best price sits at the back of each side comes from the lab's book code.

Worked example: three orders at 189.25 (300, 100, 200), then the 100 is cancelled. The numbers are illustrative.

Unsure / left out: the product names for each level (for example Nasdaq Basic and TotalView) and their contents, since I did not verify them this session.
