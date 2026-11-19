# scenes.html / scenes.js / style.css for cpp-live-optimize (exec'd by gen.py)
O = []
def a(s): O.append(s)
def scene(i): a(f'<div class="scene" id="s-{i}">')
def end(): a('</div>')
def esc(s): return html.escape(s)
FOOT = 'measured on this box: shared 4-vCPU KVM, Xeon 2.1 GHz · g++ 13.3 -O2 · pinned, chrt -f 10'

def h2(t, cue=0): a(f'<div class="h2" data-cue="{cue}" style="left:120px;top:108px">{t}</div>')
def lbl(t, x, y, cue, d=0, w=None, cls='', extra=''):
    ww = f'width:{w}px;' if w else ''
    dd = f' data-d="{d}"' if d else ''
    a(f'<div class="lbl {cls}" data-cue="{cue}"{dd} {extra} style="left:{x}px;top:{y}px;{ww}">{t}</div>')
def foot(cue, y=890, d=0.4, t=FOOT):
    a(f'<div class="foot" data-cue="{cue}" data-d="{d}" style="left:120px;top:{y}px">{t}</div>')

def code(lines, x, y, w, cue=0, d=0, lang='cpp', sm=False, extra='', title=None):
    """lines: str, or (text, opts) with opts dict: hl=(cue,end), dele=cue, add=cue, dim=cue."""
    fn = hl_cpp if lang == 'cpp' else hl_asm
    parts = []
    for ln in lines:
        o = {}
        if isinstance(ln, tuple): ln, o = ln
        attr = ''
        if 'hl' in o:
            s, e = o['hl']; attr += f' data-hl="{s}"' + (f' data-hlend="{e}"' if e is not None else '')
        if 'dim' in o: attr += f' data-dim="{o["dim"]}"'
        cls = 'line'
        if 'add' in o:
            cls += ' addl'
            body = f'<span class="gut" data-cue="{o["add"]}" data-anim="none">+</span><span class="type c-green" data-cue="{o["add"]}" data-dur="{o.get("dur", 1.0)}" data-anim="none">{esc(ln)}</span>'
        else:
            body = fn(ln) if ln else ' '
            if 'dele' in o:
                body = f'<span class="gut gm" data-cue="{o["dele"]}" data-anim="none">-</span>' + body + \
                       f'<span class="delov" data-cue="{o["dele"]}" data-anim="fade"></span>'
        parts.append(f'<span class="{cls}"{attr}>{body}</span>')
    dd = f' data-d="{d}"' if d else ''
    c = 'code sm' if sm else 'code'
    if title:
        lbl(title, x, y - 34, cue, d)
    a(f'<div class="{c}" data-cue="{cue}"{dd} {extra} style="left:{x}px;top:{y}px;width:{w}px">' + ''.join(parts) + '</div>')

def meter(frm, to=None, at=None, part=1):
    """Running latency meter, top right. frm/to: (label, p50, p99)."""
    to = to or frm
    hdr = 'PER MESSAGE · SINGLE THREAD' if part == 1 else 'STAMP → SIGNAL · TWO THREADS'
    a(f'<div class="meter" data-from="{frm[1]},{frm[2]}" data-to="{to[1]},{to[2]}" data-at="{at if at is not None else -1}" '
      f'data-la="{esc(frm[0])}" data-lb="{esc(to[0])}" style="left:1300px;top:100px">'
      f'<div class="mh">{hdr}</div><div class="mb"><span class="mlab"></span>'
      f'<span class="mk">p50</span><span class="mv m50"></span><span class="mk">p99</span><span class="mv m99"></span></div></div>')

def bar(label, val, x, y, scale, cue, color, d=0, txt=None, lw=300, h=46):
    a(f'<div class="brow" data-cue="{cue}" data-d="{d}" style="left:{x}px;top:{y}px"><div class="nm" style="width:{lw}px">{label}</div>'
      f'<div class="b grow" data-cue="{cue}" data-d="{d+0.2}" data-w="{max(4,int(val*scale))}" style="background:{color};height:{h}px"></div>'
      f'<div class="v" style="color:{color}">{txt or f(val) + " ns"}</div></div>')

V = {k: (k, ST[k][0], ST[k][1]) for k in ST}
LAB = {'v0': 'v0 naive', 'v1': 'v1 data', 'v1h': 'v1 table', 'v2a': 'v2a 4 acc', 'v2': 'v2 pipeline', 'v3': 'v3 branches', 'v4': 'v4 memory'}
def mv(k): return (LAB[k], ST[k][0], ST[k][1])

# ================================================================ title
scene('title')
a('<div class="eyebrow" data-cue="0" style="left:140px;top:170px">TRADING LAB · C++ LOW LATENCY INTERVIEW</div>')
a('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:225px;width:1700px">Optimize it live</div>')
a('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:390px;width:1600px">One market-data handler. Six steps. Every number measured.</div>')
steps = [('1', 'data structures', 'teal'), ('2', 'pipelining', 'blue'), ('3', 'branches', 'amber'), ('4', 'memory', 'green'),
         ('5', 'memory order', 'violet'), ('6', 'cache lines', 'pink')]
a('<svg class="full"><path class="draw" data-cue="1" data-dur="2.2" d="M 170 610 L 1760 610" stroke="#33464f" stroke-width="4" fill="none"/></svg>')
for k, (n, t, c) in enumerate(steps):
    x = 140 + k * 285
    a(f'<div class="stepc" data-cue="1" data-d="{0.2+0.3*k:.1f}" style="left:{x}px;top:560px;border-color:var(--{c})"><b style="background:var(--{c})">{n}</b>{t}</div>')
a('<div class="lbl" data-cue="1" data-d="0.2" style="left:140px;top:520px">PART 1 · ONE THREAD</div>')
a('<div class="lbl" data-cue="1" data-d="1.4" style="left:1280px;top:520px">PART 2 · TWO THREADS</div>')
a('<div class="tagx" data-cue="2" style="left:140px;top:720px;border-color:var(--green);color:var(--green)">✓ same signals, every version</div>')
a('<div class="tagx" data-cue="2" data-d="0.5" style="left:620px;top:720px;border-color:var(--teal);color:var(--teal)">p50 · p99 per message, never averages</div>')
end()

# ================================================================ snippet
scene('snippet')
h2('The snippet you are handed')
naive = [
    ('std::map<std::string, State> book;', {'hl': (2, 3)}),
    'int on_msg(const Msg& m) {',
    '  if (m.qty == 0) { ++invalid; return 0; }  // + price, side',
    ('  std::string sym(m.stock, 8);', {'hl': (2, 3)}),
    ('  State& s = book[sym];', {'hl': (2, 3)}),
    ('  if (m.type == \'Q\') {', {'hl': (1, 2)}),
    ('    if (m.side == \'B\') s.bid = m.price; else s.ask = m.price;', {'hl': (1, 2)}),
    ('  } else s.trades.push_back(Trade{sym, m.price, m.qty});', {'hl': (3, 4)}),
    ('  double pv = 0; uint64_t vol = 0;      // last 32 trades', {'hl': (4, None)}),
    ('  for (i = from; i < n; ++i) { pv += double(t[i].price) * t[i].qty; vol += t[i].qty; }', {'hl': (4, None)}),
    ('  double edge = (mid - pv / vol) / (s.ask - s.bid);', {'hl': (4, None)}),
    ('  if (edge > 0.25) return 1;', {'hl': (4, None)}),
    ('  if (edge < -0.25) return -1;', {'hl': (4, None)}),
    '  return 0;  }',
]
code(naive, 120, 210, 1640, cue=0, sm=True)
a('<div class="msgbox" data-cue="1" style="left:120px;top:780px">'
  '<div class="bytes">'
  '<div style="width:90px;background:var(--amber)">type</div><div style="width:90px;background:var(--amber)">side</div>'
  '<div style="width:150px;background:var(--teal)">locate</div><div style="width:150px;background:#7fb6c9">qty</div>'
  '<div style="width:260px;background:var(--green)">price ·1/10000 $</div><div style="width:260px;background:var(--violet)">stock[8]</div>'
  '<div style="width:260px;background:#55707f">ts</div></div></div>')
lbl('struct Msg · 32 bytes · ITCH-style: integer price, stock locate, 8-byte symbol', 120, 860, 1, 0.4)
end()

# ================================================================ measure
scene('measure')
h2('Measure before you touch it')
meter(mv('v0'))
code(['for (size_t i = 0; i < feed.size(); ++i) {',
      ('  uint64_t t0 = tsc_begin();      // lfence; rdtsc; lfence', {'hl': (1, 2)}),
      ('  int s = h.on_msg(feed[i]);', {'hl': (1, 2)}),
      ('  uint64_t t1 = tsc_end();        // rdtscp; lfence', {'hl': (1, 2)}),
      '  cycles[i] = uint32_t(t1 - t0);',
      '}',
      ('sort(cycles);  p50 = cycles[n/2];  p99 = cycles[n*99/100];', {'hl': (2, 3)})],
     120, 230, 1000, cue=1, sm=True, title='bench.cpp · 2,000,000 messages · 500 symbols')
