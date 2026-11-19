import sys
sys.path.insert(0, '/tmp/claude-0/vx/ai1316tools')
from hl import code_html, check
OUT = '/mnt/project-files/videos/explainers/ai-15-fixed-point'
LEFT = r'''
struct Levels {
  double base;               // price of level 0
  std::vector<double> qty;   // one slot per tick
  double notional = 0;
};
constexpr double kTick = 0.01, kEps = 1e-9;
void apply(Levels& L, double px, double qty) {
  const double t = px / kTick;
  if (std::fabs(t - std::round(t)) > kEps)
    throw std::invalid_argument("off tick");
  const auto i = static_cast<std::size_t>(
      std::round((px - L.base) / kTick));
  L.qty[i] += qty;
  L.notional += px * qty;
}
'''
RIGHT = r'''
// price in ticks of 0.01: 5012.25 -> 501225
using Ticks = int64_t;
struct Levels {
  Ticks base;                // price of level 0
  std::vector<int64_t> qty;  // one slot per tick
  int64_t notional = 0;      // ticks x qty, exact
};
// px: validated and converted once, at the edge
void apply(Levels& L, Ticks px, int64_t qty) {
  const auto i = std::size_t(px - L.base);
  L.qty[i] += qty;
  L.notional += px * qty;
}
'''
check(LEFT); check(RIGHT)
h = []; A = h.append
# title
A('<div class="scene" id="s-title">')
A('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">PATTERN 15 / 16</div>')
A('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:215px">Prices as<br>integer ticks</div>')
A('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:520px;width:1600px">double + epsilon + std::round vs int64 ticks (fixed point)</div>')
A('<div class="big mono c-red" data-cue="1" style="left:140px;top:650px">0.1 + 0.2 = <span class="type" data-cue="1" data-d="0.3" data-dur="1.6">0.30000000000000004</span></div>')
A('<div class="big mono c-teal" data-cue="2" style="left:140px;top:760px">10 + 20 = 30 <span class="c-muted" style="font-size:30px">ticks of 0.01</span></div>')
A('</div>')
# general
A('<div class="scene" id="s-general">')
A('<div class="h2" data-cue="0" style="left:70px;top:110px">Apply an update at a price</div>')
A('<div class="side c-red" data-cue="1" style="left:70px;top:200px">GENERAL-PURPOSE</div>')
A(code_html(LEFT, {7: (2, 3), 8: (2, 3), 9: (2, 3), 10: (2.5, 3), 11: (2.5, 3), 13: (3, 4)}, cls="code sm left", style="left:70px;top:240px;width:880px", cue=1))
# tick grid number line
A('<div class="lbl" data-cue="2" style="left:1040px;top:250px">THE TICK GRID (0.01) · zoomed in</div>')
A('<svg class="full"><path class="draw" data-cue="2" d="M1060 400 L1820 400" stroke="#8ea3b1" stroke-width="3" fill="none"/>'
  + ''.join(f'<path class="draw" data-cue="2" data-d="{0.15*i}" d="M{1120+i*300} 380 L{1120+i*300} 420" stroke="#8ea3b1" stroke-width="3" fill="none"/>' for i in range(3))
  + '</svg>')
for i, lab in enumerate(['5012.09', '5012.10', '5012.11']):
    A(f'<div class="lbl" data-cue="2" data-d="{0.15*i}" style="left:{1120+i*300-50}px;top:432px;font-size:24px">{lab}</div>')
A('<div class="dot" data-cue="2.4" data-anim="fade" style="left:1438px;top:388px"></div>')
A('<div class="note" data-cue="2.4" data-d="0.3" style="left:1040px;top:500px;width:780px">the double nearest 5012.10 is<br><span class="c-amber">5012.100000000000363797880709…</span><br>so "on the grid" needs a tolerance</div>')
A('<div class="chip amber" data-cue="2.7" style="left:1040px;top:660px">|t - round(t)| &lt;= 1e-9 ?</div>')
A('<div class="chip red" data-cue="3" style="left:1040px;top:740px">notional += px * qty, in double</div>')
A('</div>')
# wrong
A('<div class="scene" id="s-wrong">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">What double prices do (g++ 13, this box)</div>')
A('<div class="th" data-cue="0" data-d="0.3" style="left:120px;top:200px;width:620px">expression</div>')
A('<div class="th c-red" data-cue="0" data-d="0.3" style="left:760px;top:200px">double</div>')
A('<div class="th c-teal" data-cue="0" data-d="0.3" style="left:1340px;top:200px">int64 ticks</div>')
rows = [(1, '0.1 + 0.2 == 0.3', 'false · 0.30000000000000004', '10 + 20 == 30'),
        (1.5, 'map: +100 @ 0.3, +50 @ 0.1+0.2', '2 levels', '1 level, qty 150'),
        (2, '100.00 + ten 0.01 steps == 100.10', 'false · 100.10000000000005', '10000 + 10 == 10010'),
        (3, 'int64_t(0.29 / 0.01)', '28 · (28.999999999999996)', '29'),
        (4, '1,000,000 fills of 3 @ 0.01', '29999.9999996277', '3000000 = 30000.00')]
