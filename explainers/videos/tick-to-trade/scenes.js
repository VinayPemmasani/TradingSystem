// Ring animations: occupied slots between tail and head, computed from u alone.
function ringFill(prefix, n, head, tail, cls) {
  for (let j = 0; j < n; j++) {
    const el = document.getElementById(prefix + j);
    if (!el) continue;
    let on = false;
    for (let k = tail; k < head; k++) if (((k % n) + n) % n === j) { on = true; break; }
    el.classList.toggle(cls, on);
  }
}

SCENES['rx'] = {
  draw(u, cue) {
    const t0 = cue(2) + 0.8;
    const head = Math.max(0, Math.floor((u - t0) / 0.22));
    const tail = Math.max(0, head - 6);
    ringFill('rx-slot', 16, head, tail, 'on');
  }
};

SCENES['seq'] = {
  draw(u, cue) {
    const t0 = cue(0) + 0.8;
    const head = Math.max(0, Math.floor((u - t0) / 0.45));
    const tail = Math.max(0, head - 3 - (Math.floor((u - t0) / 1.7) % 2));
    ringFill('sq-slot', 12, head, tail, 'on');
    const h = document.getElementById('sq-head'), t = document.getElementById('sq-tail');
    if (h) h.style.left = (460 + (head % 12) * 85) + 'px';
    if (t) t.style.left = (460 + (tail % 12) * 85) + 'px';
  }
};
