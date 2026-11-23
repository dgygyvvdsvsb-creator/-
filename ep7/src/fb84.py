"""EP6 (new) — the coach's flashback: May 1984, Kingston v Newcastle. Draft, no voice."""
import os, sys, json
from cast84 import *
from persp import _xzy, _c
from PIL import ImageEnhance

PLATFORM = os.environ.get("PLATFORM", "tiktok")
EP = 7
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
FOLLOW = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"
LINES = [
    [("1984.", Y), ("ONE", W), ("JUMP.", R_), ("ONE", W), ("CAREER", W), ("OVER.", R_)],
    [("YOU", W), ("ASKED", W), ("FOR", W), ("THE", W), ("SHIRT.", Y), ("\"SHOW", W), ("ME.\"", Y)],
    [("YOU", W), ("DIVE.", W), ("ORANGE", O), ("GLOVES.", O), ("RED", R_), ("STRING.", R_)],
    [("THE", W), ("COACH", W), ("GOES", W), ("PALE.", B)],
    [("MAY", Y), ("1984.", Y), ("KINGSTON", Y), ("AGAINST", W), ("NEWCASTLE.", B)],
    [("TEN", W), ("THOUSAND", W), ("STANDING.", W), ("RAIN.", B), ("MUD.", W)],
    [("IN", W), ("KINGSTON'S", Y), ("GOAL:", W), ("GRANDAD.", G), ("TWENTY-TWO.", W)],
    [("SAME", W), ("ORANGE", O), ("GLOVES.", O), ("SAME", W), ("RED", R_), ("STRING.", R_)],
    [("NEWCASTLE'S", B), ("NUMBER", W), ("NINE:", W), ("THE", W), ("COACH.", Y), ("TWENTY.", W)],
    [("MINUTE", W), ("TWELVE.", W), ("VOLLEY.", W), ("GRANDAD", G), ("FLIES.", Y), ("SAVED!", G)],
    [("REBOUND...", W), ("SAVED", G), ("AGAIN!", G)],
    [("KINGSTON", Y), ("SCORE.", Y), ("ONE-NIL.", Y)],
    [("NUMBER", W), ("NINE", B), ("CAN'T", R_), ("BEAT", W), ("HIM.", W)],
    [("EIGHTY-NINTH", R_), ("MINUTE.", R_), ("LAST", W), ("CORNER.", W)],
    [("THE", W), ("BALL", W), ("HANGS", Y), ("IN", W), ("THE", W), ("LIGHTS.", Y)],
    [("GRANDAD", G), ("JUMPS.", W), ("NUMBER", W), ("NINE", B), ("JUMPS...", W)],
    [("KNEE", R_), ("FIRST.", R_)],
    [("SILENCE.", W)],
    [("GRANDAD", G), ("DOESN'T", R_), ("GET", W), ("UP.", R_), ("GLOVES", O), ("STILL", W), ("ON.", W)],
    [("THE", W), ("BALL", W), ("ROLLS", W), ("IN.", W), ("ONE-ONE.", R_)],
    [("A", W), ("STRETCHER.", W), ("TEN", W), ("THOUSAND", W), ("PEOPLE...", W), ("QUIET.", B)],
    [("NUMBER", W), ("NINE", B), ("LOOKS", W), ("DOWN.", W), ("NO", W), ("ONE", W), ("SEES", W), ("HIS", W), ("FACE.", R_)],
    [("TODAY.", W), ("THE", W), ("COACH'S", W), ("WHISTLE", Y), ("FALLS.", R_)],
    [("ACCIDENT...", B), ("OR", W), ("ON", R_), ("PURPOSE?", R_)],
    [("VOTE", W), ("BELOW.", G), (FOLLOW, R_), ("FOR", W), ("PART 8.", Y)],
]
PAST = set(range(4, 22)) | {0}          # scenes shown on old VHS tape
UYF = 0                                  # extra top offset for UI under the captions (set by ep7 for TikTok)
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"vo/lines_{PLATFORM}.json")
if os.path.exists(_vf):
    VOICE = [tuple(x) for x in json.load(open(_vf))]
else:
    VOICE, t0 = [], 0.05
    for i, ws in enumerate(LINES):
        d_ = max(1.25, 0.34 * len(ws) + 0.3)
        if i in (16, 17):
            d_ = 1.4
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
    for j, w in enumerate(ws):
        cur.append(w)
        nxt_ends = j + 1 < len(ws) and ws[j + 1][0][-1] in ".?!" and len(cur) == 3 and not w[0][-1] in ".,?!\":"
        if w[0][-1] in ".,?!\":" or w[0].endswith("...") or (len(cur) == 3 and not nxt_ends) or len(cur) == 4:
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
    if i == 0 and t < 0.4:
        cur = [(w, -1, c) for w, _, c in cur]
    caption(img, cur, t, size=56, wrap=620)


def vignette(img, a=0.5):
    key = ("vig", a)
    if key not in _c:
        m = Image.new("L", (FW, FH), 0)
        ImageDraw.Draw(m).ellipse([-200, -100, FW + 200, FH + 100], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(160)).point(lambda v: int((255 - v) * a))
        lay = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
        lay.putalpha(m)
        _c[key] = lay
    img.alpha_composite(_c[key])


def slowmo_bars(img, k):
    if k <= 0:
        return
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, FW, int(40 * k)], fill=(0, 0, 0))
    d.rectangle([0, FH - int(40 * k), FW, FH], fill=(0, 0, 0))


# ------------------------------------------------------------------ 1984 score bug (top-left, retro)
def score84(t):
    k = 1 if t >= STARTS[11] + 0.45 * D(11) else 0
    n = 1 if t >= STARTS[19] + 0.6 * D(19) else 0
    if t < STARTS[11]:
        m = 12
    elif t < STARTS[13]:
        m = int(lerp(31, 76, (t - STARTS[11]) / (STARTS[13] - STARTS[11])))
    else:
        m = 89
    return k, n, m


def match_clock(t):
    keys = [(STARTS[9], 12 * 60), (STARTS[11], 31 * 60), (STARTS[12], 64 * 60), (STARTS[13], 88 * 60 + 40), (STARTS[22], 89 * 60 + 58)]
    if t <= keys[0][0]:
        return keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= t <= b:
            return int(lerp(va, vb, (t - a) / (b - a)))
    return keys[-1][1]