for k, (c, e, d, t) in enumerate(rows):
    y = 250 + k * 110
    A(f'<div class="row15" data-cue="{c}" style="left:120px;top:{y}px;width:1680px"></div>')
    A(f'<div class="mono rt" data-cue="{c}" style="left:140px;top:{y+22}px;width:600px">{e}</div>')
    A(f'<div class="mono rt c-red" data-cue="{c}" data-d="0.4" style="left:760px;top:{y+22}px">{d}</div>')
    A(f'<div class="mono rt c-teal" data-cue="{c}" data-d="0.8" style="left:1340px;top:{y+22}px">{t}</div>')
A('<div class="chip amber" data-cue="5" style="left:120px;top:820px">every epsilon and round() is a patch for this</div>')
A('</div>')
# cost
A('<div class="scene" id="s-cost">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Per update, in the compiled loop</div>')
A('<div class="side c-red" data-cue="1" style="left:120px;top:220px">DOUBLE (objdump, -O2)</div>')
ops = [('divsd', 'amber', 1, 300), ('call round', 'red', 2, 210), ('spill/reload', 'mute', 2, 200), ('sub · andpd · comisd', 'mute', 2, 290),
       ('divsd', 'amber', 1, 300), ('call round', 'red', 2, 210), ('cvttsd2si · addsd · mulsd · addsd', 'mute', 3, 0)]
x = 120; y = 270
for i, (t, k, c, w) in enumerate(ops):
    if w == 0:
        x = 120; y += 90; w = 560
    A(f'<div class="op {k}" data-cue="{c}" data-d="{0.15*i:.2f}" style="left:{x}px;top:{y}px;width:{w}px">{t}</div>')
    x += w + 12
A('<div class="note" data-cue="1" data-d="1.0" style="left:120px;top:460px">divsd: typically 13-15 cycles latency on current x86</div>')
A('<div class="chip red" data-cue="3" style="left:120px;top:520px">≈ 35 instructions per update · 2 calls</div>')
A('<div class="side c-teal" data-cue="4" style="left:120px;top:640px">INT64 TICKS</div>')
for i, t in enumerate(['sub', 'add [qty+i]', 'imul', 'add [notional]']):
    A(f'<div class="op teal" data-cue="4" data-d="{0.2*i:.2f}" style="left:{120+i*232}px;top:690px;width:220px">{t}</div>')
A('<div class="chip teal" data-cue="4" data-d="1.0" style="left:120px;top:790px">10 instructions per update · 0 calls</div>')
A('</div>')
# hot
A('<div class="scene" id="s-hot">')
A('<div class="h2" data-cue="0" style="left:60px;top:110px">Integer ticks, converted once</div>')
A('<div class="side c-red" data-cue="0" style="left:60px;top:200px">GENERAL</div>')
A('<div class="side c-teal" data-cue="0" data-d="0.3" style="left:980px;top:200px">HOT PATH</div>')
A(code_html(LEFT, {}, cls="code sm left", style="left:60px;top:240px;width:880px", cue=0, extra=' data-dim="1"'))
A(code_html(RIGHT, {0: (1, 2), 1: (0, 1), 7: (1, 2), 8: (2, 3), 9: (2, 3), 11: (3, 4), 5: (3, 4)}, cls="code sm right", style="left:980px;top:240px;width:880px", cue=0, extra=' data-d="0.3"'))
A('<div class="chip teal" data-cue="4" style="left:980px;top:740px">== is exact: safe as map / hash key</div>')
A('<div class="chip amber" data-cue="4" data-d="1.5" style="left:980px;top:810px">int64 max ≈ 9.2e18 · check ticks x qty worst case</div>')
A('<div class="chip teal" data-cue="1" data-d="0.8" style="left:60px;top:740px">"5012.25" → 501225 at the feed parser (pattern 16)</div>')
A('</div>')
# numbers
A('<div class="scene" id="s-numbers">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">ns per update, p50 (lower is better)</div>')
A('<div class="note" data-cue="0" data-d="0.3" style="left:120px;top:190px;width:1700px">measured on a shared 4-vCPU cloud VM · g++ 13 -O2 · 8,192 updates · 2,000-level book · pinned · median of 3 runs x 41 passes</div>')
SC = 80; X0 = 560
def bar(y, name, val, col, cue, d=0.0, txt=None):
    A(f'<div class="blab" data-cue="{cue}" data-d="{d}" style="left:110px;top:{y}px">{name}</div>')
    A(f'<div class="bar grow" data-cue="{cue}" data-d="{d}" data-w="{val*SC:.0f}" data-anim="fade" style="left:{X0}px;top:{y-2}px;background:{col}"></div>')
    A(f'<div class="bv" data-cue="{cue}" data-d="{d+0.7}" style="left:{X0+val*SC+16:.0f}px;top:{y-3}px;color:{col}">{txt or val}</div>')
