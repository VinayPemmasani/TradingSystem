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
SCENES['example'] = {
  setup() { const c = STR.chart('ex-c', { w: 1680, h: 170, x: [-12, 8], y: [-10, 13], xt: [-12, -8, -4, 0, 4, 8], fx: (v) => (v > 0 ? '+' : '') + v + '%', pad: { l: 20, b: 40, t: 10, r: 20 } });
    c.hline(0, '#8ea3b1', '2 6'); c.vline(-3.81, '#ff8fc8'); const f = (x) => ((1 + x / 100) * 1.05 / 1.01 - 1) * 100; this.l = c.line([[-12, f(-12)], [8, f(8)]], '#ffb347', 4); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(3)) / 1.5); }
};
SCENES['lose'] = {
  setup() { const r = STR.rng(15); const a = []; let p = 0; for (let i = 0; i <= 200; i++) { a.push([i, p]); p += 0.12 + 0.25 * STR.gauss(r) - (i > 150 && i < 158 ? 2.6 : 0); }
    const c = STR.chart('lo-c', { w: 1000, h: 440, x: [0, 200], y: [-5, 22], pad: { l: 10, b: 10, t: 10, r: 10 } }); c.hline(0, '#8ea3b1', '2 6'); this.l = c.line(a, '#ffb347', 4); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(0)) / 5); }
};
