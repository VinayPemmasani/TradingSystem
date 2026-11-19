# Generates scenes.html for cpp-memory-order.
OUT = "/mnt/project-files/videos/explainers/cpp-memory-order/scenes.html"
H = []
def a(s): H.append(s)

def code(lines, x, y, w, cue=0, size=25, d=0, extra=""):
    out = []
    for ln in lines:
        if isinstance(ln, tuple):
            end = f' data-hlend="{ln[2]}"' if len(ln) > 2 else ""
            out.append(f'<span class="line" data-hl="{ln[1]}"{end}>{ln[0]}</span>')
        else:
            out.append(f'<span class="line">{ln}</span>')
    return f'<div class="code" data-cue="{cue}" data-d="{d}" {extra} style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px">' + "".join(out) + "</div>"

K = lambda s: f'<span class="k">{s}</span>'
R = lambda s: f'<span class="r">{s}</span>'
C = lambda s: f'<span class="c">{s}</span>'
V = lambda s: f'<span class="v">{s}</span>'
G = lambda s: f'<span class="g">{s}</span>'
X = lambda s: f'<span class="x">{s}</span>'

# ---------------- title
a('<div class="scene" id="s-title">')
a('<div class="eyebrow" data-cue="0" style="left:140px;top:150px">TRADING LAB · LOW-LATENCY C++</div>')
a('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:200px">Memory ordering</div>')
a('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:360px;width:1500px">Acquire, release, and what your CPU is allowed to do.</div>')
a('<div class="box teal" data-cue="0" data-d="0.8" style="left:140px;top:520px;width:560px;height:300px"><div class="t">Thread 1 · producer</div>'
  '<div class="s" style="margin-top:22px">msg.price = 101250</div><div class="s">msg.qty&#160;&#160; = 300</div><div class="s c-amber">ready&#160;&#160;&#160;&#160; = true</div></div>')
a('<div class="box violet" data-cue="1" style="left:1220px;top:520px;width:560px;height:300px"><div class="t">Thread 2 · consumer</div>'
  '<div class="s c-amber" style="margin-top:22px">if (ready)</div><div class="s">&#160;&#160;use(msg.price)</div></div>')
a('<div class="flag" data-cue="0" data-d="1.4" style="left:860px;top:610px">ready</div>')
a('<svg class="full"><path id="ti-p" class="draw" data-cue="1" data-d="0.3" d="M 705 660 L 1210 660" stroke="var(--amber)" stroke-width="4" fill="none" marker-end="url(#ah-amber)"/></svg>')
a('<div class="tag c-red" data-cue="2" data-anim="scale" style="left:1300px;top:850px;font-size:26px;border-color:var(--red)">price = ??? (stale)</div>')
a('</div>')

# ---------------- publish
a('<div class="scene" id="s-publish">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Publish with a flag: the naive version</div>')
a(code([
    f'{K("struct")} {V("Msg")} {{ {K("long")} price; {K("int")} qty; }};',
    f'Msg msg;',
    (f'{K("bool")} ready = {K("false")};              {C("// plain bool: a data race")}', 3),
    '',
    (f'{K("void")} publish({K("long")} p, {K("int")} q) {{    {C("// thread 1")}', 1, 2),
    ('  msg.price = p;', 1, 2),
    ('  msg.qty = q;', 1, 2),
    ('  ready = <span class="k">true</span>;', 1),
    '}',
    (f'{K("long")} consume() {{                 {C("// thread 2")}', 2, 3),
    (f'  {K("while")} (!ready) {{}}              {C("// spin until published")}', 2),
    (f'  {K("return")} msg.price;', 2),
    '}',
], 120, 210, 980, cue=0, size=26))
a('<div class="lbl c-muted" data-cue="0" data-d="0.6" style="left:120px;top:870px">compiles cleanly with g++ 13.3 -O2 -Wall · it is still wrong</div>')
# memory cells
a('<div class="lbl" data-cue="1" style="left:1220px;top:230px">SHARED MEMORY</div>')
for k, (nm, val, cue, col) in enumerate([("msg.price", "p", 1, "var(--teal)"), ("msg.qty", "q", 1, "var(--teal)"), ("ready", "true", 1.6, "var(--amber)")]):
    y = 280 + k * 110
    a(f'<div class="mem" data-cue="1" style="left:1220px;top:{y}px"><span class="mn">{nm}</span></div>')
    a(f'<div class="mv mono" data-cue="{cue}" data-d="{0.3*k}" style="left:1560px;top:{y+18}px;color:{col}">{val}</div>')
