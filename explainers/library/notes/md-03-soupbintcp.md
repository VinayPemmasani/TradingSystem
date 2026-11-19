# md-03-soupbintcp: SoupBinTCP, login, replay and heartbeats (169 s)

Key facts and sources
- Every packet starts with a 2-byte big-endian Packet Length, which counts the bytes after it (the type byte included), followed by a 1-byte ASCII type. Source: lab spec `docs/specs/soupbintcp-layout.md`, from the [Nasdaq SoupBinTCP 3.00 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/soupbintcp.pdf).
- Packet types. Client: L login, U unsequenced, R heartbeat, O logout. Server: A accepted, J rejected, S sequenced, H heartbeat, Z end of session. `+` is debug and is ignored. Source: the same spec.
- Login Request is 49 bytes in all: username 6, password 10, session 10 and requested sequence number 20. Text fields are padded with spaces; numbers are ASCII digits, right-justified. A requested sequence of 0 means "start from the most recent message". Login Accepted is 33 bytes. Source: the same spec.
- Sequenced Data carries no sequence number: both sides count from 1 in each session. Source: the same spec.
- Each side sends a heartbeat after 1 s without sending anything. The server drops a client that has been silent for about 15 s, and a connection that sends no login within about 30 s. End of Session means the session cannot be rejoined. Source: the same spec.
- Lab tie-in: `libs/soup` holds the packet codec and stream reassembly. simex takes OUCH over SoupBinTCP and replays from the requested number on login. The vendor feeds also use Soup (`CLAUDE.md`, `libs/soup`).

Worked example: the client has processed 41,999 messages and asks for 42,000 (illustrative numbers).

Unsure / left out: no numbers on head-of-line blocking or latency, because there was no primary source and no measurement.
