# Median ns per increment over chunks where the other thread ran a clean chunk the whole time.
import numpy as np, sys, bisect
GHZ = float(sys.argv[1]) if len(sys.argv) > 1 else 2.1
K = 2000
def load(name):
    d = np.fromfile(f"chunks_{name}.bin", dtype=np.uint64).astype(np.float64).reshape(2, -1, 2)
    return d[0], d[1]
def clean(ch):
    dur = ch[:, 1] - ch[:, 0]
    return dur < 0.4e-3 * GHZ * 1e9                 # under 0.4 ms: not preempted
def overlapped(a, b, bclean):
    # an a-chunk counts if b's clean chunks cover its whole interval
    bs, be = b[:, 0], b[:, 1]
    ok = np.zeros(len(a), bool)
    for i, (s, e) in enumerate(a):
        j = np.searchsorted(be, s)                 # first b chunk ending after s
        cov = s
        while j < len(b) and bs[j] <= cov + 2000 and bclean[j]:
            cov = max(cov, be[j])
            if cov >= e: ok[i] = True; break
            j += 1
    return ok
for name in ("packed", "padded"):
    a, b = load(name)
    ca, cb = clean(a), clean(b)
    oa = overlapped(a, b, cb) & ca
    ob = overlapped(b, a, ca) & cb
    dur = np.concatenate([(a[:, 1] - a[:, 0])[oa], (b[:, 1] - b[:, 0])[ob]]) / GHZ / K
    alld = np.concatenate([a[:, 1] - a[:, 0], b[:, 1] - b[:, 0]]) / GHZ / K
    print(f"{name}: overlapped chunks {oa.sum()+ob.sum()} of {2*len(a)}  median {np.median(dur):.2f} ns/inc  (all chunks median {np.median(alld):.2f})")
