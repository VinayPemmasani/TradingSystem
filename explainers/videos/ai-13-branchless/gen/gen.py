import sys, random
sys.path.insert(0, '/tmp/claude-0/vx/ai1316tools')
from hl import code_html, check
OUT = '/mnt/project-files/videos/explainers/ai-13-branchless'
LEFT = r'''
Stats scan(const std::vector<Tick>& v, int big) {
  Stats s;
  for (const Tick& t : v) {
    if (t.qty <= 0) {
      std::fprintf(stderr, "bad qty %d\n", t.qty);
      ++s.bad; continue;
    }
    if (t.side == Side::Buy) {
      s.buy_vol += t.qty;
      if (t.qty >= big) ++s.big_buys;
    } else {
      s.sell_vol += t.qty;
      if (t.qty >= big) ++s.big_sells;
    }
  }
  return s; }
'''
RIGHT = r'''
[[gnu::cold, gnu::noinline]]
void on_bad(const Tick& t);  // logs; never inlined
Stats scan(const Tick* t, size_t n, int64_t big) {
  int64_t vol = 0, sv = 0, nb = 0, sb = 0, bad = 0;
  for (size_t i = 0; i < n; ++i) {
    const int64_t q = t[i].qty;
    if (q <= 0) [[unlikely]] {
      on_bad(t[i]); ++bad; continue; }
    const int64_t sell = -int64_t(t[i].side);
    const int64_t b = q >= big;
    vol += q;   sv += q & sell;
    nb  += b;   sb += b & sell;
  }
  return {vol - sv, sv, nb - sb, sb, bad};
}
'''
check(LEFT); check(RIGHT)
h = []
# ---------- title
h.append('<div class="scene" id="s-title">')
h.append('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">PATTERN 13 / 16</div>')
h.append('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:215px">Branches on<br>market data</div>')
h.append('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:520px;width:1600px">if / else per tick vs branchless arithmetic, with the rare path out of line</div>')
random.seed(5)
for i in range(27):
    b = random.random() < 0.5
    x = 140 + i * 60
    col = 'var(--blue)' if b else 'var(--pink)'
    h.append(f'<div class="cell" data-cue="1" data-d="{0.05*i:.2f}" style="left:{x}px;top:720px;width:50px;background:{col}">{"B" if b else "S"}</div>')
    h.append(f'<div class="lbl c-amber" data-cue="1.5" data-d="{0.04*i:.2f}" style="left:{x+16}px;top:676px;font-size:28px">?</div>')
h.append('<div class="lbl" data-cue="1" data-d="1.4" style="left:140px;top:806px"><span class="c-blue">B</span> buy aggressor · <span class="c-pink">S</span> sell aggressor · <span class="c-amber">?</span> a guess per tick</div>')
h.append('</div>')
# ---------- general
h.append('<div class="scene" id="s-general">')
h.append('<div class="h2" data-cue="0" style="left:70px;top:110px">Per-side volume and big trades</div>')
h.append('<div class="side c-red" data-cue="1" style="left:70px;top:200px">GENERAL-PURPOSE</div>')
h.append(code_html(LEFT, {3:(2,2.4),4:(2,2.4),5:(2,2.4),6:(2,2.4),7:(2.4,2.75),10:(2.4,2.75),9:(2.75,3),12:(2.75,3)}, cls="code sm left", style="left:70px;top:240px;width:860px", cue=1))
# flow diagram
h.append('<div class="node" data-cue="0" data-d="0.4" style="left:1330px;top:215px;width:220px">tick</div>')
h.append('<div class="dec" data-cue="2" style="left:1300px;top:340px;width:280px">qty &lt;= 0 ?</div>')
h.append('<div class="node" data-cue="2" data-d="0.3" style="left:1650px;top:340px;width:220px;border-color:var(--red);color:#ff9d93">fprintf</div>')
h.append('<div class="dec" data-cue="2.4" style="left:1340px;top:470px;width:200px">side ?</div>')
h.append('<div class="node" data-cue="2.4" data-d="0.3" style="left:1070px;top:600px;width:300px"><span class="c-blue">buy_vol</span> += q</div>')
h.append('<div class="node" data-cue="2.4" data-d="0.3" style="left:1510px;top:600px;width:300px"><span class="c-pink">sell_vol</span> += q</div>')
h.append('<div class="dec" data-cue="2.75" style="left:1090px;top:730px;width:260px">q &gt;= big ?</div>')
h.append('<div class="dec" data-cue="2.75" style="left:1530px;top:730px;width:260px">q &gt;= big ?</div>')
h.append('<svg class="full">'
 '<path class="draw" data-cue="2" d="M1440 280 L1440 332" stroke="#8ea3b1" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path class="draw" data-cue="2" data-d="0.2" d="M1582 368 L1642 368" stroke="var(--red)" stroke-width="3" fill="none" marker-end="url(#ah-red)"/>'
 '<path class="draw" data-cue="2.4" d="M1440 402 L1440 462" stroke="#8ea3b1" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path class="draw" data-cue="2.4" data-d="0.2" d="M1340 500 L1220 500 L1220 592" stroke="var(--blue)" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path class="draw" data-cue="2.4" data-d="0.2" d="M1540 500 L1660 500 L1660 592" stroke="var(--pink)" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path class="draw" data-cue="2.75" d="M1220 666 L1220 722" stroke="#8ea3b1" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path class="draw" data-cue="2.75" d="M1660 666 L1660 722" stroke="#8ea3b1" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
 '<path id="g-flow" d="M1440 250 L1440 368 L1440 500 L1660 500 L1660 630 L1660 760" stroke="none" fill="none"/>'
 '</svg>')
