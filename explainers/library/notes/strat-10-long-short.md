# strat-10-long-short: Long/short equity and factor investing (191.6 s)

Key facts and sources
- Fama-French six portfolios: each June, stocks are split at the NYSE median size and at the 30th and 70th NYSE percentiles of book-to-market. SMB = ⅓(SV + SN + SG) − ⅓(BV + BN + BG). HML = ½(SV + BV) − ½(SG + BG). Sources: Fama & French, JFE 33(1), 1993, as described in the K. French data library ([factors](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html), [six portfolios](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/six_portfolios.html)).
- Momentum: buy past winners and sell past losers over 3 to 12 months. Source: [Jegadeesh & Titman, J. Finance 48(1), 1993](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x).
- Momentum crashes happen in panic states, after market declines, when the market rebounds. Source: [Daniel & Moskowitz, "Momentum Crashes", JFE 122(2), 2016 (NBER w20439)](https://www.nber.org/papers/w20439).
- The August 2007 quant unwind is from Khandani & Lo (2007), as in strat-06.
- The worked example is made up: the six returns give SMB = 0.5% and HML = 0.7%. The 130/70 book (gross 200%, net 60%) is illustrative.
- Lab tie-in: `thesis.hpp` holds one long position on fair value. `execution.hpp` `pov_child` uses participation_bps = 600 (6% of the market's volume), and allowed = market_volume × participation_bps / 10,000, rounded to lots.

Unsure / left out: factor premia and fund performance figures, hedge fund industry sizes, and short-interest statistics.
