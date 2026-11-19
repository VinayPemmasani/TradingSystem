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


// ---- ms-04 toxicity ----
(function () {
  const Z = (x) => { const t = 1 / (1 + 0.2316419 * Math.abs(x)); const d = 0.3989423 * Math.exp(-x * x / 2);
    const p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return x > 0 ? 1 - p : p; };
  let seed = 5; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
  // per-minute volumes: quiet, then busy
  const VOL = []; for (let i = 0; i < 40; i++) VOL.push((i > 24 && i < 34 ? 3.2 : 1) * (0.5 + rnd()));
  SCENES['title'] = {
    setup() { const c = MS.chart('ti-ch', { w: 1200, h: 220, x: [0, 40], y: [-1, 1], pad: { l: 10, b: 10, t: 10 } });
      c.b = []; for (let i = 0; i < 40; i++) { const f = i > 26 && i < 34 ? 0.85 : 0.5 + (rnd() - 0.5) * 0.3; c.b.push([c.bar(i + 0.5, 0, f, 20, '#4fd18b'), c.bar(i + 0.5, 0, -(1 - f), 20, '#ff6b5e')]); } },
    draw(u, cue, H) { const c = MS.chart('ti-ch', {}); c.b.forEach((b, i) => b.forEach((e) => MS.vis(e, H.C((u - cue(1) - i * 0.06) / 0.2)))); }
  };
  SCENES['define'] = { draw(u, cue, H) { const k = H.C((u - cue(1)) / 6); H.text('df-pnl', '−$' + Math.round(k * k * 4200).toLocaleString('en-US')); } };
  SCENES['clock'] = {
    setup() { const c = MS.chart('cl-ch', { w: 1100, h: 420, x: [0, 40], y: [0, 4], xt: [0, 10, 20, 30, 40], yt: [], xl: 'minutes', yl: 'volume per minute', pad: { l: 30 } });
      c.b = VOL.map((v, i) => c.bar(i + 0.5, 0, v, 20, '#6f8796'));
      const tot = VOL.reduce((a, b) => a + b, 0), B = tot / 12; c.lines = []; let acc = 0, k = 1;
      VOL.forEach((v, i) => { acc += v; while (acc >= k * B) { const x = i + 1 - (acc - k * B) / v; c.lines.push(c.vline(x, '#ffb347', '0')); k++; } }); },
    draw(u, cue, H) { const c = MS.chart('cl-ch', {}); c.b.forEach((b, i) => MS.vis(b, H.C((u - cue(0) - 0.3 - i * 0.03) / 0.2)));
      c.lines.forEach((l, i) => MS.vis(l, H.C((u - cue(1) - 0.3 - i * 0.12) / 0.2))); }
  };
  const zsetup = () => { const c = MS.chart('cl-z', { w: 540, h: 300, x: [-3, 3], y: [0, 1], xt: [-2, 0, 2], yt: [0, 0.5, 1], fy: (v) => (v * 100) + '%', xl: 'ΔP / σ', yl: 'buy share', pad: { l: 80 } });
    const P = []; for (let i = 0; i <= 60; i++) { const x = -3 + i / 10; P.push([x, Z(x)]); } c.z = c.line(P, '#4fd18b', 5); c.d = c.dot(1, Z(1), 9, '#ffb347'); c.t = c.text(1.15, 0.78, '+1σ → 84%', '#ffb347', 'start', 20); return c; };
  const base = SCENES['clock'];
  SCENES['clock'] = { setup() { base.setup(); zsetup(); }, draw(u, cue, H) { base.draw(u, cue, H); const c = MS.chart('cl-z', {}); MS.reveal(c.z, (u - cue(4) - 0.3) / 1); MS.vis(c.d, H.C((u - cue(4) - 1.3) / 0.3)); MS.vis(c.t, H.C((u - cue(4) - 1.3) / 0.3)); } };
  const F = [0.55, 0.48, 0.62, 0.90, 0.85];
  SCENES['worked'] = {
    setup() { const c = MS.chart('wk-b', { w: 1100, h: 380, x: [0, 5], y: [0, 1], xt: [], yt: [0, 0.5, 1], fy: (v) => (v * 100) + '%', pad: { l: 80, b: 40 } });
      c.g = F.map((f, i) => c.bar(i + 0.5, 0, f, 120, '#4fd18b')); c.r = F.map((f, i) => c.bar(i + 0.5, f, 1, 120, '#ff6b5e'));
      c.bt = F.map((f, i) => c.text(i + 0.5, f / 2, Math.round(f * 100) + '% buy', '#06141a', 'middle', 22));
      c.gt = F.map((f, i) => c.text(i + 0.5, 1.04, 'gap ' + Math.abs(2 * f - 1).toFixed(2), '#ffb347', 'middle', 24)); },
    draw(u, cue, H) { const c = MS.chart('wk-b', {}); for (let i = 0; i < 5; i++) { const k = H.C((u - cue(2) - 0.3 - i * 0.2) / 0.3);
      MS.vis(c.g[i], k); MS.vis(c.r[i], k); MS.vis(c.bt[i], H.C((u - cue(4) - i * 0.3) / 0.3)); MS.vis(c.gt[i], H.C((u - cue(4) - 0.6 - i * 0.4) / 0.3)); } }
  };
  const PNL = [['makers', 1000, '#3fd0dc'], ['noise', -370, '#8ea3b1'], ['momentum', -790, '#ff8fc8'], ['value', 160, '#a98bff']];
  SCENES['lab'] = {
    setup() { const c = MS.chart('lb-ch', { w: 1100, h: 480, x: [0, 4], y: [-1000, 1200], xt: [], yt: [-800, -400, 0, 400, 800, 1200], fy: (v) => '$' + v, pad: { l: 110, b: 40 } });
      c.bs = PNL.map((p, i) => c.bar(i + 0.5, 0, p[1], 160, p[2])); c.ts = PNL.map((p, i) => c.text(i + 0.5, p[1] > 0 ? p[1] + 60 : p[1] - 110, p[0] + ' ' + (p[1] > 0 ? '+' : '−') + '$' + Math.abs(p[1]), p[2], 'middle', 24)); },
    draw(u, cue, H) { const c = MS.chart('lb-ch', {}); const at = [cue(1) + 0.6, cue(2), cue(2) + 0.4, cue(3)];
      at.forEach((t, i) => { MS.vis(c.bs[i], H.C((u - t) / 0.4)); MS.vis(c.ts[i], H.C((u - t - 0.2) / 0.4)); }); }
  };
})();
