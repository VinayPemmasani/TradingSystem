# Generates /mnt/project-files/videos/explainers/fpga-book/scenes.html
OUT = "/mnt/project-files/videos/explainers/fpga-book/scenes.html"
H = []
def a(s): H.append(s)

def attrs(cue=None, d=None, anim=None, out=None, hl=None, hlend=None, dim=None, extra=""):
    s = ""
    if cue is not None: s += f' data-cue="{cue}"'
    if d: s += f' data-d="{d}"'
    if anim: s += f' data-anim="{anim}"'
    if out is not None: s += f' data-out="{out}"'
    if hl is not None: s += f' data-hl="{hl}"'
    if hlend is not None: s += f' data-hlend="{hlend}"'
    if dim is not None: s += f' data-dim="{dim}"'
    return s + extra

def div(cls, x, y, w=None, h=None, inner="", style="", **k):
    st = f"left:{x}px;top:{y}px;"
    if w is not None: st += f"width:{w}px;"
    if h is not None: st += f"height:{h}px;"
    a(f'<div class="{cls}" style="{st}{style}"{attrs(**k)}>{inner}</div>')

# byte region in the frame (single Add Order at byte 64)
def region(b):
    if b < 14: return "--eth"
    if b < 34: return "--ip"
    if b < 42: return "--udp"
    if b < 62: return "--mold"
    if b < 64: return "--len"
    if b < 100: return "--itch"
    return None

# Add Order fields: (name, msg offset, length, colour var)
FIELDS = [("type", 0, 1, "--f-type"), ("locate", 1, 2, "--f-loc"), ("tracking", 3, 2, "--f-trk"),
          ("timestamp", 5, 6, "--f-ts"), ("order ref", 11, 8, "--f-ref"), ("side", 19, 1, "--f-side"),
          ("shares", 20, 4, "--f-sh"), ("stock", 24, 8, "--f-stk"), ("price", 32, 4, "--f-px")]
BASE = 64

def segs_of(off, ln):
    """split frame bytes [BASE+off, BASE+off+ln) into (word, lane0, nlanes)"""
    out = []; b = BASE + off; e = b + ln
    while b < e:
        w, l = divmod(b, 8); n = min(8 - l, e - b); out.append((w, l, n)); b += n
    return out

def svg_open(): a('<svg class="full">')
def svg_close(): a('</svg>')
def path(pid, d, color, cue, dur=0.9, d_=None, marker=None, width=4, dash=None, out=None):
    m = f' marker-end="url(#{marker})"' if marker else ''
    ex = f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<path id="{pid}" class="draw" d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{m}{attrs(cue=cue, d=d_, out=out)} data-dur="{dur}"/>')

# ---------------------------------------------------------------- 1 hook
a('<div class="scene" id="s-hook">')
div("eyebrow", 140, 250, inner="TRADING LAB · HARDWARE", cue=0)
div("h1", 132, 300, 900, inner="FPGA<br>order book", cue=0, d=0.2)
div("sub", 140, 610, 860, inner="Decode ITCH and build the book <span class='c-teal'>while the packet is still arriving</span>.", cue=1)
div("lbl", 140, 760, 860, inner="one Add Order · clock by clock · byte by byte", cue=2)
CW, CH, X0, Y0 = 78, 46, 1120, 175
for w in range(13):
    div("rl", X0 - 110, Y0 + w * 52 + 8, 90, inner=f"clk {w}", cue=0.6, d=round(w * 0.14, 2), anim="fade", style="font-size:18px")
    for l in range(8):
        b = w * 8 + l; r = region(b)
        bg = f"var({r})" if r else "#15242e"
        div("fc", X0 + l * (CW + 6), Y0 + w * 52, CW, CH, "", style=f"background:{bg};" + ("" if r else "border-color:#243a47"),
            cue=0.6, d=round(w * 0.14, 2), anim="fade")
div("", X0 - 8, Y0 + 8 * 52 - 6, 8 * (CW + 6) + 10, 5 * 52 + 6, "", style="border:3px solid var(--f-ref);border-radius:10px;",
    cue=2, anim="fade", hl=2)
div("tag", X0 + 8 * (CW + 6) - 210, Y0 + 13 * 52 + 6, inner="Add Order: words 8–12", style="color:var(--f-ref)", cue=2, d=0.3)
a('</div>')

# ---------------------------------------------------------------- 2 why
a('<div class="scene" id="s-why">')
div("h2", 120, 110, inner="Software waits. Hardware streams.", cue=0)
div("lbl", 120, 230, inner="SOFTWARE · itch-fh on one core", style="color:var(--blue)", cue=0)
sw = [("socket recv", "UDP packet"), ("libs/mold", "sequence check"), ("itch dispatch", "decode"), ("OrderMap", "find(ref)"), ("OrderBook", "level update")]
for i, (t, s) in enumerate(sw):
    cue = 0 if i < 2 else 1
    div("stage blue", 120 + i * 345, 280, 280, 120, f"{t}<small>{s}</small>", cue=cue, d=round(0.3 * i if i < 2 else 0.4 * (i - 2), 2))