def bug84(img, t):
    k, n, _ = score84(t)
    m = match_clock(t) // 60 + 1
    d = ImageDraw.Draw(img)
    x, y = 40, 248
    d.rectangle([x, y, x + 330, y + 46], fill=(10, 10, 16), outline=(230, 230, 230), width=3)
    d.rectangle([x + 6, y + 8, x + 24, y + 38], fill=KIN); d.rectangle([x + 156, y + 8, x + 174, y + 38], fill=NEW)
    f = font(800, 24)
    d.text((x + 34, y + 23), f"KIN {k}", font=f, fill=(255, 255, 255), anchor="lm")
    d.text((x + 136, y + 23), "-", font=f, fill=(255, 255, 255), anchor="mm")
    d.text((x + 184, y + 23), f"{n} NEW", font=f, fill=(255, 255, 255), anchor="lm")
    d.rectangle([x + 268, y + 6, x + 324, y + 40], fill=(200, 40, 40))
    d.text((x + 296, y + 23), f"{m}'", font=font(800, 22), fill=(255, 255, 255), anchor="mm")


# ------------------------------------------------------------------ 1984 sets
def set84(hor=520, Zg=14.0, camX=0.0, camH=1.8, goal=True):
    c = Cam(camX=camX, camH=camH, hor=hor)
    img = old_stadium(hor)
    mud_pitch(img, c, Zg)
    if goal and Zg:
        goal3d(img, c, Zg)
    return img, c


def keeper84(img, cam, X, Z, side, phase, height_m=1.75):
    """keeper_world with young Grandad: set, explosive push, catch at full stretch, fall, short rest, up again"""
    k = cam.k(Z)
    s = height_m * k / 31.0
    if phase < 0.12:
        dip = math.sin(phase / 0.12 * math.pi) * 0.08
        ground_shadow(img, cam, X, Z, 0.45)
        sprite_at(img, cam, young_grandad(pose="ready"), X, Z, Y=-dip, height_m=height_m)
        return cam.p(X + side * 0.7, Z, 1.1)
    if phase < 0.38:
        a = ease_out((phase - 0.12) / 0.26)
        Xc = X + side * 1.5 * a
        Yc = 0.35 + 0.55 * math.sin(a * math.pi * 0.5)
        rot = 90 * ease_out(min(1.0, a * 1.6))
    elif phase < 0.55:
        f = (phase - 0.38) / 0.17
        Xc = X + side * (1.5 + 0.25 * f)
        Yc = 0.9 * (1 - f) ** 2 + 0.08 * abs(math.sin(f * math.pi * 2)) * (1 - f)
        rot = 90
    elif phase < 0.72:
        Xc, Yc, rot = X + side * 1.75, 0.0, 90
    else:
        Xu = X + side * 1.75
        f = ease_out((phase - 0.72) / 0.14)
        ground_shadow(img, cam, Xu, Z, 0.45)
        sprite_at(img, cam, young_grandad(pose="sit" if f < 1 else "catch", mouth="smile"), Xu, Z,
                  Y=-0.25 * (1 - f), height_m=height_m * (0.8 + 0.2 * f))
        return cam.p(Xu, Z, 1.0 if f >= 1 else 0.6)
    sp = young_grandad(pose="reach", mouth="open" if phase < 0.55 else "smile")
    sp = sp.resize((max(1, int(24 * s)), max(1, int(39 * s))), Image.NEAREST)
    sp = sp.rotate(-rot if side > 0 else rot, expand=True, resample=Image.NEAREST)
    ground_shadow(img, cam, Xc, Z, 0.55 + 0.35 * clamp(1 - Yc), 80)
    gx, gy = cam.p(Xc, Z, Yc)
    yb = gy + 9 * s * 0.6
    img.alpha_composite(sp, (int(gx - sp.width / 2), int(yb - sp.height)))
    if 0.38 <= phase < 0.6 and Yc < 0.12:
        impact_lines(img, gx, cam.p(Xc, Z)[1], 0.0, (phase - 0.5) * 3, 8)
        mud_splash(img, gx, cam.p(Xc, Z)[1], (phase - 0.45) / 0.15, s * 6)
    return gx + side * (sp.width / 2 - 6 * s), yb - sp.height / 2


def mud_splash(img, x, y, k, size=40):
    if not 0 < k < 1:
        return
    d = ImageDraw.Draw(img)
    rng = random.Random(int(x))
    for i in range(10):
        ang = math.pi + rng.uniform(0.2, math.pi - 0.2)
        v = rng.uniform(0.6, 1.2) * size * 2
        px = x + math.cos(ang) * v * k
        py = y + math.sin(ang) * v * k + 120 * k * k
        r = rng.uniform(3, 7)
        d.ellipse([px - r, py - r, px + r, py + r], fill=MUD_D)


def side_set(t, hor=700):
    """side-on frame for the collision: terrace behind, the near post + net on the left"""
    img = old_stadium(hor).copy()
    c = Cam(camH=1.4, hor=hor)
    pitch_persp(img, c, None, warm=False)
    for k in range(6):
        x = 60 + k * 120
        tint(img, [x - 90, 1020, x + 110, 1120], MUD + (170,), True)
    d = ImageDraw.Draw(img)
    # goal frame on the left edge: post + crossbar + net
    d.line([(70, 1060), (70, 610)], fill=OL, width=26); d.line([(70, 1060), (70, 610)], fill=(250, 250, 252), width=18)
    d.line([(-10, 610), (70, 610)], fill=OL, width=26); d.line([(-10, 610), (70, 610)], fill=(250, 250, 252), width=18)
    for y in range(620, 1060, 24):
        d.line([(0, y), (60, y + 10)], fill=(200, 204, 210), width=2)
    return img


def collision(img, j, impact=0.0, t=0.0):
    """j 0..1: both rise; impact 0..1: contact (knee into Grandad's ribs). Grandad left, #9 right."""
    ground = 1060
    gx = lerp(220, 285, j) - 25 * impact
    cx = lerp(560, 470, j) + 10 * impact
    gy = ground - 250 * math.sin(j * math.pi / 2) + 60 * impact
    cy = ground - 230 * math.sin(j * math.pi / 2)
    shadow(img, gx, ground + 10, 160 * (1 - 0.4 * j), 30, 90)
    shadow(img, cx, ground + 10, 160 * (1 - 0.4 * j), 30, 90)
    g = young_grandad(pose="reach", mouth="open" if impact > 0 else "flat", blink=impact > 0.3)
    paste(img, g, 11, gx, gy, rot=-12 + 30 * impact)
    co = young_coach(pose="kickL", phase=lerp(0.3, 0.92, j), mouth="open" if impact > 0 else "flat")
    paste(img, co, 11, cx, cy, rot=10)
    return (gx + cx) / 2, (gy + cy) / 2 - 230