# histogram
import math, random
random.seed(3)
bx, by, bw = 1180, 640, 640
hist = [2, 5, 14, 40, 78, 100, 82, 55, 36, 24, 16, 11, 8, 6, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1]
for k, hv in enumerate(hist):
    hh = int(hv * 2.6)
    col = 'var(--teal)' if k < 15 else 'var(--amber)'
    a(f'<div class="hbar" data-cue="2" data-d="{0.03*k:.2f}" style="left:{bx+k*26}px;top:{by-hh}px;height:{hh}px;background:{col}"></div>')
a(f'<div class="vline" data-cue="2" data-d="0.8" style="left:{bx+6*26+12}px;top:{by-300}px;height:300px;border-color:var(--teal)"></div>')
a(f'<div class="lbl c-teal" data-cue="2" data-d="0.9" style="left:{bx+6*26+20}px;top:{by-300}px">p50</div>')
a(f'<div class="vline" data-cue="2" data-d="1.1" style="left:{bx+19*26+12}px;top:{by-300}px;height:300px;border-color:var(--amber)"></div>')
a(f'<div class="lbl c-amber" data-cue="2" data-d="1.2" style="left:{bx+19*26+20}px;top:{by-300}px">p99</div>')
a(f'<div class="axis" data-cue="2" style="left:{bx}px;top:{by}px;width:{bw}px"></div>')
lbl('latency per message →', bx, by + 12, 2)
a('<div class="box amber" data-cue="3" style="left:120px;top:600px;width:480px"><div class="t">timer floor</div>'
  f'<div class="s">empty handler: p50 {ST["timer"][0]:.1f} ns</div><div class="s">inside every row below</div></div>')
a('<div class="term" data-cue="4" style="left:640px;top:600px;width:480px">$ ./test<br>'
  '<span class="c-green">v0 naive  … signals 204b86b2…</span><br><span class="c-green">v4 alloc  … signals 204b86b2…</span><br>'
  '<span class="c-muted">identical signals and final state</span></div>')
end()

# ================================================================ baseline
scene('baseline')
h2('Baseline: the naive handler')
meter(mv('v0'))
a('<div class="box" data-cue="0" style="left:120px;top:220px;width:760px"><div class="lbl">THE BOX</div>'
  '<div class="s" style="line-height:1.6;margin-top:8px">4 vCPU KVM guest · Intel Xeon @ 2.1 GHz<br>shared with other jobs · g++ 13.3 -O2<br>thread pinned to CPU 2 · chrt -f 10 (SCHED_FIFO)</div></div>')
a(f'<div class="bign c-red" data-cue="1" style="left:980px;top:230px"><span class="count" data-cue="1" data-from="0" data-to="{ST["v0"][0]:.0f}" data-dur="1.2">0</span></div>')
a('<div class="lbl" data-cue="1" data-d="0.3" style="left:990px;top:390px">ns · p50</div>')
a(f'<div class="bign c-amber" data-cue="1" data-d="0.8" style="left:1380px;top:230px"><span class="count" data-cue="1" data-d="0.8" data-from="0" data-to="{ST["v0"][1]:.0f}" data-dur="1.2">0</span></div>')
a('<div class="lbl" data-cue="1" data-d="1.1" style="left:1390px;top:390px">ns · p99</div>')
sus = [('1', 'std::map&lt;std::string&gt; lookup', 'teal'), ('2', 'std::string built per message', 'teal'),
       ('3', 'history vector: push_back', 'green'), ('4', '32-step loop, one accumulator', 'blue'), ('5', 'two double divides', 'blue')]
for k, (n, t, c) in enumerate(sus):
    a(f'<div class="sus" data-cue="{2 if k == 0 else 3}" data-d="{0.35*k:.2f}" style="left:{120+ (k%3)*580}px;top:{520 + (k//3)*110}px;border-color:var(--{c})"><b style="background:var(--{c})">{n}</b>{t}</div>')
foot(1, 800, 0.6)
end()

# ================================================================ ds-map
scene('ds-map')
h2('Step 1 · a tree of strings → a flat array')
meter(mv('v0'))
# tree
nodes = {'MSFT': (520, 230), 'GOOG': (330, 340), 'TSLA': (710, 340), 'AMD': (230, 450), 'IBM': (430, 450), 'NVDA': (610, 450),
         'XOM': (810, 450), 'AAPL': (180, 560), 'INTC': (380, 560), 'JPM': (480, 660)}
edges = [('MSFT', 'GOOG'), ('MSFT', 'TSLA'), ('GOOG', 'AMD'), ('GOOG', 'IBM'), ('TSLA', 'NVDA'), ('TSLA', 'XOM'), ('AMD', 'AAPL'), ('IBM', 'INTC'), ('INTC', 'JPM')]
svg = ['<svg class="full">']
for p_, c_ in edges:
    (x1, y1), (x2, y2) = nodes[p_], nodes[c_]
    svg.append(f'<path class="draw" data-cue="1" data-dur="0.6" d="M {x1} {y1+29} L {x2} {y2+29}" stroke="#4a3f73" stroke-width="3" fill="none"/>')
svg.append('<path id="dsm-chase" d="M 520 259 L 330 369 L 430 479 L 380 589 L 480 689" fill="none" stroke="none"/>')
svg.append('</svg>')
a(''.join(svg))
for k, (n, (x, y)) in enumerate(nodes.items()):
    hl = ' data-hl="2" data-hlend="3"' if n in ('MSFT', 'GOOG', 'IBM', 'INTC', 'JPM') else ''
    a(f'<div class="node" data-cue="1" data-d="{0.05*k:.2f}"{hl} style="left:{x-50}px;top:{y}px">{n}</div>')
a('<div class="pkt" data-path="dsm-chase" data-cue="1.5" data-dur="2.4" data-loop="1" data-out="3" style="background:var(--violet);box-shadow:0 0 16px var(--violet)"></div>')
lbl('find "JPM": 5 hops, 5 string compares,<br>each hop a dependent load', 120, 740, 2, 0.3, 700, 'c-violet', 'data-out="end"')
# array
a('<div class="lbl" data-cue="4" style="left:1000px;top:230px">st[m.locate] · one multiply-add, one load</div>')
for k in range(10):
    hit = k == 6
    a(f'<div class="acell{" hit" if hit else ""}" data-cue="4" data-d="{0.05*k:.2f}" style="left:{1000+k*84}px;top:270px">{k+1 if k<9 else "…"}</div>')
a('<div class="tagx" data-cue="4" data-d="0.7" style="left:1490px;top:350px;border-color:var(--teal);color:var(--teal)">locate = 7</div>')
a('<div class="bytes" data-cue="3" style="left:1000px;top:450px">'
  '<div style="width:110px;background:var(--amber)">type</div><div style="width:190px;background:var(--teal)">stock locate</div>'
  '<div style="width:170px;background:#55707f">tracking</div><div style="width:270px;background:#3d5563;color:#cfe">timestamp (6)</div></div>')
lbl('ITCH 5.0 header · locate: 2 bytes at offset 1 · lab BookBuilder indexes by it', 1000, 530, 3, 0.3, 840)
code([('std::map<std::string, State> book;', {'dele': 4}),
      ('State& s = book[std::string(m.stock, 8)];', {'dele': 4}),
      ('std::vector<State> st(512);', {'add': 4.3}),
      ('State& s = st[m.locate];', {'add': 4.6})], 1000, 610, 820, cue=4, sm=True)
end()

# ================================================================ ds-layout
scene('ds-layout')
h2('Hot fields in one cache line')
meter(mv('v0'), mv('v1'), 3)
lbl('BEFORE · one std::map node', 120, 210, 0)
a('<div class="bytes" data-cue="0" data-d="0.2" style="left:120px;top:245px">'
  '<div style="width:180px;background:#55707f">tree links 32</div><div style="width:180px;background:var(--violet)">key string 32</div>'
  '<div style="width:180px;background:#7fb6c9">symbol 32</div><div style="width:90px;background:var(--teal)">bid ask</div>'
  '<div style="width:135px;background:var(--green)">trades 24</div><div style="width:45px;background:var(--amber)">upd</div></div>')
lbl('144 bytes, wherever malloc put it · 3 cache lines', 120, 325, 0, 0.4)
lbl('AFTER · alignas(64) State, one line', 120, 410, 1)
a('<div class="bytes" data-cue="1" data-d="0.2" style="left:120px;top:445px">'
  '<div style="width:90px;background:var(--teal)">bid 8</div><div style="width:90px;background:var(--teal)">ask 8</div>'
  '<div style="width:270px;background:var(--green)">trades 24</div><div style="width:90px;background:var(--amber)">upd 8</div>'
  '<div style="width:180px;background:#26363f;color:#8ea3b1">pad 16</div></div>')
a('<div class="cline" data-cue="1" data-d="0.5" style="left:120px;top:525px;width:720px">64 bytes · static_assert(sizeof(State) == 64)</div>')
a('<div class="box" data-cue="2" style="left:120px;top:600px;width:720px"><div class="t" style="font-size:26px">cold: std::vector&lt;std::string&gt; names(512)</div>'
  '<div class="s">read when printing, never per message</div></div>')
