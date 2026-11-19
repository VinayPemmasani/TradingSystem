# fh-06-symbols: Symbol directories and instrument ids

Key facts and sources:

- Stock Locate (2 bytes at offset 1): "dynamically assigned each day, starting with a value of 1", will not change intraday, "no expectation that the assignment will be the same across multiple days"; locate 0 for non-stock messages; Stock Directory messages are sent at the start of each day for all active symbols. Source: [Nasdaq TotalView-ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).
- Stock Directory (R) is 39 bytes: stock 11:8, market category, financial status, round lot size 21:4, …, LULD tier 32:1. Source: `docs/specs/itch50-layout.md` (lab repo).
- `BookBuilder` holds 65,536 `Instrument`s indexed by locate; `find_locate` is a linear scan marked "not for hot paths"; checks `locate_without_directory` and `locate_symbol_mismatch`. Source: `libs/book/include/lab/book/book_builder.hpp`, `book_builder.cpp`.
- The trader maps locate → its own index in `instrument_of_` when it sees an R for a traded symbol. Source: `firm/trader/main.cpp`.
- Late Aeron subscribers start at the live position and miss the directory; itch-fh waits up to 10 s (`--aeron-wait-seconds`) for a first subscriber. Source: `docs/aeron.md`, `tools/itch-fh/main.cpp`.

Unsure: the advice to keep a mid-day directory snapshot is general practice, not lab code; I did not name any Nasdaq reference-data file because I could not verify one this session. Locate numbers and symbols in the directory animation are illustrative.
