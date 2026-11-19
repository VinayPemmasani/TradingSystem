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


// ---- ms-05 PFOF ----
(function () {
  SCENES['flow'] = { setup() { const h = H.$('fl-w'); if (h.children.length) return; let s = '';
      for (let i = 0; i < 6; i++) s += `<div class="node teal" style="position:absolute;left:0;top:${i * 92}px;width:520px;padding:10px 18px"><div class="t" style="font-size:24px">wholesaler ${i + 1}</div></div>`; h.innerHTML = s; } };
  SCENES['why'] = {
    setup() { const c = MS.chart('wy-ch', { w: 1060, h: 580, x: [0, 5], y: [-0.5, 3], xt: [0, 1, 2, 3, 4, 5], yt: [0, 1, 2, 3], fy: (v) => '+' + v + '¢', xl: 'minutes after a buy fill', yl: 'mid move (illustrative)', pad: { l: 100 } });
      const r = [], i = []; for (let k = 0; k <= 50; k++) { const t = k / 10; r.push([t, 0.15 * (1 - Math.exp(-t)) + 0.08 * Math.sin(t * 3)]); i.push([t, 2.4 * (1 - Math.exp(-t * 1.2))]); }
      c.r = c.line(r, '#4fd18b', 5); c.i = c.line(i, '#a98bff', 5);
      c.rt = c.text(4.9, 0.35, 'after a retail buy', '#4fd18b', 'end', 22); c.it = c.text(4.9, 2.55, 'after an informed buy', '#a98bff', 'end', 22); },
    draw(u, cue, H) { const c = MS.chart('wy-ch', {}); MS.reveal(c.r, (u - cue(1) - 0.2) / 1.2); MS.vis(c.rt, H.C((u - cue(1) - 1) / 0.4));
      MS.reveal(c.i, (u - cue(2)) / 1.2); MS.vis(c.it, H.C((u - cue(2) - 1) / 0.4)); }
  };
  SCENES['worked'] = {
    setup() { const c = MS.chart('wk-l', { w: 900, h: 600, x: [0, 10], y: [49.995, 50.045], yt: [50.00, 50.01, 50.02, 50.03, 50.04], fy: (v) => v.toFixed(2), xt: [], pad: { l: 120, b: 30 } });
      const lv = (y, col, txt, x0) => [c.line([[x0 || 0.3, y], [9.7, y]], col, 6), c.text(9.6, y + 0.0025, txt, col, 'end', 24)];
      c.bid = lv(50.00, '#4fd18b', 'best bid'); c.ask = lv(50.04, '#ff6b5e', 'best offer'); c.mid = lv(50.02, '#3fd0dc', 'mid');
      c.fill = [c.dot(3, 50.03, 14, '#4fd18b'), c.text(3.4, 50.0315, 'retail buy filled 50.03', '#4fd18b', 'start', 24)];
      const br = (x, a, b, col) => c.line([[x, a], [x, b]], col, 10);
      c.imp = br(1.5, 50.03, 50.04, '#4fd18b'); c.ws = br(6, 50.02, 50.03, '#3fd0dc'); c.pf = br(7.5, 50.0227, 50.03, '#ffb347');
      c.pft = c.text(7.8, 50.026, '0.73¢ to broker', '#ffb347', 'start', 22); },
    draw(u, cue, H) { const c = MS.chart('wk-l', {}); const a = cue(1);
      [c.bid, c.ask].forEach((l, i) => { MS.reveal(l[0], (u - a - i * 0.3) / 0.6); MS.vis(l[1], H.C((u - a - 0.5 - i * 0.3) / 0.3)); });
      MS.reveal(c.mid[0], (u - cue(4)) / 0.6); MS.vis(c.mid[1], H.C((u - cue(4) - 0.4) / 0.3));
      c.fill.forEach((e) => MS.vis(e, H.C((u - cue(2)) / 0.4))); MS.reveal(c.imp, (u - cue(2) - 0.6) / 0.5);
      MS.reveal(c.ws, (u - cue(4) - 0.5) / 0.5); MS.reveal(c.pf, (u - cue(4) - 1.2) / 0.5); MS.vis(c.pft, H.C((u - cue(4) - 1.5) / 0.3)); }
  };
  const V = [['Virtu Americas', 46.32, 73.11], ['G1 Execution', 14.62, 83.15], ['Jane Street', 13.47, 101.25], ['Citadel Securities', 10.30, 42.80], ['Hudson River Trading', 9.28, 66.75], ['Two Sigma Securities', 6.01, 75.42]];
  SCENES['data'] = {
    setup() { const h = H.$('dt-ch'); if (h.children.length) return; let s = '<div class="lbl" style="position:absolute;left:380px;top:0">share of non-directed orders</div><div class="lbl" style="position:absolute;left:1060px;top:0">paid for market orders, ¢ per 100 shares</div>';
      V.forEach((v, i) => { const y = 50 + i * 82;
        s += `<div style="position:absolute;left:0;top:${y + 8}px;font:600 26px var(--body);color:#eef4f7">${v[0]}</div>`;
        s += `<div class="dtb" data-i="${i}" style="position:absolute;left:380px;top:${y}px;height:50px;border-radius:6px;background:var(--teal)"></div><div class="dtv" style="position:absolute;left:${390 + v[1] * 11}px;top:${y + 10}px;font:600 24px var(--mono);color:var(--teal)">${v[1].toFixed(1)}%</div>`;
        s += `<div class="dta" style="position:absolute;left:1060px;top:${y}px;height:50px;border-radius:6px;background:var(--amber)"></div><div class="dtw" style="position:absolute;left:${1070 + v[2] * 4.6}px;top:${y + 10}px;font:600 24px var(--mono);color:var(--amber)">${v[2].toFixed(0)}¢</div>`; });
      h.innerHTML = s; },
    draw(u, cue, H) { const h = H.$('dt-ch'); const b = h.querySelectorAll('.dtb'), bv = h.querySelectorAll('.dtv'), a = h.querySelectorAll('.dta'), av = h.querySelectorAll('.dtw');
      V.forEach((v, i) => { const k = H.ease((u - cue(2) - i * 0.15) / 0.8); b[i].style.width = v[1] * 11 * k + 'px'; bv[i].style.opacity = H.C((u - cue(2) - 0.8 - i * 0.15) / 0.3);
        const q = H.ease((u - cue(3) - i * 0.15) / 0.8); a[i].style.width = v[2] * 4.6 * q + 'px'; av[i].style.opacity = H.C((u - cue(3) - 0.8 - i * 0.15) / 0.3); }); }
  };
})();
