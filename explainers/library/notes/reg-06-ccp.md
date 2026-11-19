# reg-06-ccp: Clearing and central counterparties

## Key facts and sources
- **PFMI** (CPMI-IOSCO, Apr 16, 2012): CCP "interposes itself between counterparties ... becoming the buyer to every seller and the seller to every buyer" (¶1.13). https://www.bis.org/cpmi/publ/d101a.pdf
- **Margin standard:** initial margin to a single-tailed confidence of at least 99%, variation margin at least daily (intraday when appropriate). I read this in RBA CCP Standard 6.3-6.4, which implements PFMI Principle 6: https://rba.gov.au/payments-and-infrastructure/financial-market-infrastructure/clearing-and-settlement-facilities/standards/central-counterparties/2012/standard-6.html
- **Netting:** "Every day, netting at NSCC reduces the value of payments that need to be exchanged by an average of 98% or more." DTCC, Jun 2021: https://www.dtcc.com/dtcc-connection/articles/2021/june/14/us-settlement-cycle-myth-buster
- **Waterfall (CME base products):** defaulter's performance bond and guaranty fund contribution; CME contribution $100 million; non-defaulters' guaranty fund; capped assessments. https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-financial-safeguards-waterfalls.html (2020). Cover 2: https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-stress-testing-practices.html
- **Lab:** drop copy Execution Report, Match Number at offset 40, same number as OUCH and ITCH Order Executed (docs/specs/dropcopy-layout.md).
- Variation margin example (10 contracts x $50/point x 20 points = $10,000) is illustrative.

## Unsure / left out
- I could not read the PFMI key considerations directly (PDF truncated); the 99% and daily VM wording is from the RBA standard.
- CME's current $100 million figure may have changed since 2020.
- Guaranty fund sizes: not stated.
