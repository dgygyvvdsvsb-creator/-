"""Test video in the new style: animated shots driven by the narrator's line timings.
python3 test_ep.py  ->  ../out/TEST_style.mp4"""
import json, math, os, subprocess, re
import numpy as np
import scenes
from scenes import *
from PIL import Image, ImageDraw, ImageFilter

FPS = 30
VO = os.path.join(HERE, "vo", "test_vo.mp3")

LINES = [
    W_("90TH", RED) + W_("MINUTE.") + W_("ONE-NIL.", Y),
    W_("MASON", RED) + W_("BREAKS THROUGH.") + W_("ONLY") + W_("YOU", Y) + W_("ARE LEFT."),
    W_("HE") + W_("SHOOTS!", RED),
    W_("YOU") + W_("FLY.", Y),
    W_("FINGERTIPS!", Y) + W_("THE STADIUM") + W_("EXPLODES!", TEAL),
    W_("SEAT 14:") + W_("GRANDAD", Y) + W_("IS ON HIS FEET."),
    W_("AFTER THE MATCH, THE") + W_("COACH", BLUE) + W_("STOPS YOU."),
    W_("TOMORROW,") + W_("YOU START.", Y),
    W_("STAY", Y) + W_("AND FIGHT DIXON, OR") + W_("LEAVE", TEAL) + W_("ON LOAN?"),
]

# ------------------------------------------------------------------ timing from the voice
def vo_segments():
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VO],
                                 capture_output=True, text=True).stdout)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", VO, "-af", "silencedetect=n=-38dB:d=0.32", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    S, cur = [], 0.0
    for a, b in zip(st, en):
        if a - cur > 0.08: S.append((cur, a))
        cur = b
    if total - cur > 0.1: S.append((cur, total))
    return S, total

HAVE_VO = os.path.exists(VO)
if HAVE_VO:
    SEG, VO_LEN = vo_segments()
else:   # no voice file: estimate line lengths (~2.7 words/s narration) with short pauses
    SEG, t = [], 0.3
    for n in (4, 7, 2, 2, 5, 6, 7, 3, 11, 6):
        d = max(1.2, n / 2.7); SEG.append((t, t + d)); t += d + 0.75
    SEG[4] = (SEG[4][0], SEG[4][1] + 0.6)
print("segments", len(SEG), [(round(a, 2), round(b, 2)) for a, b in SEG])
# merge speech segments into the 9 lines (+ the last spoken sentence "write stay or leave")
want = len(LINES) + 1
while len(SEG) > want:          # merge the closest pair
    g = min(range(len(SEG) - 1), key=lambda i: SEG[i + 1][0] - SEG[i][1])
    SEG[g] = (SEG[g][0], SEG[g + 1][1]); del SEG[g + 1]
assert len(SEG) == want, SEG
LEAD = 0.25
SPAN = [(a + LEAD, b + LEAD) for a, b in SEG]
STARTS = [0.0] + [SPAN[i][0] - 0.12 for i in range(1, len(LINES))]
TOTAL = SPAN[-1][1] + 2.2
DUR = [(STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i] for i in range(len(STARTS))]
LINES.append(W_("WRITE") + W_("STAY", Y) + W_("OR") + W_("LEAVE", TEAL) + W_("IN THE COMMENTS."))

# ------------------------------------------------------------------ helpers
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t

def glow_ring(img, cx, cy, r, a=200):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 250, 200, a), width=max(4, int(r / 8)))
    g.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], fill=(255, 255, 255, a // 3))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(5)))

def speed_lines(img, cx, cy, n=26, r0=260, r1=900, w=6, seed=0):
    d = ImageDraw.Draw(img); r = random.Random(seed)
    for i in range(n):
        a = r.random() * 2 * math.pi; q0 = r0 + r.random() * 120
        d.line([(cx + q0 * math.cos(a), cy + q0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))],
               fill=(255, 255, 255), width=w)

def score_bar(img, minute="90'"):
    d = ImageDraw.Draw(img)
    x0, y0 = 250, 1640
    d.rounded_rectangle([x0, y0, FW - x0, y0 + 86], 18, fill=(10, 14, 34), outline=Y, width=4)
    d.rectangle([x0 + 24, y0 + 22, x0 + 66, y0 + 64], fill=(44, 170, 76))
    d.rectangle([FW - x0 - 66, y0 + 22, FW - x0 - 24, y0 + 64], fill=(214, 52, 58))
    d.text((FW / 2, y0 + 43), "1 - 0", font=font(800, 50), fill=(255, 255, 255), anchor="mm")
    d.text((FW / 2, y0 + 118), minute, font=font(800, 38), fill=RED, anchor="mm")

