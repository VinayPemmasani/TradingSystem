# Generates /mnt/project-files/videos/explainers/rest-api/scenes.html
OUT = "/mnt/project-files/videos/explainers/rest-api/scenes.html"
COL = {"client": "teal", "dns": "violet", "lb": "blue", "api": "amber", "db": "green", "me": "pink"}
HEX = {"teal": "#3fd0dc", "violet": "#a98bff", "blue": "#6aa8ff", "amber": "#ffb347", "green": "#4fd18b",
       "pink": "#ff8fc8", "red": "#ff6b5e", "muted": "#8ea3b1"}
AH = {"teal": "ah-teal", "violet": "ah-violet", "amber": "ah-amber", "green": "ah-green", "red": "ah-red",
      "blue": "ah", "pink": "ah", "muted": "ah"}


def cue(c, d=None, anim=None, out=None):
    s = f' data-cue="{c}"'
    if d: s += f' data-d="{d}"'
    if anim: s += f' data-anim="{anim}"'
    if out is not None: s += f' data-out="{out}"'
    return s


def lane(x, name, sub, col, top, c, d=0, w=230):
    return (f'<div class="box {col} lane"{cue(c, d)} style="left:{x - w // 2}px;top:{top}px;width:{w}px">'
            f'<div class="t c-{col}">{name}</div>' + (f'<div class="s">{sub}</div>' if sub else '') + '</div>')


def life(x, y1, y2, c, d=0):
    return f'<path class="draw lifeline" d="M{x} {y1} L{x} {y2}"{cue(c, d)} data-dur="0.8"/>'


def msg(pid, x1, y1, x2, y2, col, c, d=0, w=5, dash=False):
    sx = 1 if x2 > x1 else -1
    xe = x2 - sx * 10
    ds = ' stroke-dasharray="1 1"' if False else ''
    st = f'stroke:{HEX[col]};stroke-width:{w}' + (';' if not dash else '')
    return (f'<path id="{pid}" class="draw" d="M{x1} {y1} L{xe} {y2}" style="fill:none;{st}"'
            f' marker-end="url(#{AH[col]})"{cue(c, d)} data-dur="0.7"/>')


def mlabel(x1, x2, y, text, col, c, d=0, size=24, dy=-40, sub=None):
    l, r = min(x1, x2), max(x1, x2)
    s = (f'<div class="mlab"{cue(c, d, "fade")} style="left:{l}px;width:{r - l}px;top:{y + dy}px;color:{HEX[col]};font-size:{size}px">{text}'
         + (f'<div class="msub">{sub}</div>' if sub else '') + '</div>')
    return s


def scene(sid, body):
    return f'<div class="scene" id="s-{sid}">\n{body}\n</div>\n'


H = []

# ---------------- 0 TITLE
H.append(scene("title", f'''
<div class="eyebrow"{cue(0)} style="left:140px;top:280px">Trading lab · Protocols</div>
<div class="h1"{cue(0, 0.3)} style="left:132px;top:330px;width:900px">REST API<br>calls</div>
<div class="sub"{cue(0, 0.6)} style="left:140px;top:640px;width:820px">What really happens in one call,<br>and how REST is designed.</div>
<div class="code"{cue(0, 1.2)} style="left:1060px;top:300px;width:720px;font-size:26px"><span class="k">POST</span> /v1/orders
<span class="c">Content-Type: application/json</span>

{{<span class="g">"symbol"</span>: <span class="g">"AAPL"</span>,
 <span class="g">"side"</span>: <span class="g">"BUY"</span>,
 <span class="g">"quantity"</span>: <span class="r">100</span>,
 <span class="g">"price"</span>: <span class="g">"189.25"</span>}}</div>
<div{cue(1, 0, "fade")} style="left:1060px;top:710px;width:720px;display:flex;gap:12px;flex-wrap:wrap">
 <span class="pill c-teal">client</span><span class="pill c-violet">DNS</span><span class="pill c-blue">load balancer</span>
 <span class="pill c-amber">API server</span><span class="pill c-green">database</span><span class="pill c-pink">matching engine</span></div>
'''))

# ---------------- 1 CAST
LX = {"client": 210, "dns": 510, "lb": 810, "api": 1110, "db": 1410, "me": 1710}
NAMES = {"client": ("Client", "your code"), "dns": ("DNS", "resolver"), "lb": ("Load bal.", "venue edge"),
         "api": ("API server", "handlers"), "db": ("Database", "orders"), "me": ("Matching", "engine")}
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Life of one call</div>\n'
b += '<div class="band"' + cue(2, 0, "fade") + f' style="left:{LX["client"] + 30}px;top:345px;width:{LX["lb"] - LX["client"] - 60}px;height:590px"></div>\n'
b += '<div class="lbl c-amber"' + cue(2, 0.2, "fade") + f' style="left:{LX["client"] + 40}px;top:880px;width:{LX["lb"] - LX["client"] - 80}px;text-align:center">internet · 1 RTT per crossing</div>\n'
svg = '<svg class="full">'
for i, k in enumerate(LX):
    b += lane(LX[k], *NAMES[k], COL[k], 220, 1, 0.5 * i, w=250) + "\n"
    svg += life(LX[k], 330, 860, 1, 0.5 * i + 0.3)
