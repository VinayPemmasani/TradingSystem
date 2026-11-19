# ex-06-fees: Maker-taker fees, rebates and inverted venues

## Key facts and sources
- **Rule 610(c) access-fee cap:** $0.003 per share for protected quotes at or above $1, and 0.3% of the quote price below $1. The Sept 2024 amendments lower it to $0.001 (0.1% below $1), but compliance is delayed to the first business day of November 2027. So the old cap still applies.
  - 2024 rule: Release 34-101070 (https://www.sec.gov/rules/final/2024/34-101070.pdf)
  - Delay order: https://public-inspection.federalregister.gov/2026-11997.pdf
  - Current rule text: https://www.ecfr.gov (17 CFR 242.610)
- **Nasdaq equity price list (read Nov 2026):**
  - Standard remove fee: $0.0030 per share (≥ $1).
  - Base displayed add credit: $0.0018 (Tape A/B); Tape C is $0.0013.
  - Highest general tier credit: $0.00305, for members adding more than 1.50% of volume.
  - Source: https://nasdaqtrader.com/Trader.aspx?id=PriceListTrading
- **Cboe BYX standard rates (≥ $1), effective Oct 19, 2026:** adding displayed liquidity is a $0.00200 fee, and removing liquidity earns a $0.00020 rebate. Source: https://cboe.com/us/equities/membership/fee_schedule/byx/
- **Worked example:** this is arithmetic on those base rates, with an illustrative $20.00 × $20.01 quote. The best-to-worst gap is $0.0148 × 10,000 = $148.
- **Lab:**
  - simex sets the OUCH liquidity flag to A for the resting order and R for the aggressor (exchange/simex/matcher.cpp). Crosses get O, C or H (docs/specs/ouch50-layout.md).
  - README.md: "no fees or rebates are counted".

## Unsure / left out
- "Routers that count fees send orders there first" is the stated rationale for inverted pricing. The video gives no statistic for how much faster fills are, because I found no primary source with a number.
- The video shows base rates only. Tier qualifications change monthly.