a('<div class="tag c-violet" data-cue="2" style="left:1220px;top:640px;font-size:24px;border-color:var(--violet)">thread 2: sees ready → reads price</div>')
a('<div class="promise" data-cue="3" style="left:1220px;top:720px;width:580px">if <span class="c-amber">ready</span> is true,<br>then <span class="c-teal">msg</span> is complete</div>')
a('</div>')

# ---------------- reorder
a('<div class="scene" id="s-reorder">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Two layers can reorder</div>')
a('<div class="box blue" data-cue="1" style="left:120px;top:220px;width:800px;height:620px"><div class="t c-blue">1 · The compiler</div></div>')
a('<div class="body" data-cue="2" style="left:160px;top:300px;width:720px;font-size:27px">A data race is undefined behavior, so GCC may assume no other thread writes <span class="mono c-amber">ready</span>.</div>')
a(code([
    C('# g++ -O2 -S broken.cpp'),
    'consume():',
    '    endbr64',
    ('    movq    msg(%rip), %rax', 3),
    '    ret',
], 160, 450, 720, cue=3, size=26))
a('<div class="lbl c-red" data-cue="3" data-d="0.6" style="left:160px;top:720px;width:720px;line-height:1.5">no load of ready, no loop:<br>the spin loop was deleted</div>')
a('<div class="box pink" data-cue="4" style="left:1000px;top:220px;width:800px;height:620px"><div class="t c-pink">2 · The CPU</div></div>')
a('<div class="cpu" data-cue="4" data-d="0.3" style="left:1040px;top:320px;width:280px">core 1<div class="lbl">program order</div></div>')
for k, t in enumerate(["price = p", "qty = q", "ready = true"]):
    a(f'<div class="sbq mono" data-cue="4" data-d="{0.4+0.2*k}" style="left:1040px;top:{410+k*62}px">{t}</div>')
a('<div class="lbl" data-cue="5" style="left:1340px;top:330px">STORE BUFFER</div>')
a('<div class="sb" data-cue="5" style="left:1340px;top:370px;width:420px;height:230px"></div>')
for k, t in enumerate(["ready = true", "qty = q", "price = p"]):
    a(f'<div class="sbq mono sbi" id="ro-s{k}" data-cue="5" data-d="0.2" data-anim="fade" style="left:1360px;top:{390+k*70}px;background:{"#3d2f17" if k==0 else "#123038"}">{t}</div>')
a('<div class="lbl" data-cue="5" data-d="1.4" style="left:1340px;top:640px">→ L1 → other cores see them</div>')
a('<div class="lbl c-pink" data-cue="5" data-d="2.0" style="left:1040px;top:720px;width:720px;line-height:1.5">ARM: may drain in a different order<br>x86: drains in program order</div>')
a('</div>')

# ---------------- tso
a('<div class="scene" id="s-tso">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">x86 (TSO) versus ARM</div>')
rows = [("load → later load", "kept", "may reorder", 1),
        ("store → later store", "kept", "may reorder", 1),
        ("load → later store", "kept", "may reorder", 1),
        ("store → later load", "may reorder", "may reorder", 2)]
a('<div class="lbl" data-cue="0" style="left:120px;top:235px;width:520px">PAIR (different addresses)</div>')
a('<div class="colh c-teal" data-cue="0" data-d="0.3" style="left:700px;top:220px">x86-64</div>')
a('<div class="colh c-violet" data-cue="3" style="left:1250px;top:220px">ARM (AArch64)</div>')
for k, (pair, x86, arm, cue) in enumerate(rows):
    y = 300 + k * 120
    a(f'<div class="pair mono" data-cue="0" data-d="{0.2+k*0.15}" style="left:120px;top:{y}px">{pair}</div>')
    good = x86 == "kept"
    a(f'<div class="cellx {"ok" if good else "bad"}" data-cue="{cue}" data-d="{0.1*k if cue==1 else 0}" {"data-hl=\"2\" data-hlend=\"3\"" if not good else ""} style="left:700px;top:{y}px">{x86}</div>')
    a(f'<div class="cellx bad" data-cue="4" data-d="{0.15*k}" style="left:1250px;top:{y}px">{arm}</div>')
