// One price per step through the indirect call, four per step once inlined and vectorized.
SCENES['machine'] = {
  draw(u, cue) {
    const ta = cue(2) + 0.6, tb = cue(3) + 0.6, step = 0.14;
    const na = u < ta ? 0 : Math.min(64, Math.floor((u - ta) / step) + 1);
    const nb = u < tb ? 0 : Math.min(64, 4 * (Math.floor((u - tb) / step) + 1));
    for (let i = 0; i < 64; i++) {
      const A = document.getElementById('m8a-' + i), B = document.getElementById('m8b-' + i);
      if (A) A.classList.toggle('on-a', i < na);
      if (B) B.classList.toggle('on-b', i < nb);
    }
  }
};