def ball_side(img, x, y, size=2.6):
    draw_ball(img, x, y, size)


# ------------------------------------------------------------------ scenes
def s_hook(t, u, T):
    img = side_set(t)
    k = clamp(t / D(0))
    mx, my = collision(img, 1.0, 0.25 + 0.1 * k, t)
    ball_side(img, mx + 30 - 60 * k, my - 120 - 30 * k, 2.6)
    impact_lines(img, mx, my + 140, -0.05, 0.10 + 0.08 * k, 14)
    glow_ring(img, mx, my + 140, 120 + 30 * k, 0.6, (255, 250, 220))
    rain84(img, t, 120)
    return cam(img, 1.08 + 0.05 * k, mx, my + 200)


def present_pitch(t, Zg=8.5):
    c = Cam(camH=2.2, hor=470)
    img = backdrop(470, stadium=False)
    pitch_persp(img, c, Zgoal=Zg)
    goal3d(img, c, Zg)
    return img, c


def s_showme(t, u, T):
    img, c = present_pitch(t)
    side = -1
    phase = min(0.66, clamp((u - 0.25) / 0.75))
    gx, gy = keeper_world(img, c, 0, 8.5, side, phase)
    shot = arc((-0.05, 2.4, 0.0), (side * 1.5, 8.5, 0.95), apex=0.45)
    if phase < 0.33:
        a = phase / 0.33
        if a > 0:
            ball_trail(img, c, shot, a, 0.15)
        ball_at(img, c, *at(shot, a))
    else:
        draw_ball(img, gx, gy + 14, 0.16 * c.k(8.5) / 6.5)
    ground_shadow(img, c, 3.4, 7.0, 0.4)
    sprite_at(img, c, coach(look=-1, mouth="open" if u < 0.2 else "flat"), 3.4, 7.0, height_m=1.75)
    paste(img, dixon(view="back", pose="kick" if 0.15 < u < 0.4 else "stand", phase=clamp((u - 0.15) / 0.15), gloves=False), 11, 300, 1330)
    return cam(img, 1 + 0.03 * u, 360, 700)


def s_glove(t, u, T):
    """slow motion: YOUR orange glove + red string meet the ball"""
    img, c = present_pitch(t)
    img = img.filter(ImageFilter.GaussianBlur(8))
    S = 10
    w, h = FW // S, FH // S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dx = int(6 * u)
    G1, G2 = (252, 140, 27), (206, 98, 14)
    d.polygon([(0, 120), (0, 104), (18 + dx, 74), (30 + dx, 86), (12, 128)], fill=(40, 168, 74))     # green sleeve
    d.polygon([(18 + dx, 74), (30 + dx, 86), (36 + dx, 78), (24 + dx, 66)], fill=SKIN["light"][0])  # wrist
    d.line([(20 + dx, 70), (31 + dx, 81)], fill=(225, 30, 40), width=2)                              # red string
    d.rounded_rectangle([24 + dx, 38, 46 + dx, 70], 4, fill=G1)                                       # glove palm
    for f in range(4):
        d.rectangle([26 + dx + f * 5, 24 + (2 if f in (0, 3) else 0), 29 + dx + f * 5, 40], fill=G1)
        d.line([(29 + dx + f * 5, 26), (29 + dx + f * 5, 40)], fill=G2)
    d.rectangle([24 + dx, 62, 46 + dx, 68], fill=G2)                                                  # strap
    d.polygon([(46 + dx, 52), (52 + dx, 44), (54 + dx, 48), (48 + dx, 58)], fill=G1)                  # thumb
    im = outline(im)
    img.alpha_composite(im.resize((w * S, h * S), Image.NEAREST))
    bx = 520 - 40 * u
    draw_ball(img, bx, 330, 7.5)
    glow_ring(img, 360 + dx * 10, 600, 200 + 30 * math.sin(t * 6), 0.4, (255, 220, 160))
    glow_ring(img, 260 + dx * 10, 760, 60 + 10 * math.sin(t * 8), 0.8, (255, 80, 80))     # the red string glows
    slowmo_bars(img, 1.0)
    return cam(img, 1.0 + 0.06 * u, 360, 640)


def s_pale(t, u, T):
    img, c = present_pitch(t)
    img = img.filter(ImageFilter.GaussianBlur(6))
    paste(img, coach(mouth="open", look=-1), 28, 380, 1620)
    vignette(img, 0.4 + 0.4 * u)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(1 - 0.75 * u).convert("RGBA")
    img = cam(img, 1.0 + 0.25 * ease_in_out(u), 380, 760)
    if u > 0.7:      # tape glitch into the past
        img = vhs(img, t, (u - 0.7) / 0.3 * 1.6)
        d = ImageDraw.Draw(img)
        rng = random.Random(int(t * 30))
        for _ in range(int(12 * (u - 0.7) / 0.3)):
            y = rng.uniform(0, FH); hgt = rng.uniform(6, 40)
            band = img.crop((0, int(y), FW, int(y + hgt)))
            img.paste(band, (int(rng.uniform(-40, 40)), int(y)))
    return img


