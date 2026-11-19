# ms-02-adverse: Adverse selection

## Key facts and sources
- Glosten & Milgrom (1985), J. Financial Economics 14, 71–100: competitive risk-neutral specialist, zero expected profit per trade; ask = E[V | buy], bid = E[V | sell]; spread wider with more/better-informed insiders; transaction prices are a martingale; market can shut down. https://www.edegan.com/pdfs/Glosten%20Milgrom%20%281985%29%20-%20Bid%20Ask%20and%20Transaction%20Prices%20in%20a%20Specialist%20Market%20with%20Heterogeneously%20Informed%20Trades.pdf ; https://econpapers.repec.org/RePEc:eee:jfinec:v:14:y:1985:i:1:p:71-100
- Lab: exchange/agents/main.cpp: noise traders (marketable IOC, random side), value traders (know value, act when |value − last trade| ≥ 3 ticks), makers quote around value + noise; `--value-rate` (default 5 value steps/s); per-population PnL at final value.

## Worked numbers (mine)
- V ∈ {99, 101}, p = ½, μ = 0.2: P(101|buy) = 0.6, ask 100.20, bid 99.80, spread 0.40 = μ(V_H − V_L); μ = ½ → $1.00.
- Per 5 traders: 4 × 20¢ − 80¢ = 0. After one buy: bid 100.00, ask 100.385 (shown 100.38). Quote path for B,B,S,B,B,S,B,B,B computed by Bayes.

## Unsure / left out
- The lab's agents results are noisy run to run (I ran simex+agents: makers did not reliably lose more at higher value rate), so the video only suggests the experiment, with no claimed outcome.

Duration: 183.4 s.