svg += '<path class="draw" d="M100 340 L100 840" style="stroke:#8ea3b1;stroke-width:3;fill:none" marker-end="url(#ah)"' + cue(2) + '/>'
svg += f'<path id="cast-rt" d="M{LX["client"]} 420 L{LX["lb"]} 470 L{LX["client"]} 520" style="fill:none;stroke:none"/>'
svg += msg("cast-a1", LX["client"], 420, LX["lb"], 470, "teal", 2, 0.5)
svg += msg("cast-a2", LX["lb"], 500, LX["client"], 550, "blue", 2, 1.2)
svg += '</svg>'
b += svg
b += '<div class="lbl"' + cue(2, 0, "fade") + ' style="left:60px;top:850px">time</div>'
b += '<div class="pkt" data-path="cast-rt"' + cue(2, 2) + ' data-dur="1.6" data-loop="1" style="background:var(--teal)"></div>'
H.append(scene("cast", b))


# shared lanes for connect
def lanes_static(keys, top=200, w=230):
    s, v = "", '<svg class="full">'
    for k in keys:
        s += lane(LX[k], *NAMES[k], COL[k], top, 0, 0, w) + "\n"
        v += life(LX[k], top + 110, 900, 0, 0.1)
    return s, v


# ---------------- 2 CONNECT
s, v = lanes_static(["client", "dns", "lb"])
b = '<div class="h2"' + cue(0) + ' style="left:1000px;top:110px">DNS, then TCP</div>\n' + s
C, D_, L = LX["client"], LX["dns"], LX["lb"]
v += msg("cn-q", C, 360, D_, 390, "teal", 0, 1.0)
v += msg("cn-r", D_, 450, C, 480, "violet", 0, 2.4)
v += msg("cn-syn", C, 520, L, 560, "teal", 1, 0.8)
v += msg("cn-sa", L, 580, C, 620, "blue", 1, 2.2)
v += msg("cn-ack", C, 680, L, 720, "teal", 2, 1.0)
v += f'<path class="draw" d="M150 520 L130 520 L130 620 L150 620" style="fill:none;stroke:#ffb347;stroke-width:3"' + cue(2, 2.6) + '/>'
v += '</svg>'
b += v
b += mlabel(C, D_, 375, "A? api.venue.example", "teal", 0, 1.0)
b += mlabel(C, D_, 465, "203.0.113.10 · TTL 60", "violet", 0, 2.4)
b += '<div class="tag c-muted"' + cue(0, 3.2, "fade") + ' style="left:560px;top:380px">cached? skip it</div>'
b += mlabel(C, L, 540, "SYN", "teal", 1, 0.8)
b += mlabel(C, L, 600, "SYN-ACK", "blue", 1, 2.2)
b += mlabel(C, L, 700, "ACK + first data", "teal", 2, 1.0)
b += '<div class="rtt"' + cue(2, 2.6, "fade") + ' style="left:20px;top:548px">1 RTT</div>'
b += ('<div class="box"' + cue(1, 0.5) + ' style="left:1000px;top:480px;width:800px"><div class="t">Three-way handshake</div>'
      '<div class="s">SYN → SYN-ACK → ACK<br>the client may send data with its ACK</div></div>')
b += ('<div class="box amber"' + cue(2, 2.8) + ' style="left:1000px;top:680px;width:800px"><div class="t c-amber">Cost so far: DNS + 1 RTT</div>'
      '<div class="s">the connection can then stay open (keep-alive)</div></div>')
H.append(scene("connect", b))

