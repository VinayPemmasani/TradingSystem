# Career track: market data developer to quant

`head_to_head.py` scores two profiles on the same 82 problems this project has built:
the 14 MD-413 and MD-414 incident reports (`interview/md-41{3,4}-exercise`), the 60
planted bugs of the MD-415 bug bank (`interview/md-415-bank`, copied to
`md415_bugs.json`), and 8 research problems from the $5bn paper fund run (PR #28).

- Profile A: a quant dev/researcher who knows a handful of exchanges.
- Profile B: a market data veteran, 15 years, 40-50 feeds, no strategy experience.
- Profile B+: the veteran after the 16-week course on the page.

Skill levels and engineering incident dollar values are assumptions, written out at the
top of the script. Paper fund dollar values are measured from that run. The script writes
`results.json`: chance solved, hours and value per problem, totals by group, a sweep over
fund size, and a 20,000-run Monte Carlo.

```bash
python3 career/head_to_head.py
python3 career/build_page.py --equity /mnt/project-files/paperfund/results/baseline_5bn/equity.csv \
    --out career/dist/index.html
```

`web/index.html` is the page template (Feed to Alpha): the gap map, ten animated course
modules, the head-to-head, and the pay question.
