# oe-06-cancel-replace: Cancel/replace and its races

Key facts and sources
- OUCH Cancel Order (X) 11 bytes: UserRefNum, Quantity (the new intended remaining size; 0 cancels), Appendage Length. Replace Order (U) 40 bytes: OrigUserRefNum, UserRefNum, Quantity, Price, TIF, Display, ISO, ClOrdID, Appendage Length. Replace quantity counts the whole chain including executed shares; the replacement rests with quantity minus executed; in simex it always loses time priority. Replace has no Side or Symbol field. Answers: Order Canceled (C, 20 bytes, with Reason) and Order Replaced (U, 68 bytes, OrigUserRefNum and UserRefNum). Source: lab spec `docs/specs/ouch50-layout.md`, from the [Nasdaq OUCH 5.0 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf).
- FIX: OrderCancelRequest F and OrderCancelReplaceRequest G carry 41 OrigClOrdID and a new 11 ClOrdID; OrderCancelReject 9 with 434 (1 cancel, 2 replace) and 102 CxlRejReason (0 too late to cancel). fixgw sends the final fill's ExecutionReport, then OrderCancelReject 102=0. Source: lab spec `docs/specs/fix44-subset.md`, `exchange/fixgw/gateway.cpp`.
- Lab: one request in flight per order (`firm/trader/trading.cpp`); during a replace both the old order and its replacement count as exposure (`firm/oms/oms.hpp`, kPendingSwap); `Oms::cancel()` refuses while a replace is in flight; a replace to no more than executed shares is answered by Order Canceled; `risk.hpp` `check_replace` adds only growth to the worst case; on Order Replaced the OMS finishes the old order and carries its executed shares to the new one.

Worked example (illustrative): 100 @ 187.25 replaced by 100 @ 187.30 while 40 execute; replacement rests with 60.

Unsure / left out: other venues' priority rules for replaces (e.g. keeping priority on a size decrease) were not verified; the video says only that a replace "can" cost queue position and that simex always moves it to the back.