def s_card(t, u, T):
    img = old_stadium(700).copy()
    pitch_persp(img, Cam(camH=1.4, hor=700), None, warm=False)
    img = img.filter(ImageFilter.GaussianBlur(5))
    tint(img, [0, 0, FW, FH], (0, 0, 0, 110))
    if u < 0.18:     # static noise
        rng = np.random.default_rng(int(t * 30))
        n = (rng.random((FH // 4, FW // 4)) * 255).astype(np.uint8)
        img = Image.fromarray(n, "L").resize((FW, FH), Image.NEAREST).convert("RGBA")
        return img
    k = spring(t - T - 0.18 * D(4), 12, 7)
    d = ImageDraw.Draw(img)
    if k > 0.15:
        d.text((360, 560), "MAY 1984", font=font(800, max(2, int(110 * min(1.1, k)))), fill=C_Y, anchor="mm", stroke_width=6, stroke_fill=OL)
    k2 = spring(t - T - 0.45 * D(4), 12, 7)
    if k2 > 0.05:
        crest(img, 190, 800, 1.3 * min(1.1, k2), "KIN")
        crest(img, 530, 800, 1.3 * min(1.1, k2), "NEW")
        d = ImageDraw.Draw(img)
        d.text((360, 800), "vs", font=font(800, 50), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=OL)
        d.text((190, 900), "KINGSTON", font=font(800, 34), fill=KIN, anchor="mm", stroke_width=4, stroke_fill=OL)
        d.text((530, 900), "NEWCASTLE", font=font(800, 34), fill=(120, 160, 250), anchor="mm", stroke_width=4, stroke_fill=OL)
    return img


FANS = []
_r = random.Random(84)
for row in range(7):
    for k in range(9):
        FANS.append((row, k * 84 - 20 + (42 if row % 2 else 0) + _r.uniform(-10, 10), _r.random(), _r.choice(
            [KIN, KIN, KIN, (60, 60, 70), (120, 60, 50), (70, 80, 110), NEW]), _r.choice(["dark", "brown", "blond", "ginger", "black", "grey"]),
            _r.choice(["light", "light", "tan", "brown"]), _r.random() < 0.35))


def s_terrace(t, u, T):
    """close on the standing terrace: rows of fans in scarves and flat caps, jumping in the rain"""
    img = Image.new("RGBA", (FW, FH), (36, 32, 46, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, 420):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, y / 420)) for a, b in zip((18, 20, 44), (46, 40, 60))))
    glow(img, 120, 120, 260, (255, 240, 200), 0.5); glow(img, 620, 90, 260, (255, 240, 200), 0.5)
    d = ImageDraw.Draw(img)
    for row in range(7):                      # concrete steps + crush barriers
        y = 380 + row * 130
        d.rectangle([0, y + 90, FW, y + 130], fill=(70, 66, 78))
        d.line([(0, y + 92), (FW, y + 92)], fill=(96, 92, 104), width=4)
        if row % 2 == 0:
            d.line([(0, y + 60), (FW, y + 60)], fill=(170, 174, 186), width=8)
            for x in range(40, FW, 160):
                d.line([(x, y + 60), (x, y + 120)], fill=(150, 154, 166), width=6)
    for row, x, ph, col, hair, skin, scarf in sorted(FANS, key=lambda f: f[0]):
        y = 380 + row * 130 + 92
        sc = 4 + row * 0.55
        jump = abs(math.sin(t * 5 + ph * 6)) * 16
        sp = person(Kit(col, (40, 40, 50), (40, 40, 50)), skin=skin, hair=hair, style="short",
                    pose="celebrate" if ph > 0.5 else "stand", trousers=True, blink=int(t * 3 + ph * 10) % 9 == 0)
        paste(img, sp, int(sc), x + lerp(-30, 30, u) * (row + 1) / 4, y - jump)
        if scarf:
            dd = ImageDraw.Draw(img)
            sy = y - jump - 34 * sc
            for k in range(6):
                dd.rectangle([x - 30 + k * 10, sy + math.sin(t * 7 + k + ph * 5) * 6, x - 21 + k * 10, sy + 8 + math.sin(t * 7 + k + ph * 5) * 6],
                             fill=KIN if k % 2 else (30, 30, 36))
    rain84(img, t, 120)
    return cam(img, 1.05, 360, 760)


def s_grandad_intro(t, u, T):
    img, c = set84(560, 7.0, camH=1.1)
    bob = abs(math.sin(t * 5)) * 0.06
    pose = "catch" if int(t * 4) % 2 else "ready"
    ground_shadow(img, c, 0, 7.0, 0.5)
    sprite_at(img, c, young_grandad(pose=pose, mouth="smile"), 0, 7.0, Y=bob, height_m=1.85)
    for X in (-6.5, 6.0):
        ground_shadow(img, c, X, 5.5, 0.35)
        sprite_at(img, c, kingston(5 if X < 0 else 4, view="back"), X, 5.5, height_m=1.75)
    rain84(img, t, 100)
    pill(img, 360, 1030, "KINGSTON · No. 1", (30, 30, 36), spring(t - T - 0.3, 13, 7), 30, fg=KIN)
    return cam(img, 1.0 + 0.08 * u, 360, 760)


def s_same(t, u, T):
    img = old_stadium(560).filter(ImageFilter.GaussianBlur(5))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(70, 110, 62))
    clap = int(t * 3) % 2 == 0 and u < 0.55
    paste(img, young_grandad(pose="catch" if clap else "stand", mouth="smile", blink=0.6 < u < 0.64), 24, 360, 1450)
    # the gloves and the red string glow
    k = 0.5 + 0.5 * math.sin(t * 7)
    if u < 0.55:
        glow_ring(img, 360, 1050, 150 + 20 * k, 0.6, (255, 190, 90))
    else:
        glow_ring(img, 178, 1085, 60 + 12 * k, 0.9, (255, 70, 70))
    rain84(img, t, 90)
    return cam(img, 1.0 + 0.05 * u, 360, 800)


def s_nine(t, u, T):
    img = old_stadium(560).filter(ImageFilter.GaussianBlur(5))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(70, 110, 62))
    paste(img, young_coach(mouth="grin" if u > 0.4 else "flat", look=-1, blink=0.2 < u < 0.24), 24, 360, 1430 - abs(math.sin(t * 4)) * 10)
    rain84(img, t, 90)
    pill(img, 360, 1030, "NEWCASTLE · No. 9", (30, 30, 36), spring(t - T - 0.3, 13, 7), 30, fg=(140, 180, 255))
    return cam(img, 1.0 + 0.05 * u, 360, 820)


VOLLEY = arc((1.45, 7.4, 0.3), (-1.6, 14.0, 1.25), apex=0.7)


