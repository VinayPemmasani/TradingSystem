import sys
sys.path.insert(0, '/tmp/claude-0/vx/cpp-branches-layout')
from cg import code
O = []
add = O.append
def scene(i): add(f'<div class="scene" id="s-{i}">')
def end(): add('</div>')
FOOT = 'g++ 13 -O2 · 64 Ki calls · best of 31 · shared 4-vCPU cloud box'
def bar(nm, v, txt, col, cue, top, S=60, w=330, d=0.3, cc=''):
    add(f'<div class="brow" data-cue="{cue}" data-d="{d}" style="left:120px;top:{top}px"><div class="nm" style="width:{w}px">{nm}</div><div class="b grow" data-cue="{cue}" data-d="{d+0.2}" data-w="{max(4,int(v*S))}" style="background:{col}"></div><div class="v" style="color:{col}">{txt}</div></div>')

STRAT = ['struct Strategy {',
         '  virtual ~Strategy() = default;',
         '  virtual int quote(int mid) const = 0;',
         '};',
         'struct Maker final : Strategy {',
         '  int edge = 2;',
         '  int quote(int mid) const override { return mid - edge; }',
         '};']

# ---------- title
scene('title')
add('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">TRADING LAB · C++ LOW LATENCY</div>')
add('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:210px">Static dispatch</div>')
add('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:380px;width:1500px">virtual · final · templates · variant · choose once</div>')
add('<div class="box amber" data-cue="0" data-d="0.8" style="left:140px;top:600px;width:330px;height:130px"><div class="t">trading thread</div><div class="s">millions of calls</div></div>')
add('<div class="box green" data-cue="0" data-d="1.2" style="left:1450px;top:600px;width:330px;height:130px"><div class="t">quote(mid)</div><div class="s">the strategy</div></div>')
add('<svg class="full">'
    '<path id="ti-v" class="draw" data-cue="1" d="M 470 640 C 760 500 1160 500 1450 640" stroke="var(--red)" stroke-width="4" fill="none" marker-end="url(#ah-red)"/>'
    '<path id="ti-s" class="draw" data-cue="1" data-d="0.6" d="M 470 665 L 1450 665" stroke="var(--teal)" stroke-width="4" fill="none" marker-end="url(#ah-teal)"/>'
    '<path id="ti-a" class="draw" data-cue="1" data-d="1.2" d="M 470 690 C 760 830 1160 830 1450 690" stroke="var(--amber)" stroke-width="4" fill="none" marker-end="url(#ah-amber)"/></svg>')
add('<div class="lbl c-red" data-cue="1" style="left:860px;top:500px">virtual call</div>')
add('<div class="lbl c-teal" data-cue="1" data-d="0.6" style="left:850px;top:625px">direct, inlined</div>')
add('<div class="lbl c-amber" data-cue="1" data-d="1.2" style="left:860px;top:800px">variant + visit</div>')
add('<div class="pkt" data-cue="2" data-path="ti-s" data-dur="1.2" data-loop="1" style="background:var(--teal);box-shadow:0 0 14px var(--teal)"></div>')
add('<div class="pkt" data-cue="2" data-path="ti-v" data-dur="2.4" data-loop="1" style="background:var(--red);box-shadow:0 0 14px var(--red)"></div>')
end()

