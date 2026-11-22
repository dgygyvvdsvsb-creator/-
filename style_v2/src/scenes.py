"""Key shots of the remi_sport look, rebuilt with our cast. Run: python3 scenes.py"""
import math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from sprites import *

FW, FH = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out"); os.makedirs(OUT, exist_ok=True)
FONTS = os.path.join(HERE, "..", "..", "ep3", "src", "fonts")
def font(w, s): return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{w}.ttf"), s)
Y, TEAL, RED, BLUE = (255, 205, 40), (60, 220, 170), (255, 80, 80), (100, 170, 255)
rnd = random.Random(7)

# ------------------------------------------------------------------ helpers
def lowres(w=180, h=320): return Image.new("RGBA", (w, h), (0, 0, 0, 255))
def up(im, k=6): return im.resize((im.width * k, im.height * k), Image.NEAREST)

def shadow(img, cx, y, w, a=90):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.ellipse([cx - w / 2, y - w * 0.09, cx + w / 2, y + w * 0.09], fill=(0, 0, 0, a))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6)))

def put(img, spr, k, cx, foot, rot=0, sh=True):
    s = big(spr, k)
    if rot: s = s.rotate(rot, expand=True, resample=Image.NEAREST)
    if sh: shadow(img, cx, foot - 2 * k, s.width * 0.5)
    img.alpha_composite(s, (int(cx - s.width / 2), int(foot - s.height)))

