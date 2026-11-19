# Generates scenes.html and style.css for the kafka explainer.
OUT = "/mnt/project-files/videos/explainers/kafka"
H = []
def a(s): H.append(s)

def attrs(cue=None, d=None, anim=None, out=None, od=None, hl=None, hld=None, hlend=None, dim=None, dimend=None, extra=""):
    s = ""
    if cue is not None: s += f' data-cue="{cue}"'
    if d: s += f' data-d="{d}"'
    if anim: s += f' data-anim="{anim}"'
    if out is not None: s += f' data-out="{out}"'
    if od: s += f' data-od="{od}"'
    if hl is not None: s += f' data-hl="{hl}"'
    if hld: s += f' data-hld="{hld}"'
    if hlend is not None: s += f' data-hlend="{hlend}"'
    if dim is not None: s += f' data-dim="{dim}"'
    if dimend is not None: s += f' data-dimend="{dimend}"'
    return s + extra

def box(x, y, w, t, s="", col="", cue=None, d=None, h=None, style="", tsize=None, **k):
    hs = f"height:{h}px;" if h else ""
    ts = f' style="font-size:{tsize}px"' if tsize else ""
    sub = f'<div class="s">{s}</div>' if s else ""
    a(f'<div class="box {col}" style="left:{x}px;top:{y}px;width:{w}px;{hs}{style}"{attrs(cue, d, **k)}><div class="t"{ts}>{t}</div>{sub}</div>')

def tag(x, y, text, cue=None, d=None, style="", cls="tag", **k):
    a(f'<div class="{cls}" style="left:{x}px;top:{y}px;{style}"{attrs(cue, d, **k)}>{text}</div>')

def div(x, y, html, cue=None, d=None, style="", cls="", **k):
    c = f' class="{cls}"' if cls else ""
    a(f'<div{c} style="left:{x}px;top:{y}px;{style}"{attrs(cue, d, **k)}>{html}</div>')

COL = {"teal": "#3fd0dc", "amber": "#ffb347", "green": "#4fd18b", "red": "#ff6b5e", "violet": "#a98bff", "blue": "#6aa8ff", "pink": "#ff8fc8", "muted": "#8ea3b1"}
def path(pid, dd, col, cue, d=None, dur=None, arrow=True, width=4, dash=False, **k):
    mk = {"teal": "ah-teal", "amber": "ah-amber", "green": "ah-green", "red": "ah-red", "violet": "ah-violet"}.get(col, "ah")
    m = f' marker-end="url(#{mk})"' if arrow else ""
    du = f' data-dur="{dur}"' if dur else ""
    pid_s = f' id="{pid}"' if pid else ""
    da = ' stroke-dasharray="8 8"' if dash else ""
    cls = "" if dash else ' class="draw"'
    # dashed paths fade in instead of drawing (draw uses the dasharray itself)
    an = ' data-anim="fade"' if dash else ""
    a(f'<path{pid_s}{cls} d="{dd}" fill="none" stroke="{COL[col]}" stroke-width="{width}" stroke-linecap="round"{da}{m}{an}{attrs(cue, d, **k)}{du}/>')

def pkt(pid, cue, col="teal", d=None, dur=1.4, loop=True, phase=0, size=None, **k):
    sz = f"width:{size}px;height:{size}px;margin:-{size//2}px 0 0 -{size//2}px;" if size else ""
    a(f'<div class="pkt" data-path="{pid}" data-dur="{dur}"{" data-loop=\"1\"" if loop else ""} data-phase="{phase}" style="{sz}background:var(--{col});box-shadow:0 0 14px var(--{col})"{attrs(cue, d, **k)}></div>')

def svg_open(): a('<svg class="full">')
def svg_close(): a('</svg>')

def scene(sid): a(f'\n<!-- {sid} -->\n<div class="scene" id="s-{sid}">')
def end(): a('</div>')

def h2(text, cue=0, top=112):
    a(f'<div class="h2" style="left:120px;top:{top}px"{attrs(cue)}>{text}</div>')

def pipeline(active, cue=0):
    steps = ["send()", "serialize", "partition", "accumulator", "sender", "broker"]
    parts = []
    for i, s in enumerate(steps):
        c = "chip on" if s == active else "chip"
        parts.append(f'<span class="{c}">{s}</span>')
        if i < len(steps) - 1: parts.append('<span class="arr">→</span>')
    a(f'<div class="pipe" style="left:120px;top:196px"{attrs(cue, 0.3)}>{"".join(parts)}</div>')

# ------------------------------------------------------------------ hook
scene("hook")
div(120, 200, "TRADING LAB · LOW LEVEL", cls="eyebrow")
div(112, 250, "Kafka", cls="h1")
div(120, 420, "A pump, topics and partitions,<br>from the bytes up", cls="sub", style="width:820px")
div(120, 560, "a design sketch · the lab has no Kafka today", cue=2, d=1.5, cls="lbl", style="color:var(--amber)")
div(1000, 186, "HOT PATH · multicast + shared memory", cue=0, d=-0.4, cls="lbl", style="color:var(--blue)")
box(1000, 230, 230, "simex", col="blue", cue=0, d=-0.3, tsize=28)
box(1290, 230, 230, "itch-fh", col="blue", cue=0, d=0.2, tsize=28)
box(1580, 230, 220, "trader", col="blue", cue=0, d=0.7, tsize=28)
for i, (n, c) in enumerate([("risk", "red"), ("research", "violet"), ("audit", "green"), ("TCA", "pink")]):
    box(1580, 470 + i * 100, 220, n, col=c, cue=1, d=0.5 + 0.6 * i, tsize=28)
