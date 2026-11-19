# Generates scenes.html for cpp-false-sharing.
OUT = "/mnt/project-files/videos/explainers/cpp-false-sharing/scenes.html"
TEAL, VIOLET, AMBER, RED, GREEN, BLUE, MUTED = "var(--teal)", "var(--violet)", "var(--amber)", "var(--red)", "var(--green)", "var(--blue)", "var(--muted)"
H = []
def a(s): H.append(s)

def code(lines, x, y, w, cue=0, size=25, extra=""):
    out = []
    for ln in lines:
        if isinstance(ln, tuple):
            txt, hl = ln[0], ln[1]
            end = f' data-hlend="{ln[2]}"' if len(ln) > 2 else ""
            out.append(f'<span class="line" data-hl="{hl}"{end}>{txt}</span>')
        else:
            out.append(f'<span class="line">{ln}</span>')
    return f'<div class="code" data-cue="{cue}" {extra} style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px">' + "".join(out) + "</div>"

def strip(cells, x, y, cw, h=64, cue=0, d=0, extra="", ident=""):
    """cells: list of (label, bg, fg) each one cell of width cw."""
    idattr = f' id="{ident}"' if ident else ""
    inner = "".join(f'<div style="width:{cw*(c[3] if len(c)>3 else 1)}px;height:{h}px;background:{c[1]};color:{c[2]}">{c[0]}</div>' for c in cells)
    return f'<div class="bytes"{idattr} data-cue="{cue}" data-d="{d}" {extra} style="left:{x}px;top:{y}px">{inner}</div>'

E = "#1a2a35"   # empty byte
EF = "#6f8796"

# ---------------- title
a('<div class="scene" id="s-title">')
a('<div class="eyebrow" data-cue="0" style="left:140px;top:150px">TRADING LAB · LOW-LATENCY C++</div>')
a('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:200px">Cache lines &amp;<br>false sharing</div>')
a('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:500px;width:1500px">Two threads. Two counters. One 64-byte line.</div>')
a('<div class="box teal" data-cue="0" data-d="0.8" style="left:140px;top:650px;width:330px;height:150px;text-align:center"><div class="t">Core 1</div><div class="s">thread 1 · ++a</div></div>')
a('<div class="box violet" data-cue="0" data-d="1.0" style="left:1450px;top:650px;width:330px;height:150px;text-align:center"><div class="t">Core 2</div><div class="s">thread 2 · ++b</div></div>')
cells = [("a", TEAL, "#06141a"), ("b", VIOLET, "#06141a")] + [("", E, EF)] * 6
a(strip(cells, 640, 690, 80, h=70, cue=1, extra='data-hl="2"', ident="tl-line"))
a('<div class="lbl" data-cue="1" style="left:640px;top:775px;width:640px;text-align:center">one 64-byte cache line</div>')
a('<svg class="full"><path id="tl-pp" d="M 480 725 L 1440 725" stroke="none" fill="none"/></svg>')
a(f'<div class="pkt" data-cue="1.5" data-path="tl-pp" data-dur="0.9" data-loop="1" style="background:{AMBER};box-shadow:0 0 16px {AMBER}"></div>')
a('</div>')

# ---------------- line
a('<div class="scene" id="s-line">')
a('<div class="h2" data-cue="0" style="left:128px;top:110px">Memory moves in 64-byte lines</div>')
X0, CW, Y = 128, 26, 330
for i in range(64):
    bg = "#24414f"
    hl = ' data-hl="2.6"' if i == 56 else ""
    a(f'<div class="cell" data-cue="1" data-d="{0.2 + i*0.012:.3f}" data-anim="fade"{hl} style="left:{X0+i*CW}px;top:{Y}px;width:{CW}px;background:{bg};color:#9fb6c3;font-size:14px"></div>')
for i in list(range(0, 64, 8)) + [63]:
    a(f'<div class="lbl" data-cue="1" data-d="0.3" style="left:{X0+i*CW-17}px;top:{Y-36}px;width:60px;text-align:center;font-size:18px">{i}</div>')
