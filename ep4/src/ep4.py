"""EP4 — the night at the hospital, the trial at Riverside. EP5/EP6 style engine."""
import os, sys, json
from persp import *
from persp import _xzy, _c
from cast4 import *
from PIL import ImageEnhance

PLATFORM = os.environ.get("PLATFORM", "tiktok")
EP = 4
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
FOLLOW = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"
if PLATFORM == "youtube":
    VOTE = [("YOU", W), ("CHOSE", W), ("GRANDAD.", B), ("SO", W), ("YOU", W), ("STAYED.", W), ("ALL", W), ("NIGHT.", B)]
else:
    VOTE = [("YOU", W), ("CHOSE", W), ("THE", W), ("TRIAL.", Y), ("BUT", W), ("FIRST...", W), ("ONE", W), ("NIGHT.", B)]
LINES = [
    [("THEY", W), ("STARTED", W), ("WITHOUT", R_), ("YOU.", R_)],
    VOTE,
    [("HOSPITAL", W), ("CHAIR.", W), ("BEEPING", W), ("MONITOR.", G), ("NO", R_), ("SLEEP.", R_)],
    [("FOUR", B), ("A.M.", B), ("HIS", W), ("HAND", W), ("FINDS", W), ("YOURS.", Y)],
    [("\"GO", W), ("TO", W), ("THAT", W), ("TRIAL.\"", Y), ("\"NOT", W), ("WITHOUT", W), ("YOU.\"", B)],
    [("EIGHT", Y), ("A.M.", Y), ("\"HE", W), ("CAN", W), ("GO", G), ("HOME.\"", G)],
    [("GRANDAD", B), ("GRABS", W), ("HIS", W), ("CANE.", W), ("\"HOME?", W), ("NO.", R_), ("RIVERSIDE.\"", Y)],
    [("MUM'S", W), ("OLD", W), ("CAR.", W), ("TWO", Y), ("HOURS.", Y), ("RAIN.", B)],
    [("YOU", W), ("SPRINT.", Y), ("GLOVES", O), ("IN", W), ("HAND.", W)],
    [("\"KEEPERS", W), ("WERE", W), ("AT", W), ("NINE", Y), ("THIRTY.", Y), ("TOO", R_), ("LATE.\"", R_)],
    [("MASON", R_), ("LAUGHS.", W), ("\"HOSPITAL", W), ("BOY.\"", R_)],
    [("THEN", W), ("THE", W), ("COACH", W), ("SEES", W), ("GRANDAD...", B), ("AND", W), ("FREEZES.", Y)],
    [("\"TEN", Y), ("MINUTES.", Y), ("TRIAL", W), ("MATCH.", W), ("GO.\"", G)],
    [("FIRST", W), ("SHOT.", W), ("THROUGH", W), ("YOUR", W), ("LEGS.", R_), ("NO", W), ("SLEEP.", R_)],
    [("YOU", W), ("GET", W), ("BACK", G), ("UP.", G), ("LIKE", W), ("GRANDAD", B), ("SAID.", W)],
    [("ONE", W), ("ON", W), ("ONE.", W), ("YOU", W), ("SPREAD", W), ("BIG.", Y), ("SAVED!", G)],
    [("LAST", R_), ("KICK.", R_), ("MASON.", R_), ("TOP", Y), ("CORNER...", Y), ("FINGERTIPS!", G), ("OUT!", G)],
    [("FINAL", W), ("WHISTLE.", W), ("\"YOU'RE", G), ("IN.\"", G)],
    [("BUT", W), ("YOU'D", W), ("LIVE", Y), ("THERE.", Y), ("TWO", W), ("HOURS", W), ("FROM", W), ("HOME.", R_)],
    [("MUM", W), ("WORKS", W), ("NIGHTS.", B), ("WHO", W), ("LOOKS", W), ("AFTER", W), ("GRANDAD?", B)],
    [("HE", W), ("JUST", W), ("SAYS,", W), ("\"GO.\"", G), ("HIS", W), ("HAND", W), ("SHAKES.", R_)],
    [("THE", W), ("ACADEMY...", Y), ("OR", W), ("HOME?", B)],
    [("VOTE", W), ("BELOW.", G), (FOLLOW, R_), ("FOR", W), ("EP. 5.", Y)],
]
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"vo/lines_{PLATFORM}.json")
if os.path.exists(_vf):
    VOICE = [tuple(x) for x in json.load(open(_vf))]
else:   # estimated narration timing (no voice yet)
    VOICE, t0 = [], 0.05
    for ws in LINES:
        d_ = max(1.3, 0.34 * len(ws) + 0.3)
        VOICE.append((t0, t0 + d_)); t0 += d_ + 0.42
STARTS = [max(0.0, a - 0.12) for a, _ in VOICE]
STARTS[0] = 0.0
TOTAL = VOICE[-1][1] + 1.6


def D(i):
    return (STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i]


def word_times(i):
    ws = LINES[i]
    st, en = VOICE[i]
    lens = [len(w) + 2 for w, _ in ws]
    tot, acc, out = sum(lens), 0, []
    for (w, c), L in zip(ws, lens):
        out.append((w, st + (en - st) * acc / tot - 0.03, c))
        acc += L
    return out


def chunks(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if w[0][-1] in ".,?!\"" or w[0].endswith("...") or len(cur) == 3:
            out.append(cur)
            cur = []
    if cur:
        if out and len(cur) == 1 and len(out[-1]) < 3 and out[-1][-1][0][-1] not in ".?!":
            out[-1] += cur
        else:
            out.append(cur)
    return out


def overlay(img, t, i):
    banner(img, EP)
    ch = chunks(word_times(i)) if i else [word_times(0)]
    cur = ch[0]
    for c in ch:
        if t >= c[0][1] - 0.04:
            cur = c
    if i == 0 and t < 0.4:          # frame 0 = TikTok preview: the first chunk fully lit
        cur = [(w, -1, c) for w, _, c in cur]
    caption(img, cur, t, size=56, wrap=620)


# ------------------------------------------------------------------ small UI
def clock_pill(img, x, y, text, k=1.0, bg=(200, 40, 50), size=40):
    if k <= 0.02:
        return
    d = ImageDraw.Draw(img)
    f = font(800, max(6, int(size * k)))
    w = d.textlength(text, font=f) + 70 * k
    h = size * 1.5 * k
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], int(16 * k), fill=bg, outline=OL, width=5)
    cx, cy, r = x - w / 2 + 30 * k, y, 13 * k          # little clock icon
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=max(1, int(4 * k)))
    d.line([(cx, cy), (cx, cy - r * 0.6)], fill=(255, 255, 255), width=max(1, int(3 * k)))
    d.line([(cx, cy), (cx + r * 0.5, cy)], fill=(255, 255, 255), width=max(1, int(3 * k)))
    d.text((x + 16 * k, y), text, font=f, fill=(255, 255, 255), anchor="mm")


def timer_value(t):
    keys = [(STARTS[12] + 0.4, 600), (STARTS[13], 560), (STARTS[15], 400), (STARTS[16], 8), (STARTS[17], 0)]
    if t <= keys[0][0]:
        return 600
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= t <= b:
            return int(lerp(va, vb, (t - a) / (b - a)))
    return 0


def score_state(t):
    return 0, (1 if t >= STARTS[13] + 0.51 * D(13) else 0)


def trial_bar(img, t):
    l, r = score_state(t)
    v = timer_value(t)
    d = ImageDraw.Draw(img)
    y = 248
    d.rounded_rectangle([150, y, 570, y + 54], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.rectangle([162, y + 11, 186, y + 43], fill=TRI); d.rectangle([424, y + 11, 448, y + 43], fill=RS)
    d.text((305, y + 27), f"TRIAL  {l} - {r}  RIV", font=font(800, 24), fill=(255, 255, 255), anchor="mm")
    d.rounded_rectangle([460, y + 9, 560, y + 45], 8, fill=(210, 52, 56))
    d.text((510, y + 27), f"{v // 60}:{v % 60:02d}", font=font(800, 22), fill=(255, 255, 255), anchor="mm")


def slowmo_bars(img, k):
    if k <= 0:
        return
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, FW, int(40 * k)], fill=(0, 0, 0))
    d.rectangle([0, FH - int(40 * k), FW, FH], fill=(0, 0, 0))


def vignette(img, a=0.5, col=(0, 0, 0)):
    key = ("vig", a, col)
    if key not in _c:
        m = Image.new("L", (FW, FH), 0)
        ImageDraw.Draw(m).ellipse([-200, -100, FW + 200, FH + 100], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(160)).point(lambda v: int((255 - v) * a))
        lay = Image.new("RGBA", (FW, FH), col + (255,))
        lay.putalpha(m)
        _c[key] = lay
    img.alpha_composite(_c[key])


