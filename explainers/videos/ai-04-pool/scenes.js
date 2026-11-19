// Heap: a new order lands in a hole; pages fault in one by one. Pool: free-list pops and pushes.
SCENES['cost'] = {
  draw(u, cue, H) {
    const t = cue(3) + 0.6, on = u >= t;
    const k = document.getElementById('hp-k6');
    if (k) { k.style.background = on ? 'var(--amber)' : '#0f1b23'; k.style.borderStyle = on ? 'solid' : 'dashed'; k.style.borderColor = on ? 'var(--amber)' : '#4b6474'; }
    const n = document.getElementById('hp-new');
    if (n) { n.style.opacity = H.C((u - t + 0.4) / 0.4); n.style.left = '470px'; }
    const t0 = cue(4) + 0.8;
    const m = u < t0 ? 0 : Math.min(12, 1 + Math.floor((u - t0) / 0.35));
    for (let j = 0; j < 12; j++) {
      const p = document.getElementById('hp-p' + j); if (!p) continue;
      const f = j < m;
      p.style.borderStyle = f ? 'solid' : 'dashed';
      p.style.borderColor = f ? 'var(--amber)' : '#4b6474';
      p.style.color = f ? 'var(--amber)' : 'var(--muted)';
      p.textContent = f ? 'fault' : '4 KB';
    }
  }
};
SCENES['hot'] = {
  draw(u, cue, H) {
    const script = [['a', 0], ['a', 1], ['a', 2], ['r', 1], ['a', 1], ['a', 3], ['r', 0], ['a', 0], ['a', 4], ['r', 3], ['a', 3], ['a', 5]];
    const t0 = cue(3), n = u < t0 ? 0 : Math.min(script.length, 1 + Math.floor((u - t0) / 0.6));
    const used = new Set(); const free = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
    for (let k = 0; k < n; k++) { const [op, s] = script[k]; if (op === 'a') { used.add(s); free.splice(free.indexOf(s), 1); } else { used.delete(s); free.unshift(s); } }
    for (let j = 0; j < 12; j++) {
      const el = document.getElementById('pl-s' + j); if (!el) continue;
      const on = used.has(j);
      el.style.background = on ? 'var(--teal)' : '#0f1b23';
      el.style.borderColor = on ? 'var(--teal)' : 'var(--line)';
      el.style.color = on ? '#06141a' : 'var(--muted)';
      el.textContent = on ? 'order' : '';
    }
    const f = document.getElementById('pl-f');
    if (f) f.style.left = (60 + (free[0] ?? 11) * 68 + 6) + 'px';
  }
};