a(f'<div class="brace" data-cue="1" data-d="1.0" style="left:{X0}px;top:{Y+76}px;width:{64*CW}px;border-color:var(--teal)"></div>')
a(f'<div class="lbl c-teal" data-cue="1" data-d="1.0" style="left:{X0}px;top:{Y+100}px;width:{64*CW}px;text-align:center">one line · 64 bytes · aligned to a multiple of 64</div>')
a(f'<div class="glow" data-cue="3" data-anim="fade" style="left:{X0-6}px;top:{Y-6}px;width:{64*CW+12}px;height:76px"></div>')
a(f'<div class="lbl c-amber" data-cue="3" style="left:{X0+56*CW-160}px;top:{Y-80}px;width:400px;text-align:center">you read byte 56 …</div>')
a(f'<div class="lbl c-teal" data-cue="3" data-d="0.6" style="left:{X0}px;top:{Y-80}px;width:600px">… the core fetches all 64</div>')
# address split
a('<div class="lbl" data-cue="2" style="left:128px;top:530px">ADDRESS (64-bit)</div>')
a(strip([("line number · bits 63..6", "#2c5866", "#dff6fa", 14), ("offset · bits 5..0", AMBER, "#06141a", 5)], 128, 570, 60, h=74, cue=2))
a('<div class="mono" data-cue="2" data-d="0.8" style="left:128px;top:670px;font-size:28px;color:#d4e0e7">0x7ffd12345678 <span class="c-muted">→</span> line <span class="c-teal">0x7ffd12345640</span> + byte <span class="c-amber">0x38</span> = <span class="c-amber">56</span></div>')
a('<div class="code" data-cue="4" style="left:128px;top:760px;width:760px;font-size:26px"><span class="line"><span class="c">$</span> getconf LEVEL1_DCACHE_LINESIZE</span><span class="line"><span class="r">64</span></span></div>')
a('<div class="lbl" data-cue="4" data-d="0.4" style="left:930px;top:790px;width:880px;line-height:1.5">this box: 4 vCPU KVM guest, Intel Xeon @ 2.10 GHz<br>coherency_line_size in sysfs also says 64</div>')
a('</div>')

# ---------------- mesi
a('<div class="scene" id="s-mesi">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Every cached line has a state</div>')
for k, (x, col, name) in enumerate([(120, "teal", "Core 1"), (540, "violet", "Core 2")]):
    a(f'<div class="box {col}" data-cue="0" data-d="{0.3+k*0.2}" style="left:{x}px;top:230px;width:380px;height:90px;text-align:center;padding-top:20px"><div class="t">{name}</div></div>')
    a(f'<div class="box" data-cue="0" data-d="{0.5+k*0.2}" style="left:{x}px;top:345px;width:380px;height:200px"><div class="lbl">L1d · private</div></div>')
    a(strip([("", "#2c5866", "#06141a")] * 8, x + 22, 400, 40, h=50, cue=0, d=0.6 + k * 0.2))
    a(f'<div class="badge" id="me-b{k}" data-cue="3" style="left:{x+120}px;top:470px">S</div>')
a('<svg class="full"><path class="draw" data-cue="5" data-d="0.4" d="M 340 600 C 420 680, 640 680, 720 600" stroke="var(--red)" stroke-width="4" fill="none" marker-end="url(#ah-red)"/></svg>')
a('<div class="lbl c-red" data-cue="5" data-d="0.6" style="left:330px;top:680px;width:420px;text-align:center;white-space:nowrap">write ⇒ invalidate the other copy</div>')
a('<div class="lbl c-amber" data-cue="5" data-d="1.2" style="left:120px;top:760px;width:900px">core 1 now owns the line (M); core 2 must miss to read it</div>')
states = [("M", "Modified", "only copy · dirty · may write", AMBER),
          ("E", "Exclusive", "only copy · clean · may write", GREEN),
          ("S", "Shared", "other cores may hold copies · read-only", BLUE),
          ("I", "Invalid", "no valid copy here", RED)]
for k, (L, name, desc, col) in enumerate(states):
    y = 230 + k * 140
    a(f'<div class="st" data-cue="{k+1}" data-hl="{k+1}" data-hlend="{k+2}" style="left:1040px;top:{y}px;border-color:{col}"><div class="sl" style="background:{col}">{L}</div><div><div class="sn">{name}</div><div class="sd">{desc}</div></div></div>')
a('</div>')

# ---------------- pingpong
a('<div class="scene" id="s-pingpong">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">One line, two writers</div>')
cells = [("a · 8 B", TEAL, "#06141a"), ("b · 8 B", VIOLET, "#06141a")] + [("", E, EF)] * 6
a(strip(cells, 360, 215, 150, h=70, cue=0, d=0.3))
a('<div class="lbl" data-cue="0" data-d="0.5" style="left:360px;top:292px;width:1200px;text-align:center">struct Packed { std::atomic&lt;long&gt; a, b; } — 16 bytes, one line</div>')
for k, (x, col, name, th) in enumerate([(160, "teal", "Core 1", "thread 1 · ++a"), (1240, "violet", "Core 2", "thread 2 · ++b")]):
    a(f'<div class="box {col}" data-cue="{k+1}" style="left:{x}px;top:360px;width:520px;height:250px"><div class="t">{name}</div><div class="s">{th}</div></div>')
    a(strip([("a", TEAL, "#06141a"), ("b", VIOLET, "#06141a")] + [("", E, EF)] * 6, x + 30, 470, 46, h=46, cue=k + 1, d=0.2, ident=f"pp-l{k}"))
    a(f'<div class="badge" id="pp-b{k}" data-cue="{k+1}" data-d="0.3" style="left:{x+30}px;top:540px">E</div>')
    a(f'<div class="cnt mono" id="pp-c{k}" data-cue="{k+1}" data-d="0.3" style="left:{x+130}px;top:548px;color:{TEAL if k==0 else VIOLET}">{"a" if k==0 else "b"} = 0</div>')