h.append('<div class="pkt" data-path="g-flow" data-cue="3" data-dur="1.6" data-loop="1" style="background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>')
h.append('<div class="chip amber" data-cue="3" data-d="0.4" style="left:1070px;top:850px">3 conditional jumps per tick, 2 on the data</div>')
h.append('</div>')
# ---------- cost
h.append('<div class="scene" id="s-cost">')
h.append('<div class="h2" data-cue="0" style="left:120px;top:110px">What the core sees</div>')
h.append('<div class="lbl" data-cue="0" data-d="0.2" style="left:120px;top:205px">INSTRUCTIONS IN FLIGHT · oldest left, fetched right</div>')
for i in range(15):
    x = 120 + i * 112
    lab = 'jcc' if i == 5 else ''
    h.append(f'<div class="slot13" id="cs-{i}" style="left:{x}px;top:250px">{lab}</div>')
h.append('<div class="lbl" data-cue="0" data-d="0.4" style="left:120px;top:340px">← retire</div>')
h.append('<div class="lbl" data-cue="0" data-d="0.4" style="left:1660px;top:340px">fetch →</div>')
h.append('<div class="chip amber" data-cue="0.6" style="left:610px;top:340px">guess: side == Buy</div>')
h.append('<div class="chip red" data-cue="1" style="left:930px;top:340px">random side: wrong ≈ 50%</div>')
h.append('<div class="chip red" id="cs-flush" data-cue="2" data-d="0.4" data-out="3" style="left:780px;top:410px">flush: typically 15-20 cycles lost</div>')
h.append('<div class="box" data-cue="3" style="left:120px;top:540px;width:520px;height:250px"><div class="t c-teal">core</div><div class="s">registers: q, side</div><div class="s" style="margin-top:18px;color:#e6eef2">add %rax, 0x0(%rbp)</div><div class="s">add %rax, 0x8(%rbp)</div></div>')
h.append('<div class="box amber" data-cue="4" style="left:1160px;top:540px;width:620px;height:250px"><div class="t c-amber">memory: Stats s</div><div class="s">buy_vol · sell_vol · big_buys · big_sells</div><div class="s" style="margin-top:18px">the return slot; fprintf is opaque,</div><div class="s">so g++ cannot keep it in registers</div></div>')
h.append('<svg class="full">'
 '<path class="draw" data-cue="4" data-d="0.3" d="M650 610 C 850 560, 960 560, 1150 610" stroke="var(--amber)" stroke-width="4" fill="none" marker-end="url(#ah-amber)"/>'
 '<path class="draw" data-cue="4" data-d="0.6" d="M1150 720 C 960 770, 850 770, 650 720" stroke="var(--amber)" stroke-width="4" fill="none" marker-end="url(#ah-amber)"/>'
 '<path id="c-mem" d="M650 610 C 850 560, 960 560, 1150 610 L1150 720 C 960 770, 850 770, 650 720 Z" stroke="none" fill="none"/>'
 '</svg>')
h.append('<div class="lbl c-amber" data-cue="4" data-d="0.5" style="left:840px;top:530px">load</div>')
h.append('<div class="lbl c-amber" data-cue="4" data-d="0.8" style="left:830px;top:775px">store</div>')
h.append('<div class="pkt" data-path="c-mem" data-cue="4" data-d="0.9" data-dur="1.4" data-loop="1" style="background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>')
h.append('</div>')
# ---------- hot
h.append('<div class="scene" id="s-hot">')
h.append('<div class="h2" data-cue="0" style="left:60px;top:110px">Decisions become numbers</div>')
h.append('<div class="side c-red" data-cue="0" style="left:60px;top:200px">GENERAL</div>')
h.append('<div class="side c-teal" data-cue="0" data-d="0.3" style="left:980px;top:200px">HOT PATH</div>')
h.append(code_html(LEFT, {}, cls="code sm left", style="left:60px;top:240px;width:880px", cue=0, extra=' data-dim="1"'))
h.append(code_html(RIGHT, {8:(1,2),9:(2,3),10:(3,4),11:(3,4),13:(4,5),0:(5,6),1:(5,6),6:(5,6),7:(5,6)}, cls="code sm right", style="left:980px;top:240px;width:880px", cue=0, extra=' data-d="0.3"'))
h.append('<div class="chip red" data-cue="6" style="left:60px;top:810px">2 data jumps · totals in memory</div>')
h.append('<div class="chip teal" data-cue="6" data-d="0.4" style="left:980px;top:810px">15 instr/tick · 0 data-dependent jumps</div>')
h.append('</div>')
# ---------- numbers
h.append('<div class="scene" id="s-numbers">')
h.append('<div class="h2" data-cue="0" style="left:120px;top:110px">ns per tick, p50 (lower is better)</div>')
h.append('<div class="note" data-cue="0" data-d="0.3" style="left:120px;top:190px;width:1700px">measured on a shared 4-vCPU cloud VM · g++ 13 -O2 · 16,384 ticks · pinned · median of 3 runs x 101 passes</div>')
SC = 140; X0 = 560
def bar(y, name, val, col, cue, d=0.0, txt=None):
    h.append(f'<div class="blab" data-cue="{cue}" data-d="{d}" style="left:110px;top:{y}px">{name}</div>')
    h.append(f'<div class="bar grow" data-cue="{cue}" data-d="{d}" data-w="{val*SC:.0f}" data-anim="fade" style="left:{X0}px;top:{y-2}px;background:{col}"></div>')
    h.append(f'<div class="bv" data-cue="{cue}" data-d="{d+0.7}" style="left:{X0+val*SC+16:.0f}px;top:{y-3}px;color:{col}">{txt or val}</div>')
