# sig-06-volatility: Realised volatility estimators

Builds on sig-04 (EW variance) and the `signals` video's use of volatility for scaling.

## Key facts and sources
- Close-to-close, Parkinson σ² = (ln H/L)² / (4 ln 2), Garman-Klass σ² = ½(ln H/L)² − (2 ln 2 − 1)(ln C/O)²; efficiency vs close-to-close about 4.9 (Parkinson) and 7.4 (Garman-Klass) under ideal assumptions (zero drift, continuous trading). Molnár, "Properties of range-based volatility estimators" (working paper). https://www.phys.sinica.edu.tw/~socioecono/econophysics2010/pdfs/MolnarPaper.pdf
- Realised variance from high-frequency returns is a far sharper ex-post measure than squared daily returns. Andersen & Bollerslev, "Answering the skeptics", International Economic Review 39(4), 885-905, 1998. https://faculty.washington.edu/ezivot/econ589//////AndersenBollerslevIER1998.pdf
- With microstructure noise the all-tick RV is biased; the two-scales estimator fixes it. Zhang, Mykland & Aït-Sahalia, "A tale of two time scales", JASA 2005. https://collaborate.princeton.edu/en/publications/a-tale-of-two-time-scales-determining-integrated-volatility-with-/
- Worked OHLC day (O 50.00, H 50.60, L 49.70, C 50.20, prev close 49.90): 0.60% / 1.08% / 1.25% daily; ×√252 → 9.5% / 17.1% / 19.8%. My own arithmetic.
- Signature plot: my own simulation, 40 days, true σ 1.5%/day, half-spread 1¢ at $50: RV σ 4.74% (1 s), 2.07% (10 s), 1.61% (1 min), 1.54% (5 min), 1.43% (30 min).
- Lab: `exchange/agents/main.cpp` (summary vol/step in ticks); `tools/quant-lab/main.cpp` (TRND vol 0.012 trending / 0.016 ranging).

## Unsure / left out
- Parkinson and Garman-Klass original papers (1980) not read directly; formulas and efficiencies taken from Molnár's survey.
