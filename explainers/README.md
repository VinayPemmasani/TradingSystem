# Explainer videos

Narrated 1080p explainer videos about the lab, and the tooling that makes them. The videos are not kept in git; render them from these sources.

To get the C++ samples shown in the videos running on your own PC, read [RUNNING.md](RUNNING.md). [samples.sh](samples.sh) builds every `videos/*/code` sample, runs its tests and, with `--bench`, its benchmarks.

## Videos

### Lab topics and C++ walkthroughs

| Video | Slug | Length |
| --- | --- | --- |
| Aeron IPC between processes | `aeron-ipc` (older single-file stage) | 3:14 |
| REST API calls | `rest-api` | 5:01 |
| Kafka pump and topics | `kafka` | 4:59 |
| HTTP on the wire (HTTP/1.1, HTTP/2, HTTP/3, WebSocket) | `http` | 4:55 |
| FPGA decode for book building | `fpga-book` | 5:00 |
| Signals on top of book and the full book | `signals` | 4:57 |
| Tick to trade, end to end | `tick-to-trade` | 4:39 |
| Cache lines and false sharing | `cpp-false-sharing` | 3:05 |
| Memory ordering: acquire and release | `cpp-memory-order` | 2:56 |
| No allocation on the hot path | `cpp-no-alloc` | 3:12 |
| Branches and data layout | `cpp-branches-layout` | 3:15 |
| Static vs virtual dispatch | `cpp-static-dispatch` | 3:14 |
| Walkthrough: SPSC ring buffer | `cpp-spsc-ring` | 3:08 |
| Walkthrough: order book with O(1) cancel | `cpp-order-book` | 3:02 |
| Walkthrough: fixed-point price parsing | `cpp-price-parse` | 3:14 |
| Walkthrough: sliding-window VWAP | `cpp-vwap` | 3:00 |

### AI-written code vs the hot path

| Video | Slug | Length | Code |
| --- | --- | --- | --- |
| Quote lookup | `ai-01-hashmap` | 2:56 | yes |
| Price levels | `ai-02-orderbook` | 2:58 | yes |
| Shared ownership | `ai-03-shared-ptr` | 2:51 | yes |
| Allocation per message | `ai-04-pool` | 2:57 | yes |
| A fresh vector every tick | `ai-05-vector` | 2:55 | yes |
| Copies you didn't ask for | `ai-06-copies` | 3:01 | yes |
| Exceptions for rejects | `ai-07-exceptions` | 3:11 | yes |
| Dispatch per call | `ai-08-dispatch` | 3:10 | yes |
| Logging | `ai-09-logging` | 3:05 | yes |
| Thread hand-off | `ai-10-queue` | 3:01 | yes |
| Memory order | `ai-11-memory-order` | 2:57 | yes |
| False sharing | `ai-12-false-sharing` | 2:57 | yes |
| Branches | `ai-13-branchless` | 2:55 | yes |
| Hot and cold | `ai-14-soa` | 3:10 | yes |
| Fixed point | `ai-15-fixed-point` | 3:15 | yes |
| Parsing | `ai-16-parsing` | 2:57 | yes |

### Live optimization

| Video | Slug | Length | Code |
| --- | --- | --- | --- |
| Live optimization: a market data handler, step by step | `cpp-live-optimize` | 9:43 | yes |

### Library

Three-minute videos in 11 topics; the plan and status are in [library/CATALOGUE.md](library/CATALOGUE.md), research notes in `library/notes/`. These have no `code/` directory.

#### Market data protocols

| Video | Slug | Length |
| --- | --- | --- |
| Nasdaq TotalView-ITCH 5.0, message by message | `md-01-itch` | 3:07 |
| MoldUDP64: framing, sequence numbers, gap requests | `md-02-moldudp64` | 3:02 |
| SoupBinTCP: login, heartbeats, replay | `md-03-soupbintcp` | 2:49 |
| FIX tag=value vs FAST vs SBE: why binary won | `md-04-encodings` | 2:59 |
| CME MDP 3.0: SBE, incrementals, snapshots | `md-05-cme-mdp3` | 2:59 |
| Cboe PITCH: units, sequence and spin | `md-06-pitch` | 2:48 |
| OPRA: the options price feed | `md-07-opra` | 2:52 |
| Top of book vs price level vs order by order | `md-08-feed-depth` | 2:49 |
| A/B line arbitration and snapshot recovery | `md-09-ab-lines` | 2:58 |
| SIP vs direct feeds: why they disagree | `md-10-sip-direct` | 2:53 |

#### Exchanges and matching

| Video | Slug | Length |
| --- | --- | --- |
| Inside a matching engine | `ex-01-matching` | 2:48 |
| Price-time vs pro-rata allocation | `ex-02-priority` | 2:51 |
| Order types: limit, IOC, FOK, post-only, hidden, pegged | `ex-03-order-types` | 2:49 |
| Opening and closing auctions | `ex-04-auctions` | 2:50 |
| Tick sizes, lot sizes and why they matter | `ex-05-ticks` | 2:46 |
| Maker-taker fees, rebates and inverted venues | `ex-06-fees` | 2:46 |
| Circuit breakers, LULD and volatility halts | `ex-07-breakers` | 2:57 |
| Self-trade prevention | `ex-08-stp` | 2:49 |
| Co-location and equalised cable lengths | `ex-09-colo` | 2:57 |
| Speed bumps: IEX and friends | `ex-10-speedbumps` | 2:54 |

