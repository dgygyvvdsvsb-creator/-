"""~16 s silent preview: each shot with a slow push-in (like the reference) + karaoke captions."""
import subprocess, os
import scenes
from scenes import *
from PIL import Image
FPS = 30
shots = [(s_training, 2.6), (s_locker, 2.6), (s_stadium, 2.6), (s_header, 2.4), (s_bedroom, 2.6), (s_ending, 3.4)]
tmp = os.path.join(OUT, "frames"); os.makedirs(tmp, exist_ok=True)
n = 0
for fn, dur in shots:
    scenes.REC = []
    base = fn().convert("RGBA")
    calls = scenes.REC; scenes.REC = None
    N = int(dur * FPS)
    for i in range(N):
        t = i / N
        z = 1 + 0.06 * t
        w, h = int(FW / z), int(FH / z)
        fr = base.crop(((FW - w) // 2, (FH - h) // 2, (FW - w) // 2 + w, (FH - h) // 2 + h)).resize((FW, FH), Image.NEAREST)
        for kind, a, kw in calls:
            if kind == "banner": banner(fr, **kw)
            else:
                words = a[0]; spoken = min(len(words), 1 + int(t * 1.6 * len(words)))
                caption(fr, words, spoken=spoken, **kw)
        fr.convert("RGB").save(os.path.join(tmp, f"f{n:05d}.png")); n += 1
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", os.path.join(OUT, "style_preview.mp4")], check=True)
subprocess.run(["rm", "-rf", tmp])
print("frames", n)
