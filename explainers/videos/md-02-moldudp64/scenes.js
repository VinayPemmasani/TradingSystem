SCENES['title'] = {
  setup() { const r = document.getElementById('t2-row'); let h = '';
    for (let i = 0; i < 14; i++) h += `<div class="chip" data-i="${i}" style="position:absolute;top:40px;width:110px;font-size:24px;background:#3fd0dc">${101 + i}</div>`;
    r.innerHTML = h; },
  draw(u, cue) { const lossOn = u >= cue(1);
    document.querySelectorAll('#t2-row .chip').forEach((el) => { const i = +el.dataset.i; let x = 140 + i * 130 - ((u * 40) % 130);
      el.style.left = x + 'px'; const n = 101 + i;
      let bg = '#3fd0dc', top = 40, op = 1;
      if (lossOn && n === 105) { bg = 'transparent'; el.style.border = '2px dashed #ff6b5e'; el.style.color = '#ff6b5e'; } else { el.style.border = ''; el.style.color = '#06141a'; }
      if (lossOn && n === 108) { bg = '#ffb347'; top = 0; }
      if (lossOn && n === 111) { bg = '#a98bff'; top = 80; }
      el.style.background = bg; el.style.top = top + 'px'; el.style.opacity = op; }); }
};
SCENES['gap'] = {
  setup() { const c = document.getElementById('g2-cells'); let h = '';
    for (let i = 0; i < 15; i++) h += `<div class="chip" id="g2c${i}" style="position:absolute;left:${i * 112}px;top:20px;width:100px;font-size:22px">${1001 + i}</div>`;
    c.innerHTML = h; },
  draw(u, cue) { for (let i = 0; i < 15; i++) { const n = 1001 + i, el = document.getElementById('g2c' + i);
      let st = 'none';
      if (n <= 1003) st = 'ok';
      if (n >= 1010 && u >= cue(0) + 0.5) st = 'held';
      if (n >= 1004 && n <= 1009 && u >= cue(1)) st = 'miss';
      if (u >= cue(3) + 1.6) st = 'ok';
      el.style.border = st === 'miss' ? '2px dashed #ff6b5e' : '2px solid transparent';
      el.style.background = st === 'ok' ? '#4fd18b' : st === 'held' ? '#ffb347' : st === 'miss' ? 'transparent' : '#13212b';
      el.style.color = st === 'miss' ? '#ff6b5e' : st === 'none' ? '#8ea3b1' : '#06141a'; } }
};
