# ac-10-etfs: ETFs, creation and redemption

Key facts and sources
- US ETF combined assets $16.15 tn at end-September 2026: ICI, https://www.ici.org/research/stats/etf/etfs-09-26
- Rule 6c-11 adopted 26 Sept 2019: daily website portfolio holdings, custom baskets with written policies, premium/discount and bid-ask spread disclosure: SEC press release 2019-190, https://www.sec.gov/newsroom/press-releases/2019-190
- Authorized participants buy and redeem shares directly from the ETF in creation units, in kind or cash; redemptions often in kind; arbitrage keeps price near NAV; "On average, 90 percent of the total daily activity in ETFs occurs on the secondary market" (citing ICI 2019 Factbook): SEC Release 33-10695, https://www.sec.gov/files/rules/final/2019/33-10695.pdf
- T+1 covers ETFs: investor.gov T+1 bulletin.
- Lab: BookBuilder rebuilds every Nasdaq book from ITCH, /home/claude/ts-push/libs/book/include/lab/book/book_builder.hpp; companion strategy video strat-03-etf-arb.

Unsure / left out
- The NAV 50.00 / ETF 50.10 example and the 50,000-share creation unit are illustrative; I did not verify real creation unit sizes.
- Whether rule 6c-11 requires an intraday indicative value: not confirmed, so not mentioned.
- I did not confirm which ETFs appear in the lab's 2019 ITCH sample, so the narration says "a Nasdaq-listed ETF" without naming one.
