// MESI badge flip and the ping-pong of one cache line between two cores; all from u.
const MCOL = { M: 'var(--amber)', E: 'var(--green)', S: 'var(--blue)', I: 'var(--red)' };
function badge(id, s) {
  const el = document.getElementById(id); if (!el) return;
  if (el.textContent !== s) el.textContent = s;
  el.style.background = MCOL[s];
}

SCENES['mesi'] = {
  draw(u, cue) {
    const t = cue(5) + 0.9;
    badge('me-b0', u < t ? 'S' : 'M');
    badge('me-b1', u < t ? 'S' : 'I');
  }
};

SCENES['pingpong'] = {
  draw(u, cue, H) {
    const t0 = cue(3), P = 1.1;                      // one ownership move every P seconds
    const n = u < t0 ? -1 : Math.floor((u - t0) / P); // moves so far
    const f = u < t0 ? 0 : ((u - t0) % P) / P;
    // before the ping-pong: each core has written once, last writer core 2 owns it
    const owner = n < 0 ? 1 : (n % 2 === 0 ? 0 : 1);
    badge('pp-b0', n < 0 ? 'I' : (owner === 0 ? 'M' : 'I'));
    badge('pp-b1', n < 0 ? 'M' : (owner === 1 ? 'M' : 'I'));
    if (u < cue(2)) { badge('pp-b0', u < cue(1) ? 'E' : 'M'); badge('pp-b1', 'E'); }
    // the token travels from the previous owner to the new owner during the first 45% of each period
    const tok = document.getElementById('pp-tok');
    if (tok) {
      const from = owner === 0 ? 1230 : 690, to = owner === 0 ? 690 : 1230;
      const p = H.ease(Math.min(1, f / 0.45));
      tok.style.left = H.lerp(from, to, n < 0 ? 1 : p) + 'px';
      tok.style.top = '500px';
    }
    // counters tick on the owning core
    const ca = n < 0 ? (u >= cue(1) ? 1 : 0) : Math.ceil((n + 1) / 2) + 1;
    const cb = n < 0 ? (u >= cue(2) ? 1 : 0) : Math.floor((n + 1) / 2) + 1;
    H.text('pp-c0', 'a = ' + ca);
    H.text('pp-c1', 'b = ' + cb);
    // ownership timeline: block j appears once move j has happened (from cue 4)
    for (let j = 0; j < 28; j++) {
      const el = document.getElementById('pp-t' + j); if (!el) continue;
      const tj = t0 + j * P;
      el.style.opacity = (u >= cue(4) - 0.2 && u >= tj) ? H.C((u - Math.max(tj, cue(4) - 0.2)) / 0.3) : 0;
    }
  }
};