SC = 2.2
bar('v0 map', ST['v0'][0], 940, 260, SC, 3, 'var(--red)', lw=200)
bar('v1 array', ST['v1'][0], 940, 330, SC, 3, 'var(--teal)', d=0.4, lw=200)
bar('v1 hash table', ST['v1h'][0], 940, 400, SC, 4, 'var(--blue)', d=0.6, lw=200)
lbl('p50 per message', 1150, 220, 3)
code(['uint64_t k; memcpy(&k, m.stock, 8);         // 8 bytes = 1 key',
      'size_t i = (k * 0x9E3779B97F4A7C15) >> 54;   // 1024 slots',
      'while (keys[i] != k) i = (i + 1) & 1023;    // linear probe'],
     940, 520, 900, cue=4, d=0.3, sm=True)
lbl(f'p99: v0 {f(ST["v0"][1])} · v1 {f(ST["v1"][1])} · table {f(ST["v1h"][1])} ns', 940, 690, 4, 1.0)
foot(3, 870, 0.8)
end()

# ================================================================ pipeline
scene('pipeline')
h2('Step 2 · the pipeline')
meter(mv('v1'))
stg = [('F', 'var(--blue)'), ('D', 'var(--violet)'), ('E', 'var(--amber)'), ('R', 'var(--green)')]
lbl('F fetch · D decode · E execute · R retire', 120, 200, 1)
# independent instructions: staircase, one per cycle
X0, Y0, CW, RH = 380, 290, 62, 54
lbl('INDEPENDENT', 120, 255, 3, 0, None, 'c-teal')
ind = ['add  r1', 'mul  r2', 'add  r3', 'mov  r4']
for r, nm in enumerate(ind):
    a(f'<div class="iname" data-cue="1" data-d="{0.15*r:.2f}" style="left:120px;top:{Y0+r*RH}px">{nm}</div>')
    for s_, (st_, col) in enumerate(stg):
        a(f'<div class="pc" data-cue="{1 if s_ < 2 else 3}" data-d="{0.15*(r+s_):.2f}" style="left:{X0+(r+s_)*CW}px;top:{Y0+r*RH}px;background:{col}">{st_}</div>')
lbl('one result per cycle: the work overlaps', X0 + 8 * CW, Y0 + 70, 3, 0.8, 520, 'c-teal')
# dependent chain
Y1 = 590
lbl('DEPENDENT · each needs the last result', 120, 545, 4, 0, None, 'c-red')
dep = ['add  x, a', 'add  x, b', 'add  x, c', 'add  x, d']
lat = 3
for r, nm in enumerate(dep):
    a(f'<div class="iname" data-cue="4" data-d="{0.15*r:.2f}" style="left:120px;top:{Y1+r*RH}px">{nm}</div>')
    e0 = 2 + r * lat
    a(f'<div class="pc" data-cue="4" data-d="{0.15*r:.2f}" style="left:{X0+r*CW}px;top:{Y1+r*RH}px;background:var(--blue)">F</div>')
    a(f'<div class="pc" data-cue="4" data-d="{0.15*r+0.1:.2f}" style="left:{X0+(r+1)*CW}px;top:{Y1+r*RH}px;background:var(--violet)">D</div>')
    if e0 > r + 2:
        a(f'<div class="pw" data-cue="5" data-d="{0.3*r:.2f}" style="left:{X0+(r+2)*CW}px;top:{Y1+r*RH}px;width:{(e0-r-2)*CW-6}px">wait</div>')
    a(f'<div class="pc" data-cue="5" data-d="{0.3*r+0.1:.2f}" style="left:{X0+e0*CW}px;top:{Y1+r*RH}px;width:{lat*CW-6}px;background:var(--amber)">E</div>')
    a(f'<div class="pc" data-cue="5" data-d="{0.3*r+0.2:.2f}" style="left:{X0+(e0+lat)*CW}px;top:{Y1+r*RH}px;background:var(--green)">R</div>')
svg = ['<svg class="full">']
for r in range(3):
    e0 = 2 + r * lat
    x1 = X0 + (e0 + lat) * CW - 8; y1 = Y1 + r * RH + 44; x2 = X0 + (e0 + lat) * CW + 4; y2 = Y1 + (r + 1) * RH + 8
    svg.append(f'<path class="draw" data-cue="5" data-d="{0.3*r+0.3:.2f}" d="M {x1} {y1} L {x2} {y2}" stroke="var(--red)" stroke-width="3" fill="none" marker-end="url(#ah-red)"/>')
svg.append('</svg>'); a(''.join(svg))
lbl('time = chain length × latency', X0 + 16 * CW, Y1 + 120, 5, 1.2, 380, 'c-red')
end()

# ================================================================ chain
scene('chain')
h2('One chain, or four?')
meter(mv('v1'), mv('v2a'), 4)
code([('double pv = 0;', {'dele': 1}),
      ('for (; i < n; ++i) pv += double(t[i].price) * t[i].qty;', {'dele': 1}),
      ('double p0 = 0, p1 = 0, p2 = 0, p3 = 0;', {'add': 1.2}),
      ('for (; i + 4 <= n; i += 4) {', {'add': 1.5}),
      ('  p0 += double(t[i].price) * t[i].qty;   // ... p1, p2, p3', {'add': 1.8}),
      ('}  pv = (p0 + p1) + (p2 + p3);', {'add': 2.2})], 120, 210, 1060, cue=0, sm=True)
# chain diagrams
for k in range(8):
    a(f'<div class="cn red" data-cue="0" data-d="{0.12*k:.2f}" style="left:{1260+k*72}px;top:240px">+</div>')
a('<svg class="full">' + ''.join(f'<path class="draw" data-cue="0" data-d="{0.12*k+0.1:.2f}" d="M {1260+k*72+52} 266 L {1260+(k+1)*72} 266" stroke="var(--red)" stroke-width="3" fill="none"/>' for k in range(7)) + '</svg>')
lbl('1 chain: 32 adds in a row', 1260, 300, 0, 0.6, None, 'c-red')
for r in range(4):
    for k in range(2):
        a(f'<div class="cn teal" data-cue="1" data-d="{0.4+0.1*(r+k):.2f}" style="left:{1260+k*72}px;top:{350+r*44}px;width:40px;height:40px;font-size:22px">+</div>')
lbl('4 chains of 8, in parallel', 1430, 410, 1, 0.8, 380, 'c-teal')
SC = 14
lbl('ISOLATED · data in L1 · per 32-trade window', 120, 520, 3)
bar('1 chain', N['ilpv'][0], 120, 560, SC, 3, 'var(--red)', d=0.2, lw=200, txt=N['ilp'][0] + ' ns')
bar('4 chains', N['ilpv'][1], 120, 625, SC, 3, 'var(--teal)', d=0.5, lw=200, txt=N['ilp'][1] + ' ns')
lbl('IN THE HANDLER · p50 per message', 120, 710, 4)
bar('v1', ST['v1'][0], 120, 750, 3.2, 4, 'var(--red)', d=0.2, lw=200)
bar('v2a', ST['v2a'][0], 120, 815, 3.2, 4, 'var(--teal)', d=0.5, lw=200)
code(['.L64:',
      '  addq      $48, %rax          # 48-byte Trade',
      ('  cvtsi2sdq -48(%rax), %xmm0   # convert price', {'hl': (5, None)}),
      ('  cvtsi2sdq %rdx, %xmm2        # convert qty', {'hl': (5, None)}),
      '  mulsd     %xmm2, %xmm0',
      ('  addsd     %xmm0, %xmm1        # the chain', {'hl': (0, 1)}),
      '  jne       .L64'], 1060, 600, 780, cue=5, lang='asm', sm=True, title='v1 loop · g++ -O2 -S (trimmed)')
end()

# ================================================================ divide
scene('divide')
h2('Delete the chain, drop the divide')
meter(mv('v2a'), mv('v2'), 6)
code([('for (...) { pv += ...; vol += ...; }    // every message', {'dele': 1}),
      ('s.pv += m.price * m.qty;  s.vol += m.qty;        // new trade', {'add': 1.2}),
      ('s.pv -= old.price * old.qty;  s.vol -= old.qty;  // 33rd back', {'add': 1.6}),
      ('double edge = (mid - pv / vol) / (ask - bid);', {'dele': 5}),
      ('if (edge > 0.25) ...  // edge > 1/4 <=> ...', {'dele': 5}),
      ('int64_t lhs = 2 * ((bid + ask) * vol - 2 * pv);', {'add': 5.2}),
      ('int64_t rhs = (ask - bid) * vol;   if (lhs > rhs) ...', {'add': 5.6})], 120, 200, 1060, cue=0, sm=True)
code([('  divsd   %xmm2, %xmm1     # pv / vol', {'hl': (3, 5)}),
      ('  subsd   %xmm1, %xmm0     # mid - vwap', {'hl': (3, 5)}),
      '  cvtsi2sdq %r8, %xmm1',
      ('  divsd   %xmm1, %xmm0     # / spread', {'hl': (3, 5)}),
      '  comisd  .LC3(%rip), %xmm0',
      '  ja      .L21'], 1240, 250, 620, cue=3, lang='asm', sm=True, title='v1 · g++ -O2 -S')
