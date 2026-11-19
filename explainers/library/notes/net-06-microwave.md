# net-06-microwave: Microwave vs fibre, Chicago to New Jersey

Key facts and sources

- Fibre group index 1.4682 at 1550 nm (Corning SMF-28 Ultra product sheet), so about 4.9 µs per km; in air n ≈ 1, about 3.34 µs per km (c = 299,792.458 km/s). Corning: https://www.corning.com/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf
- Laughlin, Aguirre and Grundfest, "Information Transmission between Financial Markets in Chicago and New York" (2014): Aurora to Carteret great-circle distance 1,179 km, speed-of-light limit 3.93 ms one way; April 2010 reaction 7.25 to 7.95 ms; Spread Networks about 6.65 ms in August 2010; microwave estimates of 4.2 to 5.2 ms in 2012; a well-designed link about 4.03 ms; roughly 70 km per tower over flat ground, so at least 20 hops. Paper: https://arxiv.org/abs/1302.5966v1 (also https://www.law.stanford.edu/publications/information-transmission-between-financial-markets-in-chicago-and-new-york)
- Nasdaq microwave FAQ: heavy rain is the most common cause of outages, clients must also take the feed over fibre, and the number of price levels carried varies with bandwidth: https://www.nasdaqtrader.com/content/productsservices/trading/colo/nasdaqcmemicrowavefaqs.pdf
- Straight fibre over 1,179 km: 1,179 x 4.9 µs ≈ 5.8 ms (arithmetic).

Unsure / left out

- The Nasdaq FAQ also quotes microwave latencies, but the document is undated, so those numbers are left out.
- All route latencies on screen carry the 2014 paper as source with the year of each measurement; current commercial links will differ and are not public in a citable form.
- "A couple of milliseconds behind" for the fibre feed is derived from the paper's 2010 fibre and 2012 microwave figures, not measured.
- Aurora (CME) and New Jersey data-centre locations are as described in the paper.
