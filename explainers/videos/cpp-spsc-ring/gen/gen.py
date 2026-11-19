import sys, json
sys.path.insert(0, '/tmp/claude-0/vx/cpp-branches-layout')
from cg import code
C = '/tmp/claude-0/vx/cpp-spsc-ring/code/'
def L(f, a, b, path=C):
    return open(path + f).read().split('\n')[a-1:b]
NUM = json.load(open('/tmp/claude-0/vx/cpp-spsc-ring/nums.json'))
O = []; add = O.append
def scene(i): add(f'<div class="scene" id="s-{i}">')
def end(): add('</div>')
def slots(prefix, n, left, top, cue, d=0, step=100):
    for k in range(n):
        add(f'<div class="slot" id="{prefix}{k}" data-cue="{cue}" data-d="{d+0.05*k:.2f}" style="left:{left+step*k}px;top:{top}px">{k}</div>')

# ---------- title
scene('title')
add('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">TRADING LAB · C++ LOW LATENCY</div>')
add('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:210px">An SPSC ring</div>')
add('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:380px;width:1500px">One producer, one consumer, no locks: built step by step, tested, measured.</div>')
add('<div class="box green" data-cue="0" data-d="0.8" style="left:140px;top:560px;width:330px;height:130px"><div class="t">book thread</div><div class="s">producer</div></div>')
add('<div class="box amber" data-cue="0" data-d="1.0" style="left:1450px;top:560px;width:330px;height:130px"><div class="t">trading thread</div><div class="s">consumer</div></div>')
slots('ti-s', 8, 560, 582, 0, 1.2)
add('<div class="lbl" data-cue="0" data-d="1.6" style="left:560px;top:540px">TopOfBook updates</div>')
chips = ['bounded', 'no allocation', 'no system calls', 'no locks']
for k, c in enumerate(chips):
    col = 'var(--teal)' if k < 3 else 'var(--amber)'
    add(f'<div class="tagx" data-cue="1" data-d="{0.5*k:.1f}" style="left:{140+300*k}px;top:770px;border-color:{col};color:{col}">{c}</div>')
end()

# ---------- mutex
scene('mutex')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">First, the obvious version</div>')
add(code(L('mutex_queue.hpp', 7, 18), 0, 'left:120px;top:210px;width:880px', hl={2: (1, 2), 3: (1, 2), 4: (1, 2), 6: (2, 3), 7: (2, 3), 8: (2, 3), 9: (2, 3), 7: (4, None)}, cls='code sm'))
add('<div class="tagx" data-cue="3" style="left:120px;top:720px;border-color:var(--muted);color:#cfdbe2">try_pop: the same, under the same lock</div>')
add('<div class="core" data-cue="4" style="left:1100px;top:260px;border-color:var(--green)">core 1<div class="s">producer</div></div>')
add('<div class="core" data-cue="4" style="left:1550px;top:260px;border-color:var(--amber)">core 2<div class="s">consumer</div></div>')
add('<svg class="full"><path id="mx-bounce" data-cue="4" data-anim="none" d="M 1355 320 L 1545 320" stroke="#33464f" stroke-width="3" fill="none"/></svg>')
add('<div class="pkt" data-cue="4" data-d="0.3" data-path="mx-bounce" data-dur="0.9" data-loop="1" style="background:var(--red);box-shadow:0 0 14px var(--red)"></div>')
add('<div class="lbl c-red" data-cue="4" data-d="0.3" style="left:1330px;top:400px;width:300px;text-align:center">m_: one cache line,<br>locked RMW each call</div>')
add('<div class="box red" data-cue="5" style="left:1100px;top:540px;width:700px;height:150px"><div class="t">contended: futex</div><div class="s">a waiter may sleep in the kernel, then be woken</div></div>')
end()

