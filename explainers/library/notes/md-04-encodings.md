# md-04-encodings: Tag=value, FAST and SBE (179 s)

Key facts and sources
- FIX tag=value framing: SOH (0x01) separates fields, tag 9 is BodyLength and tag 10 is CheckSum (the byte sum modulo 256, written as three digits). Source: lab spec `docs/specs/fix44-subset.md`, citing the [OnixS FIX 4.4 dictionary](https://www.onixs.biz/fix-dictionary/4.4/index.html).
- FAST stop-bit encoding uses 7 data bits per byte, with the high bit set on the last byte. The spec's example is 942755 = 0x39 0x45 0xA3. FAST also has templates, a presence map, and the operators copy, delta, increment, default and constant. Sources: the [FAST specification page](https://www.fixtrading.org/?p=57530) and the [CQG stop-bit note](https://help.cqg.com/apihelp/Documents/stopbitencoding.htm).
- SBE puts fields at fixed positions with native binary types. The message header carries blockLength, templateId, schemaId and version. blockLength lets an older decoder skip fields added in a newer version. Sources: the [SBE standard](https://fixtrading.org/?p=57528) and the [SBE repository](https://github.com/FIXTradingCommunity/fix-simple-binary-encoding).
- On 9 Dec 2013, CME announced that MDP 3.0 would use "Simple Binary Encoding (SBE); replaces the current FAST compression model". Source: [CME advisory 20131209](https://www.cmegroup.com/tools-information/lookups/advisories/market-data/20131209.html).
- Lab tie-in: ITCH and OUCH are decoded with fixed-offset field lists (`libs/itch`, `libs/ouch`). `fixgw` parses tag=value, converts prices to Price(4) integers and rejects anything with more than 4 decimals (`docs/specs/fix44-subset.md`).

Worked example: price 4123.25 with quantity 10 is illustrative. The tag=value form is `270=4123.25|271=10|`, which is 19 bytes. The SBE form assumes an 8-byte price and a 4-byte quantity.

Unsure / left out: the date MDP3 went into production, and any decode-speed figures (no measurement was made).