svg_open()
path("why-sw", "M 400 340 L 465 340 M 745 340 L 810 340 M 1090 340 L 1155 340 M 1435 340 L 1500 340", "#6aa8ff", 1, dur=1.2, marker=None, width=3)
path("why-swd", "M 260 420 L 1640 420", "none", 2, width=1)
path("why-hw", "M 260 770 L 1640 770", "#3fd0dc", 3, dur=1.0, width=3, dash="2 0")
svg_close()
a('<div class="pkt" data-path="why-swd" data-cue="2" data-dur="3.2" style="background:var(--blue);box-shadow:0 0 14px var(--blue)"></div>')
div("note", 120, 450, 1200, inner="one message at a time: each step starts when the previous one returns", cue=2, d=0.2)
div("lbl", 120, 590, inner="FPGA · a pipeline on the byte stream", style="color:var(--teal)", cue=3)
hw = [("parse", "headers + fields"), ("filter", "by locate"), ("order table", "RAM lookup"), ("levels", "top-N book"), ("out", "DMA / order entry")]
for i, (t, s) in enumerate(hw):
    div("stage teal", 120 + i * 345, 640, 280, 110, f"{t}<small>{s}</small>", cue=3, d=round(0.15 * i, 2))
for k in range(5):
    a(f'<div class="pkt" data-path="why-hw" data-cue="3" data-d="0.8" data-dur="2.4" data-loop="1" data-phase="{k*0.2}"></div>')
div("note", 120, 830, 1300, inner="every stage busy every clock, on a different message", cue=3, d=1.0, style="color:var(--teal)")
a('</div>')

# ---------------------------------------------------------------- 3 bus
a('<div class="scene" id="s-bus">')
div("h2", 120, 110, inner="The bus: 64 bits every clock", cue=0)
div("stage", 120, 240, 300, 110, "fiber<small>SFP+</small>", cue=3)
div("stage violet", 500, 240, 380, 110, "PCS · 10GBASE-R<small>64b/66b · 10.3125 GBd</small>", cue=3, d=0.3)
div("stage blue", 960, 240, 300, 110, "10G MAC<small>strips preamble</small>", cue=0)
div("stage teal", 1420, 240, 380, 110, "your logic<small>parser pipeline</small>", cue=0, d=0.3)
svg_open()
path("bus-a1", "M 420 295 L 492 295", "#8ea3b1", 3, marker="ah", width=3)
path("bus-a2", "M 880 295 L 952 295", "#8ea3b1", 3, d_=0.3, marker="ah", width=3)
path("bus-a3", "M 1260 295 L 1410 295", "#3fd0dc", 0, d_=0.5, marker="ah-teal", width=8)
# clock waveform: period 140 px
P0, PW, YT, YB = 300, 140, 450, 510
d = f"M {P0} {YB}"
for i in range(10):
    x = P0 + i * PW
    d += f" L {x} {YT} L {x+PW/2} {YT} L {x+PW/2} {YB} L {x+PW} {YB}"
path("bus-clk", d, "#ffb347", 1, dur=2.0, width=3)
path("bus-per", f"M {P0} 425 L {P0+PW} 425", "#ffb347", 1, d_=1.0, width=2)
svg_close()
div("lbl", 1290, 345, 220, inner="64-bit word", style="color:var(--teal)", cue=0, d=0.6)
div("lbl", 120, 465, 160, inner="clk", style="color:var(--amber);text-align:right", cue=1)
div("tag", P0 + 14, 385, inner="6.4 ns", style="color:var(--amber)", cue=1, d=1.0)
for i in range(10):
    div("fc", P0 + i * PW + 6, 530, PW - 12, 44, f"w{i}", style="background:var(--teal)", cue=1, d=round(0.2 * i, 2), anim="fade")
div("big", 300, 640, 1400, inner="8 B × <span class='c-amber'>156.25 MHz</span> = <span class='c-teal'>10 Gb/s</span>", cue=2)
div("lbl", 300, 715, 1400, inner="on the fiber: 10 Gb/s × 66/64 = 10.3125 GBd", cue=3, d=0.4)
for l in range(8):
    div("fc", 300 + l * 150, 790, 140, 60, f"lane {l}<small>bits {l*8+7}:{l*8}</small>",
        style="background:" + ("var(--teal)" if l == 0 else "#7fdbe3"), cue=4, d=round(0.06 * l, 2), anim="fade")
div("tag", 300, 865, inner="← earliest byte on the wire", style="color:var(--teal)", cue=4, d=0.6)
a('</div>')

# ---------------------------------------------------------------- 4 headers
a('<div class="scene" id="s-headers">')
div("h2", 120, 110, inner="Counting bytes into words", cue=0)
CW, CH, X0, Y0, RS = 92, 46, 230, 205, 52
for l in range(8):
    div("lane", X0 + l * (CW + 6), Y0 - 30, CW, inner=f"L{l}", cue=0)
