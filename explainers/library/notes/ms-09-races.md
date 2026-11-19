# ms-09-races: Latency races and frequent batch auctions

## Key facts and sources
- Budish, Cramton & Shim, QJE 130(4) 1547–1621 (2015); numbers from the NBER/2013 working paper: ES–SPY median return correlation 0.0073 at 1 ms, 0.0923 at 10 ms, ≈0.98 at 1 minute (2011); median arbitrage duration 97 ms (2005) → 7 ms (2011); batch auctions, e.g. once per second, 100 ms discussed. https://conference.nber.org/conf_papers/f69665.pdf ; https://econpapers.repec.org/RePEc:oup:qjecon:v:130:y:2015:i:4:p:1547-1621
- Aquilina, Budish & O'Neill, QJE 137(1) 493–564 (2022): ≈ one race per minute per symbol (FTSE 100), modal race 5–10 µs, ≈20% of volume, ≈0.5 bp "tax", ≈$5bn/yr global equities. https://econpapers.repec.org/RePEc:oup:qjecon:v:137:y:2022:i:1:p:493-564.
- Lab: engine.hpp indicative()/uncross(); docs/scenarios.md auction price rule (most paired, least imbalance, nearest reference, lower price).

## Worked numbers (mine)
- Race: stale offer 30.01, value 30.05 → $4 on 100 sh. Batch: buys 300@30.04, 200@30.03, 400@30.01; sells 200@30.00, 300@30.02, 300@30.03 → 500 @ 30.02, imbalance 0.

## Unsure / left out
- The ~800–900 opportunities per day figure (versions differ); the 1-minute correlation 0.98 is from the working paper's table as read by the fetch tool.
