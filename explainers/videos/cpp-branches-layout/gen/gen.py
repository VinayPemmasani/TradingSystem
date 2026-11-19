import sys, math
sys.path.insert(0, '/tmp/claude-0/vx/cpp-branches-layout')
from cg import code
O = []
def add(s): O.append(s)
def scene(i): add(f'<div class="scene" id="s-{i}">')
def end(): add('</div>')
FOOT = 'g++ 13 -O2 · shared 4-vCPU cloud box (KVM, Xeon 2.1 GHz) · best of several runs'

# ---------- title
scene('title')
add('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">TRADING LAB · C++ LOW LATENCY</div>')
add('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:210px;width:1700px">Branches and data layout</div>')
add('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:380px;width:1500px">What stalls a fast core, measured with g++ -O2 on this box.</div>')
add('<svg class="full"><path id="ti-run" d="M 150 560 L 1770 560" stroke="#33464f" stroke-width="3" fill="none"/></svg>')
names = ['mov','add','cmp','jae','mov','add','ld','mul','st','add','cmp','jne']
for k, n in enumerate(names):
    c = 'br' if n == 'jae' else ('ld' if n == 'ld' else '')
    add(f'<div class="ins {c}" data-cue="0" data-d="{0.6+0.07*k:.2f}" style="left:{150+136*k}px;top:590px">{n}</div>')
add('<div class="pkt" data-cue="0" data-d="1.2" data-path="ti-run" data-dur="3" data-loop="1" style="background:var(--teal);box-shadow:0 0 16px var(--teal)"></div>')
add('<svg class="full"><path class="draw" data-cue="1" data-d="1.2" d="M 613 660 L 613 720" stroke="var(--red)" stroke-width="3" fill="none" marker-end="url(#ah-red)"/>'
    '<path class="draw" data-cue="1" data-d="2.2" d="M 1021 660 L 1021 720" stroke="var(--amber)" stroke-width="3" fill="none" marker-end="url(#ah-amber)"/></svg>')
add('<div class="card" data-cue="1" data-d="1.2" style="left:430px;top:730px;border-color:var(--red)">branch guessed wrong<div class="s">flush and refetch</div></div>')
add('<div class="card" data-cue="1" data-d="2.2" style="left:900px;top:730px;border-color:var(--amber)">data not in cache<div class="s">every later use waits</div></div>')
add('<div class="lbl" data-cue="2" style="left:1380px;top:760px;width:420px;color:var(--teal)">sorted vs unsorted · branchless · likely · AoS vs SoA · L1/L2 · pointers</div>')
end()

# ---------- predict
scene('predict')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Guess first, check later</div>')
add('<div class="box amber" data-cue="0" style="left:120px;top:420px;width:280px;height:140px"><div class="t">branch</div><div class="s">cmp · jae .L3</div></div>')
add('<svg class="full">'
    '<path class="draw" data-cue="0" data-d="0.6" d="M 400 470 C 480 470 470 330 560 330 L 1440 330" stroke="var(--teal)" stroke-width="4" fill="none"/>'
    '<path class="draw" data-cue="2" data-d="1.0" d="M 400 520 C 480 520 470 650 560 650 L 1440 650" stroke="var(--green)" stroke-width="4" fill="none"/>'
    '</svg>')
add('<div class="lbl c-teal" data-cue="0" data-d="0.8" style="left:560px;top:240px">predicted path · speculative</div>')
spec = ['add','mov','ld','mul','st','add','cmp','jne']
for k, n in enumerate(spec):
    add(f'<div class="ins" data-cue="0" data-d="{1.0+0.15*k:.2f}" style="left:{560+108*k}px;top:298px;width:96px">{n}</div>')
add('<div class="box green" data-cue="1" style="left:120px;top:700px;width:420px;height:170px"><div class="lbl">branch history</div>'
    '<div class="t mono" style="margin-top:10px;font-size:30px">T T N T T N T T <span class="c-green">?</span></div><div class="s">pattern learned: next is N</div></div>')