# ------------------------------------------------------------------ academy exterior
def academy_bg(hor=470):
    """golden morning after the rain: tree line + Riverside Academy building behind the fence, a few parents"""
    key = ("acad", hor)
    if key in _c:
        return _c[key].copy()
    img = backdrop(hor, sun=(600, 260), stadium=False)
    d = ImageDraw.Draw(img)
    fy = hor - 30
    # building: two-storey block with glass windows, red stripe, crest and sign
    bx0, bx1, by0 = 170, 570, fy - 128
    d.rectangle([bx0, by0, bx1, fy - 6], fill=(232, 228, 222), outline=OL, width=5)
    d.rectangle([bx0, by0, bx1, by0 + 26], fill=RS, outline=OL, width=4)
    for r in range(2):
        for k in range(7):
            x = bx0 + 18 + k * 54
            y = by0 + 38 + r * 42
            d.rectangle([x, y, x + 36, y + 30], fill=(120, 170, 220), outline=OL, width=3)
            d.line([(x + 6, y + 24), (x + 24, y + 6)], fill=(200, 230, 255), width=3)
    d.rounded_rectangle([bx0 + 80, by0 - 40, bx1 - 80, by0 - 6], 8, fill=(16, 18, 36), outline=OL, width=4)
    d.text(((bx0 + bx1) / 2, by0 - 23), "RIVERSIDE ACADEMY", font=font(800, 22), fill=C_Y, anchor="mm")
    # crest
    cx, cy = (bx0 + bx1) / 2, by0 + 13
    d.polygon([(cx - 16, cy - 10), (cx + 16, cy - 10), (cx + 16, cy + 4), (cx, cy + 16), (cx - 16, cy + 4)], fill=C_Y, outline=OL)
    # flag poles (flags are animated per frame)
    for x in (100, 640):
        d.rectangle([x - 3, fy - 170, x + 3, fy - 6], fill=(200, 204, 214), outline=OL, width=2)
    # re-draw the fence in front of the building
    d.rectangle([0, fy, FW, hor + 4], fill=(110, 116, 140))
    for xx in range(0, FW, 10):
        d.line([(xx, fy), (xx + 10, hor + 4)], fill=(150, 156, 176), width=1)
        d.line([(xx + 10, fy), (xx, hor + 4)], fill=(150, 156, 176), width=1)
    for xx in range(0, FW, 60):
        d.rectangle([xx, fy - 6, xx + 4, hor + 4], fill=(70, 74, 92))
    d.rectangle([0, fy - 6, FW, fy - 3], fill=(70, 74, 92))
    # a handful of parents behind the fence (small local trial)
    rng = random.Random(4)
    for x in (40, 70, 560, 600, 680):
        sp = person(Kit(rng.choice([(70, 108, 189), (200, 120, 60), (90, 90, 100), (40, 120, 90)]), (40, 44, 60), (40, 44, 60)),
                    skin=rng.choice(["light", "tan", "brown"]), hair=rng.choice(["dark", "brown", "blond", "black"]), trousers=True)
        paste(img, sp, 2, x, hor + 2)
    _c[key] = img
    return img.copy()


def flags(img, t, hor=560):
    d = ImageDraw.Draw(img)
    fy = hor - 30
    for x in (100, 640):
        pts = []
        for k in range(9):
            pts.append((x + 3 + k * 7, fy - 166 + 6 * math.sin(t * 7 - k * 0.8) * k / 8))
        top = pts
        bot = [(px, py + 34) for px, py in pts[::-1]]
        d.polygon(top + bot, fill=RS, outline=OL)
        d.line([(px, py + 17) for px, py in pts], fill=(250, 250, 250), width=4)


def academy_set(hor=470, Zg=None, camX=0.0, camH=1.7, f=FOC):
    c = Cam(camX=camX, camH=camH, hor=hor, f=f)
    img = academy_bg(hor)
    pitch_persp(img, c, Zgoal=Zg)
    return img, c


def drills(img, c, t, Zg=30.0):
    """the trial is already on: far goal, a keeper diving in a drill, a coach with a ball"""
    goal3d(img, c, Zg, X=2.0, w=4.4, h=1.8)
    ph = (t * 0.45) % 1
    keeper_world(img, c, 2.0, Zg, 1 if int(t * 0.45) % 2 else -1, ph, 1.5, sprite=None) if False else None
    ground_shadow(img, c, 2.0, Zg, 0.4)
    side = 1 if int(t * 0.5) % 2 else -1
    jump = math.sin(((t * 0.5) % 1) * math.pi) if (t * 0.5) % 1 < 1 else 0
    sprite_at(img, c, dixon(pose="ready"), 2.0 + side * 0.6 * jump, Zg, Y=0.3 * jump, height_m=1.5)
    for i, (X, Z, n) in enumerate(((-3.0, Zg - 6, 3), (-5.0, Zg - 4, 5), (5.5, Zg - 7, 8), (0.5, Zg - 9, 6))):
        ground_shadow(img, c, X, Z, 0.3)
        sprite_at(img, c, trialist(n, pose="run", phase=t * 2 + i), X + math.sin(t * 1.3 + i) * 0.8, Z, height_m=1.5)
    for i, (X, Z, n) in enumerate(((-1.5, Zg - 12, 7), (3.5, Zg - 11, 4))):
        ground_shadow(img, c, X, Z, 0.3)
        sprite_at(img, c, academy(n, pose="run", phase=t * 2 + i), X + math.cos(t * 1.1 + i) * 0.8, Z, height_m=1.5)
    ground_shadow(img, c, -6.5, Zg - 3, 0.3)
    sprite_at(img, c, coach(), -6.5, Zg - 3, height_m=1.7)


# ------------------------------------------------------------------ hospital
def hospital(t, night=True):
    key = ("hosp", night)
    if key not in _c:
        wall = (70, 84, 130) if night else (214, 226, 236)
        img = Image.new("RGBA", (FW, FH), wall + (255,))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 600, FW, 640], fill=shade(wall, 0.9))            # dado rail band
        d.line([(0, 600), (FW, 600)], fill=shade(wall, 0.75), width=4)
        # floor in one-point perspective (vanishing point at 360, 420)
        fl = ((56, 64, 96), (50, 58, 88)) if night else ((196, 204, 214), (184, 192, 204))
        d.rectangle([0, 800, FW, FH], fill=fl[0])
        for r in range(12):
            y0 = 800 + (r ** 1.45) * 9
            y1 = 800 + ((r + 1) ** 1.45) * 9
            if r % 2:
                d.rectangle([0, y0, FW, y1], fill=fl[1])
        for k in range(-8, 9):
            d.line([(360 + k * 40, 800), (360 + k * 190, FH)], fill=shade(fl[0], 0.85), width=3)
        d.rectangle([0, 792, FW, 806], fill=shade(wall, 0.6))              # skirting
        # window (right): town at night / morning sky
        wx0, wy0, wx1, wy1 = 440, 190, 690, 520
        sky = Image.new("RGB", (wx1 - wx0, wy1 - wy0))
        sd = ImageDraw.Draw(sky)
        top, bot = ((16, 20, 50), (50, 50, 96)) if night else ((120, 170, 230), (236, 220, 190))
        for y in range(wy1 - wy0):
            sd.line([(0, y), (wx1 - wx0, y)], fill=tuple(int(lerp(a, b, y / (wy1 - wy0))) for a, b in zip(top, bot)))
        rng = random.Random(7)
        for k in range(9):                                                 # roofs and chimneys
            x = k * 30 - 10
            h = rng.randint(60, 130)
            col = (30, 30, 52) if night else (150, 80, 66)
            sd.rectangle([x, wy1 - wy0 - h, x + 30, wy1 - wy0], fill=col)
            sd.rectangle([x + 18, wy1 - wy0 - h - 16, x + 24, wy1 - wy0 - h], fill=col)
            for wy in range(wy1 - wy0 - h + 14, wy1 - wy0 - 10, 26):
                if rng.random() < (0.5 if night else 0.9):
                    sd.rectangle([x + 6, wy, x + 14, wy + 10], fill=(250, 210, 110) if night else (190, 220, 240))
        if night:
            sd.ellipse([180, 30, 214, 64], fill=(240, 240, 220))
        img.paste(sky, (wx0, wy0))
        d.rectangle([wx0 - 10, wy0 - 10, wx1 + 10, wy1 + 10], outline=(240, 242, 246), width=12)
        d.line([((wx0 + wx1) / 2, wy0), ((wx0 + wx1) / 2, wy1)], fill=(240, 242, 246), width=8)
        d.rectangle([wx0 - 20, wy1 + 8, wx1 + 20, wy1 + 22], fill=(240, 242, 246), outline=OL, width=3)
        # curtain on a rail
        d.rectangle([380, 160, 710, 168], fill=(160, 166, 180))
        for k in range(5):
            d.rectangle([384 + k * 14, 168, 396 + k * 14, 600], fill=(90, 150, 170) if k % 2 else (80, 136, 156))
        d.rectangle([384, 168, 454, 600], outline=OL, width=3)
        # wall panel with oxygen + sockets above the bed head
        d.rounded_rectangle([250, 380, 430, 440], 10, fill=(236, 238, 242), outline=OL, width=4)
        for k in range(3):
            d.ellipse([270 + k * 50, 396, 296 + k * 50, 422], fill=(80, 170, 110) if k == 0 else (200, 204, 214), outline=OL, width=3)
        # cabinet left with flowers + cup
        d.rectangle([20, 650, 150, 900], fill=(236, 230, 220), outline=OL, width=5)
        d.rectangle([34, 700, 136, 790], outline=(190, 182, 170), width=4)
        d.rectangle([70, 745, 100, 752], fill=(150, 150, 160))
        d.rectangle([60, 586, 96, 650], fill=(150, 200, 230), outline=OL, width=4)       # vase
        for fx, fy, col in ((58, 560, (240, 80, 90)), (80, 548, (250, 206, 40)), (100, 566, (240, 120, 160))):
            d.line([(78, 590), (fx + 8, fy + 10)], fill=(60, 130, 70), width=4)
            d.ellipse([fx, fy, fx + 18, fy + 18], fill=col, outline=OL, width=2)
        d.rectangle([110, 622, 140, 650], fill=(250, 250, 250), outline=OL, width=3)      # cup
        # chart clipboard on the wall
        d.rectangle([180, 470, 236, 550], fill=(250, 246, 236), outline=OL, width=4)
        for k in range(4):
            d.line([(190, 492 + k * 14), (226, 492 + k * 14)], fill=(150, 150, 160), width=3)
        _c[key] = img
    img = _c[key].copy()
    d = ImageDraw.Draw(img)
    # monitor on an arm (animated ECG)
    mx0, my0, mx1, my1 = 260, 230, 420, 350
    d.line([(340, 350), (340, 380)], fill=(120, 124, 140), width=8)
    d.rounded_rectangle([mx0 - 8, my0 - 8, mx1 + 8, my1 + 8], 10, fill=(40, 44, 56), outline=OL, width=4)
    d.rectangle([mx0, my0, mx1, my1], fill=(10, 20, 18))
    pts = []
    for x in range(mx0 + 4, mx1 - 4, 2):
        ph = ((x - mx0) / 60 - t * 1.2) % 1
        y = 0
        if 0.40 < ph < 0.44: y = -30
        elif 0.44 < ph < 0.48: y = 16
        elif 0.30 < ph < 0.36: y = -5
        pts.append((x, my0 + 70 + y))
    d.line(pts, fill=(90, 240, 130), width=3)
    head = mx0 + 4 + ((t * 1.2 * 60) % (mx1 - mx0 - 8))
    d.ellipse([head - 4, my0 + 66, head + 4, my0 + 74], fill=(200, 255, 210))
    d.text((mx0 + 10, my0 + 18), "HR 64", font=font(800, 20), fill=(90, 240, 130), anchor="lm")
    d.text((mx1 - 10, my0 + 18), "SpO2 95", font=font(800, 16), fill=(120, 200, 250), anchor="rm")
    # IV stand
    d.line([(600, 300), (600, 1010)], fill=(170, 174, 186), width=8)
    d.line([(560, 1010), (640, 1010)], fill=(170, 174, 186), width=8)
    d.line([(570, 300), (630, 300)], fill=(170, 174, 186), width=6)
    d.rounded_rectangle([582, 306, 618, 380], 10, fill=(220, 236, 250), outline=OL, width=3)
    drip = (t * 1.5) % 1
    d.ellipse([597, 390 + drip * 30, 603, 398 + drip * 30], fill=(200, 230, 255))
    d.line([(600, 380), (600, 390)], fill=(200, 210, 230), width=3)
    if night:
        glow(img, 340, 290, 160, (90, 240, 130), 0.18)
    return img


