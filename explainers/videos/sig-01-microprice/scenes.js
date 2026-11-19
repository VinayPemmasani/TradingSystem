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

// ---- sig-01 microprice ----
(function () {
  const yP = (p) => 290 + ((50.03 - p) / 0.01 + 0.5) * 80;
  SCENES['flaw'] = {
    setup() { SIG.ladder('fl-lad', { rows: 5, rowH: 80, pw: 170, sw: 260 }); },
    draw(u, cue, H) {
      const L = SIG.ladder('fl-lad', {}); const after = u >= cue(2);
      L.set([{ p: '50.03', a: 1500 }, { p: '50.02', a: 2700 }, { p: '50.01', a: after ? 0 : 100, hl: after && u < cue(3) }, { p: '50.00', b: 900 }, { p: '49.99', b: 1200 }], 3000);
      const k = H.ease((u - cue(2) - 0.4) / 0.8);
      const mid = H.lerp(50.005, 50.01, k), mw = H.lerp(50.009, 50.005, k);
      const pm = H.C((u - cue(0) - 0.8) / 0.5), pw = H.C((u - cue(1) - 0.3) / 0.5);
      for (const [id, y, p] of [['fl-lmid', yP(mid), pm], ['fl-mid', yP(mid) - 20, pm], ['fl-lmw', yP(mw), pw], ['fl-mw', yP(mw) - 20, pw]]) {
        const e = H.$(id); e.style.top = y + 'px'; e.style.opacity = p; }
      // keep labels apart
      const a = yP(mid), b = yP(mw); if (Math.abs(a - b) < 40) { const lo = Math.min(a, b) - 20 - 22, hi = Math.max(a, b) - 20 + 22; H.$(a < b ? 'fl-mid' : 'fl-mw').style.top = lo + 'px'; H.$(a < b ? 'fl-mw' : 'fl-mid').style.top = hi + 'px'; }
    }
  };
  SCENES['define'] = {
    setup() {
      const c = SIG.chart('df-ch', { w: 1000, h: 420, x: [0, 10], y: [49.995, 50.02], yt: [50.00, 50.005, 50.01, 50.015], fy: (v) => v.toFixed(3), xl: 'time →', pad: { l: 110 } });
      c.path = c.step([[0, 50.005], [3, 50.005], [3, 50.01], [5.5, 50.01], [5.5, 50.005], [8, 50.005], [8, 50.01], [10, 50.01]], '#3fd0dc', 4);
      c.v = [3, 5.5, 8].map((x, i) => { const l = c.vline(x, '#8ea3b1', '4 8'); const t = c.text(x, 50.0185, 'τ' + '₁₂₃'[i], '#8ea3b1', 'middle', 24); return [l, t]; });
      c.d = [[3, 50.0080], [5.5, 50.0086], [8, 50.0088]].map(([x, y]) => c.dot(x, y, 9, '#ffb347'));
      c.lim = c.hline(50.0088, '#ffb347', '10 8'); c.limt = c.text(9.9, 50.0074, 'P micro', '#ffb347', 'end', 24);
      c.ill = c.text(0.1, 49.9965, 'illustrative', '#6f8796', 'start', 18);
    },
    draw(u, cue, H) {
      const c = SIG.chart('df-ch', {});
      SIG.reveal(c.path, (u - cue(0) - 0.3) / 2.5);
      c.v.forEach((v, i) => { const p = H.C((u - cue(Math.min(i, 2)) - 0.3 - (i == 2 ? 1.2 : 0)) / 0.4); SIG.vis(v[0], p); SIG.vis(v[1], p); });
      c.d.forEach((d, i) => SIG.vis(d, H.C((u - cue(i + 1) - (i == 2 ? 0 : 0.5)) / 0.4)));
      SIG.vis(c.lim, H.C((u - cue(3) - 0.4) / 0.5)); SIG.vis(c.limt, H.C((u - cue(3) - 0.4) / 0.5)); SIG.vis(c.ill, H.C((u - cue(1)) / 0.5));
    }
  };
  SCENES['estimate'] = {
    setup() {
      const g = H.$('es-grid'); if (g.children.length) return;
      for (let r = 0; r < 2; r++) {
        const lab = document.createElement('div'); lab.className = 'lbl'; lab.style.cssText = `position:absolute;left:-180px;top:${r * 140 + 34}px`; lab.textContent = r ? 'S = 2 ticks' : 'S = 1 tick'; g.appendChild(lab);
        for (let i = 0; i < 5; i++) { const d = document.createElement('div'); d.className = 'node'; d.id = `es-c${r}${i}`;
          d.style.cssText = `position:absolute;left:${i * 180}px;top:${r * 140}px;width:160px;height:100px;padding:10px;border-color:var(--violet)`;
          d.innerHTML = `<div class="t" style="font-size:24px">${(i * 0.2).toFixed(1)}–${(i * 0.2 + 0.2).toFixed(1)}</div><div class="s">state</div>`; g.appendChild(d); }
      }
    },
    draw(u, cue, H) {
      for (let r = 0; r < 2; r++) for (let i = 0; i < 5; i++) { const d = H.$(`es-c${r}${i}`); const on = u >= cue(4) && u < cue(5) && (i === 0 || i === 4); d.classList.toggle('hl', on); }
    }
  };
  const toy = [[0.064, -0.483], [0.149, -0.445], [0.251, -0.371], [0.351, -0.259], [0.447, -0.103], [0.544, 0.085], [0.651, 0.261], [0.747, 0.371], [0.844, 0.44], [0.933, 0.481]];
  SCENES['toy'] = {
    setup() {
      const c = SIG.chart('ty-ch', { w: 1040, h: 580, x: [0, 1], y: [-0.55, 0.55], xt: [0, 0.25, 0.5, 0.75, 1], yt: [-0.5, -0.25, 0, 0.25, 0.5], fy: (v) => (v > 0 ? '+' : '') + v.toFixed(2), xl: 'imbalance I', yl: 'adjustment, ticks' });
      c.wm = c.line([[0, -0.5], [1, 0.5]], '#a98bff', 4);
      c.g = c.line(toy, '#ffb347', 6);
      c.top = [c.dot(0.877, 0.455, 10, '#ffb347'), c.dot(0.877, 0.377, 10, '#a98bff'), c.text(0.86, 0.50, '+0.46', '#ffb347', 'end', 26), c.text(0.92, 0.27, '+0.38', '#a98bff', 'start', 26)];
      c.q = [0.305, 0.35, 0.401].map((y) => [c.dot(0.75, y, 8, '#3fd0dc'), null]);
      const q = H.$('ty-q'); if (q.children.length) return;
      q.innerHTML = '<div class="lbl" style="position:absolute;left:0;top:10px">bid queue</div><div id="ty-b" style="position:absolute;left:150px;top:0;height:50px;border-radius:6px;background:var(--green)"></div>' +
        '<div class="lbl" style="position:absolute;left:0;top:90px">ask queue</div><div id="ty-a" style="position:absolute;left:150px;top:80px;height:50px;border-radius:6px;background:var(--red)"></div>';
    },
    draw(u, cue, H) {
      const c = SIG.chart('ty-ch', {});
      SIG.reveal(c.wm, (u - cue(2) - 0.6) / 1.0); SIG.reveal(c.g, (u - cue(2) - 0.2) / 1.6);
      c.top.forEach((e) => SIG.vis(e, H.C((u - cue(3) - 0.5) / 0.5)));
      c.q.forEach((p, i) => { const k = H.C((u - cue(5) - 0.3 - i * 0.6) / 0.4); SIG.vis(p[0], k); SIG.vis(p[1], k); });
      const t = u * 2.2, b = 9 + Math.round(5 * Math.sin(t) + 2 * Math.sin(2.7 * t)), a = 6 + Math.round(4 * Math.sin(1.3 * t + 1) + 2 * Math.sin(3.1 * t));
      H.$('ty-b').style.width = (b * 22) + 'px'; H.$('ty-a').style.width = (Math.max(1, a) * 22) + 'px';
    }
  };
})();
