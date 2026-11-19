import sys, json
sys.path.insert(0, '/tmp/claude-0/vx/ai1316tools')
from hl import code_html, check
OUT = '/mnt/project-files/videos/explainers/ai-14-soa'
N = json.load(open('/tmp/claude-0/vx/ai-14-soa/code/numbers.json'))
LEFT = r'''
struct Order {                       // 112 bytes
  std::string symbol, account;       // 2 x 32
  uint64_t id;
  sys_clock::time_point created, updated;
  double price; int64_t qty;
  Side side; bool active, ioc, post_only;
};
int64_t bid_depth(const std::vector<Order>& book,
                  double px) {
  int64_t total = 0;
  for (const Order& o : book)
    if (o.active && o.side == Side::Buy &&
        o.price >= px) total += o.qty;
  return total;
}
'''
RIGHT = r'''
// hot fields: one array each.
// cold fields live elsewhere, same index.
struct BookHot {
  std::vector<double>   px;
  std::vector<int64_t>  qty;
  std::vector<uint8_t>  live_bid;  // active && Buy
};
int64_t bid_depth(const BookHot& b, double px) {
  int64_t total = 0;
  for (size_t i = 0; i < b.px.size(); ++i) {
    const int64_t take =
        b.live_bid[i] & (b.px[i] >= px);
    total += b.qty[i] & -take;   // 0 or all ones
  }
  return total;
}
'''
check(LEFT); check(RIGHT)
h = []
A = h.append
# ---------- title
A('<div class="scene" id="s-title">')
A('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">PATTERN 14 / 16</div>')
A('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:215px">Hot fields,<br>cold fields</div>')
A('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:520px;width:1600px">a vector of fat structs vs struct-of-arrays and a hot/cold split</div>')
# title graphic: one fat order with 18 hot bytes
F = [('symbol', 0, 32, 'cold'), ('account', 32, 32, 'cold'), ('id', 64, 8, 'cold'), ('created', 72, 8, 'cold'), ('updated', 80, 8, 'cold'),
     ('price', 88, 8, 'hot'), ('qty', 96, 8, 'hot'), ('s', 104, 1, 'hot'), ('a', 105, 1, 'hot'), ('', 106, 6, 'cold')]
SCx = 14
for i, (nm, off, w, k) in enumerate(F):
    col = 'var(--green)' if k == 'hot' else '#3a4f5c'
    A(f'<div class="cell" data-cue="1" data-d="{0.05*i:.2f}" data-anim="fade" style="left:{140+off*SCx}px;top:700px;width:{w*SCx}px;background:{col};color:{"#06141a" if k=="hot" else "#9fb3c0"}">{nm if w>=8 else ""}</div>')
A(f'<div class="lbl" data-cue="1" data-d="0.6" style="left:140px;top:780px">one Order = 112 bytes · <span class="c-green">the scan needs 18</span></div>')
A('</div>')
# ---------- general
A('<div class="scene" id="s-general">')
A('<div class="h2" data-cue="0" style="left:70px;top:110px">Open bid quantity at or above a price</div>')
A('<div class="side c-red" data-cue="1" style="left:70px;top:200px">GENERAL-PURPOSE</div>')
A(code_html(LEFT, {0: (1, 2), 1: (1, 2), 2: (1, 2), 3: (1, 2), 4: (1, 2), 5: (1, 2), 10: (2, 3), 11: (2, 3), 12: (2, 3)}, cls="code sm left", style="left:70px;top:240px;width:880px", cue=1))
A('<div class="box red" data-cue="1" data-d="0.6" style="left:1040px;top:250px;width:760px;height:120px"><div class="t">std::vector&lt;Order&gt;</div><div class="s">one rich struct per resting order</div></div>')
A('<div class="note" data-cue="1.5" style="left:1040px;top:400px;width:760px">2 strings · id · 2 timestamps · price · qty · 4 flags</div>')
A('<div class="chip red" data-cue="1.7" style="left:1040px;top:460px">sizeof(Order) = 112</div>')
A('<div class="chip teal" data-cue="3" style="left:1040px;top:560px">a good design for an order store</div>')
A('</div>')
# ---------- cost
A('<div class="scene" id="s-cost">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">What the scan pulls through the cache</div>')
S = 3.75; X = 120
A('<div class="lbl" data-cue="0" data-d="0.3" style="left:120px;top:205px">4 ORDERS IN A std::vector&lt;Order&gt; · 448 bytes</div>')
for k in range(4):
    for i, (nm, off, w, kd) in enumerate(F):
        col = 'var(--green)' if kd == 'hot' else '#3a4f5c'
        A(f'<div class="cell" data-cue="0" data-d="{0.3+0.1*k:.2f}" data-anim="fade" style="left:{X+(k*112+off)*S:.1f}px;top:250px;width:{w*S:.1f}px;background:{col};height:60px"></div>')
    A(f'<div class="lbl" data-cue="0" data-d="{0.3+0.1*k:.2f}" style="left:{X+k*112*S+6:.0f}px;top:318px;font-size:19px">order {k}</div>')
