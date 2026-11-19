# oe-04-risk: Pre-trade risk checks and the market access rule

Key facts and sources
- SEC Rule 15c3-5 (17 CFR 240.15c3-5): (c)(1)(i) prevent orders exceeding pre-set credit or capital thresholds; (c)(1)(ii) reject erroneous orders exceeding price or size parameters, order by order or over a short period, or duplicative orders; (d) controls under the broker-dealer's direct and exclusive control; (e) review at least annually, CEO certifies annually. Source: [17 CFR 240.15c3-5, govinfo](https://www.govinfo.gov/content/pkg/CFR-2011-title17-vol3/pdf/CFR-2011-title17-vol3-sec240-15c3-5.pdf).
- (c)(2) regulatory controls: prevent orders in securities a person is restricted from trading; restrict access to pre-approved and authorized persons and accounts; surveillance personnel receive immediate post-trade execution reports. Source: [17 CFR 240.15c3-5, Cornell LII](https://www.law.cornell.edu/cfr/text/17/240.15c3-5).
- Adopting release 34-63241, published 15 Nov 2010; effective 14 Jan 2011; compliance 14 Jul 2011; it eliminates "unfiltered" or "naked" access. Source: [Federal Register 2010-28303](https://www.federalregister.gov/documents/2010/11/15/2010-28303/risk-management-controls-for-brokers-or-dealers-with-market-access).
- Knight Capital: SEC charged it on 16 Oct 2013; on 1 Aug 2012 its router sent more than 4 million orders in the first 45 minutes while trying to fill 212 customer orders; $12 million penalty. Source: [SEC press release 2013-222](https://www.sec.gov/news/press-release/2013-222).
- Lab: `firm/risk/include/lab/risk/risk.hpp`: checks in order kill, quantity, notional, (no reference), collar, position (shares + working on that side + this order), open orders, rate (token bucket); with no two-sided market (mid 0) the order is blocked as "no reference price"; defaults 1,000 shares, $100,000, 500 bps, 2,000 shares, 200 orders, 2,000/s burst 100; cancels never checked; blocks counted per verdict.

Worked example (illustrative, lab default limits): mid 187.25, collar ±9.3625 (177.8875 to 196.6125); 400 x 187.30 = $74,920 passes; 600 x 187.30 = $112,380 blocked by notional; 500 x 197.00 = $98,500 blocked by the collar.

Unsure / left out: the 2011 extension of some compliance dates to 30 Nov 2011 (not verified, left out).
