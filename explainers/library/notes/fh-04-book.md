# fh-04-book: Building an order-by-order book

Key facts and sources (lab repo /home/claude/ts-push):

- Book rules: A/F add; E and C reduce, an order executed to zero leaves without a delete; X reduces; D removes; U removes the original and adds a new reference with the same side and instrument; P, Q, B never touch the visible book. Source: `libs/book/include/lab/book/book_builder.hpp` header (citing ITCH 5.0 section 4.3) and [Nasdaq TotalView-ITCH 5.0 spec](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).
- Price levels: per side a `std::vector<Level>` sorted worst→best, `Level{price, orders, shares}`, scans from the back. Source: `libs/book/include/lab/book/order_book.hpp`.
- OrderMap: open addressing, linear probing, backward-shift deletion, identity hash; the code comment says a multiplicative hash measured ~35% slower on the itch_bench book rebuild, and attributes the sequential-reference assumption to Nasdaq. Default BookBuilder reserve: 1u << 22 live orders. Source: `libs/book/include/lab/book/order_map.hpp`, `book_builder.cpp`.
- Integrity checks and the FNV-1a digest. Source: `book_builder.hpp`, `book_builder.cpp`.
- `BookSide::insert_at` calls `levels_.push_back`, which can allocate when a side grows past its capacity; no reserve of levels was found. This is my reading of the code, shown as a caveat.

Unsure: "reference numbers come in sequence" is the lab's comment; the ITCH spec only says the reference is unique for the day, so the video attributes it to the lab's notes. The 35% figure is quoted from a code comment, not re-measured (the box was overloaded). Example order numbers and prices are illustrative.
