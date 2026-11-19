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

// ---- sig-06 volatility ----
(function () {
  let s = 9; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const gauss = () => { let a = 0; for (let i = 0; i < 6; i++) a += rnd(); return (a - 3) * Math.SQRT2; };
  const P = []; let p = 50; for (let i = 0; i < 160; i++) { p *= Math.exp(gauss() * 0.002); P.push([i, p]); }
  SCENES['title'] = {
    setup() { const lo = Math.min(...P.map((q) => q[1])), hi = Math.max(...P.map((q) => q[1]));
      const c = SIG.chart('ti-ch', { w: 1640, h: 260, x: [0, 160], y: [lo - 0.3, hi + 0.3], pad: { l: 10, b: 10, t: 10 } });
      const up = P.map(([i, v]) => [i, v * 1.004]), dn = P.map(([i, v]) => [i, v * 0.996]);
      c.u = c.line(up, 'rgba(169,139,255,.6)', 2); c.d = c.line(dn, 'rgba(169,139,255,.6)', 2); c.p = c.line(P, '#3fd0dc', 4); },
    draw(u, cue) { const c = SIG.chart('ti-ch', {}); const k = (u - cue(1)) / 6; SIG.reveal(c.p, k); SIG.reveal(c.u, k - 0.03); SIG.reveal(c.d, k - 0.03); }
  };
  SCENES['close'] = {
    setup() { const c = SIG.chart('cl-ch', { w: 820, h: 600, x: [0, 4], y: [49.6, 50.7], yt: [49.7, 49.9, 50.1, 50.3, 50.5, 50.7], fy: (v) => v.toFixed(2) });
      c.pc = [c.svg.appendChild(SIG.el('line', { x1: c.X(0.4), x2: c.X(1.2), y1: c.Y(49.9), y2: c.Y(49.9), stroke: '#8ea3b1', 'stroke-width': 4 })), c.text(0.8, 49.86, 'prev close', '#8ea3b1', 'middle', 20)];
      c.wick = c.svg.appendChild(SIG.el('line', { x1: c.X(2.6), x2: c.X(2.6), y1: c.Y(50.6), y2: c.Y(49.7), stroke: '#a98bff', 'stroke-width': 5 }));
      c.body = c.svg.appendChild(SIG.el('rect', { x: c.X(2.6) - 70, y: c.Y(50.2), width: 140, height: c.Y(50.0) - c.Y(50.2), fill: '#4fd18b', rx: 4 }));
      c.lab = [c.text(2.85, 50.6, 'H 50.60', '#4fd18b', 'start', 22), c.text(2.85, 49.7, 'L 49.70', '#ff6b5e', 'start', 22), c.text(2.35, 50.2, 'C 50.20', '#eef4f7', 'end', 22), c.text(2.35, 49.98, 'O 50.00', '#eef4f7', 'end', 22)];
      c.arr = c.svg.appendChild(SIG.el('path', { d: `M${c.X(1.2)} ${c.Y(49.9)} L${c.X(2.6) - 80} ${c.Y(50.2)}`, stroke: '#ffb347', 'stroke-width': 3, 'stroke-dasharray': '8 6', fill: 'none' })); },
    draw(u, cue, H) { const c = SIG.chart('cl-ch', {}); const k = H.C((u - cue(2) - 0.2) / 0.5);
      c.pc.forEach((e) => SIG.vis(e, k)); SIG.vis(c.body, H.C((u - cue(2) - 0.8) / 0.5)); SIG.vis(c.wick, H.C((u - cue(2) - 1.4) / 0.5)); c.lab.forEach((e) => SIG.vis(e, H.C((u - cue(2) - 1.8) / 0.5))); SIG.vis(c.arr, H.C((u - cue(3)) / 0.5)); }
  };
  const R2 = []; for (let i = 0; i < 78; i++) { const r = gauss(); R2.push(r * r); }
  const mx = Math.max(...R2);
  SCENES['realised'] = {
    setup() { const g = H.$('rv-bars'); if (g.children.length) return;
      g.innerHTML = R2.map((v, i) => `<div id="rb${i}" style="position:absolute;left:${i * 21.8}px;bottom:0;width:16px;height:${Math.max(3, v / mx * 210)}px;border-radius:3px;background:var(--amber)"></div>`).join(''); },
    draw(u, cue, H) { R2.forEach((v, i) => SIG.vis(H.$('rb' + i), H.C((u - cue(1) - i * 0.04) / 0.2))); }
  };
  const B = []; let e = 50.005; for (let i = 0; i < 40; i++) { e += gauss() * 0.002; const side = rnd() < 0.5 ? 1 : -1; B.push([i, Math.round((e + side * 0.01) * 100) / 100, e]); }
  SCENES['noise'] = {
    setup() { const c = SIG.chart('nz-px', { w: 700, h: 300, x: [0, 40], y: [49.98, 50.03], yt: [49.99, 50.00, 50.01, 50.02], fy: (v) => v.toFixed(2), pad: { l: 100 } });
      c.e = c.line(B.map((q) => [q[0], q[2]]), '#3fd0dc', 3); c.t = c.step(B.map((q) => [q[0], q[1]]), '#ff6b5e', 3);
      const n = SIG.chart('nz-ch', { w: 900, h: 580, x: [0, 4], y: [0, 5], xt: [0, 1, 2, 3, 4], yt: [0, 1, 2, 3, 4, 5], fx: (v) => ['1 s', '10 s', '1 min', '5 min', '30 min'][v], fy: (v) => v + '%', xl: 'sampling interval', yl: 'realised σ, daily' });
      n.tr = [n.hline(1.5, '#4fd18b', '10 8'), n.text(0.1, 1.15, 'true 1.5%', '#4fd18b', 'start', 22)];
      const V = [4.743, 2.067, 1.612, 1.535, 1.429];
      n.l = n.line(V.map((v, i) => [i, v]), '#ffb347', 4); n.d = V.map((v, i) => [n.dot(i, v, 9, '#ffb347'), n.text(i === 4 ? i - 0.08 : i + 0.08, v + 0.2, (v + 1e-9).toFixed(2) + '%', '#ffb347', i === 4 ? 'end' : 'start', 22)]); },
    draw(u, cue, H) { const c = SIG.chart('nz-px', {}); SIG.reveal(c.e, (u - cue(0) - 0.4) / 2); SIG.reveal(c.t, (u - cue(0) - 0.6) / 2);
      const n = SIG.chart('nz-ch', {}); n.tr.forEach((x) => SIG.vis(x, H.C((u - cue(1) - 0.8) / 0.4)));
      const show = [cue(3), cue(3) + 0.6, cue(2) - 0.6 + 0.6, cue(2), cue(2) + 0.6];
      n.d.forEach((d, i) => { const k = H.C((u - show[i] - 0.4) / 0.3); SIG.vis(d[0], k); SIG.vis(d[1], k); });
      SIG.reveal(n.l, H.C((u - cue(3) - 1.2) / 1.0)); }
  };
})();
