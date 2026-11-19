# ac-03-futures: Futures

Key facts and sources
- Global 2025 volume 119.29 bn futures and options contracts; futures 30.64 bn (+8.6%): FIA, "ETD Volume – December 2025", https://www.fia.org/fia/articles/etd-volume-december-2025
- E-mini S&P 500: $50 × index, minimum tick 0.25 points = $12.50, cash settlement against a Special Opening Quotation on the third Friday of the contract month: CME Rulebook chapter 358, https://www.cmegroup.com/rulebook/CME/IV/350/358.pdf
- CME Clearing is the counterparty to every trade, calculates settlement variation and performance bond (initial margin) twice daily for futures and options: CME Clearing Financial Safeguards, https://www.cmegroup.com/clearing/files/financialsafeguards.pdf
- Implied IN / implied OUT, with the Sep ask 9500 / Dec bid 9450 → implied spread ask 50 example: CME client wiki "Implied Orders", https://cmegroupclientsite.atlassian.net/wiki/display/EPICSANDBOX/Implied+Orders
- MDP 3.0 is SBE-encoded binary (see md-05-cme-mdp3 note for sources). "Nearly 24-hour access": CME E-mini S&P 500 product page.
- Lab: simex/agents/itch-fh `--strip NAME=A+B`, a strip that trades its own book and lifts both legs through implied liquidity (/home/claude/ts-push/docs/scenarios.md, lab/book/implied.hpp).

Unsure / left out
- The index level 6,000, the 20-point fall and the ESZ6 ladder are illustrative.
- "Each contract trades only on the exchange that lists it" is a general statement about non-fungible futures, not quoted from a source.
- No exchange rankings, margin levels or open interest figures.
