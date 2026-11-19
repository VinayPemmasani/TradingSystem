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
function tiles(id, n, cols, size, gap) { const h = document.getElementById(id); if (h._t) return h._t; const out = [];
  for (let i = 0; i < n; i++) { const d = document.createElement('div'); d.style.cssText = `position:absolute;left:${(i % cols) * (size + gap)}px;top:${Math.floor(i / cols) * (size + gap)}px;width:${size}px;height:${size}px;border-radius:10px;border:2px solid var(--violet);background:rgba(169,139,255,.15)`; h.appendChild(d); out.push(d); }
  h._t = out; return out; }
SCENES['title'] = { setup() { this.t = tiles('ti-bk', 12, 6, 70, 16); }, draw(u, cue, H) { this.t.forEach((d, k) => STR.vis(d, H.P(u, cue(1) + k * 0.06, 0.3))); } };
SCENES['nav'] = {
  setup() { const r = STR.rng(21); const a = []; let p = 0; for (let i = 0; i <= 200; i++) { a.push([i, p]); p = 0.9 * p + 0.06 * STR.gauss(r) + (i > 120 && i < 128 ? 0.04 : 0) - (i > 160 && i < 168 ? 0.06 : 0); }
    const c = STR.chart('nv-c1', { w: 1520, h: 250, x: [0, 200], y: [-0.6, 0.6], yt: [-0.4, 0, 0.4], fy: (v) => (v > 0 ? '+' : '') + v.toFixed(1) + '%', pad: { l: 90, b: 20, t: 10, r: 10 } });
    c.hline(0, '#a98bff'); this.l = c.line(a, '#3fd0dc', 3); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(1)) / 4); }
};
SCENES['fast'] = { setup() { this.t = tiles('fa-g', 20, 5, 86, 18); },
  draw(u, cue, H) { this.t.forEach((d, k) => { const on = u > cue(0) ? (Math.floor(u * 3 + k * 1.7) % 7 === 0) : false; d.style.background = on ? 'rgba(169,139,255,.65)' : 'rgba(169,139,255,.15)'; STR.vis(d, H.P(u, cue(0) + k * 0.03, 0.3)); }); } };
SCENES['futures'] = {
  setup() { const c = STR.chart('fu-c', { w: 600, h: 200, x: [0, 78], y: [-0.1, 0.45], pad: { l: 20, b: 20, t: 10, r: 10 } });
    const r = STR.rng(4); const a = []; for (let i = 0; i <= 78; i++) a.push([i, 0.32 * (1 - i / 78) + (i < 78 ? 0.03 * STR.gauss(r) * Math.sqrt(1 - i / 78) : 0)]);
    c.hline(0, '#ffb347'); this.l = c.line(a, '#6aa8ff', 4); c.text(78, 0.05, 'expiry', '#8ea3b1', 'end'); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(5)) / 3); }
};
SCENES['lose'] = { setup() { this.t = tiles('lo-g', 24, 6, 110, 16); },
  draw(u, cue, H) { this.t.forEach((d, k) => { const filled = (k * 7) % 10 < 6; const p = H.P(u, cue(1) + 0.2 + k * 0.05, 0.3);
    d.style.background = p > 0.5 ? (filled ? 'rgba(79,209,139,.6)' : 'rgba(255,143,200,.25)') : 'rgba(169,139,255,.15)'; d.style.borderColor = p > 0.5 ? (filled ? 'var(--green)' : 'var(--pink)') : 'var(--violet)'; STR.vis(d, H.P(u, cue(0) + k * 0.02, 0.3)); }); } };
