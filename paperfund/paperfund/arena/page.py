"""Fill the Fund Arena page template with an arena.json. Usage:
python3 -m paperfund.arena.page out/arena/arena.json out/arena/index.html [doc_url]"""

import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).with_name("web") / "arena.html"


def build(arena_json, out_html, doc_url="#"):
    data = Path(arena_json).read_text()
    html = TEMPLATE.read_text().replace("/*ARENA_DATA*/null", data).replace('/*DOC_URL*/"#"', json.dumps(doc_url))
    Path(out_html).write_text(html)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "#")