a('<svg class="full"><path id="pp-path" d="M 690 500 L 1230 500" stroke="#2c4351" stroke-width="3" stroke-dasharray="8 8" fill="none" data-cue="3"/></svg>')
a('<div class="tok" id="pp-tok" data-cue="3" data-anim="none" style="left:0;top:0">line</div>')
a('<div class="lbl c-red" data-cue="3" data-d="0.4" style="left:760px;top:420px;width:400px;text-align:center">request for ownership</div>')
# timeline
a('<div class="lbl" data-cue="4" style="left:160px;top:660px">WHO OWNS THE LINE</div>')
a('<div class="lbl c-teal" data-cue="4" style="left:160px;top:705px">core 1</div>')
a('<div class="lbl c-violet" data-cue="4" style="left:160px;top:765px">core 2</div>')
a('<div class="tlax" data-cue="4" style="left:290px;top:820px;width:1470px"></div>')
for j in range(28):
    row = j % 2
    a(f'<div class="tb" id="pp-t{j}" style="left:{290+j*52}px;top:{700+row*60}px;background:{TEAL if row==0 else VIOLET}"></div>')
a('<div class="lbl c-amber" data-cue="5" style="left:290px;top:850px">no shared data — only a shared line</div>')
a('<div class="big c-red" data-cue="6" data-anim="scale" style="left:1240px;top:640px">FALSE SHARING</div>')
a('</div>')

# ---------------- fix
a('<div class="scene" id="s-fix">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Fix: one line per writer</div>')
a(code([
    ('<span class="k">struct</span> <span class="v">Packed</span> {             <span class="c">// one line</span>', 0, 1),
    ('  std::atomic&lt;<span class="k">long</span>&gt; a{<span class="r">0</span>};', 0, 1),
    ('  std::atomic&lt;<span class="k">long</span>&gt; b{<span class="r">0</span>};', 0, 1),
    '};',
    ('<span class="k">struct</span> <span class="v">Padded</span> {             <span class="c">// two lines</span>', 1, 2),
    ('  <span class="k">alignas</span>(<span class="r">64</span>) std::atomic&lt;<span class="k">long</span>&gt; a{<span class="r">0</span>};', 1, 2),
    ('  <span class="k">alignas</span>(<span class="r">64</span>) std::atomic&lt;<span class="k">long</span>&gt; b{<span class="r">0</span>};', 1, 2),
    '};',
    ('<span class="k">static_assert</span>(<span class="k">sizeof</span>(Packed) == <span class="r">16</span>);', 2, 3),
    ('<span class="k">static_assert</span>(<span class="k">sizeof</span>(Padded) == <span class="r">128</span>);', 2, 3),
], 120, 220, 860, cue=0, size=26))
a('<div class="lbl c-muted" data-cue="2" data-d="0.5" style="left:120px;top:690px">compiled with g++ 13.3 -std=c++20 -O2 on this box</div>')
a('<div class="lbl" data-cue="0" data-d="0.4" style="left:1060px;top:220px">PACKED · 16 BYTES</div>')
a(strip([("a", TEAL, "#06141a"), ("b", VIOLET, "#06141a")] + [("", E, EF)] * 6, 1060, 260, 88, h=60, cue=0, d=0.4))
a('<div class="lbl" data-cue="1" style="left:1060px;top:390px">PADDED · 128 BYTES</div>')
a(strip([("a", TEAL, "#06141a")] + [("pad", E, EF)] * 7, 1060, 430, 88, h=60, cue=1, d=0.2))
a(strip([("b", VIOLET, "#06141a")] + [("pad", E, EF)] * 7, 1060, 500, 88, h=60, cue=1, d=0.5))
a('<div class="lbl" data-cue="1" data-d="0.3" style="left:1060px;top:568px">line 0 · bytes 0–63&#160;&#160;&#160;&#160;line 1 · bytes 64–127</div>')
a(f'<div class="badge" data-cue="3" style="left:1780px;top:436px;background:{AMBER}">M</div>')
a(f'<div class="badge" data-cue="3" data-d="0.2" style="left:1780px;top:506px;background:{AMBER}">M</div>')
a('<div class="lbl c-teal" data-cue="3" data-d="0.4" style="left:1060px;top:640px">core 1 keeps line 0</div>')
a('<div class="lbl c-violet" data-cue="3" data-d="0.6" style="left:1060px;top:680px">core 2 keeps line 1</div>')
a('<div class="lbl c-green" data-cue="3" data-d="0.9" style="left:1060px;top:720px">no invalidations · writes hit L1</div>')
a('</div>')

