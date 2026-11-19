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
const MM_PNL=[-122, -1004, -1860, -2630, -3350, -3995, -4457, -4802, -5001, -5293, -5663, -5946, -6212, -6558, -6879, -7032, -7215, -7349, -7466, -7567, -7715, -7845, -8006, -8184, -8369, -8470, -8545, -8626, -8727, -8891, -9023, -9229, -9370, -9513, -9675, -9696, -9822, -9938, -9995, -10065, -10228, -10389, -10514, -10643, -10735, -10794, -10878, -10911, -10979, -11049, -11121, -11207, -11258, -11344, -11386, -11431, -11481, -11588, -11733, -11775, -11833, -11944, -12024, -12112, -12179, -12216, -12284, -12376, -12397, -12478, -12575, -12636, -12673, -12736, -12784, -12870, -12903, -13022, -13171, -13231, -13275, -13338, -13356, -13417, -13460, -13539, -13608, -13690, -13730, -13792, -14203, -14538, -14784, -14996, -15212, -15506, -15731, -15896, -16091, -16204, -16347, -16520, -16728, -16893, -16992, -17070, -17215, -17303, -17433, -17654, -17813, -17919, -18104, -18241, -18375, -18455, -18540, -18730, -18918, -19025, -19214, -19381, -19559, -19691, -19787, -19965, -20048, -20123, -20228, -20322, -20316];
SCENES['lose'] = {
  setup() {
    const r = STR.rng(7); let p = 100, a = [], b = [];
    for (let i = 0; i <= 60; i++) { a.push([i, p]); p += (i > 8 ? -0.012 : 0) + 0.018 * STR.gauss(r); }
    p = 100; for (let i = 0; i <= 60; i++) { b.push([i, p]); p += 0.01 * STR.gauss(r); if (i === 40) p -= 0.25; }
    const c1 = STR.chart('lo-c1', { w: 800, h: 430, x: [0, 60], y: [99.5, 100.2], yt: [99.6, 99.8, 100, 100.2], fy: (v) => v.toFixed(1), xl: 'time →' });
    this.l1 = c1.line(a, '#3fd0dc', 4); this.d1 = c1.dot(8, a[8][1], 10, '#4fd18b');
    this.z1 = c1.rect(8, 60, a[8][1], 99.55, '#ff8fc8', 0.12);
    const c2 = STR.chart('lo-c2', { w: 800, h: 430, x: [0, 60], y: [99.5, 100.2], yt: [99.6, 99.8, 100, 100.2], fy: (v) => v.toFixed(1), xl: 'time →' });
    this.l2 = c2.line(b, '#3fd0dc', 4); this.ds = [32, 35, 37, 39].map((i) => c2.dot(i, b[i][1], 9, '#a98bff'));
  },
  draw(u, cue, H) {
    STR.reveal(this.l1, (u - cue(1)) / 3); STR.vis(this.d1, H.P(u, cue(1) + 0.6)); STR.vis(this.z1, H.P(u, cue(1) + 1.6));
    STR.reveal(this.l2, (u - cue(2)) / 4); this.ds.forEach((d, k) => STR.vis(d, H.P(u, cue(3) + k * 0.3)));
  }
};
SCENES['as'] = {
  setup() {
    const t = document.getElementById('as-ticks');
    for (let v = 98; v <= 101; v += 0.5) { const e = document.createElement('div'); e.className = 'lbl';
      e.style.cssText = `position:absolute;left:${210 + (v - 97.5) * 375 - 30}px;top:715px;width:60px;text-align:center`; e.textContent = v.toFixed(1); t.appendChild(e); }
  },
  draw(u, cue, H) {
    const X = (v) => 210 + (v - 97.5) * 375;
    const k = H.P(u, cue(3), 1.2); const r = 100 - 0.8 * k;
    const sp = 1.69 * H.P(u, cue(4), 1.0);
    const m = H.$('as-mid'); m.style.left = (X(100) - 70) + 'px'; STR.vis(m, H.P(u, cue(0)));
    const rl = H.$('as-rl'); rl.style.left = (X(r) - 2) + 'px'; STR.vis(rl, H.P(u, cue(1)));
    const rt = H.$('as-r'); rt.style.left = (X(r) - 20) + 'px'; STR.vis(rt, H.P(u, cue(1)));
    H.text(rt, u >= cue(7) ? 'r = 99.2' : 'r');
    const bar = H.$('as-bar'); bar.style.left = X(r - sp / 2) + 'px'; bar.style.width = Math.max(0, X(r + sp / 2) - X(r - sp / 2)) + 'px'; STR.vis(bar, H.P(u, cue(4)));
    const b = H.$('as-b'), a = H.$('as-a');
    b.style.left = (X(r - sp / 2) - 40) + 'px'; a.style.left = (X(r + sp / 2) - 40) + 'px';
    STR.vis(b, H.P(u, cue(4) + 0.6)); STR.vis(a, H.P(u, cue(4) + 0.6));
  }
};
SCENES['lab'] = {
  setup() {
    const n = MM_PNL.length;
    const c = STR.chart('lb-c', { w: 580, h: 300, x: [0, n - 1], y: [-22000, 0], yt: [0, -10000, -20000], fy: (v) => (v / 1000) + 'k', pad: { l: 70, b: 20, t: 10, r: 10 } });
    this.l = c.line(MM_PNL.map((v, i) => [i, v]), '#ff8fc8', 4);
  },
  draw(u, cue) { STR.reveal(this.l, (u - cue(4) - 0.3) / 2.5); }
};
