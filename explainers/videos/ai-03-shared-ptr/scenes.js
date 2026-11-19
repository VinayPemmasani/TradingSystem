// use_count walks 1 -> 5 as the chain descends, then back to 1 as copies are destroyed.
SCENES['cost'] = {
  draw(u, cue, H) {
    const a = cue(2), b = cue(3) - 0.2, step = (b - a) / 9;
    const k = u < a ? -1 : Math.min(8, Math.floor((u - a) / step));   // 0..3 copies, 4..7 destroys
    const n = k < 0 ? 1 : (k < 4 ? 2 + k : (k < 8 ? 4 - (k - 4) : 1));
    H.text('cc-n', String(k < 0 ? 1 : (k >= 8 ? 1 : n)));
    for (let i = 0; i < 4; i++) {
      const on = k >= i && k < 8 - i;
      const el = document.getElementById('cc-h' + i);
      el.style.opacity = u < cue(1) ? 0 : (on ? 1 : (k >= 8 - i ? 0.35 : (u >= a ? 0 : 0.35)));
      el.style.borderColor = on ? 'var(--red)' : 'var(--line)';
    }
    const op = document.getElementById('cc-op');
    if (k >= 0 && k < 8) { op.style.opacity = 1; op.textContent = k < 4 ? 'lock add +1' : 'lock add −1'; }
    else op.style.opacity = 0;
  }
};
