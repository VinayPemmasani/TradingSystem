// Title: an illustrative rate profile with an opening burst and microbursts. Why: queue grows in a burst, then drains.
const PROF = (() => { const a = []; let s = 7; const r = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 80; i++) { let v = 0.12 + 0.08 * r(); if (i >= 6 && i < 12) v = 0.95 - (i - 6) * 0.1 + 0.05 * r(); if (i === 31 || i === 52 || i === 53) v = 0.7 + 0.2 * r(); if (i > 72) v = 0.35 + 0.3 * r(); a.push(v); } return a; })();
SCENES['title'] = {
  setup() {
    const g = document.getElementById('ti-bars'); if (!g || g.children.length) return;
    PROF.forEach((v, i) => { const d = document.createElement('div'); d.id = 'tb-' + i;
      d.style.cssText = `position:absolute;left:${i * 20.5}px;bottom:0;width:16px;height:0;border-radius:3px;background:${v > 0.5 ? 'var(--red)' : 'var(--blue)'}`; g.appendChild(d); });
  },
  draw(u, cue) {
    PROF.forEach((v, i) => { const d = document.getElementById('tb-' + i); if (!d) return;
      const p = Math.max(0, Math.min(1, (u - cue(0) - 0.8 - i * 0.03) / 0.4)); d.style.height = (v * 250 * p) + 'px'; });
  }
};
SCENES['why'] = {
  draw(u, cue, H) {
    // arrivals exceed drain between t1 and t2, then queue drains
    const t1 = cue(1) + 0.3, t2 = cue(1) + 2.8;
    let q = 0;
    if (u > t1) q = Math.min(u, t2) - t1;          // grows at 1/s
    if (u > t2) q = Math.max(0, q - (u - t2) * 0.6); // drains slower
    const el = document.getElementById('wy-q'); if (el) el.style.width = Math.min(868, q * 340) + 'px';
    H.text('wy-in', u > t1 && u < t2 ? 'rate: BURST' : 'rate: normal');
  }
};
