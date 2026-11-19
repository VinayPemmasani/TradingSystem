# ex-05-ticks: Tick sizes, lot sizes and why they matter

## Key facts and sources
- Rule 612 minimum pricing increment: $0.01 for quotes at or above $1.00, and $0.0001 below $1.00. Source: 17 CFR 242.612 (https://www.ecfr.gov/current/title-17/chapter-II/part-242/subject-group-ECFR3dd95cf4d3/section-242.612).
- Sept 18, 2024 amendments: a $0.005 increment for NMS stocks whose time-weighted average quoted spread is at most $0.015. Source: Release 34-101070 (https://www.sec.gov/rules/final/2024/34-101070.pdf).
- Compliance with Rule 612, Rule 610(c) and 600(b)(89)(i)(F) was first delayed to November 2026, then to the first business day of November 2027. Source: SEC order, June 2026 (https://public-inspection.federalregister.gov/2026-11997.pdf). The video says one cent "still applies today".
- Round-lot tiers by price: 100 shares up to $250.00, 40 for $250.01–1,000, 10 for $1,000.01–10,000, and 1 above $10,000. Source: Release 34-101070.
- E-mini S&P 500: $50 × the index, with a minimum fluctuation of 0.25 index points, so one tick is $12.50. Source: CME Rulebook chapter 358 (https://www.cmegroup.com/rulebook/CME/IV/350/358/358.pdf).
- Three-Month SOFR futures: 0.0025 (a quarter of a basis point, $6.25) in the nearest expiries, and 0.005 ($12.50) in the others. Source: CME contract specs (https://www.cmegroup.com/content/dam/cmegroup/education/files/sofr-futures-contract-specifications.pdf).
- Lab facts:
  - Price(4) fixed point; one cent is 100 (exchange/agents/main.cpp kTick, market_maker.hpp tick).
  - The engine checks only that price > 0, price ≤ 1,999,999,900 (199,999.99), and quantity ≤ 999,999 (engine.hpp validate()). It has no tick check.
- The $10.00 and $500 basis-point figures are arithmetic. The books and the ES price level are illustrative.

## Unsure / left out
- I could not confirm whether the price-based round-lot definition is already in force or is covered by the delay orders. The video shows the tiers without a compliance date.
- I left out the proposed rescission of Rule 611 and options penny-pilot ticks.
