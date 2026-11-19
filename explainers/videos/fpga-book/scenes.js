// Custom animation for the fpga-book explainer. draw() is stateless: everything from u.
SCENES['exec'] = {
  draw(u, cue, H) {
    // E executes 200 at cue 2, X cancels 100 at cue 3, D removes the rest at cue 3.5
    const steps = [[cue(2) + 0.3, 300, '1,000', 3, 'E: −200 executed'],
                   [cue(3) + 0.5, 200, '900', 3, 'X: −100 cancelled'],
                   [cue(3.5) + 0.5, 0, '700', 2, 'D: −200, order gone']];
    let os = 500, ls = '1,200', lo = 3, op = '';
    for (const [t, o, l, n, s] of steps) if (u >= t) { os = o; ls = l; lo = n; op = s; }
    H.text('ex-os', String(os)); H.text('ex-ls', ls); H.text('ex-lo', String(lo)); H.text('ex-op', op);
    H.$('ex-op').style.visibility = op ? 'visible' : 'hidden';
  }
};
SCENES['levels'] = {
  draw(u, cue, H) {
    const p = H.P(u, cue(2) + 0.2, 0.6);
    for (let i = 2; i < 6; i++) {
      const el = H.$('lv-r' + i);
      el.style.transform = `translateY(${86 * p}px)`;
      H.text('lv-l' + i, 'L' + (p > 0.5 ? i + 1 : i));
    }
    // L5 is pushed out of the registers into RAM
    const r5 = H.$('lv-r5');
    r5.style.opacity = String(parseFloat(r5.style.opacity || 1) * (1 - H.P(u, cue(2) + 0.6, 0.6)));
    H.text('lv-s0', u >= cue(4) + 0.3 ? '500' : '800');
    H.$('lv-r0').classList.toggle('hl', u >= cue(4) + 0.3);
  }
};
