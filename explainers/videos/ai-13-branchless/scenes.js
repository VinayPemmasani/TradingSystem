
SCENES['cost'] = { draw(u, cue, H) {
  const t0 = cue(0) + 0.3, tf = cue(2) + 0.3;
  for (let i = 0; i < 15; i++) {
    const el = document.getElementById('cs-' + i);
    let vis = H.C((u - (t0 + 0.12 * i)) / 0.25);
    let bg = i < 5 ? '#4b6b7a' : i === 5 ? 'var(--amber)' : '#2a8f99', bd = bg;
    if (i > 5 && u > tf) {
      if (u < tf + 1.0) { bg = 'var(--red)'; bd = bg; }
      else if (u < tf + 1.6 + 0.12 * (i - 6)) { vis = 0.25; bg = '#0f1b23'; bd = 'var(--red)'; }
      else { bg = '#2a8f99'; bd = bg; vis = H.C((u - (tf + 1.6 + 0.12 * (i - 6))) / 0.25); }
    }
    el.style.opacity = vis; el.style.background = bg; el.style.borderColor = bd;
  }
}};
