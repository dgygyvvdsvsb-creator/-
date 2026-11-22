"""'remi_sport' style engine for From Zero to Legend (EP5 on).
Tiny pixel sprites (18x30) scaled up with NEAREST, 1-px dark outline, one shadow tone;
smooth simple backgrounds; glow/impact FX; big Poppins captions."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

FW, FH, FPS = 720, 1280, 30
FONTDIR = "/tmp/claude-0/-home-user--/67093071-fe87-56fe-a818-3433aa12d626/scratchpad/fonts/"
OL = (22, 18, 28)

SKIN = {"light": ((240, 196, 160), (214, 164, 128)), "tan": ((205, 150, 110), (176, 122, 86)),
        "brown": ((150, 98, 66), (120, 74, 48)), "dark": ((104, 66, 46), (82, 50, 34)),
        "old": ((236, 192, 158), (206, 164, 132))}
HAIR = {"dark": (52, 36, 30), "black": (26, 22, 24), "blond": (240, 204, 96), "ginger": (214, 104, 40),
        "white": (240, 240, 246), "brown": (110, 70, 40), "grey": (150, 150, 160)}


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def spring(t, k=12.0, damp=6.0):
    return 0.0 if t <= 0 else 1 - math.exp(-damp * t) * math.cos(k * t)


def shade(c, k=0.78):
    return tuple(int(v * k) for v in c)


# ------------------------------------------------------------------ sprites
class Kit:
    def __init__(self, shirt, shorts, socks, number=None, num_col=(250, 250, 250), gloves=None, sleeve=None):
        self.shirt, self.shorts, self.socks = shirt, shorts, socks
        self.number, self.num_col, self.gloves = number, num_col, gloves
        self.sleeve = sleeve or shirt


DIGITS = {  # 3x5 pixel digits
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
}


def _num(d, x, y, n, col):
    for i, ch in enumerate(str(n)):
        g = DIGITS.get(ch)
        if not g:
            continue
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "1":
                    d.point((x + i * 4 + c, y + r), fill=col)


def outline(im, col=OL):
    """1-px outline around opaque pixels (8-neighbour dilation)"""
    a = np.array(im.split()[3]) > 0
    p = np.pad(a, 1)
    dil = np.zeros_like(a)
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            dil |= p[dy:dy + a.shape[0], dx:dx + a.shape[1]]
    ring = dil & ~a
    arr = np.array(im)
    arr[ring] = col + (255,)
    return Image.fromarray(arr, "RGBA")


def person(kit=None, skin="light", hair="dark", style="short", pose="stand", view="front", phase=0.0,
           blink=False, mouth="flat", look=0, gloves=False, bracelet=False, extra=None):
    """returns an RGBA sprite (W=24 x H=34 incl. 3px margin) with outline. extra: list of callables(d)"""
    W, H = 24, 39
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sk, skd = SKIN[skin]
    hc = HAIR[hair]
    kit = kit or Kit((60, 120, 200), (30, 34, 50), (60, 120, 200))
    ox, oy = 3, 10  # margin so outline/limbs fit
    R = lambda x0, y0, x1, y1, c: d.rectangle([ox + x0, oy + y0, ox + x1, oy + y1], fill=c)
    P = lambda x, y, c: d.point((ox + x, oy + y), fill=c)

    # ---------------- legs
    def legs(sit=False):
        if pose == "run":
            s = math.sin(phase * math.tau)
            off = int(round(s * 2))
            for lx, o in ((5, off), (10, -off)):
                R(lx, 18 + max(0, -o) // 2, lx + 2, 21, sk)
                R(lx + o // 2, 22, lx + 2 + o // 2, 25 - max(0, o) // 2, kit.socks)
                R(lx - 1 + o // 2, 26 - max(0, o) // 2, lx + 2 + o // 2, 27 - max(0, o) // 2, OL)
        elif pose == "kick":
            R(5, 18, 7, 21, sk); R(5, 22, 7, 25, kit.socks); R(4, 26, 7, 27, OL)
            k = phase  # 0 back .. 1 through
            ang = lerp(-0.9, 1.1, k)
            for i in range(9):
                x = 11 + math.sin(ang) * i
                y = 18 + math.cos(ang) * i
                c = sk if i < 4 else (kit.socks if i < 8 else OL)
                R(int(x) - 1, int(y), int(x) + 1, int(y), c)
        elif pose == "kickL":   # strikes with the screen-LEFT leg (player's left foot when seen from behind)
            R(10, 18, 12, 21, sk); R(10, 22, 12, 25, kit.socks); R(10, 26, 13, 27, OL)
            k = phase
            ang = lerp(-0.9, 1.1, k)
            for i in range(9):
                x = 6 - math.sin(ang) * i
                y = 18 + math.cos(ang) * i
                c = sk if i < 4 else (kit.socks if i < 8 else OL)
                R(int(x) - 1, int(y), int(x) + 1, int(y), c)
        elif sit or pose in ("sit", "hurt"):
            R(5, 18, 7, 20, kit.shorts); R(10, 18, 12, 20, kit.shorts)
            R(5, 21, 7, 23, sk); R(10, 21, 12, 23, sk)
            R(5, 24, 7, 25, kit.socks); R(10, 24, 12, 25, kit.socks)
            R(4, 26, 7, 26, OL); R(10, 26, 13, 26, OL)
        else:
            spread = 1 if pose in ("ready", "celebrate") else 0
            for lx in (5 - spread, 10 + spread):
                R(lx, 18, lx + 2, 21, sk)
                R(lx, 22, lx + 2, 25, kit.socks)
                R(lx, 23, lx + 2, 23, shade(kit.socks, 0.85))
                R(lx - (1 if lx < 8 else 0), 26, lx + 2 + (1 if lx > 8 else 0), 27, OL)
                R(lx, 26, lx + 2, 26, (60, 60, 70))

    legs()
    # shorts
    if pose not in ("sit", "hurt"):
        R(4, 15, 13, 18, kit.shorts)
        R(11, 15, 13, 18, shade(kit.shorts))
        R(8, 17, 9, 18, shade(kit.shorts, 0.7))
    # torso
    R(3, 8, 14, 15, kit.shirt)
    R(12, 8, 14, 15, shade(kit.shirt))
    R(6, 8, 11, 8, shade(kit.shirt, 0.6))  # collar
    if view == "back" and kit.number is not None:
        _num(d, ox + 9 - 2 * len(str(kit.number)), oy + 9, kit.number, kit.num_col)
    elif view == "front" and kit.number is not None:
        _num(d, ox + 6, oy + 10, kit.number, kit.num_col) if False else None
        # small number on the chest
        g = str(kit.number)
        _num(d, ox + 9, oy + 10, g[-1], kit.num_col)
    # arms
    def arm(side, hx, hy):
        sx = 2 if side < 0 else 15
        sy = 9
        steps = max(abs(hx - sx), abs(hy - sy), 1)
        for i in range(steps + 1):
            x = round(lerp(sx, hx, i / steps))
            y = round(lerp(sy, hy, i / steps))
            c = kit.sleeve if i < steps * 0.35 else sk
            R(x - (1 if side < 0 else 0), y, x + (0 if side < 0 else 1), y, c)
        if gloves:
            R(hx - 2, hy - 1, hx + 1, hy + 2, (252, 140, 27))
            R(hx - 2, hy + 2, hx + 1, hy + 2, (206, 98, 14))
        else:
            R(hx - 1, hy, hx, hy + 1, sk)
        if bracelet and ((side < 0 and view == "front") or (side > 0 and view == "back")):
            # hero's RIGHT wrist: screen-left in front view, screen-right in back view
            bx = round(lerp(sx, hx, 0.75))
            by = round(lerp(sy, hy, 0.75))
            R(bx - 1, by, bx + 1, by, (225, 30, 40))

    if pose == "hurt":
        arm(-1, 5, 20); arm(1, 11, 20)
    elif pose in ("stand", "sit"):
        arm(-1, 1, 15); arm(1, 16, 15)
    elif pose == "run":
        s = math.sin(phase * math.tau)
        arm(-1, 1, 13 + int(s * 2)); arm(1, 16, 13 - int(s * 2))
    elif pose == "ready":
        arm(-1, -1, 11); arm(1, 18, 11)
    elif pose in ("celebrate", "dive"):
        arm(-1, 2, 1); arm(1, 15, 1)
    elif pose == "reach":   # arms stretched far beyond the head (flying save)
        arm(-1, 5, -7); arm(1, 12, -7)
    elif pose == "kick":
        arm(-1, -1, 12); arm(1, 17, 13)
    elif pose == "kickL":
        arm(-1, 0, 13); arm(1, 18, 12)
    elif pose == "catch":
        arm(-1, 6, 12); arm(1, 11, 12)
    elif pose == "whisper":
        arm(-1, 1, 15); arm(1, 11, 6)
    elif pose == "phone":
        arm(-1, 6, 12); arm(1, 11, 12)
        R(7, 10, 10, 13, (30, 32, 44)); R(8, 11, 9, 12, (120, 190, 255))
    # head
    R(4, 0, 13, 7, sk)
    R(11, 1, 13, 7, skd)
    if view == "front":
        # hair styles
        if style == "short":
            R(4, -1, 13, 1, hc); R(4, 2, 4, 3, hc); R(13, 2, 13, 3, hc); R(7, 2, 8, 2, hc)
        elif style == "curly":
            R(3, -2, 14, 1, hc); R(2, 1, 3, 5, hc); R(14, 1, 15, 5, hc)
            for x in range(2, 16, 2):
                R(x, -4, x, -3, hc)            # bumpy curly top
            for x in range(3, 15, 2):
                P(x, -3, hc)
            for y in range(1, 6, 2):
                P(1, y, hc); P(16, y, hc)       # curls on the sides
            for x in (5, 9, 12):
                P(x, -1, shade(hc, 1.35))       # curl highlights
        elif style == "spiky":
            R(4, -1, 13, 1, hc); R(4, 2, 4, 2, hc); R(13, 2, 13, 2, hc)
            for x in (4, 7, 10, 13):
                R(x, -3, x + 1, -2, hc)
        elif style == "bald":
            R(3, 2, 4, 5, hc); R(13, 2, 14, 5, hc); R(5, 0, 8, 0, (250, 220, 196))
        elif style == "pony":
            R(4, -1, 13, 1, hc); R(3, 1, 4, 6, hc); R(13, 1, 14, 6, hc); R(14, 4, 15, 9, hc)
        elif style == "cap":   # proper football cap: rounded crown, club logo, brim over the eyes
            NAVY, NAVY_D = (34, 46, 96), (22, 30, 66)
            R(4, -3, 13, -3, NAVY); R(3, -2, 14, 1, NAVY); R(11, -2, 14, 1, NAVY_D)
            R(8, -2, 9, -1, (250, 206, 40))                       # club badge
            R(2, 1, 15, 2, NAVY_D)                                # brim
            R(4, 3, 4, 4, hc); R(13, 3, 13, 4, hc)                # grey sideburns
        # face
        ey = 3
        if blink:
            R(6 + look, ey + 1, 6 + look, ey + 1, OL); R(10 + look, ey + 1, 10 + look, ey + 1, OL)
        else:
            for ex in (6, 10):
                P(ex + look, ey, (250, 250, 250)); P(ex + look, ey + 1, OL)
        R(5, ey - 1, 7, ey - 1, shade(hc, 0.8) if style != "bald" else (200, 200, 210))
        R(9, ey - 1, 11, ey - 1, shade(hc, 0.8) if style != "bald" else (200, 200, 210))
        if mouth == "open":
            R(7, 5, 9, 6, (150, 40, 50))
        elif mouth == "smile":
            R(7, 6, 9, 6, (150, 40, 50)); P(6, 5, (150, 40, 50)); P(10, 5, (150, 40, 50))
        elif mouth == "grin":
            R(6, 5, 10, 6, (150, 40, 50)); R(7, 5, 9, 5, (250, 250, 250))
        elif mouth == "sad":
            R(7, 5, 9, 5, (150, 40, 50)); P(6, 6, (150, 40, 50)); P(10, 6, (150, 40, 50))
        else:
            R(7, 6, 9, 6, (170, 80, 80))
    else:  # back of the head
        R(4, -1, 13, 6, hc)
        R(4, 6, 13, 7, skd)
        if style == "curly":
            R(3, -2, 14, 6, hc)
            for x in range(2, 16, 2):
                R(x, -4, x, -3, hc)
            for y in range(0, 7, 2):
                P(2, y, hc); P(15, y, hc)
            for x in (5, 9, 12):
                P(x, 1, shade(hc, 1.35)); P(x - 1, 4, shade(hc, 1.35))
        if style == "bald":
            R(5, -1, 12, 3, sk)
    if extra:
        for fn in extra:
            fn(d, ox, oy)
    im = outline(im)
    if pose in ("dive", "lying"):
        im = im.rotate(-90 if pose == "lying" else -70, resample=Image.NEAREST, expand=True)
    return im


def grandad(pose="sit", blink=False, mouth="smile", tube=False, look=0):
    """Grandad: bald top, white side hair, glasses, full white beard, brown cardigan, cane."""
    card = Kit((150, 98, 58), (70, 70, 80), (70, 70, 80))

    def details(d, ox, oy):
        P = lambda x, y, c: d.point((ox + x, oy + y), fill=c)
        R = lambda x0, y0, x1, y1, c: d.rectangle([ox + x0, oy + y0, ox + x1, oy + y1], fill=c)
        R(5, 5, 12, 8, (245, 243, 248))           # beard
        R(6, 8, 11, 9, (245, 243, 248))
        R(12, 5, 12, 8, (210, 210, 222))
        R(8, 4, 9, 4, (200, 150, 120))            # nose
        if mouth == "open":
            R(7, 6, 9, 7, (150, 40, 50))
        elif mouth == "smile":
            R(7, 7, 9, 7, (150, 40, 50))
        # glasses
        for ex in (5, 9):
            R(ex, 2, ex + 2, 3, (60, 60, 76))
        if not blink:
            P(6 + look, 3, (250, 250, 250)); P(10 + look, 3, (250, 250, 250))
        if tube:  # nasal cannula: under the nose, over both ears, down to the chest
            pass  # cannula is drawn thin at full resolution by the scene
        for y in (10, 12, 14):
            P(8, y, (240, 206, 120))  # buttons
        R(8, 9, 9, 9, (238, 232, 214))
    if tube:
        SKIN["ill"] = ((222, 190, 168), (196, 164, 146))
    im = person(card, skin="ill" if tube else "old", hair="white", style="bald", pose="sit" if pose == "sit" else "stand",
                blink=blink, mouth="flat", extra=[details])
    return im


def cane(h=18):
    im = Image.new("RGBA", (6, h + 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([3, 3, 3, h + 2], fill=(130, 80, 38))
    d.rectangle([1, 1, 3, 1], fill=(130, 80, 38))
    d.point((1, 2), fill=(130, 80, 38))
    return outline(im)


def ball_sprite():
    """round pixel ball 13x13 with black patches"""
    n = 13
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    px = im.load()
    c = (n - 1) / 2
    for y in range(n):
        for x in range(n):
            if (x - c) ** 2 + (y - c) ** 2 <= (c + 0.35) ** 2:
                px[x, y] = (250, 250, 250, 255)
    for x, y in ((6, 5), (5, 6), (6, 6), (7, 6), (5, 7), (6, 7), (7, 7)):   # centre patch
        px[x, y] = OL + (255,)
    for x, y in ((2, 4), (2, 5), (10, 4), (10, 5), (4, 10), (5, 10), (8, 10), (7, 10), (6, 1), (5, 1), (7, 1)):
        px[x, y] = (60, 60, 70, 255)
    for x, y in ((3, 3), (4, 3), (3, 2)):  # shine
        px[x, y] = (255, 255, 255, 255)
    return outline(im)


def big(sprite, scale):
    return sprite.resize((sprite.width * scale, sprite.height * scale), Image.NEAREST)


def paste(img, sprite, scale, cx, by, rot=0, alpha=1.0):
    """paste a sprite scaled with NEAREST, anchored at bottom-centre (cx, by) in full-res coords"""
    s = big(sprite, max(1, int(scale)))
    if rot:
        s = s.rotate(rot, resample=Image.NEAREST, expand=True)
    if alpha < 1:
        a = s.split()[3].point(lambda v: int(v * alpha))
        s.putalpha(a)
    img.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height)))
    return s


def shadow(img, cx, y, w, h=None, a=90):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    h = h or w * 0.22
    d.ellipse([cx - w / 2, y - h / 2, cx + w / 2, y + h / 2], fill=(0, 0, 0, a))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(4)))


# ------------------------------------------------------------------ cast (series anchors)
def hero(**kw):
    kw.setdefault("bracelet", True)
    return person(Kit((40, 168, 74), (245, 245, 250), (40, 168, 74), 0), skin="light", hair="dark",
                  style="short", **kw)


def mason(**kw):
    return person(Kit((210, 52, 56), (245, 245, 250), (210, 52, 56), 9), skin="light", hair="blond",
                  style="spiky", **kw)


def okafor(**kw):
    return person(Kit((246, 206, 40), (30, 30, 36), (246, 206, 40), 1, num_col=(30, 30, 36)), skin="dark",
                  hair="black", style="short", **{"gloves": True, **kw})


def dixon(**kw):
    return person(Kit((60, 120, 210), (30, 34, 50), (60, 120, 210), 2), skin="tan", hair="brown",
                  style="curly", **{"gloves": True, **kw})


def coach(**kw):
    return person(Kit((30, 40, 80), (30, 40, 80), (30, 30, 36)), skin="light", hair="grey", style="cap", **kw)


# ------------------------------------------------------------------ backgrounds
_cache = {}


def sky_trees(top=(120, 170, 220), bot=(186, 214, 236), tree=(44, 104, 60), rain=False, key="day"):
    if key in _cache:
        return _cache[key].copy()
    img = Image.new("RGB", (FW, FH))
    d = ImageDraw.Draw(img)
    for y in range(FH):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, clamp(y / 700))) for a, b in zip(top, bot)))
    ov = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    rng = random.Random(3)
    for i in range(16):
        x = rng.uniform(-60, FW + 60)
        r = rng.uniform(90, 150)
        od.ellipse([x - r, 330 - r * 0.8, x + r, 330 + r], fill=tree + (255,))
    for i in range(14):
        x = rng.uniform(-60, FW + 60)
        r = rng.uniform(60, 110)
        od.ellipse([x - r, 380 - r * 0.6, x + r, 380 + r], fill=shade(tree, 0.82) + (255,))
    img.paste(ov.filter(ImageFilter.GaussianBlur(5)), (0, 0), ov.filter(ImageFilter.GaussianBlur(5)))
    _cache[key] = img
    return img.copy()


def crowd_band(img, y0, y1, seed=1, blur=2.5, cols=None):
    """distant stand: rows of tiny pixel fans (blurred)"""
    cols = cols or [(40, 168, 74), (210, 52, 56), (240, 240, 245), (40, 90, 200), (246, 206, 40)]
    lay = Image.new("RGBA", (FW // 4, (y1 - y0) // 4 + 1), (60, 50, 70, 255))
    d = ImageDraw.Draw(lay)
    rng = random.Random(seed)
    for ry in range(0, lay.height, 4):
        d.rectangle([0, ry + 3, lay.width, ry + 3], fill=(150, 46, 62))
        for x in range(rng.randint(0, 2), lay.width, 3):
            if rng.random() < 0.8:
                d.rectangle([x, ry + 1, x + 1, ry + 2], fill=rng.choice(cols))
                d.point((x, ry), fill=rng.choice(list(SKIN.values()))[0])
    lay = lay.resize((FW, lay.height * 4), Image.NEAREST).filter(ImageFilter.GaussianBlur(blur))
    img.paste(lay, (0, y0))


def pitch(img, y0, stripes=10, c1=(58, 150, 72), c2=(52, 138, 66), lines=True, diag=0.0):
    d = ImageDraw.Draw(img)
    i = 0
    while True:
        y = y0 + (i ** 1.25) * 9
        y2 = y0 + ((i + 1) ** 1.25) * 9
        d.rectangle([0, y, FW, y2], fill=c1 if i % 2 else c2)
        if y2 > FH:
            break
        i += 1
    if lines:
        d.line([(-50, y0 + 40), (FW + 50, y0 + 40 + diag * FW)], fill=(236, 244, 236), width=5)


def adboards(img, y, h=34):
    d = ImageDraw.Draw(img)
    cols = [(210, 52, 56), (40, 90, 200), (246, 206, 40), (40, 150, 80)]
    labs = ["RIVERSIDE", "PIE SHOP", "BUS 42", "GO KEEPERS"]
    f = font(800, 20)
    for k in range(6):
        x = k * 150 - 40
        d.rectangle([x, y, x + 150, y + h], fill=cols[k % 4])
        d.text((x + 75, y + h / 2), labs[k % 4], font=f, fill=(255, 255, 255), anchor="mm")


def goal(img, cx, by, w, h, depth=0.18):
    d = ImageDraw.Draw(img)
    x0, x1 = cx - w / 2, cx + w / 2
    net = Image.new("RGBA", img.size, (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    nd.rectangle([x0, by - h, x1, by], fill=(255, 255, 255, 40))
    step = max(8, w / 22)
    x = x0
    while x <= x1:
        nd.line([(x, by - h), (x, by)], fill=(255, 255, 255, 120), width=2)
        x += step
    y = by - h
    while y <= by:
        nd.line([(x0, y), (x1, y)], fill=(255, 255, 255, 120), width=2)
        y += step
    img.alpha_composite(net)
    pw = max(5, int(w / 40))
    for xx in (x0, x1 - pw):
        d.rectangle([xx - 2, by - h - 2, xx + pw + 2, by], fill=OL)
        d.rectangle([xx, by - h, xx + pw, by], fill=(250, 250, 252))
    d.rectangle([x0 - 2, by - h - 2, x1 + 2, by - h + pw + 2], fill=OL)
    d.rectangle([x0, by - h, x1, by - h + pw], fill=(250, 250, 252))


# ------------------------------------------------------------------ FX
def glow_ring(img, x, y, r, a=0.8, col=(255, 255, 255)):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(8, 0, -1):
        rr = r * i / 8
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (int(255 * a * (1 - i / 9) * 0.35),))
    d.ellipse([x - r, y - r, x + r, y + r], outline=col + (int(255 * a),), width=6)
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(3)))


def speed_lines(img, t, cx, cy, n=22, a=110, r0=260, r1=640):
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(int(t * 24))
    for _ in range(n):
        ang = rng.uniform(0, math.tau)
        ra = rng.uniform(r0, r0 + 120)
        rb = rng.uniform(r1, r1 + 200)
        d.line([(cx + math.cos(ang) * ra, cy + math.sin(ang) * ra), (cx + math.cos(ang) * rb, cy + math.sin(ang) * rb)],
               fill=(255, 255, 255, a), width=4)


def impact_lines(img, x, y, t0, t, n=10):
    k = clamp((t - t0) / 0.25)
    if k <= 0 or k >= 1:
        return
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(n):
        ang = i / n * math.tau
        ra, rb = 40 + 80 * k, 90 + 140 * k
        d.line([(x + math.cos(ang) * ra, y + math.sin(ang) * ra), (x + math.cos(ang) * rb, y + math.sin(ang) * rb)],
               fill=(255, 255, 255, int(230 * (1 - k))), width=5)


def flash(img, a, col=(255, 255, 255)):
    if a <= 0:
        return img
    return Image.blend(img.convert("RGB"), Image.new("RGB", img.size, col), clamp(a)).convert("RGBA")


def rain(img, t, a=70, n=120):
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(5)
    for _ in range(n):
        x, y, s = rng.uniform(0, FW), rng.uniform(0, FH), rng.uniform(0.6, 1)
        yy = (y + t * 1000 * s) % FH
        xx = (x - yy * 0.1) % FW
        d.line([(xx, yy), (xx - 3, yy + 26 * s)], fill=(220, 230, 255, int(a * s)), width=2)


def cam(img, zoom=1.0, cx=FW / 2, cy=FH / 2, dx=0, dy=0, rot=0):
    if rot:
        img = img.rotate(rot, resample=Image.BILINEAR, center=(cx, cy))
    if zoom == 1 and not dx and not dy:
        return img
    nw, nh = FW / zoom, FH / zoom
    x0 = cx - nw * (cx / FW) - dx / zoom
    y0 = cy - nh * (cy / FH) - dy / zoom
    return img.transform((FW, FH), Image.EXTENT, (x0, y0, x0 + nw, y0 + nh), Image.BILINEAR)


def shake(t, t0, dur=0.25, amp=10):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        return math.sin(t * 90) * amp * k, math.cos(t * 70) * amp * k
    return 0, 0


# ------------------------------------------------------------------ text / UI
_f = {}


def font(w, s):
    if (w, s) not in _f:
        _f[(w, s)] = ImageFont.truetype(FONTDIR + f"Poppins-{w}.ttf", s)
    return _f[(w, s)]


C_W, C_Y, C_R, C_B, C_G, C_O = (250, 250, 250), (250, 206, 40), (240, 80, 80), (92, 196, 252), (110, 222, 120), (252, 150, 40)
C_DIM = (150, 156, 175)


def banner(img, ep):
    d = ImageDraw.Draw(img)
    f = font(600, 19)
    a, b = f"EP. {ep} · FROM ZERO TO ", "LEGEND"
    wa, wb = d.textlength(a, font=f), d.textlength(b, font=f)
    x = (FW - wa - wb) / 2
    for txt, col, xx in ((a, (240, 240, 245), x), (b, C_Y, x + wa)):
        d.text((xx, 62), txt, font=f, fill=col, stroke_width=3, stroke_fill=OL)


def caption(img, words, t, wrap=600, y=108, size=50):
    if not words:
        return
    d = ImageDraw.Draw(img)
    f = font(800, size)
    sp = d.textlength(" ", font=f)
    lines, cur, cw = [], [], 0
    for w in words:
        ww = d.textlength(w[0], font=f)
        if cur and cw + sp + ww > wrap:
            lines.append(cur); cur, cw = [], 0
        cw += (sp if cur else 0) + ww
        cur.append((w, ww))
    lines.append(cur)
    for ln in lines:
        tot = sum(ww for _, ww in ln) + sp * (len(ln) - 1)
        x = (FW - tot) / 2
        for (txt, st, col), ww in ln:
            d.text((x, y), txt, font=f, fill=col if t >= st else C_DIM, stroke_width=7, stroke_fill=OL)
            x += ww + sp
        y += size + 6


NO_TAGS = {"YOU", "MASON · #9", "OKAFOR · 12", "DIXON · KEEPER #2", "YOU · 11 · NO. 3", "+1 HEAD"}  # no labels over players


def pill(img, x, y, text, bg, k=1.0, size=30, fg=(255, 255, 255), border=OL):
    if text in NO_TAGS:
        return
    if k <= 0.02:
        return
    d = ImageDraw.Draw(img)
    f = font(800, max(6, int(size * k)))
    w = d.textlength(text, font=f)
    h = size * k
    d.rounded_rectangle([x - w / 2 - 18 * k, y - h * .78, x + w / 2 + 18 * k, y + h * .78], int(12 * k),
                        fill=bg, outline=border, width=4)
    d.text((x, y), text, font=f, fill=fg, anchor="mm")


def bubble(img, x, y, text, k=1.0, size=30, tail="down"):
    """speech bubbles are banned (user rule): dialogue goes in the captions only"""
    return
    if k <= 0.02:
        return
    d = ImageDraw.Draw(img)
    f = font(800, int(size * k))
    lines = text.split("\n")
    w = max(d.textlength(l, font=f) for l in lines) + 36 * k
    h = (size * 1.2 * len(lines) + 24) * k
    x0, y0 = x - w / 2, y - h
    d.rounded_rectangle([x0 - 4, y0 - 4, x0 + w + 4, y0 + h + 4], int(16 * k), fill=OL)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(14 * k), fill=(252, 252, 252))
    if tail == "down":
        d.polygon([(x - 14 * k, y0 + h), (x + 14 * k, y0 + h), (x, y0 + h + 22 * k)], fill=(252, 252, 252), outline=OL)
    for i, l in enumerate(lines):
        d.text((x, y0 + 12 * k + i * size * 1.2 * k + size * 0.6 * k), l, font=f, fill=OL, anchor="mm")


def score_bar(img, y, left, right, score, minute=None, k=1.0):
    if k <= 0.02:
        return
    d = ImageDraw.Draw(img)
    w = 440 * k
    x0 = FW / 2 - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + 60], 16, fill=(16, 18, 36), outline=C_Y, width=4)
    f = font(800, 28)
    d.rectangle([x0 + 14, y + 14, x0 + 44, y + 46], fill=(40, 168, 74), outline=OL, width=3)
    d.rectangle([x0 + w - 44, y + 14, x0 + w - 14, y + 46], fill=(210, 52, 56), outline=OL, width=3)
    d.text((FW / 2, y + 30), f"{left}  {score}  {right}", font=f, fill=(255, 255, 255), anchor="mm")
    if minute:
        d.rounded_rectangle([FW / 2 - 50, y + 62, FW / 2 + 50, y + 96], 8, fill=(210, 52, 56))
        d.text((FW / 2, y + 79), minute, font=font(800, 22), fill=(255, 255, 255), anchor="mm")


def draw_ball(img, cx, by, size):
    """smooth round football at full resolution (anti-aliased), bottom-centre anchored like paste()"""
    r = size * 6.5
    S = 4
    n = int(r * 2 + 12)
    lay = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = n * S / 2
    R_ = r * S
    d.ellipse([c - R_ - 3 * S, c - R_ - 3 * S, c + R_ + 3 * S, c + R_ + 3 * S], fill=OL)
    d.ellipse([c - R_, c - R_, c + R_, c + R_], fill=(250, 250, 250))
    d.regular_polygon((c, c, R_ * 0.33), 5, rotation=0, fill=OL)
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5
        px, py = c + math.cos(a) * R_ * 0.82, c + math.sin(a) * R_ * 0.82
        d.regular_polygon((px, py, R_ * 0.22), 5, rotation=180, fill=(50, 50, 60))
    d.ellipse([c - R_ * 0.6, c - R_ * 0.7, c - R_ * 0.25, c - R_ * 0.4], fill=(255, 255, 255))
    mask = Image.new("L", lay.size, 0)
    ImageDraw.Draw(mask).ellipse([c - R_ - 3 * S, c - R_ - 3 * S, c + R_ + 3 * S, c + R_ + 3 * S], fill=255)
    lay.putalpha(Image.composite(lay.split()[3], Image.new("L", lay.size, 0), mask))
    lay = lay.resize((n, n), Image.LANCZOS)
    img.alpha_composite(lay, (int(cx - n / 2), int(by - n / 2 - r)))
