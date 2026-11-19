# Generates scenes.html for cpp-no-alloc.
import math
OUT = "/mnt/project-files/videos/explainers/cpp-no-alloc/scenes.html"
H = []
def a(s): H.append(s)

def code(lines, x, y, w, cue=0, size=25, d=0):
    out = []
    for ln in lines:
        if isinstance(ln, tuple):
            end = f' data-hlend="{ln[2]}"' if len(ln) > 2 else ""
            out.append(f'<span class="line" data-hl="{ln[1]}"{end}>{ln[0]}</span>')
        else:
            out.append(f'<span class="line">{ln}</span>')
    return f'<div class="code" data-cue="{cue}" data-d="{d}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px">' + "".join(out) + "</div>"

K = lambda s: f'<span class="k">{s}</span>'
R = lambda s: f'<span class="r">{s}</span>'
C = lambda s: f'<span class="c">{s}</span>'
V = lambda s: f'<span class="v">{s}</span>'

# ---------------- title
a('<div class="scene" id="s-title">')
a('<div class="eyebrow" data-cue="0" style="left:140px;top:150px">TRADING LAB · LOW-LATENCY C++</div>')
a('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:200px">No allocation<br>on the hot path</div>')
a('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:500px;width:1500px">Pools, arenas, reserve, prefaulting, and the allocations you don’t see.</div>')
# deterministic "latency samples": mostly short, a few spikes
import random
rnd = random.Random(7)
base_y = 900
for i in range(56):
    spike = i in (13, 31, 47)
    h = rnd.randint(28, 60) if not spike else rnd.randint(200, 260)
    cue = 2 if spike else 1
    col = "var(--red)" if spike else "var(--teal)"
    a(f'<div class="bar" data-cue="{cue}" data-d="{0.02*i if not spike else 0.2}" data-anim="fade" style="left:{140+i*29}px;top:{base_y-h}px;width:20px;height:{h}px;background:{col};border-radius:4px"></div>')
a(f'<div class="tlax" data-cue="1" style="left:140px;top:{base_y+4}px;width:1640px"></div>')
a('<div class="lbl c-teal" data-cue="1" data-d="0.8" style="left:140px;top:600px">each bar: one allocation (illustration)</div>')
a('<div class="lbl c-red" data-cue="2" data-d="0.5" style="left:1300px;top:600px">page fault · syscall</div>')
a('</div>')

# ---------------- why
a('<div class="scene" id="s-why">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Why malloc’s cost is not fixed</div>')
a('<div class="box blue" data-cue="0" data-d="0.3" style="left:120px;top:260px;width:300px;height:110px;text-align:center"><div class="t">new / malloc</div><div class="s">general purpose</div></div>')
a('<div class="box green" data-cue="1" style="left:560px;top:220px;width:420px;height:110px"><div class="t c-green">tcache</div><div class="s">per thread · no lock</div></div>')
a('<div class="box amber" data-cue="1" data-d="0.8" style="left:560px;top:380px;width:420px;height:110px"><div class="t c-amber">arena + lock</div><div class="s">on a cache miss</div></div>')
a('<div class="box red" data-cue="2" style="left:1120px;top:380px;width:660px;height:110px"><div class="t c-red">kernel: brk / mmap</div><div class="s">grow the heap · large blocks are mmapped</div></div>')
a('<div class="box red" data-cue="3" style="left:1120px;top:620px;width:660px;height:110px"><div class="t c-red">page fault</div><div class="s">first write to a new page</div></div>')
a('<svg class="full">'
  '<path class="draw" data-cue="1" d="M 420 300 L 550 280" stroke="var(--green)" stroke-width="4" fill="none" marker-end="url(#ah-green)"/>'
  '<path class="draw" data-cue="1" data-d="0.8" d="M 420 340 L 550 430" stroke="var(--amber)" stroke-width="4" fill="none" marker-end="url(#ah-amber)"/>'
  '<path class="draw" data-cue="2" d="M 980 435 L 1110 435" stroke="var(--red)" stroke-width="4" fill="none" marker-end="url(#ah-red)"/>'
  '<path class="draw" data-cue="3" d="M 1450 490 L 1450 610" stroke="var(--red)" stroke-width="4" fill="none" marker-end="url(#ah-red)"/>'
  '</svg>')
