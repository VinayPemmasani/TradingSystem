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

// ---- sig-04 online features ----
(function () {
  let s = 3; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const P = [], E = []; let p = 50, m = 50; for (let i = 0; i < 120; i++) { p += (rnd() - 0.48) * 0.02; m += 0.1 * (p - m); P.push([i, p]); E.push([i, m]); }
  SCENES['title'] = {
    setup() { const c = SIG.chart('ti-ch', { w: 820, h: 260, x: [0, 120], y: [Math.min(...P.map((q) => q[1])) - 0.02, Math.max(...P.map((q) => q[1])) + 0.02], pad: { l: 10, b: 10, t: 10 } });
      c.p = c.line(P, '#3fd0dc', 3); c.e = c.line(E, '#ffb347', 5); },
    draw(u, cue) { const c = SIG.chart('ti-ch', {}); SIG.reveal(c.p, (u - 1) / 8); SIG.reveal(c.e, (u - 1.3) / 8); }
  };
  SCENES['ewma'] = {
    setup() { const c = SIG.chart('ew-ch', { w: 920, h: 400, x: [-0.6, 12.6], y: [0, 0.32], xt: [0, 2, 4, 6, 8, 10, 12], yt: [0, 0.1, 0.2, 0.3], fy: (v) => v.toFixed(1), xl: 'updates ago k' });
      c.b = []; for (let k = 0; k <= 12; k++) c.b.push(c.bar(k, 0, 0.3 * Math.pow(0.7, k), 46, '#ffb347'));
      c.h = c.vline(1.943, '#a98bff', '8 8'); c.ht = c.text(2.1, 0.29, 'h = 1.94', '#a98bff', 'start', 24); },
    draw(u, cue, H) { const c = SIG.chart('ew-ch', {}); c.b.forEach((b, k) => SIG.vis(b, H.C((u - cue(2) - 0.2 - k * 0.08) / 0.3))); SIG.vis(c.h, H.C((u - cue(2) - 1.6) / 0.4)); SIG.vis(c.ht, H.C((u - cue(2) - 1.6) / 0.4)); }
  };
  const ticks = [0.05, 0.12, 0.2, 0.31, 0.33, 0.335, 0.338, 0.341, 0.344, 0.347, 0.35, 0.353, 0.356, 0.36, 0.52, 0.66, 0.8, 0.93];
  SCENES['time'] = {
    setup() { const t = H.$('tm-ticks'); if (t.children.length) return;
      let h = '<div style="position:absolute;left:0;top:60px;width:1700px;height:3px;background:#2c4351"></div>';
      ticks.forEach((x, i) => { h += `<div id="tk${i}" style="position:absolute;left:${x * 1700}px;top:30px;width:4px;height:60px;background:var(--teal)"></div>`; });
      h += '<div id="tk-b" class="tag c-pink" style="position:absolute;left:470px;top:-20px">burst: 10 messages in a microsecond</div>'; t.innerHTML = h;
      const c = SIG.chart('tm-ch', { w: 840, h: 400, x: [0, 4], y: [0, 1], xt: [0, 1, 2, 3, 4], yt: [0, 0.5, 1], fx: (v) => v + ' s', xl: 'age of a value', yl: 'its weight now' });
      const L = []; for (let i = 0; i <= 80; i++) { const x = i / 20; L.push([x, Math.exp(-x / 1.4427)]); } c.w = c.line(L, '#ffb347', 5);
      c.hh = [c.hline(0.5, '#a98bff', '6 8'), c.vline(1, '#a98bff', '6 8'), c.text(1.08, 0.56, 'half-life 1 s', '#a98bff', 'start', 22)]; },
    draw(u, cue, H) { ticks.forEach((x, i) => SIG.vis(H.$('tk' + i), H.C((u - cue(0) - 0.3 - x * 3) / 0.15))); SIG.vis(H.$('tk-b'), H.C((u - cue(0) - 2) / 0.4));
      const c = SIG.chart('tm-ch', {}); SIG.reveal(c.w, (u - cue(2) - 0.2) / 1.2); c.hh.forEach((e) => SIG.vis(e, H.C((u - cue(2) - 1.2) / 0.4))); }
  };
  SCENES['vwap'] = {
    setup() { const c = SIG.chart('vw-ch', { w: 900, h: 520, x: [0, 4], y: [49.99, 50.06], yt: [50.00, 50.02, 50.04, 50.06], fy: (v) => v.toFixed(2), xl: 'time' });
      c.t = [[0.6, 50.00, 300], [1.4, 50.04, 100], [2.2, 50.02, 600]].map(([x, y, q]) => c.dot(x, y, 6 + Math.sqrt(q) * 0.7, '#3fd0dc'));
      c.v = c.step([[0.6, 50.0], [1.4, 50.01], [2.2, 50.016], [4, 50.016]], '#3fd0dc', 3);
      c.vt = c.text(3.95, 50.0115, 'VWAP 50.016', '#3fd0dc', 'end', 24);
      c.m = c.hline(50.05, '#ffb347', '10 8'); c.mt = c.text(3.95, 50.054, 'mid 50.05', '#ffb347', 'end', 24); },
    draw(u, cue, H) { const c = SIG.chart('vw-ch', {}); c.t.forEach((d, i) => SIG.vis(d, H.C((u - cue(2) - 0.2 - i * 0.8) / 0.3)));
      SIG.reveal(c.v, (u - cue(2) - 0.2) / 2.6); SIG.vis(c.vt, H.C((u - cue(2) - 2.6) / 0.4)); SIG.vis(c.m, H.C((u - cue(3)) / 0.4)); SIG.vis(c.mt, H.C((u - cue(3)) / 0.4)); }
  };
})();