def bed(img, x0=250, x1=700, top=820):
    d = ImageDraw.Draw(img)
    for x in (x0 + 20, x1 - 30):                                    # legs + wheels
        d.rectangle([x, top + 60, x + 12, top + 190], fill=(170, 174, 186), outline=OL, width=3)
        d.ellipse([x - 8, top + 182, x + 20, top + 210], fill=(60, 60, 70), outline=OL, width=3)
    d.rectangle([x0, top + 40, x1, top + 70], fill=(180, 184, 196), outline=OL, width=5)      # frame
    d.rectangle([x0, top, x1, top + 44], fill=(246, 248, 252), outline=OL, width=5)          # mattress
    d.rectangle([x0 - 16, top - 140, x0 + 6, top + 70], fill=(170, 174, 186), outline=OL, width=5)   # headboard
    d.rectangle([x1 - 6, top - 60, x1 + 14, top + 70], fill=(170, 174, 186), outline=OL, width=5)    # footboard
    d.rounded_rectangle([x0 + 8, top - 54, x0 + 120, top + 6], 18, fill=(255, 255, 255), outline=OL, width=4)   # pillow


def grandad_in_bed(img, t, x0=250, top=820, scale=8, eyes_closed=True, blanket=(110, 160, 210)):
    sp = big(grandad(pose="stand", blink=eyes_closed, mouth="flat"), scale).rotate(90, expand=True, resample=Image.NEAREST)
    img.alpha_composite(sp, (int(x0 - 44), int(top - sp.height + 8 * scale)))
    d = ImageDraw.Draw(img)
    breath = math.sin(t * 2.2) * 4
    bx = x0 + 108
    d.rounded_rectangle([bx, top - 124 - breath, 700, top + 30], 26, fill=blanket, outline=OL, width=5)
    d.line([(bx + 40, top - 60 - breath), (690, top - 56)], fill=shade(blanket, 0.82), width=4)
    d.rounded_rectangle([bx, top - 124 - breath, bx + 40, top + 30], 14, fill=(250, 250, 252), outline=OL, width=4)   # sheet fold


def chair(img, cx, by):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 96, by - 262, cx + 96, by - 84], 22, fill=(60, 110, 150), outline=OL, width=6)    # backrest
    d.rounded_rectangle([cx - 106, by - 96, cx + 106, by - 60], 14, fill=(70, 124, 166), outline=OL, width=6)    # seat at his hips
    for x in (cx - 92, cx + 80):
        d.rectangle([x, by - 60, x + 12, by + 6], fill=(150, 154, 166), outline=OL, width=3)


# ------------------------------------------------------------------ scenes
def s_hook(t, u, T, cont=False):
    """you sprint at the camera across the academy grass; behind you, the trial has already started"""
    img, c = academy_set(600, None, camX=0.0, camH=1.0)
    flags(img, t, 600)
    drills(img, c, t, 30.0)
    v = clamp((t - T) / D(0)) if not cont else 1.0
    Z = lerp(5.4, 2.6, v)
    hx, hy = c.p(-0.4, Z, 0.75)
    speed_lines(img, t, hx, hy, n=10, a=60, r0=1.0 * c.k(Z) + 40, r1=1.0 * c.k(Z) + 420)
    ground_shadow(img, c, -0.4, Z, 0.4)
    sprite_at(img, c, hero(pose="run", phase=t * 2.8, gloves=True, mouth="open"), -0.4, Z, Y=abs(math.sin(t * 2.8 * math.pi)) * 0.06, height_m=1.5)
    clock_pill(img, 360, 300, "10:02", spring(t - 0.0, 14, 7) if t > 0.05 else 1.0)
    return cam(img, 1.02 + 0.06 * v, 360, 800)


def s_rewind(t, u, T):
    """the hook rewinds (VHS lines) into the night before; the vote result stamps in"""
    if u < 0.35:
        k = u / 0.35
        img = s_hook(STARTS[1] - k * 2.0, 1 - k, 0.0)
        img = img.convert("RGB")
        img = Image.blend(img, Image.new("RGB", img.size, (20, 24, 60)), 0.35 * k).convert("RGBA")
        d = ImageDraw.Draw(img, "RGBA")
        rng = random.Random(int(t * 30))
        for _ in range(8):
            y = rng.uniform(0, FH)
            d.rectangle([0, y, FW, y + rng.uniform(4, 16)], fill=(255, 255, 255, 60))
        d.polygon([(300, 640), (360, 600), (360, 680)], fill=(255, 255, 255, 220))
        d.polygon([(360, 640), (420, 600), (420, 680)], fill=(255, 255, 255, 220))
        return img
    img = hospital(t, night=True)
    bed(img); grandad_in_bed(img, t)
    chair(img, 150, 1010)
    paste(img, hero(pose="sit", blink=False, mouth="flat"), 8, 150, 1010)
    img = img.convert("RGB")
    img = Image.blend(img, Image.new("RGB", img.size, (10, 12, 30)), 0.5).convert("RGBA")
    k = spring(t - T - 0.35 * D(1), 13, 7)
    pill(img, 360, 560, "12 HOURS EARLIER", (40, 60, 140), k, 40)
    vote = "YOU CHOSE: GRANDAD" if PLATFORM == "youtube" else "YOU CHOSE: TRIAL"
    pill(img, 360, 680, vote, (40, 150, 80), spring(t - T - 0.5 * D(1), 13, 7), 34)
    return cam(img, 1.0 + 0.04 * u, 360, 700)


def s_chair(t, u, T):
    img = hospital(t, night=True)
    bed(img); grandad_in_bed(img, t)
    chair(img, 150, 1010)
    paste(img, hero(pose="sit", blink=int(t * 2) % 9 == 0, mouth="flat"), 8, 150, 1010)
    vignette(img, 0.55)
    if u < 0.5:
        clock_pill(img, 190, 600, "23:47", spring(t - T, 13, 7), bg=(40, 60, 140))
        return cam(img, 1.0 + 0.05 * u, 360, 760)
    return cam(img, 1.55 + 0.08 * u, 210, 820)       # push on your tired face


HAND_SK = SKIN["light"][0]