def flash(img, a):
    if a <= 0: return
    img.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, int(255 * min(1, a)))))

# ------------------------------------------------------------------ static backgrounds
def bg_broadcast():
    img = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for y in range(370): d.line([(0, y), (FW, y)], fill=(8 + y // 40, 12 + y // 30, 30 + y // 15))
    crowd(img, 370, 760); adboard(img, 760, 46)
    b = lowres(180, 190); dd = ImageDraw.Draw(b); stripes(dd, 0, 190, 180, n=9)
    dd.line([(0, 14), (180, 14)], fill=(236, 240, 236)); dd.ellipse([60, 120, 120, 170], outline=(236, 240, 236))
    dd.line([(0, 145), (180, 145)], fill=(236, 240, 236))
    img.paste(up(b), (0, 806))
    return img

def bg_goal_front():
    img = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for y in range(370): d.line([(0, y), (FW, y)], fill=(8 + y // 40, 12 + y // 30, 30 + y // 15))
    crowd(img, 370, 820, k=8); adboard(img, 820, 56)
    img.paste(img.crop((0, 370, FW, 876)).filter(ImageFilter.GaussianBlur(1.6)), (0, 370))
    b = lowres(180, 175); dd = ImageDraw.Draw(b); stripes(dd, 0, 175, 180, n=8)
    dd.line([(0, 48), (180, 48)], fill=(236, 240, 236))
    dd.line([(14, 48), (0, 80)], fill=(236, 240, 236)); dd.line([(166, 48), (180, 80)], fill=(236, 240, 236))
    img.paste(up(b), (0, 876))
    return img

GOAL = (230, 850, 720, 1166)        # x0, x1, top, goal line (youth goal: h = 1.2 x keeper, w = 2 x h)
def draw_goal(img, front=True):
    d = ImageDraw.Draw(img)
    x0, x1, yt, yb = GOAL
    if front:
        for x in range(x0, x1, 22): d.line([(x, yt), (x, yb)], fill=(205, 210, 220), width=2)
        for y in range(yt, yb, 22): d.line([(x0, y), (x1, y)], fill=(205, 210, 220), width=2)
    d.rectangle([x0 - 14, yt - 14, x1 + 14, yt], fill=(250, 250, 250))
    d.rectangle([x0 - 14, yt, x0, yb], fill=(250, 250, 250)); d.rectangle([x1, yt, x1 + 14, yb], fill=(250, 250, 250))

def bg_stand():
    img = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    crowd(img, 0, FH, k=13)
    img = img.filter(ImageFilter.GaussianBlur(5))
    img.alpha_composite(Image.new("RGBA", img.size, (8, 12, 34, 120)))
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
    for y in range(400): o.line([(0, y), (FW, y)], fill=(8, 12, 34, int(255 * (1 - y / 400) ** 0.6)))
    img.alpha_composite(ov)
    return img

BG = {}
def bg(key, fn):
    if key not in BG: BG[key] = fn()
    return BG[key].copy()

def bg_locker():
    scenes.REC = []; im = scenes.s_locker.__wrapped__() if hasattr(scenes.s_locker, "__wrapped__") else None
    scenes.REC = None
    return im

def locker_plain():
    b = lowres(); d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 180, 200], fill=(34, 120, 76))
    for x in range(0, 180, 22):
        d.rectangle([x, 20, x + 20, 196], fill=(48, 150, 92)); d.rectangle([x + 18, 20, x + 20, 196], fill=(30, 104, 64))
        d.rectangle([x + 3, 30, x + 15, 31], fill=(30, 96, 60)); d.rectangle([x + 3, 34, x + 15, 35], fill=(30, 96, 60))
        d.rectangle([x + 14, 100, x + 15, 110], fill=(210, 216, 222))
    d.rectangle([0, 0, 180, 18], fill=(24, 34, 60))
    for yy in range(200, 320, 12):
        for xx in range(0, 180, 12):
            d.rectangle([xx, yy, xx + 11, yy + 11], fill=(92, 104, 134) if ((xx + yy) // 12) % 2 else (104, 116, 148))
    d.rectangle([0, 196, 180, 200], fill=(60, 64, 84))
    d.rectangle([0, 176, 180, 182], fill=(156, 108, 64)); d.rectangle([0, 182, 180, 184], fill=(112, 76, 44))
    for x in (20, 160): d.rectangle([x, 184, x + 3, 204], fill=(70, 70, 80))
    return up(b)

# ------------------------------------------------------------------ shots  f(t, D) -> (frame, zoom, shake)
def run_spr(fn, t, rate=7, **kw):
    return fn(pose="run", step=int(t * rate) % 2, **kw)

def sh_0(t, D):          # broadcast: Mason runs with the ball, 90'
    img = bg("bc", bg_broadcast)
    x = lerp(160, 820, t / D); y = lerp(1500, 1180, t / D)
    for i, (dx, dy, n) in enumerate(((-230, 120, 4), (-330, -60, 5))):
        put(img, run_spr(lambda **k: blue(n, **k) if False else red(n, **k), t + i * 0.1, skin="dark" if i else "light"), 7, x + dx - 40 * t, y + dy)
    put(img, run_spr(mason, t, rate=8, mouth="flat"), 8, x, y)
    bx = x + 70 + 12 * math.sin(t * 16); img.alpha_composite(ball(6), (int(bx - 30), int(y - 60)))
    # dashed run line
    d = ImageDraw.Draw(img)
    for k in range(10):
        a = (x + 120 + k * 40, y - 40 - k * 32)
        d.line([a, (a[0] + 20, a[1] - 16)], fill=(255, 220, 80), width=7)
    score_bar(img)
    return img, 1 + 0.05 * t / D, 0

def sh_1(t, D):          # over-the-shoulder: Mason comes at you
    img = bg("gf", bg_goal_front)
    p = ease(t / D)
    # far: defenders chasing, Mason growing
    put(img, run_spr(red, t + .2, n=5) if False else run_spr(lambda **k: red(5, **k), t + .2), lerp(5, 8, p), lerp(300, 260, p), lerp(1080, 1320, p))
    s = lerp(6, 12, p)
    mx, my = lerp(620, 560, p), lerp(1020, 1420, p)
    put(img, run_spr(mason, t, rate=8, mouth="flat"), int(s), mx, my)
    img.alpha_composite(ball(int(s * 0.7)), (int(mx + s * 5), int(my - s * 7)))
    # you: back, ready stance, gentle breathing bob
    bob = 8 * math.sin(t * 5)
    put(img, hero(view="back", gloves=True, pose="ready"), 28, 540, 2330 + bob, sh=False)
    return img, 1 + 0.07 * p, 0

def sh_2(t, D):          # the shot: ball flies at the camera
    img = bg("gf", bg_goal_front).filter(ImageFilter.GaussianBlur(4))
    p = t / D
    put(img, mason(mouth="open", pose="celebrate" if False else "stand"), 14, 540, 1500)
    k = int(lerp(5, 46, p ** 1.6))
    cx, cy = 560 + 40 * p, lerp(1250, 900, p)
    if p > 0.05: speed_lines(img, cx, cy, r0=k * 5 + 40, seed=int(t * 12))
    if p < 0.25: glow_ring(img, 560, 1260, 80 + 300 * p)
    b = ball(k); img.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))
    return img, 1.0, 10 * p

def sh_3(t, D):          # the dive (slow motion) — front view of the goal
    img = bg("gf", bg_goal_front)
    draw_goal(img)
    p = ease(t / D)
    x0, x1, yt, yb = GOAL
    # hero: push-off then flight to the top corner (viewer's right)
    hx = lerp(540, 790, p); hy = yb - lerp(0, 230, math.sin(min(1, p * 1.15) * math.pi / 2))
    rot = lerp(0, -70, ease(p * 1.4))
    spr = hero(gloves=True, pose="dive" if p > 0.12 else "ready", mouth="open" if p > 0.3 else "flat")
    put(img, spr, 11, hx, hy, rot=rot, sh=False)
    shadow(img, hx, yb + 6, 220 * (1 - p * 0.4))
    # the ball, curling into the top corner
    bp = min(1, t / D * 1.05)
    bx, by = lerp(470, 845, bp), lerp(1650, 735, bp) - 120 * math.sin(bp * math.pi)
    k = int(lerp(14, 7, bp))
    d = ImageDraw.Draw(img)
    for q in range(10):        # yellow curved arc behind the ball
        a = max(0, bp - q * 0.03); ax, ay = lerp(470, 845, a), lerp(1650, 735, a) - 120 * math.sin(a * math.pi)
        d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=(255, 210, 60))
    img.alpha_composite(ball(k), (int(bx - 5 * k), int(by - 5 * k)))
    return img, 1.02 + 0.08 * p, 0

def sh_4(t, D):          # fingertips -> over the bar -> land -> celebrate, crowd jumps
    img = bg("gf", bg_goal_front)
    x0, x1, yt, yb = GOAL
    jump = abs(math.sin(t * 9)) * 18 if t > 0.5 else 0
    if jump:
        top = img.crop((0, 370, FW, 820)); img.paste(top, (0, int(370 - jump)))
    draw_goal(img)
    if t < 0.55:          # contact: ball touched over the bar
        p = t / 0.55
        put(img, hero(gloves=True, pose="dive", mouth="open"), 11, 800, yb - 230 + 40 * p, rot=-70, sh=False)
        bx, by = 860 + 60 * p, 700 - 160 * p
        img.alpha_composite(ball(7), (int(bx - 35), int(by - 35)))
        if p < 0.5: glow_ring(img, 860, 700, 60 + 160 * p); flash(img, 0.6 * (1 - p * 2))
        return img, 1.12, 14 * (1 - p)
    if t < 1.0:           # lands on the grass
        put(img, hero(gloves=True, pose="dive", mouth="open"), 11, 780, yb + 40, rot=-90, sh=True)
        return img, 1.08, 6 if t < 0.65 else 0
    # celebration
    p = min(1, (t - 1.0) / 0.4)
    put(img, hero(gloves=True, pose="celebrate", mouth="grin"), 13, 560, yb + 260 - 30 * abs(math.sin(t * 7)))
    d = ImageDraw.Draw(img)
    for i in range(14):
        a = t * 1.3 + i; sx = (i * 137 + t * 90) % FW; sy = 300 + (i * 211 + t * 240) % 700
        d.rectangle([sx, sy, sx + 14, sy + 14], fill=[Y, TEAL, RED, (255, 255, 255)][i % 4])
    return img, 1.0 + 0.04 * p, 0

def sh_5(t, D):          # Grandad on his feet in seat 14
    img = bg("st", bg_stand)
    p = t / D
    jump = abs(math.sin(t * 6)) * 14
    put(img, mum(pose="celebrate", mouth="grin"), 13, 190, 1640 - jump * 0.6, sh=False)
    k, cx, foot = 22, 600, 1960 - jump
    put(img, grandad(pose="wave", mouth="grin"), k, cx, foot, sh=False)
    # his cane, raised high in the right hand (held, not floating)
    d = ImageDraw.Draw(img)
    hx, hy = cx + 6 * k, foot - 29 * k
    d.rectangle([hx - 6, hy - 9 * k, hx + 12, hy + 6 * k], fill=(120, 78, 40), outline=(26, 20, 30), width=5)
    d.rectangle([hx - 3 * k, hy - 9 * k - 2, hx + 12, hy - 8 * k + 2], fill=(120, 78, 40), outline=(26, 20, 30), width=5)
    d.rectangle([hx - 3 * k, hy - 8 * k, hx - 3 * k + 18, hy - 7 * k + 4], fill=(120, 78, 40), outline=(26, 20, 30), width=5)
    # hand over the cane
    d.rectangle([hx - k, hy - k // 2, hx + k, hy + k], fill=(241, 196, 156), outline=(26, 20, 30), width=5)
    # seat number plate
    d.rounded_rectangle([800, 1700, 1000, 1780], 12, fill=(10, 14, 34), outline=Y, width=4)
    d.text((900, 1740), "SEAT 14", font=font(800, 34), fill=Y, anchor="mm")
    return img, 1.0 + 0.07 * p, 0

def sh_6(t, D):          # locker room: you walk in, the coach stops you
    img = bg("lk", locker_plain)
    p = min(1, t / (D * 0.7))
    put(img, alfie(pose="sit", mouth="smile"), 10, 170, 1170, sh=False)
    put(img, dixon(pose="sit"), 10, 930, 1170, sh=False)
    hx = lerp(-80, 420, ease(p))
    spr = hero(pose="run", step=int(t * 5) % 2) if p < 1 else hero(mouth="flat")
    put(img, spr, 14, hx, 1700)
    put(img, coach(mouth="open" if p >= 1 and int(t * 6) % 2 else "flat"), 14, 790, 1700)
    return img, 1.0 + 0.05 * t / D, 0

def sh_7(t, D):          # close-up: "tomorrow, you start"
    img = bg("lk", locker_plain).filter(ImageFilter.GaussianBlur(5))
    p = ease(t / (D * 0.5))
    face = hero(mouth="open" if t > D * 0.35 else "flat")
    k = 44
    put(img, face, k, 540, 2700, sh=False)        # head + shoulders fill the frame
    if t > D * 0.35:
        d = ImageDraw.Draw(img)
        for i, (sx, sy) in enumerate(((210, 760), (880, 700), (930, 1000))):
            s = 18 + 6 * math.sin(t * 10 + i)
            d.polygon([(sx, sy - s * 2), (sx + s * .5, sy - s * .5), (sx + s * 2, sy), (sx + s * .5, sy + s * .5),
                       (sx, sy + s * 2), (sx - s * .5, sy + s * .5), (sx - s * 2, sy), (sx - s * .5, sy - s * .5)], fill=Y)
    return img, 1.0 + 0.06 * p, 0

def ending_base():
    scenes.REC = []; im = scenes.s_ending(); scenes.REC = None
    return im.convert("RGBA")

def sh_8(t, D):          # the choice: two cards + typing box
    img = bg("end", ending_base)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([170, 600, 910, 680], 40, fill=(10, 14, 34), outline=(220, 224, 240), width=4)
    word = "STAY"; n = int(max(0, t - D * 0.45) * 6)
    shown = word[:min(4, n)] + ("|" if int(t * 3) % 2 else "")
    d.text((215, 640), shown, font=font(800, 40), fill=Y, anchor="lm")
    pulse = 1 + 0.03 * math.sin(t * 6)
    return img, pulse, 0

SHOTS = [sh_0, sh_1, sh_2, sh_3, sh_4, sh_5, sh_6, sh_7, sh_8]

def caption_for(t):
    # find the line being spoken; karaoke by character share
    li = 0
    for i, (a, b) in enumerate(SPAN):
        if t >= a - 0.12: li = i
    a, b = SPAN[li]
    words = LINES[li]
    lens = np.cumsum([len(w) + 1 for w, _ in words]); lens = lens / lens[-1]
    spoken = int(np.searchsorted(lens, (t - a) / max(0.1, b - a), side="right")) + (1 if t >= a else 0)
    return words, min(len(words), max(0, spoken))

def render():
    tmp = os.path.join(OUT, "tframes"); os.makedirs(tmp, exist_ok=True)
    N = int(TOTAL * FPS)
    for fi in range(N):
        t = fi / FPS
        si = max(i for i in range(len(STARTS)) if STARTS[i] <= t)
        img, z, shake = SHOTS[si](t - STARTS[si], DUR[si])
        if shake:
            img = img.transform(img.size, Image.AFFINE, (1, 0, random.uniform(-shake, shake), 0, 1, random.uniform(-shake, shake)))
        w, h = int(FW / z), int(FH / z)
        img = img.crop(((FW - w) // 2, (FH - h) // 2, (FW - w) // 2 + w, (FH - h) // 2 + h)).resize((FW, FH), Image.NEAREST)
        if t - STARTS[si] < 0.06 and si: flash(img, 0.25)
        banner(img)
        words, sp = caption_for(t)
        caption(img, words, spoken=sp)
        img.convert("RGB").save(os.path.join(tmp, f"f{fi:05d}.png"))
    return tmp

# ------------------------------------------------------------------ sound
SR = 44100
def sfx():
    N = int((TOTAL + .1) * SR); out = np.zeros(N, np.float32); rng = np.random.default_rng(3)
    def add(t, sig, g=1.):
        i = int(t * SR)
        if 0 <= i < N: n = min(len(sig), N - i); out[i:i + n] += g * sig[:n]
    lp = lambda x, k: np.convolve(x, np.ones(k) / k, "same")
    noise = lambda d: rng.standard_normal(int(d * SR)).astype(np.float32)
    def env(n, a=.005, r=.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
    def kick(t, g=1): x = np.arange(int(.25 * SR)) / SR; add(t, np.sin(2 * np.pi * (150 * np.exp(-x * 18) + 60) * x) * np.exp(-x * 14) + .3 * noise(.25) * np.exp(-x * 60), .55 * g)
    def thud(t, g=1): x = np.arange(int(.4 * SR)) / SR; add(t, np.sin(2 * np.pi * (90 * np.exp(-x * 5)) * x) * np.exp(-x * 9), .6 * g)
    def whoosh(t, g=1): n = int(.3 * SR); add(t - .08, lp(noise(.3), 10) * np.sin(np.linspace(0, np.pi, n)) ** 2, .2 * g)
    def roar(t, d=1.6, g=1): n = int(d * SR); add(t, lp(noise(d), 30) * np.sin(np.linspace(0, np.pi, n)) ** .7, .35 * g)
    def whistle(t, d=.5): x = np.arange(int(d * SR)) / SR; add(t, np.sin(2 * np.pi * (2900 + 60 * np.sin(2 * np.pi * 30 * x)) * x) * np.minimum(1, x / .02) * np.minimum(1, (d - x) / .05), .12)
    def tick(t): add(t, np.sin(2 * np.pi * 1200 * np.arange(int(.05 * SR)) / SR) * env(int(.05 * SR), .002, .02), .12)
    bed = lp(noise(N / SR), 40)[:N] * 0.05
    S = STARTS
    bed[int(S[6] * SR):] *= 0.15          # inside the locker room: quiet
    out += bed
    thud(0, 1.4)
    for s in S[1:]: whoosh(s)
    for k in range(int(DUR[0] * 3.5)): kick(S[0] + 0.2 + k / 3.5, 0.35)
    for k in range(int(DUR[1] * 4)): kick(S[1] + 0.15 + k / 4, 0.3 + 0.1 * k / 4)
    kick(S[2] + 0.02, 1.5); whoosh(S[2] + 0.3, 2)
    thud(S[3] + 0.1, .8); whoosh(S[3] + 0.4, 1.5)
    thud(S[4] + 0.02, 1.4); roar(S[4] + 0.1, 3.2, 1.8); thud(S[4] + 0.6, 1.0)
    roar(S[5], DUR[5], 1.2)
    whistle(S[6] - 0.6, 0.9)
    for k in range(4): thud(S[6] + 0.2 + k * 0.4, .4)
    thud(S[7] + 0.05, 1.0)
    for k in range(4): tick(S[8] + DUR[8] * 0.45 + k / 6)
    out[-int(.4 * SR):] *= np.linspace(1, 0, int(.4 * SR))
    return out

def mix():
    fx = sfx(); N = len(fx)
    if not HAVE_VO:
        vv = np.zeros(N, np.float32); out = fx / max(1, np.abs(fx).max() / 0.95)
    else:
        v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                     capture_output=True).stdout, np.int16).astype(np.float32) / 32768
        vv = np.zeros(N, np.float32); i0 = int(LEAD * SR); n = min(len(v), N - i0); vv[i0:i0 + n] = v[:n]
        e = np.convolve(np.abs(vv), np.ones(2205) / 2205, "same")
        out = fx * (1 - 0.55 * np.clip(e / 0.05, 0, 1)) + vv
        out /= max(1, np.abs(out).max() / 0.95)
    import wave
    p = os.path.join(OUT, "test_mix.wav")
    w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
    return p

if __name__ == "__main__":
    import sys
    print("starts", [round(s, 2) for s in STARTS], "total", round(TOTAL, 2))
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i, s in enumerate(STARTS):
            t = s + DUR[i] * 0.6
            img, z, _ = SHOTS[i](t - s, DUR[i]); banner(img); w_, sp = caption_for(t); caption(img, w_, spoken=sp)
            img.convert("RGB").resize((360, 640)).save(os.path.join(OUT, f"_chk{i}.png"))
        raise SystemExit
    tmp = render(); wav = mix()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"), "-i", wav,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    os.path.join(OUT, "TEST_style.mp4")], check=True)
    subprocess.run(["rm", "-rf", tmp])
    print("done")
