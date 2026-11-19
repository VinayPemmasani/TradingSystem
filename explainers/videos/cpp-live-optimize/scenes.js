
// running latency meter: .meter[data-from,data-to,data-at] ; ring/mesi animations
(function(){
function fmt(v){ return v >= 1000 ? (v/1000).toFixed(1) + ' µs' : (v >= 10 ? Math.round(v) : v.toFixed(1)) + ' ns'; }
function meters(u, cue, H, sc){
  document.querySelectorAll('#s-' + sc.id + ' .meter').forEach(function(m){
    var A = m.dataset.from.split(',').map(Number), B = m.dataset.to.split(',').map(Number);
    var at = parseFloat(m.dataset.at), p = 0;
    if (at >= 0) p = H.ease((u - cue(at)) / 1.4);
    H.text(m.querySelector('.m50'), fmt(H.lerp(A[0], B[0], p)));
    H.text(m.querySelector('.m99'), fmt(H.lerp(A[1], B[1], p)));
    H.text(m.querySelector('.mlab'), p < 0.5 ? m.dataset.la : m.dataset.lb);
    m.classList.toggle('chg', at >= 0 && u > cue(at) && u < cue(at) + 3);
  });
}
var ids = ["title", "snippet", "measure", "baseline", "ds-map", "ds-layout", "pipeline", "chain", "divide", "predict", "branchless", "hidden", "prealloc", "part1", "split", "mutex", "flag", "reorder", "acqrel", "ring", "mesi", "padfix", "results", "checklist"];
ids.forEach(function(id){ SCENES[id] = { draw: function(u, cue, H, sc){ meters(u, cue, H, sc); if (EXTRA[id]) EXTRA[id](u, cue, H, sc); } }; });
var EXTRA = {};
EXTRA['prealloc'] = function(u, cue, H){
  var n = Math.max(0, Math.floor((u - cue(1)) * 6));
  for (var k = 0; k < 32; k++){ var el = document.getElementById('pa-s' + k);
    var filled = n > k || n >= 32; var cur = (n % 32) === k && n > 0;
    el.classList.toggle('on', filled && !cur); el.classList.toggle('old', cur); }
};
EXTRA['ring'] = function(u, cue, H){
  var t0 = cue(1), h = Math.max(0, Math.floor((u - t0) * 2.2)), t = Math.max(0, Math.floor((u - t0 - 0.9) * 2.2));
  if (t > h) t = h;
  for (var k = 0; k < 8; k++){ var el = document.getElementById('rg-' + k);
    var on = false; for (var i = t; i < h; i++) if (i % 8 === k) on = true; el.classList.toggle('on', on); }
  document.getElementById('rg-h').style.left = (1200 + (h % 8) * 80) + 'px';
  document.getElementById('rg-t').style.left = (1200 + (t % 8) * 80) + 'px';
};
EXTRA['mesi'] = function(u, cue, H){
  var a = document.getElementById('me-s1'), b = document.getElementById('me-s2');
  var ph = u < cue(3) ? 0 : Math.floor((u - cue(3)) / 0.8) % 2;
  var s1 = ph === 0 ? 'M' : 'I', s2 = ph === 0 ? 'I' : 'M';
  H.text(a, s1); H.text(b, s2); a.className = 'st ' + s1; b.className = 'st ' + s2;
};
})();