#### Feed handlers

| Video | Slug | Length |
| --- | --- | --- |
| Anatomy of a feed handler | `fh-01-anatomy` | 2:49 |
| Arbitrating A and B multicast in code | `fh-02-arbitration` | 3:04 |
| Gap detection, retransmission and stale books | `fh-03-gaps` | 3:01 |
| Building an order-by-order book | `fh-04-book` | 3:00 |
| Normalising many venues into one format | `fh-05-normalise` | 3:05 |
| Symbol directories and instrument ids | `fh-06-symbols` | 2:53 |
| Surviving the open: bursts and microbursts | `fh-07-bursts` | 2:54 |
| Fanning out to strategies: shared memory rings | `fh-08-fanout` | 3:03 |
| Timestamping and measuring feed latency | `fh-09-timestamps` | 2:58 |
| Testing with pcap replay | `fh-10-replay` | 2:52 |

#### Network

| Video | Slug | Length |
| --- | --- | --- |
| Multicast and IGMP for market data | `net-01-multicast` | 2:55 |
| UDP vs TCP in trading | `net-02-udp-tcp` | 2:53 |
| Kernel bypass: Onload, ef_vi, DPDK | `net-03-bypass` | 2:56 |
| Hardware timestamps and PTP | `net-04-ptp` | 2:50 |
| Cut-through switches and per-hop latency | `net-05-switches` | 2:47 |
| Microwave vs fibre: Chicago to New Jersey | `net-06-microwave` | 2:55 |
| Nagle, delayed ACK and TCP_NODELAY | `net-07-nagle` | 2:51 |
| Interrupts, coalescing, busy polling, IRQ affinity | `net-08-irq` | 2:48 |
| Taps, packet capture and latency monitoring | `net-09-capture` | 2:49 |
| Inside a colo: cross-connects and network layout | `net-10-colo-net` | 2:53 |

#### Signal generation

| Video | Slug | Length |
| --- | --- | --- |
| Microprice | `sig-01-microprice` | 2:57 |
| Order book imbalance | `sig-02-imbalance` | 2:48 |
| Trade flow and aggressor imbalance | `sig-03-trade-flow` | 2:55 |
| EWMA, VWAP and online features | `sig-04-ewma` | 3:10 |
| Lead-lag: futures lead cash | `sig-05-lead-lag` | 3:01 |
| Realised volatility estimators | `sig-06-volatility` | 2:59 |
| Queue position and fill probability | `sig-07-queue` | 2:46 |
| Fair value from futures basis | `sig-08-basis` | 2:58 |
| Signal horizon and decay | `sig-09-decay` | 2:55 |
| Combining signals with online linear models | `sig-10-combine` | 3:02 |

#### HFT and hedge fund strategies

| Video | Slug | Length |
| --- | --- | --- |
| Market making | `strat-01-mm` | 2:55 |
| Statistical arbitrage: pairs | `strat-02-pairs` | 2:49 |
| Index and ETF arbitrage | `strat-03-etf-arb` | 3:14 |
| Latency arbitrage | `strat-04-latency-arb` | 3:02 |
| Trend following and CTAs | `strat-05-trend` | 3:05 |
| Short-term mean reversion | `strat-06-mean-rev` | 2:56 |
| Options market making and delta hedging | `strat-07-options-mm` | 3:04 |
| Merger arbitrage and event-driven | `strat-08-event` | 2:58 |
| Global macro and carry | `strat-09-macro` | 3:08 |
| Long/short equity and factor investing | `strat-10-long-short` | 3:12 |

#### Order entry

| Video | Slug | Length |
| --- | --- | --- |
| OUCH 5.0 order entry | `oe-01-ouch` | 3:00 |
| FIX 4.4: NewOrderSingle to fill | `oe-02-fix` | 2:56 |
| The order state machine | `oe-03-state` | 3:00 |
| Pre-trade risk checks and the market access rule | `oe-04-risk` | 3:08 |
| Drop copy | `oe-05-dropcopy` | 3:01 |
| Cancel/replace and its races | `oe-06-cancel-replace` | 3:08 |
| Sequence numbers, resends and gap fill | `oe-07-seq` | 3:01 |
| Throttles and message rate limits | `oe-08-throttles` | 3:01 |
| Kill switches | `oe-09-kill` | 2:58 |
| Smart order routing | `oe-10-sor` | not rendered yet |

#### Asset classes