box(1000, 470, 260, "pump", "drop copy → topics", col="amber", cue=2, d=0.2, tsize=30)
box(1000, 720, 260, "Kafka", "fills · quotes", col="teal", cue=2, d=1.2, tsize=30)
svg_open()
path(None, "M1232 268 L1284 268", "muted", 0, d=0, width=3)
path(None, "M1522 268 L1574 268", "muted", 0, d=0.5, width=3)
path("hk-a", "M1115 310 L1115 464", "amber", 2, d=0)
path("hk-b", "M1130 568 L1130 714", "amber", 2, d=1.0)
for i in range(4):
    y = 508 + i * 100
    path(f"hk-c{i}", f"M1262 760 C1420 760 1420 {y} 1574 {y}", "teal", 2, d=1.6 + 0.2 * i, width=3)
svg_close()
pkt("hk-a", 2, "amber", d=0.8, dur=1.2, phase=0)
pkt("hk-b", 2, "amber", d=1.6, dur=1.2, phase=0.5)
for i, c in enumerate(["red", "violet", "green", "pink"]):
    pkt(f"hk-c{i}", 2, c, d=2.2 + 0.1 * i, dur=1.6, phase=0.25 * i)
end()

# ------------------------------------------------------------------ pump
scene("pump")
h2("The pump")
box(700, 300, 360, "pump", "KafkaProducer<br>acks=all · idempotent", col="amber", cue=0, d=0.3)
box(120, 230, 400, "drop copy", "simex → DROP01 session<br>SoupBinTCP · every fill", col="blue", cue=1)
box(120, 470, 400, "itch-fh", "ITCH 5.0 market data", col="blue", cue=2)
box(1180, 230, 300, "fills", "key = Account", col="teal", cue=3, d=0.6)
box(1180, 470, 300, "quotes", "key = Symbol", col="teal", cue=3, d=1.2)
div(720, 450, "record = key + value", cue=3, d=2.4, cls="tag", style="color:var(--amber)")
cons = [("risk", "red"), ("research", "violet"), ("audit", "green"), ("TCA", "pink")]
for i, (n, c) in enumerate(cons):
    box(1580, 200 + i * 110, 220, n, col=c, cue=4, d=0.2 + 0.4 * i, tsize=28)
svg_open()
path("pm-a", "M524 300 C610 300 610 345 696 345", "blue", 1, d=0.4)
path("pm-b", "M524 515 C610 515 610 395 696 395", "blue", 2, d=0.4)
path("pm-c", "M1064 345 C1120 345 1120 280 1176 280", "amber", 3, d=0.6)
path("pm-d", "M1064 395 C1120 395 1120 520 1176 520", "amber", 3, d=1.2)
for i, (n, c) in enumerate(cons):
    y = 238 + i * 110
    path(f"pm-f{i}", f"M1482 270 C1530 270 1530 {y} 1576 {y}", c, 4, d=0.3 + 0.4 * i, width=3)
for i, (n, c) in [(1, cons[1]), (3, cons[3])]:
    y = 248 + i * 110
    path(f"pm-q{i}", f"M1482 515 C1530 515 1530 {y} 1576 {y}", c, 4, d=1.6, width=3)
svg_close()
pkt("pm-a", 1, "blue", d=1.2, dur=1.3)
pkt("pm-b", 2, "blue", d=1.0, dur=1.3, phase=0.4)
pkt("pm-c", 3, "amber", d=1.4, dur=1.1)
pkt("pm-d", 3, "amber", d=2.0, dur=1.1, phase=0.5)
# drop copy bytes
fields = [("D", 1, "#f3c56b"), ("Timestamp", 8, "#7fb2ff"), ("Account", 6, "#ffb347"), ("UserRef", 4, "#7fb2ff"),
          ("S", 1, "#9ec4ff"), ("Qty", 4, "#7fb2ff"), ("Symbol", 8, "#9ec4ff"), ("Price", 8, "#7fb2ff"),
          ("Match No.", 8, "#9ec4ff"), ("L", 1, "#7fb2ff"), ("Order Ref", 8, "#9ec4ff")]
sc = 28
cells = "".join(f'<div style="width:{n*sc}px;background:{c}">{f}</div>' for f, n, c in fields)
div(160, 708, "EXECUTION REPORT 'D' · 57 BYTES · BIG-ENDIAN · LAB DROP COPY", cue=1, d=0.8, cls="lbl")
div(160, 748, cells, cue=1, d=1.2, cls="bytes")
offs = [0]
for f, n, c in fields: offs.append(offs[-1] + n)
o = "".join(f'<span style="position:absolute;left:{x*sc}px;transform:translateX(-50%)">{x}</span>' for x in offs if x not in (1, 20, 49))
div(160, 826, o, cue=1, d=1.6, cls="lbl", style="width:1600px;height:30px;font-size:18px")
div(160 + 9 * sc, 864, "↑ Account becomes the key of the fills topic", cue=3, d=3.0, cls="lbl", style="color:var(--amber)")
end()

# ------------------------------------------------------------------ log
scene("log")
h2("A partition is an append-only log")
div(120, 215, "topic: fills", cue=0, d=0.4, cls="lbl", style="color:var(--teal)")
rows = [11, 8, 10]
for r, n in enumerate(rows):
    y = 290 + r * 140
    div(120, y + 18, f"fills-{r}", cue=0, d=0.6 + 0.3 * r, cls="h3", style="font-size:32px;font-family:var(--mono)")
    for i in range(n):
        last = (r == 0 and i == n - 1)
        bg = "#ffb347" if last else ("#2a8f9b" if i % 2 else "#3fd0dc")
        if last:
            div(330 + i * 100, y, f"{i}", cue=1, d=1.6, cls="cellk", anim="left", hl=2, hlend=3,
                style=f"width:92px;background:{bg}")
        else:
            div(330 + i * 100, y, f"{i}", cue=1, d=round(0.07 * i + 0.25 * r, 2), cls="cellk", anim="scale",
                style=f"width:92px;background:{bg}")