# ---------- layout
scene('layout')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">The lock-free layout</div>')
add(code(L('ring_simple.hpp', 5, 12), 0, 'left:120px;top:210px;width:960px', hl={2: (1, 2), 3: (1, 2), 5: (3, 4), 6: (3, 4), 7: (4, None)}, cls='code sm'))
add('<div class="box teal" data-cue="1" data-d="0.6" style="left:1150px;top:210px;width:650px;height:110px"><div class="t mono" style="font-size:30px">slot = 13 &amp; 7 = 5</div><div class="s">index &amp; (N − 1): no division</div></div>')
add('<div class="box amber" data-cue="2" data-d="0.4" style="left:1150px;top:345px;width:650px;height:110px"><div class="t mono" style="font-size:30px">full: head − tail == N</div><div class="s">64-bit counters that only grow</div></div>')
lines = [('line A · head_', 'producer writes', 'var(--green)'), ('line B · tail_', 'consumer writes', 'var(--amber)'), ('lines C… · buf_[N]', 'the slots', '#8ea3b1')]
for k, (a, b, col) in enumerate(lines):
    add(f'<div class="cl" data-cue="4" data-d="{0.3*k:.1f}" style="left:1150px;top:{490+56*k}px;width:650px;border-color:{col}"><div style="width:14px;background:{col}"></div><div style="padding:8px 14px;font:600 22px var(--mono);color:#dce8ee;width:620px">{a} <span style="color:var(--muted)">· {b}</span></div></div>')
slots('ly-s', 8, 160, 720, 2, 0, 100)
add('<div class="ptr c-amber" id="ly-tail" data-cue="2" style="left:160px;top:820px">▲ tail</div>')
add('<div class="ptr c-green" id="ly-head" data-cue="2" style="left:160px;top:690px">▼ head</div>')
add('<div class="lbl" id="ly-cnt" data-cue="2" style="left:990px;top:745px"></div>')
end()

# ---------- push
scene('push')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">try_push: write, then publish</div>')
add(code(L('ring.hpp', 5, 7) + [''] + L('ring_simple.hpp', 15, 21), 0, 'left:120px;top:210px;width:930px',
         hl={5: (0, 1), 6: (1, 3), 7: (3, 4), 8: (4, None)}, cls='code sm'))
add('<div class="lbl" data-cue="4" style="left:1160px;top:210px">producer</div><div class="lbl" data-cue="4" style="left:1520px;top:210px">consumer</div>')
add('<div class="flow" data-cue="3" style="left:1120px;top:250px;width:300px;border-color:var(--green)">write slot</div>')
add('<div class="flow" data-cue="4" style="left:1120px;top:400px;width:300px;border-color:var(--green);color:var(--green)">store head<br><span style="font-size:20px">release</span></div>')
add('<div class="flow" data-cue="5" data-d="0.3" style="left:1500px;top:400px;width:300px;border-color:var(--amber);color:var(--amber)">load head<br><span style="font-size:20px">acquire</span></div>')
add('<div class="flow" data-cue="5" data-d="0.9" style="left:1500px;top:580px;width:300px;border-color:var(--amber)">read slot</div>')
add('<svg class="full"><path class="draw" data-cue="4" d="M 1270 320 L 1270 390" stroke="var(--green)" stroke-width="3" fill="none" marker-end="url(#ah-green)"/>'
    '<path class="draw" data-cue="5" data-d="0.4" d="M 1424 440 L 1494 440" stroke="var(--teal)" stroke-width="3" fill="none" marker-end="url(#ah-teal)"/>'
    '<path class="draw" data-cue="5" data-d="1.0" d="M 1650 490 L 1650 570" stroke="var(--amber)" stroke-width="3" fill="none" marker-end="url(#ah-amber)"/></svg>')
add('<div class="lbl c-teal" data-cue="5" data-d="0.6" style="left:1300px;top:500px;width:200px;text-align:center">sees head,<br>sees data</div>')
add('<div class="tagx" data-cue="2" style="left:120px;top:690px;border-color:var(--amber);color:var(--amber)">full → return false: never blocks</div>')
end()

