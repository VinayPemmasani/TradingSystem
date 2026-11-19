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


// ---- ms-10 volume ----
(function () {
  const P = [12, 8, 7, 6, 5.5, 5, 5, 5, 5.5, 6, 6.5, 7.5, 11.5], CL = 9.5;
  const LB = ['9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', 'close'];
  function curve(id, w, h, labels) { const c = MS.chart(id, { w, h, x: [0, 14], y: [0, 14], xt: [], yt: labels ? [0, 5, 10] : [], fy: (v) => v + '%', pad: { l: labels ? 70 : 10, b: labels ? 50 : 10 } });
    c.b = P.map((p, i) => c.bar(i + 0.5, 0, p, w / 18, '#a7b8c4')); c.b.push(c.bar(13.5, 0, CL, w / 18, '#ffb347'));
    if (labels) c.l = LB.map((l, i) => c.text(i + 0.5, -1.4, l, i === 13 ? '#ffb347' : '#8ea3b1', 'middle', 18)); return c; }
  SCENES['title'] = { setup() { curve('ti-ch', 1300, 340, false); }, draw(u, cue, H) { const c = MS.chart('ti-ch', {}); c.b.forEach((b, i) => MS.vis(b, H.C((u - cue(1) - i * 0.12 - (i === 13 ? cue(2) - cue(1) : 0)) / 0.3))); } };
  SCENES['why'] = {
    setup() { const h = H.$('wy-d'); if (h.children.length) return; let seed = 3; const r = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
      h._d = []; for (let i = 0; i < 46; i++) { const d = document.createElement('div'); const cl = i < 18 ? 0 : (i < 32 ? 1 : 2); const x = cl === 0 ? 80 + r() * 260 : cl === 1 ? 700 + r() * 300 : 1320 + r() * 300;
        d.style.cssText = `position:absolute;left:${r() * 1650}px;top:${r() * 330}px;width:24px;height:24px;border-radius:50%;background:${i % 7 === 0 ? 'var(--violet)' : 'var(--green)'}`; d._x0 = parseFloat(d.style.left); d._y0 = parseFloat(d.style.top); d._x1 = x; d._y1 = 60 + r() * 240; d._v = i % 7 === 0; h.appendChild(d); h._d.push(d); } },
    draw(u, cue, H) { H.$('wy-d')._d.forEach((d) => { const k = H.ease((u - (d._v ? cue(2) : cue(1)) - 0.3) / 1.5); d.style.left = H.lerp(d._x0, d._x1, k) + 'px'; d.style.top = H.lerp(d._y0, d._y1, k) + 'px'; }); }
  };
  SCENES['close'] = { setup() { const h = H.$('cl-d'); if (h.children.length) return; h._d = []; for (let i = 0; i < 30; i++) { const d = document.createElement('div'); d.style.cssText = `position:absolute;left:${i * 42}px;top:10px;width:30px;height:30px;border-radius:6px;background:${i % 3 ? 'var(--green)' : 'var(--red)'}`; h.appendChild(d); h._d.push(d); } },
    draw(u, cue, H) { H.$('cl-d')._d.forEach((d, i) => { d.style.opacity = H.C((u - cue(2) - i * 0.05) / 0.2); }); } };
  SCENES['vwap'] = {
    setup() { const c = curve('vw-ch', 1700, 560, true); c.t = P.concat([CL]).map((p, i) => c.text(i + 0.5, p + 0.5, Math.round(p * 1000).toLocaleString('en-US'), i === 13 ? '#ffb347' : '#3fd0dc', 'middle', 20)); },
    draw(u, cue, H) { const c = MS.chart('vw-ch', {}); c.b.forEach((b, i) => MS.vis(b, H.C((u - cue(1) - 0.3 - i * 0.08) / 0.3))); c.l.forEach((b, i) => MS.vis(b, H.C((u - cue(1) - 0.3 - i * 0.08) / 0.3)));
      const at = (i) => i === 0 ? cue(3) + 0.8 : i === 13 ? cue(4) + 1.6 : cue(4) + 0.2 + i * 0.06; c.t.forEach((t, i) => MS.vis(t, H.C((u - at(i)) / 0.3))); }
  };
  SCENES['lab'] = {
    setup() { const c = MS.chart('lb-ch', { w: 620, h: 300, x: [0, 13], y: [0, 10], xt: [], yt: [], xl: '13 half hours', yl: 'simulated volume', pad: { l: 20, b: 40 } });
      c.b = []; for (let i = 0; i < 13; i++) c.b.push(c.bar(i + 0.5, 0, 7.7, 34, '#6aa8ff')); },
    draw(u, cue, H) { const c = MS.chart('lb-ch', {}); c.b.forEach((b, i) => MS.vis(b, H.C((u - cue(1) - i * 0.06) / 0.3))); }
  };
})();
