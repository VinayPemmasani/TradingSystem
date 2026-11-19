# oe-10-sor: Smart order routing

Key facts and sources
- Reg NMS Rule 611(a)(1): trading centers must keep policies reasonably designed to prevent trade-throughs of protected quotations; exceptions include intermarket sweep orders ((b)(5), (b)(6)). Source: [17 CFR 242.611](https://www.law.cornell.edu/cfr/text/17/242.611).
- Definitions (242.600(b)): protected bid/offer = displayed by an automated trading center, disseminated under an NMS plan, and the best bid or offer of an exchange or association; only quotes of automated trading centers are protected; ISO = limit order marked ISO, sent simultaneously with orders to take the full displayed size of every better protected quote. Source: [17 CFR 242.600](https://www.law.cornell.edu/cfr/text/17/242.600).
- June 2026: the SEC proposed rescinding Rules 611 and 610(e) (proposed rule, comments due 17 Aug 2026). Source: [Federal Register 2026-12163](https://www.govinfo.gov/content/pkg/FR-2026-06-17/html/2026-12163.htm). No adoption found by 19 Nov 2026.
- Lab: one venue (simex); OUCH Enter Order ISO at byte 29, Replace Order at byte 23, echoed in Order Accepted at byte 45 (`docs/specs/ouch50-layout.md`); `firm/strategy/include/lab/strategy/execution.hpp` `work_toward()` (capped child) and `pov_child()` (default 600 bps = 6% of market volume).

Worked example (illustrative): buy 1,000 up to 187.26; A 300 @ 187.25, B 200 @ 187.25, C 500 @ 187.26; three ISOs.

Unsure / left out: access fee caps and their 2024 amendments (not verified, left out); no claims about router performance.
