# ac-02-options: Listed equity options

Key facts and sources
- OCC 2025 total contract volume 15,263,912,452 (+24.3%), ADV 60.8 million; equity 8.27 bn, ETF 5.68 bn, index 1.26 bn: OCC, "Annual 2025 and December 2025 volume", https://www.theocc.com/newsroom/views/2026/01-05-occ-annual-2025-and-december-2025-volume
- OCC is a central counterparty and serves "20 exchanges and trading platforms": https://www.theocc.com/company-information/what-is-occ
- OPRA participants cover about 20 exchanges, SIAC is the processor, and quote traffic is "the vast majority": https://www.opraplan.com/faqs . Cboe's 2025 review says a planned MEMX venue "would bring the count to 20 exchanges", i.e. 19 today, hence "about 20".
- OPRA projected 13.575 bn messages/day for July 2026, one stream only: OPRA Capacity Projections Update (Sept 2025), https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf
- Standard equity option = 100 shares, American-style, exercise delivers stock T+1: OCC equity options specs, https://www.theocc.com/clearance-and-settlement/clearing/equity-options-product-specifications
- SPX: European, cash-settled, $100 per index point; SPXW expiries Monday–Friday: Cboe SPX fact sheet, https://cdn.cboe.com/resources/spx/spx-fact-sheet.pdf
- 0DTE SPX = 59% of SPX volume in 2025: Cboe, "The State of the Options Industry: 2025", https://www.cboe.com/insights/posts/the-state-of-the-options-industry-2025
- Lab: vendor Server conflates per subscription, /home/claude/ts-push/libs/vendor/include/lab/vendor/server.hpp. Lab ITCH day 368,366,634 messages (/mnt/project-files/quant-real/script.log).

Unsure / left out
- The call quote, delta 0.5 and the +$0.50 move are illustrative (delta-only, no gamma).
- The bar chart compares a 2026 OPRA projection with a 2019 Nasdaq day replayed in the lab; it is labelled as such but they are different years and feeds.
- Exact number of US options exchanges (19 vs 20) differs by source and counting; the video says "about 20".
- No premium-settlement timing, tick sizes or payment-for-order-flow figures.
