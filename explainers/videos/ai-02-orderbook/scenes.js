// Flat bid array: quantities per tick, best cursor moves on add-better and delete-best.
SCENES['hot'] = {
  draw(u, cue, H) {
    const base = {3: 4, 6: 2, 8: 6, 9: 3, 11: 5, 12: 2, 14: 7};   // index -> qty (hundreds)
    const q = Object.assign({}, base);
    let best = 14;
    const tAdd = cue(5) + 0.3, tDel = cue(6) + 0.4;
    if (u >= tAdd) { q[16] = 3; best = 16; }
    if (u >= tDel) { delete q[16]; const steps = Math.min(2, Math.floor((u - tDel) / 0.45)); best = 16 - steps; }
    for (let j = 0; j < 24; j++) {
      const el = document.getElementById('fb-c' + j); if (!el) continue;
      const v = q[j] || 0;
      el.textContent = v ? String(v * 100) : '0';
      el.style.color = v ? '#06141a' : '#4b6474';
      el.style.background = v ? (j === best ? 'var(--amber)' : 'var(--teal)') : '#0f1b23';
    }
    const c = document.getElementById('fb-cur');
    if (c) c.style.left = (190 + best * 62 - 14) + 'px';
  }
};
