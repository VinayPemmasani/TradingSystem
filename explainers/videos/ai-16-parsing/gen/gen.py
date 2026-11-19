import sys
sys.path.insert(0, '/tmp/claude-0/vx/ai1316tools')
from hl import code_html, check
OUT = '/mnt/project-files/videos/explainers/ai-16-parsing'
LEFT = r'''
struct Quote {
  std::string sym; double px; int qty; };
// "ESZ6,5012.25,17" -> {"ESZ6", 5012.25, 17}
Quote parse(const std::string& line) {
  std::stringstream ss(line);
  std::string sym, px, qty;
  std::getline(ss, sym, ',');
  std::getline(ss, px, ',');
  std::getline(ss, qty, ',');
  return {sym, std::stod(px), std::stoi(qty)};
}
'''
REGEX = r'''
static const std::regex re(
    R"(([A-Z0-9]+),(\d+(?:\.\d{1,2})?),(-?\d+))");
std::smatch m;
if (!std::regex_match(line, m, re)) throw ...;
return {m[1].str(), std::stod(m[2].str()),
        std::stoi(m[3].str())};
'''
RIGHT = r'''
bool parse(std::string_view s, Quote& q) {
  const char *p = s.data(), *e = p + s.size();
  const char* c = std::find(p, e, ',');
  const char* f = std::find(c + (c < e), e, ',');
  if (f == e || f-c < 2 || f-c > 17) return false;
  q.sym = std::string_view(p, c - p);
  int64_t t = 0; int nf = -1;   // nf: decimals
  for (++c; c < f; ++c) {
    if (*c == '.' && nf < 0) { nf = 0; continue; }
    const unsigned d = unsigned(*c - '0');
    if (d > 9 || nf == 2) return false;
    t = t * 10 + d; nf += nf >= 0;
  }
  q.px = t * (nf <= 0 ? 100 : nf == 1 ? 10 : 1);
  auto [r, ec] = std::from_chars(f + 1, e, q.qty);
  return ec == std::errc{} && r == e; }
'''
check(LEFT); check(RIGHT); check(REGEX)
h = []; A = h.append
# title
A('<div class="scene" id="s-title">')
A('<div class="eyebrow" data-cue="0" style="left:140px;top:160px">PATTERN 16 / 16</div>')
A('<div class="h1" data-cue="0" data-d="0.2" style="left:132px;top:215px">Parsing a<br>text feed</div>')
A('<div class="sub" data-cue="0" data-d="0.5" style="left:140px;top:520px;width:1600px">stringstream, stod and regex vs a digit loop straight into int64 ticks</div>')
line = 'ESZ6,5012.25,17'
for i, ch in enumerate(line):
    col = 'var(--blue)' if i < 4 else ('#3a4f5c' if ch == ',' else ('var(--amber)' if i < 12 else 'var(--violet)'))
    A(f'<div class="cell" data-cue="1" data-d="{0.06*i:.2f}" style="left:{140+i*62}px;top:700px;width:56px;background:{col};font-size:28px">{ch}</div>')
A('<div class="lbl" data-cue="1" data-d="1.0" style="left:140px;top:786px"><span class="c-blue">symbol</span> · <span class="c-amber">price</span> · <span class="c-violet">quantity</span> · one message, 15 bytes</div>')
A('<div class="chip teal" data-cue="2" data-d="0.4" style="left:1180px;top:705px">→ {"ESZ6", 501225, 17}</div>')
A('</div>')
# general
A('<div class="scene" id="s-general">')
A('<div class="h2" data-cue="0" style="left:70px;top:110px">Text line in, Quote out</div>')
A('<div class="mono chip" data-cue="0" data-d="0.4" style="left:1040px;top:210px;font-size:30px">"ESZ6,5012.25,17"</div>')
A('<div class="side c-red" data-cue="1" style="left:70px;top:200px">GENERAL-PURPOSE</div>')
A(code_html(LEFT, {4: (1, 2), 6: (1, 2), 7: (1, 2), 8: (1, 2), 9: (1, 2)}, cls="code sm left", style="left:70px;top:240px;width:880px", cue=1))
A('<div class="chip red" data-cue="2" style="left:70px;top:640px">bad input: std::invalid_argument</div>')
A('<div class="side c-red" data-cue="3" style="left:1040px;top:330px">OR: std::regex</div>')
A(code_html(REGEX, {}, cls="code sm left", style="left:1040px;top:370px;width:820px;font-size:19px", cue=3))
A('</div>')
# cost
A('<div class="scene" id="s-cost">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Per line, before a single digit is read</div>')
steps = [(1, 'stringstream ss(line)', 'stream buffer + locale copy'), (2, 'copy of the line', '≥ 16 chars: heap (0.8 allocs/line)'),
         (3, 'getline x 3', 'a std::string per field'), (3.5, 'stod → strtod', 'C locale · exponents · hex · inf')]