div(330 + 11 * 100 + 10, 306, "← append", cue=1, d=1.4, cls="lbl", style="color:var(--amber);font-size:26px")
div(330, 740, "offset · int64 · assigned by the leader · never changes, never reused", cue=2, d=0.4, cls="tag", style="font-size:24px;color:var(--teal)")
# readers on row 2
y2 = 290 + 2 * 140
for off, n, c in [(7, "risk", "red"), (3, "audit", "green")]:
    x = 330 + off * 100 - 4
    div(x, y2 - 10, "", cue=3, d=0.4 if n == "risk" else 1.2, anim="fade", style=f"width:5px;height:92px;background:var(--{c});border-radius:3px")
    div(x - 40, y2 + 90, f"{n} @ {off}", cue=3, d=0.4 if n == "risk" else 1.2, cls="lbl", style=f"color:var(--{c})")
div(330, 820, "a reader's whole state is one number per partition: the next offset", cue=3, d=2.0, cls="body")
end()

# ------------------------------------------------------------------ partition
scene("partition")
h2("Choosing a partition")
pipeline("partition")
box(120, 300, 420, "ProducerRecord", 'topic <span class="c-teal">fills</span><br>key&nbsp;&nbsp; <span class="c-amber">"FIRM02"</span><br>value 57 bytes', col="amber", cue=0, d=0.6)
div(120, 500, 'key bytes  46 49 52 4D 30 32', cue=0, d=2.4, cls="tag", style="font-size:22px")
code = ('<span class="line" data-hl="1" data-hld="0.5" data-hlend="1.45">h = <span class="k">murmur2</span>(keyBytes)   <span class="c">// 0x9550D99D, negative</span></span>'
        '<span class="line" data-hl="1.45" data-hlend="1.75">h &amp; <span class="r">0x7fffffff</span>         <span class="c">// 0x1550D99D</span></span>'
        '<span class="line" data-hl="1.75" data-hlend="3">  % numPartitions (<span class="r">6</span>) <span class="c">// = 1</span></span>')
div(600, 300, code, cue=1, cls="code", style="width:840px;font-size:26px")
for i in range(6):
    hlk = {}
    if i == 1: hlk = dict(hl=1.8, hlend=3)
    if i == 4: hlk = dict(hl=3, hld=0.5, hlend=4)
    if i == 5: hlk = dict(hl=4, hld=0.3)
    box(1520, 290 + i * 82, 280, f"fills-{i}", col="teal", cue=0, d=0.8 + 0.12 * i, tsize=26, style="padding:10px 20px", **hlk)
div(600, 470, 'FIRM02 → always fills-1 · FIRM01 → fills-0', cue=2, d=0.2, cls="tag", style="font-size:24px;color:var(--amber)")
div(600, 520, 'same key, same partition (while the count stays at 6)', cue=2, d=1.2, cls="lbl")
svg_open()
path("pt-k", "M1442 420 C1480 420 1480 395 1516 395", "amber", 2, d=0.0, width=3)
path("pt-s1", "M1032 700 C1300 700 1300 645 1516 645", "violet", 3, d=3.2, width=3)
path("pt-s2", "M432 790 C1200 790 1300 733 1516 733", "violet", 4, d=0.6, width=3)
svg_close()
pkt("pt-k", 2, "amber", d=0.4, dur=0.9)
pkt("pt-k", 2, "amber", d=0.7, dur=0.9, phase=0.5)
div(120, 620, 'key = null → sticky partition', cue=3, cls="lbl", style="color:var(--violet);font-size:24px")
div(120, 680, '<div style="position:absolute;inset:0;border:2px dashed var(--line);border-radius:6px"></div>', cue=3, d=0.2, style="width:900px;height:40px")
div(120, 680, '', cue=3, d=0.4, cls="grow", extra=' data-w="900" data-dur="3.4"', style="height:40px;background:var(--violet);border-radius:6px;opacity:.85")
div(130, 686, 'bytes sent to fills-4', cue=3, d=0.8, style="font:600 22px var(--mono);color:#140d2a")
div(1030, 640, 'batch.size', cue=3, d=3.0, cls="lbl", style="color:var(--violet)")
div(120, 770, '', cue=4, d=0.0, cls="grow", extra=' data-w="300" data-dur="2"', style="height:40px;background:var(--violet);border-radius:6px;opacity:.6")
div(130, 776, 'then fills-5', cue=4, d=0.3, style="font:600 22px var(--mono);color:#140d2a")
div(120, 830, 'adaptive: picks less-loaded brokers more often', cue=4, d=0.8, cls="lbl", style="color:var(--violet)")
end()

# ------------------------------------------------------------------ batch
scene("batch")
h2("The record accumulator")
pipeline("accumulator")
div(120, 290, '<div class="lbl" style="position:absolute;left:24px;top:16px">RecordAccumulator · one deque of batches per partition · buffer.memory 32 MiB</div>',
    cue=0, d=0.3, style="width:1120px;height:540px;border:2px solid var(--amber);border-radius:16px;background:rgba(19,33,43,.7)")
prow = [("fills-0", 370), ("fills-1", 500), ("quotes-3", 630)]
for i, (n, y) in enumerate(prow):
    div(150, y + 16, n, cue=0, d=0.6 + 0.2 * i, cls="lbl", style="font-size:24px;color:var(--teal)")
    for j in range(2 if i != 1 else 1):
        div(330 + j * 160, y, "sealed", cue=0, d=0.8 + 0.2 * i + 0.1 * j, cls="cellk", style="width:140px;background:#2a8f9b;font-size:18px")
    xx = 330 + (2 if i != 1 else 1) * 160
    div(xx, y, '', cue=0, d=0.9 + 0.2 * i, style="width:300px;height:70px;border:2px dashed #ffb347;border-radius:6px")
