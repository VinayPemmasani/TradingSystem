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
SCENES['title'] = {
  setup() { const r = STR.rng(4); const a = []; let p = 35; for (let i = 0; i <= 140; i++) { if (i === 40) p = 47.5; if (i > 40) p += 0.03 * (49.6 - p) / 2 + 0.12 * STR.gauss(r); else p += 0.3 * STR.gauss(r); a.push([i, p]); }
    const c = STR.chart('ti-c', { w: 1100, h: 340, x: [0, 140], y: [30, 53], pad: { l: 10, b: 10, t: 10, r: 10 } }); this.o = c.hline(50, '#ffb347'); this.l = c.line(a, '#3fd0dc', 4); },
  draw(u, cue, H) { STR.reveal(this.l, (u - cue(0) - 0.8) / 3); STR.vis(this.o, H.P(u, cue(1))); }
};
SCENES['example'] = {
  setup() { const c = STR.chart('ex-c', { w: 900, h: 560, x: [0, 3], y: [30, 54], yt: [35, 40, 45, 48, 50], fy: (v) => '$' + v, pad: { l: 90, b: 20, t: 16, r: 20 } });
    this.o = c.hline(50, '#4fd18b'); this.k = c.hline(35, '#ff8fc8'); this.n = c.hline(48, '#3fd0dc', '2 4');
    this.t = [c.text(3, 50.6, 'offer $50', '#4fd18b', 'end', 26), c.text(3, 35.6, 'break $35', '#ff8fc8', 'end', 26), c.text(3, 46.6, 'trades $48', '#3fd0dc', 'end', 26)]; },
  draw(u, cue, H) { STR.vis(this.n, H.P(u, cue(0))); STR.vis(this.t[2], H.P(u, cue(0))); STR.vis(this.o, H.P(u, cue(0) + 0.6)); STR.vis(this.t[0], H.P(u, cue(0) + 0.6)); STR.vis(this.k, H.P(u, cue(2))); STR.vis(this.t[1], H.P(u, cue(2))); }
};
SCENES['risk'] = {
  setup() { const r = STR.rng(12); const c = STR.chart('ri-c', { w: 800, h: 330, x: [0, 40], y: [-30, 8], pad: { l: 10, b: 10, t: 10, r: 10 } }); c.hline(0, '#8ea3b1', '2 6'); this.b = [];
    for (let i = 0; i < 40; i++) { const brk = i === 17 || i === 33; const v = brk ? -22 - 6 * r() : 2 + 3 * r(); this.b.push(STR.el('rect', { x: c.X(i + 0.15), y: c.Y(Math.max(v, 0)), width: c.X(0.7) - c.X(0), height: Math.abs(c.Y(v) - c.Y(0)), fill: brk ? '#ff8fc8' : '#4fd18b', rx: 3 }, c.svg)); }
    const p = STR.chart('ri-p', { w: 800, h: 430, x: [-30, 20], y: [-12, 6], xt: [-30, -20, -10, 0, 10, 20], fx: (v) => v + '%', yt: [-10, -5, 0, 5], fy: (v) => v + '%', xl: 'market return', yl: 'arb return (stylised)', pad: { l: 90, b: 50, t: 40, r: 20 } });
    p.hline(0, '#8ea3b1', '2 6'); p.vline(0, '#8ea3b1', '2 6'); this.p = p.line([[-30, -11], [-20, -7], [-10, -3], [-4, 1.5], [0, 1.5], [20, 1.5]], '#ffb347', 5); },
  draw(u, cue, H) { this.b.forEach((b, i) => STR.vis(b, H.P(u, cue(0) + 0.5 + i * 0.06, 0.2))); STR.reveal(this.p, (u - cue(4)) / 2); }
};