| Video | Slug | Length |
| --- | --- | --- |
| Cash equities | `ac-01-equities` | 3:15 |
| Listed equity options | `ac-02-options` | 3:04 |
| Futures | `ac-03-futures` | 2:53 |
| FX spot: ECNs, banks and last look | `ac-04-fx` | 2:59 |
| US Treasuries | `ac-05-treasuries` | 2:59 |
| Corporate bonds and RFQ trading | `ac-06-credit` | 2:48 |
| Crypto spot and perpetual futures | `ac-07-crypto` | 3:03 |
| Commodities | `ac-08-commodities` | 3:03 |
| Interest rate swaps | `ac-09-rates` | 2:48 |
| ETFs: creation and redemption | `ac-10-etfs` | 2:52 |

#### The biggest exchanges and why

| Video | Slug | Length |
| --- | --- | --- |
| NYSE | `big-01-nyse` | 3:08 |
| Nasdaq | `big-02-nasdaq` | 3:07 |
| CME Group | `big-03-cme` | 3:06 |
| Cboe | `big-04-cboe` | 2:57 |
| ICE | `big-05-ice` | 2:57 |
| London Stock Exchange Group | `big-06-lseg` | 2:59 |
| Deutsche Börse and Eurex | `big-07-eurex` | 3:08 |
| Japan Exchange Group | `big-08-jpx` | 3:03 |
| HKEX, Shanghai and Shenzhen | `big-09-asia` | 2:57 |
| Why liquidity concentrates: network effects | `big-10-why` | 2:49 |

#### Risk, regulation and post-trade

| Video | Slug | Length |
| --- | --- | --- |
| Reg NMS and order protection | `reg-01-nms` | 3:13 |
| MiFID II for trading firms | `reg-02-mifid` | 3:11 |
| Knight Capital, 1 August 2012 | `reg-03-knight` | 3:10 |
| The 6 May 2010 flash crash | `reg-04-flash-crash` | 3:13 |
| Real-time position and PnL risk | `reg-05-realtime-risk` | 3:02 |
| Clearing and central counterparties | `reg-06-ccp` | 3:00 |
| Settlement and T+1 | `reg-07-settlement` | 3:01 |
| Best execution and TCA | `reg-08-best-ex` | 2:55 |
| Spoofing, layering and surveillance | `reg-09-surveillance` | 2:56 |

#### Market microstructure

| Video | Slug | Length |
| --- | --- | --- |
| What the spread pays for | `ms-01-spread` | 2:58 |
| Adverse selection | `ms-02-adverse` | 3:03 |
| Market impact and the square-root law | `ms-03-impact` | 3:08 |
| Order flow toxicity | `ms-04-toxicity` | 3:00 |
| Payment for order flow and wholesalers | `ms-05-pfof` | 3:00 |
| Dark pools | `ms-06-dark` | 3:05 |
| Fragmentation across venues | `ms-07-fragmentation` | 3:10 |
| Queue dynamics at a price level | `ms-08-queues` | not rendered yet |
| Latency races and frequent batch auctions | `ms-09-races` | not rendered yet |
| Intraday volume curves and the close | `ms-10-volume` | not rendered yet |

## Layout

- `engine/` holds the scene engine and pipeline. Read `engine/GUIDE.md` before writing a video.
  - `stage.html` and `engine.js` are a stateless `render(t)`; visuals are cued to narration sentences with `data-cue` attributes.
  - `tts.py` voices `script.json` with kokoro-onnx (voice `am_michael`).
  - `build_data.py` lays out the scene timing.
  - `render.js` screenshots each frame with Playwright into ffmpeg.
  - `make.sh` does all of the above.
- `videos/<slug>/` holds one video:
  - `script.json` (narration, which is also the captions), `scenes.html`, and optional `scenes.js`, `style.css` and `pron.json`.
  - `gen/`, where present, has the generator that wrote `scenes.html`. It still points at the scratch paths it was written in.
  - `code/` holds the C++ shown on screen, with its tests and benchmarks, and where present a `README.md` on how it was measured plus the raw results (`*.out`, `*.txt`, `*.s`). It is not part of the CMake build: `samples.sh` builds it into `build/samples/<slug>/`, or build one file by hand, for example `g++ -std=c++20 -O2 -Wall -Wextra -pthread test.cpp -o test` (see [RUNNING.md](RUNNING.md)).
- `ai-vs-ll/` is the brief, research and per-pattern notes for the `ai-*` series.
- `library/` is the plan (`CATALOGUE.md`), the brief and the research notes for the 11-topic library.

## Rendering

The engine expects these layouts:
- sources in `/mnt/project-files/videos/explainers/<slug>/`
- work files in `/tmp/claude-0/vx/<slug>/`
- the voice model in `/tmp/claude-0/av/voice/`

The model is `kokoro-v1.0.onnx` and `voices-v1.0.bin`, from the github.com/thewh1teagle/kokoro-onnx releases. Change the paths at the top of each script to render elsewhere.

```
bash engine/make.sh <slug> 3   # 3 render workers -> <slug>.mp4
```

Benchmark numbers in the videos were measured on a shared, heavily loaded 4-vCPU cloud box, and the videos say so. Rerun the `code/` benchmarks on pinned cores for real numbers.