for i, (c, t, s) in enumerate(steps):
    x = 120 + i * 430
    A(f'<div class="card2" data-cue="{c}" style="left:{x}px;top:230px;width:400px;height:170px;border-color:var(--amber)"><div class="ct" style="font-size:27px">{t}</div><div class="cs" style="font-size:21px">{s}</div></div>')
A('<svg class="full">' + ''.join(f'<path class="draw" data-cue="{steps[i+1][0]}" d="M{120+i*430+402} 315 L{120+(i+1)*430-4} 315" stroke="var(--amber)" stroke-width="3" fill="none" marker-end="url(#ah-amber)"/>' for i in range(3)) + '</svg>')
A('<div class="card2" data-cue="4" style="left:120px;top:460px;width:830px;height:170px;border-color:var(--red)"><div class="ct">std::regex_match</div><div class="cs">3 allocations per line (counted) · backtracking executor</div></div>')
A('<div class="card2" data-cue="5" style="left:980px;top:460px;width:820px;height:170px;border-color:var(--red)"><div class="ct">result: double px</div><div class="cs">5012.25 → nearest double · pattern 15 starts here</div></div>')
A('<div class="note" data-cue="1" data-d="1.0" style="left:120px;top:680px;width:1600px">allocations counted with a replaced global operator new · libstdc++ (g++ 13)</div>')
A('</div>')
# hot
A('<div class="scene" id="s-hot">')
A('<div class="h2" data-cue="0" style="left:60px;top:110px">Bytes straight into ticks</div>')
A('<div class="side c-red" data-cue="0" style="left:60px;top:200px">GENERAL</div>')
A('<div class="side c-teal" data-cue="0" data-d="0.3" style="left:980px;top:200px">HOT PATH</div>')
A(code_html(LEFT, {}, cls="code sm left", style="left:60px;top:240px;width:880px", cue=0, extra=' data-dim="1"'))
A(code_html(RIGHT, {0: (0, 1), 15: (0, 1), 2: (1, 2), 3: (1, 2), 5: (1, 2), 6: (2, 3), 7: (2, 3), 8: (2, 3), 9: (2, 3), 10: (2, 3), 11: (2, 3), 13: (2, 3), 14: (3, 4), 4: (4, 5)}, cls="code sm right", style="left:980px;top:240px;width:880px", cue=0, extra=' data-d="0.3"'))
A('<div class="note" data-cue="1" data-d="0.5" style="left:60px;top:640px;width:880px">Quote { string_view sym; int64_t px; /* ticks */ int64_t qty; }</div>')
A('<div class="chip red" data-cue="4" style="left:60px;top:720px">rejects: "5.0e3" · " 5012.25" · "5012.255"</div>')
A('<div class="chip teal" data-cue="5" style="left:60px;top:800px">200,000 random lines: same result as general</div>')
A('</div>')
# numbers
A('<div class="scene" id="s-numbers">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">ns per line (3 fields), p50</div>')
A('<div class="note" data-cue="0" data-d="0.3" style="left:120px;top:190px;width:1700px">measured on a shared 4-vCPU cloud VM · g++ 13 -O2 · 4,096 lines · pinned · median of 3 runs x 31 passes · allocations counted per line</div>')
SC = 0.6; X0 = 620
def bar(y, name, val, col, cue, d=0.0, txt=None, alloc=None):
    A(f'<div class="blab" data-cue="{cue}" data-d="{d}" style="left:110px;top:{y}px;width:480px">{name}</div>')
    A(f'<div class="bar grow" data-cue="{cue}" data-d="{d}" data-w="{max(val*SC,4):.0f}" data-anim="fade" style="left:{X0}px;top:{y-2}px;background:{col}"></div>')
    A(f'<div class="bv" data-cue="{cue}" data-d="{d+0.7}" style="left:{X0+max(val*SC,4)+16:.0f}px;top:{y-3}px;color:{col}">{txt}</div>')
