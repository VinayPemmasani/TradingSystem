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


// ---- ms-07 fragmentation ----
(function () {
  SCENES['title'] = {
    setup() { const h = H.$('ti-net'); if (h.children.length) return; const svg = MS.el('svg', { width: 1640, height: 400, style: 'position:absolute;left:0;top:0;overflow:visible' }, h);
      h._l = []; h._n = []; const cx = 820, cy = 200;
      for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2, r = 160 + (i % 3) * 25; const x = cx + Math.cos(a) * r * 3.6, y = cy + Math.sin(a) * r;
        h._l.push(MS.el('line', { x1: cx, y1: cy, x2: x, y2: y, stroke: i < 17 ? '#a7b8c4' : '#3a5566', 'stroke-width': 2 }, svg));
        h._n.push(MS.el('circle', { cx: x, cy: y, r: 14, fill: i < 17 ? '#a7b8c4' : '#3a5566' }, svg)); }
      h._c = MS.el('circle', { cx, cy, r: 40, fill: '#3fd0dc' }, svg); const t = MS.el('text', { x: cx, y: cy + 9, 'text-anchor': 'middle', style: 'font:700 26px var(--mono);fill:#06141a' }, svg); t.textContent = 'XYZ'; },
    draw(u, cue, H) { const h = H.$('ti-net'); h._n.forEach((n, i) => { const k = H.C((u - cue(1) - i * 0.08) / 0.3); n.style.opacity = k; h._l[i].style.opacity = k * 0.6; }); }
  };
  const SH = [['NYSE group', 18.77, '#a7b8c4'], ['Nasdaq', 13.53, '#a7b8c4'], ['Cboe', 8.78, '#a7b8c4'], ['IEX', 4.20, '#a7b8c4'], ['MEMX', 2.22, '#a7b8c4'], ['4 others', 0.84, '#a7b8c4'], ['off-exchange (TRFs)', 51.66, '#3fd0dc']];
  SCENES['count'] = {
    setup() { const h = H.$('ct-ch'); if (h.children.length) return; let s = '';
      SH.forEach((p, i) => { const y = i * 74 + 10; s += `<div style="position:absolute;left:0;top:${y + 8}px;width:300px;font:600 25px var(--body);color:${i === 6 ? '#3fd0dc' : '#eef4f7'}">${p[0]}</div><div class="ctb" style="position:absolute;left:310px;top:${y}px;height:48px;border-radius:6px;background:${p[2]}"></div><div class="ctv" style="position:absolute;left:${320 + p[1] * 14}px;top:${y + 8}px;font:600 24px var(--mono);color:${p[2]}">${p[1].toFixed(1)}%</div>`; });
      h.innerHTML = s; },
    draw(u, cue, H) { const h = H.$('ct-ch'); const b = h.querySelectorAll('.ctb'), v = h.querySelectorAll('.ctv'); const at = [cue(2) + 0.3, cue(3), cue(3) + 0.6, cue(3) + 1.0, cue(3) + 1.2, cue(3) + 1.4, cue(4) + 0.3];
      SH.forEach((p, i) => { const k = H.ease((u - at[i]) / 0.8); b[i].style.width = p[1] * 14 * k + 'px'; v[i].style.opacity = H.C((u - at[i] - 0.7) / 0.3); }); }
  };
  const VEN = [['A', '30.02', 800, 800], ['B', '30.02', 1000, 1000], ['C', '30.02', 500, 500], ['D', '30.03', 1200, 700]];
  SCENES['sweep'] = {
    setup() { const h = H.$('sw-v'); if (h.children.length) return; let s = '';
      VEN.forEach((v, i) => { const x = i * 275; s += `<div class="node" style="position:absolute;left:${x}px;top:0;width:250px;padding:12px"><div class="t" style="font-size:28px">exch ${v[0]}</div><div class="s">offer ${v[1]}</div></div>`;
        s += `<div style="position:absolute;left:${x + 30}px;top:130px;width:190px;height:240px;border-radius:10px;background:#0b1820;border:1px solid var(--line)"><div class="swq" style="position:absolute;left:0;bottom:0;width:190px;border-radius:10px;background:rgba(255,107,94,.75)"></div><div class="swt" style="position:absolute;left:0;top:-36px;width:190px;text-align:center;font:600 24px var(--mono);color:#ffaaa2"></div></div>`; });
      h.innerHTML = s; },
    draw(u, cue, H) { const h = H.$('sw-v'); const q = h.querySelectorAll('.swq'), t = h.querySelectorAll('.swt');
      VEN.forEach((v, i) => { const show = H.C((u - cue(i < 3 ? 2 : 3) - (i < 3 ? i * 0.3 : 0)) / 0.4); const take = H.ease((u - cue(4) - 0.4) / 1.0);
        const left = v[2] - v[3] * take; q[i].style.height = (left / 1200 * 240 * show) + 'px'; H.text(t[i], show > 0 ? Math.round(left).toLocaleString('en-US') : ''); }); }
  };
  SCENES['fade'] = {
    setup() { const c = MS.chart('fd-ch', { w: 1300, h: 560, x: [0, 500], y: [0, 4.5], xt: [0, 100, 200, 300, 400, 500], fx: (v) => v + ' µs', yt: [], xl: 'time after the router sends', pad: { l: 140 } });
      ['A', 'B', 'C', 'D'].forEach((n, i) => { c.text(-10, 4 - i - 0.1, 'exch ' + n, '#eef4f7', 'end', 24); });
      c.arr = [[20, 4], [60, 3], [110, 2], [320, 1]].map(([x, y]) => [c.line([[0, y], [x, y]], '#4fd18b', 5), c.dot(x, y, 11, '#4fd18b')]);
      c.pr = c.text(30, 4.25, 'fill prints', '#ffb347', 'start', 22);
      c.see = c.line([[20, 4], [140, 1.15]], '#a98bff', 3); c.can = [c.dot(150, 1, 13, '#a98bff'), c.text(160, 1.3, 'quote cancelled', '#a98bff', 'start', 22)];
      c.miss = c.text(330, 0.65, 'your order lands: nothing left', '#ff8fc8', 'start', 22); },
    draw(u, cue, H) { const c = MS.chart('fd-ch', {}); c.arr.forEach((a, i) => { MS.reveal(a[0], (u - cue(1) - 0.3 - i * 0.2) / 0.8); MS.vis(a[1], H.C((u - cue(1) - 1.0 - i * 0.2) / 0.2)); });
      MS.vis(c.pr, H.C((u - cue(2)) / 0.3)); MS.reveal(c.see, (u - cue(2) - 0.3) / 0.8); c.can.forEach((e) => MS.vis(e, H.C((u - cue(2) - 1.1) / 0.3))); MS.vis(c.miss, H.C((u - cue(3)) / 0.3)); }
  };
  SCENES['lab'] = {
    setup() { const h = H.$('lb-m'); if (h.children.length) return; let s = '';
      ['venue 1', 'venue 2', 'venue 3'].forEach((n, i) => { s += `<div class="node" style="position:absolute;left:0;top:${i * 120}px;width:260px;padding:10px"><div class="t" style="font-size:26px">${n}</div></div><div class="node blue" style="position:absolute;left:400px;top:${i * 120}px;width:300px;padding:10px"><div class="t" style="font-size:26px">book ${i + 1}</div></div>`; });
      s += `<div class="node teal" style="position:absolute;left:900px;top:110px;width:420px"><div class="t">merge tops</div><div class="s">our NBBO view</div></div><div class="node green" style="position:absolute;left:1440px;top:110px;width:260px"><div class="t">router</div></div>`;
      h.innerHTML = s; const svg = MS.el('svg', { width: 1700, height: 360, style: 'position:absolute;left:0;top:0;overflow:visible' }, h);
      for (let i = 0; i < 3; i++) { MS.el('line', { x1: 270, y1: i * 120 + 32, x2: 390, y2: i * 120 + 32, stroke: '#6aa8ff', 'stroke-width': 3 }, svg); MS.el('line', { x1: 710, y1: i * 120 + 32, x2: 890, y2: 160, stroke: '#3fd0dc', 'stroke-width': 3 }, svg); }
      MS.el('line', { x1: 1330, y1: 160, x2: 1430, y2: 160, stroke: '#4fd18b', 'stroke-width': 3 }, svg); }
  };
})();
