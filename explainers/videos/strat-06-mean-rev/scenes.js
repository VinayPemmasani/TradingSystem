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
function relBars(id, w, h, n, seed) { const r = STR.rng(seed); const v = []; for (let i = 0; i < n; i++) v.push(STR.gauss(r) * 2); const m = v.reduce((a, b) => a + b, 0) / n; const x = v.map((a) => a - m);
  const c = STR.chart(id, { w, h, x: [0, n], y: [-5, 5], pad: { l: 10, b: 10, t: 10, r: 10 } }); c.hline(0, '#8ea3b1', '2 6');
  const bars = x.map((a, i) => [c.bar ? null : STR.el('rect', { x: c.X(i + 0.15), y: c.Y(Math.max(a, 0)), width: c.X(0.7) - c.X(0), height: Math.abs(c.Y(a) - c.Y(0)), fill: 'none', stroke: '#3fd0dc', 'stroke-width': 3, rx: 4 }, c.svg), a]);
  return bars.map(([b, a]) => [b, a]); }
function drawRel(bars, u, t0, t1, H) { bars.forEach(([b, a], i) => { STR.vis(b, H.P(u, t0 + i * 0.04, 0.3)); const on = u > t1 + i * 0.05; b.setAttribute('fill', on ? (a > 0 ? 'rgba(255,107,94,.6)' : 'rgba(79,209,139,.6)') : 'none'); b.setAttribute('stroke', on ? (a > 0 ? '#ff6b5e' : '#4fd18b') : '#3fd0dc'); }); }
SCENES['title'] = { setup() { this.b = relBars('ti-b', 1100, 330, 24, 3); }, draw(u, cue, H) { drawRel(this.b, u, cue(1), cue(1) + 1.5, H); } };
SCENES['rule'] = { setup() { this.b = relBars('ru-c', 1680, 360, 30, 9); }, draw(u, cue, H) { drawRel(this.b, u, cue(2), cue(2) + 1.8, H); } };
SCENES['edge'] = {
  setup() { const r = STR.rng(17); const a = []; let p = 100; for (let i = 0; i <= 120; i++) { a.push([i, p]); const pull = i > 40 && i < 52 ? -0.5 : 0; p += pull + (i > 52 ? 0.12 * (100 - p) : 0) + 0.15 * STR.gauss(r); }
    const c = STR.chart('ed-c', { w: 900, h: 480, x: [0, 120], y: [92, 103], pad: { l: 10, b: 10, t: 10, r: 10 } }); c.hline(100, '#8ea3b1', '4 6');
    this.l = c.line(a, '#3fd0dc', 4); this.d = c.dot(52, a[52][1], 11, '#4fd18b'); },
  draw(u, cue, H) { STR.reveal(this.l, (u - cue(1)) / 3); STR.vis(this.d, H.P(u, cue(1) + 1.4)); }
};
SCENES['aug'] = {
  setup() { const v = [['Aug 7', -1.16], ['Aug 8', -2.83], ['Aug 9', -2.86], ['Aug 10', 5.92]];
    const c = STR.chart('au-c', { w: 1000, h: 520, x: [0, 4], y: [-4, 7], yt: [-4, -2, 0, 2, 4, 6], fy: (x) => (x > 0 ? '+' : '') + x + '%', xt: [0.5, 1.5, 2.5, 3.5], fx: (x) => v[Math.floor(x)][0] });
    c.hline(0, '#8ea3b1', '2 6');
    this.b = v.map(([k, x], i) => { const g = STR.el('g', {}, c.svg); STR.el('rect', { x: c.X(i + 0.2), y: c.Y(Math.max(x, 0)), width: c.X(0.6) - c.X(0), height: Math.abs(c.Y(x) - c.Y(0)), fill: x < 0 ? '#ff8fc8' : '#4fd18b', rx: 6 }, g);
      const t = STR.el('text', { x: c.X(i + 0.5), y: x < 0 ? c.Y(x) + 30 : c.Y(x) - 12, 'text-anchor': 'middle', style: 'font-size:26px;fill:#eef4f7' }, g); t.textContent = (x > 0 ? '+' : '') + x.toFixed(2) + '%'; return g; }); },
  draw(u, cue, H) { this.b.forEach((g, i) => STR.vis(g, H.P(u, i < 3 ? cue(1) + 0.8 + i * 1.0 : cue(2)))); }
};