# ---------- vtable
scene('vtable')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Two loads, then an indirect call</div>')
add(code(STRAT, 0, 'left:120px;top:220px;width:900px', hl={1: (3, 4), 2: (0, 2), 6: (0, 2)}, cls='code sm'))
add('<div class="lbl" data-cue="1" style="left:1080px;top:200px">a Maker object</div>')
add('<div class="bytes" data-cue="1" style="position:absolute;left:1080px;top:236px"><div style="width:200px;background:var(--violet)">vptr · 8 B</div><div style="width:140px;background:#8ea3b1">edge · 4 B</div><div style="width:100px;background:#33464f;color:#cfdbe2">pad</div></div>')
add('<div class="lbl" data-cue="1" data-d="0.6" style="left:1080px;top:380px">Maker\'s vtable</div>')
rows = [('−16', 'offset to top'), ('−8', 'typeinfo'), ('+0', '~Maker() complete'), ('+8', '~Maker() deleting'), ('+16', 'Maker::quote')]
for k, (o, f) in enumerate(rows):
    extra = ' data-hl="3"' if k in (2, 3) else ''
    if k == 4: extra = ' data-hl="2" data-hld="1.2"'
    add(f'<div class="vt" data-cue="1" data-d="{0.7+0.12*k:.2f}"{extra} style="left:1080px;top:{420+54*k}px;width:440px"><div class="o">{o}</div><div class="f">{f}</div></div>')
add('<svg class="full">'
    '<path class="draw" data-cue="1" data-d="1.4" d="M 1180 306 C 1180 380 1040 400 1040 470 L 1074 553" stroke="var(--violet)" stroke-width="3" fill="none" marker-end="url(#ah-violet)"/>'
    '<path class="draw" data-cue="2" data-d="1.6" d="M 1520 661 C 1600 661 1640 700 1640 740" stroke="var(--green)" stroke-width="3" fill="none" marker-end="url(#ah-green)"/></svg>')
add('<div class="box green" data-cue="2" data-d="1.8" style="left:1500px;top:750px;width:300px;height:110px"><div class="t" style="font-size:26px">quote code</div><div class="s">mid - edge</div></div>')
steps = ['1 load vptr', '2 load slot +16', '3 call *16(%rax)']
for k, s in enumerate(steps):
    add(f'<div class="tagx" data-cue="2" data-d="{0.4*k:.1f}" style="left:{120+300*k}px;top:640px;border-color:var(--violet);color:var(--violet)">{s}</div>')
add('<div class="foot" data-cue="3" data-d="0.5" style="left:120px;top:740px;width:900px">Itanium C++ ABI (Linux, g++/clang): the vptr points at the first function slot</div>')
end()

# ---------- asm
scene('asm')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Same loop, two ways</div>')
add('<div class="code sm" data-cue="0" style="left:120px;top:200px;width:1680px;padding:10px 22px"><span class="line"><span class="k">for</span> (<span class="k">int</span> i = <span class="r">0</span>; i &lt; n; ++i) sum += s.quote(mids[i]);</span></div>')
add('<div class="lbl c-red" data-cue="0" data-d="0.4" style="left:120px;top:290px">s is const Strategy&amp; · g++ -O2</div>')
add(code(['# prologue: pushq r13, r12, rbp, rbx',
          '.L16:',
          '  movq  0(%rbp), %rax   # vptr',
          '  movl  (%rbx), %esi    # mid',
          '  movq  %rbp, %rdi      # this',
          '  addq  $4, %rbx',
          '  call  *16(%rax)       # quote',
          '  addl  %eax, %r12d',
          '  cmpq  %r13, %rbx',
          '  jne   .L16'], 0, 'left:120px;top:330px;width:740px', hl={2: (1, 2), 6: (1, 2), 0: (2, 3)}, d=0.4, lang='asm', cls='code sm'))
add('<div class="lbl c-teal" data-cue="3" style="left:960px;top:290px">s is const Maker&amp;, Maker is final</div>')
add(code(['  movl  8(%rdi), %edi   # edge, once',
          '.L22:',
          '  movl  (%rsi), %eax    # mid',
          '  addq  $4, %rsi',
          '  subl  %edi, %eax      # mid - edge',
          '  addl  %eax, %edx',
          '  cmpq  %rcx, %rsi',
          '  jne   .L22'], 3, 'left:960px;top:330px;width:760px', hl={0: (4, 4.5), 2: (4.5, None), 4: (4.5, None), 5: (4.5, None)}, lang='asm', cls='code sm'))
add('<div class="tagx" data-cue="3" data-d="0.6" style="left:960px;top:720px;border-color:var(--teal);color:var(--teal)">no call · no saved registers · nothing reloaded</div>')
end()

