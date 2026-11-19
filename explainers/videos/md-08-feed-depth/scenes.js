function md8Levels(el, rows, n) { let h = '';
  rows.slice(0, n).forEach((r, i) => { const c = r[2] === 'b' ? '#4fd18b' : '#ff6b5e';
    h += `<div class="lvl" style="position:absolute;left:0;top:${i * 62}px;height:52px;width:${140 + r[1] * 0.9}px;background:${c};font-size:24px">${r[0]} × ${r[1]}</div>`; });
  el.innerHTML = h; }
const MD8 = [['189.30', 500, 'a'], ['189.29', 300, 'a'], ['189.28', 700, 'a'], ['189.27', 400, 'a'], ['189.25', 600, 'b'], ['189.24', 350, 'b'], ['189.23', 800, 'b'], ['189.22', 250, 'b']];
SCENES['l1'] = { draw(u, cue) { const el = document.getElementById('l1-hidden'); if (el.dataset.k) return; el.dataset.k = 1;
  let h = ''; for (let i = 0; i < 6; i++) h += `<div style="position:absolute;left:${i * 165}px;top:40px;width:150px;height:120px;border-radius:10px;border:2px dashed #3c5463;display:grid;place-items:center;font:700 40px var(--mono);color:#3c5463">?</div>`; el.innerHTML = h; } };
SCENES['l2'] = { draw(u, cue) { const n = Math.max(0, Math.min(8, Math.floor((u - 0.3) / 0.25))); const el = document.getElementById('l2-book');
  if (el.dataset.n !== String(n)) { md8Levels(el, MD8, n); el.dataset.n = n; } } };
SCENES['l3'] = { draw(u, cue) { const el = document.getElementById('l3-book'); const n = Math.max(0, Math.min(5, Math.floor((u - 0.3) / 0.3)));
  if (el.dataset.n === String(n)) return; el.dataset.n = n;
  const Q = [['189.27', [100, 200, 100]], ['189.25', [300, 100, 200]], ['189.24', [150, 200]], ['189.23', [500, 100, 200]], ['189.22', [250]]];
  let h = ''; Q.slice(0, n).forEach((q, i) => { const c = i === 0 ? '#ff6b5e' : '#4fd18b'; h += `<div class="lbl" style="position:absolute;left:0;top:${i * 100 + 30}px">${q[0]}</div>`;
    let x = 140; q[1].forEach((s, j) => { const w = 60 + s * 0.8; h += `<div class="lvl" style="position:absolute;left:${x}px;top:${i * 100 + 10}px;height:64px;width:${w}px;background:${c};font-size:20px">#${i * 10 + j + 1} · ${s}</div>`; x += w + 12; }); });
  el.innerHTML = h; } };
SCENES['example'] = { draw(u, cue, H) { const gone = u >= cue(4) + 0.6;
  const el = document.getElementById('ex8-l3'); const k = gone ? 'g' : 'a'; if (el.dataset.k !== k) { el.dataset.k = k;
    const O = [['A', 300], ['B', 100], ['C', 200]]; let h = '', x = 0;
    O.forEach((o) => { const w = 170 + o[1] * 1.2; const dead = gone && o[0] === 'B';
      h += `<div class="lvl" style="position:absolute;left:${x}px;top:0;height:90px;width:${w}px;background:${dead ? 'transparent' : '#a98bff'};border:${dead ? '3px dashed #ff6b5e' : 'none'};color:${dead ? '#ff6b5e' : '#06141a'};font-size:26px">order ${o[0]} · ${o[1]}</div>`; x += w + 16; });
    el.innerHTML = h; }
  H.text('ex8-l2', gone ? '189.25 × 500 · 2 orders' : '189.25 × 600 · 3 orders');
  H.text('ex8-l1', gone ? 'bid 189.25 × 500' : 'bid 189.25 × 600'); } };