# row 0 fills to batch.size
x0 = 330 + 2 * 160
div(x0, 370, '', cue=1, d=0.2, cls="grow", extra=' data-w="300" data-dur="2.8" data-out="3" data-od="0.2"', style="height:70px;background:var(--amber);border-radius:6px")
div(x0 + 316, 386, 'full: 16 KiB', cue=1, d=3.0, cls="lbl", style="color:var(--amber);font-size:24px", out=3, od=0.2)
# row 1 lingers
x1 = 330 + 160
div(x1, 500, '', cue=1, d=3.6, cls="grow", extra=' data-w="70" data-dur="0.6"', style="height:70px;background:var(--amber);border-radius:6px;opacity:.8")
div(x1 + 316, 506, 'linger.ms <span class="count" data-cue="1" data-d="4.2" data-from="0" data-to="5" data-dec="1" data-dur="3" data-post=" ms"></span>', cue=1, d=4.0, cls="lbl", style="font-size:26px;color:var(--amber)")
div(x1 + 316, 546, 'default 5 ms since 4.0 (was 0)', cue=2, d=0.2, cls="lbl", style="font-size:20px;color:var(--amber)")
# compression on row 0: full batch shrinks
div(x0, 370, 'zstd', cue=3, d=0.6, cls="cellk", anim="left", style="width:150px;background:var(--amber)")
div(x0 + 316, 386, 'compressed whole', cue=3, d=1.2, cls="lbl", style="color:var(--amber);font-size:22px")
codecs = "".join(f'<span class="chip" style="margin-right:12px">{c}</span>' for c in ["none", "gzip", "snappy", "lz4", "zstd"])
div(150, 760, codecs + '<span class="lbl" style="margin-left:8px">attributes bits 0–2</span>', cue=3, d=0.4, style="display:flex;align-items:center")
box(1340, 290, 460, "Sender thread", "drains batches that are full<br>or past linger.ms", col="blue", cue=4)
box(1340, 500, 460, "ProduceRequest → broker 1", "fills-0 · quotes-3", col="teal", cue=4, d=1.6, tsize=26)
box(1340, 680, 460, "ProduceRequest → broker 2", "fills-1", col="teal", cue=4, d=2.4, tsize=26)
svg_open()
path("bt-s", "M1240 405 L1336 360", "blue", 4, d=0.4, width=3)
path("bt-r1", "M1570 410 L1570 496", "teal", 4, d=1.4, width=3)
path("bt-r2", "M1800 380 C1860 380 1860 730 1804 730", "teal", 4, d=2.2, width=3)
svg_close()
pkt("bt-s", 4, "amber", d=0.8, dur=1.0)
end()

# ------------------------------------------------------------------ idem
scene("idem")
h2("The idempotent producer")
box(120, 260, 420, "producer", "InitProducerId on start", col="amber", cue=0, d=0.3)
box(1360, 260, 440, "broker 1 · leader", "fills-1", col="teal", cue=0, d=0.6)
div(120, 400, 'PID 4012 · epoch 0', cue=1, d=0.3, cls="tag", style="font-size:26px;color:var(--amber)")
svg_open()
path("id-p", "M544 300 L1354 300", "amber", 1, d=0.2, width=3)
path("id-r", "M1050 470 L1354 470", "red", 2, d=0.6, width=3)
path("id-f1", "M1802 330 C1905 330 1905 620 1170 696", "teal", 3, d=1.2, width=3)
path("id-f2", "M1802 300 C1870 300 1870 640 1640 696", "teal", 3, d=1.4, width=3)
path("id-ack", "M1356 272 C1100 205 800 205 546 272", "green", 3, d=3.6, width=3)
svg_close()
div(640, 330, 'seq 0–4', cue=1, d=1.8, cls="chip", style="color:var(--amber)")
div(900, 330, 'seq 5–9', cue=1, d=2.6, cls="chip", style="color:var(--amber)")
div(640, 392, 'sequence is per partition', cue=1, d=3.4, cls="lbl")
pkt("id-p", 1, "amber", d=2.0, dur=1.6)
div(870, 448, 'seq 5–9 (retry)', cue=2, d=0.2, cls="chip", style="color:var(--red);border-color:var(--red)")
pkt("id-r", 2, "red", d=0.9, dur=1.2, loop=False)
div(1360, 372, 'has 0–4, 5–9<br>keeps last 5 batches per producer', cue=1, d=4.0, cls="lbl", style="font-size:19px;line-height:1.3")
div(1360, 452, '✕ duplicate · discard, ack again', cue=2, d=2.0, cls="tag", style="color:var(--red);font-size:22px")
box(1000, 700, 340, "broker 2", "follower · in sync", col="teal", cue=3, d=0.6, tsize=28)
box(1460, 700, 340, "broker 3", "follower · in sync", col="teal", cue=3, d=0.9, tsize=28)
div(120, 640, '<span class="c-green">acks=all</span>: answer only when every<br>in-sync replica has the batch', cue=3, d=0.4, cls="body", style="width:760px")
div(120, 760, 'min.insync.replicas sets the floor', cue=3, d=2.2, cls="lbl")
pkt("id-f1", 3, "teal", d=1.8, dur=1.0)
pkt("id-f2", 3, "teal", d=2.0, dur=1.0)
pkt("id-ack", 3, "green", d=4.4, dur=1.3)
div(1020, 184, 'ack', cue=3, d=4.2, cls="lbl", style="color:var(--green)")
end()

