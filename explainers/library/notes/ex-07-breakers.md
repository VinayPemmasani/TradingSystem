# ex-07-breakers: Circuit breakers, LULD and volatility halts

## Key facts and sources
- **LULD bands:**
  - Tier 1 (S&P 500, Russell 1000, some ETPs) above $3: 5%. Tier 2 above $3: 10%.
  - $0.75–$3.00: 20%. Below $0.75: the lesser of $0.15 or 75%.
  - The reference price is the mean price over the prior 5 minutes, updated when it moves at least 1%.
  - Bands double from 3:35 to 4:00 p.m. for Tier 1, and for Tier 2 stocks at or below $3.
  - A limit state that lasts 15 seconds leads to a 5-minute trading pause, followed by a reopening auction.
  - Sources: https://www.luldplan.com, https://finra.org/investors/insights/guardrails-market-volatility, https://m.nasdaqtrader.com/content/MarketRegulation/LULD_FAQ.pdf
- **Market-wide circuit breakers:**
  - S&P 500 falls of 7% (Level 1), 13% (Level 2) and 20% (Level 3), measured from the prior close.
  - Level 1 and Level 2 halt trading for 15 minutes if hit before 3:25 p.m.; Level 3 halts trading for the rest of the day.
  - March 2020 Level 1 halts: Mar 9 at 9:34:13, Mar 12 at 9:35:44, Mar 16 at 9:30:01 and Mar 18 at 12:56:17.
  - Source: SEC Release 34-92428 (https://sec.gov/files/rules/sro/nyse/2021/34-92428.pdf)
- **Rule 201 (Reg SHO):** a 10% intraday decline triggers the short-sale price test for the rest of the day and the next day. Source: 17 CFR 242.201.
- **Worked example:** $50 × 5% = $2.50, giving a band of $47.50 to $52.50. The price path and reopening are illustrative.
- **Lab:**
  - exchange/simex/scenarios.hpp defaults: 5% band, 15 s limit state, 300 s pause, Reg SHO at a 10% drop.
  - matcher.cpp: check_limit and pause (reason LUDP), then a J collar with up to 3 extensions.
  - The MWCB scenario uses an index of 5,000.00 with levels at 4,650, 4,350 and 4,000. The reference is the first trade, or the reopening price after a cross.
  - Orders are repriced into the band by engine.hpp banded().

## Unsure / left out
- Flash-crash (May 2010) statistics: I did not re-read a primary source this session.
- The 2021 Working Group study figures.
- The video simplifies the limit state to "a quote on the band".
- Exact Plan definitions: a limit-down state is the National Best Offer at the Lower Price Band.