# ---------------- hdi
a('<div class="scene" id="s-hdi">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px;font-size:56px">std::hardware_destructive_interference_size</div>')
a(code([
    '<span class="c">// counters.hpp</span>',
    '<span class="k">#include</span> <span class="g">&lt;atomic&gt;</span>',
    ('<span class="k">#include</span> <span class="g">&lt;new&gt;</span>', 0, 1),
    '',
    ('<span class="k">constexpr</span> std::size_t kLine = std::hardware_destructive_interference_size;', 0, 2),
    '',
    '<span class="k">struct</span> <span class="v">Counters</span> {',
    '  <span class="k">alignas</span>(kLine) std::atomic&lt;<span class="k">long</span>&gt; a{<span class="r">0</span>};',
    '  <span class="k">alignas</span>(kLine) std::atomic&lt;<span class="k">long</span>&gt; b{<span class="r">0</span>};',
    '};',
], 120, 200, 1220, cue=0, size=22))
facts = [("C++17 · header &lt;new&gt;", "", 0), ("GCC ≥ 12 only", "c-amber", 1), ("x86-64 GCC: 64", "c-teal", 2), ("AArch64 GCC: 256", "c-violet", 3), ("Intel line-pair prefetch: 128", "c-pink", 5)]
for k, (t, c, cue) in enumerate(facts):
    a(f'<div class="fact {c}" data-cue="{cue}" data-d="0.3" style="left:1390px;top:{205+k*72}px">{t}</div>')
a('<div class="warn" data-cue="4" style="left:120px;top:600px;width:1680px">'
  '<div><span class="c-muted">$ g++ -std=c++20 -O2 use_counters.cpp</span></div>'
  '<div>counters.hpp:5:36: <span class="c-amber">warning:</span> use of \'std::hardware_destructive_interference_size\' [-Winterference-size]</div>'
  '<div>counters.hpp:5:36: <span class="c-teal">note:</span> its value can vary between compiler versions or with different \'-mtune\' or \'-mcpu\' flags</div>'
  '<div>counters.hpp:5:36: <span class="c-teal">note:</span> if this use is part of a public ABI, change it to instead use a constant variable you define</div>'
  '<div>counters.hpp:5:36: <span class="c-teal">note:</span> the default value for the current CPU tuning is 64 bytes</div>'
  '</div>')
a('<div class="lbl c-muted" data-cue="4" data-d="0.6" style="left:120px;top:860px">real output, GCC 13.3 on this box (the same use in a .cpp file does not warn)</div>')
a('</div>')

# ---------------- lab
a('<div class="scene" id="s-lab">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">The lab’s SpscRing</div>')
a(code([
    '<span class="c">// libs/core/include/lab/core/compiler.hpp</span>',
    ('<span class="k">inline constexpr</span> std::size_t kCacheLine = <span class="r">64</span>;', 1, 2),
    '',
    '<span class="c">// spsc_ring.hpp, private members</span>',
    ('<span class="c">// Producer-owned line.</span>', 2, 3),
    ('<span class="k">alignas</span>(kCacheLine) std::atomic&lt;std::uint64_t&gt; head_{<span class="r">0</span>};', 2, 3),
    ('std::uint64_t cached_tail_{<span class="r">0</span>};', 2, 3),
    ('<span class="c">// Consumer-owned line.</span>', 3, 4),
    ('<span class="k">alignas</span>(kCacheLine) std::atomic&lt;std::uint64_t&gt; tail_{<span class="r">0</span>};', 3, 4),
    ('std::uint64_t cached_head_{<span class="r">0</span>};', 3, 4),
    ('<span class="k">alignas</span>(kCacheLine) T slots_[Capacity]{};', 4, 5),
], 120, 210, 1000, cue=0, size=22))
a('<div class="lbl c-muted" data-cue="1" data-d="0.4" style="left:120px;top:690px;width:1000px;line-height:1.45">“Fixed at 64 rather than std::hardware_destructive_interference_size, which varies by compiler flags and would change the layout of shared-memory structs.”</div>')
rows = [("+0", [("head_", TEAL, "#06141a"), ("cached_tail_", TEAL, "#06141a")] + [("", E, EF)] * 6, 2, "producer writes"),
        ("+64", [("tail_", VIOLET, "#06141a"), ("cached_head_", VIOLET, "#06141a")] + [("", E, EF)] * 6, 3, "consumer writes"),
        ("+128", [(f"slot {i}", "#2f6b52", "#dff7ea") for i in range(8)], 4, "slots_ (T = 8 B here)")]