def ball(k=10):
    b = Image.new("RGBA", (10, 10), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([0, 0, 9, 9], fill=(26, 20, 30)); d.ellipse([1, 1, 8, 8], fill=(250, 250, 250))
    d.rectangle([4, 3, 5, 5], fill=(30, 30, 36)); d.point([(2, 6), (7, 6), (4, 8), (5, 8), (2, 2), (7, 2)], fill=(30, 30, 36))
    d.point([(7, 7), (6, 8)], fill=(190, 190, 200))
    return big(b, k)

def stripes(d, y0, y1, w, a=(48, 150, 74), b=(42, 138, 66), n=8):
    for i in range(n):
        d.rectangle([0, y0 + (y1 - y0) * i / n, w, y0 + (y1 - y0) * (i + 1) / n], fill=a if i % 2 == 0 else b)

def trees(d, horizon, w, cols=((40, 104, 58), (52, 124, 66), (30, 84, 48))):
    for i in range(16):
        x = i * w / 13 - 8 + rnd.randint(-4, 4); r = rnd.randint(13, 20)
        d.rectangle([x - 1, horizon - 10, x + 1, horizon], fill=(80, 56, 40))
        d.ellipse([x - r, horizon - 10 - r * 1.6, x + r, horizon - 6], fill=cols[2])
        d.ellipse([x - r + 2, horizon - 12 - r * 1.6, x + r - 4, horizon - 9], fill=cols[0])
        d.ellipse([x - r + 4, horizon - 12 - r * 1.5, x + r * 0.3, horizon - 18], fill=cols[1])

def fence(d, y0, y1, w):
    d.rectangle([0, y0, w, y0 + 1], fill=(170, 176, 186))
    for x in range(0, w, 3): d.rectangle([x, y0, x, y1], fill=(150, 156, 168))
    d.rectangle([0, y1, w, y1], fill=(110, 116, 128))

def crowd(img, y0, y1, k=7, colors=((214, 52, 58), (245, 245, 250), (30, 40, 90), (44, 170, 76))):
    """dense pixel crowd: rows of tiny fans (head + shirt) like the reference stadium"""
    d = ImageDraw.Draw(img)
    d.rectangle([0, y0, FW, y1], fill=(22, 26, 48))
    row = 0
    y = y0
    while y < y1 - 6 * k:
        x = -(row % 2) * 3 * k
        d.rectangle([0, y + 5 * k, FW, y + 7 * k], fill=(34, 40, 70))
        while x < FW:
            sk = rnd.choice(list(SKIN.values()))[0]; hr = rnd.choice(list(HAIR.values()))[0]
            sh = rnd.choice(colors)
            d.rectangle([x + k, y, x + 4 * k - 1, y + 3 * k - 1], fill=sk)
            d.rectangle([x + k, y, x + 4 * k - 1, y + k - 1], fill=hr)
            d.point([(0, 0)])
            d.rectangle([x + 2 * k, y + k + k // 2, x + 2 * k + k // 2, y + 2 * k], fill=(20, 16, 22))
            d.rectangle([x, y + 3 * k, x + 5 * k - 1, y + 6 * k], fill=sh)
            if rnd.random() < 0.25:   # raised arm
                d.rectangle([x + 4 * k, y - k, x + 5 * k - 1, y + 3 * k], fill=sk)
            x += 6 * k
        y += 7 * k; row += 1

def adboard(img, y, h=40):
    d = ImageDraw.Draw(img)
    for i in range(0, FW, 180):
        d.rectangle([i, y, i + 180, y + h], fill=(214, 40, 50) if (i // 180) % 2 == 0 else (245, 245, 250))
        d.rectangle([i + 50, y + 14, i + 130, y + h - 14], fill=(245, 245, 250) if (i // 180) % 2 == 0 else (214, 40, 50))

def navy_bg():
    im = Image.new("RGBA", (FW, FH))
    d = ImageDraw.Draw(im)
    for y in range(FH):
        t = 1 - abs(y / FH - 0.45) * 1.8
        t = max(0, t)
        d.line([(0, y), (FW, y)], fill=(int(8 + 26 * t), int(14 + 44 * t), int(36 + 92 * t)))
    ov = Image.new("RGBA", (FW, FH), (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
    s = 64
    for yy in range(0, FH, s):
        for xx in range(0, FW, s):
            if (xx // s + yy // s) % 2 == 0:
                o.rectangle([xx, yy, xx + s, yy + s], fill=(255, 255, 255, 10))
    im.alpha_composite(ov)
    return im

REC = None
def banner(img, ep=7):
    if REC is not None: REC.append(('banner', (), {'ep': ep})); return
    d = ImageDraw.Draw(img)
    f = font(600, 26)
    a = f"EP. {ep} · FROM ZERO TO "
    wa = d.textlength(a, font=f); wb = d.textlength("LEGEND", font=f)
    x = FW / 2 - (wa + wb) / 2
    d.text((x + 2, 104), a, font=f, fill=(0, 0, 0, 120)); d.text((x, 102), a, font=f, fill=(236, 238, 246))
    d.text((x + wa, 102), "LEGEND", font=f, fill=Y)

def caption(img, words, spoken=None, y=165, size=74):
    """words: list of (text, colour or None). spoken = how many words are 'said' (rest dim)"""
    if REC is not None: REC.append(('caption', (words,), {'y': y, 'size': size})); return
    d = ImageDraw.Draw(img)
    f = font(800, size)
    spoken = len(words) if spoken is None else spoken
    lines, cur, wcur = [], [], 0
    for i, (t, c) in enumerate(words):
        tw = d.textlength(t + " ", font=f)
        if wcur + tw > FW - 140 and cur:
            lines.append(cur); cur, wcur = [], 0
        cur.append((i, t, c)); wcur += tw
    lines.append(cur)
    for li, ln in enumerate(lines):
        tot = sum(d.textlength(t + " ", font=f) for _, t, _ in ln) - d.textlength(" ", font=f)
        x = FW / 2 - tot / 2; yy = y + li * size * 1.08
        for i, t, c in ln:
            col = (c or (255, 255, 255)) if i < spoken else (150, 156, 176)
            d.text((x + 3, yy + 5), t, font=f, fill=(0, 0, 0, 150))
            d.text((x, yy), t, font=f, fill=col, stroke_width=2, stroke_fill=(20, 18, 30))
            x += d.textlength(t + " ", font=f)

def W_(s, c=None): return [(w, c) for w in s.split()]

def finish(img, name):
    img.convert("RGB").save(os.path.join(OUT, name)); return img

# ------------------------------------------------------------------ 1. training pitch (ref ep.8 coach whistle)
def s_training():
    b = lowres(); d = ImageDraw.Draw(b)
    for y in range(120):
        t = y / 120; d.line([(0, y), (180, y)], fill=(int(110 + 70 * t), int(170 + 50 * t), int(225 + 15 * t)))
    trees(d, 112, 180); fence(d, 98, 112, 180)
    stripes(d, 112, 320, 180, n=10)
    d.line([(0, 132), (180, 128)], fill=(236, 240, 236)); d.line([(150, 320), (178, 128)], fill=(236, 240, 236))
    d.line([(120, 320), (150, 210)], fill=(236, 240, 236))
    img = up(b)
    blur = img.crop((0, 0, FW, 680)).filter(ImageFilter.GaussianBlur(2.2)); img.paste(blur, (0, 0))
    put(img, coach(mouth="open"), 12, 260, 1440)
    # whistle waves
    d = ImageDraw.Draw(img)
    for i, r in enumerate((26, 46, 66)):
        d.arc([330 - r, 1085 - r, 330 + r, 1085 + r], -40, 40, fill=(250, 250, 250), width=7)
    put(img, hero(mouth="flat"), 12, 640, 1390)
    put(img, alfie(mouth="smile"), 12, 850, 1390)
    img.alpha_composite(ball(9), (690, 1310))
    banner(img); caption(img, W_("THE COACH") + W_("BLOWS", Y) + W_("THE WHISTLE:"), spoken=4)
    return finish(img, "s1_training.png")

# ------------------------------------------------------------------ 2. locker room (ref ep.6/5)
def s_locker():
    b = lowres(); d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 180, 200], fill=(34, 120, 76))
    for x in range(0, 180, 22):
        d.rectangle([x, 20, x + 20, 196], fill=(48, 150, 92)); d.rectangle([x + 18, 20, x + 20, 196], fill=(30, 104, 64))
        d.rectangle([x + 3, 30, x + 15, 31], fill=(30, 96, 60)); d.rectangle([x + 3, 34, x + 15, 35], fill=(30, 96, 60))
        d.rectangle([x + 15, 100, x + 16, 112], fill=(210, 216, 222))
    d.rectangle([0, 0, 180, 18], fill=(24, 34, 60))
    for yy in range(200, 320, 12):
        for xx in range(0, 180, 12):
            d.rectangle([xx, yy, xx + 11, yy + 11], fill=(92, 104, 134) if ((xx + yy) // 12) % 2 else (104, 116, 148))
    d.rectangle([0, 196, 180, 200], fill=(60, 64, 84))
    d.rectangle([0, 176, 180, 182], fill=(156, 108, 64)); d.rectangle([0, 182, 180, 184], fill=(112, 76, 44))
    for x in (20, 160): d.rectangle([x, 184, x + 3, 204], fill=(70, 70, 80))
    img = up(b)
    put(img, alfie(pose="sit", mouth="flat"), 10, 170, 1170, sh=False)
    put(img, dixon(pose="sit"), 10, 900, 1170, sh=False)
    put(img, hero(mouth="sad"), 15, 560, 1700)
    img.alpha_composite(ball(8), (760, 1630))
    banner(img); caption(img, W_("WITHOUT YOU,") + W_("WE DON'T", Y) + W_("WIN.", Y), spoken=5)
    return finish(img, "s2_locker.png")

# ------------------------------------------------------------------ 3. stadium, over-the-shoulder (ref ep.4)
def s_stadium():
    img = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
    crowd(img, 290, 700)
    img.paste(img.crop((0, 290, FW, 700)).filter(ImageFilter.GaussianBlur(1.3)), (0, 290))
    d = ImageDraw.Draw(img)
    for y in range(0, 290):
        t = y / 290
        d.line([(0, y), (FW, y)], fill=(int(8 + 10 * t), int(12 + 14 * t), int(30 + 26 * t)))
    adboard(img, 700, 46)
    b = lowres(180, 200); d = ImageDraw.Draw(b)
    stripes(d, 0, 200, 180, n=9)
    d.line([(0, 18), (180, 18)], fill=(236, 240, 236))
    d.line([(40, 18), (30, 44)], fill=(236, 240, 236)); d.line([(140, 18), (150, 44)], fill=(236, 240, 236))
    d.line([(30, 44), (150, 44)], fill=(236, 240, 236))
    img.paste(up(b), (0, 746))
    d = ImageDraw.Draw(img)
    # youth goal with net
    gx0, gx1, gy0, gy1 = 380, 700, 600, 856
    for x in range(gx0, gx1, 16): d.line([(x, gy0), (x, gy1)], fill=(210, 214, 220), width=2)
    for y in range(gy0, gy1, 16): d.line([(gx0, y), (gx1, y)], fill=(210, 214, 220), width=2)
    d.rectangle([gx0 - 10, gy0 - 10, gx1 + 10, gy0], fill=(250, 250, 250))
    d.rectangle([gx0 - 10, gy0, gx0, gy1], fill=(250, 250, 250)); d.rectangle([gx1, gy0, gx1 + 10, gy1], fill=(250, 250, 250))
    put(img, okafor(pose="ready"), 6, 540, 860)
    put(img, red(4, skin="dark", hair="black"), 6, 430, 950)
    put(img, red(5, skin="light", hair="brown"), 6, 660, 980)
    put(img, mason(), 8, 230, 1230)
    # the hero, huge, back to camera, cut by the frame
    put(img, hero(view="back", gloves=True, pose="ready"), 26, 610, 2200, sh=False)
    banner(img); caption(img, W_("AND") + W_("YOU", Y) + W_("STEP UP."), spoken=2)
    return finish(img, "s3_stadium.png")

# ------------------------------------------------------------------ 4. header clash close-up (ref ep.6 "couper")
def s_header():
    b = lowres(); d = ImageDraw.Draw(b)
    for y in range(150):
        t = y / 150; d.line([(0, y), (180, y)], fill=(int(70 + 60 * t), int(120 + 60 * t), int(190 + 30 * t)))
    trees(d, 150, 180); stripes(d, 150, 320, 180, n=8)
    d.line([(0, 230), (180, 200)], fill=(230, 236, 230)); d.line([(0, 300), (180, 262)], fill=(230, 236, 230))
    img = up(b).filter(ImageFilter.GaussianBlur(3.5))
    put(img, mason(eyes="closed", mouth="open"), 30, 210, 2080, rot=-22, sh=False)
    put(img, dixon(eyes="closed", mouth="open"), 30, 900, 2120, rot=20, sh=False)
    d = ImageDraw.Draw(img)
    cx, cy = 560, 760
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill=(255, 255, 255, 70))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(20)))
    d = ImageDraw.Draw(img)
    for a in range(0, 360, 24):
        r0, r1 = 120, 120 + (60 if a % 48 else 110)
        d.line([(cx + r0 * math.cos(math.radians(a)), cy + r0 * math.sin(math.radians(a))),
                (cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a)))], fill=(255, 255, 255), width=4)
    img.alpha_composite(ball(11), (cx - 55, cy - 55))
    for (sx, sy) in ((380, 640), (720, 620), (420, 820), (760, 880), (560, 560)):
        pts = [(sx + (26 if i % 2 == 0 else 11) * math.cos(math.radians(-90 + i * 36)),
                sy + (26 if i % 2 == 0 else 11) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
        d.polygon(pts, fill=Y, outline=(120, 80, 0))
    banner(img); caption(img, W_("HEADS") + W_("COLLIDE...", RED), spoken=2)
    return finish(img, "s4_header.png")

# ------------------------------------------------------------------ 5. bedroom at night (ref ep.10 phone)
def s_bedroom():
    b = lowres(); d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 180, 320], fill=(26, 34, 74))
    d.rectangle([0, 240, 180, 320], fill=(54, 40, 44))
    for x in range(0, 180, 14): d.line([(x, 240), (x, 320)], fill=(46, 34, 38))
    # window with city
    d.rectangle([98, 60, 172, 170], fill=(220, 224, 236)); d.rectangle([102, 64, 168, 166], fill=(12, 16, 40))
    for i in range(7):
        x = 104 + i * 9; h = rnd.randint(30, 70); d.rectangle([x, 166 - h, x + 7, 166], fill=(22, 28, 60))
        for wy in range(166 - h + 3, 164, 5):
            if rnd.random() < 0.5: d.point((x + 2 + rnd.randint(0, 3), wy), fill=(250, 210, 90))
    d.rectangle([134, 60, 136, 170], fill=(220, 224, 236))
    d.rectangle([90, 52, 98, 190], fill=(40, 80, 170)); d.rectangle([172, 52, 180, 190], fill=(40, 80, 170))
    # poster
    d.rectangle([14, 70, 64, 140], fill=(232, 232, 236)); d.rectangle([17, 73, 61, 137], fill=(44, 90, 190))
    # bed
    d.rectangle([0, 214, 120, 250], fill=(60, 110, 200)); d.rectangle([0, 206, 30, 220], fill=(240, 240, 244))
    d.rectangle([0, 250, 120, 258], fill=(90, 60, 40))
    img = up(b)
    # poster: grandad in his keeper days
    gp = grandad(mouth="smile")
    img.alpha_composite(big(gp, 9), (108 + 0, 440))
    put(img, hero(mouth="flat", pose="sit"), 13, 420, 1580)
    d = ImageDraw.Draw(img)
    # phone in hand glow
    d.rounded_rectangle([470, 1270, 540, 1390], 10, fill=(20, 20, 30), outline=(250, 250, 250), width=4)
    d.rectangle([480, 1282, 530, 1378], fill=(120, 200, 255))
    banner(img); caption(img, W_("THEN YOUR") + W_("PHONE", BLUE) + W_("LIGHTS UP."), spoken=3)
    return finish(img, "s5_bedroom.png")

# ------------------------------------------------------------------ 6. ending: two option cards (ref ep.10 / ep.6)
def s_ending():
    img = navy_bg(); d = ImageDraw.Draw(img)
    d.rounded_rectangle([170, 600, 910, 680], 40, fill=(10, 14, 34), outline=(220, 224, 240), width=4)
    d.text((215, 640), "STAY|", font=font(800, 40), fill=Y, anchor="lm")
    cards = [(130, Y, "STAY", "fight Dixon for the shirt", "stadium"), (570, TEAL, "LEAVE", "loan to a smaller club", "train")]
    for x, col, lab, sub, kind in cards:
        cw, ch, cy = 380, 470, 760
        card = Image.new("RGBA", (cw, ch))
        if kind == "stadium":
            crowd(card, 0, 210); adboard(card, 210, 32)
            cd = ImageDraw.Draw(card); stripes(cd, 234, ch, cw, n=6)
            put(card, hero(gloves=True, pose="ready"), 9, cw / 2 - 40, ch - 30)
            put(card, dixon(), 8, cw / 2 + 110, ch - 60)
        else:
            cd = ImageDraw.Draw(card)
            for y in range(240): cd.line([(0, y), (cw, y)], fill=(130, 186, 230))
            cd.rectangle([0, 200, cw, 240], fill=(48, 110, 62))
            stripes(cd, 240, ch, cw, n=6)
            put(card, hero(pose="wave", mouth="smile"), 9, cw / 2 - 40, ch - 30)
            put(card, coach(), 8, cw / 2 + 120, ch - 60)
        m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw, ch], 22, fill=255)
        img.paste(card, (x, cy), m)
        d.rounded_rectangle([x - 3, cy - 3, x + cw + 3, cy + ch + 3], 24, outline=col, width=8)
        d.text((x + cw / 2, cy + ch + 60), lab, font=font(800, 52), fill=col, anchor="mm")
        d.text((x + cw / 2, cy + ch + 110), sub.upper(), font=font(700, 22), fill=(180, 190, 220), anchor="mm")
    banner(img)
    caption(img, W_("WRITE") + W_("STAY", Y) + W_("OR") + W_("LEAVE", TEAL) + W_("IN THE COMMENTS."), spoken=8)
    return finish(img, "s6_ending.png")

# ------------------------------------------------------------------ cast sheet
def s_cast():
    img = navy_bg(); d = ImageDraw.Draw(img)
    d.text((FW / 2, 90), "FROM ZERO TO LEGEND", font=font(800, 34), fill=Y, anchor="mm")
    d.text((FW / 2, 160), "THE CAST", font=font(800, 86), fill=(255, 255, 255), anchor="mm")
    d.text((FW / 2, 225), "redrawn in the reference sprite style", font=font(600, 28), fill=(190, 198, 226), anchor="mm")
    rows = [
        [(hero(), "HERO #0", "keeper · 11"), (hero(view="back", gloves=True), "HERO", "back"),
         (hero(pose="ready", gloves=True), "HERO", "ready"), (hero(pose="celebrate", gloves=True, mouth="grin"), "HERO", "joy")],
        [(grandad(mouth="smile"), "GRANDAD", "ex-keeper"), (mum(mouth="smile"), "MUM", ""),
         (coach(mouth="open"), "COACH", ""), (alfie(mouth="grin"), "ALFIE #7", "best friend")],
        [(mason(mouth="grin"), "MASON #9", "rival striker"), (okafor(), "OKAFOR #1", "first keeper"),
         (dixon(), "DIXON #2", "rival keeper"), (red(4, skin="dark", hair="black"), "#4", "defender")],
    ]
    for r, row in enumerate(rows):
        for c, (s, lab, sub) in enumerate(row):
            x, y, w, h = 30 + c * 258, 290 + r * 530, 246, 510
            d.rounded_rectangle([x, y, x + w, y + h], 20, fill=(14, 20, 50), outline=(70, 92, 160), width=3)
            put(img, s, 8, x + w / 2, y + h - 110)
            d = ImageDraw.Draw(img)
            d.text((x + w / 2, y + h - 68), lab, font=font(800, 30), fill=Y, anchor="mm")
            d.text((x + w / 2, y + h - 32), sub.upper(), font=font(700, 18), fill=(200, 206, 230), anchor="mm")
    return finish(img, "s0_cast.png")

if __name__ == "__main__":
    for f in (s_cast, s_training, s_locker, s_stadium, s_header, s_bedroom, s_ending):
        f(); print(f.__name__)