# ---------------- 3 TLS
A1, A2, B1, B2 = 180, 800, 1080, 1700
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">TLS 1.3</div>\n'
b += '<div class="lbl"' + cue(1) + ' style="left:120px;top:200px">full handshake · 1-RTT</div>'
b += '<div class="lbl c-amber"' + cue(3) + ' style="left:1000px;top:200px">resumption · 0-RTT</div>'
b += lane(A1, "Client", None, "teal", 250, 1, 0, 200) + lane(A2, "Load bal.", None, "blue", 250, 1, 0, 200)
b += lane(B1, "Client", None, "teal", 250, 3, 0, 200) + lane(B2, "Load bal.", None, "blue", 250, 3, 0, 200)
v = '<svg class="full">' + life(A1, 320, 900, 1) + life(A2, 320, 900, 1) + life(B1, 320, 900, 3) + life(B2, 320, 900, 3)
v += msg("tl-ch", A1, 400, A2, 440, "teal", 1, 0.3)
v += msg("tl-sh", A2, 530, A1, 570, "blue", 2, 0.2)
v += msg("tl-fin", A1, 670, A2, 710, "teal", 2, 3.5)
v += f'<path class="draw" d="M150 400 L135 400 L135 570 L150 570" style="fill:none;stroke:#ffb347;stroke-width:3"' + cue(2, 3.0) + '/>'
v += msg("tl-z", B1, 450, B2, 490, "amber", 3, 0.6)
v += msg("tl-zr", B2, 560, B1, 600, "blue", 3, 2.5)
v += '<path id="tl-rep" class="draw" d="M1080 740 L1690 790" style="fill:none;stroke:#ff6b5e;stroke-width:5;stroke-dasharray:14 10" marker-end="url(#ah-red)"' + cue(4, 0.6) + '/>'
v += '</svg>'
b += v
b += mlabel(A1, A2, 420, "ClientHello + key_share", "teal", 1, 0.3)
b += mlabel(A1, A2, 550, "ServerHello + key_share", "blue", 2, 0.2, sub="{Certificate, Verify, Finished}", dy=-90)
b += mlabel(A1, A2, 690, "Finished + POST /v1/orders", "teal", 2, 3.5)
b += '<div class="rtt"' + cue(2, 3.0, "fade") + ' style="left:30px;top:468px">1 RTT</div>'
b += mlabel(B1, B2, 470, "ClientHello + PSK", "amber", 3, 0.6, sub="+ early_data: POST /v1/orders", dy=-90)
b += mlabel(B1, B2, 580, "ServerHello …", "blue", 3, 2.5)
b += '<div class="box red"' + cue(4, 0.2) + ' style="left:1180px;top:650px;width:400px;text-align:center;padding:10px"><div class="t c-red" style="font-size:26px">attacker replays early data</div></div>'
b += mlabel(B1, B2, 765, "same POST again → second order?", "red", 4, 0.8)
b += ('<div class="note"' + cue(4, 2.0, "fade") + ' style="left:1000px;top:840px;width:800px">RFC 8446 §8: 0-RTT data is not replay-protected · '
      'servers can answer 425 Too Early (RFC 8470)</div>')
H.append(scene("tls", b))

# ---------------- 4 REQUEST
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">The request</div>\n'
b += ('<div class="code"' + cue(0, 0.3) + ' style="left:120px;top:210px;width:1240px;font-size:25px">'
      '<span class="line" data-hl="1" data-hlend="2"><span class="k">POST</span> <span class="v">/v1/orders</span> HTTP/1.1</span>'
      '<span class="line" data-hl="2" data-hlend="3">Host: api.venue.example</span>'
      '<span class="line" data-hl="2" data-hlend="3">Content-Type: application/json</span>'
      '<span class="line" data-hl="2" data-hlend="3">Content-Length: 126</span>'
      '<span class="line" data-hl="2" data-hlend="3">X-API-KEY: <span class="c">7f3a…64 hex</span></span>'
      '<span class="line" data-hl="2" data-hlend="3">X-TIMESTAMP: <span class="r">1763542800123</span></span>'
      '<span class="line" data-hl="2" data-hlend="3">X-RECV-WINDOW: <span class="r">5000</span></span>'
      '<span class="line" data-hl="2" data-hlend="3">X-SIGNATURE: <span class="c">9f2c…64 hex</span></span>'
      '<span class="line" data-hl="2" data-hlend="3">Idempotency-Key: <span class="c">6f1c…uuid</span></span>'
      '<span class="line"> </span>'
      '<span class="line" data-hl="3" data-hlend="4">{"symbol":<span class="g">"AAPL"</span>,"side":<span class="g">"BUY"</span>,"type":<span class="g">"LIMIT"</span>,</span>'
      '<span class="line" data-hl="3" data-hlend="4"> "quantity":<span class="r">100</span>,"price":<span class="g">"189.25"</span>,"timeInForce":<span class="g">"DAY"</span>,</span>'
      '<span class="line" data-hl="3" data-hlend="4"> "clientOrderId":<span class="g">"lab-000123"</span>}</span></div>')
b += '<div class="box amber"' + cue(1) + ' style="left:1420px;top:220px;width:380px"><div class="t c-amber">method + path</div><div class="s">what to do, to which resource</div></div>'
b += '<div class="box teal"' + cue(2) + ' style="left:1420px;top:380px;width:380px"><div class="t c-teal">headers</div><div class="s">who, what format, proof</div></div>'
b += '<div class="box green"' + cue(3) + ' style="left:1420px;top:540px;width:380px"><div class="t c-green">JSON body</div><div class="s">126 bytes of text</div></div>'
b += '<div class="box"' + cue(4) + ' style="left:1420px;top:700px;width:380px"><div class="t">≈ 490 bytes</div><div class="s">as HTTP/1.1 text<br>framing → HTTP video</div></div>'
H.append(scene("request", b))

# ---------------- 5 SIGN
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Signing · HMAC-SHA256</div>\n'
b += '<div class="lbl"' + cue(0, 0.5) + ' style="left:120px;top:200px">a common pattern, shown generically · exact string and header names differ per venue</div>'
chips = [("timestamp", "1763542800123", "amber"), ("method", "POST", "teal"), ("path", "/v1/orders", "violet"), ("body", '{"symbol":"AAPL",…}', "green")]
x = 120
for i, (n, val, col) in enumerate(chips):
    w = 300 if i < 3 else 420
    b += f'<div class="box {col}"' + cue(1, 0.4 * i) + f' style="left:{x}px;top:260px;width:{w}px;padding:12px 18px"><div class="lbl">{n}</div><div class="mono c-{col}" style="font-size:24px;margin-top:4px">{val}</div></div>'
    x += w + 30
