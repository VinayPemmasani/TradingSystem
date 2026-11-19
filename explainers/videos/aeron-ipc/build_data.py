# Lays the narrated scenes end to end (0.5 s lead-in, 1.5 s tail) and writes
# data.json for stage.html plus the full narration track.
import json, subprocess
T = json.load(open("/tmp/claude-0/av/audio/timing.json"))
order = [k for k, _ in json.load(open("/mnt/project-files/videos/aeron-source/script.json"))]
LEAD, TAIL = 0.5, 1.5
scenes, t = [], 0.0
for i, k in enumerate(order):
    dur = T[k]["dur"] + (LEAD if i == 0 else 0) + (TAIL if i == len(order) - 1 else 0)
    off = LEAD if i == 0 else 0
    scenes.append({"id": k, "start": round(t, 3), "dur": round(dur, 3),
                   "caps": [[c[0] + off, c[1] + off, c[2]] for c in T[k]["caps"]]})
    t += dur
json.dump({"scenes": scenes, "total": round(t, 3)}, open("/tmp/claude-0/av/data.json", "w"), indent=1)
with open("/tmp/claude-0/av/audio/list.txt", "w") as f:
    for k in order: f.write(f"file '/tmp/claude-0/av/audio/{k}.wav'\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/claude-0/av/audio/list.txt",
                "-af", f"adelay={int(LEAD*1000)}:all=1,apad=pad_dur={TAIL}", "-ar", "48000", "/tmp/claude-0/av/narration.wav"], check=True)
print("total", round(t, 3))
