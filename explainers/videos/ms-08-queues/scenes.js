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


// ---- ms-08 queues ----
(function () {
  // segments: [{w (px), c (color), t (label)}] laid out left to right inside a host
  function segs(id, list) { const h = H.$(id); if (!h) return; if (!h._s) { h._s = []; }
    while (h._s.length < list.length) { const d = document.createElement('div'); d.style.cssText = 'position:absolute;top:0;height:100%;border-radius:8px;display:grid;place-items:center;font:600 22px var(--mono);color:#06141a;overflow:hidden;white-space:nowrap'; h.appendChild(d); h._s.push(d); }
    let x = 0; h._s.forEach((d, i) => { const s = list[i]; if (!s || s.w <= 0.5) { d.style.opacity = 0; return; } d.style.opacity = s.o === undefined ? 1 : s.o; d.style.left = x + 'px'; d.style.width = (s.w - 4) + 'px'; d.style.background = s.c; H.text(d, s.w > 90 ? (s.t || '') : ''); x += s.w; }); }
  SCENES['title'] = { draw(u, cue, H) { const k = H.C((u - cue(1)) / 4); const q = [];
    for (let i = 0; i < 12; i++) q.push({ w: i < Math.floor(k * 5) ? 0 : 110, c: '#a7b8c4' }); q.push({ w: 110, c: '#ffb347', t: 'you' }); segs('ti-q', q); } };
  SCENES['fifo'] = { draw(u, cue, H) { const q = []; const n0 = u >= cue(3) ? 1 : 0; const can = u >= cue(3) + 1.2;
    const names = ['#1', '#2', '#3', '#4', '#5', '#6'];
    names.forEach((n, i) => { if (i < n0) return; if (can && i === 3) return; q.push({ w: 230, c: i === 4 ? '#ffb347' : '#a7b8c4', t: n + (i === 4 ? ' you' : '') }); });
    const join = H.C((u - cue(2)) / 0.5); if (join > 0) q.push({ w: 230 * join, c: '#7f93a2', t: '#7 new' });
    if (u >= cue(4) + 0.6) { const me = q.findIndex((s) => s.c === '#ffb347'); if (me >= 0) { const m = q.splice(me, 1)[0]; m.c = '#ff8fc8'; m.t = '#5 replaced'; q.push(m); } }
    segs('ff-q', q); } };
  SCENES['worked'] = { draw(u, cue, H) { const S = 1300 / 7100; let ahead = 5000, behind = 0, me = 100;
      const tr = H.ease((u - cue(2)) / 1.5), cn = H.ease((u - cue(2) - 1.2) / 1.5); ahead -= 1500 * tr + 2000 * cn; behind = 400 * H.ease((u - cue(3)) / 0.8);
      const sw = H.ease((u - cue(4) - 0.3) / 2.5) * 2000; let s = sw; const a2 = Math.max(0, ahead - s); s -= ahead - a2; const m2 = Math.max(0, me - s); s -= me - m2; const b2 = Math.max(0, behind - Math.max(0, s));
      segs('wk-q', [{ w: (5000 - ahead) * S * (1 - tr * 0) * 0, c: '#000' }, { w: a2 * S, c: '#a7b8c4', t: Math.round(a2).toLocaleString('en-US') + ' ahead' }, { w: Math.max(m2 > 0 ? 70 : 0, m2 * S), c: '#ffb347', t: 'you' }, { w: b2 * S, c: '#7f93a2', t: Math.round(b2) + ' behind' }]);
      H.text('wk-px', u >= cue(6) ? 'bid 29.99' : 'bid 30.00'); } };
  SCENES['tick'] = {
    setup() { MS.ladder('tk-lad', { rows: 4, rowH: 76, pw: 170, sw: 300 }); },
    draw(u, cue, H) { const L = MS.ladder('tk-lad', {}); const k = H.C((u - cue(0) - 1) / 3.5); const ask = Math.round(1800 * (1 - k)); const up = ask <= 0;
      L.set(up ? [{ p: '30.03', a: 2100 }, { p: '30.02', a: 900 }, { p: '30.01', b: 600, hl: true }, { p: '30.00', b: 2400 }] : [{ p: '30.02', a: 2100 }, { p: '30.01', a: ask, hl: true }, { p: '30.00', b: 2400 }, { p: '29.99', b: 1900 }], 2400);
      H.text('tk-mid', up ? 'mid 30.015' : 'mid 30.005'); } };
})();