b += ('<div class="code"' + cue(1, 2.0) + ' style="left:120px;top:420px;width:1680px;font-size:24px">'
      '<span class="r">1763542800123</span><span class="k">POST</span><span class="v">/v1/orders</span><span class="g">{"symbol":"AAPL","side":"BUY",…}</span></div>')
b += '<div class="box pink"' + cue(2) + ' style="left:120px;top:540px;width:300px;text-align:center"><div class="t c-pink">secret key</div><div class="s">never sent</div></div>'
b += '<div class="box"' + cue(2, 0.6) + ' style="left:540px;top:540px;width:480px;text-align:center"><div class="t">HMAC-SHA256</div><div class="s">(secret, string)</div></div>'
b += '<div class="code"' + cue(2, 1.4) + ' style="left:1140px;top:550px;width:660px;font-size:24px">X-SIGNATURE: <span class="c">9f2c41…e07a</span></div>'
v = '<svg class="full">'
v += '<path class="draw" d="M420 600 L530 600" style="fill:none;stroke:#ff8fc8;stroke-width:4" marker-end="url(#ah)"' + cue(2, 0.6) + '/>'
v += '<path class="draw" d="M1020 600 L1130 600" style="fill:none;stroke:#8ea3b1;stroke-width:4" marker-end="url(#ah)"' + cue(2, 1.2) + '/>'
v += '</svg>'
b += v
# window timeline
b += '<div class="box blue"' + cue(3) + ' style="left:120px;top:720px;width:560px"><div class="t c-blue">server</div><div class="s">recompute, compare<br>check |now − timestamp|</div></div>'
b += '<div class="axis"' + cue(3, 0.5, "fade") + ' style="left:780px;top:820px;width:1020px"></div>'
b += '<div class="win"' + cue(3, 1.0, "fade") + ' style="left:1240px;top:770px;width:400px;height:100px"><span>receive window · 5 s</span></div>'
b += '<div class="tick c-blue"' + cue(3, 0.8, "fade") + ' style="left:1580px;top:840px">now</div>'
b += '<div class="dot"' + cue(3, 1.6, "scale") + ' style="left:1500px;top:808px;background:var(--green)"></div>'
b += '<div class="tick c-green"' + cue(3, 1.6, "fade") + ' style="left:1470px;top:730px">✓ fresh</div>'
b += '<div class="dot"' + cue(4, 0, "scale") + ' style="left:900px;top:808px;background:var(--red)"></div>'
b += '<div class="tick c-red"' + cue(4, 0, "fade") + ' style="left:830px;top:730px">✕ replayed copy</div>'
b += '<div class="tick c-muted"' + cue(4, 2.5, "fade") + ' style="left:800px;top:870px">or: nonce must increase</div>'
H.append(scene("sign", b))

# ---------------- 6 SERVER
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Inside the venue</div>\n'
stages = [("Load bal.", "TLS ends here<br>health checks", "blue", 0), ("Router", "POST /v1/orders<br>→ placeOrder", "violet", 1),
          ("Auth", "key + signature", "teal", 2), ("Validate", "symbol, qty,<br>price on tick", "teal", 2.5), ("Handler", "risk, persist,<br>forward", "amber", 3)]
x0, w, gap = 120, 290, 57
xs = []
for i, (n, sub, col, c) in enumerate(stages):
    x = x0 + i * (w + gap); xs.append(x)
    cc = 2 if c == 2.5 else c
    dd = 1.5 if c == 2.5 else 0.3
    b += f'<div class="box {col}"' + cue(cc, dd) + f' style="left:{x}px;top:240px;width:{w}px;height:150px"><div class="t c-{col}">{n}</div><div class="s">{sub}</div></div>'
v = '<svg class="full">'
for i in range(4):
    a = xs[i] + w; c = [0, 1, 2, 2, 3][i + 1]; d = [0, 0.3, 0.3, 1.5, 0.3][i + 1] - 0.2
    v += f'<path class="draw" d="M{a} 315 L{a + gap - 4} 315" style="fill:none;stroke:#8ea3b1;stroke-width:4" marker-end="url(#ah)"' + cue(c, max(d, 0)) + '/>'