def s_hands(t, u, T):
    """4 a.m. close-up from above: Grandad's old hand slides over yours (red bracelet) on the blanket"""
    S = 8
    w, h = FW // S, FH // S                      # 90 x 160 art pixels
    im = Image.new("RGBA", (w, h), (84, 122, 172, 255))
    d = ImageDraw.Draw(im)
    for y in range(30, h, 9):                                  # blanket folds
        d.line([(0, y), (w, y - 3)], fill=(74, 110, 158), width=2)
    d.rectangle([0, 0, w, 26], fill=(28, 32, 58))              # dark room beyond the bed
    d.rectangle([0, 26, w, 30], fill=(244, 246, 250))          # sheet edge
    d.rectangle([0, 31, w, 31], fill=(200, 206, 220))
    sk, skd = SKIN["light"]
    # YOUR right hand, palm down, fingers up the screen, thumb on the left; green sleeve + red bracelet
    d.polygon([(18, 160), (22, 128), (46, 128), (52, 160)], fill=(40, 168, 74))
    d.rectangle([22, 126, 46, 130], fill=(30, 140, 60))
    d.rectangle([26, 100, 42, 127], fill=sk)                   # forearm
    d.rectangle([39, 100, 42, 127], fill=skd)
    d.rectangle([25, 112, 43, 115], fill=(225, 30, 40))        # red bracelet
    d.rectangle([28, 113, 29, 114], fill=(255, 120, 120))
    d.rectangle([22, 80, 46, 101], fill=sk)                    # back of the hand
    d.rectangle([43, 80, 46, 101], fill=skd)
    for k in range(4):                                         # fingers
        fx = 23 + k * 6
        top = 62 - (2 if k in (1, 2) else 0)
        d.rectangle([fx, top, fx + 4, 80], fill=sk)
        d.rectangle([fx + 4, top + 2, fx + 4, 80], fill=skd)
        d.rectangle([fx + 1, top, fx + 3, top + 1], fill=(250, 214, 190))   # nail
    d.polygon([(22, 92), (14, 82), (12, 76), (17, 74), (24, 84)], fill=sk)  # thumb
    # GRANDAD's left hand slides in from the right and covers yours
    k = ease_in_out(clamp(u / 0.55))
    ox = int(round(lerp(52, 0, k)))
    grip = clamp((u - 0.6) / 0.2)
    old, oldd = SKIN["old"]
    cy = 78
    d.rectangle([62 + ox, cy - 13, 95 + ox, cy + 15], fill=(150, 98, 58))            # cardigan sleeve
    d.rectangle([62 + ox, cy - 13, 66 + ox, cy + 15], fill=(120, 76, 44))            # cuff
    for by_ in (cy - 6, cy + 6):
        d.rectangle([70 + ox, by_, 71 + ox, by_ + 1], fill=(240, 206, 120))
    d.rectangle([40 + ox, cy - 11, 62 + ox, cy + 11], fill=old)                       # back of his hand
    d.rectangle([40 + ox, cy + 8, 62 + ox, cy + 11], fill=oldd)
    for (sx, sy) in ((48, cy - 4), (55, cy + 2), (51, cy + 5)):                       # age spots
        d.point((sx + ox, sy), fill=(196, 150, 116))
    for j in range(3):                                                                 # veins / knuckles
        d.line([(44 + ox, cy - 6 + j * 6), (58 + ox, cy - 6 + j * 6)], fill=oldd)
    flen = int(lerp(18, 13, grip))
    for j in range(4):                                                                 # fingers over yours
        fy = cy - 10 + j * 5
        d.rectangle([40 + ox - flen, fy, 40 + ox, fy + 3], fill=old)
        d.rectangle([40 + ox - flen, fy + 3, 40 + ox, fy + 3], fill=oldd)
    d.polygon([(48 + ox, cy - 11), (40 + ox, cy - 20), (34 + ox, cy - 20), (36 + ox, cy - 14), (42 + ox, cy - 8)], fill=old)  # thumb
    im = outline(im)
    img = im.resize((w * S, h * S), Image.NEAREST)
    glow(img, 360, 100, 320, (90, 240, 130), 0.14)
    clock_pill(img, 360, 300, "04:00", spring(t - T, 13, 7), bg=(40, 60, 140))
    if 0.6 < u < 0.85:
        glow_ring(img, 280, 640, 160 * clamp((u - 0.6) * 5), 0.45, (255, 240, 200))
    vignette(img, 0.45)
    return cam(img, 1.02 + 0.06 * u, 330, 700)


def portrait_room(t, night=True):
    img = hospital(t, night).filter(ImageFilter.GaussianBlur(6))
    return img


def s_talk(t, u, T):
    """'Go to that trial.' (Grandad, in bed)  /  'Not without you.' (you)"""
    img = portrait_room(t, True)
    d = ImageDraw.Draw(img)
    if u < 0.5:
        d.rounded_rectangle([110, 520, 610, 1000], 60, fill=(250, 250, 252), outline=OL, width=8)   # pillow behind him
        talk = int(t * 7) % 2 == 0 and u < 0.42
        paste(img, grandad(pose="sit", mouth="open" if talk else "smile", blink=0.3 < u < 0.33), 20, 360, 1290)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([20, 1090, 700, 1300], 30, fill=(110, 160, 210), outline=OL, width=8)  # blanket
        d.line([(60, 1150), (660, 1140)], fill=(90, 136, 186), width=6)
        vignette(img, 0.5)
        return cam(img, 1.0 + 0.05 * u, 360, 800)
    paste(img, hero(mouth="flat", blink=0.8 < u < 0.83, look=-1), 22, 380, 1480)
    vignette(img, 0.5)
    return cam(img, 1.0 + 0.05 * (u - 0.5), 360, 800)


def s_doctor(t, u, T):
    img = hospital(t, night=False)
    bed(img)
    d = ImageDraw.Draw(img)
    # Grandad sits up in bed, blanket on his legs
    d.rounded_rectangle([258, 690, 380, 830], 18, fill=(255, 255, 255), outline=OL, width=4)
    paste(img, grandad(pose="sit", mouth="smile", blink=int(t * 2) % 7 == 0), 8, 360, 900)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([300, 760, 700, 850], 20, fill=(110, 160, 210), outline=OL, width=5)
    # you, standing by the bed
    paste(img, hero(mouth="open" if u > 0.7 else "flat", look=-1), 8, 330, 1060)
    # the doctor walks in from the left and nods
    k = ease_out(clamp(u / 0.35))
    x = lerp(-120, 120, k)
    walking = k < 0.98
    nod = 8 if 0.55 < u < 0.68 else 0
    sp = doctor(pose="run" if walking else "stand", phase=t * 1.6, mouth="smile", look=1)
    paste(img, sp, 9, x, 1120 + nod)
    if not walking:   # clipboard in his hand
        d = ImageDraw.Draw(img)
        d.rectangle([x + 40, 960 + nod, x + 86, 1020 + nod], fill=(250, 246, 236), outline=OL, width=4)
        d.rectangle([x + 54, 952 + nod, x + 72, 962 + nod], fill=(150, 150, 160), outline=OL, width=2)
    img = cam(img, 1.2 + 0.04 * u, 330, 860)
    clock_pill(img, 170, 640, "08:00", spring(t - T, 13, 7), bg=(220, 140, 30))
    if u > 0.65:
        pill(img, 500, 640, "DISCHARGED", (40, 150, 80), spring(t - T - 0.65 * D(5), 13, 7), 34)
    return img


def s_cane(t, u, T):
    """low angle: Grandad pushes up off the bed edge with his cane; you are stunned"""
    img = hospital(t, night=False).filter(ImageFilter.GaussianBlur(2))
    bed(img, 120, 760, 980)
    rise = ease_out(clamp((u - 0.15) / 0.3))
    talk = u > 0.5 and int(t * 7) % 2 == 0
    if rise < 0.5:
        sp = grandad(pose="sit", mouth="flat")
        paste(img, sp, 16, 330, 1170)
        paste(img, cane(10), 16, 195, 1130)
    else:
        paste(img, grandad_cane(mouth="open" if talk else "smile"), 16, 330, 1220 + int(40 * (1 - rise)))
    paste(img, hero(mouth="open", look=-1), 12, 610, 1240)
    return cam(img, 1.0 + 0.05 * u, 360, 820)


