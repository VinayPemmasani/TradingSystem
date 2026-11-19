// pcap timeline: packets at their recorded times. Faults row: what the injector did to each packet.
const PC_T = [0, 40, 55, 60, 150, 165, 170, 172, 175, 300, 420, 430, 600, 610, 615, 620, 625, 800, 1000, 1180, 1300, 1310, 1500, 1600];
SCENES['pcap'] = {
  setup() {
    const g = document.getElementById('pc-tl'); if (!g || g.children.length) return;
    PC_T.forEach((t, i) => { const d = document.createElement('div'); d.id = 'pc-' + i;
      d.style.cssText = `position:absolute;left:${t}px;top:30px;width:14px;height:80px;border-radius:4px;background:var(--blue);opacity:0`; g.appendChild(d); });
  },
  draw(u, cue) {
    const t0 = cue(2) + 0.2;
    PC_T.forEach((t, i) => { const d = document.getElementById('pc-' + i); if (d) d.style.opacity = u >= t0 + t / 700 ? 1 : 0; });
  }
};
const FL = ['ok', 'ok', 'drop', 'ok', 'ok', 'burst', 'burst', 'burst', 'ok', 'dup', 'ok', 'reorder', 'ok', 'ok', 'drop', 'ok'];
SCENES['faults'] = {
  setup() {
    const g = document.getElementById('fl-row'); if (!g || g.children.length) return;
    FL.forEach((f, i) => { const d = document.createElement('div'); d.className = 'msg'; d.id = 'fl-' + i;
      d.style.cssText = `position:absolute;left:${i * 104}px;top:0;width:96px;height:90px;font-size:20px;flex-direction:column;opacity:0`;
      d.innerHTML = `<span>#${41 + i}</span><span style="font-size:15px">${f === 'ok' ? '' : f}</span>`;
      if (f === 'drop' || f === 'burst') d.classList.add('lost');
      else d.style.background = f === 'dup' ? 'var(--pink)' : f === 'reorder' ? 'var(--amber)' : 'var(--blue)';
      g.appendChild(d); });
  },
  draw(u, cue) {
    FL.forEach((f, i) => { const d = document.getElementById('fl-' + i); if (d) d.style.opacity = Math.max(0, Math.min(1, (u - cue(1) - i * 0.18) / 0.3)); });
  }
};
