# oe-03-state: The order state machine

Key facts and sources
- FIX 4.4 OrdStatus (39): A Pending New, 0 New, 1 Partially filled, 2 Filled, 4 Canceled, 6 Pending Cancel (result of OrderCancelRequest F), 8 Rejected, E Pending Replace (result of OrderCancelReplaceRequest G); 5 Replaced was removed in 4.3/4.4. Source: [OnixS FIX 4.4, tag 39](https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html).
- OUCH responses: A Accepted, U Replaced, C Canceled, E Executed, J Rejected; Order State L live / D dead. Source: lab spec `docs/specs/ouch50-layout.md` from the [Nasdaq OUCH 5.0 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf).
- Lab OMS (`firm/oms/include/lab/oms/oms.hpp`): states kFree, kPendingNew, kLive, kPendingSwap, kDone; exposure counts shares in PendingNew, Live and PendingSwap; responses that do not fit are counted in `stats.inconsistent`, printed by `firm/trader/trading.cpp` at the end of a run. One request in flight per order: `firm/trader/trading.cpp` (`work_side`). `on_rejected`: a rejected PendingNew order goes to Done; a rejected replacement leaves the original order standing.
- SoupBinTCP: Login Request carries Requested Sequence Number, the next message the client wants (0 = most recent, i.e. new messages only); the lab trader logs in with 0 (`firm/trader/order_entry.cpp`). Source: lab spec `docs/specs/soupbintcp-layout.md`, from the Nasdaq SoupBinTCP 3.0 spec.

Worked example (illustrative): buy 300, 100 executed, cancel the rest, Order Canceled for 200. OUCH Cancel Order with quantity 0 cancels the order (lab spec, "Lab interpretations").

Unsure / left out: which statuses a given venue actually sends (many do not send Pending New); the lab's fixgw sends no pending statuses. The narration presents the FIX states as the standard's vocabulary, not as what every venue emits.