for w in range(13):
    div("rl", X0 - 100, Y0 + w * RS + 10, 80, inner=f"w{w}", cue=0, style="font-size:20px")
    for l in range(8):
        b = w * 8 + l
        div("gc", X0 + l * (CW + 6), Y0 + w * RS, CW, CH, str(b) if b < 100 else "…", cue=0, anim="fade", d=round(0.03 * w, 2))
cues = {"--eth": (1, 0), "--ip": (1, 1.0), "--udp": (1, 2.0), "--mold": (2, 0), "--len": (3, 0), "--itch": (4, 0.2)}
for w in range(13):
    for l in range(8):
        b = w * 8 + l; r = region(b)
        if not r: continue
        c, dd = cues[r]
        div("fc", X0 + l * (CW + 6), Y0 + w * RS, CW, CH, str(b), style=f"background:var({r})", cue=c, d=round(dd + 0.02 * (b % 20), 2), anim="fade",
            hl=(4 if b == 64 else None))
LX = 1100
leg = [("--eth", "Ethernet", "14 B", "bytes 0–13", 1, 0), ("--ip", "IPv4, no options", "20 B", "14–33", 1, 1.0), ("--udp", "UDP", "8 B", "34–41", 1, 2.0),
       ("--mold", "MoldUDP64 header", "20 B", "42–61", 2, 0), ("--len", "message length", "2 B", "62–63", 3, 0)]
for i, (c, n, sz, rng, cu, dd) in enumerate(leg):
    div("legend", LX, 220 + i * 78, 760, inner=f"<i style='background:var({c})'></i><span style='width:330px'>{n}</span><span class='c-amber' style='width:90px'>{sz}</span><span class='c-muted'>{rng}</span>", cue=cu, d=dd)
div("lbl", LX + 42, 220 + 3 * 78 + 40, 700, inner="session 42–51 · sequence 52–59 · count 60–61", cue=2, d=0.6)
div("box teal", LX, 650, 720, inner="<div class='t'>ITCH message at byte <span class='c-teal'>64</span></div><div class='s'>64 = 8 × 8 → word 8, lane 0</div>", cue=4)
div("lbl", LX, 790, 720, inner="14 + 20 + 8 + 20 + 2 = 64 · no VLAN tag", cue=4, d=0.6)
a('</div>')

# ---------------------------------------------------------------- 5 addorder
a('<div class="scene" id="s-addorder">')
div("h2", 120, 110, inner="Where an Add Order lands", cue=0)
CW, CH, X0, Y0, RS = 116, 92, 240, 250, 112
fcue = {"type": 1, "locate": 1, "tracking": 1, "timestamp": 2, "order ref": 3, "side": 4, "shares": 4, "stock": 4.3, "price": 4.6}
for l in range(8):
    div("lane", X0 + l * (CW + 6), Y0 - 32, CW, inner=f"lane {l}", cue=0)
for i, w in enumerate(range(8, 13)):
    div("rl", X0 - 140, Y0 + i * RS + 20, 120, inner=f"w{w}<br><span style='font-size:16px'>clk {w}</span>", cue=0, style="line-height:1.2")
    for l in range(8):
        div("gc", X0 + l * (CW + 6), Y0 + i * RS, CW, CH, "", cue=0, anim="fade")
for name, off, ln, col in FIELDS:
    segs = segs_of(off, ln)
    for j, (w, l, n) in enumerate(segs):
        straddle = len(segs) > 1
        lbl = name if j == 0 else name + " ⟶" if False else (name + " (cont.)")
        if not straddle: lbl = name
        sub = f"+{off}" if j == 0 else f"+{off + (8 - segs[0][1])}"
        k = dict(cue=fcue[name], anim="fade")
        if straddle: k.update(hl=fcue[name], hlend=fcue[name] + 1)
        fs = "font-size:20px;" if n <= 1 else ""
        div("seg", X0 + l * (CW + 6), Y0 + (w - 8) * RS, n * CW + (n - 1) * 6, CH, f"{lbl if n > 1 or name in ('type','side') else lbl}<small>{sub}</small>", style=f"background:var({col});{fs}", **k)
div("seg", X0 + 4 * (CW + 6), Y0 + 4 * RS, 4 * CW + 18, CH, "next block…<small>len, next message</small>", style="background:#2a3f4c;color:#9fb3c0", cue=4.6, anim="fade")
# table
rows = [("type 'A'", "0", "64", "w8 L0"), ("locate", "1–2", "65–66", "w8 L1–2"), ("tracking", "3–4", "67–68", "w8 L3–4"),
        ("timestamp", "5–10", "69–74", "w8 L5 → w9 L2"), ("order ref", "11–18", "75–82", "w9 L3 → w10 L2"), ("side", "19", "83", "w10 L3"),
        ("shares", "20–23", "84–87", "w10 L4–7"), ("stock", "24–31", "88–95", "w11 L0–7"), ("price", "32–35", "96–99", "w12 L0–3")]
