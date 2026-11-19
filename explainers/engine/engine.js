// Explainer scene engine. A video is scenes.html (one <div class="scene" id="s-ID"> per
// script entry), optional scenes.js (window.SCENES[ID].draw(u, cue, H) for custom
// animation) and optional style.css. render(t) is stateless: every frame is
// computed from t alone, so frames can be rendered in any order.
//
// Declarative attributes on any element inside a scene:
//   data-cue="k"        appear when caption k of this scene starts (0-based)
//   data-d="0.4"        extra delay in seconds after that cue (may be negative)
//   data-fade="0.5"     fade length (default 0.5)
//   data-anim="up|fade|left|scale|none"  entry motion (default up)
//   data-out="k" data-od="0.2"  fade out at caption k (+delay); data-out="end" = scene end
//   data-hl="k" data-hld="0" data-hlend="m"   add class "hl" from cue k until cue m
//   data-dim="k"        add class "dim" from cue k (data-dimend="m" to stop)
// Element kinds:
//   <path class="draw" pathLength="1" data-cue..>  stroke draws in over data-dur (0.9 s)
//   <span class="count" data-from="0" data-to="100" data-dec="0" data-dur="1.2" data-pre="" data-post="">
//   <span class="type" data-dur="1.5">text</span>   typewriter
//   <div class="pkt" data-path="pathId" data-dur="1.2" [data-loop="1"] [data-phase="0.3"]>
//       moves along the SVG path (ids must be unique in the whole video)
//   <div class="grow" data-w="600" data-dur="1">  width grows from 0 to data-w px
(function () {
  const C = (x) => Math.max(0, Math.min(1, x));
  const ease = (x) => { x = C(x); return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; };
  const lerp = (a, b, p) => a + (b - a) * p;
  const $ = (id) => document.getElementById(id);
  const H = { C, ease, lerp, $, P: (u, a, d = 0.5) => ease((u - a) / d),
    show(el, p, dy = 18) { if (typeof el === 'string') el = $(el); el.style.opacity = p; el.style.transform = `translateY(${(1 - p) * dy}px)`; },
    text(el, s) { if (typeof el === 'string') el = $(el); if (el.textContent !== s) el.textContent = s; } };
  window.H = H;
  window.SCENES = window.SCENES || {};
  let D = null; const SC = {};

  function num(v, d) { const x = parseFloat(v); return isNaN(x) ? d : x; }

  function prep(scene) {
    const items = [];
    scene.querySelectorAll('[data-cue],[data-hl],[data-dim],.pkt').forEach((el) => {
      const ds = el.dataset;
      const it = { el, cls: el.classList, cue: ds.cue, d: num(ds.d, 0), fade: num(ds.fade, 0.5), anim: ds.anim || 'up',
        out: ds.out, od: num(ds.od, 0), hl: ds.hl, hld: num(ds.hld, 0), hlend: ds.hlend, dim: ds.dim, dimend: ds.dimend,
        dur: num(ds.dur, 0.9) };
      if (el.classList.contains('type')) it.full = el.textContent;
      if (el.classList.contains('pkt')) { it.path = ds.path; it.loop = ds.loop === '1'; it.phase = num(ds.phase, 0); it.dur = num(ds.dur, 1.2); }
      if (el.classList.contains('count')) { it.from = num(ds.from, 0); it.to = num(ds.to, 0); it.dec = num(ds.dec, 0); it.pre = ds.pre || ''; it.post = ds.post || ''; it.dur = num(ds.dur, 1.2); }
      if (el.classList.contains('grow')) { it.w = num(ds.w, 100); it.dur = num(ds.dur, 1); }
      if (el.tagName.toLowerCase() === 'path' && el.classList.contains('draw')) { el.setAttribute('pathLength', '1'); el.style.strokeDasharray = '1 1'; }
      items.push(it);
    });
    return items;
  }

  window.setup = function (d) {
    D = d;
    $('brand').textContent = d.brand || '';
    for (const s of D.scenes) {
      const el = $('s-' + s.id);
      if (!el) throw new Error('scenes.html has no element #s-' + s.id);
      SC[s.id] = { el, items: prep(el) };
      if (window.SCENES[s.id] && window.SCENES[s.id].setup) window.SCENES[s.id].setup(H);
    }
  };

  window.render = function (t) {
    const S = D.scenes; let i = S.length - 1;
    for (let k = 0; k < S.length; k++) if (t < S[k].start + S[k].dur) { i = k; break; }
    const s = S[i]; const u = t - s.start;
    for (const x of S) SC[x.id].el.style.display = x.id === s.id ? 'block' : 'none';
    const sc = SC[s.id];
    const fin = i === 0 ? 1 : C(u / 0.35);
    const fout = i === S.length - 1 ? C((D.total - t) / 0.8) : C((s.start + s.dur - t) / 0.3);
    sc.el.style.opacity = Math.min(fin, fout);
    const cue = (k) => {
      if (k === 'end') return s.dur;
      k = parseFloat(k); const n = s.caps.length;
      if (k < n) return s.caps[Math.floor(k)][0] + (k % 1) * ((s.caps[Math.floor(k)][1]) - s.caps[Math.floor(k)][0]);
      return s.dur;
    };
    for (const it of sc.items) {
      const el = it.el;
      if (it.cue !== undefined) {
        const t0 = cue(it.cue) + it.d;
        let p = ease((u - t0) / it.fade);
        if (it.out !== undefined) p *= 1 - ease((u - (cue(it.out) + it.od)) / 0.4);
        if (!it.cls.contains('pkt')) {
          el.style.opacity = p;
          if (it.anim === 'up') el.style.transform = `translateY(${(1 - p) * 18}px)`;
          else if (it.anim === 'left') el.style.transform = `translateX(${(1 - p) * -30}px)`;
          else if (it.anim === 'scale') el.style.transform = `scale(${0.9 + 0.1 * p})`;
        }
        const q = C((u - t0) / it.dur);
        if (it.cls.contains('draw')) el.style.strokeDashoffset = String(1 - ease(q));
        if (it.cls.contains('count')) { const v = lerp(it.from, it.to, ease(q)); const str = it.pre + v.toFixed(it.dec).replace(/\B(?=(\d{3})+(?!\d))/g, it.dec ? '' : ',') + it.post; if (el.textContent !== str) el.textContent = str; }
        if (it.cls.contains('type')) { const n = Math.round(it.full.length * q); const str = it.full.slice(0, n); if (el.textContent !== str) el.textContent = str; }
        if (it.cls.contains('grow')) el.style.width = (it.w * ease(q)) + 'px';
        if (it.cls.contains('pkt')) {
          const path = document.getElementById(it.path);
          let f = (u - t0) / it.dur + it.phase;
          let vis = u >= t0 && p > 0;
          if (it.loop) f = ((f % 1) + 1) % 1; else { if (f > 1) vis = false; f = C(f); }
          if (path && vis) { const L = path.getTotalLength(); const pt = path.getPointAtLength(ease(f) * L);
            el.style.left = pt.x + 'px'; el.style.top = pt.y + 'px'; el.style.opacity = it.out !== undefined ? p : 1; }
          else el.style.opacity = 0;
        }
      }
      if (it.hl !== undefined) { const on = u >= cue(it.hl) + it.hld && (it.hlend === undefined || u < cue(it.hlend)); el.classList.toggle('hl', on); }
      if (it.dim !== undefined) { const on = u >= cue(it.dim) && (it.dimend === undefined || u < cue(it.dimend)); el.classList.toggle('dim', on); }
    }
    if (window.SCENES[s.id] && window.SCENES[s.id].draw) window.SCENES[s.id].draw(u, cue, H, s);
    const ch = $('chapter'); ch.style.display = i === 0 ? 'none' : 'flex';
    H.text('ch-n', String(i)); H.text('ch-t', s.title || s.id);
    let txt = ''; for (const c of s.caps) if (u >= c[0] - 0.05 && u < c[1] + 0.25) txt = c[2];
    const ce = $('caption'); ce.style.display = txt ? 'block' : 'none'; H.text(ce, txt);
    $('prog').style.width = (1920 * t / D.total) + 'px';
  };
})();
