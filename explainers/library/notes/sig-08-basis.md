# sig-08-basis: Fair value from futures basis

Builds on sig-05 (futures lead cash) and the `signals` video (fair value from a leader).

## Key facts and sources
- CME fair value: F = S[1 + r(x/360)] − D, with S the cash index, r the interest rate, x days to expiry, D dividends in index points to expiry. CME Group, "Equity index fair value" page and FAQ. https://www.cmegroup.com/trading/equity-index/fairvalue.html and https://www.cmegroup.com/trading/equity-index/fairvaluefaq.html
- Worked example (S 6,000, r 4%, x 60, D 12): financing 40.00, F* = 6,028.00, fair basis 28.00; futures at 6,031.50 is 3.50 rich (3.50 / 6,028 ≈ 0.058%); implied cash S* = 6,043.50 / 1.00667 = 6,003.48. My own arithmetic; not a market quote.
- The printed index is built from each stock's last trade, so it lags in fast markets: standard construction, stated without numbers.
- Lab: `exchange/agents/main.cpp` `--strip NAME=A+B` (strip value = sum of legs, no carry). The 100.02 + 99.97 = 199.99 strip and +0.01 basis are illustrative.

## Unsure / left out
- No current S&P 500 level, rate or dividend figures are used; all inputs are round illustrative numbers.
- Day-count conventions other than CME's 360 and exact dividend timing are not covered.