for j in range(8):
    A(f'<div class="cline" data-cue="1" data-d="{0.05*j:.2f}" data-anim="fade" style="left:{X+j*64*S-1:.1f}px;top:236px"></div>')
A('<div class="lbl c-amber" data-cue="1" data-d="0.4" style="left:120px;top:360px">| = 64-byte cache line boundary · the core loads whole lines</div>')
for j in range(7):
    used = j in (1, 3, 4, 5, 6)
    A(f'<div class="lnbox {"used" if used else "pref"}" data-cue="2" data-d="{0.12*j:.2f}" data-anim="fade" style="left:{X+j*64*S+3:.1f}px;top:420px;width:{64*S-6:.1f}px">{"read" if used else "prefetched"}</div>')
A('<div class="chip amber" data-cue="2" data-d="1.0" style="left:120px;top:500px">18 bytes used · 80 bytes of lines read · ~112 moved per order</div>')
A('<div class="box amber" data-cue="3" style="left:120px;top:600px;width:820px;height:190px"><div class="t c-amber">1 M orders = 117 MB per scan</div><div class="s">L2 here is 2 MiB per core</div><div class="s">most lines come from far away</div></div>')
A('<div class="box" data-cue="4" style="left:980px;top:600px;width:820px;height:190px"><div class="t">cold bytes ride along</div><div class="s">strings, timestamps, unused flags</div><div class="s">evict the lines you need next</div></div>')
A('</div>')
# ---------- hot
A('<div class="scene" id="s-hot">')
A('<div class="h2" data-cue="0" style="left:60px;top:110px">Lay data out by how it is read</div>')
A('<div class="side c-red" data-cue="0" style="left:60px;top:200px">GENERAL</div>')
A('<div class="side c-teal" data-cue="0" data-d="0.3" style="left:980px;top:200px">HOT PATH</div>')
A(code_html(LEFT, {}, cls="code sm left", style="left:60px;top:240px;width:880px", cue=0, extra=' data-dim="1"'))
A(code_html(RIGHT, {3: (1, 2), 4: (1, 2), 5: (1, 2), 0: (2, 3), 1: (2, 3), 10: (3, 4), 11: (3, 4), 12: (4, 5)}, cls="code sm right", style="left:980px;top:240px;width:880px", cue=0, extra=' data-d="0.3"'))
# SoA strip
A('<div class="lbl" data-cue="3" style="left:980px;top:770px">same 4 orders, hot arrays: 68 bytes</div>')
for k in range(4):
    A(f'<div class="cell" data-cue="3" data-d="{0.08*k:.2f}" data-anim="fade" style="left:{980+k*8*S*2.2:.0f}px;top:810px;width:{8*S*2.2-2:.0f}px;height:44px;background:var(--green)">px</div>')
    A(f'<div class="cell" data-cue="3" data-d="{0.3+0.08*k:.2f}" data-anim="fade" style="left:{980+(32+k*8)*S*2.2:.0f}px;top:810px;width:{8*S*2.2-2:.0f}px;height:44px;background:#2fae6f">qty</div>')
A(f'<div class="cell" data-cue="3" data-d="0.6" data-anim="fade" style="left:{980+64*S*2.2:.0f}px;top:810px;width:{4*S*2.2-2:.0f}px;height:44px;background:#7fe0ad;font-size:15px">lb</div>')
A('<div class="chip red" data-cue="5" style="left:60px;top:800px">keep live_bid in sync on fill / cancel</div>')
A('</div>')
# ---------- numbers
A('<div class="scene" id="s-numbers">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Bytes per order, and ns per order</div>')
A(f'<div class="note" data-cue="0" data-d="0.3" style="left:120px;top:190px;width:1700px">measured on a shared 4-vCPU cloud VM · g++ 13 -O2 · pinned · p50 of 21 scans, median of 5 runs</div>')
def bar(y, name, val, col, cue, d, sc, x0, txt, w=360):
    A(f'<div class="blab" data-cue="{cue}" data-d="{d}" style="left:{x0-w-30}px;top:{y}px;width:{w}px">{name}</div>')
    A(f'<div class="bar grow" data-cue="{cue}" data-d="{d}" data-w="{val*sc:.0f}" data-anim="fade" style="left:{x0}px;top:{y-2}px;background:{col}"></div>')
    A(f'<div class="bv" data-cue="{cue}" data-d="{d+0.7}" style="left:{x0+val*sc+14:.0f}px;top:{y-3}px;color:{col}">{txt}</div>')
