# python3 sheet.py SLUG [cols=3]  -> /tmp/claude-0/vx/SLUG/prev/sheet_N.jpg, 9 frames per sheet, labelled with time
import glob, sys
from PIL import Image, ImageDraw
slug = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 3
d = f"/tmp/claude-0/vx/{slug}/prev"
fs = sorted(glob.glob(f"{d}/p_*.jpg"), key=lambda f: float(f.split('p_')[1][:-4]))
per = cols * cols; w, h = 1920 // cols, 1080 // cols
for n in range(0, len(fs), per):
    S = Image.new('RGB', (1920, 1080))
    for i, f in enumerate(fs[n:n + per]):
        im = Image.open(f).resize((w, h)); ImageDraw.Draw(im).text((8, 6), f.split('p_')[1][:-4] + 's', fill=(255, 255, 0))
        S.paste(im, ((i % cols) * w, (i // cols) * h))
    S.save(f"{d}/sheet_{n // per}.jpg", quality=85); print(f"{d}/sheet_{n // per}.jpg")