hx = xs[4] + w // 2
v += f'<path id="sv-flow" d="M60 315 L{hx - 40} 315 L{hx - 40} 450 L1165 450 L1165 548" style="fill:none;stroke:none"/>'
v += f'<path class="draw" d="M{hx - 40} 390 L{hx - 40} 450 L1165 450 L1165 548" style="fill:none;stroke:#4fd18b;stroke-width:4" marker-end="url(#ah-green)"' + cue(3, 0.4) + '/>'
v += f'<path class="draw" d="M{hx + 50} 390 L{hx + 50} 548" style="fill:none;stroke:#ff8fc8;stroke-width:4" marker-end="url(#ah)"' + cue(3, 2.2) + '/>'
v += '<path id="sv-resp" class="draw" d="M265 395 L265 588" style="fill:none;stroke:#3fd0dc;stroke-width:5" marker-end="url(#ah-teal)"' + cue(4, 0.2) + '/>'
v += '</svg>'
b += v
b += '<div class="box green"' + cue(3, 0.6) + ' style="left:1000px;top:560px;width:330px;text-align:center"><div class="t c-green">Database</div><div class="s">INSERT order</div></div>'
b += '<div class="box pink"' + cue(3, 2.4) + ' style="left:1390px;top:560px;width:330px;text-align:center"><div class="t c-pink">Matching engine</div><div class="s">internal binary link</div></div>'
b += ('<div class="code"' + cue(4, 0.6) + ' style="left:120px;top:600px;width:740px;font-size:24px"><span class="g">HTTP/1.1 201 Created</span>\n'
      'Location: /v1/orders/8812\n\n{"orderId":<span class="g">"8812"</span>,\n "clientOrderId":<span class="g">"lab-000123"</span>,\n "status":<span class="g">"NEW"</span>}</div>')
b += '<div class="pkt" data-path="sv-flow"' + cue(3, 0) + ' data-dur="3" style="background:var(--teal)"></div>'
b += '<div class="note"' + cue(4, 2.0, "fade") + ' style="left:1000px;top:730px;width:800px">fills arrive later: a stream, or GET /v1/orders/8812</div>'
H.append(scene("server", b))

# ---------------- 7 VERBS
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Resources and verbs</div>\n'
b += '<div class="lbl"' + cue(1) + ' style="left:120px;top:230px">resources, named by URIs</div>'
b += '<div class="box teal"' + cue(1, 0.3) + ' style="left:120px;top:280px;width:620px"><div class="mono" style="font-size:32px">/v1/orders</div><div class="s">collection · GET lists, POST creates</div></div>'
b += '<div class="box violet"' + cue(1, 3.0) + ' style="left:220px;top:440px;width:620px"><div class="mono" style="font-size:32px">/v1/orders/42</div><div class="s">one order · GET, DELETE cancels</div></div>'
b += '<div class="box"' + cue(1, 5.0) + ' style="left:320px;top:600px;width:620px"><div class="mono" style="font-size:32px">/v1/orders/42/fills</div><div class="s">sub-resource</div></div>'
v = '<svg class="full"><path class="draw" d="M160 375 L160 500 L210 500" style="fill:none;stroke:#2c4351;stroke-width:3"' + cue(1, 3.0) + '/>'
v += '<path class="draw" d="M260 535 L260 660 L310 660" style="fill:none;stroke:#2c4351;stroke-width:3"' + cue(1, 5.0) + '/></svg>'
b += v
rows = [("GET", "✓", "✓", 2), ("HEAD", "✓", "✓", 2), ("PUT", "✕", "✓", 3), ("DELETE", "✕", "✓", 3), ("POST", "✕", "✕", 4), ("PATCH", "✕", "✕", 4)]
t = '<table class="t verbs"' + cue(2) + ' style="left:1080px;top:230px;width:720px"><tr><th>method</th><th>safe</th><th>idempotent</th></tr>'
for m, s_, i_, c in rows:
    f = lambda x: f'<span class="{"c-green" if x == "✓" else "c-red"}">{x}</span>'
    t += f'<tr{cue(c, 0.4 if m in ("HEAD", "DELETE", "PATCH") else 0, "fade")}><td class="mono">{m}</td><td>{f(s_)}</td><td>{f(i_)}</td></tr>'
t += '</table>'
b += t
b += '<div class="note"' + cue(4, 1.0, "fade") + ' style="left:1080px;top:760px;width:720px">RFC 9110 §9.2 · OPTIONS and TRACE are also safe · PATCH is RFC 5789</div>'
H.append(scene("verbs", b))

# ---------------- 8 STATUS
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Status codes</div>\n'
groups = [
    (1, "green", "2xx · success", [("200", "OK"), ("201", "Created"), ("202", "Accepted")]),
    (2, "amber", "4xx · client error", [("400", "Bad Request"), ("401", "Unauthorized"), ("403", "Forbidden"), ("404", "Not Found")]),
    (3, "amber", "", [("409", "Conflict"), ("422", "Unprocessable Content")]),
    (5, "red", "5xx · server error", [("500", "Internal Server Error"), ("503", "Service Unavailable")]),
]
ypos = {1: 220, 2: 380, 3: 540, 5: 790}
for c, col, title, codes in groups:
    y = ypos[c]
    if title: b += f'<div class="lbl c-{col}"' + cue(c) + f' style="left:120px;top:{y}px">{title}</div>'
    x = 120
    for k, (code, name) in enumerate(codes):
        w = 130 + len(name) * 13
        b += f'<div class="sc {col}"' + cue(c, 0.25 * k + 0.2) + f' style="left:{x}px;top:{y + 40}px;width:{w}px"><b>{code}</b> {name}</div>'
        x += w + 24