a('<div class="lbl c-amber" data-cue="2" data-d="0.6" style="left:700px;top:790px;width:500px;line-height:1.45">the store is still in the store buffer<br>when the load reads cache</div>')
a('<div class="lbl c-violet" data-cue="4" data-d="0.8" style="left:1250px;top:790px;width:560px;line-height:1.45">unless a dependency, barrier,<br>or acquire / release says otherwise</div>')
a('</div>')

# ---------------- acqrel
a('<div class="scene" id="s-acqrel">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Release on the store, acquire on the load</div>')
a('<div class="lane teal" data-cue="0" style="left:160px;top:210px">Thread 1</div>')
a('<div class="lane violet" data-cue="0" style="left:1160px;top:210px">Thread 2</div>')
L1 = [("msg.price = p;", 300, "teal", 0.3), ("msg.qty = q;", 380, "teal", 0.5)]
for t, y, c, d in L1:
    a(f'<div class="op mono" data-cue="0" data-d="{d}" style="left:160px;top:{y}px;border-color:var(--{c})">{t}</div>')
a('<div class="op mono strong" data-cue="1" style="left:160px;top:500px;border-color:var(--amber)">ready.store(true, <span class="c-amber">memory_order_release</span>);</div>')
a('<div class="fence" data-cue="1" data-d="0.4" style="left:160px;top:480px;width:640px;border-color:var(--amber)"></div>')
a('<div class="lbl c-amber" data-cue="1" data-d="0.6" style="left:160px;top:440px">▲ nothing above may move below</div>')
a('<div class="op mono strong" data-cue="2" style="left:1160px;top:500px;border-color:var(--amber)">ready.load(<span class="c-amber">memory_order_acquire</span>) == true</div>')
a('<div class="fence" data-cue="2" data-d="0.4" style="left:1160px;top:578px;width:640px;border-color:var(--amber)"></div>')
a('<div class="lbl c-amber" data-cue="2" data-d="0.6" style="left:1160px;top:590px">▼ nothing below may move above</div>')
for t, y, d in [("use(msg.price);", 650, 0.8), ("use(msg.qty);", 730, 1.0)]:
    a(f'<div class="op mono" data-cue="2" data-d="{d}" style="left:1160px;top:{y}px;border-color:var(--violet)">{t}</div>')
a('<svg class="full">'
  '<path class="draw" data-cue="3" data-d="0.2" data-dur="1.2" d="M 830 532 C 950 532, 1030 532, 1150 532" stroke="var(--amber)" stroke-width="6" fill="none" marker-end="url(#ah-amber)"/>'
  '<path class="draw" data-cue="4" data-d="0.2" data-dur="1.2" d="M 600 330 C 980 330, 900 680, 1150 680" stroke="var(--green)" stroke-width="3" stroke-dasharray="0" fill="none" marker-end="url(#ah-green)"/>'
  '<path class="draw" data-cue="4" data-d="0.5" data-dur="1.2" d="M 600 410 C 960 410, 900 760, 1150 760" stroke="var(--green)" stroke-width="3" fill="none" marker-end="url(#ah-green)"/>'
  '</svg>')
a('<div class="hb" data-cue="3" data-d="0.8" style="left:860px;top:450px">happens-before</div>')
a('<div class="lbl c-green" data-cue="4" data-d="1.0" style="left:700px;top:820px;width:700px;text-align:center">writes before the store are visible after the load</div>')
a('</div>')

# ---------------- asm
a('<div class="scene" id="s-asm">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">What g++ -O2 emits on x86-64</div>')
a(code([
    C('// fixed.cpp: atomic flag'),
    (f'ready.store({K("true")}, std::memory_order_release);', 1, 2),
    '',
    (f'{K("while")} (!ready.load(std::memory_order_acquire)) {{}}', 2, 4),
    (f'{K("return")} msg.price;', 2, 4),
], 120, 210, 860, cue=0, size=24))
a(code([
    C('# publish(long, int)'),
    '    movq    %rdi, msg(%rip)',
    '    movl    %esi, 8+msg(%rip)',
    ('    movb    $1, ready(%rip)      <span class="c"># release: plain mov</span>', 1, 2),
    '    ret',
    C('# consume()'),
    ('.L4: movzbl ready(%rip), %eax   <span class="c"># acquire: plain mov</span>', 2, 4),
    ('    testb   %al, %al', 2, 4),
    ('    je      .L4                  <span class="c"># the loop stays</span>', 2, 4),
    '    movq    msg(%rip), %rax',
    '    ret',
], 1020, 210, 780, cue=0, d=0.5, size=22))
a(code([
    C('# store_relaxed()'),
    ('    movl    $1, flag(%rip)', 1, 2),
    C('# store_release()'),
    ('    movl    $1, flag(%rip)', 1, 2),
], 120, 470, 860, cue=1, d=0.3, size=22))
a('<div class="lbl c-muted" data-cue="1" data-d="0.6" style="left:120px;top:690px">real output: g++ 13.3 -O2 -S on this box (directives trimmed)</div>')
a('<div class="note teal" data-cue="3" style="left:120px;top:750px;width:860px">x86: the hardware already keeps these orders.<br>Acquire / release mostly restrain the compiler.</div>')
a('<div class="note violet" data-cue="4" style="left:1020px;top:750px;width:780px">AArch64: release store → <span class="mono">stlr</span><br>acquire load → <span class="mono">ldar</span> (or <span class="mono">ldapr</span>)</div>')
a('</div>')