bar(270, 'double + eps + round', 13.2, 'var(--red)', 1)
bar(320, 'int64 ticks', 2.5, 'var(--teal)', 2)
A('<div class="chip amber" data-cue="2" data-d="0.8" style="left:900px;top:308px">≈ 5x</div>')
bar(370, 'double, no eps check', 4.5, 'var(--violet)', 3)
A('<div class="gl" data-cue="4" style="left:120px;top:470px">after 335,872 updates, notional</div>')
A('<div class="mono big2 c-red" data-cue="4" data-d="0.3" style="left:120px;top:520px">double  84,539,714,399.649658</div>')
A('<div class="mono big2 c-teal" data-cue="4" data-d="0.6" style="left:120px;top:580px">ticks   84,539,714,399.65 (exact)</div>')
A('<div class="chip red" data-cue="4" data-d="1.0" style="left:1240px;top:545px">off by $0.00034</div>')
A('<div class="rule" data-cue="5" style="left:120px;top:690px;width:1660px;font-size:32px">Speed: modest per update. <span class="c-amber">Correctness: the reason to switch.</span></div>')
A('</div>')
# close
A('<div class="scene" id="s-close">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Where each belongs</div>')
cards = [(0, 'var(--muted)', 'double is fine', 'analytics · risk · signals · ~1e-16 relative error'),
         (1, 'var(--red)', 'double is not fine', 'compare · match · sum money · map / hash keys'),
         (2, 'var(--teal)', 'Convert at the edge', 'tick size from reference data'),
         (2.5, 'var(--amber)', 'Tick varies by price band?', 'use the smallest increment as the unit')]
for i, (c, col, t, s) in enumerate(cards):
    x = 120 + (i % 2) * 850; y = 220 + (i // 2) * 190
    A(f'<div class="card2" data-cue="{c}" data-d="0.3" style="left:{x}px;top:{y}px;width:810px;height:160px;border-color:{col}"><div class="ct">{t}</div><div class="cs">{s}</div></div>')
A('<div class="rule" data-cue="3" style="left:120px;top:640px;width:1660px">Integer ticks inside. <span class="c-amber">Decimal text only at the edges.</span></div>')
A('</div>')
open(f'{OUT}/scenes.html', 'w').write('\n'.join(h) + '\n')
css = open('/tmp/claude-0/vx/ai1316tools/common.css').read() + '''
.big{font:700 64px var(--mono)}
.big2{font:700 38px var(--mono);white-space:pre}
.dot{position:absolute;width:24px;height:24px;border-radius:50%;background:var(--amber);box-shadow:0 0 14px var(--amber)}
.th{font:700 26px var(--mono);color:var(--muted)}
.row15{height:90px;border-radius:12px;background:var(--panel);border:1px solid var(--line)}
.rt{font-size:27px;font-weight:600;white-space:nowrap}
.op{height:64px;border-radius:10px;display:grid;place-items:center;font:700 23px var(--mono);border:2px solid}
.op.amber{border-color:var(--amber);color:var(--amber);background:#2a2214}
.op.red{border-color:var(--red);color:#ff9d93;background:#3a1f22}
.op.mute{border-color:var(--line);color:#b7c7d2;background:var(--panel)}
.op.teal{border-color:var(--teal);color:var(--teal);background:#0d2229}
'''
open(f'{OUT}/style.css', 'w').write(css)
print('ok')
