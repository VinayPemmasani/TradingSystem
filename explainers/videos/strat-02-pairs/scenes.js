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
const PZ=[0.0, 1.0, -1.008, -0.697, 1.276, 1.092, 0.988, -0.717, 1.03, 0.799, -0.85, 0.739, 1.352, -0.239, 0.847, -0.323, 0.422, 1.116, 0.241, 0.684, 0.582, 0.767, 1.405, 0.702, 0.601, 1.407, 1.282, 0.388, 1.282, -0.18, 1.847, 1.674, 0.344, 0.16, 0.926, 0.433, 1.148, 1.669, 0.418, 1.997, 2.022, 1.402, 0.787, 0.877, 1.518, 0.991, 1.908, -0.003, -1.22, 0.301, 0.993, 1.037, 1.034, 0.642, 0.372, 1.436, 0.945, 0.807, 0.162, -1.195, -0.063, -0.308, -0.006, -0.192, -0.955, 0.939, -0.732, -1.38, 0.4, -0.344, 0.634, -0.234, -0.478, -1.061, 1.116, -0.236, -0.388, -0.719, -0.396, -0.598, -1.292, -0.804, -0.773, 0.353, 0.019, -1.148, -1.157, -1.159, -1.481, 0.562, 0.481, -0.74, 0.368, 1.445, 1.684, 1.754, 1.676, 0.796, 0.721, 1.88, -0.164, -0.725, -0.567, -0.613, -1.728, -0.146, -1.851, -0.75, -1.971, -2.114, -1.675, -1.645, -2.015, -1.847, -1.523, -1.762, -1.173, -2.046, -1.704, -1.54, -1.399, -2.443, -2.276, -2.031, -0.966, -1.275, -1.762, -1.76, -1.634, -1.176, -1.006, -1.279, -1.484, -1.386, -1.448, -1.373, -0.822, -1.046, -0.975, -1.145, -1.001, -0.595, -1.294, -0.743, -0.434, 0.188, 1.149, 0.861, 0.57, 0.084, 0.38, -0.269, -0.272, -0.391, 0.772, 1.108, -0.392, -0.006, -0.243, -0.501, 1.647, 1.153, 1.822, 0.072, 0.731, 0.59, -0.952, 1.855, 0.144, -0.318, -1.176, -1.438, -0.54, -0.49, 1.874, -1.281, -1.518, -1.009, -0.937, -1.443, -1.482, -1.224, -1.377, -0.872, -0.87, -2.489, -1.087, -1.748, -1.616, -1.517, -1.391, -1.29, -1.569, -1.733, -1.951, -1.971, -1.359, -1.93, -2.037, -2.311, -1.778, -1.74, -1.653, -2.021, -1.695, -1.855, -1.892, -1.73, -1.621, -1.535, -1.406, -1.257, -1.349, -1.439, -1.471, -1.107, -1.234, -1.43, -1.113, -1.319, -1.299, -0.663, -0.748, -0.765, -1.314, -1.247, -1.471, -1.087, -1.119, -0.983, -0.966, -1.139, -1.011, -0.816, -0.362, -1.254, -0.095, -0.323, -0.1, -0.911, -0.852, -0.995, -0.995, -0.939, -1.191, -1.016, 0.459, -0.259, -0.652, -0.891, 1.073, 0.119, -0.121, 2.231, 0.714, -0.461, -0.977, -0.86, 1.034, -1.635, -2.65, -1.649, -2.213, 0.134, -1.331, -1.99, -1.278, -1.634, 0.668, 1.538, -0.515, -1.789, -0.428, -2.017, -2.303, -1.94, -1.817, -0.929, -1.865, -1.609, -1.449, -1.687, -1.096, -1.324, -1.712, -0.927, 0.193, -1.806, -2.587, -1.645, -2.79, -1.796, -1.729, -1.645, -1.869, -0.909, -1.067, -2.07, -0.842, -1.568, -1.584, -1.207, -1.748, -0.668, -1.253, -1.252, -1.903, -1.48, -1.875, -1.644, -1.357, -0.868, -0.794, -0.921, -0.145, -2.053, -0.392, -1.366, -1.612, -1.198, 0.238, -0.433, 0.267, -0.902, -1.015, -0.618, -0.602, -1.508, -1.65, -1.151, -1.217, -1.147, -1.294, -0.341, -1.296, -0.479, -1.339, -1.722, -0.155, 0.74, 0.022, -1.218, -1.094, -1.258, -1.137, -1.639, -0.422, -1.228, -1.106, -0.632, 1.001, -0.17, 0.087, 2.16, 1.63, 2.912, -1.491, 0.376, 1.105, 0.223, 0.197, 3.171, 1.323, 2.887, 2.114, 1.845, 2.555, 2.235, 2.104, 2.602, 1.793, 0.699, 2.249, 2.639, 1.872, 1.461, 0.927, 0.233, -0.181, 1.068, -0.345, 1.113, 0.505, 1.296, 0.77, 0.304, -0.212, 1.016, 0.995, -0.727];const PEV=[[40, "in"], [47, "out"], [109, "in"], [145, "out"], [185, "in"], [236, "out"], [253, "in"], [255, "out"], [260, "in"], [263, "out"], [273, "in"], [286, "out"], [288, "in"], [314, "out"], [315, "in"], [320, "out"], [353, "in"], [356, "out"], [361, "in"], [377, "out"]];
function pairPaths(seed, n, gapFn) { const r = STR.rng(seed); let f = 1, g = 0; const a = [], b = [];
  for (let i = 0; i <= n; i++) { a.push([i, f * Math.exp(g / 2)]); b.push([i, f * Math.exp(-g / 2)]); f *= Math.exp(0.0015 + 0.01 * STR.gauss(r)); g = gapFn(i, g, r); } return [a, b]; }
