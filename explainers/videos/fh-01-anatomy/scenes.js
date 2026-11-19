// Ring occupancy in the pipeline scene: the rx thread fills slots; once the book thread
// appears (cue 4) it drains them, so a window of 2-4 filled slots walks around the ring.
SCENES['pipeline'] = {
  draw(u, cue) {
    const t0 = cue(3) + 0.5, tc = cue(4) + 0.3;
    const head = u < t0 ? 0 : Math.floor((u - t0) / 0.3) + 1;
    const tail = u < tc ? 0 : Math.max(0, head - 2 - (Math.floor((u - tc) / 0.9) % 3));
    for (let j = 0; j < 8; j++) {
      const el = document.getElementById('r1-' + j); if (!el) continue;
      let on = false;
      for (let s = tail; s < Math.min(head, tail + 8); s++) if (s % 8 === j) on = true;
      el.classList.toggle('on', on);
    }
  }
};