rc = [1, 1, 1, 2, 3, 4, 4, 4.3, 4.6]
a('<table class="t" style="left:1270px;top:215px;width:600px;font-size:22px">')
a('<tr data-cue="0"><th>field</th><th>msg</th><th>frame</th><th>word · lane</th></tr>')
for (f, m, fr, wl), c, (_, _, _, col) in zip(rows, rc, FIELDS):
    a(f'<tr data-cue="{c}" data-anim="fade"><td style="color:var({col})">{f}</td><td class="n">{m}</td><td>{fr}</td><td>{wl}</td></tr>')
a('</table>')
div("lbl", 1270, 800, 600, inner="docs/specs/itch50-layout.md · big-endian", cue=0, d=0.5)
a('</div>')

# ---------------------------------------------------------------- 6 stitch
a('<div class="scene" id="s-stitch">')
div("h2", 120, 110, inner="Stitching a field across two clocks", cue=0)
CW, X0 = 106, 300
def strip(y, cells, cue, out=None, d=None):
    for l, (txt, col) in enumerate(cells):
        div("fc", X0 + l * (CW + 6), y, CW, 70, txt, style=f"background:var({col});font-size:19px", cue=cue, d=d, anim="fade", out=out)
w9 = [("ts", "--f-ts")] * 3 + [(f"ref[{i}]", "--f-ref") for i in range(5)]
w10 = [(f"ref[{i}]", "--f-ref") for i in range(5, 8)] + [("side", "--f-side")] + [("shares", "--f-sh")] * 4
div("rl", 90, 250, 190, inner="clk 9<br><span style='font-size:17px'>word 9</span>", cue=0, out=3)
strip(240, w9, 0, out=3)
div("rl", 90, 420, 190, inner="clk 10<br><span style='font-size:17px'>word 10</span>", cue=0.5, out=3)
strip(410, w10, 0.5, out=3)
div("", X0 + 3 * (CW + 6) - 6, 234, 5 * (CW + 6) + 6, 82, "", style="border:3px solid var(--amber);border-radius:10px", cue=1, anim="fade", out=3)
div("", X0 - 6, 404, 3 * (CW + 6) + 6, 82, "", style="border:3px solid var(--amber);border-radius:10px", cue=2, anim="fade", out=3)
div("lbl", 1250, 210, 400, inner="hold register (5 bytes)", style="color:var(--amber)", cue=1, out=3)
for i in range(5):
    div("fc", 1250 + i * 112, 245, 106, 70, f"ref[{i}]", style="background:var(--f-ref);font-size:19px", cue=1, d=0.5 + 0.08 * i, anim="fade", out=3)
svg_open()
path("st-a1", "M 1196 275 L 1240 275", "#ffb347", 1, d_=0.3, marker="ah-amber", width=3, out=3)
path("st-a2", "M 1530 320 L 1530 600 L 1000 600 L 1000 640", "#ffb347", 2, marker="ah-amber", width=3, out=3)
path("st-a3", "M 460 490 L 460 640", "#ffb347", 2, d_=0.2, marker="ah-amber", width=3, out=3)
svg_close()
for i in range(8):
    div("fc", X0 + i * (CW + 6), 655, CW, 70, f"ref[{i}]", style="background:var(--f-ref);font-size:19px", cue=2, d=0.6 + 0.05 * i, anim="fade", out=3)
div("tag", X0 + 8 * (CW + 6) + 20, 670, inner="order ref valid · clk 10", style="color:var(--green)", cue=2, d=1.0, out=3)
div("code", X0, 760, inner="ref = {w9.L3, w9.L4, w9.L5, w9.L6, w9.L7, w10.L0, w10.L1, w10.L2}  <span class='c'>// L3 is the high byte</span>",
    style="font-size:22px", cue=2, d=1.2, out=3)
# word 12 realign
div("rl", 90, 260, 190, inner="clk 12<br><span style='font-size:17px'>word 12</span>", cue=3, d=0.3)
w12 = [("price", "--f-px")] * 4 + [("len", "--len")] * 2 + [("type", "--f-type"), ("locate", "--f-loc")]
strip(250, w12, 3, d=0.3)
div("", X0 + 6 * (CW + 6) - 6, 244, 2 * (CW + 6) + 6, 82, "", style="border:3px solid var(--amber);border-radius:10px", cue=3, d=0.8, anim="fade")
div("lbl", X0 + 6 * (CW + 6) - 10, 340, 400, inner="next message: byte 102 = lane 6", style="color:var(--amber)", cue=3, d=0.8)
div("stage amber", X0, 420, 2 * (CW + 6) * 4 - 6 - 0, 96, "byte shifter · rotate by 6 lanes<small>words 12 + 13 → message-aligned word</small>", cue=3, d=1.2)
al = [("type", "--f-type"), ("locate", "--f-loc"), ("locate", "--f-loc"), ("tracking", "--f-trk"), ("tracking", "--f-trk"), ("ts", "--f-ts"), ("ts", "--f-ts"), ("ts", "--f-ts")]
strip(580, al, 3, d=1.8)
div("lbl", X0, 670, 900, inner="every later message decodes at fixed lanes, like the first", cue=3, d=2.0)
a('</div>')

