# oe-05-dropcopy: Drop copy

Key facts and sources
- The lab's drop copy is lab-defined (not a Nasdaq spec), carried over SoupBinTCP 3.00; served by simex on the order entry port to a drop copy account (default DROP01:lab) that cannot send orders (anything but heartbeats and logout is ignored); one Execution Report per firm execution, for every firm account, in matching-engine order; historical liquidity (owner 0) is not reported; integers big-endian, prices 4 implied decimals. Source: lab spec `docs/specs/dropcopy-layout.md`.
- Execution Report (D), 57 bytes: type 0:1, timestamp 1:8, account 9:6, UserRefNum 15:4, side 19:1, quantity 20:4, symbol 24:8, price 32:8, match number 40:8 (same as OUCH and ITCH Order Executed), liquidity flag 48:1, order reference number 49:8 (ITCH order number). Source: same.
- SEC Rule 15c3-5(c)(2)(iv): controls must "assure that appropriate surveillance personnel receive immediate post-trade execution reports that result from market access". Source: [17 CFR 240.15c3-5](https://www.govinfo.gov/content/pkg/CFR-2011-title17-vol3/pdf/CFR-2011-title17-vol3-sec240-15c3-5.pdf).
- Lab reconciliation: `research/lab_research/pnl.py` `reconcile()` outer-joins the trader's fills and the drop copy on (match, user_ref) and compares side, quantity, price, symbol; keying on both covers a self-trade, which the trader prevents; `scripts/e2e-posttrade.sh` requires a clean result (`CLAUDE.md`). `tools/dropcopy` writes the CSV.

Worked example (illustrative): match numbers 9001 to 9004, UserRefNums 7, 9, 12, 13, two breaks.

Unsure / left out: real venues' drop copy formats (FIX-based or not) were not checked in detail, so the video only says venues define their own.