a('<div class="cost c-green" data-cue="1" data-d="0.4" style="left:1000px;top:250px">tens of ns</div>')
a('<div class="cost c-amber" data-cue="1" data-d="1.2" style="left:600px;top:510px">contended? you wait</div>')
a('<div class="cost c-red" data-cue="2" data-d="0.4" style="left:1120px;top:510px">a system call</div>')
a('<div class="cost c-red" data-cue="3" data-d="0.4" style="left:1120px;top:750px">microseconds, at random</div>')
a('<div class="lbl c-muted" data-cue="2" data-d="0.8" style="left:120px;top:620px;width:900px;line-height:1.5">glibc defaults: blocks of 128 KiB and up go to mmap (M_MMAP_THRESHOLD)</div>')
a('</div>')

# ---------------- rule
a('<div class="scene" id="s-rule">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">The lab’s rule</div>')
a('<div class="quote" data-cue="0" data-d="0.3" style="left:120px;top:220px;width:1680px">'
  '<div class="lbl" style="margin-bottom:14px">/home/claude/ts-push/CLAUDE.md · Hot-path rules</div>'
  '<div class="ql" data-hl="1" data-hlend="2">- No allocation, locks, exceptions, syscalls or logging I/O on hot threads.</div>'
  '<div class="ql" data-hl="2">&#160;&#160;Allocate and fault pages in at startup. Log through <span class="c-teal">lab::LogChannel</span> only.</div></div>')
a('<div class="phase" data-cue="2" style="left:120px;top:560px;width:700px;border-color:var(--amber)"><div class="pt c-amber">STARTUP</div><div class="ps">allocate · reserve · touch every page</div></div>')
a('<div class="phase" data-cue="2" data-d="0.5" style="left:860px;top:560px;width:940px;border-color:var(--green)"><div class="pt c-green">TRADING (hot threads)</div><div class="ps">reuse only · no new memory</div></div>')
a('<svg class="full"><path class="draw" data-cue="2" data-d="0.3" d="M 120 760 L 1790 760" stroke="#8ea3b1" stroke-width="3" fill="none" marker-end="url(#ah)"/></svg>')
a('<div class="lbl" data-cue="2" data-d="0.6" style="left:1700px;top:780px">time</div>')
a('</div>')

# ---------------- pool
a('<div class="scene" id="s-pool">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Object pools and free lists</div>')
a(code([
    f'{K("template")} &lt;{K("class")} T&gt; {K("class")} {V("Pool")} {{',
    ' public:',
    (f'  {K("explicit")} Pool(std::size_t n) : slots_(n) {{', 0, 1),
    (f'    {K("for")} (std::size_t i = {R("0")}; i + {R("1")} &lt; n; ++i) slots_[i].next = &amp;slots_[i + {R("1")}];', 0, 1),
    ('    free_ = &amp;slots_[<span class="r">0</span>];', 0, 1),
    '  }',
    (f'  T* get() {K("noexcept")} {{ T* p = free_; {K("if")} (p) free_ = p-&gt;next; {K("return")} p; }}', 1, 3),
    (f'  {K("void")} put(T* p) {K("noexcept")} {{ p-&gt;next = free_; free_ = p; }}', 1, 3),
    ' private:',
    '  std::vector&lt;T&gt; slots_;',
    '  T* free_ = <span class="k">nullptr</span>;',
    '};',
], 120, 200, 1120, cue=0, size=20))
for j in range(8):
    a(f'<div class="slot" id="pl-s{j}" data-cue="0" data-d="{0.4+0.05*j}" style="left:{1300+j*62}px;top:250px"></div>')
