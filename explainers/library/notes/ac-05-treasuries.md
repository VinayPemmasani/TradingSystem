# ac-05-treasuries: US Treasuries

Key facts and sources
- Treasury ADV $1,224.7 bn (2026 through October) and $31.8 tn outstanding (as of September 2026): SIFMA US Treasury Securities Statistics, https://www.sifma.org/research/statistics/us-treasury-securities-statistics
- PTFs did 61% of electronic interdealer-broker volume (48% of all IDB), Apr–Dec 2019 TRACE data; the IDB venue is an anonymous CLOB: FEDS Notes, "Principal Trading Firm Activity in Treasury Cash Markets", Aug 2020, https://www.federalreserve.gov/econres/notes/feds-notes/principal-trading-firm-activity-in-treasury-cash-markets-20200804.html
- FINRA disseminates individual transactions in on-the-run nominal coupons in an end-of-day file (from 25 Mar 2024), with size caps: Regulatory Notice 24-06, https://www.finra.org/rules-guidance/notices/24-06
- Fedwire Securities: book-entry, transfers against payment, final at transfer: https://www.federalreserve.gov/paymentsystems/fedsecs_about.htm . T+1 standard (government debt included): investor.gov T+1 bulletin.
- SEC Treasury clearing rule compliance: eligible cash trades 31 Dec 2026, repo 30 Jun 2027: https://www.sec.gov/featured-topics/treasury-clearing-implementation
- DV01: computed for a 10-year 4% semiannual note at par: price sensitivity 0.0818 per 100 per bp (duration ≈ 8.18), ≈ $8,200 per bp on $10 m.
- Lab: price-time matching engine, /home/claude/ts-push/libs/match/include/lab/match/engine.hpp

Unsure / left out
- The interdealer ladder prices are illustrative decimals; I did not use the 32nds convention or venue tick sizes because I did not verify them this session.
- "Most trading is in on-the-run issues" is a general description; no figure given.
- Venue names (BrokerTec, Tradeweb etc.) and market shares left out: no primary figures read.
- SIFMA trading data source (likely FINRA TRACE) is not named on the page.
