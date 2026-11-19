// example: A loses 102, B loses 104. For each packet: arrival times on A and B (null = lost).
const EX9 = [[101, 0.0, 0.25], [102, null, 0.0], [103, 0.0, 0.3], [104, 0.0, null], [105, 0.1, 0.0]];
SCENES['example'] = { draw(u, cue) { const el = document.getElementById('ex9');
  const cues = [cue(3), cue(4), cue(5), cue(6), cue(6) + 1.2];
  let h = '';
  EX9.forEach((p, i) => { const x = i * 290, t0 = cues[i];
    const showA = u >= cue(1), showB = u >= cue(2);
    const lostA = p[1] === null, lostB = p[2] === null;
    const winA = !lostA && (lostB || p[1] <= p[2]);
    const decided = u >= t0 + 0.4;
    const box = (y, lost, win, col) => {
      const st = lost ? `border:3px dashed #ff6b5e;background:transparent;color:#ff6b5e` : `background:${col};color:#06141a;opacity:${decided && !win ? 0.3 : 1}`;
      return `<div class="chip" style="position:absolute;left:${x}px;top:${y}px;width:200px;font-size:26px;${st}">${lost ? '✕ ' : ''}${p[0]}${decided && !lost ? (win ? ' ✓' : ' dup') : ''}</div>`; };
    if (showA) h += box(10, lostA, winA, '#3fd0dc');
    if (showB) h += box(150, lostB, !winA, '#a98bff');
    if (decided) h += `<div class="chip" style="position:absolute;left:${x}px;top:350px;width:200px;font-size:26px;background:#4fd18b">${p[0]} · ${winA ? 'A' : 'B'}</div>`; });
  if (el.innerHTML !== h) el.innerHTML = h; } };
