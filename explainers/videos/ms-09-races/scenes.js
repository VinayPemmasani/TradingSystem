// ---- shared helpers for the market microstructure series (ms-01..10) ----
window.MS = (function () {
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


// ---- ms-09 races ----
(function () {
  SCENES['mech'] = {
    setup() { const c = MS.chart('mc-c', { w: 880, h: 500, x: [0, 3], y: [0, 1], xt: [], yt: [0, 0.5, 1], fy: (v) => v.toFixed(1), pad: { l: 80, b: 60 } });
      const D = [['1 ms', 0.0073], ['10 ms', 0.0923], ['1 min', 0.98]];
      c.b = D.map((d, i) => c.bar(i + 0.5, 0, Math.max(d[1], 0.008), 150, '#3fd0dc')); c.t = D.map((d, i) => c.text(i + 0.5, d[1] + 0.04, d[1] < 0.01 ? d[1].toFixed(4) : d[1].toFixed(2), '#3fd0dc', 'middle', 26));
      c.l = D.map((d, i) => c.text(i + 0.5, -0.08, d[0], '#8ea3b1', 'middle', 24)); },
    draw(u, cue, H) { const c = MS.chart('mc-c', {}); const at = [cue(1) + 1.6, cue(1) + 1.0, cue(1) + 0.3];
      c.b.forEach((b, i) => { MS.vis(b, H.C((u - at[i]) / 0.4)); MS.vis(c.t[i], H.C((u - at[i] - 0.2) / 0.4)); MS.vis(c.l[i], H.C((u - at[i]) / 0.4)); }); }
  };
  function lane(id, batch, u, t0) { const h = H.$(id); if (!h._m) { h._m = []; for (let i = 0; i < 9; i++) { const d = document.createElement('div'); d.style.cssText = 'position:absolute;width:26px;height:26px;border-radius:50%;margin:-13px 0 0 -13px'; h.appendChild(d); h._m.push(d); }
      if (batch) for (let k = 1; k <= 5; k++) { const l = document.createElement('div'); l.style.cssText = `position:absolute;left:${k * 300}px;top:0;width:3px;height:200px;background:var(--amber);opacity:.8`; h.appendChild(l); const t = document.createElement('div'); t.className = 'lbl'; t.style.cssText = `position:absolute;left:${k * 300 + 10}px;top:170px;color:var(--amber)`; t.textContent = 'clear'; h.appendChild(t); }
      const base = document.createElement('div'); base.style.cssText = `position:absolute;left:0;top:${batch ? 80 : 70}px;width:1700px;height:3px;background:#2c4351`; h.appendChild(base); }
    const xs = [60, 140, 260, 380, 455, 470, 700, 980, 1240]; const col = ['#4fd18b', '#ff6b5e', '#a98bff', '#3fd0dc', '#a98bff', '#3fd0dc', '#4fd18b', '#ff6b5e', '#4fd18b'];
    h._m.forEach((d, i) => { const x = xs[i]; const k = H.C((u - t0 - x / 300) / 0.2); let y = batch ? 80 : 70;
      if (batch) { const edge = Math.ceil(x / 300) * 300; const ku = H.C((u - t0 - edge / 300) / 0.3); y = 80 - 40 * ku; d.style.opacity = k * (1 - 0.6 * ku); } else d.style.opacity = k;
      d.style.left = x + 'px'; d.style.top = y + 'px'; d.style.background = col[i]; }); }
  SCENES['fba'] = { draw(u, cue, H) { lane('fb-c', false, u, cue(0) + 0.3); lane('fb-b', true, u, cue(1)); } };
  SCENES['worked'] = {
    setup() { const c = MS.chart('wk-ch', { w: 1040, h: 600, x: [0, 1000], y: [29.995, 30.045], xt: [0, 200, 400, 600, 800], yt: [30.00, 30.01, 30.02, 30.03, 30.04], fy: (v) => v.toFixed(2), xl: 'shares', pad: { l: 110 } });
      c.d = c.line([[0, 30.045], [0, 30.04], [300, 30.04], [300, 30.03], [500, 30.03], [500, 30.01], [900, 30.01], [900, 29.995]], '#4fd18b', 5);
      c.s = c.line([[0, 29.995], [0, 30.00], [200, 30.00], [200, 30.02], [500, 30.02], [500, 30.03], [800, 30.03], [800, 30.045]], '#ff6b5e', 5);
      c.dt = c.text(910, 30.012, 'demand', '#4fd18b', 'start', 22); c.st = c.text(810, 30.035, 'supply', '#ff6b5e', 'start', 22);
      c.x = c.dot(500, 30.02, 14, '#ffb347'); c.xt = c.text(520, 30.0225, '500 @ 30.02', '#ffb347', 'start', 26); },
    draw(u, cue, H) { const c = MS.chart('wk-ch', {}); MS.reveal(c.d, (u - cue(1) - 0.3) / 1.4); MS.vis(c.dt, H.C((u - cue(1) - 1.4) / 0.3));
      MS.reveal(c.s, (u - cue(2) - 0.3) / 1.4); MS.vis(c.st, H.C((u - cue(2) - 1.4) / 0.3)); MS.vis(c.x, H.C((u - cue(3) - 0.5) / 0.3)); MS.vis(c.xt, H.C((u - cue(4)) / 0.3)); }
  };
})();
