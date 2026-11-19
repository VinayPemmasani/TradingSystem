// Custom animation for the VWAP explainer. Everything is computed from u (stateless).
function mkdiv(H, hostScene, id, cls, css, txt) {
  const d = document.createElement('div'); d.id = id; d.className = cls; if (txt !== undefined) d.textContent = txt;
  Object.assign(d.style, css); H.$(hostScene).appendChild(d); return d;
}

// ---- naive: deque of 6 trades, a scan box sweeps over all of them on every trade
SCENES['naive'] = {
  setup(H) {
    for (let i = 0; i < 6; i++) mkdiv(H, 's-naive', 'nv-t' + i, 'tbox', { left: (1100 + i * 116) + 'px', top: '260px', opacity: 0 }, String(i + 1));
  },
  draw(u, cue, H) {
    for (let i = 0; i < 6; i++) H.$('nv-t' + i).style.opacity = H.P(u, cue(0) + 0.8 + i * 0.1, 0.4);
    const t0 = cue(1) + 2.0;
    const s = H.$('nv-scan');
    if (u < t0) { s.style.opacity = 0; H.text('nv-cnt', '0'); return; }
    const per = 0.18, k = Math.floor((u - t0) / per);
    s.style.opacity = 1;
    s.style.left = (1100 + (k % 6) * 116 - 4) + 'px';
    H.text('nv-cnt', (k + 1).toLocaleString('en-US'));
  }
};

// ---- sums: a 3 s window slides over a timeline of trades
const TR = { t: [0.4, 1.1, 1.9, 2.6, 3.4, 4.0, 4.9, 5.5, 6.3, 7.2, 7.8, 8.6, 9.3],
  q: [200, 100, 300, 100, 200, 400, 100, 300, 200, 100, 300, 200, 100],
  c: [10002, 10004, 10001, 10003, 10005, 10006, 10004, 10007, 10008, 10006, 10009, 10010, 10008] };  // cents