for k, (off, cells, cue, note) in enumerate(rows):
    y = 240 + k * 150
    a(f'<div class="lbl" data-cue="{cue}" style="left:1160px;top:{y+18}px;width:70px;text-align:right">{off}</div>')
    cells = [(c[0], c[1], c[2], 2) if c[0] in ("cached_tail_", "cached_head_") else c for c in cells]
    if k < 2: cells = cells[:2] + cells[3:]
    a(strip(cells, 1250, y, 68, h=60, cue=cue, d=0.1))
    col = ["c-teal", "c-violet", "c-green"][k]
    a(f'<div class="lbl {col}" data-cue="{cue}" data-d="0.4" style="left:1250px;top:{y+70}px">{note}</div>')
a('<div class="lbl" data-cue="4" data-d="0.8" style="left:1160px;top:690px;width:680px;line-height:1.45">offsetof checked on a copy: tail_ at 64, slots_ at 128</div>')
a('<div class="lbl c-amber" data-cue="5" style="left:1160px;top:770px;width:680px">each index line has exactly one writer</div>')
a('</div>')

# ---------------- measured
a('<div class="scene" id="s-measured">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Measured on this box</div>')
a('<div class="pill" data-cue="0" data-d="0.4" style="left:120px;top:200px">4 vCPU KVM · Xeon @ 2.10 GHz · g++ 13.3 -O2 -pthread · SCHED_FIFO</div>')
a(code([
    ('<span class="c">// one pinned thread per counter, cores 1 and 2</span>', 1, 2),
    ('<span class="k">for</span> (<span class="k">long</span> i = <span class="r">0</span>; i &lt; N; ++i)', 1, 2),
    ('  c.a.fetch_add(<span class="r">1</span>, std::memory_order_relaxed);', 1, 2),
], 120, 270, 1000, cue=1, size=24))
a('<div class="lbl" data-cue="2" style="left:120px;top:470px">NS PER INCREMENT · MEDIAN</div>')
a('<div class="lbl c-red" data-cue="2" style="left:120px;top:530px;width:200px">packed</div>')
a('<div class="grow bar" data-cue="2" data-w="@PW@" data-dur="1.2" style="left:330px;top:520px;background:var(--red);height:56px"></div>')
a('<div class="val mono c-red" data-cue="2" data-d="1.0" style="left:@PWX@px;top:528px"><span class="count" data-cue="2" data-d="0.2" data-from="0" data-to="@P@" data-dec="1" data-post=" ns">0</span></div>')
a('<div class="lbl c-green" data-cue="3" style="left:120px;top:630px;width:200px">padded</div>')
a('<div class="grow bar" data-cue="3" data-w="@QW@" data-dur="1.2" style="left:330px;top:620px;background:var(--green);height:56px"></div>')
a('<div class="val mono c-green" data-cue="3" data-d="1.0" style="left:@QWX@px;top:628px"><span class="count" data-cue="3" data-d="0.2" data-from="0" data-to="@Q@" data-dec="1" data-post=" ns">0</span></div>')
a('<div class="big c-amber" data-cue="4" data-anim="scale" style="left:1250px;top:300px">@R@× faster</div>')
a('<div class="lbl c-muted" data-cue="5" style="left:120px;top:740px;width:1600px;line-height:1.5">@NOTE@</div>')
a('</div>')

import json, os
N = json.load(open("/tmp/claude-0/vx/cpp-false-sharing/nums.json"))
html = "\n".join(H)
scale = 900 / max(N["P"], N["Q"])
pw, qw = round(N["P"] * scale), round(N["Q"] * scale)
for k, v in {"@PW@": pw, "@QW@": qw, "@PWX@": 330 + pw + 20, "@QWX@": 330 + qw + 20, "@P@": N["P"], "@Q@": N["Q"],
             "@R@": N["R"], "@NOTE@": N["NOTE"]}.items():
    html = html.replace(k, str(v))
open(OUT, "w").write(html)
print("wrote", OUT)