# ---------- cost
scene('cost')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">The cost is what the call hides</div>')
items = [('var(--green)', 'vptr and slot loads: L1 hits', 1, 0), ('var(--green)', 'target predicted before the loads finish', 1, 0.6),
         ('var(--red)', 'no inlining: no hoisting, folding or vectorizing', 2, 0), ('var(--red)', 'changing targets: indirect mispredicts', 5, 0)]
for k, (col, t, cue, d) in enumerate(items):
    add(f'<div class="chk" data-cue="{cue}" data-d="{d}" data-anim="left" style="left:140px;top:{220+70*k}px;font-size:32px"><i style="background:{col}"></i>{t}</div>')
add('<div class="lbl" data-cue="4" style="left:120px;top:540px">ns per call · sum of quote(mid) over 64 Ki mids</div>')
bar('virtual, one object', 1.42, '1.4 ns', 'var(--red)', 4, 590, w=400)
bar('inlined (final)', 0.35, '0.35 ns', 'var(--teal)', 4, 655, d=0.8, w=400)
bar('virtual, 2 types random', 10.8, '7.6–10.8 ns', 'var(--red)', 5, 720, d=0.5, w=400)
add(f'<div class="foot" data-cue="5" data-d="1.2" style="left:120px;top:810px">{FOOT} · ranges over 7 runs</div>')
end()

# ---------- final
scene('final')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">final: one possible target</div>')
add(code(STRAT[4:] + ['int run_final(const Maker& s, const int* mids, int n) {',
          '  int sum = 0;',
          '  for (int i = 0; i < n; ++i) sum += s.quote(mids[i]);',
          '  return sum;',
          '}'], 0, 'left:120px;top:210px;width:1000px', hl={0: (0, 1), 6: (1, 3)}, cls='code sm'))
add('<svg class="full"><path class="draw" data-cue="2" data-d="0.3" d="M 470 755 L 620 755" stroke="var(--teal)" stroke-width="3" fill="none" marker-end="url(#ah-teal)"/>'
    '<path class="draw" data-cue="2" data-d="1.2" d="M 1050 755 L 1200 755" stroke="var(--teal)" stroke-width="3" fill="none" marker-end="url(#ah-teal)"/></svg>')
add('<div class="flow" data-cue="1" data-d="0.5" style="left:120px;top:715px;width:350px;border-color:var(--muted)">s.quote(mid)</div>')
add('<div class="flow" data-cue="2" data-d="0.5" style="left:630px;top:715px;width:420px;border-color:var(--teal);color:var(--teal)">call Maker::quote</div>')
add('<div class="flow" data-cue="2" data-d="1.4" style="left:1210px;top:715px;width:590px;border-color:var(--green);color:var(--green)">inline: subl %edi, %eax</div>')
add('<div class="box teal" data-cue="3" style="left:1180px;top:240px;width:620px;height:130px"><div class="t">devirtualization</div><div class="s">virtual call → direct call → inlined</div></div>')
add('<div class="box" data-cue="4" style="left:1180px;top:400px;width:620px;height:150px;border-color:var(--line)"><div class="lbl">also when the type is visible</div><div class="t mono" style="font-size:24px;margin-top:8px">Maker m; Strategy&amp; s = m;<br>s.quote(x);  // direct</div></div>')
end()

# ---------- templates
scene('templates')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Templates, concepts, CRTP</div>')
add(code(['template <class S>',
          'concept Quoter = requires(const S& s, int mid) {',
          '  { s.quote(mid) } -> std::same_as<int>;',
          '};',
          'template <Quoter S>',
          'int run_static(const S& s, const int* mids, int n) {',
          '  int sum = 0;',
          '  for (int i = 0; i < n; ++i) sum += s.quote(mids[i]);',
          '  return sum;',
          '}'], 0, 'left:120px;top:220px;width:880px', hl={4: (0, 2), 5: (0, 2), 7: (1, 2), 1: (2, 3), 2: (2, 3)}, cls='code sm'))
