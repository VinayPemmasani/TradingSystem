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

// ---- sig-09 decay ----
(function () {
  const phi = 0.9, beta = 0.1;
  const ic = (h) => { const cov = beta * (1 - Math.pow(phi, h)) / (1 - phi); let vs = 0; for (let j = 0; j < h; j++) for (let k = 0; k < h; k++) vs += Math.pow(phi, Math.abs(j - k)); return cov / Math.sqrt(h + beta * beta * vs); };
  const IC = []; for (let h = 1; h <= 60; h++) IC.push([h, ic(h)]);
  SCENES['title'] = {
    setup() { const c = SIG.chart('ti-ch', { w: 1100, h: 260, x: [0, 60], y: [0, 0.22], pad: { l: 10, b: 10, t: 10 } }); c.l = c.line(IC, '#ffb347', 5); },
    draw(u, cue) { SIG.reveal(SIG.chart('ti-ch', {}).l, (u - cue(1)) / 3); }
  };
  SCENES['ic'] = {
    setup() { const c = SIG.chart('ic-ch', { w: 1700, h: 360, x: [0, 60], y: [0, 1.05], xt: [0, 10, 20, 30, 40, 50, 60], yt: [0, 0.5, 1], fy: (v) => v.toFixed(1), xl: 'horizon h (steps)', yl: 'scaled to 1' });
      const M = [], N = []; for (let h = 0; h <= 60; h++) { M.push([h, 1 - Math.pow(phi, h)]); N.push([h, Math.sqrt(h / 60)]); }
      c.m = c.line(M, '#ffb347', 5); c.n = c.line(N, '#ff8fc8', 4); },
    draw(u, cue) { const c = SIG.chart('ic-ch', {}); SIG.reveal(c.m, (u - cue(4) - 0.2) / 1.2); SIG.reveal(c.n, (u - cue(4) - 1.6) / 1.2); }
  };
  SCENES['worked'] = {
    setup() { const c = SIG.chart('wk-ch', { w: 960, h: 560, x: [0, 60], y: [0, 0.25], xt: [1, 10, 20, 30, 40, 50, 60], yt: [0, 0.05, 0.1, 0.15, 0.2, 0.25], fy: (v) => v.toFixed(2), xl: 'horizon h (steps)', yl: 'IC(h)' });
      c.l = c.line(IC, '#ffb347', 5);
      c.p = [[1, '0.10'], [11, '0.20'], [50, '0.13']].map(([h, t]) => [c.dot(h, ic(h), 10, '#ffb347'), c.text(h + 1.2, ic(h) + 0.012, t + (h === 11 ? ' peak' : ''), '#ffb347', 'start', 24)]); },
    draw(u, cue, H) { const c = SIG.chart('wk-ch', {}); SIG.reveal(c.l, (u - cue(2) - 0.2) / 2.5);
      const at = [cue(2) + 0.4, cue(3) + 0.3, cue(3) + 1.6]; c.p.forEach((p, i) => p.forEach((e) => SIG.vis(e, H.C((u - at[i]) / 0.4)))); }
  };
  SCENES['latency'] = {
    setup() { const c = SIG.chart('lt-ch', { w: 1100, h: 560, x: [0, 30], y: [0, 1.05], xt: [0, 2, 10, 20, 30], yt: [0, 0.19, 0.5, 1], fy: (v) => Math.round(v * 100) + '%', xl: 'steps after the signal', yl: 'share of the predicted move done' });
      const M = []; for (let h = 0; h <= 30; h += 0.25) M.push([h, 1 - Math.pow(phi, h)]);
      c.sh = c.svg.insertBefore(SIG.el('rect', { x: c.X(0), y: c.Y(1.05), width: c.X(2) - c.X(0), height: c.Y(0) - c.Y(1.05), fill: 'rgba(255,143,200,.16)' }), c.svg.firstChild);
      c.l = c.line(M, '#ffb347', 5); c.t = c.text(1, 0.9, 'latency', '#ff8fc8', 'middle', 22); },
    draw(u, cue, H) { const c = SIG.chart('lt-ch', {}); SIG.reveal(c.l, (u - cue(0) - 0.5) / 2); SIG.vis(c.sh, H.C((u - cue(1)) / 0.5)); SIG.vis(c.t, H.C((u - cue(1)) / 0.5)); }
  };
  SCENES['markout'] = {
    setup() { const c = SIG.chart('mk-ch', { w: 740, h: 560, x: [-0.5, 4.5], y: [-0.7, 0.7], yt: [-0.5, 0, 0.5], fy: (v) => (v > 0 ? '+' : '') + v + '¢', xt: [0, 1, 2, 3, 4], fx: (v) => ['fill', '1 ms', '10 ms', '100 ms', '1 s'][v], yl: 'per share, buy at 50.00' });
      c.z = c.hline(0, '#5b6f7c', '4 6'); const V = [0.5, 0.4, 0.3, -0.2, -0.5];
      c.l = c.line(V.map((v, i) => [i, v]), '#ffb347', 4); c.d = V.map((v, i) => [c.dot(i, v, 10, v >= 0 ? '#4fd18b' : '#ff6b5e'), c.text(i, v + (v >= 0 ? 0.08 : -0.13), (v > 0 ? '+' : '') + v.toFixed(1), v >= 0 ? '#4fd18b' : '#ff6b5e', 'middle', 22)]); },
    draw(u, cue, H) { const c = SIG.chart('mk-ch', {}); const at = [cue(2) + 0.5, cue(3), cue(3) + 0.3, cue(3) + 1.5, cue(3) + 2.2];
      c.d.forEach((d, i) => d.forEach((e) => SIG.vis(e, H.C((u - at[i]) / 0.4)))); SIG.reveal(c.l, (u - cue(3)) / 3); }
  };
  SCENES['match'] = {
    setup() { const g = H.$('mt-ax'); if (g.children.length) return;
      const ticks = [['1 ms', 0], ['1 s', 0.27], ['5 min', 0.5], ['1 day', 0.75]];
      let h = '<div style="position:absolute;left:0;top:100px;width:1700px;height:4px;background:#2c4351"></div>';
      ticks.forEach(([t, x]) => { h += `<div class="lbl" style="position:absolute;left:${x * 1700}px;top:115px">${t}</div><div style="position:absolute;left:${x * 1700}px;top:90px;width:3px;height:24px;background:#8ea3b1"></div>`; });
      h += '<div id="mt-a" class="chip" style="position:absolute;left:0;top:30px;width:470px;background:var(--amber)">market maker: ms to s</div>';
      h += '<div id="mt-b" class="chip" style="position:absolute;left:820px;top:30px;background:var(--violet)">pairs: 5-min samples</div>';
      h += '<div id="mt-c" class="chip" style="position:absolute;left:1260px;top:30px;background:var(--blue)">trend: daily closes</div>';
      g.innerHTML = h; },
    draw(u, cue, H) { SIG.vis(H.$('mt-a'), H.C((u - cue(1)) / 0.4)); SIG.vis(H.$('mt-b'), H.C((u - cue(2)) / 0.4)); SIG.vis(H.$('mt-c'), H.C((u - cue(2) - 1.2) / 0.4)); }
  };
})();