# latency timeline: div -> sub -> div
TX, TY, CY = 120, 640, 26
lbl('CRITICAL PATH · cycles (typical recent Intel)', TX, TY - 50, 4)
seg = [('divsd ~13–15', 14, 'var(--red)'), ('sub', 3, 'var(--amber)'), ('divsd ~13–15', 14, 'var(--red)'), ('cmp', 2, 'var(--amber)')]
x = TX
for k, (t, c, col) in enumerate(seg):
    a(f'<div class="tl" data-cue="4" data-d="{0.35*k:.2f}" style="left:{x}px;top:{TY}px;width:{c*CY-4}px;background:{col}">{t}</div>')
    x += c * CY
xi = TX
for k, (t, c) in enumerate([('imul', 3), ('', 1), ('imul', 3), ('', 1)]):
    a(f'<div class="tl" data-cue="5" data-d="{0.25*k:.2f}" style="left:{xi}px;top:{TY+70}px;width:{c*CY-4}px;background:var(--teal)">{t}</div>')
    xi += c * CY
SC = 14
bar('divide path', N['divv'][0], 1240, 560, SC, 5, 'var(--red)', d=0.6, lw=220, txt=N['div'][0] + ' ns')
bar('cross-multiply', N['divv'][1], 1240, 625, SC, 5, 'var(--teal)', d=0.9, lw=220)
lbl('isolated, dependent calls', 1240, 690, 5, 1.0)
a(f'<div class="box teal" data-cue="6" style="left:1240px;top:760px;width:600px"><div class="t">v2 · p50 {f(ST["v2"][0])} ns</div><div class="s">p99 {f(ST["v2"][1])} ns · same signals, all integers</div></div>')
end()

# ================================================================ predict
scene('predict')
h2('Step 3 · which branches are random?')
meter(mv('v2'))
a('<div class="box amber" data-cue="1" style="left:120px;top:230px;width:330px"><div class="t">branch</div><div class="s">cmp · je .L275</div></div>')
a('<svg class="full">'
  '<path class="draw" data-cue="1" data-d="0.4" d="M 450 270 C 520 270 520 220 600 220 L 1000 220" stroke="var(--teal)" stroke-width="4" fill="none"/>'
  '<path class="draw" data-cue="2" data-d="0.3" d="M 450 310 C 520 310 520 360 600 360 L 1000 360" stroke="var(--green)" stroke-width="4" fill="none"/></svg>')
lbl('guessed path · fetched ahead', 1030, 208, 1, 0.5, None, 'c-teal')
a('<div class="flush" data-cue="2" data-anim="scale" style="left:590px;top:196px;width:420px;height:50px">FLUSHED</div>')
lbl('real path · refetched · 15–20 cycles typical', 1030, 348, 2, 0.6, 700, 'c-green')
random.seed(11)
rows = [('validation', [1 if random.random() > 0.01 else 0 for _ in range(28)], 3, 'predictable: ~1% fail'),
        ('bid or ask', [random.randint(0, 1) for _ in range(28)], 4, '50 / 50'),
        ('quote or trade', [1 if random.random() < 0.7 else 0 for _ in range(28)], 4, '70 / 30'),
        ('signal', [random.choice([0, 1, 2]) for _ in range(28)], 4.5, '40 / 20 / 40')]
for k, (nm, bits, cue, note) in enumerate(rows):
    y = 500 + k * 85
    a(f'<div class="rname" data-cue="{cue}" style="left:120px;top:{y}px">{nm}</div>')
    for j, b in enumerate(bits):
        col = ['#2a3a45', 'var(--green)', 'var(--amber)'][b]
        a(f'<div class="bit" data-cue="{cue}" data-d="{0.02*j:.2f}" style="left:{440+j*36}px;top:{y}px;background:{col}"></div>')
    good = k == 0
    a(f'<div class="tagx" data-cue="{cue}" data-d="0.7" style="left:1470px;top:{y+2}px;border-color:var(--{"green" if good else "red"});color:var(--{"green" if good else "red"})">{note}</div>')
end()

# ================================================================ branchless
scene('branchless')
h2('Branches into data, then read the asm')
meter(mv('v2'), mv('v3'), 6)
code([('if (m.side == \'B\') s.bid = m.price; else s.ask = m.price;', {'dele': 1}),
      ('s.px[m.side == \'S\'] = m.price;          // px[0] bid, px[1] ask', {'add': 1.2}),
      ('if (lhs > rhs) return 1;  if (lhs < -rhs) return -1;', {'dele': 2}),
      ('int sig = (lhs > rhs) - (lhs < -rhs);    // +1, 0, -1', {'add': 2.2}),
      ('bool ok = (m.qty != 0) & (m.price > 0) & ((m.side == \'B\') | (m.side == \'S\'));', {'add': 2.6})],
     120, 200, 1680, cue=0, sm=True)
code([('  cmpb  $66, 1(%rbx)', {'hl': (4, 5)}),
      ('  je    .L275           # bid or ask?', {'hl': (4, 5)}),
      '  ...',
      ('  cmpq  %rdx, %rcx', {'hl': (4, 5)}),
      ('  jg    .L203           # buy?', {'hl': (4, 5)})], 120, 500, 780, cue=3, lang='asm', sm=True, title='v2 · g++ -O2 -S · jumps')
code([('  cmpb  $83, 1(%rbp)', {'hl': (5, 6)}),
      ('  sete  %al', {'hl': (5, 6)}),
      ('  movq  %rdx, (%rbx,%rax,8)  # px[side]', {'hl': (5, 6)}),
      '  ...',
      ('  setg  %dl  ·  setg %cl', {'hl': (5, 6)}),
      ('  subl  %ecx, %eax        # buy - sell', {'hl': (5, 6)})], 1000, 500, 820, cue=5, lang='asm', sm=True, title='v3 · g++ -O2 -S · no jumps')
a(f'<div class="tagx" data-cue="6" style="left:120px;top:830px;border-color:var(--green);color:var(--green)">p50 {f(ST["v2"][0])} → {f(ST["v3"][0])} ns · p99 {f(ST["v2"][1])} → {f(ST["v3"][1])} ns</div>')
end()

# ================================================================ hidden
scene('hidden')
h2('Step 4 · count the allocations')
meter(mv('v3'))
code(['void* operator new(std::size_t n) {',
      ('  if (g_count_allocs) ++g_allocs;', {'hl': (1, 2)}),
      '  return std::malloc(n);   // + bad_alloc',
      '}'], 120, 200, 760, cue=1, sm=True)
a('<div class="ctr" data-cue="2" style="left:960px;top:200px"><div class="lbl">ALLOCATIONS PER RUN · 2M MESSAGES</div>'
  f'<div class="row"><span>v0 naive</span><b class="c-red"><span class="count" data-cue="2" data-from="0" data-to="{N["allocs"][0]}" data-dur="1.4">0</span></b></div>'
  f'<div class="row"><span>v1 – v3</span><b class="c-amber"><span class="count" data-cue="2" data-d="0.4" data-from="0" data-to="{N["allocs"][1]}" data-dur="1.4">0</span></b></div></div>')
lbl('500 map nodes + 500 vectors × 12 buffers (capacity 1 → 2048)', 960, 430, 2, 1.0, 860)
# vector growth
caps = [1, 2, 4, 8, 16, 32, 64]
x = 120
for k, cp in enumerate(caps):
    w = 14 + cp * 6
    a(f'<div class="vg" data-cue="3" data-d="{0.3*k:.2f}" style="left:{x}px;top:520px;width:{w}px"></div>')
    a(f'<div class="lbl" data-cue="3" data-d="{0.3*k:.2f}" style="left:{x}px;top:580px">{cp}</div>')
    x += w + 26
lbl('capacity doubles: new buffer · move every Trade · free the old one', 120, 625, 3, 1.6, 1100, 'c-amber')
a(f'<div class="box red" data-cue="4" style="left:120px;top:700px;width:760px"><div class="t">the tail, not the median</div>'
  f'<div class="s">v3: p50 {f(ST["v3"][0])} ns · p99 {f(ST["v3"][1])} ns · p99.9 {ST["v3"][2]:,.0f} ns</div></div>')
a('<div class="box violet" data-cue="6" style="left:960px;top:700px;width:860px"><div class="t" style="font-size:27px">std::string sym(m.stock, 8)</div>'
  '<div class="s">8 chars ≤ 15: libstdc++ small-string buffer, no malloc</div></div>')
end()

