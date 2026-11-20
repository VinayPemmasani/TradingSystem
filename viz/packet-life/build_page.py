#!/usr/bin/env python3
"""Builds the packet-life page with its data inlined, so it opens straight from disk.

    python3 viz/packet-life/build_page.py                      uses trace.json beside this script
    ./build/release/tools/order-trace/order-trace > t.json
    python3 viz/packet-life/build_page.py --trace t.json --out packet-life.html
"""
import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def inline(obj) -> str:
    # Compact, and safe inside a <script> element.
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trace", default=HERE / "trace.json", type=pathlib.Path, help="order-trace output")
    ap.add_argument("--scene", default=HERE / "scene.json", type=pathlib.Path)
    ap.add_argument("--out", default=pathlib.Path("packet-life.html"), type=pathlib.Path)
    a = ap.parse_args()

    trace = json.loads(a.trace.read_text())
    scene = json.loads(a.scene.read_text())
    stage_ids = {s["id"]: s for s in trace["stages"]}
    for leg in scene["legs"]:
        src = stage_ids.get(leg.get("from", leg["stage"]))
        if leg["stage"] not in stage_ids or src is None:
            print(f"scene.json: stage {leg['stage']} is not in the trace", file=sys.stderr)
            return 1
        if leg["msg"] >= len(src["msgs"]):
            print(f"scene.json: {leg['stage']} has no message {leg['msg']}", file=sys.stderr)
            return 1

    page = (HERE / "index.html").read_text()
    for marker, obj in (("/*TRACE_JSON*/", trace), ("/*SCENE_JSON*/", scene)):
        if marker not in page:
            print(f"index.html has no {marker} marker", file=sys.stderr)
            return 1
        page = page.replace(marker, inline(obj), 1)
    a.out.write_text(page)
    print(f"Wrote {a.out}: {len(trace['stages'])} stages, {len(scene['legs'])} legs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
