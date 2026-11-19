# strat-09-macro: Global macro and carry (188.0 s)

Key facts and sources
- Carry is the futures return if the price stays the same: C_t = (S_t − F_t)/F_t. For a currency forward, it equals the interest-rate spread. Carry predicts returns in currencies, bonds, commodities and equity indices, and is exposed to global recessions, liquidity and volatility risk. Source: [Koijen, Moskowitz, Pedersen & Vrugt, "Carry", JFE 127(2), 2018](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf).
- Currency carry traders face crash risk, with negatively skewed returns, linked to sudden unwinding when risk appetite and funding liquidity dry up. Source: [Brunnermeier, Nagel & Pedersen, "Carry Trades and Currency Crashes", NBER Macroeconomics Annual 2008 (w14473)](https://www.nber.org/papers/w14473).
- Worked example (illustrative): fund at 1%, invest at 5%, spot 1.00. By covered interest parity F = 1.01/1.05 ≈ 0.962, carry ≈ (1 − 0.962)/0.962 ≈ 3.96% a year, and the breakeven depreciation is ≈ −3.8%. The P&L paths are illustrative.
- Lab tie-in: the lab has no macro book. Its strategies size by a fixed dollar notional. `thesis.hpp` records an outside view with entry, exit and stop before the trade.

Unsure / left out: carry and macro performance figures, fund industry sizes, and specific historical crash magnitudes.
