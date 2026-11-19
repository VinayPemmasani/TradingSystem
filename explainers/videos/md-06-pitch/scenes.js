SCENES['units'] = {
  setup() { const s = 'AAPL ABNB AMZN CSCO F GOOG INTC MSFT NVDA ORCL PEP QQQ SPY TSLA XOM'.split(' '); let h = '';
    s.forEach((x, i) => { const c = x[0] <= 'F' ? '#3fd0dc' : x[0] <= 'O' ? '#a98bff' : '#ffb347';
      h += `<div class="chip" style="position:absolute;left:${i * 112}px;top:0;width:104px;font-size:20px;background:${c}">${x}</div>`; });
    document.getElementById('u6-sym').innerHTML = h; },
  draw(u, cue, H) { const t = Math.max(0, u - cue(1));
    H.text('u6-s1', 'seq ' + (1 + Math.floor(t * 23)).toLocaleString('en-US'));
    H.text('u6-s2', 'seq ' + (1 + Math.floor(t * 11)).toLocaleString('en-US'));
    H.text('u6-s3', 'seq ' + (1 + Math.floor(t * 31)).toLocaleString('en-US')); } };
SCENES['recovery'] = { draw(u, cue) { const t0 = cue(5) + 0.4; const n = u < t0 ? 0 : Math.min(10, Math.floor((u - t0) / 0.4));
  let h = ''; for (let i = 0; i < n; i++) h += `<div class="chip" style="position:absolute;left:${i * 80}px;top:0;width:72px;height:56px;font-size:18px;background:#3fd0dc">${2001 + i}</div>`;
  const el = document.getElementById('r6-buf'); if (el.dataset.n !== String(n)) { el.innerHTML = h; el.dataset.n = n; } } };