def s_volley(t, u, T):
    img, c = set84(640, 14.0, camH=2.0)
    kick = 0.3
    kp = min(0.7, 0.1 + clamp((u - kick) / 0.9) * 0.9) if u > kick else 0.05
    gx, gy = keeper84(img, c, 0, 14.0, -1, kp)
    for X, Z, n, team in ((-2.6, 10.5, 5, "K"), (2.4, 11, 4, "K"), (3.6, 8, 7, "N")):
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, kingston(n) if team == "K" else newcastle(n, view="back", pose="run", phase=t * 2), X, Z, height_m=1.7)
    if u < kick:      # the cross drops onto his volley
        a = u / kick
        ball_at(img, c, lerp(6.0, 1.45, a), lerp(10.0, 7.4, a), 2.8 * (1 - a) + 0.3 * a)
    elif kp < 0.38:
        a = clamp((u - kick) / 0.26)
        ball_trail(img, c, VOLLEY, a, 0.15)
        ball_at(img, c, *at(VOLLEY, a))
    else:             # parried: it spills off his gloves and drops loose in the six-yard box
        b = clamp((kp - 0.38) / 0.3)
        ball_at(img, c, lerp(-1.6, -1.4, b), lerp(14.0, 13.6, b), 1.25 * (1 - b) + 0.35 * abs(math.sin(b * math.pi)) * (1 - b))
        if b < 0.3:
            glow_ring(img, gx, gy, 60, 0.8 * (1 - b / 0.3), (255, 255, 200))
    ground_shadow(img, c, 1.6, 6.9, 0.4)
    sprite_at(img, c, young_coach(view="back", pose="kick" if u > kick - 0.08 else "run",
                                   phase=clamp((u - kick + 0.08) / 0.15) if u > kick - 0.08 else t * 2.4), 1.6, 6.9, height_m=1.8)
    rain84(img, t, 100)
    return cam(img, 1.2 + 0.06 * u, 360, 860)


def s_rebound(t, u, T):
    """he parried it; #8 hits the rebound, Grandad springs across and blocks it"""
    img, c = set84(640, 14.0, camH=2.0)
    rb = arc((-1.4, 13.6, 0.4), (2.4, 9.8, 0.0), apex=1.4)
    shot = arc((2.4, 9.8, 0.1), (1.4, 14.0, 0.5), apex=0.2)
    if u < 0.3:          # Grandad still on the ground after the first save
        s = 1.75 * c.k(14) / 31
        sp = young_grandad(pose="reach").resize((int(24 * s), int(39 * s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
        x, y = c.p(-1.7, 14.0)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * s)))
        a = u / 0.3
        ball_at(img, c, *at(rb, a))
    else:
        ph = clamp((u - 0.3) / 0.7)
        gx, gy = keeper84(img, c, -0.4, 14.0, 1, min(0.7, 0.1 + ph * 0.9))
        a = clamp((u - 0.38) / 0.12)
        if a < 1:
            ball_trail(img, c, shot, a, 0.15)
            ball_at(img, c, *at(shot, a))
        else:
            b = clamp((u - 0.5) / 0.5)
            ball_at(img, c, lerp(1.4, 4.5, b), lerp(13.6, 11.0, b), 1.8 * math.sin(b * math.pi) + 0.1)
            if b < 0.3:
                glow_ring(img, gx, gy, 70, 0.8 * (1 - b / 0.3), (255, 255, 200))
    ground_shadow(img, c, 2.7, 9.6, 0.35)          # the striker is nearer the camera: drawn last
    sprite_at(img, c, newcastle(8, pose="kick" if 0.3 < u < 0.45 else "run", phase=clamp((u - 0.3) / 0.12) if u > 0.3 else t * 2), 2.7, 9.6, height_m=1.7)
    rain84(img, t, 100)
    return cam(img, 1.2 + 0.06 * u, 360, 860, *shake(t, T + 0.5 * D(10), .3, 10))


def s_score(t, u, T):
    """behind Grandad's goal: far end, Kingston score; Grandad jumps, the terrace erupts"""
    c = Cam(camH=1.7, hor=520)
    img = old_stadium(520)
    mud_pitch(img, c, None)
    goal3d(img, c, 70.0, w=7.3, h=2.4)
    goalt = 0.4
    for i, (X, Z) in enumerate(((-3, 58), (1, 62), (4, 60))):
        sprite_at(img, c, kingston(6 + i, pose="run", phase=t * 2), X + math.sin(t + i), Z, height_m=1.8)
    sprite_at(img, c, person(Kit((90, 90, 100), (30, 30, 36), (90, 90, 100)), hair="black", gloves=True, pose="ready"), 0.5, 69.5, height_m=1.8)
    a = clamp(u / goalt)
    ball_at(img, c, lerp(1.0, 2.6, a), lerp(62, 70.5, a), 0.6 * math.sin(a * math.pi) + 0.2)
    jump = abs(math.sin(clamp((u - goalt) / 0.6) * math.pi * 2)) * 50 if u > goalt else 0
    paste(img, young_grandad(view="back", pose="celebrate" if u > goalt else "ready"), 14, 340, 1420 - jump)
    gx_, gy_ = c.p(2.6, 70.5, 0.4)
    if u > goalt:
        glow_ring(img, gx_, gy_, 20 + 60 * clamp((u - goalt) * 4), 0.9 * (1 - clamp((u - goalt) * 4)), (255, 230, 150))
        img = flash(img, 0.25 * clamp(1 - (u - goalt) * 6), (255, 220, 120))
    rain84(img, t, 100)
    z = ease_in_out(clamp((u - goalt) / 0.3))
    return cam(img, lerp(3.2, 1.0, z), lerp(gx_, 360, z), lerp(gy_ + 60, 720, z))


def s_angry(t, u, T):
    img, c = set84(560, 12.0, camH=1.4)
    sprite_at(img, c, young_grandad(pose="ready", mouth="smile"), 0, 12.0, height_m=1.8)
    img = img.filter(ImageFilter.GaussianBlur(3))
    kick = 0.45
    paste(img, young_coach(pose="kick" if u > kick else "stand", phase=clamp((u - kick) / 0.15), mouth="open", look=-1), 22, 360, 1450)
    if u > kick:
        mud_splash(img, 430, 1180, (u - kick) / 0.4, 60)
    rain84(img, t, 90)
    return cam(img, 1.0 + 0.05 * u, 360, 860)


