# sig-03-trade-flow: Trade flow and aggressor side

Builds on the `signals` video (trade flow imbalance) and sig-02 (book imbalance).

## Key facts and sources
- ITCH 5.0 Order Executed (E, 31 bytes, order reference at offset 11) and Executed With Price (C) name the resting order, so the book knows its side and the aggressor is the opposite side; Cross Trade (Q) prints auction volume with no aggressor. Lab spec `docs/specs/itch50-layout.md`; Nasdaq TotalView-ITCH 5.0 spec https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/
- Lee-Ready (1991): trades above/below the prevailing midpoint are buys/sells; at the midpoint use the tick test (vs last different price); for their 1988 data, quotes lagged 5 seconds. Lee & Ready, "Inferring trade direction from intraday data", Journal of Finance 46(2), 733-746, 1991. https://ideas.repec.org/a/bla/jfinan/v46y1991i2p733-46.html
- Lee-Ready accuracy about 72% (LR 72.1%, Table 6, ArcaTrade data, 3-31 Dec 2004). Rosenthal, "Modeling trade direction", 2008 (MPRA 36784). https://mpra.ub.uni-muenchen.de/36784/1/MPRA_paper_36784.pdf
- Kyle (1985) linear impact Δp = λ·V.
- Long memory in order signs, London Stock Exchange. Lillo & Farmer, "The long memory of the efficient market", 2004. https://arxiv.org/abs/cond-mat/0311053
- Worked examples (50.00/50.02 classification; λ = 2,900 / 1,800,000 = 1.6¢ per 1,000 shares from six windows): my own numbers.
- Lab: `tools/itch-dump/main.cpp` `--tob-csv` columns traded_bid, traded_ask.

## Unsure / left out
- Lee-Ready zero-tick details beyond "last different price" are not shown. Kyle's paper was not re-read this session; only the textbook linear form is used, with no numbers from it.
