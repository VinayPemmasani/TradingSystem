"""The tests every strategy result in this project goes through, in one place.

Daily returns in, plain floats out. numpy only. References:
- Probabilistic and Deflated Sharpe Ratio: Bailey and Lopez de Prado (2012, 2014).
- Minimum track record length: Bailey and Lopez de Prado (2012).
- Stationary block bootstrap: Politis and Romano (1994).
"""

from __future__ import annotations

import math

import numpy as np

DAYS = 252
_EULER = 0.5772156649015329


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _phi_inv(p: float) -> float:
    # Acklam's rational approximation, |error| < 1.2e-9; enough for test thresholds.
    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00, 3.754408661907416e00]
    lo = 0.02425
    if p < lo:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > 1 - lo:
        return -_phi_inv(1 - p)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def moments(r: np.ndarray) -> tuple[float, float, float, float]:
    r = np.asarray(r, float)
    mu, sd = r.mean(), r.std(ddof=1)
    if sd == 0:
        return mu, 0.0, 0.0, 3.0
    z = (r - mu) / sd
    return float(mu), float(sd), float((z ** 3).mean()), float((z ** 4).mean())


def sharpe(r) -> float:
    mu, sd, _, _ = moments(r)
    return mu / sd * math.sqrt(DAYS) if sd else 0.0


def max_drawdown(r) -> float:
    eq = np.cumprod(1 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def psr(r, sr_benchmark_annual: float = 0.0) -> float:
    """Probability the true Sharpe beats the benchmark, given skew and fat tails."""
    mu, sd, sk, ku = moments(r)
    if not sd:
        return 0.5
    sr = mu / sd
    sr0 = sr_benchmark_annual / math.sqrt(DAYS)
    den = math.sqrt(max(1e-12, 1 - sk * sr + (ku - 1) / 4 * sr * sr))
    return _phi((sr - sr0) * math.sqrt(len(r) - 1) / den)


def expected_max_sharpe(trial_sharpes_annual: list[float]) -> float:
    """Sharpe the best of N worthless trials would show by luck (annualised)."""
    n = len(trial_sharpes_annual)
    if n < 2:
        return 0.0
    v = float(np.var(np.asarray(trial_sharpes_annual) / math.sqrt(DAYS), ddof=1))
    e = math.sqrt(v) * ((1 - _EULER) * _phi_inv(1 - 1 / n) + _EULER * _phi_inv(1 - 1 / (n * math.e)))
    return e * math.sqrt(DAYS)


def dsr(r, trial_sharpes_annual: list[float]) -> float:
    """Deflated Sharpe: PSR against the best Sharpe luck alone would give over all trials."""
    return psr(r, expected_max_sharpe(trial_sharpes_annual))


def min_track_record_years(r, confidence: float = 0.95) -> float | None:
    """Years of this track record needed to say Sharpe > 0 at the confidence; None if Sharpe <= 0."""
    mu, sd, sk, ku = moments(r)
    if not sd or mu <= 0:
        return None
    sr = mu / sd
    n = 1 + (1 - sk * sr + (ku - 1) / 4 * sr * sr) * (_phi_inv(confidence) / sr) ** 2
    return n / DAYS


def bootstrap_sharpe_ci(r, reps: int = 2000, block: int = 10, seed: int = 7) -> tuple[float, float]:
    """95% interval for the annual Sharpe from a stationary block bootstrap."""
    r = np.asarray(r, float)
    n = len(r)
    rng = np.random.default_rng(seed)
    out = np.empty(reps)
    for i in range(reps):
        idx = np.empty(n, int)
        j = rng.integers(n)
        for k in range(n):
            if k and rng.random() < 1 / block:
                j = rng.integers(n)
            idx[k] = j
            j = (j + 1) % n
        out[i] = sharpe(r[idx])
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def alpha_beta(r, bench) -> tuple[float, float, float]:
    """Annual alpha, beta and the alpha t-stat from an OLS of r on the benchmark."""
    r, b = np.asarray(r, float), np.asarray(bench, float)
    x = np.column_stack([np.ones_like(b), b])
    coef, *_ = np.linalg.lstsq(x, r, rcond=None)
    resid = r - x @ coef
    s2 = resid @ resid / (len(r) - 2)
    cov = s2 * np.linalg.inv(x.T @ x)
    return float(coef[0] * DAYS), float(coef[1]), float(coef[0] / math.sqrt(cov[0, 0]))


def scorecard(r, bench=None, trials: list[float] | None = None) -> dict:
    r = np.asarray(r, float)
    mu, sd, sk, ku = moments(r)
    lo, hi = bootstrap_sharpe_ci(r)
    out = {
        "days": int(len(r)),
        "ann_return": float((np.prod(1 + r)) ** (DAYS / len(r)) - 1),
        "ann_vol": sd * math.sqrt(DAYS),
        "sharpe": sharpe(r),
        "sharpe_ci95": [lo, hi],
        "t_stat": (mu / sd * math.sqrt(len(r))) if sd else 0.0,
        "psr": psr(r),
        "skew": sk,
        "kurtosis": ku,
        "max_drawdown": max_drawdown(r),
        "hit_rate": float((r > 0).sum() / max(1, (r != 0).sum())),
        "min_track_years": min_track_record_years(r),
    }
    if trials:
        out["dsr"] = dsr(r, trials)
        out["luck_sharpe"] = expected_max_sharpe(trials)
    if bench is not None:
        a, b, t = alpha_beta(r, bench)
        out.update(alpha=a, beta=b, alpha_t=t)
    return out


def sign_test_p(wins: int, n: int) -> float:
    """One-sided p-value that at least `wins` of n coin flips come up heads."""
    return float(sum(math.comb(n, k) for k in range(wins, n + 1)) / 2 ** n)
