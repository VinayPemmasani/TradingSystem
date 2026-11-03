import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paperfund import costs, synthetic  # noqa: E402
from paperfund.config import CostConfig, FundConfig  # noqa: E402
from paperfund.data import Fundamentals, Market  # noqa: E402
from paperfund.engine import PaperFund  # noqa: E402
from paperfund.sentiment import MiroFishSignals  # noqa: E402


def world(days=150):
    bars, news, eps = synthetic.world(days, seed=7)
    eps["available"] = pd.to_datetime(eps["available"]).dt.date
    return bars, news, Fundamentals(eps)


def run(bars, news, fund, cfg=None):
    m = Market(bars)
    cfg = cfg or FundConfig(warmup=40)
    sig = MiroFishSignals(news, m, swarm_seeds=2) if news else None
    return PaperFund(m, cfg, sig, fund).run()


class Costs(unittest.TestCase):
    def test_square_root_impact_grows_with_size(self):
        c = CostConfig()
        small = costs.cost_fraction(1_000, 100.0, 10e6, 0.02, c)
        big = costs.cost_fraction(1_000_000, 100.0, 10e6, 0.02, c)
        self.assertGreater(big, small)
        # 10% of ADV at 2% daily vol: 0.7 * 0.02 * sqrt(0.1) ~= 44bp of impact
        self.assertAlmostEqual(big - small, 0.7 * 0.02 * (np.sqrt(0.1) - np.sqrt(1e-4)), places=6)

    def test_thin_names_have_wider_spreads(self):
        c = CostConfig()
        self.assertGreater(costs.half_spread_bps(10.0, 1e6, c), costs.half_spread_bps(200.0, 50e6, c))


class Ledger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bars, cls.news, cls.fund = world()
        cls.res = run(cls.bars, cls.news, cls.fund)

    def test_pnl_rows_add_up_to_equity(self):
        eq = self.res.equity
        for sleeve in [c for c in eq.columns if c not in ("fund", "benchmark")]:
            booked = self.res.pnl.loc[self.res.pnl["sleeve"] == sleeve, "pnl"].sum()
            self.assertAlmostEqual(booked, eq[sleeve].iloc[-1] - eq[sleeve].iloc[0],
                                   delta=1e-6 * self.res.cfg.capital, msg=sleeve)

    def test_exchange_split_covers_everything(self):
        p = self.res.pnl
        self.assertAlmostEqual(p.groupby("exchange")["pnl"].sum().sum(), p["pnl"].sum(), places=2)
        self.assertEqual(set(p["exchange"]), {"NASDAQ", "NYSE"})

    def test_participation_cap_is_respected(self):
        cfg = FundConfig(warmup=40)
        cfg.costs.max_participation = 0.001
        res = run(self.bars, None, self.fund, cfg)
        self.assertGreater(res.stats["participation_cap_hits"], 0)
        self.assertLessEqual(res.stats["max_participation_used"], 0.001 + 1e-12)


class NoLookahead(unittest.TestCase):
    def test_future_data_does_not_change_the_past(self):
        bars, news, fund = world(140)
        bars = bars.assign(date=pd.to_datetime(bars["date"]).dt.date)
        dates = sorted(bars["date"].unique())
        cut = dates[110]
        full = run(bars, news, fund).equity["fund"]
        part = run(bars[bars["date"] <= cut], [n for n in news if n.ts.date() <= cut], fund).equity["fund"]
        common = part.index[:-1]
        np.testing.assert_allclose(full.loc[common].to_numpy(), part.loc[common].to_numpy(), rtol=1e-9)


class Scale(unittest.TestCase):
    def test_small_fund_pays_less_per_dollar(self):
        bars, _, fund = world(120)
        s = FundConfig(warmup=40, capital=1e6)
        b = FundConfig(warmup=40, capital=5e9)
        rs, rb = run(bars, None, fund, s), run(bars, None, fund, b)
        per_dollar = lambda r: r.pnl["cost"].sum() / max(r.pnl["traded"].sum(), 1.0)
        self.assertLess(per_dollar(rs), per_dollar(rb))


if __name__ == "__main__":
    unittest.main()
