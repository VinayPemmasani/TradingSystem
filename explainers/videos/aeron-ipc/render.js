const { chromium } = require('playwright'); const fs=require('fs'); const {spawn}=require('child_process');
const D=JSON.parse(fs.readFileSync('/tmp/claude-0/av/data.json')); const FPS=30;
const mode=process.argv[2];
async function page(b,dsf){const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
 p.on('pageerror',e=>console.log('ERR',e.message)); await p.goto('file:///mnt/project-files/videos/aeron-source/stage.html'); await p.evaluate(()=>document.fonts.ready); await p.evaluate(d=>setup(d),D); return p;}
(async()=>{const b=await chromium.launch();
 if(mode==='preview'){ const p=await page(b,1); const ts=process.argv.slice(3).map(Number);
   for(const t of ts){await p.evaluate(t=>render(t),t); await p.waitForTimeout(50); await p.screenshot({path:`/tmp/claude-0/av/prev/p_${t.toFixed(2)}.jpg`,type:'jpeg',quality:80});} }
 else { const [w,W]=[+process.argv[3],+process.argv[4]]; const N=Math.round(D.total*FPS); const a=Math.floor(N*w/W), z=Math.floor(N*(w+1)/W);
   const p=await page(b,2);
   const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-threads','2',`/tmp/claude-0/av/seg_${w}.mp4`],{stdio:['pipe','inherit','inherit']});
   const t0=Date.now();
   for(let f=a;f<z;f++){ await p.evaluate(t=>render(t),f/FPS); const buf=await p.screenshot({type:'jpeg',quality:94});
     if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
     if((f-a)%300===0) console.log(`w${w} ${f-a}/${z-a} ${((Date.now()-t0)/1000).toFixed(0)}s`); }
   ff.stdin.end(); await new Promise(r=>ff.on('close',r)); console.log('done',w,(Date.now()-t0)/1000); }
 await b.close();})();
