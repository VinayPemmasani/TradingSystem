# ex-08-stp: Self-trade prevention

## Key facts and sources
- **CME Globex Self-Match Prevention:**
  - The SMP ID goes in FIX tag 2362 (SelfMatchPreventionID). Tag 8000 picks the instruction: N cancels the aggressing order, O cancels the resting order.
  - With no instruction, CME cancels the resting order.
  - Cancel reports carry ExecRestatementReason 103 (cancel oldest) or 107 (cancel newest).
  - SMP is optional, and one ID can span orders with common ownership.
  - Source: CME client systems wiki, Self-Match Prevention (https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/).
  - CME Rule 534 prohibits wash trades (CME Rulebook ch. 5).
- **Nasdaq/BX Rule 4757(a)(3) anti-internalization:** decrement, cancel oldest, cancel newest, or the remover's choice ("use remover"). Source: https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204
- **Binance STP modes:** EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH and DECREMENT. Source: https://developers.binance.com/docs/binance-spot-api-docs/faqs/stp_faq
- **Lab:**
  - simex has no STP. OrderKey puts the owner in its top 16 bits (libs/match engine.hpp make_key).
  - firm/trader/trading.cpp works client-side. It never bids at or above its own working ask, or offers at or below its own bid. It counts self-trades as two fills that share a match number, and any self-trade fails the run.
  - OUCH cancel reason Q is self-match prevention (docs/specs/ouch50-layout.md).
- **Example:** the orders (sell 500, buy 300 at $100.25, ID 7) are illustrative.

## Unsure / left out
- I did not quote the full CME Rule 534 text or any enforcement statistics.
- "Cancel both" on screen is Binance's EXPIRE_BOTH. I did not confirm whether Nasdaq offers a both-sides mode, so it is not attributed to Nasdaq.
- "Log every prevented trade" is advice, not a rule.