def s_car(t, u, T):
    """side view, parallax: Mum's old red car in the rain; clock races toward 10:00"""
    img = Image.new("RGBA", (FW, FH), (90, 100, 130, 255))
    d = ImageDraw.Draw(img)
    for y in range(760):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, y / 760)) for a, b in zip((70, 80, 110), (160, 168, 186))))
    sp = t * 1.0
    for layer, (y0, col, spd, rr) in enumerate(((560, (110, 124, 140), 40, 140), (640, (60, 100, 70), 120, 90))):
        for k in range(-2, 9):
            x = (k * rr * 1.6 - sp * spd) % (FW + 400) - 200
            d.ellipse([x - rr, y0 - rr * 0.7, x + rr, y0 + rr], fill=col)
    d.rectangle([0, 700, FW, 760], fill=(60, 100, 70))
    d.rectangle([0, 760, FW, FH], fill=(64, 66, 76))                  # road
    for k in range(-1, 8):                                             # lane dashes
        x = (k * 180 - sp * 900) % (FW + 180) - 180
        d.rectangle([x, 1080, x + 100, 1094], fill=(240, 240, 240))
    d.rectangle([0, 760, FW, 790], fill=(150, 154, 166))               # barrier
    for k in range(-1, 12):
        x = (k * 90 - sp * 600) % (FW + 90) - 90
        d.rectangle([x, 730, x + 12, 790], fill=(120, 124, 136), outline=OL, width=2)
    # road sign passes once
    sx = lerp(900, -400, clamp((u - 0.35) / 0.55))
    d.rectangle([sx + 120, 520, sx + 136, 760], fill=(140, 140, 150), outline=OL, width=3)
    d.rounded_rectangle([sx, 400, sx + 260, 540], 12, fill=(30, 110, 70), outline=(250, 250, 250), width=6)
    d.text((sx + 130, 445), "RIVERSIDE", font=font(800, 30), fill=(255, 255, 255), anchor="mm")
    d.text((sx + 130, 495), "ACADEMY  2 MI", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
    # the car (pixel art, scale 8)
    S = 8
    car = Image.new("RGBA", (70, 32), (0, 0, 0, 0))
    cd = ImageDraw.Draw(car)
    cd.rectangle([2, 14, 67, 25], fill=(200, 56, 56))
    cd.polygon([(14, 14), (22, 4), (50, 4), (58, 14)], fill=(200, 56, 56))
    cd.polygon([(17, 14), (23, 6), (35, 6), (35, 14)], fill=(150, 190, 220))       # front window... (driving right)
    cd.polygon([(37, 14), (37, 6), (49, 6), (55, 14)], fill=(150, 190, 220))
    cd.rectangle([2, 19, 67, 20], fill=(160, 40, 40))
    cd.rectangle([64, 15, 67, 17], fill=(250, 230, 140))                           # headlight
    cd.rectangle([2, 15, 4, 17], fill=(250, 60, 60))
    car = outline(car)
    bob = int(math.sin(t * 9) > 0.6)
    cx, cy = 340, 1060 - bob * S
    img.alpha_composite(big(car, S), (int(cx - 35 * S), int(cy - 26 * S)))
    # heads in the windows: Grandad in the front (passenger side, near us), Mum behind him driving, you in the back
    def head(sprite):
        return sprite.crop((0, 4, 24, 20))
    paste(img, head(mum(look=1)), 4, cx + 60 + 26, cy - 15 * S)
    paste(img, head(grandad(look=1, mouth="smile")), 5, cx + 26, cy - 14 * S)
    paste(img, head(hero(look=1, mouth="flat")), 5, cx - 100 + 26 - 40, cy - 14 * S)
    d = ImageDraw.Draw(img)
    for wx in (cx - 35 * S + 14 * S, cx + 35 * S - 16 * S):             # wheels with spinning spokes
        r = 5 * S
        d.ellipse([wx - r, cy - 2 * S - r + 4 * S, wx + r, cy - 2 * S + r + 4 * S], fill=(30, 30, 36), outline=OL, width=4)
        wy = cy + 2 * S
        for k in range(3):
            a = t * 30 + k * 2.1
            d.line([(wx, wy), (wx + math.cos(a) * r * 0.7, wy + math.sin(a) * r * 0.7)], fill=(170, 170, 180), width=6)
    # spray behind the wheels
    dd = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(int(t * 20))
    for _ in range(30):
        x = cx - 35 * S - rng.uniform(0, 160)
        y = cy + rng.uniform(-30, 20)
        dd.ellipse([x, y, x + 10, y + 6], fill=(220, 230, 255, 120))
    rain(img, t, 110, 160)
    m = int(lerp(12, 61, ease_in_out(u)))
    hh, mm = (9, m) if m < 60 else (10, m - 60)
    clock_pill(img, 360, 300, f"{hh:02d}:{mm:02d}", 1.0, bg=(200, 40, 50) if hh == 10 else (40, 60, 140))
    return cam(img, 1.0 + 0.03 * u, 360, 800)


def s_run(t, u, T):
    """tracking shot: you sprint along the fence, gloves on, the trial going on behind"""
    img = academy_bg(520).copy()
    flags(img, t, 520)
    c = Cam(camX=t * 5.0, camH=1.4, hor=520)
    pitch_persp(img, c, None)
    d = ImageDraw.Draw(img)
    for k in range(-2, 14):                                   # near touchline posts / cones streaming past
        x = (k * 120 - t * 900) % (FW + 240) - 120
        d.polygon([(x, 1180), (x + 30, 1180), (x + 15, 1130)], fill=(252, 140, 27), outline=OL)
    for i, (Xo, Z, n) in enumerate(((2, 14, 3), (7, 18, 7), (-4, 16, 5))):
        X = Xo + t * 5.0 + math.sin(t + i) * 0.7
        ground_shadow(img, c, X, Z, 0.3)
        sp = trialist(n, pose="run", phase=t * 2 + i) if n != 7 else academy(7, pose="run", phase=t * 2 + i)
        sprite_at(img, c, sp, X, Z, height_m=1.5)
    bob = abs(math.sin(t * 3 * math.pi)) * 14
    shadow(img, 360, 1135, 220, 34, 100)
    paste(img, hero(pose="run", phase=t * 3, gloves=True, mouth="open"), 13, 360, 1140 - bob)
    speed_lines(img, t, 360, 900, n=8, a=60, r0=280, r1=600)
    clock_pill(img, 360, 300, "10:02", 1.0)
    return cam(img, 1.0 + 0.03 * u, 360, 820)


def pitch_side(blur=3, hor=520):
    img, c = academy_set(hor, 26.0, camH=1.6)
    flags(img, 0, hor)
    goal3d(img, c, 26.0, w=4.4, h=1.8)
    for i, (X, Z, n) in enumerate(((-3, 18, 3), (2, 16, 7), (4, 21, 5))):
        ground_shadow(img, c, X, Z, 0.3)
        sprite_at(img, c, trialist(n) if n != 7 else academy(7), X, Z, height_m=1.5)
    sprite_at(img, c, dixon(pose="ready"), 0, 26, height_m=1.5)
    return img.filter(ImageFilter.GaussianBlur(blur)) if blur else img


def clipboard(img, x, y, lines, k=1.0, tick=None):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + 250, y + 300], 14, fill=(250, 246, 236), outline=OL, width=6)
    d.rectangle([x + 80, y - 16, x + 170, y + 20], fill=(120, 120, 130), outline=OL, width=4)
    for i, (txt, col) in enumerate(lines):
        d.text((x + 125, y + 70 + i * 62), txt, font=font(800, 30), fill=col, anchor="mm")
    if tick is not None and tick > 0:
        tx, ty = x + 200, y + 70 + 62 * 2
        pts = [(tx - 30, ty), (tx - 10, ty + 22), (tx + 30, ty - 26)]
        n = clamp(tick)
        if n < 0.5:
            d.line([pts[0], (lerp(pts[0][0], pts[1][0], n * 2), lerp(pts[0][1], pts[1][1], n * 2))], fill=(40, 160, 70), width=10)
        else:
            d.line([pts[0], pts[1], (lerp(pts[1][0], pts[2][0], (n - .5) * 2), lerp(pts[1][1], pts[2][1], (n - .5) * 2))], fill=(40, 160, 70), width=10)


def s_late(t, u, T):
    """over your shoulder: the coach, clipboard: 'Keepers were at 9:30.'"""
    img = pitch_side(3)
    talk = int(t * 7) % 2 == 0 and u < 0.85
    paste(img, coach(mouth="open" if talk else "flat", look=-1, blink=0.5 < u < 0.53), 20, 330, 1500)
    clipboard(img, 450, 960, [("GK SESSION", OL), ("9:30", (210, 52, 56)), ("DONE", (40, 150, 80))])
    paste(img, hero(view="back", gloves=True), 17, 120, 1560)
    return cam(img, 1.0 + 0.12 * ease_in_out(u), 420, 900)


def s_mason(t, u, T):
    img = pitch_side(5)
    paste(img, mason(mouth="grin" if int(t * 6) % 2 else "smile", look=-1), 26, 360, 1560)
    return cam(img, 1.02 + 0.05 * u, 360, 820)


def s_freeze(t, u, T):
    """Grandad arrives at the fence with Mum; the coach turns, sees him, and freezes"""
    if u < 0.5:
        img, c = academy_set(560, None, camH=1.6)
        flags(img, t, 560)
        k = ease_out(clamp(u / 0.45))
        X = lerp(-1.6, -0.4, k)
        for sp, dx in ((grandad_cane(mouth="smile", blink=int(t * 2) % 7 == 0), 0.0), (mum(look=1), -0.9)):
            ground_shadow(img, c, X + dx, 6.0, 0.35)
            bob = 0.04 * abs(math.sin(t * 4 + dx)) if k < 0.98 else 0
            sprite_at(img, c, sp, X + dx, 6.0, Y=bob, height_m=1.75 if dx == 0 else 1.65)
        paste(img, coach(view="back"), 19, 520, 1540)
        return cam(img, 1.0 + 0.04 * u, 360, 820)
    img = pitch_side(6)
    v = (u - 0.5) / 0.5
    paste(img, coach(mouth="open", look=-1, blink=False), 30, 380, 1640)
    vignette(img, 0.55 + 0.25 * v)
    img = img.convert("RGB")
    img = ImageEnhance.Color(img).enhance(1 - 0.5 * v).convert("RGBA")
    return cam(img, 1.0 + 0.12 * ease_out(v), 360, 760)


def s_go(t, u, T):
    """'Ten minutes. Trial match. Go.' — you run into the goal, the clock starts"""
    img, c = academy_set(560, 12.0, camH=2.2)
    flags(img, t, 560)
    goal3d(img, c, 12.0, w=4.4, h=1.8)
    k = ease_out(clamp(u / 0.7))
    X = lerp(4.5, 0.0, k)
    Z = lerp(9.5, 12.0, k)
    ground_shadow(img, c, X, Z, 0.4)
    sprite_at(img, c, hero(view="back" if k < 0.95 else "front", pose="run" if k < 0.95 else "ready", phase=t * 2.6, gloves=True), X, Z, height_m=1.5)
    for i, (Xo, Z2, n) in enumerate(((-3.5, 8.5, 3), (2.6, 7.5, 5), (-1.2, 9.0, 6))):
        ground_shadow(img, c, Xo, Z2, 0.35)
        sprite_at(img, c, trialist(n, view="back"), Xo, Z2, height_m=1.5)
    ground_shadow(img, c, -6, 4.0, 0.4)
    sprite_at(img, c, coach(look=1), -6, 4.0, height_m=1.75)
    big_k = spring(t - T - 0.05, 12, 6)
    clock_pill(img, 360, 1000, "10:00 LEFT", big_k, bg=(14, 16, 30), size=54)
    if u > 0.75:
        impact_lines(img, *c.p(-6, 4.0, 1.4), T + 0.75 * D(12), t, 10)
    return cam(img, 1.0 + 0.04 * u, 360, 720)


