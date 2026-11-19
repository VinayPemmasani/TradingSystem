SCENES['cme'] = { draw(u, cue, H) {
  // count up to 1,500 by cue 1, hold, then to 2,250 at cue 3
  let n = 0; const a = cue(0) + 0.5, b = cue(1), c = cue(3);
  if (u > a) n = Math.min(1500, (u - a) / Math.max(0.5, b - a) * 1500);
  if (u > c) n = 1500 + Math.min(750, (u - c) / 1.2 * 750);
  n = Math.round(n);
  document.getElementById('t8-fill').style.width = (n / 2500 * 1676) + 'px';
  document.getElementById('t8-fill').style.background = n >= 2250 ? '#ff6b5e' : n >= 1500 ? '#ffb347' : '#3fd0dc';
  H.text('t8-n', n.toLocaleString('en-US') + ' messages'); } };
SCENES['bucket'] = { draw(u, cue, H) {
  let t = 0; const c1 = cue(1), c4 = cue(4), c5 = cue(5);
  if (u > c1) t = Math.min(100, (u - c1) / 2 * 100);
  if (u > c5) { const d = u - c5; t = d < 1 ? 100 * (1 - d) : Math.min(50, (d - 1) / 1.5 * 50); }
  t = Math.round(t);
  document.getElementById('t8-lvl').style.height = (t / 100 * 480) + 'px';
  document.getElementById('t8-lvl').style.top = (796 - t / 100 * 480) + 'px';
  H.text('t8-tok', String(t)); } };
