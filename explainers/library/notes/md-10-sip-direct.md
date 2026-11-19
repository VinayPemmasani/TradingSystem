# md-10-sip-direct: SIP vs direct feeds (173 s)

Key facts and sources
- Tape C covers Nasdaq-listed stocks under the UTP plan ([UTP plan overview](https://utpplan.com/PageParts/Overview.html)).
- The UTP SIP's median quote latency was 12.8 µs in Q2 2024 ([UTP statistics Q2 2024](https://utpplan.com/DOC/UTP_Website_Statistics_Q2-2024-June.pdf)). The year and source appear on screen.
- Rule 603(a) of Reg NMS: an exchange may not release data on its proprietary feeds before it sends that data to the processor. NYSE's OpenBook Ultra ran ahead of the SIP from June 2008, by milliseconds to seconds, and NYSE paid a $5 million penalty ([SEC order 34-67857, 14 Sept 2012](https://www.sec.gov/litigation/admin/2012/34-67857.pdf)).
- On 9 Dec 2020 the SEC adopted the market data infrastructure rules: odd lots, 5 levels of depth and auction information in core data, plus competing consolidators. The SEC describes the exclusive SIP model as dating to the late 1970s ([SEC press release 2020-311](https://www.sec.gov/news/press-release/2020-311)).
- Lab tie-in: the vendor `Consolidator` builds Level 1 records from direct ITCH books (`libs/vendor`).

Worked example: the NBBO moving from 10.00 to 10.01 is illustrative.

Unsure / left out: where exactly UTP measures its latency (the report does not define it), the names of the CTA/SIAC processors, and the implementation status of the 2020 rules.
