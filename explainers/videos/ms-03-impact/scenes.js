// ---- shared helpers for the market microstructure series (ms-01..10) ----
window.MS = (function () {
  const NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  // A chart inside a positioned div. o: {w,h,x:[a,b],y:[a,b],xt:[],yt:[],fx,fy,pad:{l,b,t,r},xl,yl}
  function chart(id, o) {
    const host = document.getElementById(id); if (!host) return null;
    if (host._chart) return host._chart;
    const pad = Object.assign({ l: 90, b: 50, t: 16, r: 20 }, o.pad || {});
    const W = o.w, Hh = o.h;
    const svg = el('svg', { width: W, height: Hh, class: 'chart', style: 'position:absolute;left:0;top:0;overflow:visible' }, host);
    const X = (v) => pad.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * (W - pad.l - pad.r);
    const Y = (v) => Hh - pad.b - (v - o.y[0]) / (o.y[1] - o.y[0]) * (Hh - pad.t - pad.b);
    const fx = o.fx || ((v) => String(v)), fy = o.fy || ((v) => String(v));
    for (const t of o.yt || []) { el('line', { x1: pad.l, x2: W - pad.r, y1: Y(t), y2: Y(t), class: 'grid' }, svg); const tx = el('text', { x: pad.l - 12, y: Y(t) + 7, 'text-anchor': 'end' }, svg); tx.textContent = fy(t); }
    for (const t of o.xt || []) { const tx = el('text', { x: X(t), y: Hh - pad.b + 32, 'text-anchor': 'middle' }, svg); tx.textContent = fx(t); }
    el('line', { x1: pad.l, x2: W - pad.r, y1: Hh - pad.b, y2: Hh - pad.b, class: 'ax' }, svg);
    el('line', { x1: pad.l, x2: pad.l, y1: pad.t, y2: Hh - pad.b, class: 'ax' }, svg);
    if (o.xl) { const t = el('text', { x: W - pad.r, y: Hh - pad.b + 32 + (o.xt && o.xt.length ? 0 : 0), 'text-anchor': 'end', dy: o.xt && o.xt.length ? 34 : 0 }, svg); t.textContent = o.xl; }
    if (o.yl) { const t = el('text', { x: pad.l, y: pad.t - 14 }, svg); t.textContent = o.yl; }
    const c = {
      svg, X, Y,
      line(pts, color, width, dash) { const d = pts.map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join(' ');
        const p = el('path', { d, fill: 'none', stroke: color, 'stroke-width': width || 4, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', pathLength: 1 }, svg);
        if (dash) p.setAttribute('data-dash', dash); p.style.strokeDasharray = '1 1'; p.style.strokeDashoffset = '1'; return p; },
      step(pts, color, width) { const q = []; for (let i = 0; i < pts.length; i++) { if (i) q.push([pts[i][0], pts[i - 1][1]]); q.push(pts[i]); } return c.line(q, color, width); },
      dot(x, y, r, color) { return el('circle', { cx: X(x), cy: Y(y), r: r || 7, fill: color }, svg); },
      bar(x, y0, y1, w, color) { const a = Math.min(Y(y0), Y(y1)), b = Math.max(Y(y0), Y(y1)); return el('rect', { x: X(x) - w / 2, y: a, width: w, height: b - a, fill: color, rx: 4 }, svg); },
      text(x, y, s, color, anchor, size) { const t = el('text', { x: X(x), y: Y(y), fill: color || '#8ea3b1', 'text-anchor': anchor || 'start', style: 'fill:' + (color || '#8ea3b1') + (size ? ';font-size:' + size + 'px' : '') }, svg); t.textContent = s; return t; },
      hline(y, color, dash) { return el('line', { x1: pad.l, x2: W - pad.r, y1: Y(y), y2: Y(y), stroke: color, 'stroke-width': 2, 'stroke-dasharray': dash || '8 8' }, svg); },
      vline(x, color, dash) { return el('line', { x1: X(x), x2: X(x), y1: pad.t, y2: Hh - pad.b, stroke: color, 'stroke-width': 2, 'stroke-dasharray': dash || '8 8' }, svg); }
    };
    host._chart = c; return c;
  }
  function reveal(path, p) { if (path) path.style.strokeDashoffset = String(1 - Math.max(0, Math.min(1, p))); }
  function vis(e, p) { if (e) e.style.opacity = Math.max(0, Math.min(1, p)); }
  // Price ladder. o: {rows, rowH, pw (price col), sw (size col), max}
  function ladder(id, o) {
    const host = document.getElementById(id); if (!host) return null;
    if (host._lad) return host._lad;
    host.classList.add('lad');
    const rh = o.rowH || 60, pw = o.pw || 170, sw = o.sw || 260;
    host.style.width = (pw + 2 * sw) + 'px'; host.style.height = (o.rows * rh) + 'px';
    const hb = document.createElement('div'); hb.className = 'lhead'; hb.style.left = '0px'; hb.textContent = 'BID SIZE'; host.appendChild(hb);
    const ha = document.createElement('div'); ha.className = 'lhead'; ha.style.left = (sw + pw) + 'px'; ha.textContent = 'ASK SIZE'; host.appendChild(ha);
    const rows = [];
    for (let i = 0; i < o.rows; i++) {
      const r = document.createElement('div'); r.className = 'lr'; r.style.cssText = `top:${i * rh}px;height:${rh}px;width:${pw + 2 * sw}px`;
      r.innerHTML = `<div class="lb" style="width:${sw}px"><div class="lbar"></div><div class="lq"></div></div><div class="lp" style="width:${pw}px"></div><div class="la" style="width:${sw}px"><div class="lbar"></div><div class="lq"></div></div>`;
      host.appendChild(r); rows.push(r);
    }
    const L = {
      rows, rowH: rh,
      // levels: top row first: [{p:'50.02', b:0, a:2700}]
      set(levels, max) {
        for (let i = 0; i < rows.length; i++) {
          const lv = levels[i] || { p: '', b: 0, a: 0 }; const r = rows[i];
          r.children[1].textContent = lv.p;
          const bb = r.children[0], aa = r.children[2];
          const setSide = (box, q) => { const w = q > 0 ? Math.max(6, (sw - 12) * Math.min(1, q / max)) : 0; box.children[0].style.width = w + 'px'; const s = q > 0 ? q.toLocaleString('en-US') : ''; if (box.children[1].textContent !== s) box.children[1].textContent = s; };
          setSide(bb, lv.b); setSide(aa, lv.a);
          r.style.background = lv.hl ? 'rgba(255,179,71,.18)' : '';
        }
      }
    };
    host._lad = L; return L;
  }
  const f2 = (v) => v.toFixed(2), f3 = (v) => v.toFixed(3), f4 = (v) => v.toFixed(4);
  return { el, chart, reveal, vis, ladder, f2, f3, f4 };
})();


// ---- ms-03 impact ----
(function () {
  SCENES['title'] = {
    setup() { const c = MS.chart('ti-ch', { w: 1100, h: 330, x: [0, 20], y: [0, 1.2], pad: { l: 20, b: 20 } });
      const P = []; for (let i = 0; i <= 20; i++) P.push([i, Math.sqrt(i / 20) + 0.04 * Math.sin(i * 1.7)]);
      c.p = c.line(P, '#3fd0dc', 5); c.d = []; for (let i = 1; i <= 19; i += 2) c.d.push(c.dot(i, 0.06, 9, '#4fd18b')); },
    draw(u, cue, H) { const c = MS.chart('ti-ch', {}); const k = H.C((u - cue(1)) / 3);
      MS.reveal(c.p, k); c.d.forEach((d, i) => MS.vis(d, k * 20 > i * 2 + 1 ? 1 : 0)); }
  };
  SCENES['kyle'] = {
    setup() { const c = MS.chart('ky-ch', { w: 660, h: 420, x: [-3, 3], y: [-3, 3], xt: [-2, 0, 2], yt: [-2, 0, 2], xl: 'order flow x + u', yl: 'p − μ', pad: { l: 70 } });
      c.l = c.line([[-3, -1.5], [3, 1.5]], '#ffb347', 5); c.l2 = c.line([[-3, -0.75], [3, 0.75]], '#a98bff', 4); c.t2 = c.text(2.9, -0.4, 'more noise: flatter', '#a98bff', 'end', 20); },
    draw(u, cue, H) { const c = MS.chart('ky-ch', {}); MS.reveal(c.l, (u - cue(1) - 0.3) / 1); MS.reveal(c.l2, (u - cue(4)) / 1); MS.vis(c.t2, H.C((u - cue(4) - 0.8) / 0.4)); }
  };
  SCENES['kworked'] = {
    setup() { const c = MS.chart('kw-ch', { w: 780, h: 520, x: [0, 1], y: [100, 101.2], xt: [], yt: [100, 100.5, 101], fy: (v) => '$' + v.toFixed(2), pad: { l: 110 } });
      c.v = c.line([[0, 101], [1, 101]], '#a98bff', 3); c.vt = c.text(0.98, 101.05, 'true value (insider knows)', '#a98bff', 'end', 22);
      c.p = c.line([[0, 100], [0.3, 100], [0.7, 100.5], [1, 100.5]], '#3fd0dc', 6); c.pt = c.text(0.98, 100.56, 'price after trading: halfway', '#3fd0dc', 'end', 22);
      c.mt = c.text(0.02, 100.05, 'prior μ = $100', '#8ea3b1', 'start', 22); },
    draw(u, cue, H) { const c = MS.chart('kw-ch', {}); MS.reveal(c.v, (u - cue(4)) / 0.6); MS.vis(c.vt, H.C((u - cue(4) - 0.3) / 0.4)); MS.vis(c.mt, H.C((u - cue(4)) / 0.4));
      MS.reveal(c.p, (u - cue(4) - 0.5) / 1.2); MS.vis(c.pt, H.C((u - cue(4) - 1.5) / 0.4)); }
  };
  SCENES['sqrt'] = {
    setup() { const c = MS.chart('sq-ch', { w: 1000, h: 600, x: [0, 5], y: [0, 0.3], xt: [0, 1, 2, 3, 4, 5], yt: [0, 0.1, 0.2, 0.3], fx: (v) => v + '%', fy: (v) => v.toFixed(1) + 'σ', xl: 'Q / V (share of daily volume)', yl: 'impact', pad: { l: 100 } });
      const S = [], L = []; for (let i = 0; i <= 100; i++) { const x = i / 20; S.push([x, Math.sqrt(x / 100)]); }
      c.lin = c.line([[0, 0], [3, 0.3]], '#8ea3b1', 3); c.sq = c.line(S, '#ffb347', 6);
      c.lt = c.text(3.1, 0.29, 'linear (Kyle-like)', '#8ea3b1', 'start', 22); c.st = c.text(4.9, 0.255, 'Y σ √(Q/V), Y = 1', '#ffb347', 'end', 24); },
    draw(u, cue, H) { const c = MS.chart('sq-ch', {}); MS.reveal(c.sq, (u - cue(1)) / 1.5); MS.vis(c.st, H.C((u - cue(1) - 1.2) / 0.4));
      MS.reveal(c.lin, (u - cue(1) - 0.8) / 1); MS.vis(c.lt, H.C((u - cue(1) - 1.6) / 0.4)); }
  };
  SCENES['ac'] = {
    setup() { const c = MS.chart('ac-ch', { w: 1000, h: 600, x: [0, 1], y: [0, 1], xt: [0, 0.5, 1], yt: [0, 0.5, 1], fx: (v) => v === 1 ? 'T' : v === 0 ? '0' : 'T/2', fy: (v) => v === 1 ? 'X' : v === 0 ? '0' : 'X/2', xl: 'time', yl: 'shares still to buy', pad: { l: 90 } });
      const curve = (k) => { const P = []; for (let i = 0; i <= 60; i++) { const t = i / 60; P.push([t, k === 0 ? 1 - t : Math.sinh(k * (1 - t)) / Math.sinh(k)]); } return P; };
      c.a = c.line(curve(0), '#3fd0dc', 5); c.b = c.line(curve(3), '#ffb347', 5); c.c2 = c.line(curve(8), '#ff8fc8', 4);
      c.bt = c.text(0.2, 0.33, 'κT = 3', '#ffb347', 'start', 22); c.ct = c.text(0.08, 0.1, 'κT = 8', '#ff8fc8', 'start', 22); c.at = c.text(0.55, 0.5, 'κT = 0', '#3fd0dc', 'start', 22); },
    draw(u, cue, H) { const c = MS.chart('ac-ch', {}); MS.reveal(c.a, (u - cue(2)) / 1); MS.vis(c.at, H.C((u - cue(2) - 0.8) / 0.4));
      MS.reveal(c.b, (u - cue(3) - 0.3) / 1); MS.vis(c.bt, H.C((u - cue(3) - 1.1) / 0.4)); MS.reveal(c.c2, (u - cue(3) - 1.2) / 1); MS.vis(c.ct, H.C((u - cue(3) - 2) / 0.4)); }
  };
  SCENES['lab'] = {
    setup() { const c = MS.chart('lb-ch', { w: 520, h: 360, x: [0, 100], y: [0, 6], xt: [0, 50, 100], yt: [0, 3, 6], fx: (v) => v + 'k', fy: (v) => v + 'k', xl: 'market volume', yl: 'our shares', pad: { l: 70, b: 50 } });
      c.m = c.line([[0, 0], [100, 6]], '#ffb347', 3); const P = [[0, 0]]; let d = 0; for (let x = 0; x <= 100; x += 2) { const a = 0.06 * x; if (a - d >= 0.5) { P.push([x, d]); d = Math.floor(a * 2) / 2; } P.push([x, d]); }
      c.us = c.line(P, '#4fd18b', 5); c.t = c.text(60, 4.6, 'allowed = 6% × volume', '#ffb347', 'end', 20); },
    draw(u, cue, H) { const c = MS.chart('lb-ch', {}); MS.reveal(c.m, (u - cue(1)) / 1); MS.reveal(c.us, (u - cue(1) - 0.4) / 2); MS.vis(c.t, H.C((u - cue(1) - 2) / 0.4)); }
  };
})();
