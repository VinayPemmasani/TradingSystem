# python3 build_data.py SLUG  -> /tmp/claude-0/vx/SLUG/data.json and narration.wav
import json, subprocess, sys
slug = sys.argv[1]
SRC = f"/mnt/project-files/videos/explainers/{slug}"; W = f"/tmp/claude-0/vx/{slug}"
T = json.load(open(f"{W}/audio/timing.json")); S = json.load(open(f"{SRC}/script.json"))
V = json.load(open(f"{SRC}/video.json"))
LEAD, TAIL = 0.6, 1.8
scenes, t = [], 0.0
for i, sc in enumerate(S):
    k = sc["id"]; extra = float(sc.get("hold", 0))  # optional silent hold after narration
    off = LEAD if i == 0 else 0
    dur = T[k]["dur"] + off + extra + (TAIL if i == len(S) - 1 else 0)
    scenes.append({"id": k, "title": sc.get("title", k), "start": round(t, 3), "dur": round(dur, 3),
                   "caps": [[round(c[0] + off, 3), round(c[1] + off, 3), c[2]] for c in T[k]["caps"]]})
    t += dur
json.dump({"brand": V.get("brand", ""), "scenes": scenes, "total": round(t, 3)}, open(f"{W}/data.json", "w"), indent=1)
# audio: each scene's wav, padded to its scene length
filt, ins = [], []
for i, sc in enumerate(scenes):
    ins += ["-i", f"{W}/audio/{sc['id']}.wav"]
    off = LEAD if i == 0 else 0
    filt.append(f"[{i}]adelay={int(off*1000)}:all=1,apad=whole_dur={sc['dur']},atrim=0:{sc['dur']}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=0:a=1[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", f"{W}/narration.wav"], check=True)
print("total", round(t, 1), "s")
