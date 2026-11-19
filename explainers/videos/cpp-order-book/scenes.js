// Custom animation: naive scan cursor, price ladder with best-price markers.
SCENES['naive'] = {
  draw(u, cue, H) {
    // visit order: level 100.02 (17,23,41), 100.01 (8,52), 100.00 (5,31,64)
    const P = [[1300, 265], [1440, 265], [1580, 265], [1300, 395], [1440, 395], [1300, 525], [1440, 525], [1580, 525]];
    const t0 = cue(3), t1 = cue(4) - 0.3;
    const c = H.$('nv-cur');
    if (u < t0) { c.style.opacity = 0; H.text('nv-n', '0'); return; }
    const k = Math.min(P.length - 1, Math.floor(H.C((u - t0) / (t1 - t0)) * P.length));
    c.style.opacity = 1;
    c.style.left = (P[k][0] - 6) + 'px'; c.style.top = (P[k][1] - 6) + 'px';
    const found = k === P.length - 1 && u > t1 - 0.2;
    c.style.borderColor = found ? 'var(--green)' : 'var(--red)';
    H.text('nv-n', String(k + 1));
  }
};

const LV = { x0: 150, pitch: 80, base: 480, bids: { 3: 3, 4: 5, 5: 4, 6: 6, 7: 8, 8: 5 }, asks: { 11: 6, 12: 8, 13: 4, 14: 5, 15: 7, 16: 3, 17: 4 } };
SCENES['levels'] = {
  setup(H) {
    const host = H.$('s-levels');
    for (let i = 0; i < 20; i++) {
      const b = document.createElement('div'); b.className = 'ladder'; b.id = 'lv-b' + i;
      b.style.left = (LV.x0 + i * LV.pitch) + 'px'; b.style.top = 'auto'; b.style.bottom = (1080 - LV.base) + 'px'; b.style.height = '0px';
      host.appendChild(b);
      const c = document.createElement('div'); c.className = 'lcell'; c.id = 'lv-c' + i;
      c.style.left = (LV.x0 + i * LV.pitch) + 'px'; c.style.top = (LV.base + 8) + 'px'; c.textContent = String(i);
      host.appendChild(c);
    }
    const base = document.createElement('div'); base.id = 'lv-base';
    Object.assign(base.style, { left: (LV.x0 - 10) + 'px', top: LV.base + 'px', width: (20 * LV.pitch) + 'px', height: '3px', background: 'var(--line)' });
    host.appendChild(base);
  },
  draw(u, cue, H) {
    const t0 = cue(0) + 0.3;
    const tAdd = cue(3) + 1.0, tDel = cue(4) + 1.2;
    for (let i = 0; i < 20; i++) {
      const p = H.P(u, t0 + i * 0.04, 0.5);
      const b = H.$('lv-b' + i), c = H.$('lv-c' + i);
      c.style.opacity = p;
      let h = 0, col = 'var(--panel2)';
      if (LV.bids[i]) { h = LV.bids[i] * 20; col = 'var(--green)'; }
      if (LV.asks[i]) { h = LV.asks[i] * 20; col = 'var(--red)'; }
      if (i === 10) { h = 120 * H.P(u, tAdd, 0.5) * (1 - H.P(u, tDel, 0.5)); col = 'var(--green)'; }
      b.style.height = Math.max(h * p, 6 * p) + 'px';
      b.style.background = h ? col : 'var(--panel2)';
      b.style.opacity = h ? 0.9 : 0.6 * p;
    }
    H.$('lv-base').style.opacity = H.P(u, t0, 0.5);
    // best bid index: 8, then 10 after the add, then walks 10 -> 9 -> 8 after the cancel
    let bi = 8;
    if (u > tAdd + 0.3) bi = 10;
    if (u > tDel + 0.6) bi = H.lerp(10, 9, H.P(u, tDel + 0.6, 0.5));
    if (u > tDel + 1.3) bi = H.lerp(9, 8, H.P(u, tDel + 1.3, 0.5));
    const cx = (i) => (LV.x0 + i * LV.pitch + 36 - 40) + 'px';
    H.$('lv-bid').style.left = cx(bi);
    H.$('lv-ask').style.left = cx(11);
    for (let i = 8; i <= 10; i++) H.$('lv-c' + i).style.color = (Math.round(bi) === i && u > cue(3)) ? 'var(--green)' : 'var(--muted)';
  }
};