b += '<div class="sc amber big"' + cue(4) + ' style="left:120px;top:700px;width:520px"><b>429</b> Too Many Requests</div>'
b += '<div class="code"' + cue(4, 0.8) + ' style="left:690px;top:690px;width:430px;font-size:26px">Retry-After: <span class="r">2</span></div>'
b += '<div class="note"' + cue(4, 1.5, "fade") + ' style="left:1150px;top:705px;width:650px">seconds, or an HTTP date</div>'
b += '<div class="note"' + cue(2, 2.5, "fade") + ' style="left:1350px;top:395px;width:450px">401 means not authenticated · 403 means authenticated but not allowed</div>'
b += '<div class="note"' + cue(3, 3.0, "fade") + ' style="left:1350px;top:560px;width:450px">422: well-formed JSON, but e.g. price off tick</div>'
H.append(scene("status", b))

# ---------------- 9 IDEM
C2, S2 = 260, 980
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">"Did my order go in?"</div>\n'
b += lane(C2, "Client", None, "teal", 220, 0, 0.5, 220) + lane(S2, "API server", None, "amber", 220, 0, 0.5, 260)
v = '<svg class="full">' + life(C2, 290, 900, 0, 0.8) + life(S2, 290, 900, 0, 0.8)
v += msg("id-p1", C2, 340, S2, 370, "teal", 1, 0.2)
v += '<path class="draw" d="M980 400 L640 425" style="fill:none;stroke:#ff6b5e;stroke-width:5;stroke-dasharray:12 10"' + cue(1, 1.2) + '/>'
v += msg("id-p2", C2, 530, S2, 560, "teal", 3, 0.2)
v += msg("id-p3", C2, 690, S2, 720, "teal", 4, 2.0)
v += msg("id-r3", S2, 750, C2, 780, "green", 6, 0.6)
v += '</svg>'
b += v
b += mlabel(C2, S2, 355, "POST /v1/orders", "teal", 1, 0.2)
b += '<div class="tag c-amber"' + cue(1, 0.9, "fade") + ' style="left:1010px;top:350px">order 8812 placed</div>'
b += '<div class="tag c-red"' + cue(1, 1.5, "fade") + ' style="left:560px;top:430px">timeout ✕</div>'
b += '<div class="big-q"' + cue(2, 0, "scale", 3) + ' style="left:120px;top:380px">?</div>'
b += mlabel(C2, S2, 545, "retry, no key", "teal", 3, 0.2)
b += '<div class="tag c-red"' + cue(3, 1.0, "fade") + ' style="left:1010px;top:540px">order 8813 placed · bought twice</div>'
b += mlabel(C2, S2, 705, "retry · Idempotency-Key: 6f1c…", "teal", 4, 2.0)
b += mlabel(C2, S2, 765, "201 · order 8812 (stored result)", "green", 6, 0.6, dy=24)
b += ('<div class="box amber"' + cue(5) + ' style="left:1260px;top:600px;width:540px"><div class="lbl">key store</div>'
      '<div class="mono" style="font-size:24px;margin-top:8px">6f1c… → <span class="c-green">201, order 8812</span></div></div>')
b += '<div class="note"' + cue(6, 1.8, "fade") + ' style="left:1260px;top:770px;width:540px">Idempotency-Key header: IETF draft · many venues dedupe on client order ID</div>'
H.append(scene("idem", b))

# ---------------- 10 ETAG
XA, XS, XB = 260, 960, 1660
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">ETags · optimistic concurrency</div>\n'
b += lane(XA, "Client A", None, "teal", 210, 0, 0.5, 220) + lane(XS, "/risk-limits", None, "amber", 210, 0, 0.5, 280) + lane(XB, "Client B", None, "violet", 210, 0, 0.5, 220)
v = '<svg class="full">' + life(XA, 280, 900, 0, 0.8) + life(XS, 280, 900, 0, 0.8) + life(XB, 280, 900, 0, 0.8)
v += msg("et-g1", XS, 340, XA, 370, "amber", 1, 0.4)
v += msg("et-g2", XS, 340, XB, 370, "amber", 1, 1.4)
v += msg("et-pb", XB, 470, XS, 500, "violet", 2, 0.3)
v += msg("et-pa", XA, 600, XS, 630, "teal", 3, 0.3)
v += msg("et-412", XS, 680, XA, 710, "red", 3, 2.0)
v += msg("et-re", XA, 830, XS, 860, "teal", 3, 5.0)
v += '</svg>'
b += v
b += mlabel(XA, XS, 355, '200 · ETag: "v7"', "amber", 1, 0.4)
b += mlabel(XS, XB, 355, '200 · ETag: "v7"', "amber", 1, 1.4)
b += mlabel(XS, XB, 485, 'PUT · If-Match: "v7"', "violet", 2, 0.3)
b += '<div class="tag c-green"' + cue(2, 1.4, "fade") + ' style="left:1000px;top:520px">200 · now "v8"</div>'
b += mlabel(XA, XS, 615, 'PUT · If-Match: "v7"', "teal", 3, 0.3)
b += mlabel(XA, XS, 695, '412 Precondition Failed', "red", 3, 2.0, dy=26)
b += mlabel(XA, XS, 845, 'GET again → "v8", then retry', "teal", 3, 5.0)
b += '<div class="note"' + cue(4, 0.3, "fade") + ' style="left:1000px;top:640px;width:600px">no lock is held between calls · conflicts are detected, not prevented</div>'
H.append(scene("etag", b))

