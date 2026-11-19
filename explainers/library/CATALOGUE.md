# Trading lab video library: 11 topics x 10 three-minute videos

Status per video: todo / authoring / queued / rendered. Agents update only their own rows (re-read before editing).
Existing longer videos that already cover parts of this: rest-api, kafka, http, fpga-book, signals, tick-to-trade, aeron-ipc, 9 cpp-*, 16 ai-* patterns.

## 1. Market data protocols (md-)
| slug | title | status |
|---|---|---|
| md-01-itch | Nasdaq TotalView-ITCH 5.0, message by message | queued |
| md-02-moldudp64 | MoldUDP64: framing, sequence numbers, gap requests | queued |
| md-03-soupbintcp | SoupBinTCP: login, heartbeats, replay | queued |
| md-04-encodings | FIX tag=value vs FAST vs SBE: why binary won | queued |
| md-05-cme-mdp3 | CME MDP 3.0: SBE, incrementals, snapshots | queued |
| md-06-pitch | Cboe PITCH: units, sequence and spin | queued |
| md-07-opra | OPRA: the options price feed | queued |
| md-08-feed-depth | Top of book vs price level vs order by order | queued |
| md-09-ab-lines | A/B line arbitration and snapshot recovery | queued |
| md-10-sip-direct | SIP vs direct feeds: why they disagree | queued |

## 2. Exchanges and matching (ex-)
| ex-01-matching | Inside a matching engine | queued |
| ex-02-priority | Price-time vs pro-rata allocation | queued |
| ex-03-order-types | Order types: limit, IOC, FOK, post-only, hidden, pegged | queued |
| ex-04-auctions | Opening and closing auctions | queued |
| ex-05-ticks | Tick sizes, lot sizes and why they matter | queued |
| ex-06-fees | Maker-taker fees, rebates and inverted venues | queued |
| ex-07-breakers | Circuit breakers, LULD and volatility halts | queued |
| ex-08-stp | Self-trade prevention | queued |
| ex-09-colo | Co-location and equalised cable lengths | queued |
| ex-10-speedbumps | Speed bumps: IEX and friends | queued |

## 3. Feed handlers (fh-)
| fh-01-anatomy | Anatomy of a feed handler | queued |
| fh-02-arbitration | Arbitrating A and B multicast in code | queued |
| fh-03-gaps | Gap detection, retransmission and stale books | queued |
| fh-04-book | Building an order-by-order book | queued |
| fh-05-normalise | Normalising many venues into one format | queued |
| fh-06-symbols | Symbol directories and instrument ids | queued |
| fh-07-bursts | Surviving the open: bursts and microbursts | queued |
| fh-08-fanout | Fanning out to strategies: shared memory rings | queued |
| fh-09-timestamps | Timestamping and measuring feed latency | queued |
| fh-10-replay | Testing with pcap replay | queued |

## 4. Network (net-)
| net-01-multicast | Multicast and IGMP for market data | queued |
| net-02-udp-tcp | UDP vs TCP in trading | queued |
| net-03-bypass | Kernel bypass: Onload, ef_vi, DPDK | queued |
| net-04-ptp | Hardware timestamps and PTP | queued |
| net-05-switches | Cut-through switches and per-hop latency | queued |
| net-06-microwave | Microwave vs fibre: Chicago to New Jersey | queued |
| net-07-nagle | Nagle, delayed ACK and TCP_NODELAY | queued |
| net-08-irq | Interrupts, coalescing, busy polling, IRQ affinity | queued |
| net-09-capture | Taps, packet capture and latency monitoring | queued |
| net-10-colo-net | Inside a colo: cross-connects and network layout | queued |

## 5. Signal generation (sig-)
| sig-01-microprice | Microprice | queued |
| sig-02-imbalance | Order book imbalance | queued |
| sig-03-trade-flow | Trade flow and aggressor imbalance | queued |
| sig-04-ewma | EWMA, VWAP and online features | queued |
| sig-05-lead-lag | Lead-lag: futures lead cash | queued |
| sig-06-volatility | Realised volatility estimators | queued |
| sig-07-queue | Queue position and fill probability | queued |
| sig-08-basis | Fair value from futures basis | queued |
| sig-09-decay | Signal horizon and decay | queued |
| sig-10-combine | Combining signals with online linear models | queued |