a('<div class="ptr c-amber" id="pl-f" data-cue="1" style="left:1300px;top:320px">▲ free_</div>')
a('<div class="lbl" data-cue="0" data-d="0.6" style="left:1300px;top:205px">slots_ · teal = in use</div>')
a('<div class="lbl c-green" data-cue="2" style="left:1300px;top:380px;width:500px">no lock · no syscall · two pointer moves</div>')
a(code([
    C('// libs/match/include/lab/match/engine.hpp'),
    (f'std::size_t max_orders = {R("1u")} &lt;&lt; {R("20")};  {C("// EngineConfig: 1,048,576")}', 4, 5),
    ('nodes_(cfg.max_orders)        <span class="c">// vector&lt;Node, HugePageAllocator&lt;Node&gt;&gt;</span>', 4, 5),
    ('free_.reserve(cfg.max_orders);', 4, 5),
    (f'{K("for")} (std::size_t i = cfg.max_orders; i-- &gt; {R("0")};) free_.push_back(i);', 4, 5),
    C('// allocate(key)'),
    ('<span class="k">const</span> std::uint32_t n = free_.back(); &#8230; free_.pop_back();', 5),
    C('// release(n)'),
    ('free_.push_back(n);', 5),
], 120, 610, 1120, cue=3, size=20))
a('<div class="lbl c-muted" data-cue="4" data-d="0.5" style="left:1300px;top:640px;width:500px;line-height:1.5">condensed from the Engine constructor, allocate() and release(); the push_backs never grow past the reserve</div>')
a('</div>')

# ---------------- arena
a('<div class="scene" id="s-arena">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Arenas: std::pmr::monotonic_buffer_resource</div>')
a(code([
    (f'{K("alignas")}({R("16")}) {K("static")} {K("char")} buf[{R("64")} * {R("1024")}];       {C("// owned, faulted in at startup")}', 0, 1),
    ('std::pmr::monotonic_buffer_resource arena{', 1, 2),
    (f'    buf, {K("sizeof")} buf, std::pmr::null_memory_resource()}};  {C("// never falls back to malloc")}', 3),
    '',
    (f'std::pmr::vector&lt;Fill&gt; fills{{&amp;arena}};              {C("// scratch for one batch")}', 1, 2),
    ('fills.reserve(<span class="r">64</span>);', 1, 2),
    ('fills.push_back({<span class="r">1</span>, <span class="r">100</span>, <span class="r">101250</span>});', 1, 2),
    '<span class="c">// … batch done, fills destroyed …</span>',
    (f'arena.release();                                   {C("// free everything at once")}', 2, 3),
], 120, 200, 1500, cue=0, size=23))
a('<div class="lbl" data-cue="1" style="left:120px;top:620px">BUFFER · 64 KiB</div>')
a('<div class="abuf" data-cue="1" style="left:120px;top:660px;width:1500px"></div>')
a('<div class="afill" id="ar-fill" data-cue="1" data-anim="fade" style="left:120px;top:660px;width:0"></div>')
a('<div class="ptr c-amber" id="ar-p" data-cue="1" data-anim="fade" style="left:120px;top:750px">▲ bump</div>')
a('<div class="lbl c-green" id="ar-rel" data-cue="2" data-d="1.0" style="left:120px;top:820px">release(): pointer back to the start</div>')
a('<div class="tag c-red" data-cue="3" data-d="2.4" style="left:1650px;top:665px;border-color:var(--red)">full ⇒ bad_alloc</div>')
a('</div>')

