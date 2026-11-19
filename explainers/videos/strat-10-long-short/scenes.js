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
SCENES['factors'] = {
  setup() { const h = document.getElementById('fa-g'); const lab = [['SG', 'SN', 'SV'], ['BG', 'BN', 'BV']]; this.c = [];
    for (let r = 0; r < 2; r++) for (let k = 0; k < 3; k++) { const d = document.createElement('div'); d.className = 'node'; d.style.cssText = `position:absolute;left:${k * 380}px;top:${r * 160}px;width:340px;height:120px`; d.innerHTML = `<div class="t">${lab[r][k]}</div>`; h.appendChild(d); this.c.push([d, r, k]); } },
  draw(u, cue, H) { this.c.forEach(([d, r, k], i) => { STR.vis(d, H.P(u, cue(3) + i * 0.1, 0.3));
    let col = 'var(--line)'; if (u >= cue(4) && u < cue(5)) col = r === 0 ? 'var(--green)' : 'var(--red)'; else if (u >= cue(5) && u < cue(6)) col = k === 2 ? 'var(--green)' : (k === 0 ? 'var(--red)' : 'var(--line)'); d.style.borderColor = col; }); }
};
SCENES['lose'] = {
  setup() { const r = STR.rng(23); const a = []; let p = 20; for (let i = 0; i <= 100; i++) { a.push([i, p]); p *= Math.exp((i > 60 && i < 75 ? 0.07 : -0.002) + 0.02 * STR.gauss(r)); }
    const c = STR.chart('lo-c', { w: 800, h: 380, x: [0, 100], y: [10, 60], pad: { l: 10, b: 10, t: 10, r: 10 } }); this.l = c.line(a, '#ff6b5e', 4); },
  draw(u, cue) { STR.reveal(this.l, (u - cue(1)) / 2.5); }
};
SCENES['lab'] = {
  setup() { const h = document.getElementById('lb-g'); this.t = []; const r = STR.rng(2);
    for (let i = 0; i < 60; i++) { const d = document.createElement('div'); const lg = r() < 0.6; d.style.cssText = `position:absolute;left:${(i % 15) * 60}px;top:${Math.floor(i / 15) * 72}px;width:48px;height:56px;border-radius:8px;border:2px solid ${lg ? 'var(--green)' : 'var(--red)'};background:${lg ? 'rgba(79,209,139,.25)' : 'rgba(255,107,94,.25)'}`; h.appendChild(d); this.t.push(d); } },
  draw(u, cue, H) { this.t.forEach((d, k) => STR.vis(d, H.P(u, cue(2) + k * 0.02, 0.3))); }
};