def s_corner(t, u, T):
    if u < 0.45:     # the old scoreboard: 89'
        img = old_stadium(980).filter(ImageFilter.GaussianBlur(4))
        d = ImageDraw.Draw(img)
        d.rectangle([90, 420, 630, 820], fill=(12, 12, 16), outline=(160, 160, 170), width=10)
        f = font(800, 50)
        d.text((360, 500), "KINGSTON  1", font=f, fill=(255, 220, 120), anchor="mm")
        d.text((360, 590), "NEWCASTLE 0", font=f, fill=(255, 220, 120), anchor="mm")
        on = int(t * 3) % 2 == 0
        d.text((360, 720), "89", font=font(800, 110), fill=(255, 80, 60) if on else (120, 40, 30), anchor="mm")
        for k in range(8):
            d.ellipse([120 + k * 66, 440 + (360 if k % 2 else 0) * 0, 132 + k * 66, 452], fill=(255, 230, 150) if on else (80, 70, 50))
        return cam(img, 1.0 + 0.06 * u, 360, 640)
    c = Cam(camX=3.0, camH=2.2, hor=640, f=520)
    img = old_stadium(640)
    mud_pitch(img, c, 13.0)
    goal3d(img, c, 13.0)
    rng = random.Random(8)
    ppl = []
    for i in range(14):
        ppl.append((rng.uniform(9.0, 12.2), rng.uniform(-3.0, 3.0), i % 2))
    ppl.append((13.0, 0.3, 2))
    for Z, X, tm in sorted(ppl, key=lambda q: -q[0]):
        ground_shadow(img, c, X, Z, 0.3)
        sp = young_grandad(pose="ready") if tm == 2 else (kingston(3 + int(X * 7) % 6) if tm else newcastle([4, 5, 7, 8, 6][int(Z * 3) % 5], view="back"))
        sprite_at(img, c, sp, X + math.sin(t * 6 + X) * 0.03, Z, height_m=1.75)
    sprite_at(img, c, young_coach(view="back"), 0.6, 10.6, height_m=1.8)
    d = ImageDraw.Draw(img)
    x, y = c.p(9.6, 13.0)
    d.line([(x, y), (x, y - 50)], fill=(250, 250, 250), width=3)
    d.polygon([(x, y - 50), (x + 18, y - 45 + math.sin(t * 8) * 3), (x, y - 38)], fill=(240, 200, 40))
    ground_shadow(img, c, 9.2, 12.3, 0.3)
    sprite_at(img, c, newcastle(7, view="back"), 9.2, 12.3, height_m=1.75)
    ball_at(img, c, 9.1, 12.8, 0.0)
    rain84(img, t, 110)
    return cam(img, 1.05 + 0.04 * u, 360, 760)


def s_hang(t, u, T):
    """low angle up into the floodlights; the ball hangs in the rain"""
    img = Image.new("RGBA", (FW, FH), (14, 16, 36, 255))
    d = ImageDraw.Draw(img)
    for y in range(FH):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, y / FH)) for a, b in zip((10, 12, 30), (60, 50, 80))))
    for px, py in ((120, 260), (600, 300)):
        d.rectangle([px - 70, py - 40, px + 70, py + 40], fill=(40, 40, 50), outline=OL, width=4)
        for r in range(3):
            for k in range(5):
                d.rectangle([px - 62 + k * 26, py - 34 + r * 24, px - 42 + k * 26, py - 16 + r * 24], fill=(255, 250, 220))
        glow(img, px, py, 300, (255, 240, 200), 0.45)
    rain(img, t, 160, 220)
    bx = lerp(620, 300, u); by = lerp(420, 560, u) - 60 * math.sin(u * math.pi)
    glow(img, bx, by, 90, (255, 255, 230), 0.4)
    draw_ball(img, bx, by, 3.0)
    # heads and raised arms at the bottom edge (silhouettes)
    for i, x in enumerate((60, 200, 330, 470, 610)):
        sp = (young_grandad if i == 2 else (kingston if i % 2 else newcastle))
        s_ = sp(4 + i) if sp is not young_grandad else sp(pose="reach")
        if sp is newcastle and i == 3:
            s_ = young_coach(view="back")
        paste(img, s_, 16, x, 1660 + (60 if i != 2 else 0), alpha=1.0)
    slowmo_bars(img, 1.0)
    return cam(img, 1.0 + 0.05 * u, 360, 640)


def s_jump(t, u, T):
    img = side_set(t)
    j = ease_out(u)
    mx, my = collision(img, j * 0.96, 0.0, t)
    ball_side(img, lerp(560, mx + 40, u), max(430, lerp(430, my - 100, u)), 2.6)
    rain84(img, t, 120)
    slowmo_bars(img, 1.0)
    return cam(img, 1.0 + 0.1 * u, 380, 800)


def s_impact(t, u, T):
    img = side_set(t)
    mx, my = collision(img, 1.0, clamp(u / 0.3), t)
    if u > 0.45:        # gravity: Grandad drops out of the air into the mud, #9 lands on his feet
        return s_silence(t, (u - 0.45) / 0.55 * 0.75, T)
    b = clamp(u / 0.6)
    ball_side(img, mx + 40 + 220 * b, max(430, my - 100 - 60 * math.sin(b * math.pi * 0.6)), 2.6)
    impact_lines(img, mx, my + 160, T, t, 16)
    glow_ring(img, mx, my + 160, 80 + 300 * clamp(u * 2), 0.9 * (1 - clamp(u * 2)), (255, 255, 255))
    img = flash(img, 0.85 * clamp(1 - u * 5))
    rain84(img, t, 120)
    return cam(img, 1.15, mx, my + 200, *shake(t, T, .5, 22))


def s_silence(t, u, T):
    img = side_set(t)
    f = ease_in_out(clamp(u / 0.6))
    # Grandad falls into the mud, #9 lands on his feet
    ground = 1060
    s = 11
    g = young_grandad(pose="reach", blink=True, mouth="flat")
    paste(img, g, s, lerp(260, 300, f), lerp(870, ground + 40, f), rot=lerp(18, 90, f))
    co = young_coach(pose="stand" if f > 0.5 else "kickL", phase=0.9)
    paste(img, co, s, lerp(480, 520, f), lerp(830, ground, f))
    if 0.55 < u < 0.8:
        mud_splash(img, 300, ground + 10, (u - 0.55) / 0.25, 70)
    b = clamp(u)
    ball_side(img, lerp(700, 420, b), ground - 20 - 200 * abs(math.sin(b * math.pi * 1.5)) * (1 - b), 2.2)
    rain84(img, t, 140)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(0.25).convert("RGBA")
    vignette(img, 0.6)
    return cam(img, 1.05 + 0.04 * u, 380, 820)


