# strat-08-event: Merger arbitrage and event-driven (178.2 s)

Key facts and sources
- Mitchell & Pulvino studied 4,750 mergers from 1963 to 1998. Risk-arbitrage returns are mostly unrelated to the market, except in sharp market declines, where the payoff resembles selling index puts. Source: [Mitchell & Pulvino, "Characteristics of Risk and Return in Risk Arbitrage", J. Finance 56(6), 2001](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00402).
- Under the US HSR rules, parties above the filing thresholds generally wait 30 days (15 for a cash tender offer), and a second request extends the wait. Source: [FTC, Premerger Notification Program](https://www.ftc.gov/enforcement/premerger-notification-program).
- Worked example (illustrative): offer $50, target trades at $48, break price $35. Then 48 = p·50 + (1 − p)·35, so p = 13/15 ≈ 0.87. The gain is +$2 (≈ 4.2%) if the deal closes and −$13 if it breaks.
- Lab tie-in: `thesis.hpp` ThesisParams defaults are entry_bps 1000 (buy at least 10% below fair value), exit_bps 300, stop_bps 2500 (25% below average cost), research_days 10 and max_hold_days 230. The merger-arb mapping on screen is labelled as a sketch that is not in the lab.

Unsure / left out: the paper's return and Sharpe figures (no performance claims), historical deal-break rates, and the exact HSR dollar thresholds, which are revised every year.