# ================================================================ prealloc
scene('prealloc')
h2('A fixed window, allocated once')
meter(mv('v3'), mv('v4'), 4)
code(['struct alignas(64) State {',
      '  int64_t  px[2], pv, vol;  uint64_t updates;',
      '  uint32_t n;                 // trades seen',
      ('  int64_t  win_pv[32];        // price*qty', {'hl': (0, 1)}),
      ('  uint32_t win_q[32];', {'hl': (0, 1)}),
      '};                            // 448 bytes',
      ('uint32_t k = s.n++ & 31;      // oldest slot', {'hl': (0, 2)}),
      ('s.pv  += add - s.win_pv[k];   // evict + add', {'hl': (0, 2)}),
      ('s.win_pv[k] = add;  s.win_q[k] = m.qty;', {'hl': (0, 2)}),
      ('st = new State[512];          // once, at startup', {'hl': (2, 3)})], 120, 200, 900, cue=0, sm=True)
# ring of 32 slots
import math as _m
cx, cy, R = 1420, 430, 160
for k in range(32):
    ang = -_m.pi / 2 + 2 * _m.pi * k / 32
    a(f'<div class="slot" id="pa-s{k}" data-cue="0" data-d="{0.02*k:.2f}" style="left:{cx+R*_m.cos(ang)-15:.0f}px;top:{cy+R*_m.sin(ang)-15:.0f}px"></div>')
a(f'<div class="lbl" data-cue="0" data-d="0.6" style="left:{cx-80}px;top:{cy-14}px;width:160px;text-align:center">32 slots</div>')
a(f'<div class="ctr" data-cue="3" style="left:1180px;top:640px;width:640px"><div class="row"><span>allocations / run</span><b class="c-green">{N["allocs"][2]}</b></div></div>')
bar('p99 v3', ST['v3'][1], 120, 720, 2.6, 4, 'var(--red)', lw=170)
bar('p99 v4', ST['v4'][1], 120, 785, 2.6, 4, 'var(--green)', d=0.4, lw=170)
a(f'<div class="tagx" data-cue="5" style="left:1000px;top:770px;border-color:var(--green);color:var(--green)">p99.9: {ST["v3"][2]:,.0f} → {f(ST["v4"][2])} ns</div>')
end()

# ================================================================ part1
scene('part1')
h2('Part 1: one thread, same output')
meter(mv('v4'))
rows = [('v0 naive', 'v0', 'var(--red)'), ('1 data structures', 'v1', 'var(--teal)'), ('2 four accumulators', 'v2a', 'var(--blue)'),
        ('2 running sums', 'v2', 'var(--blue)'), ('3 branchless', 'v3', 'var(--amber)'), ('4 no allocation', 'v4', 'var(--green)')]
SC = 2.0
lbl('p50', 520, 205, 1); lbl('p99', 1180, 205, 1)
for k, (nm, key, col) in enumerate(rows):
    y = 245 + k * 82
    a(f'<div class="rname" data-cue="1" data-d="{0.25*k:.2f}" style="left:120px;top:{y}px;width:380px">{nm}</div>')
    a(f'<div class="grow bar" data-cue="1" data-d="{0.25*k+0.1:.2f}" data-w="{int(ST[key][0]*SC)}" style="left:520px;top:{y}px;height:44px;background:{col}"></div>')
    a(f'<div class="val" data-cue="1" data-d="{0.25*k+0.4:.2f}" style="left:{530+int(ST[key][0]*SC)}px;top:{y+4}px;color:{col}">{f(ST[key][0])}</div>')
    w = int(ST[key][1] * 1.0)
    a(f'<div class="grow bar" data-cue="1" data-d="{0.25*k+0.2:.2f}" data-w="{w}" style="left:1180px;top:{y}px;height:44px;background:{col};opacity:.8"></div>')
    a(f'<div class="val" data-cue="1" data-d="{0.25*k+0.5:.2f}" style="left:{1190+w}px;top:{y+4}px;color:{col}">{f(ST[key][1])}</div>')
tf = int(ST['timer'][0] * SC)
a(f'<div class="vline" data-cue="2" style="left:{520+tf}px;top:235px;height:500px;border-color:var(--muted);border-left-style:dashed"></div>')
lbl(f'timer floor {ST["timer"][0]:.1f} ns', 520 + tf + 10, 745, 2, 0.2, 400)
foot(1, 800, 1.5, FOOT + ' · ns per message')
end()

# ================================================================ split
scene('split')
h2('Part 2 · split into two threads')
meter(('v4 one thread', ST['v4'][0], ST['v4'][1]), part=2)
a('<div class="core teal" data-cue="1" style="left:120px;top:300px"><div class="t">feed thread</div><div class="s">CPU 1</div></div>')
a('<div class="core violet" data-cue="3" style="left:1280px;top:300px"><div class="t">strategy thread</div><div class="s">CPU 2 · v4 handler</div></div>')
a('<div class="qbox" data-cue="2" style="left:700px;top:320px">handoff ?</div>')
a('<svg class="full"><path id="sp-a" class="draw" data-cue="2" d="M 560 370 L 690 370" stroke="var(--teal)" stroke-width="4" fill="none" marker-end="url(#ah-teal)"/>'
  '<path id="sp-b" class="draw" data-cue="3" d="M 1130 370 L 1270 370" stroke="var(--violet)" stroke-width="4" fill="none" marker-end="url(#ah-violet)"/>'
  '<path id="sp-run" d="M 340 470 L 1500 470" fill="none" stroke="none"/></svg>')
a('<div class="pkt" data-path="sp-run" data-cue="2" data-dur="2.4" data-loop="1" style="background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>')
a('<div class="tagx" data-cue="2" style="left:120px;top:520px;border-color:var(--amber);color:var(--amber)">m.ts = rdtsc()</div>')
a('<div class="tagx" data-cue="4" style="left:1280px;top:520px;border-color:var(--amber);color:var(--amber)">latency = rdtscp() − m.ts</div>')
a('<svg class="full"><path class="draw" data-cue="4" data-d="0.3" d="M 200 600 L 1680 600" stroke="var(--amber)" stroke-width="3" fill="none" marker-end="url(#ah-amber)" marker-start="url(#ah-amber)"/></svg>')
lbl('stamp → signal, per message', 820, 615, 4, 0.5, None, 'c-amber')
a(f'<div class="box" data-cue="5" style="left:120px;top:690px;width:820px"><div class="s" style="line-height:1.6">1 message every 1 µs · 200k per run · 21 runs, interleaved<br>both threads pinned · SCHED_FIFO · median of runs</div></div>')
a(f'<div class="box" data-cue="5" data-d="0.4" style="left:1000px;top:690px;width:820px"><div class="s" style="line-height:1.6">TSCs in step? ping-pong one-way, both directions:<br>{N["tsc"][0]} ns and {N["tsc"][1]} ns → same clock</div></div>')
end()

# ================================================================ mutex
scene('mutex')
h2('Step 5 · the obvious handoff')
meter(('v4 one thread', ST['v4'][0], ST['v4'][1]), ('mutex + cv', M50, M99), 3, part=2)
code(['void push(const Msg& m) {',
      ('  { std::lock_guard g(mu); q.push(m); }', {'hl': (0, 1)}),
      ('  cv.notify_one();', {'hl': (2, 3)}),
      '}',
      'void pop_wait(Msg& out) {',
      '  std::unique_lock g(mu);',
      ('  cv.wait(g, [&] { return !q.empty(); });', {'hl': (1, 3)}),
      '  out = q.front(); q.pop();',
      '}'], 120, 210, 900, cue=0, sm=True)
a('<div class="core violet" data-cue="1" style="left:1150px;top:230px;width:300px"><div class="t">strategy</div><div class="s">asleep in futex</div></div>')
a('<div class="core" data-cue="2" style="left:1150px;top:430px;width:640px;border-color:var(--red)"><div class="t">kernel</div><div class="s">futex wake · scheduler · context switch</div></div>')
a('<svg class="full"><path class="draw" data-cue="2" data-d="0.3" d="M 1300 330 L 1300 425" stroke="var(--red)" stroke-width="3" fill="none" marker-end="url(#ah-red)" marker-start="url(#ah-red)"/></svg>')
a(f'<div class="bign c-red" data-cue="3" style="left:1150px;top:600px;font-size:110px">{us(M50)} µs</div>')
lbl('p50', 1160, 720, 3, 0.2)
a(f'<div class="bign c-red" data-cue="3" data-d="0.4" style="left:1580px;top:600px;font-size:110px">{M99/1000:.0f} µs</div>')
lbl('p99', 1590, 720, 3, 0.6)
a(f'<div class="tagx" data-cue="4" style="left:120px;top:640px;border-color:var(--muted);color:#cfdbe2">the work: ~{f(ST["v4"][0]-ST["timer"][0])} ns</div>')
foot(3, 820, 0.8, f'p50 over 21 runs ranged {us(MT["mutex"][4])}–{us(MT["mutex"][5])} µs: wake-up time depends on what else the box is running')
end()

# ================================================================ flag
scene('flag')
h2('"Just use a bool"')
code(['Msg slot;',
      'bool ready = false;',
      ('void publish(const Msg& m) {  // feed', {'hl': (1, 2)}),
      ('  slot = m;', {'hl': (4, 5)}),
      ('  ready = true;', {'hl': (4, 5)}),
      '}',
      ('int64_t consume() {           // strategy', {'hl': (1, 2)}),
      ('  while (!ready) {}', {'hl': (5, None)}),
      '  ready = false;',
      '  return slot.price;',
      '}'], 120, 200, 760, cue=0, sm=True, title='broken.cpp')
