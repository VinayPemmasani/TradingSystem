# md-01-itch: Nasdaq TotalView-ITCH 5.0, message by message (187 s)

Key facts and sources
- 11-byte common header: type 1, stock locate 2, tracking number 2, timestamp 6 (ns since midnight); big-endian integers. Lab spec `docs/specs/itch50-layout.md`, from the [Nasdaq TotalView-ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).
- Stock locate codes are assigned daily starting at 1 and announced in the Stock Directory (R) message (same Nasdaq spec).
- Add Order A = 36 bytes (ref 11:8, side 19:1, shares 20:4, stock 24:8, price 32:4); F = 40 bytes with a 4-byte MPID; E 31, X 23, U 35, D 19, P 44 bytes. Lab spec table; `libs/itch/include/lab/itch/messages.hpp`.
- Price(4) = integer with 4 implied decimals. Nasdaq may append fields; longer messages accepted (lab spec, Nasdaq spec).
- "When the number of display shares for an order reaches zero, the order is dead and should be removed from the book" (Nasdaq spec); lab `book_builder.hpp`: executed to zero leaves the book without a delete.
- Non-displayable orders are reported through Trade (P) messages (Nasdaq spec).
- TotalView-ITCH is offered over SoupBinTCP, compressed SoupBinTCP and MoldUDP64 (Nasdaq spec).
- Lab tie-in: field-list `visit()` drives encode and decode; `static_assert(layout_end<M>() == M::kSize)` in `codec.hpp`; `itch-dump` must report zero integrity errors (`CLAUDE.md`).

Worked example: the order (ref 1234, AAPL, locate 14, 100 @ 189.25 at 09:30:00) is illustrative; bytes computed with Python `struct`.

Unsure / left out: no message-mix statistics (share of A vs other types) since I had no primary source for a current day.
