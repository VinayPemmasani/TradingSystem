SCENES['tagvalue'] = { draw(u, cue) { const t0 = cue(4); const w = u < t0 ? 0 : Math.min(1680, (u - t0) * 700);
  const el = document.getElementById('tv-cursor'); el.style.width = w + 'px';
  const s = document.getElementById('tv-scan'); s.style.background = `repeating-linear-gradient(90deg,#1b2d38 0 26px,#0f1b23 26px 30px)`; } };