def shot_reverse(t, w, t_hit, shooter):
    """camera low behind the net: the striker shoots, the ball slides through your legs and bulges the net"""
    c = Cam(camX=0.6, camH=1.05, hor=600)
    img = academy_bg(600)
    flags(img, t, 600)
    pitch_persp(img, c, None)
    d = ImageDraw.Draw(img)
    for (X0, Z0, X1, Z1) in ((-30, 4.3, 30, 4.3), (-6, 4.3, -6, 8.3), (6, 4.3, 6, 8.3), (-6, 8.3, 6, 8.3), (-14, 15.3, 14, 15.3)):
        pts = [c.p(lerp(X0, X1, i / 20), lerp(Z0, Z1, i / 20)) for i in range(21)]
        d.line(pts, fill=LINE, width=max(2, int(0.07 * c.k((Z0 + Z1) / 2))))
    kick = 0.18
    ground_shadow(img, c, 1.3, 11.0, 0.4)
    sprite_at(img, c, shooter(pose="kick" if w > kick - 0.08 else "run", phase=clamp((w - kick + 0.08) / 0.1) if w > kick - 0.08 else t * 2.6), 1.3, 11.0, height_m=1.55)
    a = 0.0 if w < kick else clamp((w - kick) / (0.62 - kick))
    path = arc((1.0, 10.7, 0.1), (0.0, 2.6, 0.22), apex=0.12)
    ground_shadow(img, c, 0, 4.6, 0.5)
    ball_first = at(path, a)[1] > 4.6
    if ball_first:
        if a > 0:
            ball_trail(img, c, path, a, 0.1)
        ball_at(img, c, *at(path, a))
    late = w > 0.6
    sprite_at(img, c, hero(view="back", pose="ready" if not late else "stand", gloves=True), 0, 4.6, height_m=1.6)
    if not ball_first and a < 0.97:
        ball_trail(img, c, path, a, 0.1)
        ball_at(img, c, *at(path, min(a, 0.97)), shadow_=False)
    pl, pr = c.p(-2.5, 4.3), c.p(2.5, 4.3)
    tl, tr = c.p(-2.5, 4.3, 2.0), c.p(2.5, 4.3, 2.0)
    for a_, b_ in ((pl, tl), (pr, tr), (tl, tr)):
        d = ImageDraw.Draw(img)
        d.line([a_, b_], fill=OL, width=30); d.line([a_, b_], fill=(250, 250, 252), width=22)
    bul = None
    if a >= 0.97:
        bul = (*c.p(0.0, 2.6, 0.22), clamp((w - 0.62) / 0.06))
    net = Image.new("RGBA", img.size, (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    cell = 46

    def disp(x, y):
        if not bul:
            return x, y
        bx_, by_, k = bul
        dx, dy = x - bx_, y - by_
        r = math.hypot(dx, dy) + 1e-3
        f = k * 70 * math.exp(-(r / 230) ** 2) * (1 + 0.3 * math.sin((w - 0.62) * 40) * math.exp(-(w - 0.62) * 8))
        return x - dx / r * f * 0.2, y - dy / r * f * 0.2 + f * 0.4
    for kk in range(-30, 50):
        p1 = [disp(kk * cell + j * cell, j * cell) for j in range(-2, 32)]
        p2 = [disp(kk * cell - j * cell, j * cell) for j in range(-2, 32)]
        nd.line(p1, fill=(240, 244, 250, 90), width=3)
        nd.line(p2, fill=(240, 244, 250, 90), width=3)
    img.alpha_composite(net)
    if bul:
        draw_ball(img, bul[0], bul[1] + 50, 3.2)
        impact_lines(img, bul[0], bul[1], t_hit, t, 14)
    img = flash(img, 0.45 * clamp(1 - abs(w - 0.63) * 10), (255, 50, 50))
    trial_bar(img, t)
    zoom = 1.0 + 0.12 * ease_in_out(clamp(w / 0.6))
    return cam(img, zoom, 330, 820, *shake(t, t_hit, .35, 14))


def s_legs(t, u, T):
    if u < 0.78:
        return shot_reverse(t, u / 0.78 * 0.95, T + 0.51 * D(13), lambda **kw: academy(7, **kw))
    # 'No sleep.' — your face: heavy eyes
    img = pitch_side(5)
    paste(img, hero(blink=int(t * 3) % 2 == 0, mouth="flat", gloves=True), 24, 360, 1440)
    img = cam(img, 1.0 + 0.15 * ease_out((u - 0.78) / 0.22), 360, 820)
    trial_bar(img, t)
    return img


def s_getup(t, u, T):
    if u < 0.5:
        c = Cam(camX=0, camH=1.6, hor=560)
        img = academy_bg(560)
        flags(img, t, 560)
        pitch_persp(img, c, Zgoal=10.0)
        goal3d(img, c, 10.0)
        v = u / 0.5
        draw_ball(img, *c.p(0.4, 10.9, 0), 1.0)
        if v < 0.3:             # still going down onto his knees after the goal
            f = ease_in_out(v / 0.3)
            ground_shadow(img, c, -0.4, 9.6, 0.5)
            sprite_at(img, c, hero(pose="sit", gloves=True, mouth="sad"), -0.4, 9.6, Y=-0.3 * f, height_m=1.6)
        elif v < 0.5:
            sp_s = 1.6 * c.k(9.9) / 31
            sp = hero(pose="reach", gloves=True, blink=True).resize((int(24 * sp_s), int(39 * sp_s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
            x, y = c.p(-0.6, 9.6)
            img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * sp_s)))
        else:
            k = ease_out((v - 0.5) / 0.3)
            ground_shadow(img, c, -0.4, 9.6, 0.5)
            sprite_at(img, c, hero(pose="sit" if k < 0.5 else "stand", gloves=True, mouth="flat"), -0.4, 9.6, height_m=1.6)
            glow_ring(img, *c.p(-0.4, 9.6, 1.0), 120 * k, 0.4 * k, (255, 240, 180))
        trial_bar(img, t)
        return cam(img, 1 + 0.05 * u, 360, 900)
    # Grandad at the fence, Mum beside him: one slow nod
    img = academy_bg(560).copy()
    flags(img, t, 560)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 564, FW, FH], fill=(78, 134, 72))
    v = (u - 0.5) / 0.5
    nod = 10 if 0.35 < v < 0.6 else 0
    paste(img, mum(look=1, blink=int(t * 2) % 6 == 0), 13, 560, 1240)
    paste(img, grandad_cane(mouth="smile", blink=nod > 0), 13, 250, 1240 + nod)
    d = ImageDraw.Draw(img)
    for y in (960, 1060):                                          # railing in front of them
        d.rectangle([0, y, FW, y + 22], fill=(200, 204, 214), outline=OL, width=4)
    for x in range(30, FW, 140):
        d.rectangle([x, 950, x + 18, FH], fill=(170, 174, 186), outline=OL, width=4)
    return cam(img, 1.02 + 0.05 * v, 360, 900)


def s_1v1(t, u, T):
    c = Cam(camX=0.0, camH=1.9, hor=520)
    img = academy_bg(520)
    flags(img, t, 520)
    pitch_near(img, c, 0.0)
    Z = lerp(13, 4.0, ease_in_out(clamp(u / 0.6)))
    ground_shadow(img, c, 0.2, Z, 0.4)
    sprite_at(img, c, academy(7, pose="run" if u < 0.6 else "kick", phase=t * 2.4 if u < 0.6 else 1.0), 0.2, Z, height_m=1.55)
    for X, Z2, n in ((-3.5, Z + 3, 3), (3.2, Z + 4, 5)):
        ground_shadow(img, c, X, Z2, 0.35)
        sprite_at(img, c, trialist(n, pose="run", phase=t * 2.4), X, Z2, height_m=1.55)
    hit_u = 0.72
    if u < 0.6:
        ball_at(img, c, 0.4, Z - 0.6, 0.11)
    elif u < hit_u:                       # shot toward you (drawn before you: it is still in front of you)
        a = (u - 0.6) / (hit_u - 0.6)
        ball_at(img, c, lerp(0.4, 0.05, a), lerp(Z - 0.6, 1.75, a), lerp(0.1, 0.8, a))
    pose = "spread" if u > 0.5 else "ready"
    paste(img, hero(view="back", pose=pose, gloves=True), 13, 330, 1430)
    if u >= hit_u:                        # it smacks into your chest and rebounds out wide
        b = clamp((u - hit_u) / (1 - hit_u))
        bx = lerp(380, 690, ease_out(b)); by = lerp(1150, 760, ease_out(b)) - 160 * math.sin(b * math.pi)
        draw_ball(img, bx, by, 3.0 * (1 - 0.55 * b))
        th = T + hit_u * D(15)
        impact_lines(img, 380, 1120, th, t, 12)
        glow_ring(img, 380, 1120, 90 + 200 * b, 0.8 * (1 - b), (255, 255, 200))
        img = flash(img, 0.4 * clamp(1 - (t - th) * 8))
    trial_bar(img, t)
    return cam(img, 1 + 0.04 * u, 360, 800, *shake(t, T + hit_u * D(15), .3, 12))


TC = arc((0.3, 2.6, 0.12), (1.95, 14.0, 1.7), apex=0.9, curve=0.7)    # Mason's curler to your top corner


