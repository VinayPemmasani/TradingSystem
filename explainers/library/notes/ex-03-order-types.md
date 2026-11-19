# ex-03-order-types: limit, IOC, FOK, post-only, hidden, pegged

## Key facts and sources
- FIX 4.4 TimeInForce (59) values: 0 Day, 1 GTC, 2 OPG, 3 IOC, 4 FOK, 5 GTX, 6 GTD, 7 At the Close. Source: OnixS FIX 4.4 dictionary, https://www.onixs.biz/fix-dictionary/4.4/tagnum_59.html.
- FIX ExecInst (18) values: 6 = participate don't initiate, P = market peg, R = primary peg, M = mid-price peg. Source: https://www.onixs.biz/fix-dictionary/4.4/tagnum_18.html.
- MaxFloor (111) is the "maximum quantity ... to be shown on the exchange floor at any given time". Source: https://www.onixs.biz/fix-dictionary/4.4/tagnum_111.html.
- Nasdaq Post-Only (Rule 4702(b)(4)) is designed to post in compliance with Reg NMS Rule 610(d). If it would lock or cross a Protected Quotation, the participant chooses whether the order is adjusted or cancelled. It executes anyway if the price improvement is at least $0.01 for orders priced at $1 or more. Source: Nasdaq rulebook, Equity 4, https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204.
- At one price, displayed orders go first in time priority, then non-displayed orders in time priority. Source: Rule 4757(a), read in the BX Equity 4 text.
- ITCH P (Trade, non-cross) is 44 bytes and reports executions against non-displayed orders. OUCH Enter Order is 47 bytes, with single-byte TIF and Display fields. The OUCH market-order price is 214,748.3647 (0x7FFFFFFF). In simex, TIF 0 and 3 are supported and other codes act as day orders, and every order is shown. Sources: lab `docs/specs/ouch50-layout.md`, `docs/specs/itch50-layout.md` and `exchange/simex/gateway.cpp`.

## Unsure / left out
- Peg definitions follow the FIX 4.4 ExecInst wording (primary peg on the same side, market peg on the opposite side, mid-price). I did not read Nasdaq Rule 4703(d) in full this session.
- I did not claim which venues offer FOK for US equities.
- The book in the IOC/FOK example is illustrative.
