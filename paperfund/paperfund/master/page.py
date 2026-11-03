"""Fill the master page template. Usage:
python3 -m paperfund.master.page out/master/master.json out/master/index.html [run_date]"""

import json
import sys
from datetime import date
from pathlib import Path

TEMPLATE = Path(__file__).with_name("web") / "master.html"


def build(master_json, out_html, run_date=None):
    data = Path(master_json).read_text()
    html = TEMPLATE.read_text().replace("/*MASTER_DATA*/null", data).replace(
        '/*RUN_DATE*/""', json.dumps(run_date or date.today().isoformat()))
    Path(out_html).write_text(html)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
