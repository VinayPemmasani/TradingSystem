# reg-04-flash-crash: The 6 May 2010 flash crash

## Key facts and sources
- **Primary source:** "Findings Regarding the Market Events of May 6, 2010", staffs of the CFTC and SEC, Sep 30, 2010: https://www.sec.gov/files/marketevents-report.pdf
- Sell program: 75,000 E-mini contracts (~$4.1 billion) from 2:32 p.m., algorithm at 9% of prior minute's volume, without regard to price or time; executed in ~20 minutes; the same trader's earlier 75,000-contract program took more than 5 hours.
- HFTs: between 2:45:13 and 2:45:27 traded over 27,000 contracts (~49% of volume), net buying ~200.
- E-mini: -3% from 2:41 to 2:44; -1.7% in 15 s to 2:45:27, low 1056; buy-side depth ~$58 million, <1% of morning; Stop Logic pause 2:45:28, resumed 2:45:33; back near prior level by 3:08.
- Stocks: 2:40-3:00, over 20,000 trades in 300+ securities at >=60% from 2:40 prices, some at $0.01, some at $100,000; broken by exchanges and FINRA; >98% of shares within 10% of 2:40 values. Broad indices fell 5-6% from 2:41 to 2:45:28.
- Follow-ups in the report: single-stock circuit breaker pilot (S&P 500 approved June 10, 2010; expanded Sep 10), clearer trade-break standards, LULD under consideration.
- **Lab:** simex LULD (see ex-07-breakers), trader pulls quotes when trading_state != 'T' (firm/trader/trading.cpp), 5% collar (firm/risk).

## Unsure / left out
- The DJIA's intraday low in points: not in what I read, left out.
- 2015 Sarao spoofing charges linked to the day: not verified this session, left out.
- Chart shape on screen is illustrative; only labelled moves are from the report.
