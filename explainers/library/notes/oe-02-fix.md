# oe-02-fix: FIX 4.4, NewOrderSingle to fill

Key facts and sources
- Framing: tag=value fields ended by SOH (0x01); 8 BeginString first, 9 BodyLength second (characters from the byte after `9=...<SOH>` up to and including the SOH before `10=`), 35 MsgType third, 10 CheckSum last (sum of every byte before `10=`, mod 256, three digits). Header 49, 56, 34, 52. Source: lab spec `docs/specs/fix44-subset.md`, from the [OnixS FIX 4.4 dictionary](https://www.onixs.biz/fix-dictionary/4.4/index.html).
- NewOrderSingle (D) fields 11, 55, 54, 60, 38, 40, 44, 59; Side 1 buy; OrdType 2 limit; TimeInForce 0 day. Source: same.
- ExecType (150) 0 New, F Trade; OrdStatus (39) 0 New, 1 Partially filled, 2 Filled. Source: same; [OrdStatus 39](https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html).
- LeavesQty = OrderQty - CumQty for an active order. Source: [OnixS tag 151](https://www.onixs.biz/fix-dictionary/4.4/tagnum_151.html).
- Lab: `exchange/fixgw` maps D to OUCH Enter Order (fixgw assigns the UserRefNum and keeps the ClOrdID); Accepted to 150=0, Executed to 150=F. `libs/fix` `parse_price` rejects more than 4 decimals; fixgw answers with a session Reject 373=6.

Worked example (illustrative): 8=FIX.4.4|9=127|35=D|49=FIXA|56=SIMEX|34=12|52=20261119-14:30:00.000|11=ORD-7|55=AAPL|54=1|60=20261119-14:30:00.000|38=100|40=2|44=187.25|59=0|10=245| . BodyLength and CheckSum computed with Python this session; 150 bytes total vs 47 for OUCH Enter Order. CompIDs FIXA/SIMEX are fix-client's defaults; UserRefNum 1043 is invented. Fills 40 @ 187.25 and 60 @ 187.20, AvgPx 187.22.

Unsure / left out: no claim about how many venues accept FIX or parse-time numbers; no measurement.
