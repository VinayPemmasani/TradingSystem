// Directory stream at the start of the day; timeline for the late-joiner scene.
const DR = [['R', 1, 'A'], ['R', 2, 'AA'], ['R', 3, 'AAL'], ['R', 4, 'AAPB'], ['R', 5, 'AAME'], ['R', '…', '…'], ['S', 0, 'Q'], ['A', 13, ''], ['E', 13, ''], ['A', 2, ''], ['X', 4, '']];
SCENES['directory'] = {
  setup() {
    const g = document.getElementById('dr-feed'); if (!g || g.children.length) return;
    DR.forEach((m, i) => {
      const d = document.createElement('div'); d.className = 'msg'; d.id = 'dr-' + i;
      const bg = m[0] === 'R' ? 'var(--violet)' : m[0] === 'S' ? '#cfd8de' : 'var(--green)';
      d.style.cssText = `position:absolute;left:${i * 152}px;top:40px;width:144px;height:110px;flex-direction:column;font-size:21px;background:${bg};opacity:0`;
      d.innerHTML = `<span>${m[0]} · ${m[1]}</span><span style="font-size:18px">${m[2] ? '"' + m[2] + '"' : '&nbsp;'}</span>`;
      g.appendChild(d);
    });
  },
  draw(u, cue) {
    DR.forEach((m, i) => { const d = document.getElementById('dr-' + i); if (d) d.style.opacity = Math.max(0, Math.min(1, (u - cue(1) - 0.3 - i * 0.35) / 0.3)); });
  }
};
SCENES['late'] = {
  setup() {
    const g = document.getElementById('lt-tl'); if (!g || g.children.length) return;
    g.innerHTML = `<div style="position:absolute;left:0;top:30px;width:330px;height:60px;border-radius:10px;background:var(--violet);color:#06141a;font:700 22px var(--mono);display:grid;place-items:center">R R R R … directory</div>
      <div style="position:absolute;left:340px;top:30px;width:1340px;height:60px;border-radius:10px;background:repeating-linear-gradient(90deg,var(--green) 0 60px,#2f8a5b 60px 66px);"></div>
      <div id="lt-join" style="position:absolute;left:900px;top:0;width:4px;height:120px;background:var(--amber);opacity:0"></div>
      <div id="lt-jl" style="position:absolute;left:915px;top:96px;font:700 20px var(--mono);color:var(--amber);opacity:0;white-space:nowrap">joins here</div>`;
  },
  draw(u, cue) {
    const p = Math.max(0, Math.min(1, (u - cue(2)) / 0.4));
    for (const id of ['lt-join', 'lt-jl']) { const e = document.getElementById(id); if (e) e.style.opacity = p; }
  }
};
