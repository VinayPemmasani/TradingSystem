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

// ---- sig-03 trade flow ----
(function () {
  // deterministic pseudo-random trades for the title tape
  const T = []; let s = 7; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 60; i++) { const buy = rnd() < (i % 20 < 12 ? 0.68 : 0.35); T.push({ b: buy, q: 100 * (1 + Math.floor(rnd() * 5)) }); }
  SCENES['title'] = {
    setup() { const t = H.$('ti-tape'); if (t.children.length) return;
      t.innerHTML = T.map((x, i) => `<div class="chip" id="tt${i}" style="position:absolute;top:20px;left:0;background:var(--${x.b ? 'green' : 'red'})">${x.b ? '+' : '−'}${x.q}</div>`).join(''); },
    draw(u, cue, H) { const t0 = cue(1); let sv = 0;
      T.forEach((x, i) => { const e = H.$('tt' + i); const x0 = 1640 - (u - t0 - i * 0.28) * 260; e.style.left = x0 + 'px'; e.style.opacity = x0 < 1640 && x0 > -120 ? 1 : 0; if (x0 < 1640) sv += x.b ? x.q : -x.q; });
      H.text('ti-sv', (sv >= 0 ? '+' : '−') + Math.abs(sv).toLocaleString('en-US') + ' shares'); }
  };
  SCENES['leeready'] = {
    setup() { const c = SIG.chart('lr-axis', { w: 900, h: 420, x: [0, 10], y: [49.995, 50.025], yt: [50.00, 50.01, 50.02], fy: (v) => v.toFixed(2), xl: 'time', pad: { l: 110 } });
      c.zb = c.svg.appendChild(SIG.el('rect', { x: c.X(0), y: c.Y(50.025), width: c.X(10) - c.X(0), height: c.Y(50.0105) - c.Y(50.025), fill: 'rgba(79,209,139,.12)' }));
      c.zs = c.svg.appendChild(SIG.el('rect', { x: c.X(0), y: c.Y(50.0095), width: c.X(10) - c.X(0), height: c.Y(49.995) - c.Y(50.0095), fill: 'rgba(255,107,94,.12)' }));
      c.bid = c.hline(50.00, '#4fd18b', '0'); c.ask = c.hline(50.02, '#ff6b5e', '0'); c.mid = c.hline(50.01, '#3fd0dc', '8 8');
      c.lb = c.text(9.9, 50.0225, 'buy zone', '#4fd18b', 'end', 22); c.ls = c.text(9.9, 49.997, 'sell zone', '#ff6b5e', 'end', 22);
      c.tr = [[2, 50.02, '#4fd18b'], [4, 50.00, '#ff6b5e'], [6, 50.01, '#ffb347'], [8, 50.01, '#ffb347']].map(([x, y, col]) => c.dot(x, y, 11, col)); },
    draw(u, cue, H) { const c = SIG.chart('lr-axis', {});
      [c.zb, c.zs, c.lb, c.ls].forEach((e) => SIG.vis(e, H.C((u - cue(2) - 0.3) / 0.5)));
      c.tr.forEach((d, i) => SIG.vis(d, H.C((u - cue(i < 2 ? 2 : 3) - 0.6 - (i % 2) * 0.6) / 0.3))); }
  };
  SCENES['classify'] = {
    setup() { const c = SIG.chart('cl-ch', { w: 640, h: 420, x: [0, 5], y: [49.995, 50.025], yt: [50.00, 50.01, 50.02], fy: (v) => v.toFixed(2), pad: { l: 110 } });
      c.hline(50.00, '#4fd18b', '0'); c.hline(50.02, '#ff6b5e', '0'); c.hline(50.01, '#3fd0dc', '8 8');
      c.p = [[1, 50.02, '#4fd18b', 1], [2, 50.00, '#ff6b5e', 1.6], [3, 50.01, '#4fd18b', 2], [4, 50.01, '#4fd18b', 4]].map(([x, y, col, k]) => [c.dot(x, y, 12, col), k]); },
    draw(u, cue, H) { const c = SIG.chart('cl-ch', {}); c.p.forEach(([d, k]) => { const ci = Math.floor(k), dd = (k % 1) * 2; SIG.vis(d, H.C((u - cue(ci) - dd) / 0.3)); }); }
  };
  const pts = [[600, 1.0], [-300, -0.5], [900, 1.5], [-700, -1.0], [200, 0.5], [-100, 0.0]];
  SCENES['lambda'] = {
    setup() { const c = SIG.chart('lm-ch', { w: 960, h: 560, x: [-1000, 1000], y: [-1.5, 2], xt: [-1000, -500, 0, 500, 1000], yt: [-1, 0, 1, 2], fx: (v) => (v > 0 ? '+' : '') + v, fy: (v) => (v > 0 ? '+' : '') + v + '¢', xl: 'signed volume V, shares (1 s windows)', yl: 'mid change Δp' });
      c.d = pts.map(([x, y]) => c.dot(x, y, 11, x > 0 ? '#4fd18b' : '#ff6b5e'));
      const L = 0.0016111; c.fit = c.line([[-1000, -1000 * L], [1000, 1000 * L]], '#ffb347', 4); },
    draw(u, cue, H) { const c = SIG.chart('lm-ch', {}); c.d.forEach((d, i) => SIG.vis(d, H.C((u - cue(4) - 0.3 - i * 0.35) / 0.3))); SIG.reveal(c.fit, (u - cue(5) - 0.2) / 1.2); }
  };
  const SG = '++++−+++++−−+−−−−+−−−++++++−++++−−−−−+−−'.split('');
  SCENES['lab'] = {
    setup() { const g = H.$('lb-signs'); if (g.children.length) return;
      g.innerHTML = SG.map((x, i) => `<div id="sg${i}" style="position:absolute;left:${i * 42}px;top:0;width:36px;height:56px;border-radius:7px;display:grid;place-items:center;font:700 28px var(--mono);color:#06141a;background:var(--${x === '+' ? 'green' : 'red'})">${x}</div>`).join(''); },
    draw(u, cue, H) { SG.forEach((x, i) => SIG.vis(H.$('sg' + i), H.C((u - cue(1) - i * 0.07) / 0.2))); }
  };
})();
