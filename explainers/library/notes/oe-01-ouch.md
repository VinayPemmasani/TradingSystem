# oe-01-ouch: OUCH 5.0 order entry

Key facts and sources
- OUCH messages travel inside SoupBinTCP: Unsequenced Data packets firm to exchange, Sequenced Data packets exchange to firm, so responses can be replayed on re-login. Source: lab spec `docs/specs/ouch50-layout.md`, from the [Nasdaq OUCH 5.0 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf).
- Enter Order (O) is 47 bytes: UserRefNum 1:4, Side 5:1, Quantity 6:4, Symbol 10:8, Price 18:8, Time In Force 26, Display 27, Capacity 28, ISO 29, CrossType 30, ClOrdID 31:14, Appendage Length 45:2. Order Accepted is 64 bytes and adds the Order Reference Number; Order Executed is 36 bytes (quantity, price, liquidity flag, match number). Account Query is 3 bytes; its response (15 bytes) carries NextUserRefNum. Source: same.
- UserRefNum: 4-byte unsigned, unique and strictly increasing per account for the day; lower numbers are ignored as retransmissions. Source: same.
- Price: 8 bytes, 4 implied decimals; maximum 199,999.9900; 214,748.3647 (0x7FFFFFFF) marks a market order. Integers big-endian; alpha left-justified, space-padded. Source: same.
- Lab: `libs/ouch/include/lab/ouch/messages.hpp` (one `visit()` field list per message drives encode and decode, compile-time length check); `firm/trader/order_entry.cpp` (order entry thread owns the socket; rings to the trading thread); `exchange/simex/gateway.cpp` `admit()` (ignores ref <= last ref; rejects quantity 0x0013 and price 0x001D).

Worked example: buy 100 at 187.25, UserRefNum 7, symbol AAPL. Illustrative numbers; 187.25 x 10,000 = 1,872,500 = 0x1C9274.

Unsure / left out: simex ignores a ref equal to the last one too (`<=`); the spec text says "lower" numbers, so the narration says "lower". No latency figures: no primary source.
