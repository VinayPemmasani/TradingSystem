// Histogram bucket layout: 0..63 exact, then each power of two split into 32 buckets.
SCENES['histogram'] = {
  setup() {
    const g = document.getElementById('hg-axis'); if (!g || g.children.length) return;
    const segs = ['0 – 63', '64 – 127', '128 – 255', '256 – 511', '512 – 1023', '…'];
    segs.forEach((lab, k) => {
      const x = k * 280, d = document.createElement('div');
      d.style.cssText = `position:absolute;left:${x}px;top:0;width:270px;height:120px;border-radius:10px;background:${k === 0 ? '#173a2c' : '#13212b'};border:2px solid ${k === 0 ? 'var(--green)' : 'var(--line)'};overflow:hidden`;
      d.id = 'hg-' + k;
      if (k < 5) for (let i = 1; i < 32; i++) { const t = document.createElement('div'); t.style.cssText = `position:absolute;left:${i * 270 / 32}px;top:${k === 0 ? 60 : 30}px;width:1px;height:${k === 0 ? 30 : 60}px;background:${k === 0 ? '#4fd18b' : '#6aa8ff'};opacity:.8`; d.appendChild(t); }
      const l = document.createElement('div'); l.style.cssText = `position:absolute;left:${x}px;top:135px;width:270px;text-align:center;font:600 20px var(--mono);color:#8ea3b1`; l.textContent = lab;
      g.appendChild(d); g.appendChild(l);
    });
  },
  draw(u, cue) {
    for (let k = 0; k < 6; k++) { const d = document.getElementById('hg-' + k); if (d) d.style.opacity = Math.max(0, Math.min(1, (u - cue(1) - k * 0.35) / 0.4)); }
  }
};
