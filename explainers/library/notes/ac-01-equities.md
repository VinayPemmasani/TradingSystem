# ac-01-equities: Cash equities

Key facts and sources
- 29 national securities exchanges registered under Exchange Act s.6(a), some of them options-only (SEC list, last updated 7 Jan 2026): https://www.sec.gov/about/divisions-offices/division-trading-markets/national-securities-exchanges
- T+1 standard settlement from 28 May 2024, covering equities, ETFs and corporate and government debt: https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor-bulletin
- Global equity market capitalisation USD 151.94 tn at end-2025 (shown as "about $152 trillion"): WFE FY 2025 Market Highlights, https://www.world-exchanges.org/our-work/articles/fy-2025-market-highlights (report PDF linked there).
- NSCC is the central counterparty for virtually all broker-to-broker trades and nets them through CNS; DTC moves securities by book entry; netting rate 98.6% (as shown on the DTCC CNS page, Q3 2026): https://www.dtcc.com/products-and-services/clearing-settlement-services/equities-clearing/cns
- Nasdaq opening cross 9:30 and closing cross 4:00 p.m. ET: Nasdaq Opening/Closing Cross FAQ, https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf
- Reg NMS Rule 611: trading centers must have policies and procedures to prevent trade-throughs of protected quotations: 17 CFR 242.611, https://www.law.cornell.edu/cfr/text/17/242.611
- Lab: 368,366,634 ITCH messages in the 30 Jan 2019 Nasdaq TotalView-ITCH day (/mnt/project-files/quant-real/script.log); itch-fh, simex and OUCH from /home/claude/ts-push/README.md.

Unsure / left out
- The three-exchange NBBO example and order sizes are illustrative.
- No off-exchange market share figure and no tick-size rule: the SEC's 2024 Rule 612 half-penny amendments have had their compliance dates moved, and I could not confirm the status as of today, so the video does not mention tick sizes.
- 17 CFR 242.600 now defines the NBBO as disseminated by a competing consolidator or self-aggregator (2020 market data infrastructure rules). The video describes the exclusive SIP model, which I believe is still how the NBBO is published in practice; I did not confirm the competing-consolidator rollout status.