bar(270, 'stringstream + getline + stod', 300, 'var(--red)', 1, txt='300 · 0.8 allocs')
A(f'<div class="bar grow" data-cue="2" data-d="0.0" data-w="{730*SC:.0f}" data-anim="fade" style="left:{X0}px;top:318px;background:#c95a50"></div>')
A(f'<div class="bar grow hatch" data-cue="2" data-d="1.0" data-w="{(1720-730)*SC:.0f}" data-anim="fade" style="left:{X0+730*SC:.0f}px;top:318px"></div>')
A('<div class="blab" data-cue="2" style="left:110px;top:320px;width:480px">std::regex + stod / stoi</div>')
A(f'<div class="bv" data-cue="2" data-d="1.6" style="left:{X0}px;top:356px;color:#ff9d93">best 730 · p50 up to 1,720 · 3 allocs</div>')
bar(420, 'from_chars, double price', 27, 'var(--violet)', 3, txt='27 · 0 allocs')
bar(470, 'hot: digit loop + from_chars', 19, 'var(--teal)', 4, txt='19 · 0 allocs · 6.4 ns/field')
A('<div class="chip amber" data-cue="4" data-d="1.2" style="left:1100px;top:458px">≈ 15x vs stream</div>')
A('<div class="gl" data-cue="5" style="left:120px;top:580px">at 1,000,000 messages per second</div>')
A('<div class="cpu" data-cue="5" data-d="0.3" style="left:120px;top:640px;width:1600px"></div>')
A('<div class="grow" data-cue="5" data-d="0.5" data-w="480" style="position:absolute;left:120px;top:640px;height:60px;background:var(--red);border-radius:10px 0 0 10px"></div>')
A('<div class="bv c-red" data-cue="5" data-d="1.2" style="left:140px;top:715px">stream: 30% of a core</div>')
A('<div class="grow" data-cue="5" data-d="1.4" data-w="32" style="position:absolute;left:120px;top:760px;height:60px;background:var(--teal);border-radius:10px 0 0 10px"></div>')
A('<div class="cpu" data-cue="5" data-d="1.4" style="left:120px;top:760px;width:1600px"></div>')
A('<div class="bv c-teal" data-cue="5" data-d="1.8" style="left:180px;top:772px">hot: 2%</div>')
A('</div>')
# close
A('<div class="scene" id="s-close">')
A('<div class="h2" data-cue="0" style="left:120px;top:110px">Parse what you were promised</div>')
cards = [(0, 'var(--muted)', 'General parsers: right for', 'config · command lines · CSV reports · tests'),
         (1, 'var(--teal)', 'Feed handler: fixed format', 'the venue spec defines every byte'),
         (2, 'var(--amber)', 'State the constraints', 'no allocation · integer ticks · reject off-spec'),
         (2.5, 'var(--amber)', 'Errors as values', 'return false / an error code, not a throw')]
for i, (c, col, t, s) in enumerate(cards):
    x = 120 + (i % 2) * 850; y = 220 + (i // 2) * 190
    A(f'<div class="card2" data-cue="{c}" data-d="0.3" style="left:{x}px;top:{y}px;width:810px;height:160px;border-color:{col}"><div class="ct">{t}</div><div class="cs">{s}</div></div>')
A('<div class="rule" data-cue="3" style="left:120px;top:640px;width:1660px">Parse the bytes you were promised, <span class="c-amber">straight into the type you will use.</span></div>')
A('</div>')
open(f'{OUT}/scenes.html', 'w').write('\n'.join(h) + '\n')
css = open('/tmp/claude-0/vx/ai1316tools/common.css').read() + '''
.hatch{height:30px;border-radius:0 6px 6px 0;background:repeating-linear-gradient(45deg,rgba(255,107,94,.55) 0 8px,rgba(255,107,94,.15) 8px 16px)}
.cpu{height:60px;border-radius:10px;border:2px solid var(--line);background:transparent}
'''
open(f'{OUT}/style.css', 'w').write(css)
print('ok')
