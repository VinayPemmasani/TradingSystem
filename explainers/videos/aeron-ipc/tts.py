import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/tmp/claude-0/av/voice/kokoro-v1.0.onnx","/tmp/claude-0/av/voice/voices-v1.0.bin")
S=json.load(open("/mnt/project-files/videos/aeron-source/script.json")); out={}
for name,text in S:
    # per-sentence for caption timing
    import re
    sents=re.split(r'(?<=[.!?])\s+',text); parts=[]; caps=[]; t=0
    for s in sents:
        a,sr=k.create(s.replace("ITCH","itch").replace("IPC","I P C").replace("OUCH","ouch").replace("cnc","C N C").replace("simex","sim ex"),voice="am_michael",speed=1.1,lang="en-us")
        gap=np.zeros(int(sr*0.24),dtype=a.dtype)
        caps.append([round(t,3),round(t+len(a)/sr,3),s]); parts+= [a,gap]; t+=len(a)/sr+0.24
    a=np.concatenate(parts); sf.write(f"/tmp/claude-0/av/audio/{name}.wav",a,sr); out[name]={"dur":round(len(a)/sr,3),"caps":caps}
    print(name,out[name]["dur"],flush=True)
json.dump(out,open("/tmp/claude-0/av/audio/timing.json","w"),indent=1)