# ------------------------------------------------------------------ format
scene("format")
h2("RecordBatch v2 · 61-byte header")
SC = 50
def brow(x, y, flds, cue, offs0):
    cells = []
    for i, (n, sz, c) in enumerate(flds):
        cells.append(f'<div style="width:{sz*SC}px;background:{c};flex-direction:column;display:flex;justify-content:center;align-items:center" data-cue="{cue}" data-d="{0.32*i:.2f}" data-anim="fade">'
                     f'<span>{n}</span><span style="font-size:15px;opacity:.75">{sz} B</span></div>')
    div(x, y, "".join(cells), cls="bytes")
    o = offs0; marks = [o]
    for n, sz, c in flds: o += sz; marks.append(o)
    m = "".join(f'<span style="position:absolute;left:{(v-offs0)*SC}px;transform:translateX(-50%)">{v}</span>' for v in marks)
    div(x, y - 34, m, cue=cue, d=0.2, cls="lbl", style="width:1700px;height:30px;font-size:17px")
TL, AM, MU = "#3fd0dc", "#ffb347", "#9fb4c2"
r1 = [("baseOffset", 8, TL), ("batchLength", 4, MU), ("leaderEpoch", 4, "#a98bff"), ("2", 1, MU), ("crc", 4, "#ff8fc8"), ("attr", 2, MU), ("lastOffsetΔ", 4, TL)]
r2 = [("baseTimestamp", 8, "#4fd18b"), ("maxTimestamp", 8, "#4fd18b"), ("producerId", 8, AM), ("epoch", 2, AM), ("baseSequence", 4, AM), ("records", 4, MU)]
brow(110, 262, r1, 1, 0)
div(110 + 16 * SC - 6, 342, 'magic', cue=1, d=1.0, cls="lbl", style="font-size:17px")
brow(110, 452, r2, 2, 27)
div(110, 560, 'crc: CRC-32C over attributes → end · the leader epoch sits outside it, so the broker can stamp it', cue=1, d=3.4, cls="lbl", style="font-size:21px")
div(110, 598, 'attributes: bits 0–2 codec · 3 timestamp type · 4 transactional · 5 control batch', cue=2, d=2.5, cls="lbl", style="font-size:21px")
div(110, 660, 'RECORD · ZIGZAG VARINTS · A FILL KEYED "FIRM01" · NOT TO SCALE', cue=3, cls="lbl")
rec = [("len", 110, "2 B"), ("attr", 90, "1"), ("tsΔ", 90, "1"), ("offΔ", 90, "1"), ("keyLen", 90, "1"), ("FIRM01", 200, "6"), ("valLen", 90, "1"), ("value · execution report", 700, "57"), ("hdrs", 90, "1")]
cells = []
for i, (n, w, s) in enumerate(rec):
    bg = AM if n == "FIRM01" else ("#7fb2ff" if n.startswith("value") else "#c6d3db")
    cells.append(f'<div style="width:{w}px;background:{bg};flex-direction:column;display:flex;justify-content:center;align-items:center" data-cue="3" data-d="{0.25+0.2*i:.2f}" data-anim="fade"><span>{n}</span><span style="font-size:15px;opacity:.75">{s}{"" if s.endswith("B") else " B"}</span></div>')
div(110, 700, "".join(cells), cls="bytes")
div(110, 800, '71 bytes on disk = 57 value + 6 key + 8 framing · deltas stay small, so most varints take 1 byte', cue=3, d=2.4, cls="tag", style="font-size:22px;color:var(--teal)")
end()

# ------------------------------------------------------------------ broker
scene("broker")
h2("The broker: page cache, then segments")
box(120, 240, 640, "broker 1 · leader · fills-1", "append to the active segment", col="teal", cue=0, d=0.2)
box(120, 430, 640, "page cache (RAM)", "write() returns here", col="blue", cue=1)
box(120, 630, 640, "disk", "the kernel writes back later", col="", cue=2, d=0.3)
div(120, 790, '✕ no fsync per write · log.flush.* unset', cue=2, d=1.6, cls="tag", style="color:var(--red);font-size:24px")
svg_open()
path("bk-a", "M440 352 L440 424", "teal", 1, d=0.2, width=3)
path("bk-b", "M440 542 L440 624", "muted", 2, d=0.6, width=3, dash=True)
svg_close()
pkt("bk-a", 1, "teal", d=0.5, dur=0.8)
div(880, 220, '/var/lib/kafka/fills-1/', cue=3, cls="lbl", style="color:var(--teal);font-size:24px")
segs = [("00000000000000000000", 0.2), ("00000000000003813306", 0.5), ("00000000000007642980", 0.8)]
for i, (nm, dd) in enumerate(segs):
    x = 880 + i * 310
    if i < 2:
        div(x, 262, 'closed', cue=3, d=dd, cls="cellk", style="width:300px;background:#2a8f9b")
    else:
        div(x, 262, '', cue=3, d=dd, style="width:300px;height:64px;border:2px dashed var(--teal);border-radius:6px")
        div(x, 262, '', cue=3, d=dd, cls="grow", extra=' data-w="180" data-dur="10"', style="height:64px;background:var(--teal);border-radius:6px")
        div(x + 186, 280, 'active', cue=3, d=dd, cls="lbl", style="color:var(--teal);font-size:19px")
    div(x, 334, nm, cue=3, d=dd + 0.2, cls="lbl", style="font-size:17px")
fc = [(".log", "record batches<br>appended in order", 0.2), (".index", "offset → position<br>8-byte entries<br>one per 4 KiB", 2.4), (".timeindex", "time → offset<br>12-byte entries<br>sparse, like .index", 5.0)]
for i, (n, s, dd) in enumerate(fc):
    box(880 + i * 310, 400, 300, n, s, col="teal", cue=4, d=dd, tsize=30, h=200)
