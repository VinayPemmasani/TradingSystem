# net-10-colo-net: Inside a colo

Key facts and sources

- Nasdaq co-location: round trip, order to acknowledgement, under 50 µs; 10 Gb Ultra matches 40 Gb latency and lowers round trips by 2 to 5 µs on average: https://www.nasdaqtrader.com/TRADER.ASPX?ID=COLO
- Nasdaq General 8 (Connectivity) rule lists cabinets with power, 1, 10 and 40 Gb fibre and Ultra connections, third-party network (TNO) cross-connects and a shared GPS antenna: https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20General%208
- Equinix: a cross-connect is a "dedicated, physical cabling link between two parties"; single-mode fibre only since 31 March 2024: https://docs.equinix.com/cross-connect/
- Fibre at about 4.9 µs per km (Corning group index 1.4682): https://www.corning.com/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf ; so 10 km adds about 100 µs per round trip.
- Vendor best cases reused from earlier videos: Arista 7130 layer 1, 5 ns (https://www.arista.com/en/products/7130l-series); Cisco Nexus 3548, 250 ns (https://www.cisco.com/c/en/us/products/collateral/switches/nexus-3548-switch/data_sheet_c78-707001.html); AMD Onload half round trip about 1 µs (https://docs.amd.com/r/en-US/ug1586-onload-user/Latency-Test-Results).
- Microwave needs fibre backup; rain is the most common outage cause: https://www.nasdaqtrader.com/content/productsservices/trading/colo/nasdaqcmemicrowavefaqs.pdf
- Lab: simex publishes on multicast over loopback, CPUs per docs/core-plan.md, OUCH over SoupBinTCP back to simex (/home/claude/ts-push).

Unsure / simplified

- The cabinet layout (A/B feeds into a layer 1 switch, separate order switch, GPS-steered PTP clock, taps to capture) is a typical design, not any one firm's.
- The budget adds vendor best cases from different test benches; it is a scale illustration.