# ---------- pop
scene('pop')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">try_pop: the mirror image</div>')
add(code(L('ring_simple.hpp', 23, 29), 0, 'left:120px;top:210px;width:880px', hl={2: (1, 3), 3: (3, None), 4: (3, None)}, cls='code sm'))
add('<div class="box amber" data-cue="1" data-d="0.5" style="left:1080px;top:210px;width:720px;height:120px"><div class="t" style="font-size:28px">acquire pairs with push\'s release</div><div class="s">slot contents visible before we read them</div></div>')
add('<div class="box" data-cue="2" style="left:1080px;top:360px;width:720px;height:110px;border-color:var(--line)"><div class="t mono" style="font-size:28px">tail == head → empty</div></div>')
slots('pp-s', 8, 160, 650, 0, 0.3, 100)
add('<div class="ptr c-amber" id="pp-tail" data-cue="0" style="left:160px;top:750px">▲ tail</div>')
add('<div class="ptr c-green" id="pp-head" data-cue="0" style="left:160px;top:620px">▼ head</div>')
add('<div class="lbl c-amber" data-cue="3" data-d="0.5" style="left:1000px;top:680px;width:780px">store tail + 1, release: the producer may now reuse the slot</div>')
end()

# ---------- cached
scene('cached')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Cache the other side\'s index</div>')
add(code(L('ring.hpp', 14, 17), 2, 'left:120px;top:200px;width:980px', hl={1: (2, 3), 3: (2, 3)}, cls='code sm'))
add(code(L('ring.hpp', 21, 30), 2, 'left:120px;top:390px;width:980px', hl={2: (3, 4), 3: (3, 4), 4: (3, 4)}, d=0.5, cls='code sm'))
add('<div class="core" data-cue="0" style="left:1170px;top:230px;border-color:var(--green)">producer<div class="s">core 1</div></div>')
add('<div class="core" data-cue="0" style="left:1550px;top:230px;border-color:var(--amber)">consumer<div class="s">core 2</div></div>')
add('<svg class="full"><path id="ca-b1" d="M 1425 270 L 1545 270" stroke="#33464f" stroke-width="2" fill="none"/><path id="ca-b2" d="M 1545 320 L 1425 320" stroke="#33464f" stroke-width="2" fill="none"/></svg>')
add('<div class="pkt" data-cue="1" data-out="2" data-path="ca-b1" data-dur="0.6" data-loop="1" style="background:var(--green)"></div>')
add('<div class="pkt" data-cue="1" data-out="2" data-path="ca-b2" data-dur="0.6" data-loop="1" data-phase="0.5" style="background:var(--amber)"></div>')
add('<div class="lbl c-red" data-cue="1" data-out="2" style="left:1170px;top:380px;width:630px">every call: head_ and tail_ lines move between cores</div>')
add('<div class="lbl c-teal" data-cue="2" data-d="0.4" style="left:1170px;top:380px;width:630px">usually: no read of the other line at all</div>')
add('<div class="box green" data-cue="3" style="left:1170px;top:470px;width:630px;height:120px"><div class="t" style="font-size:26px">producer rereads tail_</div><div class="s">only when cached_tail_ says full</div></div>')
add('<div class="box amber" data-cue="4" style="left:1170px;top:620px;width:630px;height:120px"><div class="t" style="font-size:26px">consumer rereads head_</div><div class="s">only when cached_head_ says empty</div></div>')
end()

# ---------- test
scene('test')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Test it under pressure</div>')
add(code(L('test.cpp', 9, 22), 0, 'left:120px;top:200px;width:900px', hl={1: (1, 2), 2: (1, 2), 3: (1, 2), 7: (2, 3), 8: (2, 3), 9: (2, 3), 12: (2, 3)}, cls='code sm'))
add('<div class="tagx" data-cue="0" data-d="0.6" style="left:1080px;top:210px;border-color:var(--amber);color:var(--amber)">check&lt;Ring&lt;uint64_t, 8&gt;&gt;: wraps constantly</div>')
add(f'<div class="term" data-cue="3" style="position:absolute;left:1080px;top:300px;width:720px">{NUM["test_term"]}</div>')
add(f'<div class="term" data-cue="3" data-d="1.0" style="position:absolute;left:1080px;top:{NUM["tsan_top"]}px;width:720px">{NUM["tsan_term"]}</div>')
end()