def s_lastkick(t, u, T):
    if u < 0.4:
        v = u / 0.4
        c = Cam(camX=0.4, camH=2.6, hor=500)
        img = academy_bg(500)
        flags(img, t, 500)
        pitch_persp(img, c, Zgoal=14.0)
        goal3d(img, c, 14.0)
        kick = 0.45
        a = clamp((v - kick) / 0.55) * 0.4
        ground_shadow(img, c, 0, 14, 0.45)
        sprite_at(img, c, hero(pose="ready", gloves=True), 0, 14, height_m=1.6)
        if a > 0:
            ball_trail(img, c, TC, a, 0.15)
        ball_at(img, c, *at(TC, a))
        paste(img, mason(view="back", pose="kick" if v > kick - 0.12 else "run", phase=clamp((v - kick + 0.12) / 0.2) if v > kick - 0.12 else t * 2.4), 11, 240, 1330)
        trial_bar(img, t)
        return cam(img, 1.03 + 0.04 * v, 380, 760)
    v = (u - 0.4) / 0.6
    c = Cam(camX=1.6, camH=1.6, hor=560)
    img = academy_bg(560)
    flags(img, t, 560)
    pitch_persp(img, c, Zgoal=6.0, box=False)
    goal3d(img, c, 6.0)
    sc = 1.6 * c.k(6.0) / 31
    sp = hero(pose="reach", gloves=True, mouth="open").resize((int(24 * sc), int(39 * sc)), Image.NEAREST).rotate(-55, expand=True, resample=Image.NEAREST)
    hit = 0.25
    fly = clamp(v / hit)
    kx, ky = c.p(lerp(0.9, 1.35, fly), 6.0, lerp(1.05, 1.3, math.sin(fly * math.pi / 2)))
    if v > 0.32:   # gravity takes him back down onto the grass, lying on his side
        f = clamp((v - 0.32) / 0.2)
        sp = hero(pose="reach", gloves=True, mouth="open" if f < 1 else "grin").resize((int(24 * sc), int(39 * sc)), Image.NEAREST).rotate(lerp(-55, -90, f), expand=True, resample=Image.NEAREST)
        kx, ky = c.p(1.45, 6.0, lerp(1.3, 0.28, f * f))
        if 0.5 < v < 0.62:
            impact_lines(img, kx, c.p(1.45, 6.0)[1], T + 0.4 * D(16) + 0.52 * 0.6 * D(16), t, 8)
    ground_shadow(img, c, 1.3, 6.0, 0.8, 70)
    img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
    if v < hit:
        a = v / hit
        bx, by = c.p(lerp(1.5, 2.25, a), lerp(3.0, 6.0, a), lerp(1.75, 1.9, a))
    else:
        b = clamp((v - hit) / 0.6)
        Yb = 2.05 + 0.6 * math.sin(b * math.pi) - 2.05 * b * b if b < 0.82 else 0.25 * abs(math.sin((b - 0.82) / 0.18 * math.pi))
        bx, by = c.p(2.25 + 1.7 * b, 6.0 + 2.2 * b, max(0.0, Yb))
    draw_ball(img, bx, by, 1.6)
    th = T + (0.4 + 0.6 * hit) * D(16)
    if v >= hit:
        impact_lines(img, *c.p(2.25, 6.0, 2.0), th, t, 12)
        glow_ring(img, *c.p(2.25, 6.0, 2.0), 60 + 160 * clamp((v - hit) * 3), 0.9 * (1 - clamp((v - hit) * 2)), (255, 255, 210))
    slowmo_bars(img, 1 - ease_out((v - hit) * 3) if v > hit else 1)
    img = flash(img, 0.45 * clamp(1 - abs(v - hit) * 14))
    trial_bar(img, t)
    return cam(img, 1.05, 420, 720, *shake(t, th, .35, 14))


def s_in(t, u, T):
    if u < 0.5:
        img = pitch_side(4)
        talk = int(t * 7) % 2 == 0 and u > 0.25
        paste(img, coach(mouth="open" if talk else "smile", look=-1), 20, 300, 1500)
        clipboard(img, 440, 880, [("TRIAL", OL), ("GK: #0", OL), ("IN", (40, 150, 80))], tick=(u - 0.2) / 0.2)
        return cam(img, 1.0 + 0.05 * u, 360, 820)
    v = (u - 0.5) / 0.5
    img, c = academy_set(560, None, camH=1.4)
    flags(img, t, 560)
    ground_shadow(img, c, 2.6, 12.0, 0.3)
    sprite_at(img, c, grandad_cane(mouth="smile"), 2.6, 12.0, height_m=1.7)
    sprite_at(img, c, mum(mouth="smile"), 3.6, 12.0, height_m=1.6)
    hop = abs(math.sin(v * math.pi * 2)) * 30
    shadow(img, 330, 1300, 200, 34, 100)
    paste(img, hero(pose="celebrate", gloves=True, mouth="grin"), 14, 330, 1300 - hop)
    glow_ring(img, 330, 1000, 160 + 40 * v, 0.4 * (1 - v), (255, 240, 180))
    return cam(img, 1.0 + 0.04 * v, 360, 860)


def choice_bg():
    img = Image.new("RGBA", (FW, FH), (20, 26, 70, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, FH, 60):
        for x in range(0, FW, 60):
            if (x // 60 + y // 60) % 2:
                d.rectangle([x, y, x + 60, y + 60], fill=(24, 32, 82))
    return img


def house_icon(img, x, y, s=1.0):
    d = ImageDraw.Draw(img)
    d.rectangle([x - 60 * s, y - 50 * s, x + 60 * s, y + 40 * s], fill=(170, 74, 60), outline=OL, width=5)
    for r in range(4):
        d.line([(x - 60 * s, y - 30 * s + r * 20 * s), (x + 60 * s, y - 30 * s + r * 20 * s)], fill=(140, 58, 48), width=2)
    d.polygon([(x - 76 * s, y - 50 * s), (x, y - 106 * s), (x + 76 * s, y - 50 * s)], fill=(70, 60, 70), outline=OL)
    d.rectangle([x + 26 * s, y - 116 * s, x + 42 * s, y - 80 * s], fill=(110, 70, 60), outline=OL, width=3)
    d.rectangle([x - 14 * s, y - 6 * s, x + 14 * s, y + 40 * s], fill=(40, 90, 60), outline=OL, width=3)
    for wx in (-42, 26):
        d.rectangle([x + wx * s, y - 34 * s, x + (wx + 18) * s, y - 14 * s], fill=(250, 220, 120), outline=OL, width=3)


def academy_icon(img, x, y, s=1.0):
    d = ImageDraw.Draw(img)
    d.rectangle([x - 80 * s, y - 70 * s, x + 80 * s, y + 40 * s], fill=(232, 228, 222), outline=OL, width=5)
    d.rectangle([x - 80 * s, y - 70 * s, x + 80 * s, y - 54 * s], fill=RS, outline=OL, width=3)
    for r in range(2):
        for k in range(4):
            xx = x - 66 * s + k * 36 * s
            yy = y - 44 * s + r * 36 * s
            d.rectangle([xx, yy, xx + 24 * s, yy + 24 * s], fill=(120, 170, 220), outline=OL, width=2)
    d.polygon([(x - 14 * s, y - 100 * s), (x + 14 * s, y - 100 * s), (x + 14 * s, y - 86 * s), (x, y - 74 * s), (x - 14 * s, y - 86 * s)], fill=C_Y, outline=OL)


def s_map(t, u, T):
    """twist: the map — home to Riverside, 2 hours; move in on Monday"""
    img = choice_bg()
    d = ImageDraw.Draw(img)
    k = spring(t - T, 13, 7)
    d.rounded_rectangle([50, 400 + 600 * (1 - min(1, k)), 670, 1060 + 600 * (1 - min(1, k))], 30, fill=(214, 226, 200), outline=OL, width=7)
    if k > 0.6:
        rng = random.Random(3)
        for _ in range(7):                                      # fields + a river on the paper map
            x, y = rng.uniform(80, 560), rng.uniform(440, 960)
            d.rounded_rectangle([x, y, x + rng.uniform(60, 120), y + rng.uniform(40, 90)], 14, fill=(196, 214, 180))
        d.line([(60, 600), (200, 680), (300, 640), (460, 760), (660, 720)], fill=(130, 180, 230), width=18)
        a = ease_in_out(clamp((u - 0.15) / 0.45))
        p0, p1 = (180, 930), (540, 540)
        mid = (220, 700)
        pts = [((1 - s_) ** 2 * p0[0] + 2 * (1 - s_) * s_ * mid[0] + s_ * s_ * p1[0],
                (1 - s_) ** 2 * p0[1] + 2 * (1 - s_) * s_ * mid[1] + s_ * s_ * p1[1]) for s_ in np.linspace(0, a, 40)]
        for j in range(0, len(pts) - 1, 2):
            d.line([pts[j], pts[j + 1]], fill=OL, width=16); d.line([pts[j], pts[j + 1]], fill=C_R, width=9)
        house_icon(img, *p0, 0.8)
        academy_icon(img, p1[0], p1[1] + 20, 0.8)
        d = ImageDraw.Draw(img)
        d.text((p0[0], p0[1] + 70), "HOME", font=font(800, 30), fill=OL, anchor="mm")
        d.text((p1[0], p1[1] + 90), "RIVERSIDE", font=font(800, 30), fill=OL, anchor="mm")
        if a > 0.95:
            pill(img, 430, 790, "2 HRS", (200, 40, 50), spring(t - T - 0.6 * D(18), 13, 7), 44)
        if u > 0.55:
            pill(img, 360, 340, "MOVE IN: MONDAY", (14, 16, 30), spring(t - T - 0.55 * D(18), 13, 7), 34)
    return cam(img, 1.0 + 0.03 * u, 360, 760)


def s_mum(t, u, T):
    """Mum in the car park with Grandad's pill box; her night shifts"""
    img, c = academy_set(560, None, camH=1.6)
    flags(img, t, 560)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 760, FW, FH], fill=(84, 86, 96))                  # car park tarmac
    for x in range(-40, FW, 160):
        d.line([(x, 760), (x - 60, FH)], fill=(230, 230, 230), width=6)
    img = img.filter(ImageFilter.GaussianBlur(4))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([420, 800, 760, 1000], 40, fill=(200, 56, 56), outline=OL, width=6)   # Mum's car, blurred behind
    d.rectangle([470, 820, 700, 880], fill=(150, 190, 220), outline=OL, width=4)
    MB = 1480
    paste(img, mum(pose="phone", mouth="sad", blink=int(t * 2) % 7 == 0), 22, 330, MB)
    # the pill organiser in her hands (covers the phone)
    d = ImageDraw.Draw(img)
    bx, by = 160, MB - 420
    d.rounded_rectangle([bx, by, bx + 360, by + 110], 14, fill=(240, 240, 246), outline=OL, width=6)
    for k_, lab in enumerate("MTWTFSS"):
        x = bx + 12 + k_ * 49
        d.rectangle([x, by + 12, x + 42, by + 98], fill=(250, 250, 255), outline=(150, 156, 172), width=3)
        d.text((x + 21, by + 32), lab, font=font(800, 22), fill=OL, anchor="mm")
        d.ellipse([x + 10, by + 54, x + 32, by + 76], fill=[(240, 80, 80), (250, 206, 40), (92, 160, 252)][k_ % 3], outline=OL, width=2)
    for hx_ in (bx - 18, bx + 342):                                  # her hands hold both ends
        d.rounded_rectangle([hx_, by + 20, hx_ + 36, by + 90], 10, fill=SKIN["light"][0], outline=OL, width=5)
    img = cam(img, 1.0 + 0.1 * ease_in_out(u), 360, 900)
    if u > 0.12:
        pill(img, 360, 296, "NIGHT SHIFT · 8PM-8AM", (40, 60, 140), spring(t - T - 0.12 * D(19), 13, 7), 30)
    return img


