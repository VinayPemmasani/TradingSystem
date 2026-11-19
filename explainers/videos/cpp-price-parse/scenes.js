// Custom animation: digit-loop cursor, SWAR byte lanes, benchmark bars.
SCENES['loop'] = {
  draw(u, cue, H) {
    const xs = [200, 290, 380, 470, 560, 650, 740, 830];
    const c = H.$('lp-cur');
    const t1 = cue(1) + 0.6, t1e = cue(2) - 0.2, t3 = cue(3) + 0.3, t3e = cue(3) + 2.4;
    let k = -1, w = 0, f = 0;
    if (u >= t1) { const n = Math.min(3, 1 + Math.floor((u - t1) / ((t1e - t1) / 3))); k = n - 1; w = [1, 12, 123][k]; }
    if (u >= t3) { const n = Math.min(4, 1 + Math.floor((u - t3) / ((t3e - t3) / 4))); k = 3 + n; f = [4, 45, 456, 4567][n - 1]; w = 123; }
    c.style.opacity = k < 0 ? 0 : 1;
    if (k >= 0) c.style.left = (xs[k] - 6) + 'px';
    c.style.borderColor = k >= 4 ? 'var(--amber)' : 'var(--green)';
    H.text('lp-w', String(w));
    H.text('lp-f', String(f));
  }
};

const SW = { x0: 100, pitch: 104 };
SCENES['swar'] = {
  setup(H) {
    const host = H.$('s-swar');
    const mk = (id, cls, x, y, w, txt, css) => { const d = document.createElement('div'); d.id = id; d.className = cls; d.textContent = txt;
      Object.assign(d.style, { left: x + 'px', top: y + 'px', width: w + 'px', opacity: 0 }, css || {}); host.appendChild(d); return d; };
    const col = (i) => i === 0 ? 'var(--muted)' : i < 4 ? 'var(--teal)' : 'var(--amber)';
    for (let i = 0; i < 8; i++) {
      mk('sw-a' + i, 'byte', SW.x0 + i * SW.pitch, 240, 96, "'" + i + "'", { color: col(i), borderColor: col(i) });
      mk('sw-h' + i, 'lbl', SW.x0 + i * SW.pitch, 316, 96, '0x3' + i, { textAlign: 'center' });
      mk('sw-b' + i, 'byte', SW.x0 + i * SW.pitch, 350, 96, String(i), { color: col(i), borderColor: col(i) });
    }
    [['1', 0], ['23', 1], ['45', 2], ['67', 3]].forEach(([t, j]) => mk('sw-c' + j, 'byte', SW.x0 + j * 2 * SW.pitch, 450, 2 * SW.pitch - 8, t, { color: 'var(--violet)', borderColor: 'var(--violet)' }));
    [['123', 0], ['4567', 1]].forEach(([t, j]) => mk('sw-d' + j, 'byte', SW.x0 + j * 4 * SW.pitch, 450, 4 * SW.pitch - 8, t, { color: 'var(--violet)', borderColor: 'var(--violet)' }));
    mk('sw-e', 'byte', SW.x0, 450, 8 * SW.pitch - 8, '1234567', { color: 'var(--green)', borderColor: 'var(--green)', fontSize: '34px' });
    mk('sw-src', 'big', 1060, 240, 700, '"123.4567"', { fontSize: '48px', color: 'var(--ink)' });
    mk('sw-src2', 'note', 1060, 320, 760, 'whole "123" right-aligned into bytes 0–3, fraction "4567" left-aligned into 4–7', { fontSize: '24px' });
    mk('sw-lab', 'lbl', 1060, 455, 700, 'one 64-bit result = Price(4)', { color: 'var(--green)', fontSize: '26px' });
  },
  draw(u, cue, H) {
    const a = H.P(u, cue(0) + 0.3, 0.5);
    for (let i = 0; i < 8; i++) {
      H.$('sw-a' + i).style.opacity = H.P(u, cue(0) + 0.3 + i * 0.08, 0.4);
      H.$('sw-h' + i).style.opacity = H.P(u, cue(0) + 1.2 + i * 0.05, 0.4);
      H.$('sw-b' + i).style.opacity = H.P(u, cue(1) + 0.6 + i * 0.06, 0.4);
    }
    const t2 = cue(2);
    const c = H.P(u, t2 + 0.4, 0.4) * (1 - H.P(u, t2 + 1.4, 0.3));
    const d = H.P(u, t2 + 1.5, 0.4) * (1 - H.P(u, t2 + 2.6, 0.3));
    const e = H.P(u, t2 + 2.7, 0.4);
    for (let j = 0; j < 4; j++) H.$('sw-c' + j).style.opacity = c;
    for (let j = 0; j < 2; j++) H.$('sw-d' + j).style.opacity = d;
    H.$('sw-e').style.opacity = e;
    H.$('sw-src').style.opacity = H.P(u, cue(3), 0.5);
    H.$('sw-src2').style.opacity = H.P(u, cue(3) + 0.8, 0.5);
    H.$('sw-lab').style.opacity = H.P(u, cue(4), 0.5);
    void a;
  }
};

// [label, low, high, colour, cue, delay]
const BP = [['stod', 171, 210, 'var(--red)', 1, 0], ['strtod', 122, 182, 'var(--red)', 1, 0.4], ['stringstream', 366, 663, 'var(--red)', 1, 2.2],
  ['digit loop', 19, 38, 'var(--teal)', 2, 0], ['from_chars', 22, 46, 'var(--teal)', 2, 0.4], ['SWAR', 26, 47, 'var(--violet)', 3, 0],
  ['lab parse_price', 42, 63, 'var(--blue)', 2, 1.4]];
SCENES['bench'] = {
  setup(H) {
    const host = H.$('s-bench'); const X = 430, S = 1150 / 700;
    BP.forEach(([n, lo, hi, c], i) => {
      const y = 320 + i * 78;
      const mk = (id, cls, css, txt) => { const d = document.createElement('div'); d.id = id; d.className = cls; if (txt) d.textContent = txt; Object.assign(d.style, css); host.appendChild(d); };
      mk('bp-l' + i, 'barl', { left: (X - 280) + 'px', top: (y + 6) + 'px', color: c, opacity: 0 }, n);
      mk('bp-r' + i, 'bar', { left: X + 'px', top: y + 'px', height: '40px', width: '0px', background: c, opacity: 0.3 });
      mk('bp-b' + i, 'bar', { left: X + 'px', top: y + 'px', height: '40px', width: '0px', background: c });
      mk('bp-v' + i, 'barv', { left: (X + hi * S + 16) + 'px', top: (y + 6) + 'px', color: c, opacity: 0 }, lo + '–' + hi + ' ns');
    });
  },
  draw(u, cue, H) {
    const S = 1150 / 700;
    BP.forEach(([, lo, hi, , k, dl], i) => {
      const p = H.P(u, cue(k) + dl, 0.9);
      H.$('bp-l' + i).style.opacity = H.P(u, cue(k) + dl, 0.4);
      H.$('bp-b' + i).style.width = (lo * S * p) + 'px';
      H.$('bp-r' + i).style.width = (hi * S * p) + 'px';
      H.$('bp-v' + i).style.opacity = H.P(u, cue(k) + dl + 0.7, 0.4);
    });
  }
};