# ---------------- 11 RULES
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Pages, limits, versions</div>\n'
b += '<div class="lbl c-red"' + cue(1) + ' style="left:120px;top:220px">?offset=3&amp;limit=3</div>'
b += '<div class="lbl c-green"' + cue(2) + ' style="left:560px;top:220px">?after=ord_8812&amp;limit=3</div>'
rowsA = ["8814", "8813", "8812", "8811", "8810", "8809"]
for i, r in enumerate(rowsA):
    y = 340 + i * 62
    b += f'<div class="row"' + cue(1, 0.1 * i, "fade") + f' style="left:120px;top:{y}px;width:360px">ord_{r}</div>'
    b += f'<div class="row"' + cue(2, 0.1 * i, "fade") + f' style="left:560px;top:{y}px;width:360px">ord_{r}</div>'
# new row inserted for offset view
b += '<div class="row new"' + cue(1, 2.0, "left") + ' style="left:120px;top:278px;width:360px">ord_8815 · new</div>'
b += '<div class="row new"' + cue(2, 0.6, "left") + ' style="left:560px;top:278px;width:360px">ord_8815 · new</div>'
b += '<div class="pagebox muted"' + cue(1, 0.8, "fade") + ' style="left:104px;top:330px;width:392px;height:196px"></div>'
b += '<div class="pagebox red"' + cue(1, 3.0, "fade") + ' style="left:110px;top:454px;width:380px;height:196px"></div>'
b += '<div class="tag c-red"' + cue(1, 3.4, "fade") + ' style="left:120px;top:730px">page 2 repeats ord_8812</div>'
b += '<div class="tick c-muted"' + cue(1, 0.8, "fade") + ' style="left:390px;top:352px;font-size:18px">page 1</div>'
b += '<div class="tick c-red"' + cue(1, 3.0, "fade") + ' style="left:390px;top:600px;font-size:18px">page 2</div>'
b += '<div class="tick c-green"' + cue(2, 1.0, "fade") + ' style="left:830px;top:662px;font-size:18px">page 2</div>'
b += '<div class="pagebox green"' + cue(2, 1.0, "fade") + ' style="left:550px;top:516px;width:380px;height:196px"></div>'
b += '<div class="tag c-green"' + cue(2, 1.4, "fade") + ' style="left:560px;top:730px">continues after ord_8812</div>'
# limits
b += '<div class="lbl"' + cue(3) + ' style="left:1080px;top:220px">rate limit · example weights</div>'
lim = [("GET /ticker", 1, "teal"), ("POST /orders", 1, "amber"), ("GET /orders?all", 40, "violet")]
for i, (n, wgt, col) in enumerate(lim):
    y = 270 + i * 70
    b += f'<div class="mono"' + cue(3, 0.3 * i, "fade") + f' style="left:1080px;top:{y}px;font-size:24px;width:300px">{n}</div>'
    b += f'<div class="grow bar" data-w="{9 * wgt}"' + cue(3, 0.3 * i + 0.2) + f' style="left:1340px;top:{y - 4}px;background:var(--{col})"></div>'
    b += f'<div class="mono c-muted"' + cue(3, 0.3 * i + 0.6, "fade") + f' style="left:{1340 + 9 * wgt + 14}px;top:{y}px;font-size:22px">w {wgt}</div>'
b += '<div class="note"' + cue(3, 2.0, "fade") + ' style="left:1080px;top:490px;width:720px">budget per window · over it → 429</div>'
# versions
b += '<div class="lbl"' + cue(4) + ' style="left:1080px;top:590px">versioning</div>'
b += '<div class="box"' + cue(4, 0.3) + ' style="left:1080px;top:640px;width:330px"><div class="mono c-teal" style="font-size:30px">/v1/orders</div><div class="s">keeps working</div></div>'
b += '<div class="box"' + cue(4, 1.0) + ' style="left:1470px;top:640px;width:330px"><div class="mono c-violet" style="font-size:30px">/v2/orders</div><div class="s">new shape</div></div>'
b += '<div class="note"' + cue(4, 2.0, "fade") + ' style="left:1080px;top:790px;width:720px">or a header, or a media type</div>'
H.append(scene("rules", b))

# ---------------- 12 RTT
PX = 22  # px per ms
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">Counting round trips</div>\n'
b += '<div class="lbl"' + cue(1) + ' style="left:120px;top:240px">cold call</div>'
segs = [("DNS", 0, 12, "violet", "≥0"), ("TCP", 12, 20, "blue", "1 RTT"), ("TLS 1.3", 32, 20, "amber", "1 RTT"), ("request", 52, 20, "teal", "1 RTT")]
for i, (n, x, w, col, l) in enumerate(segs):
    left = 120 + x * PX
    st = 'background:repeating-linear-gradient(45deg,#a98bff 0 10px,#6a56a8 10px 20px)' if n == "DNS" else f'background:var(--{col})'
    b += f'<div class="grow seg" data-w="{w * PX - 6}"' + cue(1, 0.9 * i, "fade") + f' style="left:{left}px;top:280px;{st}">{n}</div>'
    b += f'<div class="lbl"' + cue(1, 0.9 * i + 0.5, "fade") + f' style="left:{left}px;top:390px;width:{w * PX - 6}px;text-align:center">{l}</div>'
