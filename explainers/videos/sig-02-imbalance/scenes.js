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

// ---- sig-02 imbalance ----
(function () {
  function gauge(id, w) {
    const g = H.$(id); if (!g || g._g) return g && g._g;
    g.innerHTML = `<div style="position:absolute;left:0;top:70px;width:${w}px;height:10px;border-radius:5px;background:linear-gradient(90deg,var(--red),#2c4351 50%,var(--green))"></div>` +
      [-1, -0.5, 0, 0.5, 1].map((v) => `<div class="lbl" style="position:absolute;left:${(v + 1) / 2 * w - 30}px;top:95px;width:60px;text-align:center">${v > 0 ? '+' + v : v}</div>`).join('') +
      `<div class="lbl" style="position:absolute;left:0;top:30px;color:var(--red)">only sellers</div><div class="lbl" style="position:absolute;right:0;top:30px;color:var(--green)">only buyers</div>` +
      `<div class="gn" style="position:absolute;top:45px;width:6px;height:60px;margin-left:-3px;border-radius:3px;background:var(--amber);box-shadow:0 0 14px var(--amber)"></div>` +
      `<div class="gv" style="position:absolute;top:0;width:140px;margin-left:-70px;text-align:center;font:700 30px var(--mono);color:var(--amber)"></div>`;
    g._g = { set(v) { const x = (v + 1) / 2 * w; g.querySelector('.gn').style.left = x + 'px'; const t = g.querySelector('.gv'); t.style.left = x + 'px'; const s = (v >= 0 ? '+' : '') + v.toFixed(2); if (t.textContent !== s) t.textContent = s; } };
    return g._g;
  }
  SCENES['title'] = { setup() { gauge('ti-g', 1100); }, draw(u) { gauge('ti-g', 1100).set(0.55 * Math.sin(u * 0.9) + 0.25 * Math.sin(u * 2.3)); } };
  SCENES['define'] = { setup() { gauge('df-g', 820); }, draw(u, cue, H) {
    const k = H.ease((u - cue(3) - 0.3) / 1.0); const wob = 0.4 * Math.sin(u * 1.1) - 0.1;
    gauge('df-g', 820).set(H.lerp(wob, 0.8, k)); } };
  SCENES['predict'] = {
    setup() { const q = H.$('pr-q'); if (q.children.length) return;
      let s = '<div class="lbl" style="position:absolute;left:0;top:40px;color:var(--red)">ask 50.01</div><div class="lbl" style="position:absolute;left:0;top:200px;color:var(--green)">bid 50.00</div>';
      for (let i = 0; i < 4; i++) s += `<div id="pr-a${i}" style="position:absolute;left:${170 + i * 58}px;top:20px;width:50px;height:70px;border-radius:8px;background:var(--red)"></div>`;
      for (let i = 0; i < 9; i++) s += `<div style="position:absolute;left:${170 + i * 58}px;top:180px;width:50px;height:70px;border-radius:8px;background:var(--green)"></div>`;
      s += '<div id="pr-up" class="tag c-amber" style="position:absolute;left:170px;top:320px;opacity:0">ask queue empty → mid up half a tick</div>';
      s += '<div id="pr-rho" class="lbl" style="position:absolute;left:170px;top:270px">ρ = (9 − 4) / 13 = +0.38</div>';
      q.innerHTML = s; },
    draw(u, cue, H) { const t0 = cue(4) + 0.6; let left = 4;
      for (let i = 3; i >= 0; i--) { const k = H.C((u - t0 - (3 - i) * 0.9) / 0.4); H.$('pr-a' + i).style.opacity = 1 - k; if (k >= 1) left--; }
      H.text('pr-rho', left > 0 ? `ρ = (9 − ${left}) / ${9 + left} = +${((9 - left) / (9 + left)).toFixed(2)}` : 'ρ = +1.00');
      SIG.vis(H.$('pr-up'), H.C((u - t0 - 3.6) / 0.4)); }
  };
  const toy = [[-0.872, 0.017], [-0.703, 0.055], [-0.498, 0.129], [-0.289, 0.248], [-0.099, 0.403], [0.088, 0.585], [0.301, 0.761], [0.502, 0.873], [0.698, 0.944], [0.867, 0.981]];
  const B = 4.008, lg = (x) => 1 / (1 + Math.exp(-B * x));
  SCENES['worked'] = {
    setup() { const c = SIG.chart('wk-ch', { w: 1060, h: 600, x: [-1, 1], y: [0, 1], xt: [-1, -0.5, 0, 0.5, 1], yt: [0, 0.25, 0.5, 0.75, 1], fy: (v) => v.toFixed(2), xl: 'imbalance ρ', yl: 'P(next mid move up)' });
      c.pts = toy.map(([x, y]) => c.dot(x, y, 9, '#3fd0dc'));
      const L = []; for (let i = 0; i <= 80; i++) { const x = -1 + i / 40; L.push([x, lg(x)]); } c.fit = c.line(L, '#ffb347', 5);
      c.m0 = [c.dot(0, 0.5, 11, '#ffb347'), c.text(0.04, 0.46, '0.50', '#ffb347', 'start', 26)];
      c.m5 = [c.dot(0.5, lg(0.5), 11, '#ffb347'), c.text(0.47, 0.92, '0.88', '#ffb347', 'end', 26), c.vline(0.5, '#ffb347', '6 8')]; },
    draw(u, cue, H) { const c = SIG.chart('wk-ch', {});
      c.pts.forEach((p, i) => SIG.vis(p, H.C((u - cue(0) - 0.4 - i * 0.12) / 0.3)));
      SIG.reveal(c.fit, (u - cue(1) - 0.2) / 1.4);
      c.m0.forEach((e) => SIG.vis(e, H.C((u - cue(2) - 0.3) / 0.4))); c.m5.forEach((e) => SIG.vis(e, H.C((u - cue(3) - 0.5) / 0.4))); }
  };
  SCENES['maker'] = {
    setup() { SIG.ladder('mk-lad', { rows: 4, rowH: 80, pw: 170, sw: 260 }); },
    draw(u, cue, H) { const L = SIG.ladder('mk-lad', {}); const hit = u >= cue(3) + 1.0;
      L.set([{ p: '50.02', a: 1200 }, { p: '50.01', a: 1500 }, { p: '50.00', b: hit ? 0 : 300, hl: u >= cue(2) && !hit }, { p: '49.99', b: 800 }], 1600); }
  };
})();
