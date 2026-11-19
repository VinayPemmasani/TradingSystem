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

// ---- sig-08 basis ----
(function () {
  let s = 13; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const F = []; let f = 6031; for (let i = 0; i < 100; i++) { f += (rnd() - 0.5) * 3; F.push([i, f]); }
  SCENES['title'] = {
    setup() { const c = SIG.chart('ti-ch', { w: 1300, h: 260, x: [0, 100], y: [5975, 6060], pad: { l: 10, b: 10, t: 10 } });
      c.f = c.line(F, '#6aa8ff', 4); c.c = c.line(F.map(([i, v]) => [i, v - 28]), '#3fd0dc', 4);
      c.a = c.svg.appendChild(SIG.el('line', { x1: c.X(92), x2: c.X(92), y1: c.Y(F[92][1]), y2: c.Y(F[92][1] - 28), stroke: '#ffb347', 'stroke-width': 4 })); },
    draw(u, cue, H) { const c = SIG.chart('ti-ch', {}); const k = (u - cue(1)) / 4; SIG.reveal(c.f, k); SIG.reveal(c.c, k - 0.03); SIG.vis(c.a, H.C((u - cue(1) - 4) / 0.5)); }
  };
  SCENES['invert'] = {
    setup() { const c = SIG.chart('iv-ch', { w: 1100, h: 260, x: [5998, 6006], y: [0, 1], xt: [5998, 6000, 6002, 6004, 6006], fx: (v) => v.toLocaleString('en-US'), pad: { l: 20, b: 50, t: 10 } });
      c.p = [c.vline(6000, '#3fd0dc', '0'), c.text(6000, 0.85, 'printed 6,000.00', '#3fd0dc', 'middle', 24)];
      c.s = [c.vline(6003.48, '#ffb347', '0'), c.text(6003.48, 0.6, 'implied 6,003.48', '#ffb347', 'middle', 24)];
      c.g = c.svg.appendChild(SIG.el('line', { x1: c.X(6000), x2: c.X(6003.48), y1: c.Y(0.3), y2: c.Y(0.3), stroke: '#a98bff', 'stroke-width': 4, 'marker-end': 'url(#ah-violet)' }));
      c.gt = c.text(6001.74, 0.36, '+3.48', '#a98bff', 'middle', 24); },
    draw(u, cue, H) { const c = SIG.chart('iv-ch', {}); c.p.forEach((e) => SIG.vis(e, H.C((u - cue(2) - 0.2) / 0.4))); c.s.forEach((e) => SIG.vis(e, H.C((u - cue(2) - 0.8) / 0.4))); SIG.vis(c.g, H.C((u - cue(2) - 1.4) / 0.4)); SIG.vis(c.gt, H.C((u - cue(2) - 1.4) / 0.4)); }
  };
  const P = []; let fp = 6031, idx = 6003; const PI = [];
  for (let i = 0; i < 120; i++) { fp += (i > 50 && i < 70 ? 0.6 : 0) + (rnd() - 0.5) * 1.2; P.push([i, fp]); if (i % 8 === 0) idx = fp - 28 - (i > 50 && i < 80 ? 2.5 : 0); PI.push([i, idx]); }
  SCENES['practice'] = {
    setup() { const lo = Math.min(...PI.map((q) => q[1])) - 4, hi = Math.max(...P.map((q) => q[1])) + 4;
      const c = SIG.chart('pr-ch', { w: 1060, h: 600, x: [0, 120], y: [lo, hi], yt: [Math.ceil(lo / 10) * 10, Math.ceil(lo / 10) * 10 + 20, Math.ceil(lo / 10) * 10 + 40], fy: (v) => v.toLocaleString('en-US'), xl: 'time', pad: { l: 110 } });
      c.f = c.line(P, '#6aa8ff', 4); c.sf = c.line(P.map(([i, v]) => [i, v - 28]), '#ffb347', 4); c.pi = c.step(PI, '#3fd0dc', 3);
      c.l = [c.text(118, P[119][1] + 3, 'futures', '#6aa8ff', 'end', 22), c.text(118, P[119][1] - 33, 'S* = F − 28', '#ffb347', 'end', 22), c.text(60, PI[60][1] - 5, 'printed index', '#3fd0dc', 'middle', 22)]; },
    draw(u, cue, H) { const c = SIG.chart('pr-ch', {}); SIG.reveal(c.f, (u - cue(1) - 0.3) / 3); SIG.reveal(c.sf, (u - cue(1) - 0.6) / 3); SIG.reveal(c.pi, (u - cue(3)) / 2.5);
      SIG.vis(c.l[0], H.C((u - cue(1) - 3) / 0.4)); SIG.vis(c.l[1], H.C((u - cue(1) - 3.3) / 0.4)); SIG.vis(c.l[2], H.C((u - cue(3) - 1.5) / 0.4)); }
  };
  SCENES['lab'] = {
    setup() { const g = H.$('lb-g'); if (g.children.length) return; const w = 1100;
      g.innerHTML = `<div style="position:absolute;left:0;top:60px;width:${w}px;height:10px;border-radius:5px;background:linear-gradient(90deg,var(--red),#2c4351 50%,var(--green))"></div>` +
        ['−0.10', '−0.05', '0', '+0.05', '+0.10'].map((t, i) => `<div class="lbl" style="position:absolute;left:${i * w / 4 - 40}px;top:85px;width:80px;text-align:center">${t}</div>`).join('') +
        `<div id="lb-n" style="position:absolute;top:35px;width:6px;height:60px;margin-left:-3px;border-radius:3px;background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>`; },
    draw(u, cue, H) { const v = 0.01 + 0.012 * Math.sin(u * 1.3) + 0.006 * Math.sin(u * 3.1); H.$('lb-n').style.left = ((v + 0.1) / 0.2 * 1100) + 'px'; }
  };
})();