b += '<div class="tag c-violet"' + cue(1, 4.0, "fade") + ' style="left:120px;top:440px">DNS: 0 if cached, else a resolver round trip</div>'
b += '<div class="lbl"' + cue(2) + ' style="left:120px;top:540px">warm keep-alive call</div>'
b += f'<div class="grow seg" data-w="{20 * PX - 6}"' + cue(2, 0.6, "fade") + f' style="left:120px;top:580px;background:var(--teal)">request</div>'
b += f'<div class="lbl"' + cue(2, 1.0, "fade") + f' style="left:120px;top:690px;width:{20 * PX - 6}px;text-align:center">1 RTT</div>'
b += ('<div class="box amber"' + cue(3) + ' style="left:1080px;top:540px;width:720px"><div class="lbl">typical · 20 ms internet RTT</div>'
      '<div style="font:700 44px var(--mono);margin-top:10px">cold ≈ <span class="count c-amber" data-from="0" data-to="60"' + cue(3, 2.5) + '>0</span> ms + DNS</div>'
      '<div style="font:700 44px var(--mono);margin-top:6px">warm ≈ <span class="count c-teal" data-from="0" data-to="20"' + cue(3, 4.5) + '>0</span> ms</div>'
      '<div class="s">plus server time in both</div></div>')
b += '<div class="note"' + cue(3, 6.0, "fade") + ' style="left:120px;top:780px;width:900px">HTTP/1.1 keep-alive or HTTP/2 reuse the connection · 0-RTT is unsafe for orders</div>'
H.append(scene("rtt", b))

# ---------------- 13 TRADING
b = '<div class="h2"' + cue(0) + ' style="left:120px;top:110px">REST in trading</div>\n'
b += '<div class="box green"' + cue(0, 1.0) + ' style="left:120px;top:210px;width:540px"><div class="t c-green">REST</div><div class="s">accounts · balances<br>reference data · slow order entry</div></div>'
b += '<div class="box red"' + cue(1) + ' style="left:120px;top:370px;width:540px"><div class="t c-red">not REST</div><div class="s">market data → ITCH multicast<br>fast orders → OUCH / SoupBinTCP</div></div>'
b += '<div class="lbl"' + cue(2) + ' style="left:760px;top:210px">one new order, bytes on the stream</div>'
b += '<div class="mono c-pink"' + cue(2, 0.5, "fade") + ' style="left:760px;top:258px;font-size:24px">OUCH Enter Order 47 + SoupBinTCP 3 = 50 B</div>'
b += '<div class="grow seg" data-w="100"' + cue(2, 1.0, "fade") + ' style="left:760px;top:300px;height:56px;background:var(--pink)"></div>'
b += '<div class="mono c-amber"' + cue(3, 0, "fade") + ' style="left:760px;top:378px;font-size:24px">signed JSON over HTTP/1.1 ≈ 490 B of text</div>'
b += '<div class="grow seg" data-w="984"' + cue(3, 0.4, "fade") + ' style="left:760px;top:420px;height:56px;background:var(--amber)"></div>'
b += '<div class="lbl"' + cue(4) + ' style="left:120px;top:515px">latency to an answer · typical, log scale</div>'
import math
def lx(us): return 280 * math.log10(us / 10)
lat = [("colocated OUCH", 30, "pink", "tens of µs"), ("REST warm, 20 ms RTT", 20000, "teal", "≈ 20 ms"), ("REST cold", 60000, "amber", "≈ 60 ms + DNS")]
for i, (n, us, col, l) in enumerate(lat):
    y = 570 + i * 80
    w = max(int(lx(us)), 8)
    b += f'<div class="mono"' + cue(4, 0.6 * i, "fade") + f' style="left:120px;top:{y + 8}px;font-size:24px;width:400px">{n}</div>'
    b += f'<div class="grow seg" data-w="{w}"' + cue(4, 0.6 * i + 0.2, "fade") + f' style="left:520px;top:{y}px;height:52px;background:var(--{col})"></div>'
    b += f'<div class="mono c-{col}"' + cue(4, 0.6 * i + 1.0, "fade") + f' style="left:{520 + w + 16}px;top:{y + 8}px;font-size:24px">{l}</div>'
axis = '<div class="lbl"' + cue(4, 0.2, "fade") + ' style="left:520px;top:815px;width:1300px;height:30px">'
for k, lab in enumerate(["10 µs", "100 µs", "1 ms", "10 ms", "100 ms"]):
    axis += f'<span style="position:absolute;left:{280 * k - 30}px">{lab}</span>'
axis += '</div>'
b += axis
H.append(scene("trading", b))

open(OUT, "w").write("".join(H))
print("ok", len(H))