SCENES['title'] = {
  setup() { const [a, b] = pairPaths(3, 120, (i, g, r) => 0.85 * g + 0.012 * STR.gauss(r) + (i > 50 && i < 60 ? 0.012 : 0));
    const c = STR.chart('ti-c', { w: 1000, h: 330, x: [0, 120], y: [0.8, 1.5], pad: { l: 10, b: 10, t: 10, r: 10 } });
    this.a = c.line(a, '#3fd0dc', 4); this.b = c.line(b, '#a98bff', 4); },
  draw(u, cue) { STR.reveal(this.a, (u - cue(0) - 0.8) / 3); STR.reveal(this.b, (u - cue(0) - 0.8) / 3); }
};
SCENES['form'] = {
  setup() { const [a, b] = pairPaths(11, 250, (i, g, r) => 0.95 * g + 0.012 * STR.gauss(r));
    const c = STR.chart('fo-c', { w: 1240, h: 470, x: [0, 250], y: [0.7, 1.9], yt: [0.8, 1.0, 1.2, 1.4, 1.6, 1.8], fy: (v) => v.toFixed(1), xt: [0, 63, 125, 188, 250], fx: (v) => Math.round(v / 250 * 12) + 'm' });
    this.v = []; for (let i = 5; i < 250; i += 10) { const l = STR.el('line', { x1: c.X(i), x2: c.X(i), y1: c.Y(a[i][1]), y2: c.Y(b[i][1]), stroke: '#ffb347', 'stroke-width': 3 }, c.svg); this.v.push(l); }
    this.a = c.line(a, '#3fd0dc', 4); this.b = c.line(b, '#a98bff', 4); },
  draw(u, cue, H) { STR.reveal(this.a, (u - cue(2)) / 2.5); STR.reveal(this.b, (u - cue(2)) / 2.5); this.v.forEach((l, k) => STR.vis(l, H.P(u, cue(3) + k * 0.06, 0.3))); }
};
SCENES['trade'] = {
  setup() { const r = STR.rng(5); let g = 0; const s = [];
    for (let i = 0; i <= 125; i++) { s.push([i, g]); g = 0.93 * g + 0.45 * STR.gauss(r) + (i > 20 && i < 32 ? 0.5 : 0) - (i > 70 && i < 80 ? 0.55 : 0); }
    const c = STR.chart('tr-c', { w: 1300, h: 560, x: [0, 125], y: [-5, 5], yt: [-4, -2, 0, 2, 4], xt: [0, 21, 42, 63, 84, 105, 125], fx: (v) => Math.round(v / 21) + 'm', yl: 'gap, in formation σ' });
    c.hline(2, '#ffb347'); c.hline(-2, '#ffb347'); c.hline(0, '#3fd0dc', '2 6');
    this.l = c.line(s, '#eef4f7', 3);
    let open = 0; this.ev = [];
    for (const [i, v] of s) { if (!open && Math.abs(v) > 2) { open = Math.sign(v); this.ev.push([i, c.dot(i, v, 11, '#ffb347')]); } else if (open && Math.sign(v) !== open) { open = 0; this.ev.push([i, c.dot(i, v, 11, '#3fd0dc')]); } }
    this.n = 125; },
  draw(u, cue, H) { const p = (u - cue(1)) / 6; STR.reveal(this.l, p); STR.vis(this.l, H.P(u, cue(0)));
    this.ev.forEach(([i, d]) => STR.vis(d, p * this.n >= i ? 1 : 0)); }
};
SCENES['lose'] = {
  setup() { const r = STR.rng(9); let g = 0, h = 0; const s = [], t = [];
    for (let i = 0; i <= 100; i++) { s.push([i, g]); t.push([i, h]); g = i < 30 ? g + 0.08 + 0.1 * STR.gauss(r) : 0.9 * g + 0.15 * STR.gauss(r); h = i < 30 ? g : h + 0.07 + 0.12 * STR.gauss(r); }
    const c = STR.chart('lo-c', { w: 1200, h: 560, x: [0, 100], y: [-2, 8], yt: [0, 2, 4, 6, 8], yl: 'gap, σ' }); c.hline(2, '#ffb347');
    this.g = c.line(s, '#4fd18b', 4); this.h = c.line(t.slice(29), '#ff8fc8', 5); },
  draw(u, cue) { STR.reveal(this.g, (u - cue(0)) / 3); STR.reveal(this.h, (u - cue(2)) / 3); }
};
SCENES['lab'] = {
  setup() { const c = STR.chart('lb-c', { w: 730, h: 380, x: [0, 389], y: [-4, 4], yt: [-4, -2, 0, 2, 4], xt: [0, 120, 240, 360], fx: (v) => ['9:30', '11:30', '13:30', '15:30'][v / 120], pad: { l: 50, b: 40, t: 10, r: 10 } });
    c.hline(2, '#ffb347'); c.hline(-2, '#ffb347');
    this.l = c.line(PZ.map((v, i) => [i, v]), '#eef4f7', 2);
    this.d = PEV.map(([i, k]) => [i, c.dot(i, PZ[i], 7, k === 'in' ? '#ffb347' : '#3fd0dc')]); },
  draw(u, cue) { const p = (u - cue(4)) / 3; STR.reveal(this.l, p); this.d.forEach(([i, d]) => STR.vis(d, p * 389 >= i ? 1 : 0)); }
};
