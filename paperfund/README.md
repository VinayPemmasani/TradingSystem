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