const SM = { x0: 120, sx: 160, base: 520, W: 3 };
SCENES['sums'] = {
  setup(H) {
    mkdiv(H, 's-sums', 'sm-axis', '', { left: SM.x0 + 'px', top: SM.base + 'px', width: (10 * SM.sx + 40) + 'px', height: '3px', background: 'var(--line)', opacity: 0 });
    mkdiv(H, 's-sums', 'sm-win', '', { left: '0px', top: '250px', width: (SM.W * SM.sx) + 'px', height: (SM.base - 250) + 'px', border: '3px solid var(--amber)', borderRadius: '10px', background: 'rgba(255,179,71,.08)', opacity: 0 });
    mkdiv(H, 's-sums', 'sm-wl', 'lbl', { left: '0px', top: '215px', color: 'var(--amber)', opacity: 0 }, 'window 3 s');
    TR.t.forEach((t, i) => {
      mkdiv(H, 's-sums', 'sm-b' + i, 'bar', { left: (SM.x0 + t * SM.sx - 14) + 'px', top: (SM.base - TR.q[i] * 0.5) + 'px', width: '28px', height: (TR.q[i] * 0.5) + 'px', background: 'var(--teal)', opacity: 0 });
      mkdiv(H, 's-sums', 'sm-l' + i, 'lbl', { left: (SM.x0 + t * SM.sx - 40) + 'px', top: (SM.base - TR.q[i] * 0.5 - 30) + 'px', width: '80px', textAlign: 'center', fontSize: '17px', opacity: 0 }, (TR.c[i] / 100).toFixed(2));
    });
  },
  draw(u, cue, H) {
    H.$('sm-axis').style.opacity = H.P(u, cue(0), 0.5);
    // "now" moves from 3.5 s to 9.6 s between cue 1 and the end of cue 3
    const a = cue(1), b = cue(4) - 0.2;
    const now = u < a ? 3.5 : 3.5 + (9.6 - 3.5) * H.C((u - a) / (b - a));
    const lo = now - SM.W;
    const vis = H.P(u, cue(0) + 0.3, 0.5);
    let pq = 0, q = 0;
    TR.t.forEach((t, i) => {
      const inWin = t <= now && t > lo, future = t > now;
      const bar = H.$('sm-b' + i), lab = H.$('sm-l' + i);
      bar.style.opacity = future ? 0 : vis * (inWin ? 1 : 0.25);
      bar.style.background = inWin ? 'var(--teal)' : 'var(--muted)';
      lab.style.opacity = future ? 0 : vis * (inWin ? 1 : 0.3);
      if (inWin) { pq += TR.c[i] * TR.q[i]; q += TR.q[i]; }
    });
    const w = H.$('sm-win'); w.style.left = (SM.x0 + lo * SM.sx) + 'px'; w.style.opacity = vis;
    const wl = H.$('sm-wl'); wl.style.left = (SM.x0 + lo * SM.sx) + 'px'; wl.style.opacity = vis;
    H.text('sm-pq', (pq / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
    H.text('sm-q', q.toLocaleString('en-US'));
    // VWAP in Price(4): pq is in cents*shares -> *100 for Price(4)*shares; round half up
    H.text('sm-v', q ? (Math.floor((pq * 100 + Math.floor(q / 2)) / q) / 10000).toFixed(4) : '–');
  }
};

// ---- ring: 8 slots in a circle; pushes and pops advance over the scene
const RG = { cx: 1500, cy: 470, r: 250 };
SCENES['ring'] = {
  setup(H) {
    for (let k = 0; k < 8; k++) {
      const a = -Math.PI / 2 + k * Math.PI / 4;
      mkdiv(H, 's-ring', 'rg-s' + k, 'rslot', { left: (RG.cx + RG.r * Math.cos(a) - 60) + 'px', top: (RG.cy + RG.r * Math.sin(a) - 36) + 'px', opacity: 0 }, '');
      mkdiv(H, 's-ring', 'rg-i' + k, 'lbl', { left: (RG.cx + (RG.r - 115) * Math.cos(a) - 20) + 'px', top: (RG.cy + (RG.r - 115) * Math.sin(a) - 12) + 'px', width: '40px', textAlign: 'center', opacity: 0 }, String(k));
    }
    mkdiv(H, 's-ring', 'rg-hp', 'tag', { left: '0px', top: '0px', color: 'var(--red)', opacity: 0 }, 'head');
    mkdiv(H, 's-ring', 'rg-tp', 'tag', { left: '0px', top: '0px', color: 'var(--teal)', opacity: 0 }, 'tail');
  },
  draw(u, cue, H) {
    const v = H.P(u, cue(0) + 0.5, 0.5);
    // before cue 3: pushes only (3 -> 7). From cue 3: pops and pushes. From cue 4: full, head frozen.
    const cap = 8;
    let tail = 3, head = 0;
    if (u >= cue(1)) tail = 3 + Math.min(4, Math.floor((u - cue(1)) / 0.55) + 1);
    if (u >= cue(3)) {
      const uu = Math.min(u, cue(4));
      head = Math.floor((uu - cue(3)) / 0.8) + 1;
      tail = Math.min(7 + Math.floor((uu - cue(3)) / 0.6) + 1, head + cap - 1);
    }
    if (u >= cue(4) + 0.5) tail = head + cap;
    for (let k = 0; k < 8; k++) {
      const s = H.$('rg-s' + k);
      s.style.opacity = v; H.$('rg-i' + k).style.opacity = v;
      // newest trade index i in [head, tail) with i & 7 == k
      let i = tail - 1 - ((tail - 1 - k) % 8 + 8) % 8;
      const live = i >= head && i < tail;
      H.text(s, live ? 'T' + i : '');
      s.style.borderColor = live ? 'var(--teal)' : 'var(--line)';
      s.style.color = live ? 'var(--teal)' : 'var(--muted)';
      s.style.background = (live && tail - head === cap) ? '#1d2a33' : 'var(--panel)';
    }
    const pos = (k, rr) => { const a = -Math.PI / 2 + (k & 7) * Math.PI / 4; return [RG.cx + rr * Math.cos(a), RG.cy + rr * Math.sin(a)]; };
    const [hx, hy] = pos(head, RG.r + 105), [tx, ty] = pos(tail, RG.r + 105);
    const hp = H.$('rg-hp'), tp = H.$('rg-tp');
    hp.style.left = (hx - 34) + 'px'; hp.style.top = (hy - 18) + 'px'; hp.style.opacity = H.P(u, cue(2), 0.4);
    tp.style.left = (tx - 30) + 'px'; tp.style.top = (ty - 18 + (head % 8 === tail % 8 ? 34 : 0)) + 'px'; tp.style.opacity = H.P(u, cue(2), 0.4);
    H.text('rg-h', String(head)); H.text('rg-t', String(tail));
  }
};

// ---- maxmin: prices one per second, window 4 s, monotonic max deque recomputed from scratch
const MM = [50, 70, 70, 60, 65, 55, 80, 62, 58, 61];
SCENES['maxmin'] = {
  setup(H) {
    MM.forEach((p, i) => {
      mkdiv(H, 's-maxmin', 'mm-t' + i, 'tbox', { left: (100 + i * 112) + 'px', top: '255px', opacity: 0 }, String(p));
      mkdiv(H, 's-maxmin', 'mm-s' + i, 'lbl', { left: (100 + i * 112) + 'px', top: '330px', width: '96px', textAlign: 'center', opacity: 0 }, 't=' + i);
    });
    for (let j = 0; j < 4; j++) mkdiv(H, 's-maxmin', 'mm-q' + j, 'tbox', { left: (100 + j * 112) + 'px', top: '440px', borderColor: 'var(--green)', color: 'var(--green)', opacity: 0 }, '');
  },
  draw(u, cue, H) {
    const a = cue(1), b = cue(4) - 0.3;
    const step = u < a ? -1 : Math.min(MM.length - 1, Math.floor((u - a) / ((b - a) / MM.length)));
    const W = 4;
    const dq = [];
    for (let k = 0; k <= step; k++) {
      while (dq.length && dq[dq.length - 1][1] <= MM[k]) dq.pop();
      dq.push([k, MM[k]]);
      while (dq.length && dq[0][0] <= k - W) dq.shift();
    }
    MM.forEach((p, i) => {
      const e = H.$('mm-t' + i), s = H.$('mm-s' + i);
      const shown = i <= Math.max(step, 2);
      const inWin = step >= 0 ? (i <= step && i > step - W) : i <= 2;
      e.style.opacity = shown ? H.P(u, cue(0) + 0.4 + i * 0.1, 0.4) * (inWin ? 1 : 0.3) : 0;
      s.style.opacity = e.style.opacity;
      e.style.borderColor = inWin ? 'var(--teal)' : 'var(--line)';
    });
    for (let j = 0; j < 4; j++) {
      const q = H.$('mm-q' + j);
      if (j < dq.length) { q.style.opacity = 1; H.text(q, String(dq[j][1])); q.style.background = j === 0 ? '#16352a' : 'var(--panel)'; }
      else q.style.opacity = 0;
    }
    H.text('mm-hi', dq.length ? String(dq[0][1]) : '–');
  }
};

// ---- bench: log-scale bars, [label, low, high, colour, cue, delay]
const BV = [['ring · 1k in window', 73, 125, 'var(--teal)', 3, 0.0], ['deque · 1k in window', 2971, 4152, 'var(--red)', 1, 0.8],
  ['ring · 10k in window', 79, 109, 'var(--teal)', 3, 0.4], ['deque · 10k in window', 25637, 36191, 'var(--red)', 2, 0.2]];
SCENES['bench'] = {
  setup(H) {
    const X = 450;
    BV.forEach(([n, lo, hi, c], i) => {
      const y = 340 + i * 95;
      const w = (v) => 300 * Math.log10(v / 10);
      mkdiv(H, 's-bench', 'bv-l' + i, 'barl', { left: (X - 360) + 'px', top: (y + 8) + 'px', width: '340px', color: c, opacity: 0, fontSize: '24px' }, n);
      mkdiv(H, 's-bench', 'bv-r' + i, 'bar', { left: X + 'px', top: y + 'px', height: '50px', width: '0px', background: c, opacity: 0.3 });
      mkdiv(H, 's-bench', 'bv-b' + i, 'bar', { left: X + 'px', top: y + 'px', height: '50px', width: '0px', background: c });
      mkdiv(H, 's-bench', 'bv-v' + i, 'barv', { left: (X + w(hi) + 16) + 'px', top: (y + 8) + 'px', color: c, opacity: 0 },
        hi >= 1000 ? (lo / 1000).toFixed(1) + '–' + (hi / 1000).toFixed(1) + ' µs' : lo + '–' + hi + ' ns');
    });
  },
  draw(u, cue, H) {
    BV.forEach(([, lo, hi, , k, dl], i) => {
      const w = (v) => 300 * Math.log10(v / 10);
      const p = H.P(u, cue(k) + dl, 1.0);
      H.$('bv-l' + i).style.opacity = H.P(u, cue(k) + dl, 0.4);
      H.$('bv-b' + i).style.width = (w(lo) * p) + 'px';
      H.$('bv-r' + i).style.width = (w(hi) * p) + 'px';
      H.$('bv-v' + i).style.opacity = H.P(u, cue(k) + dl + 0.8, 0.4);
    });
  }
};
