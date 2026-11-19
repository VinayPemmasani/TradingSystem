# Code-block HTML helper for scenes.html: escaping, light C++/asm colouring, per-line highlight cues.
import html, re
KW = set("""alignas auto bool break case char class const constexpr continue default delete do double else enum explicit
extern false final for if inline int long namespace noexcept nullptr operator override private public return short
signed sizeof static static_assert struct switch template this true typename using virtual void volatile while
concept requires""".split())
TY = set("""size_t uint8_t uint32_t uint64_t int64_t u8 T std atomic mutex lock_guard optional variant Order Hot Strategy
Maker Taker Quote Market Book unique_ptr vector array SpscRing MutexQueue Ring Capacity""".split())
TOK = re.compile(r'(//.*$)|("(?:[^"\\]|\\.)*")|(\[\[\w+\]\])|(\b0x[0-9a-fA-F]+\b|\$-?\d+|\b\d+\b)|([A-Za-z_]\w*)|(\s+)|(.)')
def hl_cpp(s):
    out = []
    for m in TOK.finditer(s):
        c, st, at, num, w, sp, o = m.groups()
        if c: out.append(f'<span class="c">{html.escape(c)}</span>')
        elif st: out.append(f'<span class="g">{html.escape(st)}</span>')
        elif at: out.append(f'<span class="v">{html.escape(at)}</span>')
        elif num: out.append(f'<span class="r">{html.escape(num)}</span>')
        elif w:
            if w in KW: out.append(f'<span class="k">{w}</span>')
            elif w in TY: out.append(f'<span class="v">{w}</span>')
            else: out.append(w)
        else: out.append(html.escape(sp or o))
    return ''.join(out)
def hl_asm(s):
    if '#' in s:
        a, b = s.split('#', 1)
        return hl_asm(a) + f'<span class="c">#{html.escape(b)}</span>'
    m = re.match(r'^(\s*)([a-z]\w*)(\s+)(.*)$', s)
    if s.rstrip().endswith(':'): return f'<span class="r">{html.escape(s)}</span>'
    if m:
        a, op, sp, rest = m.groups()
        rest = re.sub(r'(%\w+)', r'\1', html.escape(rest))
        rest = re.sub(r'(\$-?\d+)', r'<span class="r">\1</span>', rest)
        return f'{a}<span class="k">{op}</span>{sp}{rest}'
    return html.escape(s)
def code(lines, cue, style, hl=None, d=0, lang='cpp', cls='code', extra=''):
    """hl: {line_index: (hl_cue, hl_end or None)}; line_index 0-based."""
    hl = hl or {}
    f = hl_cpp if lang == 'cpp' else hl_asm
    parts = []
    for i, ln in enumerate(lines):
        a = ''
        if i in hl:
            s, e = hl[i]
            a = f' data-hl="{s}"' + (f' data-hlend="{e}"' if e is not None else '')
        parts.append(f'<span class="line"{a}>{f(ln) if ln else " "}</span>')
    dd = f' data-d="{d}"' if d else ''
    return f'<div class="{cls}" data-cue="{cue}"{dd} {extra} style="{style}">' + ''.join(parts) + '</div>'
