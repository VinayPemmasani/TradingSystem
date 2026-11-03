"""Transaction costs and capacity. This is where a $5B fund and a $10k account differ most.

Per share traded, as a fraction of price:

    commission + half spread + impact,   impact = Y * sigma_daily * sqrt(q / ADV)

The square-root law is the standard empirical model of what large orders cost
(Almgren, Thum, Hauptmann and Li, "Direct Estimation of Equity Market Impact",
2005; Toth et al., "Anomalous price impact and the critical nature of
liquidity", 2011). A fill is also capped at ``max_participation`` of the day's
volume; the rest of the order is simply not done that day.
"""

from __future__ import annotations

import math

from .config import CostConfig


def half_spread_bps(price: float, adv_shares: float, cfg: CostConfig) -> float:
    dollar_adv = max(price * adv_shares, 1.0)
    return cfg.half_spread_bps * max(1.0, math.sqrt(1e9 / dollar_adv))


def cost_fraction(shares: float, price: float, adv_shares: float, sigma: float,
                  cfg: CostConfig) -> float:
    """Cost of trading ``shares`` (absolute) as a fraction of notional."""
    if shares <= 0:
        return 0.0
    adv = max(adv_shares, 1.0)
    impact = cfg.impact_coef * max(sigma, 0.003) * math.sqrt(shares / adv)
    fixed = (cfg.commission_bps + half_spread_bps(price, adv, cfg) + cfg.retail_fx_bps) / 1e4
    return fixed + impact


def fill_cap(adv_shares: float, cfg: CostConfig) -> float:
    return max(adv_shares, 0.0) * cfg.max_participation
