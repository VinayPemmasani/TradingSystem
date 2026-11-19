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

// ---- sig-05 lead-lag ----
(function () {
  let s = 5; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const F = [], C = []; let f = 0; const fs = [];
  for (let i = 0; i < 100; i++) { f += (rnd() - 0.47) * 1.2; fs.push(f); F.push([i, f]); }
  for (let i = 0; i < 100; i++) C.push([i, (fs[Math.max(0, i - 4)] * 0.7 + fs[Math.max(0, i - 3)] * 0.3) + (rnd() - 0.5) * 0.3]);
  const lo = Math.min(...F.map((p) => p[1]), ...C.map((p) => p[1])) - 0.5, hi = Math.max(...F.map((p) => p[1]), ...C.map((p) => p[1])) + 0.5;
  SCENES['title'] = {
    setup() { const c = SIG.chart('ti-ch', { w: 1100, h: 260, x: [0, 100], y: [lo, hi], pad: { l: 10, b: 10, t: 10 } }); c.f = c.line(F, '#6aa8ff', 4); c.c = c.line(C, '#3fd0dc', 4); },
    draw(u, cue) { const c = SIG.chart('ti-ch', {}); const p = (u - cue(1)) / 6; SIG.reveal(c.f, p); SIG.reveal(c.c, p - 0.04); }
  };
  SCENES['today'] = {
    setup() { const c = SIG.chart('td-ch', { w: 900, h: 480, x: [-0.5, 3.5], y: [0, 1], yt: [0, 0.25, 0.5, 0.75, 1], fy: (v) => v.toFixed(2) });
      c.b = [['1 ms', 0.0073], ['10 ms', 0.0923], ['1 s', 0.6879], ['1 min', 0.9798]].map(([n, v], i) => [c.bar(i, 0, v, 120, i === 1 || i === 3 ? '#ffb347' : '#5b6f7c'), c.text(i, -0.08, n, '#8ea3b1', 'middle', 22), c.text(i, v + 0.03, v.toFixed(2), i === 1 || i === 3 ? '#ffb347' : '#8ea3b1', 'middle', 24)]); },
    draw(u, cue, H) { const c = SIG.chart('td-ch', {}); c.b.forEach((b, i) => { const k = H.C((u - cue(2) - 0.2 - i * 0.3) / 0.3); b.forEach((e) => SIG.vis(e, k)); }); }
  };
  const R = [[-3, 0.002], [-2, 0.006], [-1, 0.004], [0, 0.13], [1, 0.373], [2, 0.711], [3, 0.01]];
  SCENES['measure'] = {
    setup() { const c = SIG.chart('ms-ch', { w: 860, h: 600, x: [-3.6, 3.6], y: [0, 0.8], xt: [-3, -2, -1, 0, 1, 2, 3], yt: [0, 0.2, 0.4, 0.6, 0.8], fy: (v) => v.toFixed(1), xl: 'lag k (steps)', yl: 'ρ(k)' });
      c.b = R.map(([k, v]) => [c.bar(k, 0, v, 70, k === 2 ? '#ffb347' : k < 0 ? '#5b6f7c' : '#6aa8ff'), c.text(k, v + 0.025, v.toFixed(2), k === 2 ? '#ffb347' : '#8ea3b1', 'middle', 22)]);
      c.n = c.text(-3.3, 0.12, 'cash does not lead', '#8ea3b1', 'start', 22); },
    draw(u, cue, H) { const c = SIG.chart('ms-ch', {}); c.b.forEach((b, i) => { const k = H.C((u - cue(2) - 0.8 - i * 0.25) / 0.3); b.forEach((e) => SIG.vis(e, k)); }); SIG.vis(c.n, H.C((u - cue(3) - 1.5) / 0.4)); }
  };
  SCENES['predict'] = {
    setup() { const c = SIG.chart('pd-ch', { w: 640, h: 240, x: [0, 10], y: [99.5, 103], pad: { l: 10, b: 10, t: 10 } });
      c.f = c.step([[0, 100], [3, 100], [3, 102], [10, 102]], '#6aa8ff', 4); c.v = c.step([[0, 100], [3.2, 100], [3.2, 100.6], [10, 100.6]], '#ffb347', 4);
      c.t1 = c.text(9.8, 102.3, 'futures', '#6aa8ff', 'end', 20); c.t2 = c.text(9.8, 100.85, 'follower fair value', '#ffb347', 'end', 20); },
    draw(u, cue, H) { const c = SIG.chart('pd-ch', {}); const p = (u - cue(3) - 0.5) / 1.5; SIG.reveal(c.f, p); SIG.reveal(c.v, p - 0.05); SIG.vis(c.t1, H.C(p * 2 - 1)); SIG.vis(c.t2, H.C(p * 2 - 1)); }
  };
})();
