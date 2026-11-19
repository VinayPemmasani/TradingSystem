// Pool free list, arena bump pointer, page prefaulting: all computed from u.
SCENES['pool'] = {
  draw(u, cue, H) {
    // ops: get, get, get, put(1), get, get, put(0), get ... ; slots used in a fixed script
    const script = [['g', 0], ['g', 1], ['g', 2], ['p', 1], ['g', 1], ['g', 3], ['p', 0], ['g', 0], ['g', 4], ['p', 3], ['g', 3], ['g', 5]];
    const t0 = cue(1), n = u < t0 ? 0 : Math.min(script.length, 1 + Math.floor((u - t0) / 0.7));
    const used = new Set(); const free = [0, 1, 2, 3, 4, 5, 6, 7];
    for (let k = 0; k < n; k++) { const [op, s] = script[k]; if (op === 'g') { used.add(s); free.splice(free.indexOf(s), 1); } else { used.delete(s); free.unshift(s); } }
    for (let j = 0; j < 8; j++) { const el = document.getElementById('pl-s' + j); if (el) el.classList.toggle('on', used.has(j)); }
    const f = document.getElementById('pl-f'); if (f) f.style.left = (1300 + (free[0] ?? 7) * 62) + 'px';
  }
};

SCENES['arena'] = {
  draw(u, cue, H) {
    const t0 = cue(1) + 0.4, tr = cue(2) + 1.0;
    let w = u < t0 ? 0 : Math.min(1300, Math.floor((u - t0) / 0.35) * 50);
    if (u >= tr) w = Math.max(0, (u < cue(3) ? 0 : Math.min(1450, Math.floor((u - cue(3)) / 0.08) * 50)));
    const f = document.getElementById('ar-fill'), p = document.getElementById('ar-p');
    if (f) f.style.width = w + 'px';
    if (p) p.style.left = (120 + w - 10) + 'px';
  }
};

SCENES['pages'] = {
  draw(u, cue, H) {
    const t0 = cue(1) + 0.3;
    const n = u < t0 ? 0 : Math.min(16, 1 + Math.floor((u - t0) / 0.18));
    for (let j = 0; j < 16; j++) { const el = document.getElementById('pg-' + j); if (el) el.classList.toggle('on', j < n); }
    H.text('pg-lab', n === 16 ? 'touched at startup: every page is mapped before trading starts' : 'not mapped yet: the first write to each page faults');
  }
};