# ---------------------------------------------------------------- 7 filter
a('<div class="scene" id="s-filter">')
div("h2", 120, 110, inner="Filter by stock locate", cue=0)
CW, X0 = 106, 200
w8 = [("type", "--f-type"), ("locate", "--f-loc"), ("locate", "--f-loc"), ("tracking", "--f-trk"), ("tracking", "--f-trk"), ("ts", "--f-ts"), ("ts", "--f-ts"), ("ts", "--f-ts")]
div("rl", 20, 255, 160, inner="clk 8", cue=0)
for l, (t, c) in enumerate(w8):
    div("fc", X0 + l * (CW + 6), 240, CW, 70, t, style=f"background:var({c});font-size:19px", cue=0, anim="fade", hl=(0 if l in (1, 2) else None), hlend=2)
svg_open()
path("fl-a1", "M 418 320 L 418 440", "#ffb347", 1, marker="ah-amber", width=4)
path("fl-keep", "M 890 520 L 1060 520 L 1060 350 L 1420 350", "#4fd18b", 2, marker="ah-green", width=4)
path("fl-drop", "M 890 560 L 1060 560 L 1060 720 L 1420 720", "#ff6b5e", 2, marker="ah-red", width=4)
svg_close()
div("stage amber", 200, 450, 690, 160, "keep[locate]<small>65,536 × 1 bit · block RAM<br>one bit per stock locate</small>", cue=1)
div("stage green", 1430, 290, 400, 120, "order table<small>keep = 1</small>", cue=2)
div("stage red", 1430, 660, 400, 120, "drop<small>keep = 0</small>", cue=2)
for k in range(3):
    a(f'<div class="pkt" data-path="fl-keep" data-cue="2" data-d="0.5" data-dur="1.6" data-loop="1" data-phase="{k/3:.2f}" style="background:var(--green);box-shadow:0 0 14px var(--green)"></div>')
    a(f'<div class="pkt" data-path="fl-drop" data-cue="2" data-d="0.5" data-dur="1.6" data-loop="1" data-phase="{k/3+0.15:.2f}" style="background:var(--red);box-shadow:0 0 14px var(--red)"></div>')
# clock timeline
TY = 830
div("tl", 200, TY, 1300, style="height:3px", cue=2)
for i, (c, t, col) in enumerate([(8, "locate in", "--amber"), (9, "keep bit read", "--green"), (10, "order ref complete", "--f-ref")]):
    x = 200 + i * 520
    div("tick", x, TY - 7, cue=2, d=0.3 * i)
    div("kv", x - 20, TY + 18, 480, inner=f"<span style='color:var({col})'>clk {c}</span> · {t}", cue=2, d=0.3 * i)
a('</div>')

# ---------------------------------------------------------------- 8 table
a('<div class="scene" id="s-table">')
div("h2", 120, 110, inner="The order table", cue=0)
div("lbl", 120, 215, inner="E · X · D · U carry only the 64-bit order reference", cue=0, d=0.3)
# ref bar: 16 nibbles
for i in range(16):
    low = i >= 11
    div("fc", 120 + i * 54, 260, 50, 60, "", style="background:" + ("var(--f-ref)" if low else "#2c6b4a"), cue=0, d=0.4, anim="fade",
        hl=(2 if low else None), hlend=4)
div("lbl", 120, 330, 900, inner="order ref: high bits = tag · low bits = address", cue=2, d=0.4)
# RAM column
RX, RY = 1080, 220
div("lbl", RX, RY - 8, 400, inner="block RAM / UltraRAM", style="color:var(--green)", cue=1)
for i in range(8):
    sel = i == 4
    div("gc", RX, RY + 30 + i * 58, 760, 52, "", style=("border-color:var(--green);background:#16352a" if sel else ""), cue=1, d=0.05 * i, anim="fade",
        hl=(3 if sel else None))
ent = [("tag", 150, "#2c6b4a", "#e6edf2"), ("locate", 110, "var(--f-loc)", None), ("side", 80, "var(--f-side)", None), ("price", 200, "var(--f-px)", None), ("shares", 200, "var(--f-sh)", None)]
x = RX
for t, w, bg, fg in ent:
    div("fc", x, RY + 30 + 4 * 58, w, 52, t, style=f"background:{bg};" + (f"color:{fg};" if fg else "") + "font-size:19px", cue=1, d=0.6, anim="fade")
    x += w + 4
