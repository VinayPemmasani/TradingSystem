# reg-05-realtime-risk: Real-time position and PnL risk

## Key facts and sources
- **Rules cited:** RTS 6 (Delegated Reg. 2017/589) Art. 16 real-time alerts within five seconds: https://www.legislation.gov.uk/eur/2017/589/data.html ; SEC Rule 15c3-5 financial controls on credit/capital thresholds: https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm
- **Lab (read-only):** firm/oms/include/lab/oms/oms.hpp Position {shares, cash (Price(4) x shares), open_buy, open_sell, pnl(price) = cash + shares x price}; firm/risk/include/lab/risk/risk.hpp worst-case check shares + open_buy + added <= max_position (2,000), replace counts only growth; firm/trader/trading.cpp marks PnL at last_mid; research/lab_research/pnl.py positions() and reconcile() on (match, user_ref), flagging only_firm / only_exchange / mismatched; research/report.py exits 1 on a break.
- **Worked example (arithmetic):** buy 300 @ 50.00, sell 100 @ 50.10 -> 200 shares, cash -9,990; mark 50.05 -> PnL +20 (10 realised + 10 open). Working bid 1,000 + new 900 + 200 = 2,100 > 2,000 -> blocked.

## Unsure / left out
- The lab has no automatic loss limit; the video says so.
- No industry statistics used.
