# reg-08-best-ex: Best execution and TCA

## Key facts and sources
- **FINRA Rule 5310(a)(1):** reasonable diligence to ascertain the best market so that "the resultant price to the customer is as favorable as possible under prevailing market conditions"; factors (A)-(E). Supplementary Material .09: regular and rigorous review at least quarterly, by security and order type; compares price improvement, worse-than-quote, limit fill rates, speed, size, costs. https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310
- **MiFID II Art. 27(1):** "all sufficient steps to obtain ... the best possible result", taking into account price, costs, speed, likelihood of execution and settlement, size, nature. https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-27-obligation-execute-orders
- **Implementation shortfall:** Perold, "The Implementation Shortfall: Paper versus Reality", Journal of Portfolio Management (1988). https://www.proquest.com/docview/195579087
- **Lab:** research/lab_research/tca.py: capture s*(m0 - price) with the mid strictly before the fill; markouts at 1 ms, 10 ms, 100 ms, 1 s; summary in cents/share and bp. On-screen code is simplified.
- All prices in examples are illustrative (20.00 / 20.03 -> 15 bp; 19.99 buy, mid 20.00 -> 19.97).

## Unsure / left out
- SEC Rules 605/606 and their 2024 amendments' compliance dates: not verified, left out.
- The SEC's 2022 Regulation Best Execution proposal and its status: left out.