svg_open()
path("tb-a", "M 1000 320 C 1040 320 1040 494 1072 494", "#4fd18b", 3, marker="ah-green", width=4)
svg_close()
div("code", 120, 420, inner="<span class='c'>// libs/book order_map.hpp: identity hash</span>\n<span class='k'>return</span> static_cast&lt;std::size_t&gt;(key) &amp; mask_;", style="font-size:23px", cue=2)
div("note", 120, 575, 880, inner="Nasdaq assigns references in sequence, so live orders sit in a sliding window of adjacent slots.", cue=2, d=0.8)
div("lbl", RX, 720, 760, inner="read ≈ 1–2 clocks on chip (typical)", style="color:var(--green)", cue=3, d=0.4)
# capacity
div("box amber", 120, 780, 820, inner="<div class='t'>BookBuilder(expected_live_orders = 1u &lt;&lt; 22)</div><div class='s'>4,194,304 live orders × ~16 B ≈ 64 MiB</div>", cue=4)
div("note", 1000, 785, 840, inner="More than most FPGAs hold on chip. Filter by locate, or put the table in <span class='c-amber'>off-chip DRAM / HBM</span> and pay tens of clocks per access (typical).", cue=4, d=0.6)
a('</div>')

# ---------------------------------------------------------------- 9 hazard
a('<div class="scene" id="s-hazard">')
div("h2", 120, 110, inner="Back-to-back hazards", cue=0)
GX, GY, CWd = 420, 250, 165
for c in range(8):
    div("lane", GX + c * CWd, GY - 40, CWd - 10, inner=f"clk t+{c}", cue=0, style="font-size:20px")
div("rl", 60, GY + 14, 330, inner="Add  ref R", style="color:var(--green);font-size:26px", cue=0, d=0.3)
div("rl", 60, GY + 114, 330, inner="Delete ref R", style="color:var(--red);font-size:26px", cue=1, d=0.6)
A = [(0, 2, "read slot", "#2c6b4a", "#e6edf2"), (2, 1, "modify", "var(--green)", None), (3, 1, "write", "var(--green)", None)]
for s, n, t, bg, fg in A:
    div("blk", GX + s * CWd, GY, n * CWd - 10, inner=t, style=f"background:{bg};" + (f"color:{fg};" if fg else ""), cue=0, d=0.5 + 0.3 * s, anim="fade")
D = [(3, 2, "read slot", "var(--red)"), (5, 1, "modify", "#7a3b37"), (6, 1, "write", "#7a3b37")]
for s, n, t, bg in D:
    div("blk", GX + s * CWd, GY + 100, n * CWd - 10, inner=t, style=f"background:{bg};color:#f1f5f8" if bg != "var(--red)" else f"background:{bg}", cue=2, d=0.2 * (s - 3), anim="fade")
div("lbl", GX + 3 * CWd, GY + 170, 820, inner="19-byte Delete + 2-byte length ≈ 3 words later", cue=2, d=0.2)
div("tag", GX + 3 * CWd, GY + 210, inner="✕ reads the slot before the Add's write lands → stale", style="color:var(--red);border-color:var(--red)", cue=2, d=1.6)
svg_open()
path("hz-fwd", f"M {GX+3*CWd+80} {GY+60} C {GX+4*CWd} {GY+80} {GX+5*CWd-40} {GY+80} {GX+5*CWd+40} {GY+96}", "#4fd18b", 3, d_=0.8, marker="ah-green", width=5)
svg_close()
div("stage green", GX + 0 * CWd, 600, 600, 130, "ref == in-flight write ref?<small>compare against every write stage</small>", cue=3)
div("tag", GX + 3 * CWd, GY + 265, inner="✓ forward the Add's newest value to the Delete", style="color:var(--green);border-color:var(--green)", cue=3, d=1.2)
div("note", GX, 770, 1200, inner="Same idea as a CPU's bypass network: the RAM is the slow path; registers hold the truth for a few clocks.", cue=3, d=1.8)
a('</div>')

# ---------------------------------------------------------------- 10 exec
a('<div class="scene" id="s-exec">')
div("h2", 120, 110, inner="Executions, cancels, deletes", cue=0)
msgs = [("E", "Order Executed · 31 B", "ref 11:8 · executed shares 19:4", 0, "--f-ref"),
        ("X", "Order Cancel · 23 B", "ref 11:8 · cancelled shares 19:4", 3, "--amber"),
        ("D", "Order Delete · 19 B", "ref 11:8", 3.5, "--red")]
for i, (t, n, f, c, col) in enumerate(msgs):
    div("box", 120, 230 + i * 150, 620, inner=f"<div class='t'><span style='color:var({col})'>{t}</span> · {n}</div><div class='s'>{f}</div>", cue=c,
        style=f"border-color:var({col})")
div("stage green", 840, 250, 360, 120, "order table<small>lookup(ref)</small>", cue=1)
div("box", 1290, 230, 540, inner="<div class='s'>order R</div><div class='t mono'>locate 42 · B · <span class='c-teal'>101.2500</span></div><div class='kv'>shares <span id='ex-os' class='c-violet'>500</span></div>", cue=1, d=0.4, out=4.5, extra=' id="ex-ord"')
div("box teal", 1290, 520, 540, inner="<div class='s'>bid level 101.2500</div><div class='kv'>shares <span id='ex-ls' class='c-violet'>1,200</span> · orders <span id='ex-lo'>3</span></div>", cue=2)
div("tag", 1290, 700, inner="", cue=2, extra=' id="ex-op"', style="color:var(--amber)")
svg_open()
path("ex-a1", "M 740 290 L 832 300", "#4fd18b", 1, marker="ah-green", width=3)
path("ex-a2", "M 1200 310 L 1282 300", "#4fd18b", 1, d_=0.4, marker="ah-green", width=3)
path("ex-a3", "M 1560 420 L 1560 512", "#3fd0dc", 2, marker="ah-teal", width=3)
svg_close()
div("note", 1290, 790, 560, inner="order at zero → leaves the table · level at zero → leaves the book", cue=4, style="color:var(--teal)")
a('</div>')