div(880, 650, 'files are named by the segment\'s first offset', cue=3, d=1.0, cls="lbl")
div(880, 710, 'log.segment.bytes = 1 GiB → roll to a new segment', cue=5, d=0.1, cls="tag", style="font-size:24px;color:var(--amber)")
div(880, 770, 'only the active segment is written; closed ones are read-only', cue=5, d=1.0, cls="lbl")
end()

# ------------------------------------------------------------------ replicate
scene("replicate")
h2("Replication and the high watermark")
rws = [("broker 1 · leader", 10, "teal"), ("broker 2", 10, "muted"), ("broker 3", 8, "muted")]
CX, CW = 420, 92
for r, (n, cnt, c) in enumerate(rws):
    y = 250 + r * 112
    inner = "".join(f'<div class="cellk" style="position:absolute;left:{CX + i*CW}px;top:{y}px;width:86px;background:#3fd0dc">{i}</div>' for i in range(cnt))
    inner += f'<div class="lbl" style="position:absolute;left:120px;top:{y+20}px;color:var(--{c});font-size:22px">{n}</div>'
    kw = dict(dim=4) if r == 0 else {}
    div(0, 0, inner, cue=0, d=0.3 + 0.4 * r, style="width:1920px;height:1080px", anim="fade", **kw)
svg_open()
path("rp-a", "M1340 285 C1395 285 1395 395 1340 395", "teal", 0, d=1.2, width=3)
path("rp-b", "M1340 285 C1410 285 1410 507 1160 507", "teal", 0, d=1.4, width=3)
svg_close()
pkt("rp-a", 0, "teal", d=1.6, dur=1.0)
pkt("rp-b", 0, "teal", d=1.8, dur=1.2, phase=0.4)
div(1430, 240, '<div class="t">ISR = {1, 2, 3}</div><div class="s">caught up within<br>replica.lag.time.max.ms<br>30 s by default</div>', cue=1, d=0.3, cls="box green", style="width:370px")
hx = CX + 8 * CW - 4
div(hx, 232, '', cue=2, d=0.3, anim="fade", style="width:5px;height:330px;background:var(--green);border-radius:3px;box-shadow:0 0 16px var(--green)")
div(hx - 120, 572, 'high watermark = 8', cue=2, d=0.5, cls="tag", style="color:var(--green);font-size:24px")
box(120, 660, 520, "consumer", "reads offsets 0–7 only", col="green", cue=2, d=2.0, tsize=28)
for r in range(2):
    div(CX + 8 * CW - 2, 246 + r * 112, '', cue=3, d=0.1, anim="fade", style="width:182px;height:78px;border-radius:8px;background:repeating-linear-gradient(45deg,rgba(255,179,71,.55) 0 10px,rgba(255,179,71,.15) 10px 20px);border:2px solid var(--amber)")
div(hx + 8, 200, 'not committed · invisible to consumers', cue=3, d=0.2, cls="lbl", style="color:var(--amber)")
div(1430, 430, '<div class="t">leader epoch 7 → 8</div><div class="s">broker 1 fails,<br>broker 2 leads;<br>a stale replica truncates<br>to where epoch 7 ended</div>', cue=4, d=0.3, cls="box violet", style="width:370px")
box(700, 660, 680, "KRaft controller quorum", "Raft log of cluster metadata<br>elects leaders · no ZooKeeper since 4.0", col="violet", cue=5, d=0.3)
end()

# ------------------------------------------------------------------ group
scene("group")
h2("Consumer groups")
for i in range(6):
    box(120, 250 + i * 95, 240, f"fills-{i}", col="teal", cue=0, d=0.3 + 0.1 * i, tsize=26, style="padding:10px 20px")
div(620, 222, 'group: risk', cue=0, d=1.6, cls="lbl", style="color:var(--red)")
box(620, 260, 320, "risk-1", "fills-0, 1, 2", col="red", cue=1, d=0.2)
box(620, 470, 320, "risk-2", "fills-3, 4, 5", col="red", cue=1, d=0.6)
div(620, 662, 'group: audit', cue=1, d=2.4, cls="lbl", style="color:var(--green)")
box(620, 700, 320, "audit-1", "all six", col="green", cue=1, d=2.6)
svg_open()
for i in range(6):
    y = 290 + i * 95
    ty = 315 if i < 3 else 525
    path(f"gr-r{i}", f"M364 {y} C490 {y} 490 {ty} 616 {ty}", "red", 1, d=0.4 + 0.15 * i, width=3)
for i in range(6):
    y = 290 + i * 95
    path(f"gr-a{i}", f"M364 {y} C490 {y} 490 750 616 750", "green", 1, d=3.0 + 0.1 * i, width=2)
svg_close()
code1 = ('<span class="k">FetchRequest</span>       → broker 1\n  max_wait_ms  <span class="r">500</span>\n  min_bytes    <span class="r">1</span>\n  fills-0  fetch_offset <span class="r">1043</span>')
div(1040, 260, code1, cue=2, d=0.2, cls="code", style="width:760px;font-size:25px")
code2 = ('<span class="k">FetchResponse</span>\n  high_watermark  <span class="r">1187</span>\n  records  <span class="g">batches, as stored</span>')
div(1040, 520, code2, cue=3, d=2.0, cls="code", style="width:760px;font-size:25px")
div(1040, 720, 'sendfile(): page cache → socket,<br>no copy through user space (without TLS)', cue=3, d=5.0, cls="lbl", style="font-size:22px;line-height:1.4")
end()

# ------------------------------------------------------------------ commit
scene("commit")
h2("Offsets, rebalances and lag")
offs = list(range(1039, 1048))
for i, o in enumerate(offs):
    div(120 + i * 98, 240, str(o), cue=0, d=0.1 + 0.04 * i, cls="cellk", style=f"width:92px;background:{'#3fd0dc' if o < 1043 else '#2a8f9b'};font-size:18px")
