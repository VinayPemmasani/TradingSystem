// Signals explainer: price ladders and live signal values. Every draw() is
// stateless: the book is rebuilt from a base book plus the events whose time
// has passed. Prices are ITCH Price(4) integers (one cent = 100).
(function () {
  const S = window.SCENES;
  const TICK = 100;
  const BASE = { b: { 500100: 600, 500000: 1100, 499900: 500, 499800: 900, 499700: 1300 },
                 a: { 500300: 400, 500400: 900, 500500: 700, 500600: 1200, 500700: 800 } };
  const copy = (k) => ({ b: Object.assign({}, k.b), a: Object.assign({}, k.a) });
  const usd = (p) => (p / 10000).toFixed(2);
  const usd4 = (p) => (p / 10000).toFixed(4);
  const sgn = (x, d) => (x >= 0 ? '+' : '−') + Math.abs(x).toFixed(d);

  function levels(side) { // [[px, qty]] best first
    const o = Object.keys(side).map(Number).filter((p) => side[p] > 0).map((p) => [p, side[p]]);
    return o;
  }
  function bids(k) { return levels(k.b).sort((x, y) => y[0] - x[0]); }
  function asks(k) { return levels(k.a).sort((x, y) => x[0] - y[0]); }
  function top(k) { const b = bids(k)[0], a = asks(k)[0]; return { pb: b[0], qb: b[1], pa: a[0], qa: a[1] }; }
  function mid(k) { const t = top(k); return Math.floor((t.pb + t.pa) / 2); }
  function micro(k) { const t = top(k); return t.pb + Math.floor((t.pa - t.pb) * t.qb / (t.qb + t.qa)); }
  function microF(k) { const t = top(k); return t.pb + (t.pa - t.pb) * t.qb / (t.qb + t.qa); }
  function depth(k, N, lam) {
    const B = bids(k).slice(0, N), A = asks(k).slice(0, N);
    let wb = 0, wa = 0, pbs = 0, pas = 0;
    B.forEach(([p, q], i) => { const w = Math.pow(lam, i); wb += w * q; pbs += w * q * p; });
    A.forEach(([p, q], i) => { const w = Math.pow(lam, i); wa += w * q; pas += w * q * p; });
    const Bb = pbs / wb, Ab = pas / wa;
    return { di: (wb - wa) / (wb + wa), pn: (Bb * wa + Ab * wb) / (wa + wb) };
  }

  // ---------- ladder ----------
  function mkLadder(H, id, pxTop, n, rh) {
    const root = H.$(id); root.innerHTML = '';
    const L = { root, pxTop, n, rh, rows: {}, marks: {} };
    for (let i = 0; i < n; i++) {
      const px = pxTop - i * TICK;
      const r = document.createElement('div'); r.className = 'lr';
      r.style.top = (i * rh) + 'px'; r.style.height = rh + 'px';
      r.innerHTML = '<div class="lb"><div class="lbar"></div><span class="lq"></span></div><div class="lp">' + usd(px) +
        '</div><div class="la"><div class="lbar"></div><span class="lq"></span></div>';
      root.appendChild(r);
      L.rows[px] = { r, bb: r.querySelector('.lb .lbar'), bq: r.querySelector('.lb .lq'),
                     ab: r.querySelector('.la .lbar'), aq: r.querySelector('.la .lq') };
    }
    const h1 = document.createElement('div'); h1.className = 'lhead'; h1.style.left = '60px'; h1.textContent = 'BID SIZE';
    const h2 = document.createElement('div'); h2.className = 'lhead'; h2.style.left = '260px'; h2.textContent = 'PRICE';
    const h3 = document.createElement('div'); h3.className = 'lhead'; h3.style.left = '440px'; h3.textContent = 'ASK SIZE';
    root.appendChild(h1); root.appendChild(h2); root.appendChild(h3);
    return L;
  }
  const ly = (L, px) => (L.pxTop - px) / TICK * L.rh + L.rh / 2;
  function paint(L, k, flash) {
    for (const px in L.rows) {
      const R = L.rows[px]; const qb = k.b[px] || 0, qa = k.a[px] || 0;
      R.bb.style.width = (Math.min(qb / 1500, 1) * 210) + 'px'; R.bb.style.opacity = qb ? 1 : 0;
      R.ab.style.width = (Math.min(qa / 1500, 1) * 210) + 'px'; R.ab.style.opacity = qa ? 1 : 0;
      H.text(R.bq, qb ? String(qb) : ''); H.text(R.aq, qa ? String(qa) : '');
      R.r.classList.toggle('flash', !!(flash && flash[px]));
    }
  }
  function mark(L, name, color, px, label, op) {
    let m = L.marks[name];
    if (!m) {
      m = document.createElement('div'); m.className = 'mk'; m.style.borderTopColor = color;
      const side = name === 'mid' ? 'left:auto;right:622px;' : '';
      m.innerHTML = '<span style="' + side + 'color:' + color + '"></span>'; L.root.appendChild(m); L.marks[name] = m;
    }
    m.style.top = ly(L, px) + 'px'; m.style.opacity = op; H.text(m.firstChild, label);
  }
  // events: [time, side, px, newQty]; applied when u >= time
  function play(base, ev, u) {
    const k = copy(base); const fl = {}; let last = -1;
    ev.forEach((e, i) => { if (u >= e[0]) { k[e[1]][e[2]] = e[3]; last = i; } });
    if (last >= 0 && u - ev[last][0] < 0.45) fl[ev[last][2]] = 1;
    return { k, fl, n: last + 1 };
  }

  // ---------- hook ----------
  let hk;
  const HKEV = [[0, 'a', 500300, 250], [0.6, 'b', 500100, 900], [1.2, 'a', 500300, 0], [1.8, 'b', 500200, 200],
    [2.4, 'a', 500400, 600], [3.0, 'b', 500200, 500], [3.6, 'a', 500300, 300], [4.2, 'b', 500100, 700],
    [4.8, 'a', 500400, 1000], [5.4, 'b', 500200, 0], [6.0, 'a', 500300, 500], [6.6, 'b', 500100, 400]];
  S.hook = {
    setup(H) { hk = mkLadder(H, 'hk-lad', 500700, 11, 56); },
    draw(u, cue, H) {
      const t0 = cue(1) + 0.6;
      const { k, fl } = play(BASE, HKEV.map((e) => [t0 + e[0]].concat(e.slice(1))), u);
      paint(hk, k, fl);
      const on = H.C((u - cue(1)) / 0.5);
      mark(hk, 'mid', 'var(--teal)', mid(k), 'mid', on);
      mark(hk, 'mic', 'var(--amber)', microF(k), 'micro ' + usd4(micro(k)), on);
    } };

  // ---------- pipeline ----------
  S.pipeline = {
    setup(H) {
      const el = H.$('pl-book'); el.innerHTML = '';
      const q = [[900, 1], [1300, 1], [700, 1], [1100, 1], [500, 0], [600, 0], [1000, 0], [800, 0]];
      q.forEach(([v, ask], i) => {
        const d = document.createElement('div');
        d.style.cssText = 'position:absolute;height:15px;border-radius:3px;top:' + (i * 19) + 'px;' +
          (ask ? 'left:172px;background:rgba(255,107,94,.75)' : 'right:172px;background:rgba(79,209,139,.75)') + ';width:' + (v / 1300 * 160) + 'px';
        el.appendChild(d);
      });
    },
    draw(u, cue, H) {
      const t = u - cue(2);
      H.$('pl-d0').classList.toggle('hl', t > 0.5 && (Math.floor(t / 0.9) % 2 === 0));
      H.$('pl-d1').classList.toggle('hl', t > 0.5 && (Math.floor(t / 1.3) % 2 === 1));
    } };

  // ---------- tob ----------
  let tb, tbBr;
  S.tob = {
    setup(H) {
      tb = mkLadder(H, 'tb-lad', 500700, 11, 56);
      tbBr = document.createElement('div');
      tbBr.style.cssText = 'position:absolute;left:622px;width:22px;border:3px solid var(--amber);border-left:none;opacity:0';
      tbBr.innerHTML = '<span style="position:absolute;left:34px;top:50%;transform:translateY(-50%);white-space:nowrap;font:700 24px var(--mono);color:var(--amber)">2 ticks</span>';
      tb.root.appendChild(tbBr);
    },
    draw(u, cue, H) {
      paint(tb, BASE, u > cue(2) && u < cue(3) ? { 500100: 1, 500300: 1 } : null);
      mark(tb, 'mid', 'var(--teal)', 500200, 'mid 50.02', H.P(u, cue(1)));
      tbBr.style.top = ly(tb, 500300) + 'px'; tbBr.style.height = (ly(tb, 500100) - ly(tb, 500300)) + 'px';
      tbBr.style.opacity = H.P(u, cue(2));
    } };

  // ---------- micro ----------
  let mc;
  S.micro = {
    setup(H) { mc = mkLadder(H, 'mc-lad', 500700, 11, 56); },
    draw(u, cue, H) {
      const t0 = cue(4);
      const { k, fl } = play(BASE, [[t0 + 0.4, 'a', 500300, 300], [t0 + 1.3, 'a', 500300, 200], [t0 + 2.2, 'a', 500300, 100]], u);
      paint(mc, k, fl);
      const t = top(k);
      H.text('mc-i', (t.qb / (t.qb + t.qa)).toFixed(3));
      H.text('mc-m', String(micro(k)));
      mark(mc, 'mid', 'var(--teal)', mid(k), 'mid', 1);
      mark(mc, 'mic', 'var(--amber)', microF(k), 'micro ' + usd4(micro(k)), H.P(u, cue(2)));
    } };

  // ---------- depth ----------
  let dp;
  S.depth = {
    setup(H) {
      dp = mkLadder(H, 'dp-lad', 500700, 11, 56);
      for (let i = 0; i < 5; i++) {
        [[500100 - i * TICK, 'var(--green)'], [500300 + i * TICK, 'var(--red)']].forEach(([px]) => {
          const w = document.createElement('div'); w.className = 'wl dpw';
          w.style.top = (ly(dp, px) - 16) + 'px'; w.style.height = '32px';
          w.textContent = 'w' + '₀₁₂₃₄'[i] + '=' + (Math.pow(0.5, i)).toString().replace(/^0/, '');
          dp.root.appendChild(w);
        });
      }
    },
    draw(u, cue, H) {
      const t0 = cue(2);
      const { k, fl } = play(BASE, [[t0 + 0.4, 'b', 499700, 3000], [t0 + 2.0, 'a', 500300, 150]], u);
      paint(dp, k, fl);
      const d = depth(k, 5, 0.5);
      H.text('dp-di', sgn(d.di, 3));
      H.text('dp-pr', sgn((d.pn - mid(k)) / TICK, 2));
      const wo = H.P(u, cue(1) + 1);
      dp.root.querySelectorAll('.dpw').forEach((w) => { w.style.opacity = wo; });
      mark(dp, 'mid', 'var(--teal)', mid(k), 'mid', 1);
      mark(dp, 'pn', 'var(--pink)', d.pn, 'P₅ ' + usd4(d.pn), H.P(u, cue(3) + 0.5));
    } };

  // ---------- ofi scatter ----------
  S.ofi = {
    setup(H) {
      const sv = H.$('of-sc'); const ns = 'http://www.w3.org/2000/svg';
      const X0 = 1450, Y0 = 640, W = 360, Hh = 250;
      let html = '<rect x="' + X0 + '" y="' + Y0 + '" width="' + W + '" height="' + Hh + '" rx="14" fill="rgba(19,33,43,.82)" stroke="#2c4351" stroke-width="2"/>';
      html += '<line x1="' + (X0 + 20) + '" y1="' + (Y0 + Hh / 2) + '" x2="' + (X0 + W - 20) + '" y2="' + (Y0 + Hh / 2) + '" stroke="#2c4351" stroke-width="2"/>';
      html += '<line x1="' + (X0 + W / 2) + '" y1="' + (Y0 + 20) + '" x2="' + (X0 + W / 2) + '" y2="' + (Y0 + Hh - 20) + '" stroke="#2c4351" stroke-width="2"/>';
      let s = 7;
      const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
      for (let i = 0; i < 46; i++) {
        const x = (rnd() * 2 - 1) * 140; const y = 0.62 * x + (rnd() + rnd() - 1) * 28;
        html += '<circle cx="' + (X0 + W / 2 + x).toFixed(1) + '" cy="' + (Y0 + Hh / 2 - y).toFixed(1) + '" r="5" fill="#a98bff" opacity=".8"/>';
      }
      html += '<line x1="' + (X0 + W / 2 - 150) + '" y1="' + (Y0 + Hh / 2 + 93) + '" x2="' + (X0 + W / 2 + 150) + '" y2="' + (Y0 + Hh / 2 - 93) + '" stroke="#ffb347" stroke-width="3"/>';
      html += '<text x="' + (X0 + W - 24) + '" y="' + (Y0 + Hh / 2 + 28) + '" fill="#8ea3b1" font-family="IBM Plex Mono" font-size="18" text-anchor="end">OFI</text>';
      html += '<text x="' + (X0 + W / 2 + 10) + '" y="' + (Y0 + 36) + '" fill="#8ea3b1" font-family="IBM Plex Mono" font-size="18">ΔP</text>';
      html += '<text x="' + (X0 + 20) + '" y="' + (Y0 + Hh - 14) + '" fill="#8ea3b1" font-family="IBM Plex Mono" font-size="15">illustrative</text>';
      sv.innerHTML = html;
    } };

  // ---------- ofi events ----------
  const OEV = [
    { b: '50.01 × 800', a: '50.03 × 400', e: 200, row: 1, txt: 'bid add 200, price same' },
    { b: '50.01 × 800', a: '50.03 × 250', e: 150, row: 4, txt: 'trade 150 at the ask' },
    { b: '50.01 × 500', a: '50.03 × 250', e: -300, row: 1, txt: 'bid cancel 300' },
    { b: '50.01 × 500', a: '50.04 × 900', e: 250, row: 5, txt: 'trade 250 clears 50.03' },
    { b: '50.02 × 300', a: '50.04 × 900', e: 300, row: 0, txt: 'new bid 50.02 × 300' }];
  S.ofievents = {
    setup(H) {
      const lg = H.$('oe-log'); lg.innerHTML = '';
      OEV.forEach((v, i) => {
        const d = document.createElement('div'); d.id = 'oe-l' + i; d.style.opacity = 0;
        d.innerHTML = '<span class="c-muted">' + (i + 1) + '</span>  ' + v.txt + '  <span class="c-violet">e = ' + (v.e > 0 ? '+' : '−') + Math.abs(v.e) + '</span>';
        lg.appendChild(d);
      });
    },
    draw(u, cue, H) {
      const rows = H.$('oe-tab').querySelectorAll('tr');
      let n = 0; for (let i = 0; i < OEV.length; i++) if (u >= cue(4) + 0.6 + i * 1.5) n = i + 1;
      let sum = 0; for (let i = 0; i < n; i++) sum += OEV[i].e;
      for (let i = 0; i < OEV.length; i++) H.$('oe-l' + i).style.opacity = i < n ? 1 : 0;
      const cur = n > 0 ? OEV[n - 1] : null;
      rows.forEach((r, i) => r.classList.toggle('on', !!cur && cur.row === i));
      H.text('oe-b', cur ? cur.b : '50.01 × 600'); H.text('oe-a', cur ? cur.a : '50.03 × 400');
      // animate the bar toward the running sum
      let prev = 0; for (let i = 0; i < n - 1; i++) prev += OEV[i].e;
      const p = n > 0 ? H.ease((u - (cue(4) + 0.6 + (n - 1) * 1.5)) / 0.5) : 0;
      const v = prev + (sum - prev) * p;
      const bar = H.$('oe-bar');
      bar.style.width = (Math.abs(v) * 0.8) + 'px'; bar.style.left = (v >= 0 ? 250 : 250 - Math.abs(v) * 0.8) + 'px';
      H.text('oe-v', 'OFI = ' + (Math.round(v) >= 0 ? '+' : '−') + Math.abs(Math.round(v)));
    } };

  // ---------- trades ----------
  let tr;
  const TAPE = [['B', 200], ['B', 100], ['S', 300], ['B', 400], ['B', 200], ['S', 100], ['B', 300]];
  S.trades = {
    setup(H) {
      tr = mkLadder(H, 'tr-lad', 500700, 11, 56);
      const el = H.$('tr-tape'); el.innerHTML = '';
      TAPE.forEach(([s, q], i) => {
        const c = document.createElement('span'); c.className = 'chip'; c.id = 'tr-c' + i;
        c.style.background = s === 'B' ? 'var(--green)' : 'var(--red)'; c.style.opacity = 0;
        c.textContent = s + ' ' + q; el.appendChild(c);
      });
    },
    draw(u, cue, H) {
      let vb = 0, vs = 0;
      TAPE.forEach(([s, q], i) => {
        const p = H.P(u, cue(2) + 0.6 + i * 0.5, 0.3);
        H.$('tr-c' + i).style.opacity = p;
        if (p > 0.5) { if (s === 'B') vb += q; else vs += q; }
      });
      const tfi = vb + vs ? (vb - vs) / (vb + vs) : 0;
      H.text('tr-v', sgn(tfi, 2));
      H.$('tr-dot').style.left = (50 + 50 * tfi) + '%';
      const t3 = cue(3) + 0.3, t4 = cue(4) + 0.3;
      const ev = [[t3, 'b', 499900, 6000],
        [t4, 'a', 500300, 0], [t4 + 0.6, 'a', 500300, 200], [t4 + 1.3, 'a', 500300, 0],
        [t4 + 1.9, 'a', 500300, 200], [t4 + 2.6, 'a', 500300, 0], [t4 + 3.2, 'a', 500300, 200]];
      const { k, fl } = play(BASE, ev, u);
      if (u > t3 && u < cue(4)) fl[499900] = 1;
      paint(tr, k, fl);
      let refills = 0; [t4 + 0.6, t4 + 1.9, t4 + 3.2].forEach((t) => { if (u >= t) refills++; });
      H.text('tr-ice', '50.03 refills ×' + refills + (refills >= 2 ? ': iceberg?' : ''));
    } };

  // ---------- queue ----------
  const QS = 1.1; // px per share
  const QO = [['A', 200], ['B', 300], ['C', 100], ['YOU', 100], ['D', 400]];
  S.queue = {
    setup(H) {
      const el = H.$('qu-q'); el.innerHTML = '';
      QO.forEach(([n]) => {
        const d = document.createElement('div'); d.className = 'qblk'; d.id = 'qu-' + n;
        d.style.background = n === 'YOU' ? 'var(--pink)' : '#5fb7c4'; el.appendChild(d);
      });
    },
    draw(u, cue, H) {
      const tA = cue(3) + 0.3, tD = cue(4) + 0.2, tB = cue(4) + 1.6;
      const fA = H.ease((u - tA) / 1.0), fB = H.ease((u - tB) / 0.8), fD = H.ease((u - tD) / 0.8);
      const left = { A: 200 * (1 - fA), B: 300 * (1 - fB), C: 100, YOU: 100, D: 400 * (1 - fD) };
      let x = 0;
      QO.forEach(([n, q]) => {
        const d = H.$('qu-' + n); const w = left[n] * QS;
        d.style.left = x + 'px'; d.style.width = Math.max(w, 0) + 'px'; d.style.opacity = w < 4 ? 0 : 1;
        const sh = n === 'A' ? Math.round(left[n]) : q;
        H.text(d, w > 60 ? n + ' ' + sh : '');
        if (n === 'D') d.style.background = u > tD ? '#5a6872' : '#5fb7c4';
        x += w + (w > 4 ? 10 : 0);
      });
      const ahead = Math.round(left.A + left.B + left.C);
      H.text('qu-ahead', String(ahead));
      let note = '';
      if (u > tA && u < tD) note = 'A executed: off the front';
      else if (u >= tD && u < tB) note = 'D cancelled: behind you, no change';
      else if (u >= tB) note = 'B cancelled: was ahead of you';
      H.text('qu-note', note);
    } };

  // ---------- ewma chart ----------
  S.ewma = {
    setup(H) {
      const X = (t) => 160 + t * 98, Y = (v) => 520 - v * 210;
      let s = 11; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
      const ups = []; // [t, value]
      for (let t = 0; t <= 10.0001; t += 0.25) {
        ups.push([t, 0.3 * Math.sin(0.55 * t + 0.4) + (rnd() - 0.5) * 0.45]);
        if (Math.abs(t - 6) < 1e-6) { for (let j = 1; j <= 100; j++) ups.push([6 + j * 1e-8, 0.95]); ups.push([6 + 2e-6, 0.1]); }
      }
      let raw = 'M' + X(0) + ' ' + Y(ups[0][1]);
      for (let i = 1; i < ups.length; i++) raw += ' L' + X(ups[i][0]).toFixed(1) + ' ' + Y(ups[i - 1][1]).toFixed(1) + ' L' + X(ups[i][0]).toFixed(1) + ' ' + Y(ups[i][1]).toFixed(1);
      let pu = ups[0][1], tm = ups[0][1], prev = ups[0][1], pt = 0;
      let dpu = 'M' + X(0) + ' ' + Y(pu), dtm = 'M' + X(0) + ' ' + Y(tm);
      for (let i = 1; i < ups.length; i++) {
        const [t, v] = ups[i];
        pu += 0.05 * (v - pu);
        const a = 1 - Math.exp(-(t - pt) / 1.0); tm += a * (prev - tm); prev = v; pt = t;
        dpu += ' L' + X(t).toFixed(1) + ' ' + Y(pu).toFixed(1);
        dtm += ' L' + X(t).toFixed(1) + ' ' + Y(tm).toFixed(1);
      }
      H.$('ew-raw').setAttribute('d', raw); H.$('ew-pu').setAttribute('d', dpu); H.$('ew-tm').setAttribute('d', dtm);
    } };

  // ---------- fair value ----------
  const FY = (px) => 30 + (500400 - px) / TICK * 110;
  function hline(el, color, w, x, label, dashed) {
    const d = document.createElement('div');
    d.style.cssText = 'position:absolute;left:' + x + 'px;width:' + w + 'px;height:0;border-top:' + (dashed ? '3px dashed ' : '4px solid ') + color + ';opacity:0';
    d.innerHTML = '<span style="position:absolute;left:' + (w + 10) + 'px;top:-15px;white-space:nowrap;font:700 21px var(--mono);color:' + color + '">' + label + '</span>';
    el.appendChild(d); return d;
  }
  const FR = {};
  S.fair = {
    setup(H) {
      const el = H.$('fr-axis'); el.innerHTML = '';
      const ax = document.createElement('div'); ax.style.cssText = 'position:absolute;left:110px;top:0;width:2px;height:690px;background:var(--line)'; el.appendChild(ax);
      for (let px = 500400; px >= 499800; px -= TICK) {
        const t = document.createElement('div');
        t.style.cssText = 'position:absolute;left:0;width:95px;text-align:right;font:600 22px var(--mono);color:var(--muted);top:' + (FY(px) - 15) + 'px';
        t.textContent = usd(px); el.appendChild(t);
        const g = document.createElement('div'); g.style.cssText = 'position:absolute;left:112px;width:780px;height:0;border-top:1px solid rgba(142,163,177,.12);top:' + FY(px) + 'px'; el.appendChild(g);
      }
      [['market', 130], ['signals', 400], ['our quotes', 680]].forEach(([t, x]) => {
        const h = document.createElement('div'); h.style.cssText = 'position:absolute;top:-38px;left:' + x + 'px;font:600 19px var(--mono);color:var(--muted);letter-spacing:.06em';
        h.textContent = t.toUpperCase(); el.appendChild(h);
      });
      FR.mb = hline(el, 'var(--green)', 110, 130, 'bid', false);
      FR.ma = hline(el, 'var(--red)', 110, 130, 'ask', false);
      FR.mi = hline(el, 'var(--amber)', 100, 400, 'micro 50.0220', true);
      FR.fv = hline(el, 'var(--blue)', 100, 400, 'FV 50.0270', true);
      FR.qb = hline(el, 'var(--pink)', 110, 680, 'bid', false);
      FR.qa = hline(el, 'var(--pink)', 110, 680, 'ask', false);
      FR.wk = hline(el, 'var(--pink)', 110, 680, 'working', true);
      FR.terms = document.createElement('div');
      FR.terms.style.cssText = 'position:absolute;left:440px;width:18px;opacity:0';
      FR.terms.innerHTML = '<div style="height:33px;background:var(--violet)"></div><div style="height:11px;background:var(--pink)"></div><div style="height:11px;background:var(--blue)"></div>';
      el.appendChild(FR.terms);
      FR.band = document.createElement('div');
      FR.band.style.cssText = 'position:absolute;left:666px;width:138px;background:rgba(255,179,71,.12);border:2px dashed var(--amber);opacity:0';
      el.appendChild(FR.band);
    },
    draw(u, cue, H) {
      const pos = (d, px, op) => { d.style.top = FY(px) + 'px'; d.style.opacity = op; };
      pos(FR.mb, 500100, 1); pos(FR.ma, 500300, 1);
      pos(FR.mi, 500220, H.P(u, cue(1)));
      const tf = cue(1) + 1.6;
      FR.terms.style.top = FY(500270) + 'px'; FR.terms.style.opacity = H.P(u, tf - 0.6);
      pos(FR.fv, 500270, H.P(u, tf));
      const lean = 200 * H.ease((u - (cue(3) + 0.8)) / 1.0);
      pos(FR.qb, 500100 - lean, H.P(u, cue(2) + 0.3));
      pos(FR.qa, 500400 - lean, H.P(u, cue(2) + 0.3));
      pos(FR.wk, 500300, H.P(u, cue(5) + 0.3));
      FR.band.style.top = FY(500400) + 'px'; FR.band.style.height = (FY(500200) - FY(500400)) + 'px';
      FR.band.style.opacity = H.P(u, cue(5) + 0.3);
    } };

  // ---------- pitfalls ----------
  S.pitfalls = {
    setup(H) {
      const el = H.$('pf-days'); el.innerHTML = '';
      const rows = [[0, ['fit', 'fit', 'fit', 'test', '']], [1, ['', 'fit', 'fit', 'fit', 'test']], [2, ['fit+test', '', '', '', '']]];
      rows.forEach(([r, cells]) => {
        const row = document.createElement('div'); row.id = 'pf-r' + r;
        row.style.cssText = 'position:absolute;left:0;top:' + (20 + r * 78) + 'px;width:490px;height:62px;opacity:0';
        cells.forEach((c, i) => {
          if (!c) return;
          const d = document.createElement('div');
          const col = c === 'fit' ? 'var(--teal)' : c === 'test' ? 'var(--amber)' : 'var(--red)';
          d.style.cssText = 'position:absolute;top:0;height:58px;border-radius:8px;display:grid;place-items:center;font:700 20px var(--mono);color:#06141a;background:' + col +
            ';left:' + (i * 96) + 'px;width:' + (c === 'fit+test' ? 186 : 88) + 'px';
          d.textContent = c === 'fit+test' ? 'fit + test ✕' : c; row.appendChild(d);
        });
        const lab = document.createElement('div');
        lab.style.cssText = 'position:absolute;top:-22px;left:0;font:500 16px var(--mono);color:var(--muted)';
        lab.textContent = r === 2 ? 'same day: looks great, means nothing' : r === 0 ? 'day 1    2    3    4    5' : '';
        if (lab.textContent) row.appendChild(lab);
        el.appendChild(row);
      });
    },
    draw(u, cue, H) {
      H.$('pf-r0').style.opacity = H.P(u, cue(4) + 0.3);
      H.$('pf-r1').style.opacity = H.P(u, cue(4) + 1.6);
      H.$('pf-r2').style.opacity = H.P(u, cue(4) + 3.0);
    } };
})();
