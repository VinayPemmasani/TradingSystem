# ex-10-speedbumps: Speed bumps, IEX and friends

## Key facts and sources
- **IEX exchange approval:** the SEC approved IEX's exchange registration on June 17, 2016 (Release 34-78101), with a 350-microsecond delay through its point of presence (POP) and coil. Pegged-order repricing from IEX's own view of the NBBO is not delayed. Source: https://www.sec.gov/files/rules/other/2016/34-78101.pdf
- **IEX coil:** the coil has been 44 miles since the 2024 data-centre move, and was 38 miles before. Incoming orders and messages pass through the delay; IEX's market data from other venues does not. Source: https://www.iex.io/technology
- **Crumbling quote signal:** while the signal is on (2 ms), D-Peg orders do not exercise discretion to the more aggressive price. Source: IEX D-Peg rule filings (IEX Rule 11.190). The video simplifies this to "turn cautious".
- **ICE Futures US Passive Order Protection:** a 3 ms delay on aggressive orders in Gold Daily and Silver Daily futures, effective May 14, 2019. Source: CFTC statement of May 15, 2019 (https://www.cftc.gov/PressRoom/PressReleases/7928-19).
- **Cboe EDGA:** the proposed 4 ms delay on liquidity-taking orders (LP2) was disapproved by the SEC on Feb 21, 2020 (Release 34-88261).
- **Lab:**
  - simex has no speed bump. Its pipeline is gateway → SPSC ring of 64-byte Commands → matcher, which sequences commands in arrival order (exchange/simex).
  - The "350× the ring round trip" figure compares 350 µs with the 0.72–0.98 µs p50 in docs/aeron.md.
- **Race timeline:** illustrative, except for the 350 µs delay.

## Unsure / left out
- How much of IEX's 350 µs comes from the coil versus other equipment. The video does not split it.
- Studies on how speed bumps affect spreads or fill rates. I read no primary source for them.
- Other venues with delays (for example, options or FX platforms).
