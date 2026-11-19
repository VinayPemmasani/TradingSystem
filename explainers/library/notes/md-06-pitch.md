# md-06-pitch: Cboe Multicast PITCH (168 s)

Source for every fact: the [Cboe Titanium US Equities/Options Multicast PITCH specification](https://cdn.cboe.com/resources/techspec/technical-specifications-cboe-titanium-u-s-equitiesoptions-multicast-pitch-specification.pdf).

Key facts
- Symbols are split into units by a published alphabetical distribution that does not change during the day. Each unit has its own sequence numbers, starting at 1 each day.
- The Sequenced Unit Header is 8 bytes: length 2, count 1, unit 1, sequence 4 (the first message in the frame). A count of 0 is a heartbeat, sent after 1 s with no data. Binary fields are little-endian.
- Each message starts with a 1-byte length and a 1-byte type. Add Order long (0x21) is 34 bytes: order ID 8, side 1, quantity 4, symbol 6, price 8 with 4 implied decimals. Add Order short (0x22) is 26 bytes: quantity 2, price 2 with 2 decimals.
- The Time message (0x20) carries seconds since midnight, Eastern time. Other messages carry a 4-byte nanosecond offset from the last Time message.
- Recovery has two paths. The Gap Request Proxy runs over TCP, answers on a separate multicast channel, and limits requests per second, per minute and per day. The Spin Server announces spin images every second (messages 0x80 to 0x83).
- The A and B feeds carry the same content but may be framed differently, so arbitrate by unit and sequence.

Worked example: unit 3, sequence 1001, Time 34200 (9:30), then an add 1250 ns later, buy 100 at 189.25. All values are illustrative.

Unsure / left out: the exact gap-request rate limits (they vary by venue configuration), the number of units, and message rates.
