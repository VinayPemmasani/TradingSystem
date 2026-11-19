# strat-01-mm: Market making

Key facts and sources
- Reservation price r = s − qγσ²(T − t) (eq. 8) and total spread δa + δb = γσ²(T − t) + (2/γ)ln(1 + γ/k) (eq. 30), with fill intensity λ(δ) = A·exp(−kδ). Example values γ = 0.1, σ = 2, k = 1.5, s = 100 from section 3.3. Avellaneda & Stoikov, "High-frequency trading in a limit order book", Quantitative Finance 8(3), 217–224, 2008: https://math.nyu.edu/~avellane/HighFrequencyTrading.pdf
- Worked numbers are computed from those formulas: spread = 0.1·4·1 + 20·ln(1 + 0.1/1.5) ≈ 1.69; with q = 2 and T − t = 1, r = 100 − 0.8 = 99.2.
- The spread partly compensates for trading against better-informed traders: Glosten & Milgrom, Journal of Financial Economics 14(1), 71–100, 1985: https://econpapers.repec.org/RePEc:eee:jfinec:v:14:y:1985:i:1:p:71-100
- Lab maker rules (join, step inside at ≥3-tick spread, 1 tick lean per 100 shares, ±1,000 share cap, 1-tick hold): /home/claude/ts-push/firm/strategy/include/lab/strategy/market_maker.hpp (MakerParams defaults).
- 2019 sample run: P&L −$20,316.08, 33,437 fills, 59,799 orders, AAPL, Nasdaq ITCH 2019-01-30: /mnt/project-files/quant-real/script.log and quant-real.json (mm.summary). A lab replay of one day; not a performance claim.

Unsure / left out
- The round-trip example (100.00 / 100.02, 100 shares) is illustrative, not real data.
- No figures given for exchange rebates or fee caps, or for the share of volume that market makers provide; I did not verify current numbers.
- The σ = 2 parameter came from a PDF extraction that dropped the Greek letters; the value matches the paper's section 3.3 as I remember it.
