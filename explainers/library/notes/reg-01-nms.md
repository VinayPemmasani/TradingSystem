# reg-01-nms: Reg NMS and order protection

## Key facts and sources
- **Adoption:** SEC voted 3-2 on April 6, 2005; adopting release 34-51808 issued June 9, 2005, effective Aug 29, 2005. Sources: https://www.sec.gov/rules/final/34-51808.pdf ; https://www.wilmerhale.com/en/insights/publications/sec-issues-regulation-nms-adopting-release-starting-the-clock-on-sweeping-overhaul-of-the-national-market-system-june-17-2005
- **Rule 611:** trading centers must keep written policies "reasonably designed to prevent trade-throughs" of protected quotations; exceptions in 611(b) include ISOs received (b)(5) and ISOs routed (b)(6). Protected quote = automated top of book of an exchange/ADF. Source: https://www.law.cornell.edu/cfr/text/17/242.611
- **Rule 610 cap:** $0.003/share (0.3% of quote below $1.00). **Rule 612:** no quotes in increments below $0.01 at or above $1.00; $0.0001 below. Source: Release 34-51808.
- **2024 amendments** (Release 34-101070, adopted Sep 18, 2024): $0.005 tick for stocks with TWAQS <= $0.015; fee cap $0.001 (0.1% below $1). https://www.sec.gov/newsroom/press-releases/2024-137 ; https://www.federalregister.gov/documents/2024/10/08/2024-21867
- **Delays:** partial stay Dec 12, 2024; D.C. Circuit denied review Oct 14, 2025; relief orders 34-104172 (Oct 31, 2025) and 34-105656 (Jun 11, 2026) move 610(c)/612 compliance to the first business day of Nov 2027 (Nov 1, 2027). https://www.sec.gov/files/rules/exorders/2026/34-105656.pdf
- **Proposal to rescind Rule 611 and 610(e):** Release 34-105655, FR Jun 17, 2026, comments due Aug 17, 2026. https://www.govinfo.gov/content/pkg/FR-2026-06-17/html/2026-12163.htm
- **Lab:** OUCH Enter Order ISO at offset 29 (Replace: 23), docs/specs/ouch50-layout.md, libs/ouch/include/lab/ouch/messages.hpp. simex never reads the field and does not check price increments (gateway.cpp admit()).
- **Worked example:** illustrative prices; 100x10.01+300x10.02+100x10.03 = 5,010 / 500 = $10.02.

## Unsure / left out
- Exact phase-in dates for Rule 611 compliance (2006-2007): not re-read, left out.
- Number of US exchanges/venues: not stated.
- The 2026 rescission proposal's outcome is unknown as of Nov 2026.