# ---------- bench
scene('bench')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">Measured on this box</div>')
add('<div class="lbl" data-cue="0" data-d="0.4" style="left:120px;top:210px">throughput · ns per message · 2 spinning threads · capacity 1024 · uint64_t</div>')
S = NUM['scale']
rows = [('mutex queue', NUM['mutex'], NUM['mutex_txt'], 'var(--red)', 1), ('ring, no cache', NUM['nocache'], NUM['nocache_txt'], 'var(--violet)', 2), ('ring, cached', NUM['cached'], NUM['cached_txt'], 'var(--teal)', 3)]
for k, (nm, v, txt, col, cue) in enumerate(rows):
    add(f'<div class="brow" data-cue="{cue}" style="left:120px;top:{260+70*k}px"><div class="nm" style="width:280px">{nm}</div><div class="b grow" data-cue="{cue}" data-d="0.2" data-w="{max(4,int(v*S))}" style="background:{col}"></div><div class="v" style="color:{col}">{txt}</div></div>')
add('<div class="lbl" data-cue="4" style="left:120px;top:520px">ping-pong round trip · 200k samples</div>')
add(f'<div class="brow" data-cue="4" data-d="0.3" style="left:120px;top:570px"><div class="nm" style="width:280px">ring</div><div class="v c-teal" style="font-size:34px">median {NUM["rt_ring"]} ns</div><div class="foot" style="margin-left:24px">p99 {NUM["rt_ring99"]} ns</div></div>')
add(f'<div class="brow" data-cue="4" data-d="0.8" style="left:120px;top:640px"><div class="nm" style="width:280px">mutex</div><div class="v c-red" style="font-size:34px">median {NUM["rt_mutex"]} ns</div><div class="foot" style="margin-left:24px">p99 {NUM["rt_mutex99"]} ns</div></div>')
add(f'<div class="foot" data-cue="4" data-d="1.2" style="left:120px;top:740px;width:1680px">g++ 13 -O2 · shared 4-vCPU cloud box (KVM), heavily loaded by other jobs · {NUM["runs"]}</div>')
end()

# ---------- lab
scene('lab')
add('<div class="h2" data-cue="0" style="left:120px;top:110px">The lab\'s SpscRing</div>')
LAB = '/home/claude/ts-push/libs/core/include/lab/core/'
add('<div class="lbl" data-cue="0" style="left:120px;top:195px">libs/core/include/lab/core/spsc_ring.hpp</div>')
add(code(L('spsc_ring.hpp', 62, 69, LAB), 0, 'left:120px;top:235px;width:1060px;font-size:22px', hl={2: (0, 1), 3: (0, 1), 4: (0, 1)}, d=0.3, cls='code sm'))
add(code(L('spsc_ring.hpp', 28, 30, LAB), 2, 'left:120px;top:580px;width:1240px;font-size:21px', hl={0: (2, 3), 1: (2, 3), 2: (2, 3)}, cls='code sm'))
diffs = [('64-bit, always lock-free · trivially copyable', 'lives in shared memory, across processes', 2, 'var(--violet)'),
         ('zero-copy API', 'try_claim + commit · front + pop', 3, 'var(--teal)'),
         ('slots zeroed at construction', 'pages faulted in before the hot path', 4, 'var(--green)')]
for k, (t, s, cue, col) in enumerate(diffs):
    top = [235, 380, 760][k]; left = 1230 if k < 2 else 120
    w = 570 if k < 2 else 1240
    add(f'<div class="box" data-cue="{cue}" style="left:{left}px;top:{top}px;width:{w}px;height:120px;border-color:{col}"><div class="t" style="font-size:25px">{t}</div><div class="s">{s}</div></div>')
add('<div class="tagx" data-cue="1" style="left:1230px;top:195px;border-color:var(--amber);color:var(--amber)">same design · three differences</div>')
end()

open('/mnt/project-files/videos/explainers/cpp-spsc-ring/scenes.html', 'w').write('\n'.join(O) + '\n')
print('ok')