a('<div class="tagx" data-cue="2" style="left:120px;top:720px;border-color:var(--red);color:var(--red)">data race → undefined behaviour</div>')
code(['_Z7publishRK3Msg:',
      '  movdqu  (%rdi), %xmm0',
      ('  movb    $1, ready(%rip)      # flag first!', {'hl': (4, 5)}),
      ('  movaps  %xmm0, slot(%rip)', {'hl': (4, 5)}),
      '  movdqu  16(%rdi), %xmm1',
      '  movaps  %xmm1, 16+slot(%rip)',
      '  ret',
      '_Z7consumev:',
      ('  movb    $0, ready(%rip)      # no loop', {'hl': (5, None)}),
      ('  movq    8+slot(%rip), %rax', {'hl': (5, None)}),
      '  ret'], 980, 200, 820, cue=3, lang='asm', sm=True, title='g++ 13.3 -O2 -S, real output')
end()

# ================================================================ reorder
scene('reorder')
h2('Who reorders memory?')
a('<div class="box blue" data-cue="1" style="left:120px;top:220px;width:520px"><div class="t">compiler</div><div class="s">any move one thread cannot see</div></div>')
a('<div class="box pink" data-cue="2" style="left:120px;top:400px;width:520px"><div class="t">CPU</div><div class="s">store buffer · loads run ahead</div></div>')
for k, t in enumerate(['slot.price = p', 'slot.qty = q', 'ready = true']):
    a(f'<div class="sbq" data-cue="2" data-d="{0.3+0.2*k:.1f}" style="left:150px;top:{520+k*56}px">{t}</div>')
lbl('STORE BUFFER → L1 → other cores', 150, 700, 2, 0.9)
rows = [('load → later load', 'kept', 'may reorder'), ('store → later store', 'kept', 'may reorder'),
        ('load → later store', 'kept', 'may reorder'), ('store → later load', 'may reorder', 'may reorder')]
a('<div class="colh c-teal" data-cue="3" style="left:1150px;top:220px">x86-64 · TSO</div>')
a('<div class="colh c-violet" data-cue="4" style="left:1500px;top:220px">ARM · AArch64</div>')
for k, (pr, x8, ar) in enumerate(rows):
    y = 290 + k * 100
    a(f'<div class="pair" data-cue="3" data-d="{0.1*k:.1f}" style="left:720px;top:{y}px">{pr}</div>')
    ok = x8 == 'kept'
    a(f'<div class="cellx {"ok" if ok else "bad"}" data-cue="3" data-d="{0.2+0.1*k:.1f}" style="left:1150px;top:{y}px">{x8}</div>')
    a(f'<div class="cellx bad" data-cue="4" data-d="{0.1*k:.1f}" style="left:1500px;top:{y}px">{ar}</div>')
lbl('accesses to different addresses, without barriers or dependencies', 720, 700, 4, 0.8, 1100)
end()

# ================================================================ acqrel
scene('acqrel')
h2('Release and acquire: happens-before')
a('<div class="lane teal" data-cue="0" style="left:120px;top:200px">feed thread</div>')
a('<div class="lane violet" data-cue="0" style="left:1000px;top:200px">strategy thread</div>')
a('<div class="op" data-cue="0" data-d="0.3" style="left:120px;top:270px;border-color:var(--teal)">slot = m;</div>')
a('<div class="op strong" data-cue="0" data-d="0.5" style="left:120px;top:370px;border-color:var(--amber)">ready.store(true, <span class="c-amber">release</span>);</div>')
lbl('▲ nothing above may sink below', 120, 445, 0, 0.8, None, 'c-amber')
a('<div class="op strong" data-cue="0" data-d="0.7" style="left:1000px;top:370px;border-color:var(--amber)">while (!ready.load(<span class="c-amber">acquire</span>)) {}</div>')
lbl('▼ nothing below may rise above', 1000, 445, 0, 1.0, None, 'c-amber')
a('<div class="op" data-cue="0" data-d="0.9" style="left:1000px;top:490px;border-color:var(--violet)">use(slot.price);</div>')
a('<svg class="full">'
  '<path class="draw" data-cue="1" data-d="0.2" data-dur="1.2" d="M 760 400 L 990 400" stroke="var(--amber)" stroke-width="6" fill="none" marker-end="url(#ah-amber)"/>'
  '<path class="draw" data-cue="2" data-d="0.2" data-dur="1.3" d="M 420 300 C 800 300 760 520 990 520" stroke="var(--green)" stroke-width="3" fill="none" marker-end="url(#ah-green)"/>'
  '</svg>')
a('<div class="hb" data-cue="1" data-d="0.8" style="left:770px;top:330px">synchronizes-with</div>')
lbl('so slot = m happens-before use(slot.price)', 560, 570, 2, 1.0, None, 'c-green')
code(['  movaps  %xmm1, 16+slot(%rip)',
      ('  movb    $1, ready(%rip)      # release', {'hl': (3, 4)}),
      '.L4:',
      ('  movzbl  ready(%rip), %eax    # acquire', {'hl': (3, 4)}),
      '  testb   %al, %al',
      ('  je      .L4                  # loop kept', {'hl': (3, 4)})], 120, 650, 780, cue=3, lang='asm', sm=True, title='x86-64 · g++ 13.3 -O2')
code(['  stp     q1, q0, [x8]',
      ('  stlrb   w9, [x8]     // store-release', {'hl': (4, None)}),
      '.LBB1_1:',
      ('  ldarb   w9, [x8]     // load-acquire', {'hl': (4, None)}),
      '  tbz     w9, #0, .LBB1_1'], 1000, 650, 800, cue=4, lang='asm', sm=True, title='AArch64 · clang 18 -O2 (__atomic builtins)')
end()

# ================================================================ ring
scene('ring')
h2('A lock-free SPSC ring')
meter(('mutex + cv', M50, M99), ('ring, packed', R50, MT['packed'][1]), 4, part=2)
code(['bool try_push(const Msg& m) {            // feed',
      '  uint64_t h = head.load(relaxed);',
      '  if (h - tail.load(acquire) == N) return false;',
      ('  slots[h % N] = m;', {'hl': (1, 2)}),
      ('  head.store(h + 1, release);', {'hl': (1, 2)}),
      '}',
      'bool try_pop(Msg& out) {                 // strategy',
      '  uint64_t t = tail.load(relaxed);',
      ('  if (t == head.load(acquire)) return false;', {'hl': (2, 3)}),
      ('  out = slots[t % N];', {'hl': (2, 3)}),
      '  tail.store(t + 1, release);',
      '}'], 120, 200, 1000, cue=0, sm=True)
for k in range(8):
    a(f'<div class="rslot" id="rg-{k}" data-cue="0" data-d="{0.05*k:.2f}" style="left:{1200+k*80}px;top:300px"></div>')
a('<div class="ptr c-teal" id="rg-h" data-cue="1" style="left:1200px;top:255px">head</div>')
a('<div class="ptr c-violet" id="rg-t" data-cue="2" style="left:1200px;top:378px">tail</div>')
a('<div class="tagx" data-cue="3" style="left:1200px;top:430px;border-color:var(--green);color:var(--green)">no lock · no syscall</div>')
a(f'<div class="bign c-teal" data-cue="4" style="left:1200px;top:520px;font-size:110px">{f(R50)} ns</div>')
lbl(f'p50 · was {us(M50)} µs', 1210, 640, 4, 0.3)
a(f'<div class="box" data-cue="5" style="left:1200px;top:720px;width:620px"><div class="t" style="font-size:26px">1 line, 1 core to another</div><div class="s">ping-pong, one-way median: ~{N["oneway"]} ns</div></div>')
end()

# ================================================================ mesi
scene('mesi')
h2('Step 6 · cache lines and MESI')
a('<div class="core teal" data-cue="0" style="left:120px;top:210px;width:520px"><div class="t">core 1 · feed</div><div class="s">L1</div></div>')
a('<div class="core violet" data-cue="0" style="left:1280px;top:210px;width:520px"><div class="t">core 2 · strategy</div><div class="s">L1</div></div>')
a('<div class="st" id="me-s1" data-cue="1" style="left:140px;top:330px">M</div>')
a('<div class="st" id="me-s2" data-cue="1" style="left:1300px;top:330px">I</div>')
lbl('Modified · Exclusive · Shared · Invalid', 690, 225, 1, 0, 560)
a('<div class="bytes" data-cue="2" style="left:420px;top:450px">'
  '<div style="width:170px;background:var(--teal)">head</div><div style="width:170px;background:var(--violet)">tail</div>'
  '<div style="width:170px;background:var(--teal);opacity:.7">pushed</div><div style="width:170px;background:var(--violet);opacity:.7">popped</div>'
  '<div style="width:360px;background:#3d5563;color:#cfe">slots[0..]</div></div>')
