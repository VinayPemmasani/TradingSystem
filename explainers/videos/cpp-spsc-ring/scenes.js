// Ring animations: occupied slots lie between tail and head (mod 8); all from u alone.
function ringDraw(prefix, n, head, tail, x0, step, hp, tp) {
  for (let j = 0; j < n; j++) {
    const el = document.getElementById(prefix + j);
    if (!el) continue;
    let on = false;
    for (let k = tail; k < head; k++) if (k % n === j) { on = true; break; }
    el.classList.toggle('on', on);
  }
  const h = document.getElementById(hp), t = document.getElementById(tp);
  if (h) h.style.left = (x0 + (head % n) * step + 4) + 'px';
  if (t) t.style.left = (x0 + (tail % n) * step + 4) + 'px';
}

SCENES['layout'] = {
  draw(u, cue, H) {
    const t0 = cue(2) + 0.6;
    const k = Math.max(0, Math.floor((u - t0) / 0.55));
    const head = k;
    const tail = Math.max(0, k - 2 - (Math.floor(k / 3) % 4));
    ringDraw('ly-s', 8, head, tail, 160, 100, 'ly-head', 'ly-tail');
    H.text('ly-cnt', `head ${head} · tail ${tail} · used ${head - tail} of 8`);
  }
};

SCENES['pop'] = {
  draw(u, cue) {
    const t0 = cue(0) + 1.0;
    const k = Math.max(0, Math.floor((u - t0) / 0.6));
    const head = 5 + k + (Math.floor(k / 4) % 2);
    const tail = Math.min(head, Math.max(0, k * 1 + (Math.floor(k / 5) % 3)));
    ringDraw('pp-s', 8, head, tail, 160, 100, 'pp-head', 'pp-tail');
  }
};
