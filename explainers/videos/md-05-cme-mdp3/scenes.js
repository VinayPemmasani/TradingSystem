function md5Ladder(el, rows, hl) { let h = '';
  rows.forEach((r, i) => { if (!r) { h += `<div style="position:absolute;left:0;top:${i * 80}px;width:880px;height:64px;border:2px dashed #2c4351;border-radius:8px"></div>`; return; }
    const c = hl === i ? '#ffb347' : '#4fd18b';
    h += `<div class="lbl" style="position:absolute;left:0;top:${i * 80 + 18}px">L${i + 1}</div><div class="lvl" style="position:absolute;left:60px;top:${i * 80}px;height:64px;width:${120 + r[1] * 9}px;background:${c};font-size:26px">${r[0]} × ${r[1]}</div>`; });
  el.innerHTML = h; }
SCENES['example'] = { draw(u, cue) {
  let rows = [['4123.25', 20], ['4122.75', 35], ['4122.50', 50], ['4122.25', 40], ['4122.00', 60]], hl = -1;
  if (u >= cue(2) + 0.5) { rows[0] = ['4123.25', 25]; hl = 0; }
  if (u >= cue(3) + 0.8) { rows = [rows[0], ['4123.00', 15], rows[1], rows[2], rows[3]]; hl = 1; }
  if (u >= cue(4) + 0.8) { rows = [rows[1], rows[2], rows[3], rows[4], null]; hl = -1; }
  md5Ladder(document.getElementById('e5-book'), rows, hl); } };
SCENES['title'] = { draw(u, cue) { const t = u - cue(2);
  md5Ladder(document.getElementById('t5-book'), [['4123.25', Math.round(20 + 5 * Math.sin(t * 2))], ['4122.75', 30], ['4122.50', 22]], -1);
  document.getElementById('t5-book').style.transform = 'scale(0.45)'; document.getElementById('t5-book').style.transformOrigin = '0 0'; } };
SCENES['recovery'] = {
  setup() { const q = document.getElementById('r5-q'); let h = '';
    for (let i = 0; i < 12; i++) h += `<div class="chip" id="r5c${i}" style="position:absolute;left:${i * 140}px;top:10px;width:128px;font-size:22px;background:#3fd0dc">${5000 + i}</div>`;
    q.innerHTML = h; },
  draw(u, cue) { for (let i = 0; i < 12; i++) { const el = document.getElementById('r5c' + i); const n = 5000 + i;
    el.style.opacity = u >= cue(1) + i * 0.25 ? 1 : 0;
    let bg = '#3fd0dc';
    if (u >= cue(4)) bg = n < 5004 ? '#ff6b5e' : '#3fd0dc';
    if (u >= cue(5) && n >= 5004) bg = '#4fd18b';
    el.style.background = bg; el.style.opacity = (u >= cue(4) + 0.6 && n < 5004) ? 0.25 : el.style.opacity; } }
};