div(1010, 252, '…', cue=0, d=0.5, cls="h3")
for i, o in enumerate([1185, 1186]):
    div(1070 + i * 98, 240, str(o), cue=0, d=0.5, cls="cellk", style="width:92px;background:#2a8f9b;font-size:18px")
div(1264, 224, '', cue=0, d=0.6, anim="fade", style="width:5px;height:100px;background:var(--green);border-radius:3px")
div(1186, 330, 'HW 1187', cue=0, d=0.6, cls="lbl", style="color:var(--green)")
cx = 120 + 4 * 98 - 4
div(cx, 224, '', cue=0, d=0.8, anim="fade", style="width:5px;height:100px;background:var(--red);border-radius:3px")
div(cx - 90, 330, 'committed 1043', cue=0, d=0.8, cls="lbl", style="color:var(--red)")
box(1380, 200, 420, "__consumer_offsets", "key&nbsp;&nbsp; risk · fills · 0<br>value offset 1043<br>50 partitions by default", col="violet", cue=0, d=2.4)
svg_open()
path("cm-c", "M520 362 C900 440 1250 420 1376 330", "violet", 0, d=2.8, width=3)
path("cm-m", "M480 520 L616 520", "red", 1, d=2.0, width=3)
svg_close()
pkt("cm-c", 0, "violet", d=3.4, dur=1.2)
box(120, 470, 360, "risk-1", "fills-0, 1, 2", col="red", cue=1, d=0.0, dim=1.3)
div(250, 455, '✕', cue=1, d=1.0, style="font:800 110px var(--display);color:var(--red)")
box(620, 470, 360, "risk-2", "fills-3, 4, 5", col="red", cue=1, d=0.2)
div(620, 600, '+ fills-0, 1, 2', cue=1, d=2.4, cls="tag", anim="left", style="color:var(--red);font-size:24px")
pkt("cm-m", 1, "red", d=2.0, dur=0.9, loop=False)
div(1060, 480, 'group coordinator: JoinGroup → SyncGroup<br>(classic protocol, the client default)<br>or server-side assignment (KIP-848)', cue=1, d=2.8, cls="lbl", style="font-size:21px;line-height:1.45")
div(620, 660, 'risk-2 fetches fills-0 from 1043', cue=2, d=0.3, cls="lbl", style="color:var(--red)")
div(120, 760, 'lag = 1187 − 1043 = <span class="count c-red" data-cue="3" data-d="1.0" data-from="0" data-to="144" data-dur="1.4"></span>', cue=3, cls="h3", style="font-size:48px;font-family:var(--mono)")
div(1000, 772, 'alarm when it keeps growing', cue=4, d=0.2, cls="tag", style="color:var(--red);font-size:26px", hl=4, hld=0.4)
end()

# ------------------------------------------------------------------ delivery
scene("delivery")
h2("Ordering, delivery and retention", top=105)
PH = 'border:2px solid var(--line);border-radius:16px;background:rgba(19,33,43,.75)'
div(120, 190, '', cue=0, style=f"width:820px;height:330px;{PH}")
div(146, 206, 'ORDERING · PER PARTITION', cue=0, d=0.2, cls="lbl", style="color:var(--teal)")
for r, (p, k, c, n) in enumerate([("fills-0", "FIRM01", "amber", 4), ("fills-1", "FIRM02", "blue", 3)]):
    y = 260 + r * 90
    div(146, y + 14, p, cue=0, d=0.4 + 0.3 * r, cls="lbl", style="font-size:22px")
    for i in range(n):
        div(290 + i * 150, y, f"{k} #{i+1}", cue=0, d=0.6 + 0.25 * i + 0.3 * r, cls="chip", style=f"color:var(--{c})")
div(146, 446, 'key fills by Account · key quotes by Symbol', cue=1, d=0.4, cls="lbl", style="color:var(--amber)")
div(146, 478, '✕ no order between partitions', cue=1, d=2.5, cls="lbl")
div(1000, 190, '', cue=2, style=f"width:800px;height:330px;{PH}")
div(1026, 206, 'AT-LEAST-ONCE', cue=2, d=0.2, cls="lbl", style="color:var(--green)")
for i, (o, st, dd) in enumerate([("1043", "✓", 0.4), ("1044", "✓", 0.8), ("1045", "✕ crash", 1.4)]):
    col = "red" if "crash" in st else "green"
    div(1026 + i * 190, 262, f'{o} <span class="c-{col}">{st}</span>', cue=2, d=dd, cls="chip")
div(1026, 340, 'restart from committed 1043:', cue=2, d=2.4, cls="lbl")
for i, o in enumerate(["1043", "1044", "1045"]):
    div(1026 + i * 190, 380, o, cue=2, d=2.8 + 0.3 * i, cls="chip", style="color:var(--amber);border-color:var(--amber)" if i < 2 else "")
div(1026, 452, 'dedupe on Match Number (bytes 40–47)', cue=3, d=1.2, cls="lbl", style="color:var(--amber)")
div(120, 560, '', cue=4, style=f"width:820px;height:340px;{PH}")
div(146, 576, 'EXACTLY-ONCE · TRANSACTIONS', cue=4, d=0.2, cls="lbl", style="color:var(--violet)")
tx = ["transactional.id → epoch fences old instances", "outputs + consumer offsets in one transaction", "COMMIT / ABORT control markers in the log", "read_committed: read up to the last stable offset"]
for i, t in enumerate(tx):
    div(146, 626 + i * 62, t, cue=4, d=0.6 + 0.6 * i, cls="body", style="font:500 24px var(--mono);color:#d4e0e7")
