// Ring head/tail movement and Aeron's frame_length commit, computed from u.
SCENES['ring'] = {
  draw(u, cue, H) {
    const n = 8, t1 = cue(1), t2 = cue(2);
    const rawH = u < t1 ? 0 : 1 + Math.floor((u - t1) / 0.6);
    const rawT = u < t2 ? 0 : Math.floor((u - t2) / 0.45);
    const tail = Math.max(0, Math.min(rawT, rawH - 1));
    const head = Math.min(rawH, tail + n);
    for (let j = 0; j < n; j++) {
      const el = document.getElementById('rg-s' + j); if (!el) continue;
      let on = false; for (let k = Math.max(0, tail); k < head; k++) if (k % n === j) on = true;
      el.classList.toggle('on', on);
    }
    const h = document.getElementById('rg-h'), t = document.getElementById('rg-t');
    if (h) h.style.left = (1270 + (head % n) * 68) + 'px';
    if (t) t.style.left = (1270 + (Math.max(0, tail) % n) * 68) + 'px';
  }
};

SCENES['aeron'] = {
  draw(u, cue, H) {
    const fl = document.getElementById('ae-fl'), v = document.getElementById('ae-v');
    let txt = 'frame_length = 0 (zeroed term)', col = 'var(--muted)', bg = '#5b6b75';
    if (u >= cue(1)) { txt = 'frame_length = −68 · not ready'; col = 'var(--red)'; bg = 'var(--red)'; }
    if (u >= cue(2) + 0.6) { txt = 'frame_length = +68 · committed'; col = 'var(--amber)'; bg = 'var(--amber)'; }
    if (v) { H.text(v, txt); v.style.color = col; }
    if (fl) fl.style.background = bg;
  }
};
