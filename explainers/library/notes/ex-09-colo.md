# ex-09-colo: Co-location and equalised cable lengths

## Key facts and sources
- **Nasdaq BX SR-BX-2024-035, Release 34-101073 (Sept 18, 2024), Carteret NJ.** Source: https://www.sec.gov/files/rules/sro/bx/2024/34-101073.pdf. The filing states:
  - "the shortest current telco connection possible into NY11 is 160 ft" and "the longest … is 680 feet".
  - "the equidistant telco connections into NY11-4 will be 590 feet".
  - "Client connections to the matching engine will be equal across the board, within and among NY11 and NY11-4".
  - The equalization project is planned over 18–24 months.
- **NYSE Mahwah colocation:** SEC Release 34-62960 (Sept 21, 2010) offered 4 kW and 8 kW cabinets. Source: https://www.sec.gov/files/rules/sro/nyse/2010/34-62960.pdf
- **Fibre speed:** Corning SMF-28 Ultra has a group index of 1.4682 at 1550 nm (https://csmedia.corning.com/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf). That gives c / 1.4682 ≈ 4.90 ns per metre.
  - 520 ft = 158.5 m ≈ 0.78 µs one way.
  - 100 km ≈ 0.49 ms one way.
  - Both are arithmetic.
- **Lab:**
  - docs/aeron.md: aeron-ping ran 500,000 round trips of 64 bytes between two pinned processes on a shared 4-vCPU container. The p50 was 0.72–0.81 µs over Aeron IPC and 0.76–0.98 µs over SpscRing. With both processes on one physical core, the ring reached 76 ns.
  - simex has --matcher-cpu, --gateway-cpu and --md-cpu (exchange/simex/main.cpp).

## Unsure / left out
- I did not verify NYSE's own cable-equalisation practice (for example, coiled fibre), so the video does not claim it.
- "The farthest cabinet sets the length" is a logical consequence of equal lengths, not a quote from a filing.
- I left out colocation prices and current cabinet power options.