add('<div class="flush" data-cue="2" data-anim="scale" style="left:548px;top:284px;width:880px;height:92px">FLUSHED</div>')
add('<div class="lbl c-green" data-cue="2" data-d="0.9" style="left:560px;top:560px">actual path · refetched</div>')
for k, n in enumerate(['mov','add','ret']):
    add(f'<div class="ins ok" data-cue="2" data-d="{1.5+0.2*k:.2f}" style="left:{560+108*k}px;top:618px;width:96px">{n}</div>')
add('<div class="big c-red" data-cue="3" style="left:1480px;top:370px"><span class="count" data-cue="3" data-from="0" data-to="15" data-dur="1">0</span>–20</div>')
add('<div class="h3" data-cue="3" data-d="0.3" style="left:1484px;top:520px;width:380px">cycles per mispredict</div>')
add('<div class="lbl" data-cue="3" data-d="0.5" style="left:1484px;top:640px;width:380px">typical, current x86 cores</div>')
end()

# ---------- sorted
scene('sorted')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Same work, sorted or not</div>')
add(code(['size_t keep_branchy(const u8* in,',
          '                    size_t n, u8* out) {',
          '  size_t k = 0;',
          '  for (size_t i = 0; i < n; ++i)',
          '    if (in[i] >= 128) out[k++] = in[i];',
          '  return k;',
          '}'], 0, 'left:120px;top:220px;width:800px', hl={4: (0, None)}, cls='code sm'))
add('<div class="tagx" data-cue="0" data-d="1.2" style="left:120px;top:540px;border-color:var(--amber);color:var(--amber)">asm: testb %al, %al · jns .L3   the branch</div>')
import random
random.seed(5)
vals = [random.randrange(256) for _ in range(24)]
add('<div class="lbl" data-cue="1" style="left:1010px;top:220px">unsorted · taken?</div>')
for k, v in enumerate(vals):
    add(f'<div class="bit {"k" if v>=128 else "n"}" data-cue="1" data-d="{0.3+0.04*k:.2f}" style="left:{1010+33*k}px;top:260px"></div>')
add('<div class="lbl" data-cue="2" style="left:1010px;top:340px">sorted · taken?</div>')
for k, v in enumerate(sorted(vals)):
    add(f'<div class="bit {"k" if v>=128 else "n"}" data-cue="2" data-d="{0.3+0.04*k:.2f}" style="left:{1010+33*k}px;top:380px"></div>')
add('<div class="lbl" data-cue="1" data-d="1.4" style="left:1010px;top:450px;color:var(--red)">coin flip: half mispredict</div>')
add('<div class="lbl" data-cue="2" data-d="1.4" style="left:1430px;top:450px;color:var(--green)">one switch, then right</div>')
S = 120  # px per ns
add(f'<div class="brow" data-cue="1" data-d="0.5" style="left:120px;top:640px"><div class="nm">unsorted</div><div class="b grow" data-cue="1" data-d="0.5" data-w="{int(4.78*S)}" style="background:var(--red)"></div><div class="v c-red">4.78 ns</div></div>')
add(f'<div class="brow" data-cue="2" data-d="0.5" style="left:120px;top:710px"><div class="nm">sorted</div><div class="b grow" data-cue="2" data-d="0.5" data-w="{int(0.52*S)}" style="background:var(--green)"></div><div class="v c-green">0.52 ns</div></div>')
add('<div class="lbl" data-cue="1" style="left:400px;top:600px">per element · 64 Ki random bytes · half kept</div>')
add('<div class="box red" data-cue="3" style="left:1180px;top:620px;width:620px;height:150px"><div class="t" style="font-size:44px">≈ 8.5 ns</div><div class="s">per mispredict: (4.78 − 0.52) / 0.5</div></div>')
add(f'<div class="foot" data-cue="3" data-d="0.6" style="left:120px;top:800px">{FOOT}</div>')
end()

# ---------- branchless
scene('branchless')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Branchless: nothing to guess</div>')
add(code(['size_t keep_branchless(const u8* in,',
          '                       size_t n, u8* out) {',
          '  size_t k = 0;',
          '  for (size_t i = 0; i < n; ++i) {',
          '    out[k] = in[i];        // always store',
          '    k += (in[i] >= 128);   // advance 0 or 1',
          '  }',
          '  return k;',
          '}'], 0, 'left:120px;top:220px;width:800px', hl={4: (0, 1), 5: (0.5, 1)}, cls='code sm'))