# ---------------- fixed
a('<div class="scene" id="s-fixed">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">reserve, and fixed capacity</div>')
a(code([
    'std::vector&lt;Order&gt; v;',
    (f'v.reserve({R("1000")});                {C("// startup: one allocation")}', 1),
    (f'{K("for")} ({K("int")} i = {R("0")}; i &lt; {R("1000")}; ++i)', 1),
    (f'  v.push_back(Order{{}});         {C("// hot path: 0 mallocs")}', 1),
    (f'v.push_back(Order{{}});           {C("// #1001: reallocates, 1 malloc")}', 0, 1),
], 120, 200, 1000, cue=0, size=24))
a('<div class="lbl c-muted" data-cue="1" data-d="0.5" style="left:120px;top:460px">malloc calls counted on this box (glibc, g++ 13.3)</div>')
a('<div class="card" data-cue="2" style="left:120px;top:530px;width:820px;border-color:var(--teal)"><div class="ct c-teal">libs/book · OrderMap</div>'
  '<div class="cs">OrderMap(std::size_t initial_capacity = 1u &lt;&lt; 20)</div><div class="cd">open addressing · growth rehashes everything</div></div>')
a('<div class="card" data-cue="3" style="left:980px;top:530px;width:820px;border-color:var(--violet)"><div class="ct c-violet">libs/match · Engine</div>'
  '<div class="cs">levels_per_side = 512 · side.reserve() at open</div><div class="cd">grows only if an instrument outgrows it</div></div>')
a('<div class="card" data-cue="4" style="left:120px;top:740px;width:1680px;border-color:var(--amber)"><div class="ct c-amber">Fixed capacity</div>'
  '<div class="cs">std::array&lt;T, N&gt; + a count, or C++26 std::inplace_vector&lt;T, N&gt;</div><div class="cd">full is a result you check, not a reallocation</div></div>')
a('</div>')

# ---------------- pages
a('<div class="scene" id="s-pages">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Prefault, and use huge pages</div>')
a('<div class="lbl" data-cue="0" data-d="0.3" style="left:120px;top:220px">16 × 4 KiB PAGES, RESERVED</div>')
for j in range(16):
    a(f'<div class="pg" id="pg-{j}" data-cue="0" data-d="{0.3+0.03*j}" style="left:{120+j*104}px;top:260px">{j}</div>')
a('<div class="lbl" id="pg-lab" data-cue="0" data-d="0.8" style="left:120px;top:360px;width:1600px">not mapped yet: the first write to each page faults</div>')
a(code([
    C('// libs/core/include/lab/core/spsc_ring.hpp'),
    C('// Zeroed on construction, which also faults the pages in before the hot path runs.'),
    ('<span class="k">alignas</span>(kCacheLine) T slots_[Capacity]{};', 2),
], 120, 430, 1400, cue=2, size=23))
a('<div class="lbl" data-cue="3" style="left:120px;top:640px">TLB ENTRIES TO MAP 2 MiB</div>')
a('<div class="grid4k" data-cue="3" data-d="0.2" style="left:120px;top:680px"></div>')
a('<div class="lbl c-red" data-cue="3" data-d="0.4" style="left:120px;top:880px">4 KiB pages: 512 entries</div>')
a('<div class="hp" data-cue="3" data-d="0.9" style="left:1000px;top:680px">1</div>')
a('<div class="lbl c-green" data-cue="3" data-d="1.1" style="left:1000px;top:880px">one 2 MiB page: 1 entry</div>')
a('<div class="lbl" data-cue="3" data-d="1.4" style="left:1260px;top:690px;width:540px;line-height:1.5">lab::HugePageAllocator: mmap on a 2 MiB boundary, then madvise(MADV_HUGEPAGE); falls back to normal pages if refused</div>')
a('</div>')

# ---------------- hidden
a('<div class="scene" id="s-hidden">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Hidden allocations</div>')
a('<div class="lbl" data-cue="1" style="left:120px;top:210px">malloc CALLS COUNTED ON THIS BOX · g++ 13.3 -O2 · glibc · libstdc++</div>')
rows = [("std::function, 16-byte capture", "0", 2, "ok"), ("std::function, 24-byte capture", "1", 2, "bad"),
        ("std::string, 15 chars (SSO)", "0", 3, "ok"), ("std::string, 16 chars", "1", 3, "bad"),
        ("throw std::runtime_error", "2", 4, "bad"), ("std::make_shared&lt;Order&gt;()", "1", 5, "bad"),
        ("copy a shared_ptr", "0 · atomic ++", 5, "warn")]
