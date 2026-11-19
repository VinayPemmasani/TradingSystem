// ---- shared helpers for the strategy series (strat-01..10) ----
window.STR = (function () {
  const NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  // seeded random for illustrative series
  function rng(seed) { let a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function gauss(r) { let u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
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
    if (o.xl) { const t = el('text', { x: W - pad.r, y: Hh - pad.b + 66, 'text-anchor': 'end' }, svg); t.textContent = o.xl; }
    if (o.yl) { const t = el('text', { x: pad.l, y: pad.t - 14 }, svg); t.textContent = o.yl; }
    const c = { svg, X, Y,
      line(pts, color, width) { const d = pts.map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join(' ');
        const p = el('path', { d, fill: 'none', stroke: color, 'stroke-width': width || 4, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', pathLength: 1 }, svg);
        p.style.strokeDasharray = '1 1'; p.style.strokeDashoffset = '1'; return p; },
      dot(x, y, r, color) { return el('circle', { cx: X(x), cy: Y(y), r: r || 7, fill: color }, svg); },
      rect(x0, x1, y0, y1, color, op) { return el('rect', { x: X(x0), y: Y(Math.max(y0, y1)), width: X(x1) - X(x0), height: Math.abs(Y(y0) - Y(y1)), fill: color, 'fill-opacity': op || 0.15 }, svg); },
      text(x, y, s, color, anchor, size) { const t = el('text', { x: X(x), y: Y(y), 'text-anchor': anchor || 'start', style: 'fill:' + (color || '#8ea3b1') + (size ? ';font-size:' + size + 'px' : '') }, svg); t.textContent = s; return t; },
      hline(y, color, dash) { return el('line', { x1: pad.l, x2: W - pad.r, y1: Y(y), y2: Y(y), stroke: color, 'stroke-width': 2, 'stroke-dasharray': dash || '8 8' }, svg); },
      vline(x, color, dash) { return el('line', { x1: X(x), x2: X(x), y1: pad.t, y2: Hh - pad.b, stroke: color, 'stroke-width': 2, 'stroke-dasharray': dash || '8 8' }, svg); } };
    host._chart = c; return c;
  }
  function reveal(path, p) { if (path) path.style.strokeDashoffset = String(1 - Math.max(0, Math.min(1, p))); }
  function vis(e, p) { if (e) e.style.opacity = Math.max(0, Math.min(1, p)); }
  return { el, rng, gauss, chart, reveal, vis };
})();
function Ncdf(x) { const t = 1 / (1 + 0.2316419 * Math.abs(x)); const d = 0.3989423 * Math.exp(-x * x / 2); const p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return x > 0 ? 1 - p : p; }
function bs(S, K, T, s) { const d1 = (Math.log(S / K) + 0.5 * s * s * T) / (s * Math.sqrt(T)); return { c: S * Ncdf(d1) - K * Ncdf(d1 - s * Math.sqrt(T)), d: Ncdf(d1) }; }
SCENES['title'] = { setup() { const h = document.getElementById('ti-g'); this.t = [];
    for (let i = 0; i < 40; i++) { const d = document.createElement('div'); d.style.cssText = `position:absolute;left:${(i % 10) * 90}px;top:${Math.floor(i / 10) * 82}px;width:78px;height:68px;border-radius:8px;border:2px solid var(--teal);background:rgba(63,208,220,.12)`; h.appendChild(d); this.t.push(d); } },
  draw(u, cue, H) { this.t.forEach((d, k) => { STR.vis(d, H.P(u, cue(0) + 0.8 + k * 0.02, 0.3)); d.style.background = (Math.floor(u * 4 + k * 2.3) % 9 === 0) ? 'rgba(63,208,220,.5)' : 'rgba(63,208,220,.12)'; }); } };
SCENES['delta'] = {
  setup() { const T = 30 / 365, s = 0.2; const c = STR.chart('de-c', { w: 1000, h: 560, x: [85, 115], y: [0, 16], yt: [0, 5, 10, 15], xt: [85, 90, 95, 100, 105, 110, 115], xl: 'stock price', yl: 'call value' });
    const pts = []; for (let S = 85; S <= 115; S += 0.25) pts.push([S, bs(S, 100, T, s).c]); this.curve = c.line(pts, '#3fd0dc', 4); this.c = c;
    this.tan = STR.el('line', { stroke: '#ffb347', 'stroke-width': 4 }, c.svg); this.pt = STR.el('circle', { r: 10, fill: '#ffb347' }, c.svg); this.T = T; this.s = s; },
  draw(u, cue, H) { STR.reveal(this.curve, (u - cue(0) - 0.5) / 1.5); const c = this.c; const S = u < cue(4) ? 100 : 100 + 8 * Math.sin(Math.min(1, (u - cue(4)) / 3) * Math.PI / 2) * (u > cue(5) ? Math.cos((u - cue(5)) * 1.5) : 1);
    const b = bs(S, 100, this.T, this.s); const x0 = S - 6, x1 = S + 6; this.tan.setAttribute('x1', c.X(x0)); this.tan.setAttribute('x2', c.X(x1)); this.tan.setAttribute('y1', c.Y(b.c - 6 * b.d)); this.tan.setAttribute('y2', c.Y(b.c + 6 * b.d));
    this.pt.setAttribute('cx', c.X(S)); this.pt.setAttribute('cy', c.Y(b.c)); const v = H.P(u, cue(1) + 0.5); STR.vis(this.tan, v); STR.vis(this.pt, v); }
};
function path(seed, vol) { const r = STR.rng(seed); const a = []; let p = 100; for (let i = 0; i <= 80; i++) { a.push([i, p]); p += vol * STR.gauss(r) + 0.12 * (100 - p); } return a; }
SCENES['pnl'] = {
  setup() { const ca = STR.chart('pn-a', { w: 800, h: 260, x: [0, 80], y: [85, 115], pad: { l: 10, b: 10, t: 10, r: 10 } }); this.a = ca.line(path(3, 1.6), '#4fd18b', 3);
    const cb = STR.chart('pn-b', { w: 800, h: 260, x: [0, 80], y: [85, 115], pad: { l: 10, b: 10, t: 10, r: 10 } }); this.b = cb.line(path(4, 0.35), '#ff6b5e', 3); },
  draw(u, cue) { STR.reveal(this.a, (u - cue(1)) / 2.5); STR.reveal(this.b, (u - cue(2)) / 2.5); }
};
SCENES['example'] = {
  setup() { const G = 0.06955, th = 0.05520; const c = STR.chart('ex-c', { w: 940, h: 540, x: [0, 3], y: [-0.08, 0.26], yt: [-0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25], fy: (v) => (v * 100).toFixed(0) + '¢', xt: [0, 0.5, 1, 1.26, 2, 3], fx: (v) => '$' + v, pad: { l: 90, b: 50, t: 16, r: 20 } });
    c.hline(0, '#8ea3b1', '4 6'); const p = []; for (let m = 0; m <= 3; m += 0.05) p.push([m, 0.5 * G * m * m - th]); this.l = c.line(p, '#ffb347', 4);
    this.d = [[1.26, 0, '#3fd0dc', 'breakeven $1.26'], [2, 0.5 * G * 4 - th, '#4fd18b', '+8¢ on a $2 day'], [0.5, 0.5 * G * 0.25 - th, '#ff8fc8', '−5¢ on a 50¢ day']].map(([x, y, col, s]) => { const g = STR.el('g', {}, c.svg); STR.el('circle', { cx: c.X(x), cy: c.Y(y), r: 10, fill: col }, g); const t = STR.el('text', { x: c.X(x) + 16, y: c.Y(y) - 14, style: 'fill:' + col + ';font-size:24px' }, g); t.textContent = s; return g; }); },
  draw(u, cue, H) { STR.reveal(this.l, (u - cue(2)) / 2); STR.vis(this.d[0], H.P(u, cue(2) + 1.5)); STR.vis(this.d[1], H.P(u, cue(3))); STR.vis(this.d[2], H.P(u, cue(4))); }
};
SCENES['lose'] = {
  setup() { const r = STR.rng(5); const a = []; let p = 100; for (let i = 0; i <= 80; i++) { a.push([i, p]); p += 0.4 * STR.gauss(r) + (i === 50 ? -12 : 0); }
    const c = STR.chart('lo-c', { w: 820, h: 420, x: [0, 80], y: [80, 106], pad: { l: 10, b: 10, t: 10, r: 10 } }); this.l = c.line(a, '#3fd0dc', 4); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(0) - 0.3) / 2); }
};