add('<div class="lbl" data-cue="1" style="left:1000px;top:200px">g++ -O2 -S · the loop</div>')
add(code(['.L10:',
          '  movsbq (%rdi), %rax',
          '  addq   $1, %rdi',
          '  movb   %al, (%rdx,%rcx)',
          '  shrq   $63, %rax',
          '  addq   %rax, %rcx',
          '  cmpq   %rsi, %rdi',
          '  jne    .L10'], 1, 'left:1000px;top:240px;width:470px', hl={4: (1, 3), 5: (1, 3), 7: (1.5, 3)}, lang='asm', cls='code sm'))
add('<div class="tagx" data-cue="1" data-d="0.3" style="left:1500px;top:418px;border-color:var(--amber);color:var(--amber)">sign bit → 0 or 1</div>')
add('<div class="tagx" data-cue="1.5" style="left:1500px;top:538px;border-color:var(--teal);color:var(--teal)">only jump: the loop</div>')
S = 120
add(f'<div class="brow" data-cue="2" style="left:120px;top:660px"><div class="nm">unsorted</div><div class="b grow" data-cue="2" data-d="0.3" data-w="{int(0.35*S)}" style="background:var(--teal)"></div><div class="v c-teal">0.35 ns</div><div class="foot" style="margin-left:30px">was 4.78</div></div>')
add(f'<div class="brow" data-cue="2" data-d="0.4" style="left:120px;top:730px"><div class="nm">sorted</div><div class="b grow" data-cue="2" data-d="0.7" data-w="{int(0.35*S)}" style="background:var(--teal)"></div><div class="v c-teal">0.35 ns</div><div class="foot" style="margin-left:30px">was 0.52</div></div>')
add('<div class="box violet" data-cue="3" style="left:1000px;top:630px;width:800px;height:150px"><div class="lbl">if (v[i] >= 128) sum += v[i];</div><div class="t mono" style="font-size:30px;margin-top:8px">testb %cl, %cl · <span class="c-violet">cmovs</span> %rax, %rdx</div><div class="s">g++ -O2 made the plain sum branchless itself</div></div>')
add(f'<div class="foot" data-cue="2" data-d="1" style="left:120px;top:810px">{FOOT}</div>')
end()

# ---------- likely
scene('likely')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">[[likely]] moves code, not predictions</div>')
src = lambda a: ['void reject(int);',
          'int on_order(int qty, int limit) {',
          f'  if (qty > limit) [[{a}]] {{',
          '    reject(qty);',
          '    return -1;',
          '  }',
          '  return qty * 2;',
          '}']
add(code(src('unlikely'), 0, 'left:120px;top:230px;width:760px', hl={2: (0, 1)}, extra='data-out="4"'))
add(code(src('likely'), 4, 'left:120px;top:230px;width:760px', hl={2: (4, None)}, extra='data-anim="fade"'))
add('<div class="tagx" data-cue="1" style="left:120px;top:640px;border-color:var(--muted);color:#cfdbe2">same cmpl + conditional jump · no hint prefix · predictor learns at run time</div>')
add('<div class="lbl" data-cue="2" data-out="4" style="left:1000px;top:190px">with [[unlikely]]</div>')
add(code(['  cmpl  %esi, %edi',
          '  jg    .L10',
          '  leal  (%rdi,%rdi), %eax',
          '  ret',
          '.L10:',
          '  subq  $8, %rsp',
          '  call  _Z6rejecti@PLT',
          '  movl  $-1, %eax',
          '  addq  $8, %rsp',
          '  ret'], 2, 'left:1000px;top:230px;width:560px', hl={2: (3, 4), 3: (3, 4)}, lang='asm', cls='code sm', extra='data-out="4"'))
add('<div class="tagx" data-cue="3" data-out="4" style="left:1590px;top:300px;border-color:var(--green);color:var(--green)">hot path falls through</div>')
add('<div class="tagx" data-cue="3" data-d="0.8" data-out="4" style="left:1590px;top:470px;border-color:var(--muted);color:#cfdbe2">cold, out of line</div>')
add('<div class="lbl" data-cue="4" style="left:1000px;top:190px">with [[likely]]: jle .L2, reject path first</div>')
add(code(['  cmpl  %esi, %edi',
          '  jle   .L2',
          '  subq  $8, %rsp',
          '  call  _Z6rejecti@PLT',
          '  ...'], 4, 'left:1000px;top:230px;width:560px', hl={1: (4, None), 3: (4, None)}, lang='asm', cls='code sm', extra='data-anim="fade"'))