h.append('<div class="gl" data-cue="1" style="left:120px;top:255px">Random side, 50% big</div>')
bar(300, 'general', 7.2, 'var(--red)', 1)
bar(342, 'branchless', 1.04, 'var(--teal)', 2, txt='1.0')
h.append('<div class="chip amber" data-cue="2" data-d="0.8" style="left:900px;top:330px">≈ 7x</div>')
bar(384, 'branches + cold path', 4.9, 'var(--violet)', 3)
h.append('<div class="gl" data-cue="4" style="left:120px;top:450px">Side repeats 80%, 10% big</div>')
bar(495, 'general', 2.4, 'var(--red)', 4)
bar(537, 'branchless', 1.0, 'var(--teal)', 4, 0.3)
h.append('<div class="gl" data-cue="6" style="left:120px;top:605px">Sides in runs of 256, 1% big</div>')
bar(650, 'general', 2.1, 'var(--red)', 6, 0.6)
bar(692, 'branchless', 1.0, 'var(--teal)', 6, 0.9)
bar(734, 'branches + cold path', 0.77, 'var(--violet)', 7)
h.append('<div class="chip teal" data-cue="7" data-d="1.0" style="left:820px;top:722px">branches win when predictable</div>')
bar(776, 'lookup table [side]', 2.3, 'var(--blue)', 8)
h.append('</div>')
# ---------- close
h.append('<div class="scene" id="s-close">')
h.append('<div class="h2" data-cue="0" style="left:120px;top:110px">The missing facts</div>')
cards = [(1, 'var(--amber)', 'How random is the input?', 'aggressor side, size vs threshold'),
         (2, 'var(--amber)', 'Measure on recorded data', 'real flow sits in between · read the asm'),
         (3, 'var(--teal)', 'Rare path: out of line', '[[unlikely]] + a cold, noinline function'),
         (4, 'var(--muted)', 'Cold code: readable branches', 'startup · config · tooling')]
for i, (c, col, t, s) in enumerate(cards):
    x = 120 + (i % 2) * 850; y = 220 + (i // 2) * 190
    h.append(f'<div class="card2" data-cue="{c}" style="left:{x}px;top:{y}px;width:810px;height:160px;border-color:{col}"><div class="ct">{t}</div><div class="cs">{s}</div></div>')
h.append('<div class="rule" data-cue="5" style="left:120px;top:640px;width:1660px">Branchless for unpredictable data. Out of line for rare paths. <span class="c-amber">Let the measurement decide.</span></div>')
h.append('</div>')
open(f'{OUT}/scenes.html', 'w').write('\n'.join(h) + '\n')
css = open('/tmp/claude-0/vx/ai1316tools/common.css').read() + '''
.slot13{position:absolute;width:100px;height:70px;border-radius:10px;border:2px solid var(--line);background:#0f1b23;display:grid;place-items:center;font:700 22px var(--mono);color:#06141a;opacity:0}
'''
open(f'{OUT}/style.css', 'w').write(css)
js = r'''
SCENES['cost'] = { draw(u, cue, H) {
  const t0 = cue(0) + 0.3, tf = cue(2) + 0.3;
  for (let i = 0; i < 15; i++) {
    const el = document.getElementById('cs-' + i);
    let vis = H.C((u - (t0 + 0.12 * i)) / 0.25);
    let bg = i < 5 ? '#4b6b7a' : i === 5 ? 'var(--amber)' : '#2a8f99', bd = bg;
    if (i > 5 && u > tf) {
      if (u < tf + 1.0) { bg = 'var(--red)'; bd = bg; }
      else if (u < tf + 1.6 + 0.12 * (i - 6)) { vis = 0.25; bg = '#0f1b23'; bd = 'var(--red)'; }
      else { bg = '#2a8f99'; bd = bg; vis = H.C((u - (tf + 1.6 + 0.12 * (i - 6))) / 0.25); }
    }
    el.style.opacity = vis; el.style.background = bg; el.style.borderColor = bd;
  }
}};
'''
open(f'{OUT}/scenes.js', 'w').write(js)
print('ok')
