// Ring in "later": head runs ahead (hot thread writes), tail chases in bursts (writer drains).
SCENES['later'] = {
  draw(u, cue) {
    const t0 = cue(0) + 0.8, n = 12;
    const w = Math.max(0, Math.floor((u - t0) / 0.35));            // records written
    const t1 = cue(1);
    let r = 0;                                                      // records drained
    if (u >= t1) r = Math.min(w, Math.floor((u - t1) / 1.4) * 5);   // drains 5 at a time
    for (let i = 0; i < n; i++) {
      const el = document.getElementById('la-s' + i); if (!el) continue;
      // slot i is full if some k in [r, w) has k % n == i
      let full = false;
      for (let k = r; k < w; k++) if (k % n === i) { full = true; break; }
      el.classList.toggle('on', full);
    }
    const h = document.getElementById('la-h'), t = document.getElementById('la-t');
    if (h) h.style.left = (450 + (w % n) * 62) + 'px';
    if (t) t.style.left = (450 + (r % n) * 62) + 'px';
  }
};