end()

# ---------- aos
scene('aos')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Hot fields together, cold fields apart</div>')
add(code(['struct Order {                 // 64 bytes',
          '  uint32_t price, qty;         // hot',
          '  uint64_t id, ts_in, ts_ack;  // cold ...',
          '  char account[16], symbol[8], pad[8];',
          '};',
          'struct Hot { uint32_t price, qty; };  // 8 bytes'], 0, 'left:120px;top:220px;width:820px', hl={1: (0, 2), 5: (3, 4)}, cls='code sm'))
add('<div class="lbl" data-cue="1" style="left:1010px;top:215px">array of structs: 1 hot order per 64 B line</div>')
for r in range(4):
    add(f'<div class="cl" data-cue="1" data-d="{0.2+0.15*r:.2f}" style="left:1010px;top:{255+58*r}px;width:768px"><div class="h" style="width:96px"></div><div class="c" style="width:672px"></div></div>')
add('<div class="lbl" data-cue="3" style="left:1010px;top:510px">hot array: 8 orders per 64 B line</div>')
add('<div class="cl" data-cue="3" data-d="0.2" style="left:1010px;top:550px;width:768px">' + ''.join('<div class="h" style="width:94px;margin-right:2px"></div>' for _ in range(8)) + '</div>')
S = 100
rows = [('array of structs', 'var(--red)', 4.9, '≈ 5 ns (4.3–5.8)', 2, 'c-red'), ('hot / cold split', 'var(--amber)', 0.51, '0.51 ns', 3, 'c-amber'), ('struct of arrays', 'var(--green)', 0.43, '0.43 ns', 4, 'c-green')]
for k, (nm, col, v, txt, cue, cc) in enumerate(rows):
    add(f'<div class="brow" data-cue="{cue}" data-d="0.4" style="left:120px;top:{650+64*k}px"><div class="nm" style="width:300px">{nm}</div><div class="b grow" data-cue="{cue}" data-d="0.5" data-w="{max(4,int(v*S))}" style="background:{col}"></div><div class="v {cc}">{txt}</div></div>')
add('<div class="lbl" data-cue="2" style="left:440px;top:612px">sum price × qty over 1 Mi orders · per order · 64 MB vs 8 MB read</div>')
end()

# ---------- ws
scene('ws')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Latency by working set</div>')
add('<div class="code sm" data-cue="0" data-d="0.6" style="left:1240px;top:220px;width:560px"><span class="line"><span class="c">// each load waits for the last</span></span><span class="line"><span class="k">for</span> (...) p = p-&gt;next;</span></div>')
rows = [('32 KB', 'fits L1 (48 KB/core)', 3.2, 4.4, 2, 'var(--green)'), ('1 MB', 'fits L2 (2 MB/core)', 13, 21, 3, 'var(--teal)'),
        ('4 MB', 'past L2', 67, 67, 4, 'var(--amber)'), ('32 MB', 'past L2', 250, 304, 4, 'var(--red)'), ('1 GB', 'DRAM + page walks', 392, 392, 4, 'var(--red)')]
W = lambda ns: int(140 + 420 * math.log10(ns))
for k, (nm, sub, lo, hi, cue, col) in enumerate(rows):
    txt = f'{lo:g}–{hi:g} ns' if hi != lo else f'{lo:g} ns'
    add(f'<div class="brow" data-cue="{cue}" data-d="{0.25*k if cue==4 else 0.2:.2f}" {"data-hl=\"5\"" if cue<4 else ""} style="left:120px;top:{330+90*k}px;padding:8px 14px;border-radius:12px"><div class="nm" style="width:150px">{nm}</div><div class="b grow" data-cue="{cue}" data-d="{0.25*k if cue==4 else 0.2:.2f}" data-w="{W(hi)}" style="background:{col}"></div><div class="v">{txt}</div><div class="foot">{sub}</div></div>')