# ---------------------------------------------------------------- 11 levels
a('<div class="scene" id="s-levels">')
div("h2", 120, 110, inner="Top-N levels in registers", cue=0)
div("lbl", 360, 205, inner="bid side · best first", style="color:var(--green)", cue=0)
lv = [("101.2500", "800"), ("101.2400", "1,500"), ("101.2200", "300"), ("101.2000", "2,100"), ("101.1800", "900"), ("101.1500", "1,200")]
for i, (p, s) in enumerate(lv):
    a(f'<div class="reg" id="lv-r{i}" style="left:360px;top:{245+i*86}px;width:560px" data-cue="0" data-d="{0.1*i:.1f}" data-anim="fade"><span><span class="c-muted" id="lv-l{i}">L{i}</span>  {p} <span class="c-violet">× <span id="lv-s{i}">{s}</span></span></span></div>')
    div("fc", 250, 255 + i * 86, 80, 54, "≥?", style="background:#2a3f4c;color:#e6edf2", cue=1, anim="fade", hl=1, hlend=2)
a('<div class="reg" id="lv-new" style="left:360px;top:417px;width:560px;border-color:var(--green)" data-cue="2" data-anim="fade"><span><span class="c-muted">L2</span>  101.2300 <span class="c-violet">× 300</span></span></div>')
div("box green", 1120, 240, 600, inner="<div class='t'>Add · B · 101.2300 × 300</div><div class='s'>compare with all N levels at once</div>", cue=0.5)
div("note", 1120, 400, 640, inner="L0, L1 better · L2 and below worse → insert at L2, shift L2..L5 down one register", cue=2, d=0.4)
div("stage violet", 1120, 560, 600, 110, "deeper levels in RAM<small>refill a register when a level empties</small>", cue=3)
div("box amber", 1120, 740, 600, inner="<div class='t'>top-of-book event</div><div class='s'>L0 size 800 → 500: best bid 101.2500 × 500</div>", cue=4, d=0.6)
a('</div>')

# ---------------------------------------------------------------- 12 cut
a('<div class="scene" id="s-cut">')
div("h2", 120, 110, inner="Cut-through: book before CRC", cue=0)
# scale: 0..1200 ns over 160..1760 -> 1.3333 px/ns
SX = lambda ns: 160 + ns * 1600 / 1200
div("lbl", 160, 250, 1600, inner="one frame: 14 + 20 + 8 + 1400 + 4 FCS = 1,446 B → 181 words → 1.16 µs at the MAC", cue=0, d=0.3)
div("grow", 160, 300, h=70, style="background:linear-gradient(90deg,var(--itch),#1d5563);border-radius:8px", cue=0, extra=f' data-w="{SX(1158.4)-160:.0f}" data-dur="2.2"')
div("fc", SX(1158.4) - 50, 300, 50, 70, "FCS", style="background:var(--red);font-size:15px", cue=1)
for ns, t in [(0, "0"), (400, "400 ns"), (800, "800 ns"), (1158.4, "1.16 µs")]:
    div("tick", SX(ns), 380, cue=0)
    div("lane", SX(ns) - 70, 400, 140, inner=t, cue=0)
div("", SX(128) - 2, 285, 4, 100, "", style="background:var(--green)", cue=2)
div("tag", SX(128) - 30, 450, inner="first message booked ≈ 130 ns", style="color:var(--green);border-color:var(--green)", cue=2, d=0.2)
div("tag", SX(1158.4) - 260, 450, inner="CRC known ≈ 1.16 µs", style="color:var(--red);border-color:var(--red)", cue=1, d=0.3)
svg_open()
path("cut-br", f"M {SX(128)} 530 L {SX(128)} 550 L {SX(1158.4)} 550 L {SX(1158.4)} 530", "#ffb347", 2, d_=0.6, width=3)
svg_close()
div("lbl", SX(500), 565, 600, inner="≈ 1 µs of speculative book state", style="color:var(--amber)", cue=2, d=0.8)
div("stage amber", 160, 660, 760, 170, "roll back<small>per-packet undo log: old level values<br>restore if the MAC flags a bad frame</small>", cue=3)
div("stage red", 1000, 660, 760, 170, "drop and resync<small>mark books invalid, rebuild from<br>a snapshot or a replay</small>", cue=3, d=0.6)
a('</div>')