div(1000, 560, '', cue=5, style=f"width:800px;height:340px;{PH}")
div(1026, 576, 'RETENTION', cue=5, d=0.2, cls="lbl", style="color:var(--amber)")
for i in range(3):
    div(1026 + i * 130, 620, 'seg', cue=5, d=0.4 + 0.15 * i, cls="cellk", style="width:120px;height:52px;background:#2a8f9b;font-size:18px", **({"dim": 5.5} if i == 0 else {}))
div(1046, 606, '✕', cue=5, d=1.6, style="font:800 72px var(--display);color:var(--red)")
div(1430, 632, 'delete after 7 days', cue=5, d=1.4, cls="lbl")
div(1026, 712, 'COMPACTION · LATEST PER KEY', cue=6, cls="lbl", style="color:var(--amber)")
kv = [("FIRM01 +100", True), ("FIRM02 −50", True), ("FIRM01 +300", False), ("FIRM02 +20", False)]
for i, (t, old) in enumerate(kv):
    kw = {"dim": 6.6} if old else {}
    div(1026 + i * 190, 760, t, cue=6, d=0.3 + 0.25 * i, cls="chip", style="font-size:20px", **kw)
div(1026, 830, 'older values per key are removed', cue=6, d=2.4, cls="lbl")
end()

# ------------------------------------------------------------------ latency
scene("latency")
h2("Why Kafka stays off the hot path")
stg = ["linger ≤ 5 ms", "network hop", "page cache append", "replicate to ISR", "consumer fetch"]
row = []
for i, s_ in enumerate(stg):
    row.append(f'<span class="chip" style="font-size:24px;color:var(--teal)" data-cue="1" data-d="{0.2 + 1.1 * i:.1f}">{s_}</span>')
    if i < 4: row.append(f'<span class="arr" data-cue="1" data-d="{0.7 + 1.1 * i:.1f}" data-anim="fade">→</span>')
div(120, 230, "".join(row), cls="pipe", style="gap:18px")
X0, DEC = 160, 1600 / 6
ticks = ["100 ns", "1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms"]
div(X0, 420, '', cue=2, d=0.0, anim="fade", style="width:1600px;height:4px;background:var(--line)")
for i, t in enumerate(ticks):
    x = X0 + i * DEC
    div(x - 2, 410, '', cue=2, d=0.1 * i, anim="fade", style="width:4px;height:24px;background:var(--muted)")
    div(x - 50, 446, t, cue=2, d=0.1 * i, cls="lbl", style="width:100px;text-align:center")
kx = X0 + 4 * DEC
div(kx, 360, '', cue=2, d=0.8, cls="grow", extra=' data-w="%d" data-dur="1.2"' % int(1.9 * DEC), style="height:44px;border-radius:8px;background:linear-gradient(90deg,var(--teal),rgba(63,208,220,.15))")
div(kx, 312, 'Kafka end to end: typically milliseconds', cue=2, d=1.4, cls="lbl", style="color:var(--teal);font-size:24px")
ax = X0 + 0.875 * DEC
div(ax - 3, 350, '', cue=3, d=0.2, anim="fade", style="width:6px;height:70px;background:var(--amber);border-radius:3px;box-shadow:0 0 16px var(--amber)")
div(ax - 40, 500, 'lab Aeron IPC round trip:<br>&lt; 1 µs median, shared VM', cue=3, d=0.5, cls="lbl", style="color:var(--amber);font-size:22px;line-height:1.4")
div(120, 650, 'HOT PATH', cue=4, cls="lbl", style="color:var(--blue)")
hp = ["simex", "itch-fh", "trader"]
row = []
for i, s_ in enumerate(hp):
    row.append(f'<span class="chip" style="color:var(--blue);border-color:var(--blue)" data-cue="4" data-d="{0.2 + 0.15 * i:.2f}">{s_}</span>')
    if i < 2: row.append(f'<span class="arr" data-cue="4" data-d="{0.3 + 0.15 * i:.2f}" data-anim="fade">→</span>')
div(400, 636, "".join(row), cls="pipe", style="gap:14px")
div(120, 760, 'AFTER THE TRADE', cue=4, d=1.0, cls="lbl", style="color:var(--amber)")
at = [("pump", "amber"), ("Kafka", "teal"), ("risk", "red"), ("research", "violet"), ("audit", "green"), ("TCA", "pink")]
row = []
for i, (s_, c) in enumerate(at):
    row.append(f'<span class="chip" style="color:var(--{c});border-color:var(--{c})" data-cue="4" data-d="{1.2 + 0.2 * i:.1f}">{s_}</span>')
    if i < 2: row.append(f'<span class="arr" data-cue="4" data-d="{1.3 + 0.2 * i:.1f}" data-anim="fade">→</span>')
div(400, 746, "".join(row), cls="pipe", style="gap:14px")
div(400, 830, 'durable · replayable · shared', cue=4, d=2.6, cls="lbl", style="font-size:24px;color:var(--teal)")
end()

open(f"{OUT}/scenes.html", "w").write("\n".join(H) + "\n")

CSS = """
.chip{display:inline-block;padding:8px 16px;border-radius:10px;font:600 22px var(--mono);background:var(--panel);border:2px solid var(--line);white-space:nowrap}
.chip.on{border-color:var(--amber);color:var(--amber);box-shadow:0 0 18px rgba(255,179,71,.35)}
.pipe{display:flex;align-items:center;gap:10px}
.pipe .arr{font:600 24px var(--mono);color:var(--muted)}
.cellk{position:absolute;height:70px;border-radius:6px;display:grid;place-items:center;font:700 24px var(--mono);color:#06141a}
.tag{white-space:nowrap}
.lbl{white-space:nowrap}
.box .s{line-height:1.35}
.bytes > div span{display:block}
"""
open(f"{OUT}/style.css", "w").write(CSS)
print("ok", len(H))
