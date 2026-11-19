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
const CORR = [['1 ms', 0.0073], ['10 ms', 0.0923], ['100 ms', 0.4622], ['1 s', 0.6879], ['10 s', 0.9057], ['1 min', 0.9798]];
SCENES['corr'] = {
  setup() { const h = document.getElementById('co-rows'); this.rows = [];
    CORR.forEach(([k, v], i) => { const top = i * 88;
      const l = document.createElement('div'); l.className = 'lbl'; l.style.cssText = `position:absolute;left:0;top:${top + 14}px;width:140px`; l.textContent = k; h.appendChild(l);
      const b = document.createElement('div'); b.className = 'bar'; b.style.cssText = `left:160px;top:${top}px;height:56px;width:0;background:${v < 0.2 ? 'var(--pink)' : 'var(--teal)'}`; h.appendChild(b);
      const t = document.createElement('div'); t.className = 'tag'; t.style.cssText = `top:${top + 10}px`; t.textContent = v.toFixed(v < 0.1 ? 4 : 2); h.appendChild(t);
      this.rows.push([b, t, v]); }); },
  draw(u, cue, H) { this.rows.forEach(([b, t, v], i) => { const at = i === 5 ? cue(1) : (i < 2 ? cue(2) : cue(1) + 0.4 + (4 - i) * 0.3);
    const p = H.P(u, at, 0.9); b.style.width = (v * 1000 * p) + 'px'; t.style.left = (175 + v * 1000 * p) + 'px'; STR.vis(t, H.P(u, at + 0.6)); });
    this.rows.forEach(([b], i) => b.classList.toggle('hl', i < 2 && u >= cue(3))); }
};
SCENES['lose'] = {
  setup() { const h = document.getElementById('lo-ba'); this.o = [];
    for (let k = 0; k <= 4; k++) { const l = document.createElement('div'); l.style.cssText = `position:absolute;left:${k * 190}px;top:0;width:3px;height:380px;background:var(--teal);opacity:.6`; h.appendChild(l);
      const t = document.createElement('div'); t.className = 'lbl'; t.style.cssText = `position:absolute;left:${k * 190 - 30}px;top:390px`; t.textContent = (k * 100) + 'ms'; h.appendChild(t); }
    const r = STR.rng(8); for (let i = 0; i < 22; i++) { const d = document.createElement('div'); const x = r() * 740 + 10, y = 20 + r() * 330;
      d.style.cssText = `position:absolute;width:20px;height:20px;border-radius:50%;left:${x}px;top:${y}px;background:${r() < 0.5 ? 'var(--green)' : 'var(--red)'}`; h.appendChild(d); this.o.push([d, x]); } },
  draw(u, cue, H) { const s = (u - cue(4)) * 300; this.o.forEach(([d, x]) => { STR.vis(d, s > x ? 1 : 0); d.style.transform = s > Math.ceil((x + 1) / 190) * 190 ? 'scale(0.6)' : 'none'; }); }
};
