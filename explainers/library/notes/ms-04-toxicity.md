# ms-04-toxicity: Order flow toxicity

## Key facts and sources
- Easley, López de Prado & O'Hara, "Flow toxicity and liquidity in a high-frequency world", RFS 25(5) 1457–1493, 2012: toxicity definition (quoted); VPIN = Σ|V^S−V^B|/(nV), V = 1/50 of average daily volume, n = 50; bulk volume classification with one-minute bars, V_B = V·Z(ΔP/σ_ΔP); E-mini S&P 500 on May 6, 2010: VPIN near 0.5 vs average ≈0.23, CDF > 0.9 at least two hours before. https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf
- Andersen & Bondarenko, "VPIN and the flash crash", J. Financial Markets 17 (2014) 1–46: VPIN's all-time high came after the crash; predictive content mainly "a mechanical relation with the underlying trading intensity". https://econpapers.repec.org/RePEc:eee:finmar:v:17:y:2014:i:c:p:1-46
- Lab run (mine, Nov 19 2026): simex + `agents --symbols SYM0001 --duration 20 --value-rate 20 --seed 2`: makers +$1,000, noise −$370, momentum −$790, value +$160 on 33 fills (PnL marked at final value). One run; results vary run to run.

## Worked numbers (mine)
- Buy shares 55/48/62/90/85% → gaps .10/.04/.24/.80/.70 → VPIN 0.376 ≈ 0.38; Z(1) = 0.841.

## Unsure / left out
- The 2012 paper's exact intraday VPIN path; flash crash time of day. Whether Andersen & Bondarenko used identical data (not stated on screen).
