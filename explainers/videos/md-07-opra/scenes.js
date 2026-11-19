SCENES['why'] = { draw(u, cue) { const t = u - cue(1) - 0.3; const el = document.getElementById('w7-tree');
  const n = Math.max(0, Math.min(6 * 12, Math.floor(t * 14))); if (el.dataset.n === String(n)) return; el.dataset.n = n;
  let h = '';
  for (let e = 0; e < 6; e++) h += `<div class="lbl" style="position:absolute;left:0;top:${e * 90 + 14}px">exp ${e + 1}</div>`;
  for (let k = 0; k < n; k++) { const e = Math.floor(k / 12), s = k % 12;
    h += `<div style="position:absolute;left:${110 + s * 64}px;top:${e * 90}px;width:26px;height:50px;border-radius:5px;background:#4fd18b"></div><div style="position:absolute;left:${138 + s * 64}px;top:${e * 90}px;width:26px;height:50px;border-radius:5px;background:#ff6b5e"></div>`; }
  h += '<div class="lbl" style="position:absolute;left:110px;top:545px">strikes →  · green call · red put (illustrative)</div>';
  el.innerHTML = h; } };
SCENES['lines'] = { setup() { let h = ''; for (let i = 0; i < 96; i++) h += `<div class="ln" id="l7-${i}" style="position:absolute;left:${(i % 12) * 74}px;top:${Math.floor(i / 12) * 66}px;width:64px;height:56px;border-radius:8px;background:#18303c;font:600 18px var(--mono);color:#8ea3b1;display:grid;place-items:center">${i + 1}</div>`;
  document.getElementById('l7-grid').innerHTML = h; },
  draw(u) { for (let i = 0; i < 96; i++) { const v = Math.sin(u * 3 + i * 1.7) * Math.sin(u * 1.3 + i * 0.6); const el = document.getElementById('l7-' + i);
    el.style.background = v > 0.45 ? '#ffb347' : v > 0 ? '#2a8f99' : '#18303c'; el.style.color = v > 0 ? '#06141a' : '#8ea3b1'; } } };
SCENES['lab'] = { draw(u, cue) { const t0 = cue(0) + 0.3; const n = Math.max(0, Math.min(40, Math.floor((u - t0) / 0.15)));
  const inn = document.getElementById('c7-in'), out = document.getElementById('c7-out');
  if (inn.dataset.n !== String(n)) { let h = ''; for (let i = 0; i < n; i++) h += `<div style="position:absolute;left:${i * 42}px;top:10px;width:32px;height:60px;border-radius:6px;background:#3fd0dc"></div>`; inn.innerHTML = h; inn.dataset.n = n; }
  const m = u < cue(2) ? 0 : Math.min(8, Math.floor(n / 5)); if (out.dataset.n !== String(m)) { let h = ''; for (let i = 0; i < m; i++) h += `<div style="position:absolute;left:${i * 210 + 168}px;top:10px;width:32px;height:60px;border-radius:6px;background:#ffb347"></div>`; out.innerHTML = h; out.dataset.n = m; } } };
