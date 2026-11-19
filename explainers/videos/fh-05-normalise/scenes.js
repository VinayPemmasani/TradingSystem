// TopOfBook byte map, and the Consolidator change-mask bits.
const BITS = ['Bid', 'BidSize', 'Ask', 'AskSize', 'Last', 'LastSize', 'Volume', 'Open', 'High', 'Low', 'Trades', 'Status', 'Auction', 'Band'];
function bitRow(id) {
  const g = document.getElementById(id); if (!g || g.children.length) return;
  BITS.forEach((b, i) => {
    const d = document.createElement('div'); d.id = id + '-' + i;
    d.style.cssText = `position:absolute;left:${i * 78}px;top:0;width:74px;height:74px;border-radius:8px;border:2px solid #2c4351;background:#13212b;color:#8ea3b1;font:600 14px var(--mono);display:grid;place-items:center;text-align:center`;
    d.textContent = b; g.appendChild(d);
  });
}
function lightBits(id, on) {
  BITS.forEach((b, i) => { const d = document.getElementById(id + '-' + i); if (!d) return;
    const x = on.has(b); d.style.background = x ? 'var(--violet)' : '#13212b'; d.style.color = x ? '#06141a' : '#8ea3b1'; d.style.borderColor = x ? 'var(--violet)' : '#2c4351'; });
}
SCENES['top'] = {
  setup() {
    const g = document.getElementById('tb-bar'); if (!g || g.children.length) return;
    const F = [['rx_tsc', 8, 'var(--teal)'], ['feed_ns', 8, 'var(--blue)'], ['bid_px[2]', 8, 'var(--green)'], ['bid_qty[2]', 8, '#2f8a5b'], ['ask_px[2]', 8, 'var(--red)'], ['ask_qty[2]', 8, '#c0544b'], ['instrument', 2, 'var(--violet)'], ['locate', 2, '#c3b0ff'], ['state', 1, 'var(--amber)'], ['reserved', 11, '#2c4351']];
    let y = 0;
    for (const [n, b, c] of F) {
      const d = document.createElement('div'); const h = b * 8.6;
      d.style.cssText = `position:absolute;left:0;top:${y}px;width:540px;height:${h - 2}px;background:${c};border-radius:4px;color:#06141a;font:700 18px var(--mono);display:flex;align-items:center;justify-content:space-between;padding:0 12px`;
      d.innerHTML = n === 'reserved' ? `<span style="color:#cfd8de;font-size:16px;line-height:1.5">↑ instrument 2 B · locate 2 B · state 1 B<br>reserved</span><span style="color:#cfd8de">${b} B</span>` : (b >= 8 ? `<span>${n}</span><span>${b} B</span>` : ''); g.appendChild(d); y += h;
    }
  }
};
SCENES['record'] = {
  setup() { bitRow('rc-bits'); },
  draw(u, cue) {
    const k = u < cue(2) + 0.5 ? -1 : Math.floor((u - cue(2) - 0.5) / 0.7);
    const sets = [['Bid', 'BidSize'], ['Last', 'LastSize', 'Volume', 'Trades'], ['Ask'], ['Status'], ['Auction'], ['Band', 'Last', 'LastSize', 'Volume', 'Trades', 'High']];
    lightBits('rc-bits', new Set(k < 0 ? [] : sets[k % sets.length]));
  }
};
SCENES['example'] = {
  setup() { bitRow('ex-bits'); },
  draw(u, cue) {
    const on = [];
    if (u >= cue(2) + 1.0) on.push('LastSize', 'Volume', 'Trades');
    if (u >= cue(2) + 2.5) on.push('Last');
    if (u >= cue(3) + 0.8) on.push('Bid', 'BidSize');
    lightBits('ex-bits', new Set(on));
  }
};
