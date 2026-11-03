import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paperfund.arena import lob, world  # noqa: E402
from paperfund.arena.funds import cast, fees_and_net, run_fund  # noqa: E402


class Book(unittest.TestCase):
    def test_price_time_priority(self):
        b = lob.Book()
        b.add(1, "first", -1, 101, 100)
        b.add(2, "second", -1, 101, 100)
        b.add(3, "better", -1, 100, 50)
        fills, left = b.take(1, 180, 101)
        self.assertEqual([(f[0], f[2], f[3]) for f in fills],
                         [("better", 100, 50), ("first", 101, 100), ("second", 101, 30)])
        self.assertEqual(left, 0)
        self.assertEqual(b.side[-1][101][0][2], 70)

    def test_limit_respected_and_cancel(self):
        b = lob.Book()
        b.add(1, "a", 1, 99, 100)
        self.assertTrue(b.cancel(1))
        self.assertFalse(b.cancel(1))
        b.add(2, "a", 1, 98, 100)
        fills, left = b.take(-1, 100, 99)
        self.assertEqual(fills, [])
        self.assertEqual(left, 100)


class Races(unittest.TestCase):
    def test_faster_firm_reaches_the_front_of_the_queue(self):
        rng = np.random.default_rng(0)
        fast = lob.Firm("fast", "mm", 3.0, jitter_us=0.5)
        slow = lob.Firm("slow", "mm", 500.0, jitter_us=0.5)
        sim = lob.DaySim([fast, slow], lob.DayParams(jumps=200, big_jump_p=0.2, noise_orders=400), rng)
        sim.run(None)
        front = {"fast": 0, "slow": 0}
        for (t, maker, taker, s, price, n, rank) in sim.fills:
            if rank == 0 and maker in front:
                front[maker] += n
        self.assertGreater(front["fast"], 2 * front["slow"])

    def test_sniper_takes_stale_quotes_of_slow_maker_only(self):
        rng = np.random.default_rng(1)
        firms = [lob.Firm("slow", "mm", 2000.0, jitter_us=1), lob.Firm("snipe", "sniper", 2.0, jitter_us=0.1)]
        sim = lob.DaySim(firms, lob.DayParams(jumps=300, big_jump_p=0.5, lead_p=0, sweep_p=0, noise_orders=0), rng)
        sim.run(None)
        hits = [f for f in sim.fills if f[2] == "snipe"]
        self.assertTrue(hits)
        self.assertTrue(all(f[1] == "slow" for f in hits))

    def test_deterministic(self):
        a = lob.simulate_day(1, np.random.default_rng(5))[1]
        b = lob.simulate_day(1, np.random.default_rng(5))[1]
        self.assertEqual(a, b)


class Funds(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(3)
        self.w = world.simulate(400, rng)
        self.units = world.strategies(self.w, np.random.default_rng(4))

    def test_no_lookahead_unit_returns(self):
        w = np.zeros((5, 2))
        w[2] = [1, -1]
        r = np.arange(10, dtype=float).reshape(5, 2)
        u, tau = world.unit_returns(w, r)
        self.assertEqual(u[2], 0.0)          # decided at close 2, earns day 3
        self.assertEqual(u[3], r[3, 0] - r[3, 1])

    def test_margin_call_closes_the_fund(self):
        spec = next(s for s in cast() if s.key == "big_bet")
        spec.risk["margin_call"] = -0.01
        res = run_fund(spec, self.units, self.w["reg"], None, [[1, 1, 1], [0, 0, 0]])
        self.assertIsNotNone(res["closed"])
        eq = res["equity"]
        self.assertTrue(np.all(eq[res["closed"] + 1:] == eq[res["closed"] + 1]))

    def test_build_period_has_no_trading_but_costs_accrue(self):
        spec = next(s for s in cast() if s.key == "your_md_fund")
        units = world.strategies(self.w, np.random.default_rng(4), **spec.strat_kw)
        res = run_fund(spec, units, self.w["reg"], None, [[1, 1, 1], [0, 0, 0]])
        self.assertTrue(np.all(res["equity"][:spec.start_day + 1] == spec.capital))
        f = fees_and_net(spec, res, 400 / 252)
        self.assertAlmostEqual(f["net"], f["trading_pnl"] - spec.opex * 400 / 252)


if __name__ == "__main__":
    unittest.main()
