# sig-10-combine: Combining signals

Closes the series: combines sig-01 (microprice), sig-02 (imbalance), sig-03 (trade flow) and sig-05 (futures lead), scaled as in sig-04, at the horizon from sig-09.

## Key facts and sources
- Least squares w = (XᵀX)⁻¹Xᵀy; ridge w = (XᵀX + λI)⁻¹Xᵀy shrinks weights toward zero and toward each other when features are correlated. Standard results (no numbers taken from a source).
- Worked simulation (my own, seed 5): true weights 0.5 / 0 / 0.3, corr(micro, imbalance) = 0.9, 250 training samples. Least squares −0.29 / 0.71 / 0.42; ridge λ = 250: 0.11 / 0.21 / 0.20. Out-of-sample R² on 50,000 later samples: 2.9% (OLS), 3.7% (ridge), 4.4% (true weights). Illustrative only.
- Online version: decayed sums A ← γA + xxᵀ, b ← γb + xy, solve (A + λI)w = b on refresh; update with features from h ago once y is known. Sketch, not in the repo.
- Multi-level order flow merged into one integrated OFI variable. Cont, Cucuringu & Zhang, "Cross-impact of order flow imbalance in equity markets", Quantitative Finance 23(10), 1373-1393, 2023. https://ideas.repec.org/a/taf/quantf/v23y2023i10p1373-1393.html
- Lab: `research/` (Python, fit on earlier days, test on later); `firm/strategy/.../market_maker.hpp` (skew and hold rules turn fair value into orders). Shipping weights as constants is a proposed workflow, not existing code.

## Unsure / left out
- No claim that the combination is profitable; R² values are from the simulation only.