def s_go_hand(t, u, T):
    wt = word_times(20)[3][1]
    cut = clamp((wt + 0.75 - T) / D(20), 0.4, 0.6)
    if u < cut:
        img, c = academy_set(560, None, camH=1.6)
        flags(img, t, 560)
        img = img.filter(ImageFilter.GaussianBlur(4))
        talk = wt - 0.05 < t < wt + 0.45
        paste(img, grandad_cane(mouth="open" if talk else "smile", blink=0.38 < u < 0.41), 22, 380, 1420)
        return cam(img, 1.0 + 0.05 * u, 360, 820)
    # close-up: his hand on the cane handle trembles
    v = (u - cut) / (1 - cut)
    S = 10
    w, h = FW // S, FH // S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tr = 1 if math.sin(t * 22) > 0.2 else 0
    CN, CND = (130, 80, 38), (100, 60, 28)
    d.rectangle([40, 66, 45, 128], fill=CN); d.rectangle([44, 66, 45, 128], fill=CND)      # cane shaft
    d.rectangle([22, 60, 45, 66], fill=CN)                                                # crook handle
    d.rectangle([22, 60, 27, 74], fill=CN); d.rectangle([22, 72, 27, 74], fill=CND)
    old, oldd = SKIN["old"]
    hx = tr
    d.polygon([(44 + hx, 46), (62, 26), (76, 34), (76, 48), (54 + hx, 58)], fill=(150, 98, 58))   # cardigan sleeve
    d.rectangle([44 + hx, 44, 52 + hx, 58], fill=(120, 76, 44))                           # cuff
    d.rectangle([24 + hx, 46, 48 + hx, 61], fill=old)                                     # back of the hand on the handle
    d.rectangle([24 + hx, 58, 48 + hx, 61], fill=oldd)
    for f in range(4):                                                                     # fingers curl round the handle
        fx = 25 + hx + f * 6
        d.rectangle([fx, 61, fx + 4, 69], fill=old)
        d.rectangle([fx + 4, 61, fx + 4, 69], fill=oldd)
    for j in range(3):
        d.line([(28 + hx, 49 + j * 3), (44 + hx, 49 + j * 3)], fill=oldd)
    d.point((33 + hx, 52), fill=(196, 150, 116)); d.point((40 + hx, 55), fill=(196, 150, 116))
    im = outline(im)
    img = academy_set(560, None, camH=1.6)[0].filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(im.resize((w * S, h * S), Image.NEAREST).crop((0, 0, FW, FH)))
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(3):                                                  # small tremble marks
        a = int(160 * (0.5 + 0.5 * math.sin(t * 10 + k)))
        d.arc([120 - k * 30, 420 - k * 30, 520 + k * 30, 760 + k * 30], 200, 240, fill=(255, 255, 255, a), width=6)
    vignette(img, 0.45)
    return cam(img, 1.0 + 0.06 * v, 360, 640)


CARDS = [(190, "ACADEMY", "LEAVE ON MONDAY", C_Y), (530, "HOME", "STAY WITH GRANDAD", C_B)]


def choice_cards(img, t, T0):
    d = ImageDraw.Draw(img)
    for i, (x, lab, sub, c) in enumerate(CARDS):
        k = spring(t - T0 - i * 0.15, 13, 7)
        if k < 0.05:
            continue
        hl = 0.5 + 0.5 * math.sin(t * 3.2 + i * math.pi)
        w, h = 310 * k * (1 + 0.04 * hl), 440 * k * (1 + 0.04 * hl)
        y = 680 - 10 * hl
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 24, fill=(16, 18, 36), outline=c, width=7)
        if k > 0.6:
            if lab == "ACADEMY":
                academy_icon(img, x - 20, y - 30, 0.75)
                paste(img, hero(gloves=True, look=-1), 4, x + 90, y + 40)
                d.rectangle([x + 100, y - 4, x + 128, y + 30], fill=(40, 60, 140), outline=OL, width=3)   # kit bag
            else:
                house_icon(img, x - 40, y + 10, 0.65)
                paste(img, grandad_cane(), 4, x + 50, y + 44)
                paste(img, hero(look=-1), 4, x + 105, y + 40)
            d.text((x, y + 120), lab, font=font(800, 46), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            d.text((x, y + 170), sub, font=font(700, 20), fill=(220, 224, 240), anchor="mm")


def typing_box(img, t, T0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 960, 630, 1030], 18, fill=(16, 18, 36), outline=(255, 255, 255), width=3)
    words = ["ACADEMY", "HOME"]
    k = (t - T0) / 1.1
    wi = min(1, int(k))
    w = words[wi]
    n = int(len(w) * clamp((k - wi) * 2)) if k < 2 else len(w)
    d.text((120, 995), w[:n] + ("|" if int(t * 4) % 2 else ""), font=font(800, 30), fill=(255, 255, 255), anchor="lm")


def s_choice(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 0.2)
    typing_box(img, t, T + 0.3)
    pill(img, 360, 340, "VOTE BEFORE FRIDAY", (200, 50, 60), spring(t - T - 0.3, 13, 7), 28)
    return cam(img, 1.0 + 0.02 * u, 360, 760)


def s_end(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 10)
    img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (10, 12, 30)), 0.5 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 560], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 150), "EP. 5", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
    tap = T + 0.8
    after = t > tap
    label = ("SUBSCRIBED" if after else "SUBSCRIBE") if PLATFORM == "youtube" else ("FOLLOWING" if after else "+ FOLLOW")
    pul = 1 + (0.05 * math.sin(t * 9) if not after else 0)
    bw, bh = 330 * pul, 96 * pul
    bx, by = 440, py + 280
    d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], 22, fill=(60, 64, 90) if after else (234, 46, 72), outline=OL, width=5)
    d.text((bx, by), label, font=font(800, 36 if after else 40), fill=(255, 255, 255), anchor="mm")
    if after and t < tap + 0.5:
        glow_ring(img, bx, by, 60 + 300 * (t - tap), 0.8 * (1 - (t - tap) / 0.5), C_Y)
    if t < tap + 0.4:   # Grandad's orange glove taps it
        gx = lerp(760, bx + 100, ease_in_out((t - T) / 0.8)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, cc in ((230, "ACADEMY", C_Y), (490, "HOME", C_B)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 110, py + 400 - hop, x + 110, py + 470 - hop], 18, fill=(30, 36, 76), outline=cc, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 32), fill=cc, anchor="mm")
    d.text((360, py + 520), "VOTE IN THE COMMENTS", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    return img


def s_run_hook2(t, u, T):
    return s_run(t, u, T)


SCENES = [s_hook, s_rewind, s_chair, s_hands, s_talk, s_doctor, s_cane, s_car, s_run, s_late, s_mason, s_freeze, s_go,
          s_legs, s_getup, s_1v1, s_lastkick, s_in, s_map, s_mum, s_go_hand, s_choice, s_end]
assert len(SCENES) == len(LINES)


def grade(img):
    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.94)
    return Image.blend(img, Image.new("RGB", img.size, (60, 50, 70)), 0.06)


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s:
            i = k
    return i


def frame(t):
    i = line_at(t)
    T = STARTS[i]
    u = clamp((t - T) / max(0.1, D(i)))
    img = SCENES[i](t, u, T).convert("RGB")
    img = grade(img).convert("RGBA")
    if i > 0 and t - T < 0.07:
        img = flash(img, 0.3)
    overlay(img, t, i)
    return img.convert("RGB")


if __name__ == "__main__":
    ts = [float(x) for x in sys.argv[1].split(",")]
    ims = [frame(x).resize((240, 427)) for x in ts]
    out = Image.new("RGB", (240 * min(6, len(ims)), 427 * ((len(ims) + 5) // 6)))
    for k, im in enumerate(ims):
        out.paste(im, (240 * (k % 6), 427 * (k // 6)))
    out.save(sys.argv[2])
    print("TOTAL", round(TOTAL, 2), [round(s, 1) for s in STARTS])
