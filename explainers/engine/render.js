// node render.js SLUG preview t1 t2 ...   -> /tmp/claude-0/vx/SLUG/prev/p_<t>.jpg
// node render.js SLUG contact             -> one frame near the end of every caption
// node render.js SLUG frames W N          -> worker W of N, writes seg_W.mp4
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const [slug, mode, ...rest] = process.argv.slice(2);
const SRC = `/mnt/project-files/videos/explainers/${slug}`, ENG = '/mnt/project-files/videos/explainers/engine', W = `/tmp/claude-0/vx/${slug}`;
const D = JSON.parse(fs.readFileSync(`${W}/data.json`)); const FPS = 30;
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg' };
function read(p) { return fs.existsSync(p) ? fs.readFileSync(p) : Buffer.from(''); }
async function open(b) {
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.route('http://stage.local/**', r => {
    const u = new URL(r.request().url()); let f = u.pathname.slice(1);
    let body;
    if (f === 'stage.html') {
      body = read(`${ENG}/stage.html`).toString()
        .replace('<style id="video-css"></style>', `<style id="video-css">${read(`${SRC}/style.css`)}</style>`)
        .replace('<div id="scenes"></div>', `<div id="scenes">${read(`${SRC}/scenes.html`)}</div>`)
        .replace('<script src="engine.js"></script>', `<script>window.SCENES={};</script><script src="video.js"></script><script src="engine.js"></script>`);
    } else if (f === 'engine.js') body = read(`${ENG}/engine.js`);
    else if (f === 'video.js') body = read(`${SRC}/scenes.js`);
    else body = read(path.join(SRC, f));
    r.fulfill({ status: 200, contentType: MIME[path.extname(f)] || 'application/octet-stream', body });
  });
  await p.goto('http://stage.local/stage.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(d => setup(d), D); return p;
}
(async () => {
  const b = await chromium.launch();
  if (mode === 'preview' || mode === 'contact') {
    fs.mkdirSync(`${W}/prev`, { recursive: true });
    let ts = rest.map(Number);
    if (mode === 'contact') ts = D.scenes.flatMap(s => s.caps.map(c => +(s.start + Math.min(c[1], s.dur) - 0.05).toFixed(2)));
    const p = await open(b);
    for (const t of ts) { await p.evaluate(t => render(t), t); await p.waitForTimeout(30);
      await p.screenshot({ path: `${W}/prev/p_${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 70 }); }
    console.log('wrote', ts.length, 'frames to', `${W}/prev`);
  } else {
    const [w, N] = rest.map(Number); const total = Math.round(D.total * FPS);
    const a = Math.floor(total * w / N), z = Math.floor(total * (w + 1) / N);
    const p = await open(b);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-threads', '2', `${W}/seg_${w}.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = a; f < z; f++) { await p.evaluate(t => render(t), f / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - a) % 600 === 0) console.log(`${slug} w${w} ${f - a}/${z - a} ${((Date.now() - t0) / 1000).toFixed(0)}s`); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log(`${slug} w${w} done ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await b.close();
})();
