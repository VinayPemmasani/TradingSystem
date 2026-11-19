SCENES['example'] = {
  setup() { let h = ''; for (let i = 0; i < 120; i++) { const x = (i % 30) * 56, y = Math.floor(i / 30) * 50;
    h += `<div style="position:absolute;left:${x}px;top:${y}px;width:46px;height:40px;border-radius:6px;background:#3fd0dc" data-k="${i}"></div>`; }
    document.getElementById('k9-grid').innerHTML = h; },
  draw(u, cue) { const t0 = cue(3) + 0.6; document.querySelectorAll('#k9-grid div').forEach((el) => {
    const k = +el.dataset.k; const on = u > t0 + k * 0.025; el.style.background = on ? '#2a3a45' : '#3fd0dc'; el.style.opacity = on ? 0.5 : 1; }); } };