# ---------------- seqcst
a('<div class="scene" id="s-seqcst">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">seq_cst costs a locked store; relaxed orders nothing</div>')
a(code([
    C('# store_seq_cst(): flag.store(1)'),
    '    movl    $1, %eax',
    ('    xchgl   flag(%rip), %eax     <span class="c"># implicitly locked</span>', 1, 2),
    '    ret',
], 120, 220, 860, cue=0, d=0.3, size=24))
a('<div class="lbl" data-cue="0" data-d="0.4" style="left:1040px;top:230px;width:760px;line-height:1.5">default std::atomic order · forbids store → load reordering · one total order all threads agree on</div>')
a('<div class="lbl c-pink" data-cue="1" data-d="0.4" style="left:1040px;top:350px;width:760px">xchg waits for the store buffer to drain</div>')
a('<div class="lbl" data-cue="2" style="left:120px;top:470px">LOOP: STORE PAYLOAD, THEN PUBLISH · NS PER ITERATION · BEST OF 7</div>')
a('<div class="lbl c-green" data-cue="2" style="left:120px;top:525px;width:200px">release</div>')
a('<div class="grow bar" data-cue="2" data-w="74" data-dur="1.0" style="left:330px;top:515px;background:var(--green);height:52px"></div>')
a('<div class="val mono c-green" data-cue="2" data-d="0.6" style="left:430px;top:520px">0.70 ns</div>')
a('<div class="lbl c-red" data-cue="2.5" style="left:120px;top:605px;width:200px">seq_cst</div>')
a('<div class="grow bar" data-cue="2.5" data-w="940" data-dur="1.2" style="left:330px;top:595px;background:var(--red);height:52px"></div>')
a('<div class="val mono c-red" data-cue="2.5" data-d="1.0" style="left:1290px;top:600px">8.9 ns</div>')
a('<div class="lbl c-muted" data-cue="2.5" data-d="1.0" style="left:120px;top:670px">one thread on CPU 3, chrt -f 10, 100 million iterations · 4 vCPU KVM Xeon @ 2.10 GHz</div>')
a(code([
    C('// a statistics counter: only its own value matters'),
    (f'stats.msgs.fetch_add({R("1")}, std::memory_order_relaxed);   {C("# lock addl $1, …")}', 3),
], 120, 730, 1300, cue=3, size=24))
a('</div>')

# ---------------- ring
a('<div class="scene" id="s-ring">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">The lab’s SpscRing</div>')
a(code([
    C('// producer'),
    (f'{K("const")} std::uint64_t head = head_.load(std::memory_order_relaxed);', 3, 4),
    (f'{K("if")} (head - cached_tail_ == Capacity)', 4),
    ('  cached_tail_ = tail_.load(std::memory_order_acquire);', 4),
    (f'{K("if")} (head - cached_tail_ == Capacity) {K("return")} {K("false")};', 4),
    (f'slots_[head &amp; kMask] = value;', 1, 2),
    ('head_.store(head + <span class="r">1</span>, std::memory_order_release);', 1, 2),
    C('// consumer'),
    (f'{K("const")} std::uint64_t tail = tail_.load(std::memory_order_relaxed);', 3, 4),
    (f'{K("if")} (tail == cached_head_)', 4),
    ('  cached_head_ = head_.load(std::memory_order_acquire);', 2, 3),
    (f'{K("if")} (tail == cached_head_) {K("return")} {K("false")};', 4),
    ('out = slots_[tail &amp; kMask];', 2, 3),
    ('tail_.store(tail + <span class="r">1</span>, std::memory_order_release);', 2, 3),
], 120, 200, 1080, cue=0, size=22))
a('<div class="lbl c-muted" data-cue="0" data-d="0.5" style="left:120px;top:850px;width:1080px">libs/core/include/lab/core/spsc_ring.hpp, condensed: the real code splits this into try_claim / commit and front / pop</div>')
# diagram
a('<div class="box teal" data-cue="1" style="left:1270px;top:220px;width:250px;height:100px;text-align:center"><div class="t">producer</div><div class="s">writes head_</div></div>')
a('<div class="box violet" data-cue="2" style="left:1560px;top:220px;width:250px;height:100px;text-align:center"><div class="t">consumer</div><div class="s">writes tail_</div></div>')
for j in range(8):
    a(f'<div class="slot" id="rg-s{j}" data-cue="0" data-d="{0.3+0.05*j}" style="left:{1270+j*68}px;top:420px"></div>')
