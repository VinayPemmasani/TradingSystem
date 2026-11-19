// Ownership ping-pong of the counters' line between the two cores; all from u.
const MCOL = { M: 'var(--amber)', E: 'var(--green)', S: 'var(--blue)', I: 'var(--red)' };
function badge(id, s) { const el = document.getElementById(id); if (!el) return; if (el.textContent !== s) el.textContent = s; el.style.background = MCOL[s]; }
SCENES['pingpong'] = {
  draw(u, cue, H) {
    const t0 = cue(1), P = 1.0;
    const n = u < t0 ? -1 : Math.floor((u - t0) / P);   // writes so far (alternating A, B)
    const f = u < t0 ? 0 : ((u - t0) % P) / P;
    const owner = n < 0 ? -1 : n % 2;                   // 0 = core 1, 1 = core 2
    badge('pp-b0', owner < 0 ? 'S' : (owner === 0 ? 'M' : 'I'));
    badge('pp-b1', owner < 0 ? 'S' : (owner === 1 ? 'M' : 'I'));
    for (let i = 0; i < 2; i++) { const l = document.getElementById('pp-l' + i); if (l) l.style.opacity = owner < 0 ? 1 : (owner === i ? 1 : 0.3); }
    const tok = document.getElementById('pp-tok');
    if (tok) {
      const to = owner === 0 ? 410 : 1510, from = owner === 0 ? 1510 : 410;
      tok.style.left = (owner < 0 ? 960 : H.lerp(from, to, H.ease(Math.min(1, f / 0.45)))) + 'px';
    }
    H.text('pp-c0', 'n[0] = ' + (n < 0 ? 0 : Math.floor(n / 2) + 1));
    H.text('pp-c1', 'n[1] = ' + (n < 1 ? 0 : Math.floor((n - 1) / 2) + 1));
    for (let j = 0; j < 26; j++) {
      const el = document.getElementById('pp-t' + j); if (!el) continue;
      const tj = t0 + j * P, show = Math.max(tj, cue(3) - 0.2);
      el.style.opacity = (u >= cue(3) - 0.2 && u >= tj) ? H.C((u - show) / 0.3) : 0;
    }
  }
};
