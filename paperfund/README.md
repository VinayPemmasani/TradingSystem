# Paper Fund

A multi-strategy fund with **pretend money** ($5bn by default) run day by day on real US
equity prices, with MiroFish (`../mirofish`) turning news into signals. Simulation only:
nothing here sends an order to any broker or exchange.

## Sleeves

| Sleeve | Family | Rule |
|---|---|---|
| `systematic_trend` | systematic | time-series momentum, equal risk, 10% vol target, weekly rebalance |
| `stat_arb` | statistical arbitrage | 8 pairs, rolling OLS hedge ratio, enter at z=2, exit 0.5, stop 4 |
| `fundamental` | fundamental | earnings yield from point-in-time annual EPS, long cheapest third, short dearest third, monthly |
| `mirofish_sentiment` | news / sentiment | MiroFish forum + swarm + decide on each day's news, held for the signal horizon |
| `hft_market_making` | HFT | **modelled** from daily bars (spread capture, adverse selection, rebate); not a tick backtest |

MiroFish also tilts the other sleeves (`sentiment.overlay`). Every setting lives in
`paperfund/config.py` and can be overridden with `--config file.json`.

## How a day works

Signals use data up to the close of day *d*; orders fill at the open of *d+1*. Orders are
netted across sleeves (sleeves trading against each other cross internally), capped at 10% of
20-day average volume, and charged commission, a half spread and square-root market impact.
Shorts pay borrow. PnL is booked per sleeve, ticker and listing exchange (NASDAQ / NYSE).

## Run

```
pip install numpy pandas
python3 -m paperfund demo                       # synthetic world, no data needed
python3 -m paperfund run --prices data/prices.csv --news data/news.jsonl \
    --fundamentals data/eps.csv --out out/baseline
python3 -m paperfund scenarios ... --out out/scenarios   # placebo, realtime, capacity, robustness
python3 -m paperfund tune ... --out out/tuning           # walk-forward MiroFish tuning
python3 -m unittest discover -s tests -t .
```

Input formats: prices CSV `date,ticker,open,high,low,close,volume` (must include QQQ);
news JSONL in MiroFish's `NewsItem` shape; fundamentals CSV `ticker,period_end,filed,eps`
(`filed` is the date the number became public, used to avoid lookahead).

Data is never committed (`data/` is git-ignored).

## Honest-testing tools built in

- `placebo_news`: the same news shifted 20 sessions. If it earns as much as real news, the news adds nothing.
- `realtime_news`: fills MiroFish at the pre-news price. An upper bound on what faster data could add.
- `capacity_*`: the same strategies at $10k (retail costs incl. FX), $10m, $500m, $5bn.
- `robustness`: neighbouring parameter values; anything chosen after seeing results is labelled so.
- `tune`: picks MiroFish settings on the first half, reports the second half.

## Arena: rival funds on one exchange

`python3 -m paperfund arena --out out/arena` runs ten archetype funds against each other for five
simulated years, then 200 alternate histories (about 3 minutes). No real data and no real firms.

- `arena/lob.py`: a price-time priority order book on a microsecond clock. Fair value jumps (often
  after a lead signal on another venue's feed); each firm reacts after its own latency, so speed
  decides who pulls a stale quote, who picks it off and who reaches the front of the new queue.
  Retail flow, informed sweeps and slow funds' child orders take liquidity. A second, less contested
  venue has no top speed firms.
- `arena/world.py`: a daily stock universe and four futures markets with explicit sources of return
  (mispricing for value, flow pressure for reversal, news drift, trends) plus crisis regimes and
  crowding events.
- `arena/funds.py`: the cast (Apex HFT, Sniper Arb, Tier-2 MM, Pod Shop, Trend CTA, Value L/S,
  Big Bet, the MiroFish fund as built, your market-data fund, and the same team racing HFTs), with
  each one's risk rules (pod stops, vol targets, margin calls, daily loss limits) and running costs
  (estimates).
- `arena/run.py`: order-book days per regime, the main history (the most typical of all paths),
  alternate histories, risk metrics, correlations, who-pays-whom. Writes `arena.json` and `arena.md`.
- `python3 -m paperfund.arena.page out/arena/arena.json out/arena/index.html` builds the animated
  Fund Arena page from `arena/web/arena.html`.

## Master run: every model, the same tests

`python3 -m paperfund master --real RESULTS --arena out/arena/arena.json --qlab-bin build/release/tools/quant-lab/quant-lab --out out/master`
scores the three test benches together: the real-data paper fund (from saved `baseline_5bn/`, `scenarios/`,
`tuning/` and `ratings/` results), 20 simulated years of the C++ Quant Research Lab, and the arena. Every
result gets the same ladder: return and risk, t-stat, block-bootstrap Sharpe range, probabilistic and deflated
Sharpe (counting every variant tried), minimum track record, beta and alpha to QQQ, placebo, costs, capacity
and a walk-forward combination of sleeves (`master/stats.py`). Writes `master.json` and `master.md`;
`python3 -m paperfund.master.page out/master/master.json index.html` builds the animated page.