lbl('ONE 64-BYTE LINE · RingPacked', 420, 535, 2, 0.3)
a('<svg class="full"><path id="me-pp" d="M 380 400 C 700 330 1200 330 1540 400 C 1200 470 700 470 380 400" fill="none" stroke="none"/>'
  '<path class="draw" data-cue="3" d="M 640 380 C 900 330 1050 330 1270 380" stroke="var(--red)" stroke-width="3" fill="none" stroke-dasharray="8 8" marker-end="url(#ah-red)"/>'
  '<path class="draw" data-cue="3" data-d="0.4" d="M 1270 420 C 1050 470 900 470 640 420" stroke="var(--red)" stroke-width="3" fill="none" stroke-dasharray="8 8" marker-end="url(#ah-red)"/></svg>')
a('<div class="pkt" data-path="me-pp" data-cue="3" data-dur="1.6" data-loop="1" style="background:var(--red);box-shadow:0 0 16px var(--red);width:30px;height:30px;margin:-15px 0 0 -15px"></div>')
lbl('every write: invalidate the other copy, move the line', 690, 290, 3, 0.6, 560, 'c-red')
SC = 18
lbl('TWO THREADS · relaxed fetch_add on their own counter', 120, 620, 4)
bar('same line', N['fsv'][0], 120, 660, SC, 4, 'var(--red)', d=0.2, lw=220, txt=f'{N["fs"][0]} ns')
bar('own lines', N['fsv'][1], 120, 725, SC, 5, 'var(--green)', d=0.0, lw=220, txt=f'{N["fs"][1]} ns')
lbl('ns per increment · median of 7 runs', 120, 795, 5, 0.6)
end()

# ================================================================ padfix
scene('padfix')
h2('alignas(64), then cached indices')
meter(('ring, packed', R50, MT['packed'][1]), ('ring padded', P50, MT['padded'][1]), 1, part=2)
code([('std::atomic<uint64_t> head, tail;', {'dele': 0.6}),
      ('uint64_t pushed, popped;', {'dele': 0.6}),
      ('alignas(64) std::atomic<uint64_t> head;', {'add': 0.8}),
      ('alignas(64) std::atomic<uint64_t> tail;', {'add': 1.0}),
      ('alignas(64) uint64_t pushed;  alignas(64) uint64_t popped;', {'add': 1.2})], 120, 200, 1000, cue=0, sm=True)
for k, (t, c) in enumerate([('head', 'teal'), ('tail', 'violet'), ('pushed', 'teal'), ('popped', 'violet')]):
    a(f'<div class="lnbox" data-cue="1" data-d="{0.2*k:.1f}" style="left:{1200+k*160}px;top:220px;border-color:var(--{c})">{t}<span>64 B</span></div>')
code(['T* try_claim() {                          // lab SpscRing',
      '  const uint64_t head = head_.load(relaxed);',
      ('  if (head - cached_tail_ == Capacity) {  // looks full?', {'hl': (3, 5)}),
      ('    cached_tail_ = tail_.load(acquire);   // only then', {'hl': (3, 5)}),
      '    if (head - cached_tail_ == Capacity) return nullptr;',
      '  }',
      '  return &slots_[head & kMask];',
      '}'], 120, 470, 1000, cue=2, sm=True, title='libs/core/include/lab/core/spsc_ring.hpp')
rows = [('packed', R50, 'var(--red)'), ('alignas(64)', P50, 'var(--amber)'), ('lab SpscRing', L50, 'var(--green)')]
for k, (nm, v, col) in enumerate(rows):
    cue = [0, 1, 4][k]
    bar(nm, v, 1200, 470 + k * 70, 0.8, cue, col, d=0.3 if k else 0, lw=200)
lbl('p50 stamp → signal', 1420, 430, 0)
a('<div class="tagx" data-cue="5" style="left:1200px;top:720px;border-color:var(--muted);color:#cfdbe2;width:620px;white-space:normal;line-height:1.4">paced at 1 msg / µs the ring rarely fills, so the cached tail seldom matters</div>')
end()

# ================================================================ results
scene('results')
h2('Every step, measured')
TR = [('timer only (floor)', ST['timer'], 'c-muted'), ('v0 naive', ST['v0'], 'c-red'), ('1 · flat array, hot line', ST['v1'], 'c-teal'),
      ('2 · four accumulators', ST['v2a'], 'c-blue'), ('2 · running sums, no divide', ST['v2'], 'c-blue'),
      ('3 · branchless', ST['v3'], 'c-amber'), ('4 · no allocation', ST['v4'], 'c-green')]
TT = [('5 · mutex + condvar', MT['mutex'], 'c-red'), ('5 · SPSC ring, packed', MT['packed'], 'c-violet'),
      ('6 · alignas(64)', MT['padded'], 'c-pink'), ('6 · + cached indices (lab)', MT['lab'], 'c-green')]
def fmt(v): return f'{v/1000:.1f} µs' if v >= 1000 else f'{f(v)} ns'
rows_html = ['<tr><th>ONE THREAD · per message</th><th>p50</th><th>p99</th></tr>']
for k, (nm, v, c) in enumerate(TR):
    rows_html.append(f'<tr data-cue="1" data-d="{0.15*k:.2f}"><td class="{c}">{nm}</td><td>{fmt(v[0])}</td><td>{fmt(v[1])}</td></tr>')
rows_html.append('<tr data-cue="2"><th>TWO THREADS · stamp → signal</th><th>p50</th><th>p99</th></tr>')
for k, (nm, v, c) in enumerate(TT):
    rows_html.append(f'<tr data-cue="2" data-d="{0.2+0.15*k:.2f}"><td class="{c}">{nm}</td><td>{fmt(v[0])}</td><td data-hl="4">{fmt(v[1])}</td></tr>')
a('<table class="t big" data-cue="0" style="left:120px;top:190px;width:1180px">' + ''.join(rows_html) + '</table>')
a('<div class="box green" data-cue="3" style="left:1360px;top:250px;width:450px"><div class="t" style="font-size:27px">keep the hot path on one pinned thread</div>'
  f'<div class="s">handoff ≈ {f(L50)} ns vs work ≈ {f(ST["v4"][0]-ST["timer"][0])} ns</div></div>')
a('<div class="box amber" data-cue="4" style="left:1360px;top:480px;width:450px"><div class="t" style="font-size:27px">two-thread p99 = VM noise</div>'
  '<div class="s">hypervisor steal and neighbours; p50 is the stable signal here</div></div>')
foot(1, 890, 0.4, FOOT + ' · single thread: median of 7 runs × 2M · two threads: median of 21 runs × 200k')
end()

# ================================================================ checklist
scene('checklist')
h2('Interview talking points')
items = [('Measure first: per message, p50 / p99, same output', 'teal'),
         ('Integer ids + flat arrays, not std::map&lt;std::string&gt;', 'teal'),
         ('Short dependency chains; no divide on the hot path', 'blue'),
         ('Random branches → data; confirm with g++ -S', 'amber'),
         ('Allocate and touch memory at startup', 'green'),
         ('Publish with release, read with acquire', 'violet'),
         ('One cache line per thread’s hot data: alignas(64)', 'pink')]
for k, (t, c) in enumerate(items):
    a(f'<div class="chk" data-cue="{k+1}" style="left:140px;top:{200+k*92}px"><i style="background:var(--{c})"></i>{t}</div>')
end()

open(f'{OUT}/scenes.html', 'w').write('\n'.join(O))

