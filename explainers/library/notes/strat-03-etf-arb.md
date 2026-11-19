# strat-03-etf-arb: Index and ETF arbitrage

Key facts and sources
- How creation and redemption work, the arbitrage that keeps the market price close to NAV, and the daily website disclosure of premiums and discounts that rule 6c-11 requires. Effective date: Dec 23, 2019. SEC Release 33-10695 / IC-33646, "Exchange-Traded Funds": https://www.sec.gov/files/rules/final/2019/33-10695.pdf
- "On average, 90 percent of the total daily activity in ETFs occurs on the secondary market": the same release, citing the 2019 ICI Fact Book. The video says this.
- CME's fair value is Cash·[1 + r·(x/360)] − Dividends. The worked example uses CME's own numbers: cash 1146.00, r 5.7%, 78 days, dividends 3.47 pts gives FV 1156.68; futures at 1157.00 are 0.32 pts rich. CME Group, "Calculating Fair Value": https://www.cmegroup.com/trading/equity-index/fairvalue.html
- Lab parts: BookBuilder rebuilds every Nasdaq book from ITCH 5.0 (/home/claude/ts-push/libs/book/include/lab/book/book_builder.hpp), and prices are Price(4) integers. The O(1) incremental fair-value code on screen is a sketch, labelled "not in the repo".

Unsure / left out
- No creation unit sizes, AP counts, ETF asset totals or typical premium/discount sizes. I did not verify current figures.
- The ETF price-vs-NAV path in the creation scene is illustrative.
- The claim that fast traders use creation and redemption as a "slower valve" for inventory is a general description of the mechanism. It is not a statistic.
