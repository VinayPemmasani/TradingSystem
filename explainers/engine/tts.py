# Narration for one video: python3 tts.py SLUG
# Reads <src>/script.json [{id,title,text}] and optional <src>/pron.json [[regex, spoken], ...]
# (applied to the spoken text only; captions show the written text).
import json, re, sys, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
slug = sys.argv[1]
SRC = f"/mnt/project-files/videos/explainers/{slug}"; W = f"/tmp/claude-0/vx/{slug}"
os.makedirs(f"{W}/audio", exist_ok=True)
k = Kokoro("/tmp/claude-0/av/voice/kokoro-v1.0.onnx", "/tmp/claude-0/av/voice/voices-v1.0.bin")
S = json.load(open(f"{SRC}/script.json"))
PR = json.load(open(f"{SRC}/pron.json")) if os.path.exists(f"{SRC}/pron.json") else []
only = set(sys.argv[2:])  # optional: re-voice only these scene ids
tpath = f"{W}/audio/timing.json"
out = json.load(open(tpath)) if (only and os.path.exists(tpath)) else {}
for sc in S:
    name, text = sc["id"], sc["text"]
    if only and name not in only: continue
    sents = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s]
    parts, caps, t = [], [], 0.0
    for s in sents:
        say = s
        for a, b in PR: say = re.sub(a, b, say)
        a, sr = k.create(say, voice="am_michael", speed=1.08, lang="en-us")
        gap = np.zeros(int(sr * 0.26), dtype=a.dtype)
        caps.append([round(t, 3), round(t + len(a) / sr, 3), s]); parts += [a, gap]; t += len(a) / sr + 0.26
    a = np.concatenate(parts); sf.write(f"{W}/audio/{name}.wav", a, sr)
    out[name] = {"dur": round(len(a) / sr, 3), "caps": caps}
    print(name, out[name]["dur"], flush=True)
json.dump(out, open(tpath, "w"), indent=1)
print("total", round(sum(v["dur"] for v in out.values()), 1))