add('<div class="lbl" data-cue="1" style="left:290px;top:290px">ns per dependent load, random order, 64 B nodes · log scale</div>')
add(f'<div class="foot" data-cue="4" data-d="1.2" style="left:120px;top:800px">{FOOT} · 4 KB pages · ranges over 3 runs</div>')
end()

# ---------- chase
scene('chase')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Walk arrays, not pointers</div>')
add('<div class="lbl" data-cue="1" style="left:120px;top:215px">std::vector&lt;int&gt;: contiguous, the prefetcher runs ahead</div>')
add('<svg class="full"><path id="ch-vec" d="M 150 285 L 1060 285" fill="none" stroke="none"/>'
    '<path id="ch-list" class="draw" data-cue="2" data-d="0.2" data-dur="2.5" d="M 166 455 L 586 585 L 336 405 L 966 495 L 506 625 L 1166 425 L 806 585 L 1346 525" stroke="var(--violet)" stroke-width="3" fill="none" marker-end="url(#ah-violet)"/></svg>')
for k in range(16):
    add(f'<div class="vc" data-cue="1" data-d="{0.03*k:.2f}" style="left:{120+60*k}px;top:256px"></div>')
add('<div class="pkt" data-cue="1" data-d="0.6" data-path="ch-vec" data-dur="1.2" data-loop="1" style="background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>')
add('<div class="lbl" data-cue="2" style="left:120px;top:340px;color:var(--violet)">std::list&lt;int&gt;: scattered nodes</div>')
pts = [(166,455),(586,585),(336,405),(966,495),(506,625),(1166,425),(806,585),(1346,525)]
for k, (x, y) in enumerate(pts):
    add(f'<div class="node" data-cue="2" data-d="{0.3*k:.2f}" style="left:{x-46}px;top:{y-29}px">next</div>')
add('<div class="pkt" data-cue="4" data-path="ch-list" data-dur="5" data-loop="1" style="background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>')
add('<div class="box violet" data-cue="4" style="left:1440px;top:400px;width:360px;height:160px"><div class="t" style="font-size:28px">load → address → load</div><div class="s">no overlap, full miss each hop</div></div>')
S = 2.2
rows = [('vector', 0.19, '0.19 ns', 'var(--teal)', 1, 'c-teal'), ('list', 265, '230–270 ns', 'var(--violet)', 2, 'c-violet'), ('map', 315, '285–315 ns', 'var(--pink)', 3, 'c-pink')]
for k, (nm, v, txt, col, cue, cc) in enumerate(rows):
    add(f'<div class="brow" data-cue="{cue}" data-d="0.6" style="left:120px;top:{705+58*k}px"><div class="nm" style="width:120px">{nm}</div><div class="b grow" data-cue="{cue}" data-d="0.8" data-w="{max(4,int(v*S))}" style="background:{col}"></div><div class="v {cc}">{txt}</div></div>')
add('<div class="lbl" data-cue="1" data-d="0.6" style="left:120px;top:668px">sum 1 Mi ints · ns per element</div>')
add('<div class="foot" data-cue="3" data-d="1.2" style="left:1000px;top:880px">nodes allocated or spliced in random order · ranges over 3 runs</div>')
end()

# ---------- close
scene('close')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Checklist</div>')
items = [('var(--amber)', 'Hot branches: predictable, or branchless. Read the -S output.', 0),
         ('var(--violet)', '[[likely]] / [[unlikely]]: code layout, not prediction', 1),
         ('var(--teal)', 'Hot fields together; cold fields in a side table', 2),
         ('var(--green)', 'Working set sized for L1 and L2', 3),
         ('var(--pink)', 'Flat arrays and sorted vectors over lists and maps', 3.5),
         ('var(--blue)', 'Measure on your own machine; these came from a shared cloud box', 4)]
for k, (col, t, cue) in enumerate(items):
    add(f'<div class="chk" data-cue="{cue}" data-anim="left" style="left:140px;top:{240+95*k}px"><i style="background:{col}"></i>{t}</div>')
end()

open('/mnt/project-files/videos/explainers/cpp-branches-layout/scenes.html', 'w').write('\n'.join(O) + '\n')
print('ok', len(O))