## 6. HFT and hedge fund strategies (strat-)
| strat-01-mm | Market making | queued |
| strat-02-pairs | Statistical arbitrage: pairs | queued |
| strat-03-etf-arb | Index and ETF arbitrage | queued |
| strat-04-latency-arb | Latency arbitrage | queued |
| strat-05-trend | Trend following and CTAs | queued |
| strat-06-mean-rev | Short-term mean reversion | queued |
| strat-07-options-mm | Options market making and delta hedging | queued |
| strat-08-event | Merger arbitrage and event-driven | queued |
| strat-09-macro | Global macro and carry | queued |
| strat-10-long-short | Long/short equity and factor investing | queued |

## 7. Order entry (oe-)
| oe-01-ouch | OUCH 5.0 order entry | queued |
| oe-02-fix | FIX 4.4: NewOrderSingle to fill | queued |
| oe-03-state | The order state machine | queued |
| oe-04-risk | Pre-trade risk checks and the market access rule | queued |
| oe-05-dropcopy | Drop copy | queued |
| oe-06-cancel-replace | Cancel/replace and its races | queued |
| oe-07-seq | Sequence numbers, resends and gap fill | queued |
| oe-08-throttles | Throttles and message rate limits | queued |
| oe-09-kill | Kill switches | queued |
| oe-10-sor | Smart order routing | authoring |

## 8. Asset classes (ac-)
| ac-01-equities | Cash equities | queued |
| ac-02-options | Listed equity options | queued |
| ac-03-futures | Futures | queued |
| ac-04-fx | FX spot: ECNs, banks and last look | queued |
| ac-05-treasuries | US Treasuries | queued |
| ac-06-credit | Corporate bonds and RFQ trading | queued |
| ac-07-crypto | Crypto spot and perpetual futures | queued |
| ac-08-commodities | Commodities | queued |
| ac-09-rates | Interest rate swaps | queued |
| ac-10-etfs | ETFs: creation and redemption | queued |

## 9. The biggest exchanges and why (big-)
| big-01-nyse | NYSE | queued |
| big-02-nasdaq | Nasdaq | queued |
| big-03-cme | CME Group | queued |
| big-04-cboe | Cboe | queued |
| big-05-ice | ICE | queued |
| big-06-lseg | London Stock Exchange Group | queued |
| big-07-eurex | Deutsche Börse and Eurex | queued |
| big-08-jpx | Japan Exchange Group | queued |
| big-09-asia | HKEX, Shanghai and Shenzhen | queued |
| big-10-why | Why liquidity concentrates: network effects | queued |

## 10. Risk, regulation and post-trade (reg-)
| reg-01-nms | Reg NMS and order protection | queued |
| reg-02-mifid | MiFID II for trading firms | queued |
| reg-03-knight | Knight Capital, 1 August 2012 | queued |
| reg-04-flash-crash | The 6 May 2010 flash crash | queued |
| reg-05-realtime-risk | Real-time position and PnL risk | queued |
| reg-06-ccp | Clearing and central counterparties | queued |
| reg-07-settlement | Settlement and T+1 | queued |
| reg-08-best-ex | Best execution and TCA | queued |
| reg-09-surveillance | Spoofing, layering and surveillance | authoring |
| reg-10-capital | Margin and capital for trading firms | todo |

## 11. Market microstructure (ms-)
| ms-01-spread | What the spread pays for | queued |
| ms-02-adverse | Adverse selection | queued |
| ms-03-impact | Market impact and the square-root law | queued |
| ms-04-toxicity | Order flow toxicity | queued |
| ms-05-pfof | Payment for order flow and wholesalers | queued |
| ms-06-dark | Dark pools | queued |
| ms-07-fragmentation | Fragmentation across venues | todo |
| ms-08-queues | Queue dynamics at a price level | todo |
| ms-09-races | Latency races and frequent batch auctions | todo |
| ms-10-volume | Intraday volume curves and the close | todo |