def s_mud(t, u, T):
    """top-down: Grandad in the mud, eyes shut, gloves still on his hands"""
    img = Image.new("RGBA", (FW, FH), (70, 106, 60, 255))
    d = ImageDraw.Draw(img)
    for k in range(9):
        y = k * 150
        d.rectangle([0, y, FW, y + 75], fill=(64, 98, 56))
    rng = random.Random(3)
    for k in range(14):
        x, y, r = rng.uniform(0, FW), rng.uniform(300, 1200), rng.uniform(60, 160)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=MUD if k % 2 else MUD_D)
    d.line([(0, 1180), (FW, 1150)], fill=(220, 226, 210), width=10)       # 6-yard line, smudged
    sp = big(young_grandad(pose="reach", blink=True, mouth="flat"), 16).rotate(90, expand=True, resample=Image.NEAREST)
    img.alpha_composite(sp, (int(360 - sp.width / 2), int(720 - sp.height / 2)))
    # rain ripples in the puddles
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for k in range(10):
        ph = (t * 1.3 + k * 0.37) % 1
        x, y = rng.uniform(40, 680), rng.uniform(320, 1180)
        r = 10 + 40 * ph
        dd.ellipse([x - r, y - r * 0.5, x + r, y + r * 0.5], outline=(230, 230, 240, int(160 * (1 - ph))), width=3)
    img.alpha_composite(ov)
    if u > 0.55:
        glow_ring(img, 120, 600, 80 + 10 * math.sin(t * 6), 0.7, (255, 190, 90))   # the gloves
    rain(img, t, 90, 120)
    vignette(img, 0.55)
    return cam(img, 1.0 + 0.2 * ease_in_out(u), 360, 700)


def s_rollin(t, u, T):
    img, c = set84(520, 9.0, camX=0.8, camH=0.9)
    s = 1.75 * c.k(8.2) / 31
    sp = young_grandad(pose="reach", blink=True).resize((int(24 * s), int(39 * s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
    x, y = c.p(-1.5, 8.2)
    img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * s)))
    a = clamp(u / 0.6)
    X, Z = lerp(1.6, 0.6, a), lerp(5.5, 9.6, a)
    ball_at(img, c, X, Z, 0.0)
    for i, (Xp, Zp) in enumerate(((2.8, 6.0), (-3.4, 6.8))):
        ground_shadow(img, c, Xp, Zp, 0.35)
        sprite_at(img, c, newcastle(7 if i else 4, pose="celebrate" if u > 0.6 else "stand"), Xp, Zp, height_m=1.75)
    if u > 0.6:
        impact_lines(img, *c.p(0.6, 9.6, 0.3), T + 0.6 * D(19), t, 10)
    rain84(img, t, 110)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(0.6).convert("RGBA")
    return cam(img, 1.0 + 0.05 * u, 380, 760)


def s_stretcher(t, u, T):
    img = old_stadium(640).copy()
    pitch_persp(img, Cam(camH=1.4, hor=640), None, warm=False)
    x0 = lerp(70, 130, u)
    step = abs(math.sin(t * 4)) * 6
    S_ = 10
    by = 990
    sy = by - 17 * S_ - step                  # hand height of the medics ("phone" pose: hands at the chest)
    sx0, sx1 = x0 + 70, x0 + 490
    paste(img, medic(pose="phone", look=1), S_, x0, by - step)
    paste(img, medic(pose="phone", skin="tan", hair="black", look=-1), S_, x0 + 560, by - step)
    d = ImageDraw.Draw(img)
    d.rectangle([sx0, sy - 30, sx1, sy], fill=(230, 226, 210), outline=OL, width=4)                 # canvas
    sp = big(young_grandad(pose="stand", blink=True, mouth="flat"), 10).rotate(90, expand=True, resample=Image.NEAREST)
    img.alpha_composite(sp, (int(sx0 + 10), int(sy - sp.height + 64)))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 - 10, sy - 6, x0 + 570, sy + 6], fill=(150, 150, 160), outline=OL, width=3)     # poles, end to end
    for hx_ in (x0, x0 + 560):                                                                     # fists on the handles
        d.rounded_rectangle([hx_ - 22, sy - 14, hx_ + 22, sy + 14], 6, fill=SKIN["light"][0], outline=OL, width=3)
    rain84(img, t, 120)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(0.55).convert("RGBA")
    d = ImageDraw.Draw(img)                                           # his gloved hand hangs over the side (kept in full colour)
    hx = sx0 + 190                                                    # at his shoulder
    d.rectangle([hx, sy, hx + 22, sy + 70], fill=KEEPER_G, outline=OL, width=3)
    d.rectangle([hx - 2, sy + 62, hx + 24, sy + 70], fill=(225, 30, 40))
    d.rounded_rectangle([hx - 14, sy + 70, hx + 36, sy + 128], 10, fill=(255, 140, 20), outline=OL, width=4)
    d.rectangle([hx - 14, sy + 70, hx + 36, sy + 82], fill=(210, 96, 10), outline=OL, width=3)     # cuff strap
    for f_ in range(3):
        d.line([(hx - 2 + f_ * 12, sy + 104), (hx - 2 + f_ * 12, sy + 126)], fill=(200, 90, 10), width=3)
    return cam(img, 1.0 + 0.05 * u, 360, 800)


def s_face(t, u, T):
    img = old_stadium(560).filter(ImageFilter.GaussianBlur(6))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(60, 90, 56))
    paste(img, young_coach(mouth="flat", look=-1 if u < 0.5 else 0, blink=0.7 < u < 0.73), 26, 360, 1460 + 20 * u)
    # floodlight from above: his eyes in shadow
    top = 1460 + 20 * u - 39 * 26
    tint(img, [360 - 5 * 26, top + 12 * 26, 360 + 5 * 26, top + 15 * 26], (0, 0, 0, 160))
    rain84(img, t, 120)
    vignette(img, 0.6)
    return cam(img, 1.0 + 0.18 * ease_in_out(u), 360, 800)


