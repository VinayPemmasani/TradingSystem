// Example: bid ladder and order map after each message. Map: slot grid of live refs.
const EX_STATES = [
  null,                                                          // cue 0
  { lv: [['50.10', [['11', 300]]]] },                            // cue 1
  { lv: [['50.10', [['11', 300], ['12', 200]]]] },               // cue 2
  null,                                                          // cue 3 (same)
  { lv: [['50.10', [['11', 200], ['12', 200]]]] },               // cue 4
  { lv: [['50.11', [['13', 200]]], ['50.10', [['11', 200]]]] },  // cue 5
  null,
  { lv: [['50.11', [['13', 200]]]] },                            // cue 7
];
SCENES['example'] = {
  draw(u, cue, H) {
    let st = null;
    for (let k = 0; k < EX_STATES.length; k++) if (EX_STATES[k] && u >= cue(k) + 0.4) st = EX_STATES[k];
    const ords = [];
    for (let i = 0; i < 2; i++) {
      const L = st && st.lv[i];
      const r = document.getElementById('ex-r' + i), b = document.getElementById('ex-b' + i), c = document.getElementById('ex-c' + i);
      if (!L) { r.style.opacity = 0; b.style.opacity = 0; c.style.opacity = 0; continue; }
      const sh = L[1].reduce((a, o) => a + o[1], 0);
      H.text(r, L[0]); r.style.opacity = 1;
      b.style.opacity = 1; b.style.width = (sh * 1.3) + 'px'; H.text(b, sh + ' sh');
      c.style.opacity = 1; H.text(c, L[1].length + (L[1].length === 1 ? ' order' : ' orders') + ': ' + L[1].map(o => '#' + o[0] + ' ' + o[1]).join(', '));
      for (const o of L[1]) ords.push([o[0], L[0], o[1]]);
    }
    ords.sort((a, b) => a[0] - b[0]);
    H.text('ex-map', ords.map(o => `${o[0]} → { price ${Math.round(parseFloat(o[1]) * 10000)}, shares ${o[2]}, buy }`).join('\n'));
  }
};
SCENES['map'] = {
  setup() {
    const g = document.getElementById('mp-grid'); if (!g || g.children.length) return;
    for (let i = 0; i < 16; i++) {
      const d = document.createElement('div'); d.className = 'msg'; d.id = 'mp-' + i;
      d.style.cssText = `position:absolute;left:${i * 105}px;top:0;width:98px;height:80px;font-size:21px;flex-direction:column;background:#13212b;border:2px solid #2c4351;color:#8ea3b1`;
      g.appendChild(d);
    }
  },
  draw(u, cue, H) {
    // live window of refs [lo, lo+9) slides forward one ref every 0.6 s after cue 3
    const lo = 1000 + (u < cue(3) ? 0 : Math.floor((u - cue(3)) / 0.6));
    for (let i = 0; i < 16; i++) {
      const d = document.getElementById('mp-' + i); if (!d) continue;
      let key = -1;
      for (let r = lo; r < lo + 9; r++) if ((r & 15) === i && u >= cue(1)) key = r;
      if (key >= 0) { d.style.background = 'var(--amber)'; d.style.color = '#06141a'; d.innerHTML = `<span style="font-size:15px">slot ${i}</span>${key}`; }
      else { d.style.background = '#13212b'; d.style.color = '#8ea3b1'; d.innerHTML = `<span style="font-size:15px">slot ${i}</span>·`; }
    }
  }
};
