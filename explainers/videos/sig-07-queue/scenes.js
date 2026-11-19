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

// ---- sig-07 queue ----
(function () {
  // A queue drawn as segments: [{w, color, label}], scale px per share
  function seg(id, parts, k) { const g = H.$(id); if (!g) return;
    if (!g._s) { g._s = parts.map(() => { const d = document.createElement('div'); d.style.cssText = 'position:absolute;top:30px;height:90px;border-radius:10px;display:grid;place-items:center;font:700 26px var(--mono);color:#06141a;overflow:hidden;white-space:nowrap;border:2px solid rgba(0,0,0,.3)'; g.appendChild(d); return d; }); }
    let x = 0; parts.forEach((p, i) => { const d = g._s[i]; const w = Math.max(0, p.w * k); d.style.left = x + 'px'; d.style.width = w + 'px'; d.style.background = p.c; d.style.opacity = w < 2 ? 0 : (p.o ?? 1); const t = w > 60 ? p.l : ''; if (d.textContent !== t) d.textContent = t; x += w + (w > 0 ? 6 : 0); }); }
  SCENES['title'] = { draw(u, cue, H) { const t = H.C((u - cue(1) - 0.5) / 4); const ahead = 900 * (1 - t);
    seg('ti-q', [{ w: ahead, c: 'var(--green)', l: ahead > 250 ? Math.round(ahead) + ' ahead' : '' }, { w: 160, c: 'var(--amber)', l: 'you' }, { w: 400, c: '#3f7f5f', l: 'behind' }], 1.1); } };
  SCENES['why'] = { draw(u, cue, H) { const late = H.C((u - cue(1)) / 0.5);
    seg('wy-q', [{ w: 300, c: 'var(--green)', l: 'first' }, { w: 400, c: 'var(--green)', l: 'next' }, { w: 350 * late, c: '#3f7f5f', l: 'later' }, { w: 140 * late, c: 'var(--amber)', l: 'you' }], 1.2); } };
  SCENES['worked'] = { draw(u, cue, H) {
    const tr = H.C((u - cue(1) - 0.3) / 0.8), cx = H.C((u - cue(2) - 0.3) / 0.8);
    seg('wk-q', [{ w: 200 * (1 - tr), c: 'var(--red)', l: tr < 0.4 ? 'traded 200' : '' }, { w: 60 * (1 - cx), c: 'var(--pink)', l: '60' }, { w: 340, c: 'var(--green)', l: tr < 1 ? '' : (cx < 1 ? '400 ahead' : '340 ahead') }, { w: 150, c: 'var(--amber)', l: 'you' }, { w: 40 * (1 - cx), c: 'var(--pink)', l: '' }, { w: 360, c: '#3f7f5f', l: 'behind' }], 1.15); } };
  SCENES['prob'] = {
    setup() { const g = H.$('pb-race'); if (g.children.length) return;
      g.innerHTML = '<div class="lbl" style="position:absolute;left:0;top:10px">shares ahead → 0</div><div id="pb-a" style="position:absolute;left:0;top:50px;height:60px;border-radius:8px;background:var(--green)"></div>' +
        '<div class="lbl" style="position:absolute;left:0;top:140px">ask queue → 0 (price moves away)</div><div id="pb-b" style="position:absolute;left:0;top:180px;height:60px;border-radius:8px;background:var(--red)"></div>'; },
    draw(u, cue, H) { const t = (u - cue(2) - 0.5); const a = Math.max(0, 1 - 0.09 * t - 0.05 * Math.sin(t * 2)), b = Math.max(0, 0.75 - 0.07 * t + 0.08 * Math.sin(t * 1.7));
      H.$('pb-a').style.width = (840 * a) + 'px'; H.$('pb-b').style.width = (840 * b) + 'px'; }
  };
})();