add('<div class="tagx" data-cue="1" data-d="0.5" style="left:120px;top:660px;border-color:var(--teal);color:var(--teal)">run_static&lt;Maker&gt;</div>')
add('<div class="tagx" data-cue="1" data-d="0.9" style="left:420px;top:660px;border-color:var(--teal);color:var(--teal)">run_static&lt;Taker&gt;</div>')
add('<div class="lbl" data-cue="1" data-d="1.2" style="left:120px;top:720px">one copy per type, each with direct calls</div>')
add('<div class="lbl" data-cue="3" style="left:1000px;top:190px">CRTP</div>')
add(code(['template <class D>',
          'struct Base {',
          '  int quote(int mid) const {',
          '    return static_cast<const D*>(this)->impl(mid);',
          '  }',
          '};',
          'struct Crtp : Base<Crtp> {',
          '  int impl(int mid) const { return mid - 2; }',
          '};'], 3, 'left:1000px;top:220px;width:760px', hl={3: (3, None)}, cls='code sm'))
end()

# ---------- variant
scene('variant')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">std::variant: a closed set, inline</div>')
add(code(['using AnyStrategy = std::variant<Maker, Taker>;',
          '',
          'int run_variant(const AnyStrategy* objs,',
          '                const int* mids, int n) {',
          '  int sum = 0;',
          '  for (int i = 0; i < n; ++i)',
          '    sum += std::visit([&](const auto& s) {',
          '      return s.quote(mids[i]); }, objs[i]);',
          '  return sum;',
          '}'], 0, 'left:120px;top:220px;width:780px', hl={0: (0, 1), 6: (1, 2), 7: (1, 2)}, cls='code sm'))
add('<div class="lbl" data-cue="0" data-d="0.8" style="left:960px;top:200px">one AnyStrategy · 24 bytes</div>')
add('<div class="bytes" data-cue="0" data-d="0.8" style="position:absolute;left:960px;top:236px"><div style="width:400px;background:var(--violet)">Maker or Taker · 16 B</div><div style="width:110px;background:var(--amber)">index</div><div style="width:200px;background:#33464f;color:#cfdbe2">pad</div></div>')
add(code(['.L41:',
          '  movzbl 8(%rdi), %eax  # index',
          '  cmpb   $-1, %al       # valueless?',
          '  je     .L44           # cold',
          '  testb  %al, %al       # Maker?',
          '  je     .L47'], 1, 'left:960px;top:340px;width:740px', hl={1: (1, 2), 4: (1, 2), 5: (1, 2)}, d=0.4, lang='asm', cls='code sm'))
add('<div class="lbl" data-cue="2" style="left:120px;top:660px">ns per call</div>')
bar('variant, random', 5.0, '4.7–5.0 ns', 'var(--amber)', 2, 700, w=300)
bar('variant, one type', 0.76, '0.75 ns', 'var(--amber)', 3, 765, w=300)
add('<div class="foot" data-cue="2" data-d="0.8" style="left:960px;top:640px;width:840px">virtual, 2 types random: 7.6–10.8 ns</div>')
end()

# ---------- startup
scene('startup')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Choose once, then run monomorphic</div>')
add(code(['// at startup',
          'AnyStrategy chosen = cfg.maker ? AnyStrategy{Maker{}}',
          '                               : AnyStrategy{Taker{}};',
          '',
          'int run_chosen(const AnyStrategy& chosen,',
          '               const int* mids, int n) {',
          '  return std::visit([&](const auto& s) {',
          '    return run_static(s, mids, n);  // monomorphic',
          '  }, chosen);',
          '}'], 0, 'left:120px;top:220px;width:900px', hl={1: (1, 2), 2: (1, 2), 6: (1, 2), 7: (2, None)}, cls='code sm'))
