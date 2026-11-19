# ms-06-dark: Dark pools

## Key facts and sources
- Q1 2022: 16 exchanges 59.7% of NMS share volume, 32 ATSs 10.2%, six wholesalers 23.9%, other 6.3% (SEC order competition proposal, FR Jan 3, 2023). https://www.federalregister.gov/documents/2023/01/03/2022-27617/order-competition-rule
- Form ATS-N adopted July 18, 2018; ATSs ≈ 11.4% of NMS share volume per the release. https://www.sec.gov/news/press-release/2018-136
- Barclays ($70M) and Credit Suisse ($84.3M), Jan 31, 2016, SEC + NY AG; Barclays did not police toxic flow as promised and used slower feeds than described for NBBO. https://www.sec.gov/news/press-release/2016-16
- FINRA ATS transparency data (per-ATS volume by stock): https://finra.org/filing-reporting/otc-transparency/ats-quarterly-statistics
- Lab: docs/specs/ouch50-layout.md Display 27:1 (Y visible, N hidden; simex shows every order); exchange/simex/liquidity.hpp ignores P/Q trades that never touched the visible book.

## Worked numbers (mine)
- Mid peg: NBBO 30.00/30.02 → 20,000 @ 30.01, 1¢ × 20,000 = $200 per side. Stale-mid chart is an illustration.

## Unsure / left out
- Latest FINRA quarterly ATS share (spreadsheet download blocked by the proxy); used the SEC's Q1 2022 figure instead. FINRA publication delay not stated.
