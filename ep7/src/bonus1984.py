"""BONUS for TikTok: the full 1984 tape (no narration). Reuses the flashback scenes; skips the present-day lines."""
import os, sys, subprocess
os.environ["PLATFORM"] = "bonus"            # no voice file -> the tape keeps its own timing
from multiprocessing import Pool
import fb84 as fb
from style import caption as _caption, font, OL, C_Y, FW
from PIL import ImageDraw

fb.UYF, fb.BUG_DY = 150, 150


def banner(img, ep, y=200):
    d = ImageDraw.Draw(img)
    f = font(600, 19)
    a, b = "BONUS · THE 1984 TAPE · FROM ZERO TO ", "LEGEND"
    wa, wb = d.textlength(a, font=f), d.textlength(b, font=f)
    x = (FW - wa - wb) / 2
    for txt, col, xx in ((a, (240, 240, 245), x), (b, C_Y, x + wa)):
        d.text((xx, y), txt, font=f, fill=col, stroke_width=3, stroke_fill=OL)


def caption(img, words, t, wrap=600, y=108, size=50):
    _caption(img, words, t, wrap=wrap, y=236, size=size)


fb.banner, fb.caption = banner, caption
S, TOT = fb.STARTS, fb.TOTAL
KEEP = [(S[0], S[1]), (S[4], S[22]), (S[23], TOT)]     # hook | the whole tape | the vote + end card
D_ = sys.argv[2] if len(sys.argv) > 2 else "fb_bonus"
times = []
for a, b in KEEP:
    n = int((b - a) * 30)
    times += [a + (k + 0.5) / 30 for k in range(n)]


def work(i):
    fb.frame(times[i]).save(f"{D_}/{i:05d}.png", compress_level=1)


if __name__ == "__main__":
    os.makedirs(D_, exist_ok=True)
    with Pool(4) as pool:
        list(pool.imap_unordered(work, range(len(times)), chunksize=8))
    # audio: the full tape SFX, cut to the same pieces
    subprocess.run([sys.executable, "sfx_bonus.py", f"{D_}/sfx_full.wav"], check=True)
    parts = []
    for k, (a, b) in enumerate(KEEP):
        p = f"{D_}/a{k}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D_}/sfx_full.wav", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", p], check=True)
        parts.append(p)
    with open(f"{D_}/list.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{D_}/list.txt", f"{D_}/sfx.wav"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{D_}/%05d.png", "-i", f"{D_}/sfx.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", sys.argv[1]], check=True)
    print("frames", len(times), "seconds", round(len(times) / 30, 2))
