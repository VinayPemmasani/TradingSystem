SCENES['count'] = { draw(u, cue, H) { const t0 = cue(1); const n = u < t0 ? 0 : Math.min(41999, Math.floor(Math.pow((u - t0) / 4, 2) * 41999) + 1);
  const s = n.toLocaleString('en-US'); H.text('c3-a', s); H.text('c3-b', s); } };
SCENES['heart'] = {
  setup() { const el = document.getElementById('h3-ticks'); let h = '';
    for (let i = 0; i < 7; i++) { h += `<div class="chip" style="position:absolute;left:${300 + i * 210}px;top:255px;width:56px;height:56px;font-size:26px;background:#a98bff" data-k="s${i}">H</div>`;
      h += `<div class="chip" style="position:absolute;left:${400 + i * 210}px;top:435px;width:56px;height:56px;font-size:26px;background:#3fd0dc" data-k="c${i}">R</div>`; }
    h += '<div class="lbl" style="position:absolute;left:300px;top:340px">1 s without sending anything → heartbeat</div>';
    el.innerHTML = h; },
  draw(u) { document.querySelectorAll('#h3-ticks .chip').forEach((el) => { const i = +el.dataset.k.slice(1);
    el.style.opacity = u > 0.4 + i * 0.7 ? 1 : 0; }); }
};
