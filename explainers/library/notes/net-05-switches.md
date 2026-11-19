# net-05-switches: Store-and-forward vs cut-through

Key facts and sources

- Serialisation at 10 Gb/s: 0.1 ns per bit, so a 64-byte frame takes 51.2 ns and a 1,518-byte frame about 1.21 µs (arithmetic; frame sizes from IEEE 802.3, excluding preamble and inter-frame gap).
- Cut-through vs store-and-forward behaviour, and why cut-through falls back to buffering when the egress port is busy or slower: Cisco white paper on cut-through switching: https://www3-realm.cisco.com/en/US/prod/collateral/switches/ps9441/ps11541/ps12581/white_paper_c11-716751.pdf
- Vendor figure: Cisco Nexus 3548 latency "as low as 250 ns", 200 ns in warp mode, 50 ns for Warp SPAN. Cisco datasheet: https://www.cisco.com/c/en/us/products/collateral/switches/nexus-3548-switch/data_sheet_c78-707001.html
- Vendor figure: Arista 7130 layer 1 switching 5 ns, which Arista equates to about 1 m of fibre: https://www.arista.com/en/products/7130l-series
- Fibre: group index 1.4682 at 1550 nm (Corning SMF-28 Ultra), so about 4.9 ns per metre: https://www.corning.com/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf
- Lab: the feed publisher caps each MoldUDP64 packet, header included, at 1,400 bytes; with UDP (8) and IP (20) headers that is at most 1,428 bytes, within a 1,500-byte MTU (kDefaultMaxPayload = 1400 in libs/mold/include/lab/mold/mold.hpp; header layout in docs/specs/moldudp64-layout.md).

These are vendor best cases, measured by each vendor on their own test set-ups; real latency depends on port speeds, features enabled and load.

Unsure / simplified

- The three-switch budget ignores NIC and PHY latency on each end.
- Queueing is described with one frame ahead; real bursts can queue many frames.
