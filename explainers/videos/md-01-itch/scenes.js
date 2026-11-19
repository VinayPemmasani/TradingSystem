// md-01: title stream, book ladder, order life bar, example bar.
const MD1_COL = {A:'#4fd18b',E:'#ffb347',X:'#ff8fc8',D:'#ff6b5e',U:'#a98bff',P:'#8ea3b1'};
SCENES['title'] = {
  setup() {
    const s = document.getElementById('t-stream'); const seq = 'AAEAXDAUAEAAPDAEXAAD';
    let h = ''; for (let i = 0; i < 40; i++) { const c = seq[i % seq.length];
      h += `<div class="chip" style="position:absolute;top:28px;left:0;background:${MD1_COL[c]}" data-i="${i}">${c}</div>`; }
    s.innerHTML = h;
  },
  draw(u) {
    document.querySelectorAll('#t-stream .chip').forEach((el) => { const i = +el.dataset.i;
      const x = ((i * 96 + u * 160) % 3840) - 1000; el.style.left = x + 'px'; });
  }
};
SCENES['why'] = {
  setup() {
    const b = document.getElementById('why-book'); let h = '';
    const rows = [['ask', '189.28', 300], ['ask', '189.27', 500], ['ask', '189.26', 200], ['bid', '189.25', 400], ['bid', '189.24', 700], ['bid', '189.23', 300]];
    rows.forEach((r, i) => { h += `<div class="lvl" id="wb${i}" style="position:absolute;left:0;top:${i * 58}px;width:0;background:${r[0] === 'ask' ? '#ff6b5e' : '#4fd18b'}">${r[1]}</div>`; });
    b.innerHTML = h;
  },
  draw(u, cue) {
    const t0 = cue(3) + 0.6; const W = [180, 260, 120, 220, 300, 170];
    for (let i = 0; i < 6; i++) { const el = document.getElementById('wb' + i); const p = Math.max(0, Math.min(1, (u - t0 - i * 0.25) / 0.5));
      const wob = u > t0 + 2 ? 20 * Math.sin(u * 1.7 + i) : 0; el.style.width = (p * (W[i] + wob)) + 'px'; }
  }
};
SCENES['life'] = {
  draw(u, cue, H) {
    const el = document.getElementById('life-bar'); if (!el) return;
    let sh = 100, ref = 1234, gone = false;
    if (u >= cue(1)) sh = 60; if (u >= cue(2)) sh = 50; if (u >= cue(3)) { ref = 5678; sh = 80; } if (u >= cue(4)) gone = true;
    const col = u >= cue(4) ? '#ff6b5e' : u >= cue(3) ? '#a98bff' : u >= cue(2) ? '#ff8fc8' : '#ffb347';
    el.innerHTML = `<div class="lbl" style="position:absolute;top:0">ref ${ref} · shares ${gone ? 0 : sh}</div>` +
      `<div style="position:absolute;top:50px;height:60px;border-radius:8px;width:${gone ? 0 : sh * 5}px;background:${col};transition:none"></div>` +
      (gone ? '<div class="lbl c-red" style="position:absolute;top:130px">removed from the book</div>' : '');
  }
};
SCENES['example'] = {
  draw(u, cue, H) {
    let n = 100; if (u >= cue(4) + 0.5) n = 60; if (u >= cue(5) + 0.5) n = 50; if (u >= cue(6) + 0.5) n = 0;
    const b = document.getElementById('ex-bar'); b.style.width = (n * 15) + 'px';
    b.style.background = n === 0 ? '#ff6b5e' : '#6aa8ff';
    H.text('ex-n', String(n));
  }
};