a('<div class="ptr c-teal" id="rg-h" data-cue="1" style="left:1270px;top:500px">▲ head</div>')
a('<div class="ptr c-violet" id="rg-t" data-cue="2" style="left:1270px;top:380px">▼ tail</div>')
a('<div class="lbl c-amber" data-cue="1" data-d="0.6" style="left:1270px;top:580px;width:540px;line-height:1.5">slot write, then release store of head</div>')
a('<div class="lbl c-amber" data-cue="2" data-d="0.6" style="left:1270px;top:640px;width:540px;line-height:1.5">acquire load of head, then slot read</div>')
a('<div class="lbl" data-cue="4" data-d="0.4" style="left:1270px;top:720px;width:540px;line-height:1.5">cached_tail_ / cached_head_: the other side’s index is re-read only when the copy says full or empty</div>')
a('</div>')

# ---------------- aeron
a('<div class="scene" id="s-aeron">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Aeron: the frame length is the flag</div>')
a('<div class="lbl" data-cue="0" data-d="0.3" style="left:120px;top:220px">ONE FRAME IN THE TERM · 32-BYTE HEADER + 36-BYTE ITCH ADD ORDER = 68</div>')
cells = [("frame_length", 4, "fl"), ("v", 1, ""), ("f", 1, ""), ("type", 2, ""), ("term_offset", 4, ""), ("session_id", 4, ""), ("stream_id", 4, ""), ("term_id", 4, ""), ("reserved_value", 8, "")]
x = 120; W = 24
for nm, sz, tag in cells:
    idattr = ' id="ae-fl"' if tag else ""
    cls = "fcell fl" if tag else "fcell hdr"
    cue = 0 if tag else 1
    d = 0.5 if tag else 0.6
    a(f'<div class="{cls}"{idattr} data-cue="{cue}" data-d="{d}" data-anim="fade" style="left:{x}px;top:270px;width:{sz*W}px">{nm}<br><span class="sz">{sz}</span></div>')
    x += sz * W
a(f'<div class="fcell pay" data-cue="1" data-d="1.2" data-anim="fade" style="left:{x}px;top:270px;width:{36*W}px">payload · ITCH Add Order<br><span class="sz">36</span></div>')
a('<div class="flv mono" id="ae-v" data-cue="0" data-d="0.5" style="left:120px;top:380px">—</div>')
steps = [("1", "frame_length = −68", "store, release · frame is not ready", 1),
         ("2", "write header + payload", "plain stores", 1.5),
         ("3", "frame_length = +68", "store, release · commits the frame", 2),
         ("4", "subscriber: load frame_length, acquire", "positive ⇒ the whole frame is visible", 3)]
for k, (n, t, s, cue) in enumerate(steps):
    y = 480 + k * 105
    col = ["var(--red)", "var(--teal)", "var(--amber)", "var(--violet)"][k]
    a(f'<div class="step" data-cue="{cue}" style="left:120px;top:{y}px;border-color:{col}"><span class="sn" style="background:{col}">{n}</span><span class="mono">{t}</span><span class="lbl">{s}</span></div>')
a('<div class="lbl c-muted" data-cue="4" style="left:1280px;top:480px;width:540px;line-height:1.5">docs/aeron.md, from aeron_exclusive_publication.c at 1.47.7: one writer thread, no lock, no syscall</div>')
a('<div class="lbl c-green" data-cue="4" data-d="0.6" style="left:1280px;top:620px;width:540px;line-height:1.5">the handler gets a pointer into the shared pages: nothing is copied</div>')
a('</div>')

open(OUT, "w").write("\n".join(H))
print("wrote", OUT)