for k, (what, n, cue, cls) in enumerate(rows):
    y = 260 + k * 82
    a(f'<div class="hrow" data-cue="{cue}" data-d="{0.3*(k%2)}" style="left:120px;top:{y}px"><span class="mono">{what}</span><span class="hn {cls}">{n}</span></div>')
a('<div class="lbl c-muted" data-cue="5" data-d="0.8" style="left:120px;top:850px;width:1500px">a malloc() wrapper around __libc_malloc counted the calls; the refcount is atomic once the program has threads</div>')
a('</div>')

# ---------------- measured
a('<div class="scene" id="s-measured">')
a('<div class="h2" data-cue="0" style="left:120px;top:110px">Measured on this box: new/delete vs a pool</div>')
a('<div class="pill" data-cue="0" data-d="0.3" style="left:120px;top:200px">4 vCPU KVM · Xeon @ 2.10 GHz · g++ 13.3 -O2 · glibc malloc · one thread, chrt -f 10</div>')
a('<div class="lbl" data-cue="1" style="left:120px;top:270px;width:1680px">2 million messages · 64-byte Order · 100,000 live, then each frees a random one · timed with rdtsc, timer included</div>')
# log-scale bars: x = 330 + 330*log10(ns)
def fmt(ns): return f"{ns/1000:.1f} µs" if ns >= 1000 else f"{ns:g} ns"
def bx(ns): return round(330 * math.log10(ns))
grid = [10, 100, 1000]
for g in grid:
    a(f'<div class="gl" data-cue="2" style="left:{560+bx(g)-330}px;top:340px;height:430px"></div><div class="lbl" data-cue="2" style="left:{560+bx(g)-330-60}px;top:775px;width:120px;text-align:center;white-space:nowrap">{g if g<1000 else "1 µs"}{" ns" if g<1000 else ""}</div>')
rowsm = [("p50", 28.6, 19.0, 2, 3), ("p99", 71.4, 21.9, 2, 3), ("p99.9", 1425, 52.4, 4, 5)]
for k, (q, nv, pv, cn, cp) in enumerate(rowsm):
    y = 350 + k * 140
    a(f'<div class="q mono" data-cue="{min(cn,cp)}" style="left:120px;top:{y+20}px">{q}</div>')
    wn = bx(nv) - 330; wp = bx(pv) - 330
    a(f'<div class="grow bar" data-cue="{cn}" data-w="{wn}" data-dur="1.0" style="left:560px;top:{y}px;height:46px;background:var(--red)"></div>')
    a(f'<div class="bv mono c-red" data-cue="{cn}" data-d="0.8" style="left:{560+wn+14}px;top:{y+4}px">new {fmt(nv)}</div>')
    a(f'<div class="grow bar" data-cue="{cp}" data-w="{wp}" data-dur="1.0" style="left:560px;top:{y+56}px;height:46px;background:var(--green)"></div>')
    a(f'<div class="bv mono c-green" data-cue="{cp}" data-d="0.8" style="left:{560+wp+14}px;top:{y+60}px">pool {fmt(pv)}</div>')
a('<div class="lbl" data-cue="2" style="left:330px;top:775px">log scale</div>')
a('<div class="faults" data-cue="4" data-d="0.6" style="left:1400px;top:340px;width:420px;border-color:var(--red)"><span class="c-red">new</span>: 1,953 page faults while timing</div>')
a('<div class="faults" data-cue="5" data-d="0.3" style="left:1400px;top:470px;width:420px;border-color:var(--green)"><span class="c-green">pool</span>: 0</div>')
a('<div class="lbl c-muted" data-cue="5" data-d="0.8" style="left:120px;top:830px;width:1680px">median of 3 runs each · new p99 ranged 68–104 ns, pool p99.9 35–125 ns</div>')
a('</div>')

open(OUT, "w").write("\n".join(H))
print("wrote", OUT)
