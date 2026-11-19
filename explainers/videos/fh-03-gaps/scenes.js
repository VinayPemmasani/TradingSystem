// Detect scene: a row of sequence numbers 2001..2016 with expected and high-water pointers.
SCENES['detect'] = {
  setup() {
    const row = document.getElementById('dt-row'); if (!row || row.children.length) return;
    for (let i = 0; i < 16; i++) {
      const d = document.createElement('div'); d.className = 'msg'; d.id = 'dt-' + i;
      d.style.cssText = `position:absolute;left:${i * 104}px;top:0;width:96px;font-size:22px;background:#2c4351;color:#e6eef2`;
      d.textContent = String(2001 + i); row.appendChild(d);
    }
  },
  draw(u, cue) {
    for (let i = 0; i < 16; i++) {
      const d = document.getElementById('dt-' + i); if (!d) continue;
      let bg = '#2c4351', col = '#e6eef2', lost = false;
      if (u >= cue(1) && i < 6) { bg = 'var(--green)'; col = '#06141a'; }
      if (u >= cue(2) && i >= 6 && i <= 8) lost = true;
      if (u >= cue(3) && i >= 9 && i <= 13) { bg = 'var(--amber)'; col = '#06141a'; }
      d.classList.toggle('lost', lost);
      d.style.background = lost ? 'transparent' : bg; d.style.color = lost ? '' : col;
    }
    const e = document.getElementById('dt-exp'), h = document.getElementById('dt-high');
    if (e) e.style.left = (120 + 6 * 104 + 10) + 'px';
    if (h) h.style.left = (120 + 14 * 104 + 10) + 'px';
  }
};
