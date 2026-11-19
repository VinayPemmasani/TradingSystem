// SPSC ring with moving head/tail; Aeron log with one writer and three readers at their own positions.
SCENES['spsc'] = {
  setup() {
    const g = document.getElementById('sp-ring'); if (!g || g.children.length) return;
    for (let i = 0; i < 16; i++) { const d = document.createElement('div'); d.className = 'slot'; d.id = 'sp-' + i;
      d.style.cssText = `position:absolute;left:${i * 104}px;top:0;width:96px;height:80px;border-radius:10px;display:grid;place-items:center;font:600 18px var(--mono);color:#8ea3b1`;
      d.textContent = String(i); g.appendChild(d); }
  },
  draw(u, cue) {
    const t0 = cue(0) + 0.8;
    const head = u < t0 ? 0 : Math.floor((u - t0) / 0.45) + 1;
    const tail = u < t0 + 1.5 ? 0 : Math.floor((u - t0 - 1.5) / 0.5) + 1;
    const tl = Math.min(tail, head);
    for (let i = 0; i < 16; i++) { const d = document.getElementById('sp-' + i); if (!d) continue;
      let on = false; for (let s = tl; s < head; s++) if ((s & 15) === i) on = true; d.classList.toggle('on', on); d.style.color = on ? '#06141a' : '#8ea3b1'; }
    const h = document.getElementById('sp-head'), t = document.getElementById('sp-tail');
    if (h) h.style.left = Math.min(1540, 120 + (head & 15) * 104 + 20) + 'px';
    if (t) t.style.left = Math.min(1540, 120 + (tl & 15) * 104 + 20) + 'px';
  }
};
SCENES['aeron'] = {
  setup() {
    const g = document.getElementById('ae-log'); if (!g || g.children.length) return;
    for (let i = 0; i < 30; i++) { const d = document.createElement('div'); d.id = 'ae-' + i;
      d.style.cssText = `position:absolute;left:${i * 30}px;top:0;width:27px;height:110px;border-radius:5px;background:#13212b;border:1px solid #2c4351`;
      g.appendChild(d); }
  },
  draw(u, cue) {
    // writer advances one frame per step; readers trail it. From cue 4 reader C stalls,
    // and the writer stops 15 frames (half of the 30 drawn) ahead of it.
    const t0 = cue(1) + 0.5, step = (cue(4) - t0) / 16;
    const pos = (t) => t < t0 ? 0 : Math.floor((t - t0) / step);
    const cStall = Math.max(0, pos(cue(4)) - 10);
    let w = pos(u), c = Math.max(0, w - 10);
    if (u >= cue(4)) { c = cStall; w = Math.min(w, cStall + 15); }
    w = Math.min(w, 29);
    const r = [Math.max(0, w - 2), Math.max(0, w - 5), c];
    for (let i = 0; i < 30; i++) { const d = document.getElementById('ae-' + i); if (d) d.style.background = i < w ? 'var(--violet)' : '#13212b'; }
    const set = (id, x) => { const e = document.getElementById(id); if (e) e.style.left = (520 + x * 30) + 'px'; };
    set('ae-w', w); set('ae-pa', r[0]); set('ae-pb', r[1]); set('ae-pc', r[2]);
  }
};
