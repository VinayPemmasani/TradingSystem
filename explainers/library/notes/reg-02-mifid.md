# reg-02-mifid: MiFID II for trading firms

## Key facts and sources
- **MiFID II** (Directive 2014/65/EU) applies from 3 Jan 2018 (date of application shown on EUR-Lex for its RTS, e.g. https://eur-lex.europa.eu/eli/reg_del/2017/574/oj/eng). Art. 17: algorithmic traders notify their competent authority and have effective systems and risk controls.
- **HFT definition:** Art. 4(1)(40) (latency infrastructure such as co-location/proximity hosting/high-speed DEA; system-determined orders without human intervention; high message intraday rates), quoted via FIA: https://www.fia.org/articles/special-report-series-part-four-algorithmic-and-high-frequency-trading . Thresholds: Delegated Reg. 2017/565 Art. 19(1): on average >= 2 messages/s in any single instrument, or >= 4/s across all instruments, on a venue. https://legislation.gov.uk/id/eur/2017/565/article/19/1
- **RTS 6 (2017/589):** Art. 5 testing; Art. 9 annual self-assessment; Art. 12 kill functionality; Art. 13 surveillance; Art. 15 pre-trade controls (price collars, max order value, max order volume, max messages); Art. 16 real-time alerts within 5 s; Art. 17 post-trade controls and reconciliation; Art. 28 HFT order records kept 5 years. https://www.legislation.gov.uk/eur/2017/589/data.html (UK-retained copy; EU text https://eur-lex.europa.eu/eli/reg/2017/589/oj)
- **Clocks:** RTS 25 (2017/574) Table 2: HFT 100 µs max divergence, 1 µs granularity; all other trading 1 ms / 1 ms; voice 1 s. https://www.legislation.gov.uk/eur/2017/574/data.html . Repealed by Delegated Reg. 2025/1155 (adopted 12 Jun 2025; clock Arts. 11-16 apply from 2 Mar 2026): HFT 100 µs, granularity 0.1 µs. https://data.consilium.europa.eu/doc/document/ST-10366-2025-INIT/en/pdf and ADD-1 (Annex IV).
- **Lab:** firm/risk/include/lab/risk/risk.hpp Limits: 1,000 shares, $100,000 notional, 500 bps collar, 2,000 position, 200 open orders, 2,000 orders/s with burst 100; kill() blocks all but cancels. Drop copy reconciliation: research/report.py.

## Unsure / left out
- The 2025/1155 annex row for non-HFT algorithmic trading did not come through in the copy I read, so the video gives 1 ms only for RTS 25.
- Timestamps on screen are illustrative.
- MiFID II's narrowing of the own-account dealing exemption is not covered (not re-read).
