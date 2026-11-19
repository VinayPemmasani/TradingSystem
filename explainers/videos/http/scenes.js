// Custom animation for the HTTP explainer: flow-control window, WebSocket parse cursor, JSON scan cursor.
SCENES['flow'] = {
  draw(u, cue, H) {
    const W = 65535, full = 1296;
    const t2 = cue(2);
    const sends = [16384, 16384, 16384, 16383];
    let w = W;
    sends.forEach((n, i) => { w -= n * H.P(u, t2 + 0.6 * i + 0.3, 0.4); });
    w += 32768 * H.P(u, t2 + 3.5, 0.6);
    w = Math.max(0, Math.round(w));
    const f = H.$('fl-fill'); f.style.width = (full * w / W) + 'px';
    f.style.background = w < 1 ? 'var(--red)' : 'var(--green)';
    H.text('fl-num', w.toLocaleString('en-US'));
    H.$('fl-num').style.color = w < 1 ? 'var(--red)' : 'var(--green)';
  }
};
SCENES['wsframe'] = {
  draw(u, cue, H) {
    // cursor position (left, width) over the byte cells, which start at x=120, 120 px each
    const steps = [[cue(1), 0, 1], [cue(3), 1, 1], [cue(5), 2, 4], [cue(5) + 1.6, 6, 4]];
    let a = steps[0], b = null;
    for (let i = 0; i < steps.length; i++) if (u >= steps[i][0]) { a = steps[i]; b = steps[i + 1] || null; }
    let x = a[1], n = a[2];
    for (let i = 1; i < steps.length; i++) {
      const p = H.P(u, steps[i][0], 0.5);
      if (p > 0 && p < 1) { x = H.lerp(steps[i - 1][1], steps[i][1], p); n = H.lerp(steps[i - 1][2], steps[i][2], p); }
    }
    const c = H.$('wf-cur'); c.style.left = (116 + 120 * x) + 'px'; c.style.width = (120 * n + 8) + 'px';
  }
};
SCENES['latency'] = {
  draw(u, cue, H) {
    // the scan cursor walks the JSON characters during sentences 0-1
    const s = H.$('lt-js'); const n = s.textContent.length;
    const cw = s.getBoundingClientRect().width / n;
    const t0 = cue(0) + 0.6, t1 = cue(2);
    const k = Math.min(n - 1, Math.floor(H.C((u - t0) / (t1 - t0)) * n));
    const c = H.$('lt-scan'); c.style.left = (116 + k * cw) + 'px'; c.style.width = (cw + 8) + 'px';
  }
};
