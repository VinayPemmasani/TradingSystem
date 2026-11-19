# reg-03-knight: Knight Capital, 1 August 2012

## Key facts and sources
- **Primary source:** SEC Order, In re Knight Capital Americas LLC, Release 34-70694 (Oct 16, 2013), read via https://contracts.justia.com/companies/kcg-holdings-inc-18985/contract/555902 ; press release https://www.sec.gov/news/press-release/2013-222 (first SEC action under the market access rule; $12 million penalty).
- **Event:** loss of "over $460 million" (¶1); about 45 minutes (¶17); 212 parent orders; 4 million executions in 154 stocks, more than 397 million shares; ~$3.5 billion net long in 80 stocks and ~$3.15 billion net short in 74 (¶17).
- **Code:** Power Peg unused since 2003; in 2005 the cumulative-quantity function was moved and Power Peg not retested (¶14); RLP code (NYSE Retail Liquidity Program, to start Aug 1, 2012) repurposed the Power Peg flag (¶¶12-13); a technician did not copy the new code to one of eight SMARS servers (¶15). Removing the new code from the other seven made it worse (¶27).
- **Controls:** 97 BNET emails from ~8:01 a.m. ET, "Power Peg disabled", not acted on before the open (¶19); PMON relied on human monitoring, no automated alerts (¶25); 33 Account had a $2 million gross limit not linked to automated controls (¶23); no procedures to halt SMARS (¶21).
- **Rule 15c3-5:** adopted Nov 3, 2010 (https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm); initial compliance July 14, 2011 (order fn. 2). Also Reg SHO 200(g), 203(b) violations (not in video).
- **Lab:** firm/risk risk.hpp position check (shares + open_buy + added vs max_position 2,000), 2,000 orders/s token bucket, kill switch; drop copy spec.

## Unsure / left out
- End time of the event and Knight's market share: not in the sources I read.
- "Delete dead code / never reuse a flag" are lessons, not SEC findings.
