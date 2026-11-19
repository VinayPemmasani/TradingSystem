# ms-03-impact: Market impact and the square-root law

## Key facts and sources
- Kyle (1985), Econometrica 53(6) 1315–1335: p = μ + λ(x+u), λ = σ_V/(2σ_u), β = σ_u/σ_V, posterior variance halves, depth = 1/λ. https://ronming1303.github.io/documents/Kyle_1985_.pdf
- Tóth, Lemperière, Deremble, de Lataillade, Kockelkoren, Bouchaud, "Anomalous price impact and the critical nature of liquidity", Phys. Rev. X 1, 021006 (2011): Δ = Y σ √(Q/V), Y "of order unity", ~500,000 CFM futures trades Jun 2007–Dec 2010, Q/V from a few 10⁻⁴ to a few %, exponent 0.4–0.7 (≈0.5 small tick, ≈0.6 large tick). https://www.arxiv.org/pdf/1105.1694
- Almgren & Chriss, "Optimal execution of portfolio transactions" (2000; J. Risk 3(2)): min E + λV; x_j = X sinh(κ(T−t_j))/sinh(κT), κ ≈ √(λσ²/η); λ=0 gives a straight line. https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf
- Lab: firm/strategy/.../execution.hpp PovParams participation_bps = 600; tools/quant-lab/main.cpp fund_work(): cumulative participation since parent start, IOC at the touch, ≤5,000 per child.

## Worked numbers (mine)
- Kyle: σ_V $2, σ_u 10,000 → λ = $0.0001/share; β = 5,000 shares per $; $1 mispricing → expected move $0.50.
- √ law: σ 2%, V 5M, $50, Q 50k (1%), Y=1 → 0.2% = 10¢; 200k → 20¢; dollar cost ∝ Q^1.5 (8×).

## Unsure / left out
- No fitted value of Y from the paper (it gives none for the CFM data). Impact decay after a metaorder ends: not covered.
