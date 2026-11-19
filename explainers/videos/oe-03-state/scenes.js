SCENES['example'] = { draw(u, cue, H) {
  const k = [0,1,2,3,4,5].filter(i => u >= cue(i) + 0.2).pop() ?? -1;
  const S = ['·', 'pending new', 'live', 'live', 'live · cancel pending', 'done'];
  const P = ['0', '0', '0', '+100', '+100', '+100'];
  const E = ['0', '300', '300', '200', '200', '0'];
  const i = Math.max(0, k);
  H.text('e3-st', S[i]); H.text('e3-pos', P[i]); H.text('e3-exp', E[i]); } };