# ---------------------------------------------------------------- css
CSS = open('/mnt/project-files/videos/explainers/cpp-branches-layout/style.css').read() + r'''
.meter{position:absolute;width:580px;padding:10px 18px;border-radius:14px;background:rgba(8,18,26,.92);border:2px solid var(--line);z-index:5}
.meter .mh{font:600 16px var(--mono);color:var(--muted);letter-spacing:.08em}
.meter .mb{display:flex;align-items:baseline;gap:12px;margin-top:4px;font-family:var(--mono)}
.meter .mlab{font:600 19px var(--mono);color:#cfdbe2;width:180px;white-space:nowrap;overflow:hidden}
.meter .mk{font:600 18px var(--mono);color:var(--muted)}
.meter .mv{font:700 26px var(--mono);color:var(--teal);width:150px;white-space:nowrap}
.meter.chg .mv{color:var(--green)}
.code .line{position:relative}
.code .gut{display:inline-block;width:0;margin-left:-20px;margin-right:20px;color:var(--green);font-weight:700}
.code .gut.gm{color:var(--red)}
.code .delov{position:absolute;left:0;right:0;top:0;bottom:0;background:rgba(255,107,94,.13);pointer-events:none}
.code .delov::after{content:"";position:absolute;left:22px;right:22px;top:52%;height:2px;background:var(--red);opacity:.85}
.code .addl{background:rgba(79,209,139,.07)}
.stepc{position:absolute;display:flex;align-items:center;gap:12px;padding:10px 16px 10px 10px;border-radius:12px;border:2px solid;background:#0b161e;font:600 24px var(--body);white-space:nowrap}
.stepc b{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;color:#06141a;font:700 20px var(--mono)}
.sus{position:absolute;display:flex;align-items:center;gap:14px;padding:12px 18px 12px 12px;border-radius:12px;border:2px solid;background:#0b161e;font:600 25px var(--mono);white-space:nowrap}
.sus b{display:grid;place-items:center;width:36px;height:36px;border-radius:50%;color:#06141a;font:700 20px var(--mono)}
.bign{font:800 130px/1 var(--display);font-stretch:80%}
.term{position:absolute;padding:16px 20px;border-radius:12px;background:#050c11;border:2px solid var(--line);font:500 21px/1.55 var(--mono);color:#cfdbe2}
.hbar{position:absolute;width:22px;border-radius:4px 4px 0 0}
.vline{position:absolute;border-left:3px solid}
.axis{position:absolute;height:2px;background:#4a5f6c}
.node{position:absolute;width:100px;height:58px;border-radius:10px;border:2px solid var(--violet);background:#1b1530;display:grid;place-items:center;font:600 22px var(--mono);color:#d9ccff}
.acell{position:absolute;width:76px;height:64px;border-radius:8px;background:#16303a;border:2px solid #2d5260;display:grid;place-items:center;font:600 22px var(--mono);color:#9fd8e0}
.acell.hit{background:var(--teal);color:#06141a;border-color:var(--teal)}
.cline{position:absolute;padding:8px 14px;border-top:3px solid var(--teal);font:600 21px var(--mono);color:var(--teal)}
.iname{position:absolute;width:240px;height:46px;font:600 22px/46px var(--mono);color:#cfdbe2}
.pc{position:absolute;width:56px;height:46px;border-radius:8px;display:grid;place-items:center;font:700 21px var(--mono);color:#06141a}
.pw{position:absolute;height:46px;border-radius:8px;border:2px dashed var(--red);display:grid;place-items:center;font:600 18px var(--mono);color:var(--red)}
.cn{position:absolute;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;font:700 26px var(--mono);color:#06141a}
.cn.red{background:var(--red)} .cn.teal{background:var(--teal)}
.tl{position:absolute;height:52px;border-radius:8px;display:grid;place-items:center;font:600 19px var(--mono);color:#06141a;white-space:nowrap;overflow:hidden}
.rname{position:absolute;font:600 26px var(--mono);color:#cfdbe2;width:300px}
.bit{width:30px;height:46px}
.ctr{position:absolute;width:860px;padding:16px 22px;border-radius:14px;background:var(--panel);border:2px solid var(--line)}
.ctr .row{display:flex;justify-content:space-between;align-items:baseline;font:600 28px var(--mono);color:#cfdbe2;margin-top:8px}
.ctr .row b{font:800 64px var(--display)}
.vg{position:absolute;height:48px;border-radius:6px;background:var(--amber);border:2px solid #6b4a1c}
.slot{position:absolute;width:30px;height:30px;border-radius:7px;background:#203540;border:2px solid #2d5260}
.slot.on{background:var(--green);border-color:var(--green)}
.slot.old{background:var(--amber);border-color:var(--amber)}
.val{position:absolute;font:700 26px var(--mono)}
.core{position:absolute;width:440px;padding:18px 24px;border-radius:16px;background:var(--panel);border:3px solid var(--line)}
.core.teal{border-color:var(--teal)} .core.violet{border-color:var(--violet)}
.core .t{font:700 32px var(--body)} .core .s{font:500 22px var(--mono);color:var(--muted);margin-top:4px}
.qbox{position:absolute;width:420px;height:100px;border-radius:14px;border:3px dashed var(--amber);display:grid;place-items:center;font:700 32px var(--mono);color:var(--amber)}
.sbq{position:absolute;width:300px;padding:8px 14px;border-radius:8px;background:#123038;border:1px solid #2d5260;font:600 21px var(--mono)}
.colh{position:absolute;font:700 30px var(--body)}
.pair{position:absolute;width:400px;height:64px;font:600 25px/64px var(--mono);color:#cfdbe2}
.cellx{position:absolute;width:300px;height:64px;border-radius:10px;display:grid;place-items:center;font:700 24px var(--mono)}
.cellx.ok{background:rgba(79,209,139,.15);color:var(--green);border:2px solid var(--green)}
.cellx.bad{background:rgba(255,107,94,.12);color:var(--red);border:2px solid var(--red)}
.lane{position:absolute;font:700 30px var(--body);padding:6px 16px;border-left:6px solid}
.lane.teal{border-color:var(--teal)} .lane.violet{border-color:var(--violet)}
.op{position:absolute;padding:12px 18px;border-radius:10px;background:#0b161e;border:2px solid;font:600 24px var(--mono)}
.op.strong{border-width:3px}
.hb{position:absolute}
div.hb{padding:6px 14px;border-radius:999px;background:var(--amber);color:#06141a;font:700 21px var(--mono)}
.rslot{position:absolute;width:70px;height:64px;border-radius:8px;background:#203540;border:2px solid #2d5260}
.rslot.on{background:var(--teal);border-color:var(--teal)}
.ptr{position:absolute;font:700 24px var(--mono)}
.st{position:absolute;width:80px;height:80px;border-radius:12px;display:grid;place-items:center;font:800 46px var(--display);color:#06141a;background:#55707f}
.st.M{background:var(--green)} .st.I{background:#3a4a55;color:#9fb1bd} .st.S{background:var(--blue)}
.lnbox{position:absolute;width:148px;height:120px;border-radius:10px;border:3px solid;background:#0b161e;display:flex;flex-direction:column;justify-content:center;align-items:center;font:700 24px var(--mono)}
.lnbox span{font:500 18px var(--mono);color:var(--muted);margin-top:6px}
table.t.big{position:absolute;font:500 26px var(--mono)} table.t.big td{padding:8px 18px} table.t.big th{padding:14px 18px 6px;font-size:19px}
.foot{max-width:1680px;line-height:1.4}
table.t.big tr.hl td{background:rgba(255,179,71,.1)}
.msgbox{position:absolute}
'''
open(f'{OUT}/style.css', 'w').write(CSS)

# ---------------------------------------------------------------- js
JS = r'''
// running latency meter: .meter[data-from,data-to,data-at] ; ring/mesi animations
(function(){
function fmt(v){ return v >= 1000 ? (v/1000).toFixed(1) + ' µs' : (v >= 10 ? Math.round(v) : v.toFixed(1)) + ' ns'; }
function meters(u, cue, H, sc){
  document.querySelectorAll('#s-' + sc.id + ' .meter').forEach(function(m){
    var A = m.dataset.from.split(',').map(Number), B = m.dataset.to.split(',').map(Number);
    var at = parseFloat(m.dataset.at), p = 0;
    if (at >= 0) p = H.ease((u - cue(at)) / 1.4);
    H.text(m.querySelector('.m50'), fmt(H.lerp(A[0], B[0], p)));
    H.text(m.querySelector('.m99'), fmt(H.lerp(A[1], B[1], p)));
    H.text(m.querySelector('.mlab'), p < 0.5 ? m.dataset.la : m.dataset.lb);
    m.classList.toggle('chg', at >= 0 && u > cue(at) && u < cue(at) + 3);
  });
}
var ids = %IDS%;
ids.forEach(function(id){ SCENES[id] = { draw: function(u, cue, H, sc){ meters(u, cue, H, sc); if (EXTRA[id]) EXTRA[id](u, cue, H, sc); } }; });
var EXTRA = {};
EXTRA['prealloc'] = function(u, cue, H){
  var n = Math.max(0, Math.floor((u - cue(1)) * 6));
  for (var k = 0; k < 32; k++){ var el = document.getElementById('pa-s' + k);
    var filled = n > k || n >= 32; var cur = (n % 32) === k && n > 0;
    el.classList.toggle('on', filled && !cur); el.classList.toggle('old', cur); }
};
EXTRA['ring'] = function(u, cue, H){
  var t0 = cue(1), h = Math.max(0, Math.floor((u - t0) * 2.2)), t = Math.max(0, Math.floor((u - t0 - 0.9) * 2.2));
  if (t > h) t = h;
  for (var k = 0; k < 8; k++){ var el = document.getElementById('rg-' + k);
    var on = false; for (var i = t; i < h; i++) if (i % 8 === k) on = true; el.classList.toggle('on', on); }
  document.getElementById('rg-h').style.left = (1200 + (h % 8) * 80) + 'px';
  document.getElementById('rg-t').style.left = (1200 + (t % 8) * 80) + 'px';
};
EXTRA['mesi'] = function(u, cue, H){
  var a = document.getElementById('me-s1'), b = document.getElementById('me-s2');
  var ph = u < cue(3) ? 0 : Math.floor((u - cue(3)) / 0.8) % 2;
  var s1 = ph === 0 ? 'M' : 'I', s2 = ph === 0 ? 'I' : 'M';
  H.text(a, s1); H.text(b, s2); a.className = 'st ' + s1; b.className = 'st ' + s2;
};
})();
'''
ids = [s['id'] for s in S]
open(f'{OUT}/scenes.js', 'w').write(JS.replace('%IDS%', json.dumps(ids)))
print('wrote', OUT)
