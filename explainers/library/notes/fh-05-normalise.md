# fh-05-normalise: Normalising many venues into one format

Key facts and sources (lab repo /home/claude/ts-push):

- `TopOfBook` is `alignas(64)`, 64 bytes (static_assert), trivially copyable: rx_tsc, feed_ns, two bid and two ask levels, instrument, locate, trading_state, 11 reserved bytes. Source: `firm/oms/include/lab/oms/messages.hpp`.
- Vendor `Consolidator`: one Level 1 `Record` per locate, preallocated; after each ITCH message it builds a change mask (bid, bid size, ask, ask size, last, last size, volume, open, high, low, trades, status, auction, band); three sessions (ICF look-alike, OMM JSON/WebSocket, B-PIPE look-alike) turn it into images or updates. Source: `libs/vendor/include/lab/vendor/consolidator.hpp`, `server.hpp`, README phase 8.
- Price(4) has four implied decimals; MWCB levels use Price(8). Source: `docs/specs/itch50-layout.md`.
- Conflation per subscription (`interval_ns`). Source: `libs/vendor/include/lab/vendor/server.hpp`.

Unsure / generic: the lab has one venue, so the multi-venue hub shape and the "typical fields" list are presented as general practice, not as lab code. The ITCH/SBE/PITCH labels on the title card only name formats; no layouts are shown (md-* videos cover them). The 182.50 execution is an illustrative example.
