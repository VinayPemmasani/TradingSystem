// ---- shared helpers for the signal-generation series (sig-01..10) ----
window.SIG = (function () {
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

// ---- sig-10 combine ----
(function () {
  let s = 21; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const g = () => { let a = 0; for (let i = 0; i < 6; i++) a += rnd(); return (a - 3) * Math.SQRT2; };
  const PTS = []; for (let i = 0; i < 160; i++) { const a = g(), b = 0.9 * a + Math.sqrt(1 - 0.81) * g(); PTS.push([a, b]); }
  SCENES['ridge'] = {
    setup() { const c = SIG.chart('rg-ch', { w: 780, h: 560, x: [-3, 3], y: [-3, 3], xt: [-2, 0, 2], yt: [-2, 0, 2], xl: 'microprice − mid (sd)', yl: 'imbalance ρ (sd)' });
      c.d = PTS.map(([a, b]) => c.dot(a, b, 5, '#a98bff')); c.t = c.text(-2.8, 2.5, 'corr 0.9', '#a98bff', 'start', 24); },
    draw(u, cue, H) { const c = SIG.chart('rg-ch', {}); c.d.forEach((d, i) => SIG.vis(d, H.C((u - cue(1) - i * 0.01) / 0.3))); SIG.vis(c.t, H.C((u - cue(1) - 1.5) / 0.4)); }
  };
  const W = { tr: [0.5, 0.0, 0.3], ols: [-0.292, 0.707, 0.422], rg: [0.105, 0.211, 0.204] };
  SCENES['worked'] = {
    setup() { const c = SIG.chart('wk-ch', { w: 1100, h: 600, x: [-0.6, 2.6], y: [-0.4, 0.8], yt: [-0.2, 0, 0.2, 0.4, 0.6, 0.8], fy: (v) => v.toFixed(1), yl: 'weight' });
      c.z = c.hline(0, '#5b6f7c', '4 6');
      ['microprice', 'imbalance', 'trade flow'].forEach((n, j) => c.text(j, -0.36, n, '#8ea3b1', 'middle', 22));
      const mk = (key, off, col) => W[key].map((v, j) => [c.bar(j + off, 0, v, 70, col), c.text(j + off, v >= 0 ? v + 0.03 : v / 2 - 0.02, (v > 0 ? '+' : '') + (Math.round(v * 100) / 100).toFixed(2), v >= 0 ? col : '#0b1218', 'middle', 20)]);
      c.tr = mk('tr', -0.27, '#4fd18b'); c.ols = mk('ols', 0, '#8ea3b1'); c.rg = mk('rg', 0.27, '#ffb347');
      c.lg = [c.text(1.6, 0.76, '■ true', '#4fd18b', 'start', 22), c.text(1.6, 0.68, '■ least squares', '#8ea3b1', 'start', 22), c.text(1.6, 0.60, '■ ridge, λ = 250', '#ffb347', 'start', 22)]; },
    draw(u, cue, H) { const c = SIG.chart('wk-ch', {}); const sh = (arr, t) => arr.forEach((p) => p.forEach((e) => SIG.vis(e, H.C((u - t) / 0.4))));
      sh(c.tr, cue(0) + 1.2); sh(c.ols, cue(1) + 0.3); sh(c.rg, cue(2) + 0.3);
      SIG.vis(c.lg[0], H.C((u - cue(0) - 1.2) / 0.4)); SIG.vis(c.lg[1], H.C((u - cue(1) - 0.3) / 0.4)); SIG.vis(c.lg[2], H.C((u - cue(2) - 0.3) / 0.4)); }
  };
  SCENES['online'] = {
    setup() { const t = H.$('on-tl'); if (t.children.length) return;
      t.innerHTML = '<div style="position:absolute;left:0;top:110px;width:1700px;height:4px;background:#2c4351"></div>' +
        '<div style="position:absolute;left:300px;top:90px;width:4px;height:44px;background:var(--violet)"></div><div class="lbl" style="position:absolute;left:250px;top:150px;color:var(--violet)">t − h: features x</div>' +
        '<div style="position:absolute;left:1300px;top:90px;width:4px;height:44px;background:var(--green)"></div><div class="lbl" style="position:absolute;left:1240px;top:150px;color:var(--green)">t: target y known</div>' +
        '<div class="tag c-amber" style="position:absolute;left:560px;top:20px">update with (x from t − h, y at t)</div>'; },
    draw() {}
  };
})();