A('<div class="gl" data-cue="1" style="left:120px;top:255px">bytes moved per order</div>')
bar(305, 'fat struct (AoS)', 112, 'var(--red)', 1, 0.0, 3.2, 520, '112 B')
bar(347, 'hot/cold split', 24, 'var(--violet)', 1, 0.4, 3.2, 520, '24 B')
bar(389, 'struct of arrays', 17, 'var(--teal)', 1, 0.8, 3.2, 520, '17 B')
A(f'<div class="gl" data-cue="2" style="left:120px;top:460px">ns per order · 1 M orders (AoS 117 MB, SoA 18 MB)</div>')
sc = 34
bar(510, 'general (AoS, if)', N['m1']['aos'], 'var(--red)', 2, 0.0, sc, 520, f"{N['m1']['aos']:.0f}")
bar(552, 'AoS, same branchless body', N['m1']['aosbl'], '#c95a50', 3, 0.0, sc, 520, f"{N['m1']['aosbl']:.0f}")
bar(594, 'hot/cold split', N['m1']['hot'], 'var(--violet)', 4, 0.0, sc, 520, f"{N['m1']['hot']:.1f}")
bar(636, 'struct of arrays', N['m1']['soa'], 'var(--teal)', 2, 0.6, sc, 520, f"{N['m1']['soa']:.2f}")
A(f'<div class="gl" data-cue="5" style="left:120px;top:705px">ns per order · 8 M orders (AoS 940 MB, SoA 143 MB)</div>')
bar(755, 'AoS, same branchless body', N['m8']['aosbl'], '#c95a50', 5, 0.3, sc, 520, f"{N['m8']['aosbl']:.0f}")
bar(797, 'struct of arrays', N['m8']['soa'], 'var(--teal)', 5, 0.6, sc, 520, f"{N['m8']['soa']:.1f}")
A(f'<div class="chip amber" data-cue="5" data-d="1.4" style="left:1320px;top:790px">{N["m8"]["aosbl"]/N["m8"]["soa"]:.1f}x · byte ratio 112 / 17 = 6.6x</div>')
A('<div class="chip teal" data-cue="6" data-d="0.5" style="left:1240px;top:610px">1 M: 18 MB of hot arrays stay in cache</div>')
A('</div>')
# ---------- close
A('<div class="scene" id="s-close">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Layout follows access</div>')
cards = [(1, 'var(--muted)', 'Whole-order work: one struct', 'new order · amend · fill report · audit'),
         (2, 'var(--teal)', 'Scans: split the hot fields', 'arrays, or a small hot struct + cold store'),
         (3, 'var(--amber)', 'Cost: keep them in sync', 'one index, updated on every state change'),
         (4, 'var(--amber)', 'Measure bytes per element', 'and the working set against L1 / L2')]
for i, (c, col, t, s) in enumerate(cards):
    x = 120 + (i % 2) * 850; y = 220 + (i // 2) * 190
    A(f'<div class="card2" data-cue="{c}" style="left:{x}px;top:{y}px;width:810px;height:160px;border-color:{col}"><div class="ct">{t}</div><div class="cs">{s}</div></div>')
A('<div class="rule" data-cue="5" style="left:120px;top:640px;width:1660px">Lay data out by how the hot loop reads it, <span class="c-amber">not by what it is called.</span></div>')
A('</div>')
open(f'{OUT}/scenes.html', 'w').write('\n'.join(h) + '\n')
css = open('/tmp/claude-0/vx/ai1316tools/common.css').read() + '''
.cline{position:absolute;width:3px;height:88px;background:var(--amber);border-radius:2px}
.lnbox{position:absolute;height:56px;border-radius:8px;display:grid;place-items:center;font:600 20px var(--mono)}
.lnbox.used{background:rgba(255,179,71,.18);border:2px solid var(--amber);color:var(--amber)}
.lnbox.pref{background:rgba(142,163,177,.10);border:2px dashed #6b8392;color:#9fb3c0}
'''
open(f'{OUT}/style.css', 'w').write(css)
print('ok')
