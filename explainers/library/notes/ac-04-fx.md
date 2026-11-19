# ac-04-fx: FX spot, ECNs, banks and last look

Key facts and sources
- April 2025: $9.6 tn/day total FX, spot $3.0 tn (31%), FX swaps $4 tn, forwards $1.8 tn; USD on one side of 89.2%: BIS Triennial Survey 2025, https://www.bis.org/statistics/rpfx25_fx.htm
- Electronic execution 59% of turnover; dealers internalise "upwards of 80%" of customer trades in major hubs; most interbank trades settle through CLS: BIS Quarterly Review Dec 2025, https://www.bis.org/publ/qtrpdf/r_qt2512b.htm
- Spot = settlement within two business days; anonymous venues include Refinitiv Matching and EBS Market; disclosed multi-bank and single-bank platforms: BIS 2025 survey reporting guidelines, https://www.bis.org/publications/triennial-survey/2025survey-guidelinesturnover.pdf
- Last look definition and Principle 17 (transparency, disclosure; no trading on the client's trade request information during the window): FX Global Code, https://www.globalfxc.org/uploads/fx_global.pdf
- CLS settles payment-versus-payment (18 currencies per CLS overview, Feb 2024): https://www.cls-group.com/media/1f1hknvb/clssettlement_overview_feb2024_v1.pdf
- Lab: rt-server speaks the public Refinitiv WebSocket API (OMM JSON, tr_json2): /home/claude/ts-push/docs/specs/vendor-omm-json.md

Unsure / left out
- EUR/USD quotes, the last-look window and the reject are illustrative; no hold-time figures (none verified).
- "Many FX users watch vendor composite rates" is a general description, not a statistic.
- No microsecond latency claims for FX venues; I found no primary source.
