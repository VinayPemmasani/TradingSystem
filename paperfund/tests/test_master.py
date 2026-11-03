import math
import unittest

import numpy as np

from paperfund.master import stats


class StatsTest(unittest.TestCase):
    def test_sharpe_and_psr_on_known_series(self):
        rng = np.random.default_rng(1)
        r = rng.normal(0.001, 0.01, 2520)  # true annual Sharpe about 1.59
        self.assertAlmostEqual(stats.sharpe(r), 1.59, delta=0.35)
        self.assertGreater(stats.psr(r), 0.99)
        self.assertLess(stats.psr(-r), 0.01)

    def test_deflation_needs_more_than_luck(self):
        rng = np.random.default_rng(2)
        trials = [stats.sharpe(rng.normal(0, 0.01, 252)) for _ in range(50)]
        self.assertGreater(stats.expected_max_sharpe(trials), 1.0)  # best of 50 coin flips looks good
        r = rng.normal(0.0004, 0.01, 252)
        self.assertLess(stats.dsr(r, trials), stats.psr(r))

    def test_alpha_beta_recovers_beta(self):
        rng = np.random.default_rng(3)
        b = rng.normal(0, 0.01, 1000)
        r = 0.5 * b + rng.normal(0, 0.002, 1000)
        _, beta, _ = stats.alpha_beta(r, b)
        self.assertAlmostEqual(beta, 0.5, delta=0.03)

    def test_bootstrap_interval_contains_point_estimate(self):
        r = np.random.default_rng(4).normal(0.0005, 0.01, 300)
        lo, hi = stats.bootstrap_sharpe_ci(r, reps=300)
        self.assertLess(lo, stats.sharpe(r))
        self.assertGreater(hi, stats.sharpe(r))

    def test_sign_test(self):
        self.assertAlmostEqual(stats.sign_test_p(20, 20), 0.5 ** 20)
        self.assertAlmostEqual(stats.sign_test_p(0, 5), 1.0)
        self.assertTrue(math.isclose(stats._phi_inv(0.975), 1.959964, abs_tol=1e-5))


if __name__ == "__main__":
    unittest.main()
