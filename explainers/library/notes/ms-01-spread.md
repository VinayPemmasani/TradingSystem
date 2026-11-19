# ms-01-spread: What the spread pays for

## Key facts and sources
- Roll (1984): with trades at bid or ask with equal odds and an efficient price, Cov(Δp_t, Δp_t+1) = −s²/4, so s = 2√(−cov). Original test: CRSP daily NYSE/AMEX 1963–82. Roll, J. Finance 39(4) 1127–1139. https://www.bauer.uh.edu/rsusmel/phd/roll1984.pdf
- Three components (order processing, inventory, adverse selection); Huang & Stoll find order processing largest, adverse selection and inventory smaller. RFS 10(4) 995–1034, 1997. https://econpapers.repec.org/RePEc:oup:rfinst:v:10:y:1997:i:4:p:995-1034
- Glosten & Milgrom 1985 for adverse selection (see ms-02).
- Rule 605 amendments adopted Mar 6, 2024; realized spread horizons from <100 µs to 5 min. https://www.sec.gov/files/34-99679-fact-sheet.pdf
- Lab: exchange/agents/main.cpp: maker half_spread 1–4 ticks around value + noise; skew = position/500 ticks; value traders act at a 3-tick gap; prints PnL per population and touch spread p50/p99.

## Worked numbers (mine)
- 100.00/100.02 quote; 10 round trips × 1,000 × $0.02 = $200.
- Effective 2(100.02−100.01)=2¢; realized vs later mid 100.015 = 1¢; impact 1¢.
- Simulation: 100,000 trades, value random walk (σ 0.5¢/trade), s = 2¢; cov = −0.99 ¢², estimate 1.99¢.

## Unsure / left out
- Huang & Stoll's numeric component shares (not read; only the qualitative ordering). Bar widths on screen are illustrative.

Duration: 178.0 s.