def s_today(t, u, T):
    if u < 0.55:
        img, c = present_pitch(t)
        sprite_at(img, c, hero(pose="stand", gloves=True, look=1), 0, 8.5, height_m=1.6)
        img = img.filter(ImageFilter.GaussianBlur(2))
        CB = 1500
        paste(img, coach(mouth="open", look=-1), 22, 420, CB)
        top = CB - 39 * 22
        collar = (420 - 12 * 22 + (3 + 9) * 22, top + 18 * 22)              # neck of his shirt
        f = clamp((u - 0.25) / 0.3)
        hx, hy = 420 - 12 * 22 + (3 + 16) * 22, top + 25 * 22              # his hand by his side
        wx, wy = hx - 20, hy + 900 * f * f
        d = ImageDraw.Draw(img)
        d.line([collar, (wx + 30, wy - 10)], fill=(40, 40, 50), width=4)
        d.rounded_rectangle([wx, wy - 26, wx + 64, wy + 8], 12, fill=(200, 204, 214), outline=OL, width=4)
        d.rectangle([wx + 50, wy - 30, wx + 70, wy - 18], fill=(170, 174, 186), outline=OL, width=3)
        if u < 0.2:
            img = vhs(img, t, 1.5 * (1 - u / 0.2))
        return cam(img, 1.0 + 0.04 * u, 360, 820)
    # insert: the whistle hits the grass and bounces once, the cord trailing up out of frame
    v = (u - 0.55) / 0.45
    img = Image.new("RGBA", (FW, FH), (70, 140, 74, 255))
    d = ImageDraw.Draw(img)
    rng = random.Random(6)
    for _ in range(500):
        x, y = rng.uniform(0, FW), rng.uniform(0, FH)
        d.line([(x, y), (x + rng.uniform(-4, 4), y - rng.uniform(8, 20))], fill=(60, 126, 64) if rng.random() < 0.5 else (90, 160, 86), width=3)
    yb = 880 - 260 * max(0.0, 1 - v * 5) ** 2 if v < 0.2 else 880 - 60 * abs(math.sin((v - 0.2) * 10)) * math.exp(-(v - 0.2) * 9)
    cord = [(260, yb - 30), (200, yb + 20), (140, yb + 40), (60, yb + 30), (-20, yb + 50)]     # slack on the grass
    d.line(cord, fill=(40, 40, 50), width=8)
    d.rounded_rectangle([260, yb - 70, 420, yb + 10], 30, fill=(200, 204, 214), outline=OL, width=8)
    d.rectangle([390, yb - 80, 450, yb - 46], fill=(170, 174, 186), outline=OL, width=6)
    d.ellipse([290, yb - 56, 320, yb - 26], fill=(150, 154, 166))
    if 0.18 < v < 0.35:
        impact_lines(img, 340, yb + 10, T + 0.55 * D(22) + 0.2 * 0.45 * D(22), t, 10)
    shadow(img, 340, 900, 200, 30, 80)
    vignette(img, 0.4)
    return cam(img, 1.0 + 0.05 * v, 360, 760)


def choice_bg():
    img = Image.new("RGBA", (FW, FH), (20, 26, 70, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, FH, 60):
        for x in range(0, FW, 60):
            if (x // 60 + y // 60) % 2:
                d.rectangle([x, y, x + 60, y + 60], fill=(24, 32, 82))
    return img


CARDS = [(190, "ACCIDENT", "BOTH WENT FOR THE BALL", C_B), (530, "ON PURPOSE", "KNEE FIRST. HE MEANT IT", C_R)]


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
            paste(img, young_grandad(pose="reach"), 4, x - 40, y + 30, rot=-15)
            co = young_coach(pose="kickL", phase=0.9 if i else 0.5, mouth="grin" if i else "open")
            paste(img, co, 4, x + 45, y + 30, rot=10)
            draw_ball(img, x, y - 120, 1.2)
            d = ImageDraw.Draw(img)
            d.text((x, y + 110), lab, font=font(800, 40), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            d.text((x, y + 160), sub, font=font(700, 18), fill=(220, 224, 240), anchor="mm")


def typing_box(img, t, T0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 960, 630, 1030], 18, fill=(16, 18, 36), outline=(255, 255, 255), width=3)
    words = ["ACCIDENT", "ON PURPOSE"]
    k = (t - T0) / 1.1
    wi = min(1, int(k))
    w = words[wi]
    n = int(len(w) * clamp((k - wi) * 2)) if k < 2 else len(w)
    d.text((120, 995), w[:n] + ("|" if int(t * 4) % 2 else ""), font=font(800, 30), fill=(255, 255, 255), anchor="lm")


def s_choice(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 0.2)
    typing_box(img, t, T + 0.3)
    pill(img, 360, 340 + UYF, "VOTE BEFORE FRIDAY", (200, 50, 60), spring(t - T - 0.3, 13, 7), 28)
    return cam(img, 1.0 + 0.02 * u, 360, 760)


def s_end(t, u, T):
    img = choice_bg()
    img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (10, 12, 30)), 0.88 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 560], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 150), "PART 8", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
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
    if t < tap + 0.4:
        gx = lerp(640, bx + 100, ease_in_out((t - T) / 0.8)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, cc in ((230, "ACCIDENT", C_B), (490, "ON PURPOSE", C_R)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 115, py + 400 - hop, x + 115, py + 470 - hop], 18, fill=(30, 36, 76), outline=cc, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 28), fill=cc, anchor="mm")
    d.text((360, py + 520), "VOTE IN THE COMMENTS", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    return img


SCENES = [s_hook, s_showme, s_glove, s_pale, s_card, s_terrace, s_grandad_intro, s_same, s_nine, s_volley, s_rebound,
          s_score, s_angry, s_corner, s_hang, s_jump, s_impact, s_silence, s_mud, s_rollin, s_stretcher, s_face,
          s_today, s_choice, s_end]
assert len(SCENES) == len(LINES)


def grade(img):
    img = ImageEnhance.Color(img).enhance(0.85)
    img = ImageEnhance.Contrast(img).enhance(0.95)
    return Image.blend(img, Image.new("RGB", img.size, (60, 50, 70)), 0.05)


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
    if i in PAST and SCENES[i] is not s_card:
        img = vhs(img, t, 1.0)
        k, n, m = score84(t)
        mc = match_clock(t)
        if i != 7:
            vhs_osd(img, t, f"MAY 14 1984  {mc // 60}:{mc % 60:02d}" if i >= 9 else "MAY 14 1984")
        if 9 <= i <= 19 and i not in (14, 15, 16, 17, 18) and not (i == 13 and t < T + 0.45 * D(13)):
            bug84(img, t)
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