fl = [('config', 'var(--muted)', 1, 0.0), ('build the strategy', 'var(--amber)', 1, 0.6), ('visit once', 'var(--amber)', 1, 1.2)]
for k, (t, col, cue, d) in enumerate(fl):
    add(f'<div class="flow" data-cue="{cue}" data-d="{d}" style="left:1180px;top:{220+110*k}px;width:500px;border-color:{col}">{t}</div>')
add('<svg class="full"><path class="draw" data-cue="1" data-d="0.4" d="M 1430 290 L 1430 325" stroke="var(--muted)" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
    '<path class="draw" data-cue="1" data-d="1.0" d="M 1430 400 L 1430 435" stroke="var(--muted)" stroke-width="3" fill="none" marker-end="url(#ah)"/>'
    '<path class="draw" data-cue="2" data-d="0.0" d="M 1430 510 L 1430 555" stroke="var(--teal)" stroke-width="3" fill="none" marker-end="url(#ah-teal)"/>'
    '<path id="st-loop" data-cue="2" data-anim="none" d="M 1250 700 C 1250 620 1610 620 1610 700 C 1610 780 1250 780 1250 700" fill="none" stroke="var(--teal)" stroke-width="2" stroke-dasharray="6 8"/></svg>')
add('<div class="flow" data-cue="2" data-d="0.3" style="left:1260px;top:665px;width:340px;border-color:var(--teal);color:var(--teal)">hot loop</div>')
add('<div class="pkt" data-cue="2" data-d="0.5" data-path="st-loop" data-dur="1.4" data-loop="1" style="background:var(--teal);box-shadow:0 0 14px var(--teal)"></div>')
add('<div class="lbl" data-cue="2" data-d="0.8" style="left:1180px;top:810px;width:620px">same load · subl · addl loop as final Maker</div>')
bar('visit once, then loop', 0.35, '0.35 ns per call', 'var(--teal)', 3, 700, S=120, w=300)
end()

# ---------- lab
scene('lab')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">In the lab</div>')
strs = [('MarketMaker', 'quote()'), ('PairsTrader', 'on_sample()'), ('TrendFollower', 'on_close()'), ('ThesisTrader', 'on_day()')]
for k, (n, f) in enumerate(strs):
    add(f'<div class="box green" data-cue="0" data-d="{0.5+0.25*k:.2f}" style="left:{120+425*k}px;top:220px;width:395px;height:110px"><div class="t" style="font-size:28px">{n}</div><div class="s">{f}</div></div>')
add('<div class="lbl" data-cue="0" data-d="1.6" style="left:120px;top:345px">firm/strategy · header-only · no base class · no virtual</div>')
add(code(['// firm/trader/trading.hpp',
          'lab::strategy::MarketMaker maker_;',
          '// firm/trader/trading.cpp, Trading::reconcile',
          'auto q = maker_.quote(m, oms_.position(i).shares);'], 1, 'left:120px;top:400px;width:960px', hl={1: (1, 2), 3: (1, 2)}, cls='code sm'))
add('<div class="box" data-cue="1" data-d="1.5" style="left:1130px;top:400px;width:670px;height:130px;border-color:var(--teal)"><div class="t" style="font-size:26px">tools/quant-lab</div><div class="s">mm_, pairs_, trend_, thesis_: plain members</div></div>')
add('<div class="box amber" data-cue="2" style="left:120px;top:620px;width:960px;height:150px"><div class="lbl">objdump -dr trading.cpp.o · release build, -O3 -march=native</div><div class="t mono" style="font-size:26px;margin-top:10px">reconcile: call work_side ×3 · call quote ×0</div></div>')
add('<div class="box" data-cue="3" style="left:1130px;top:620px;width:670px;height:150px;border-color:var(--line)"><div class="lbl">libs/vendor · class Session</div><div class="t mono" style="font-size:24px;margin-top:10px">virtual on_bytes, on_update</div><div class="s">vendor servers, off the hot path</div></div>')
end()

open('/mnt/project-files/videos/explainers/cpp-static-dispatch/scenes.html', 'w').write('\n'.join(O) + '\n')
print('ok')
