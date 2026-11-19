# ac-07-crypto: Crypto spot and perpetual futures

Key facts and sources
- First perpetual swap, BitMEX XBTUSD, announced 13 May 2016; funding every 8 hours: https://www.bitmex.com/blog/five-years-ago-the-perpetual-swap-was-born-everything-changed
- Binance funding: longs pay shorts when positive; default every 8 h (00:00, 08:00, 16:00 UTC); interest 0.03%/day (0.01% per interval); F = P + clamp(I − P, ±0.05%); funding amount = notional × rate; worked example P = 0.0429% → F = 0.0100%: https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031
- Binance diff depth stream `<symbol>@depth@100ms` (or 1000 ms) with U (first) and u (final) update IDs: https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams ; Binance also documents SBE market data streams: https://developers.binance.com/docs/binance-spot-api-docs/sbe-market-data-streams
- Lab: rt-server OMM JSON over WebSocket, /home/claude/ts-push/docs/specs/vendor-omm-json.md

Unsure / left out
- No crypto market size: reported volumes vary widely and none of the brief's primary sources (BIS, FIA, WFE) give a comparable figure I read.
- The "next U = previous u + 1" continuity rule is from Binance's order-book management guide as I remember it; the page I read lists U and u but not the rule.
- The $300/day figure is my arithmetic (3 × 100 USDT) at the example rate; real rates vary each interval.
- The index/perp chart is illustrative.