# ---------------------------------------------------------------- 13 out
a('<div class="scene" id="s-out">')
div("h2", 120, 110, inner="Output, and gaps", cue=0)
div("box teal", 120, 220, 560, 230, "<div class='t'>FPGA card</div><div class='s'>parse → filter → orders → levels</div><div class='s' style='margin-top:14px;color:var(--amber)'>book events</div>", cue=0)
div("stage blue", 860, 210, 460, 100, "PCIe DMA<small>into a host ring</small>", cue=0, d=0.3)
div("stage blue", 1400, 210, 400, 100, "strategy<small>polls the ring</small>", cue=0, d=0.6)
div("stage green", 860, 350, 940, 100, "order entry on the card<small>book event → order → MAC TX, host not in the path</small>", cue=0.5)
svg_open()
path("out-a1", "M 680 260 L 852 260", "#6aa8ff", 0, d_=0.3, marker="ah", width=3)
path("out-a2", "M 1320 260 L 1392 260", "#6aa8ff", 0, d_=0.6, marker="ah", width=3)
path("out-a3", "M 680 400 L 852 400", "#4fd18b", 0.5, marker="ah-green", width=3)
svg_close()
CW, X0 = 112, 260
mold = {5: [None, None] + [("session", "--mold")] * 6, 6: [("session", "--mold")] * 4 + [("seq", "--f-loc")] * 4, 7: [("seq", "--f-loc")] * 4 + [("count", "--mold")] * 2 + [("len", "--len")] * 2}
for i, w in enumerate((5, 6, 7)):
    div("rl", 120, 535 + i * 84, 110, inner=f"w{w}", cue=1)
    for l, c in enumerate(mold[w]):
        if c is None:
            div("gc", X0 + l * (CW + 6), 520 + i * 84, CW, 66, "UDP", cue=1, anim="fade")
        else:
            div("fc", X0 + l * (CW + 6), 520 + i * 84, CW, 66, c[0], style=f"background:var({c[1]});font-size:19px", cue=1, anim="fade",
                hl=(1.5 if c[0] == "seq" else None), hlend=3)
div("lbl", X0, 780, 900, inner="sequence number: frame bytes 52–59 · w6 L4 → w7 L3", cue=1, d=0.5)
div("box red", 1300, 520, 500, inner="<div class='s'>expected 1,001 · packet says 1,004</div><div class='t' style='color:var(--red)'>gap: 3 messages missing</div>", cue=2)
div("note", 1300, 690, 520, inner="Books for every stock are now suspect: flag them, keep the gap range, and hand over to software recovery (re-request or snapshot).", cue=2, d=0.5)
a('</div>')

# ---------------------------------------------------------------- 14 timing
a('<div class="scene" id="s-timing">')
div("h2", 120, 110, inner="Cycle budget (typical)", cue=0)
BX, BW = 160, 78
for c in range(20):
    col = "var(--itch)" if c <= 12 else ("var(--green)" if c <= 15 else "var(--violet)")
    cu = 0 if c <= 12 else 1
    div("fc", BX + c * BW, 250, BW - 4, 70, str(c), style=f"background:{col}", cue=cu, d=round(0.08 * c if c <= 12 else 0.15 * (c - 13), 2), anim="fade")
div("lbl", BX, 335, 13 * BW, inner="words 0–12 arrive · price done clk 12 = 13 × 6.4 = 83.2 ns", style="color:var(--teal)", cue=0, d=0.6)
div("lbl", BX + 13 * BW, 335, 3 * BW + 40, inner="order table", style="color:var(--green)", cue=1, d=0.3)
div("lbl", BX + 16 * BW, 335, 4 * BW + 40, inner="level + TOB", style="color:var(--violet)", cue=1, d=0.6)
div("big", BX, 400, 1500, inner="20 clocks × 6.4 ns ≈ <span class='c-teal'>130 ns</span> <span class='lbl'>+ PHY and MAC latency</span>", cue=1)
# compare (log scale, 10 ns .. 10 us -> 0..1300 px)
import math
LW = lambda ns: (math.log10(ns) - 1) / 3 * 1100
rows = [("kernel socket receive", "microseconds (typical)", 3000, "var(--blue)", 2, "#8ea3b1"),
        ("BookBuilder apply", "107 ns avg · lab itch_bench, shared cloud VM", 107, "var(--blue)", 3, None),
        ("FPGA wire → book", "≈ 130 ns (typical)", 130, "var(--teal)", 3.6, None)]
div("lbl", 160, 530, 900, inner="per message · log scale", cue=2)
for i, (n, s, ns, col, cu, _) in enumerate(rows):
    y = 580 + i * 100
    div("kv", 160, y + 6, 380, inner=n, cue=cu)
    div("grow", 560, y, h=56, style=f"background:{col};border-radius:6px", cue=cu, extra=f' data-w="{LW(ns):.0f}" data-dur="1"')
    div("lbl", 560 + LW(ns) + 20, y + 14, 700, inner=s, cue=cu, d=0.8)
div("tag", 160, 890 - 0, inner="the win: no waiting for the whole packet, and no trip through the kernel", style="color:var(--teal);border-color:var(--teal);font-size:24px", cue=4)
a('</div>')

open(OUT, "w").write("\n".join(H))
print("ok", len(H))
