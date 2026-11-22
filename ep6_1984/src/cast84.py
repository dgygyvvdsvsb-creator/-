"""1984 cast + the old stadium + VHS look."""
from cast4 import *
from persp import *
from persp import _c

KIN = (236, 170, 40)         # Kingston: amber shirts, black shorts (fictional crest: black K on amber)
NEW = (46, 92, 196)          # Newcastle (fictional colours): royal blue, white shorts, castle crest
KEEPER_G = (34, 128, 66)     # Grandad's 1984 keeper jersey: green, like yours today
MUD, MUD_D = (112, 84, 56), (90, 66, 44)


def young_grandad(**kw):
    """Grandad at 22: dark hair, 80s moustache, green #1 jersey, orange gloves, red string on the right wrist"""
    def tash(d, ox, oy):
        R = lambda x0, y0, x1, y1, c: d.rectangle([ox + x0, oy + y0, ox + x1, oy + y1], fill=c)
        R(6, 5, 11, 5, HAIR["dark"])           # moustache
        R(4, 3, 4, 5, HAIR["dark"]); R(13, 3, 13, 5, HAIR["dark"])   # sideburns
    kw.setdefault("gloves", True)
    kw.setdefault("bracelet", True)
    view = kw.get("view", "front")
    ex = [tash] if view == "front" else []
    return person(Kit(KEEPER_G, (30, 30, 36), KEEPER_G, 1), skin="light", hair="dark", style="short", extra=ex, **kw)


def young_coach(**kw):
    """the coach at 20: short 80s perm with a white headband (red stripe), Newcastle blue #9"""
    HC, HL, HD = (74, 48, 30), (120, 82, 50), (52, 32, 20)
    view = kw.get("view", "front")

    def perm(d, ox, oy):
        R = lambda x0, y0, x1, y1, c: d.rectangle([ox + x0, oy + y0, ox + x1, oy + y1], fill=c)
        P = lambda x, y, c: d.point((ox + x, oy + y), fill=c)
        R(3, -3, 14, 1, HC)
        for x in range(3, 15, 2):
            P(x, -4, HC); P(x + 1, -3, HL)
        R(2, 1, 3, 6, HC); R(14, 1, 15, 6, HC)
        for y in (2, 4):
            P(2, y, HL); P(15, y, HD)
        if view == "front":
            R(4, 0, 13, 1, (250, 250, 250)); R(4, 1, 13, 1, (220, 40, 50))
        else:
            R(3, 1, 14, 7, HC); R(3, 0, 14, 1, (250, 250, 250))
    return person(Kit(NEW, (245, 245, 250), NEW, 9), skin="light", hair="brown", style="none", extra=[perm], **kw)


def kingston(n, **kw):
    sk = {4: "tan", 5: "light", 6: "brown", 8: "light", 10: "dark"}.get(n, "light")
    hr = {4: "black", 5: "ginger", 6: "black", 8: "blond", 10: "black"}.get(n, "brown")
    return person(Kit(KIN, (30, 30, 36), KIN, n, num_col=(30, 30, 36)), skin=sk, hair=hr, style="short", **kw)


def newcastle(n, **kw):
    if n == 9:
        return young_coach(**kw)
    sk = {4: "light", 5: "tan", 7: "brown", 10: "light", 11: "dark"}.get(n, "light")
    hr = {4: "blond", 5: "black", 7: "black", 10: "brown", 11: "black"}.get(n, "dark")
    return person(Kit(NEW, (245, 245, 250), NEW, n), skin=sk, hair=hr, style="short", **kw)


def referee(**kw):
    return person(Kit((28, 28, 34), (28, 28, 34), (28, 28, 34)), skin="light", hair="grey", style="short", **kw)


def medic(**kw):
    def cross(d, ox, oy):
        d.rectangle([ox + 8, oy + 10, ox + 9, oy + 13], fill=(40, 160, 80)); d.rectangle([ox + 7, oy + 11, ox + 10, oy + 12], fill=(40, 160, 80))
    return person(Kit((240, 240, 245), (40, 44, 60), (40, 44, 60)), skin=kw.pop("skin", "light"), hair=kw.pop("hair", "brown"),
                  style="short", trousers=True, extra=[cross], **kw)


def crest(img, x, y, s, team):
    d = ImageDraw.Draw(img)
    col = KIN if team == "KIN" else NEW
    pts = [(x - 40 * s, y - 46 * s), (x + 40 * s, y - 46 * s), (x + 40 * s, y + 6 * s), (x, y + 50 * s), (x - 40 * s, y + 6 * s)]
    d.polygon(pts, fill=col, outline=OL)
    d.line(pts + [pts[0]], fill=OL, width=max(2, int(6 * s)))
    if team == "KIN":
        d.text((x, y - 4 * s), "K", font=font(800, max(8, int(54 * s))), fill=(30, 30, 36), anchor="mm")
    else:   # little white castle
        d.rectangle([x - 22 * s, y - 14 * s, x + 22 * s, y + 18 * s], fill=(250, 250, 250))
        for k in range(3):
            d.rectangle([x - 22 * s + k * 17 * s, y - 26 * s, x - 12 * s + k * 17 * s, y - 14 * s], fill=(250, 250, 250))
        d.rectangle([x - 6 * s, y + 2 * s, x + 6 * s, y + 18 * s], fill=NEW)


# ------------------------------------------------------------------ the 1984 ground
def old_stadium(hor=520, night=True):
    """evening game under floodlights: standing terraces, crush barriers, a roof, lattice floodlight pylons, rain sky"""
    key = ("old", hor, night)
    if key in _c:
        return _c[key].copy()
    img = Image.new("RGB", (FW, FH))
    d = ImageDraw.Draw(img)
    top, bot = ((18, 20, 44), (70, 60, 92)) if night else ((90, 100, 130), (170, 160, 150))
    for y in range(hor + 40):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, clamp(y / (hor + 40)))) for a, b in zip(top, bot)))
    img = img.convert("RGBA")
    # floodlight pylons (lattice) with glowing light banks
    for px in (60, 660):
        base_y, top_y = hor - 20, hor - 470
        d = ImageDraw.Draw(img)
        d.polygon([(px - 22, base_y), (px + 22, base_y), (px + 8, top_y), (px - 8, top_y)], fill=(60, 60, 74))
        for yy in range(int(top_y), int(base_y), 26):
            w0 = lerp(8, 22, (yy - top_y) / (base_y - top_y))
            d.line([(px - w0, yy), (px + w0, yy + 26)], fill=(90, 90, 106), width=2)
            d.line([(px + w0, yy), (px - w0, yy + 26)], fill=(90, 90, 106), width=2)
        d.rectangle([px - 50, top_y - 60, px + 50, top_y], fill=(40, 40, 50), outline=OL, width=3)
        for r in range(3):
            for k in range(4):
                d.rectangle([px - 44 + k * 23, top_y - 54 + r * 18, px - 26 + k * 23, top_y - 40 + r * 18], fill=(255, 250, 220))
        glow(img, px, top_y - 30, 150, (255, 244, 200), 0.55)
    # stand roof
    d = ImageDraw.Draw(img)
    rt = hor - 300
    d.polygon([(0, rt), (FW, rt - 20), (FW, rt + 30), (0, rt + 50)], fill=(46, 44, 58), outline=OL)
    for x in range(40, FW, 120):
        d.rectangle([x, rt + 40, x + 8, hor - 40], fill=(60, 58, 74))      # roof pillars
    # standing terrace: dense crowd rows, scarves, flat caps, crush barriers
    lay_h = (hor - 40 - (rt + 40)) // 4
    lay = Image.new("RGBA", (FW // 4, lay_h), (52, 44, 56, 255))
    ld = ImageDraw.Draw(lay)
    rng = random.Random(84)
    cols = [KIN, KIN, KIN, (30, 30, 36), (230, 230, 230), NEW, (120, 60, 50), (90, 90, 100), (60, 70, 110)]
    for ry in range(0, lay_h, 3):
        for x in range(rng.randint(0, 1), FW // 4, 2):
            if rng.random() < 0.92:
                c = rng.choice(cols)
                ld.point((x, ry + 2), fill=c)
                ld.point((x, ry + 1), fill=rng.choice([(232, 190, 160), (200, 150, 110), (150, 100, 70)]))
                if rng.random() < 0.25:
                    ld.point((x, ry), fill=rng.choice([(60, 50, 40), (90, 90, 96), (30, 30, 36)]))   # flat caps
    for k in range(3):                                             # crush barriers
        y = int(lay_h * (0.3 + 0.25 * k))
        ld.line([(0, y), (FW // 4, y)], fill=(150, 154, 160))
    lay = lay.resize((FW, lay_h * 4), Image.NEAREST).filter(ImageFilter.GaussianBlur(0.8))
    img.alpha_composite(lay, (0, rt + 40))
    glow(img, 360, rt + 120, 400, (255, 230, 180), 0.12)
    # perimeter wall with hand-painted adverts
    d = ImageDraw.Draw(img)
    y0, y1 = hor - 40, hor + 2
    cols2 = [(150, 40, 40), (30, 70, 40), (230, 220, 200), (40, 50, 100)]
    labs = ["PIE SHOP", "KINGSTON GAZETTE", "BUS 42", "DOYLE'S CHIPS"]
    x = -30
    for k in range(6):
        w = 190
        d.rectangle([x, y0, x + w, y1], fill=cols2[k % 4], outline=OL, width=2)
        d.text((x + w / 2, (y0 + y1) / 2), labs[k % 4], font=font(800, 15), fill=(250, 240, 210) if k % 4 != 2 else (40, 40, 40), anchor="mm")
        x += w
    _c[key] = img
    return img.copy()


def mud_pitch(img, cam, Zgoal=None, box=True):
    """worn 80s pitch: duller stripes, mud in the goalmouth and down the middle"""
    pitch_persp(img, cam, Zgoal=Zgoal, box=box, warm=False)
    if Zgoal is None:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = random.Random(19)
    for k in range(16):
        X = rng.uniform(-5, 5); Z = Zgoal - rng.uniform(0.0, 7.0)
        r = rng.uniform(0.6, 1.8)
        if Z <= 0.5:
            continue
        x, y = cam.p(X, Z)
        rx, ry = r * cam.k(Z), r * 0.35 * cam.k(Z)
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(MUD if k % 3 else MUD_D) + (200,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))


def rain84(img, t, a=90):
    rain(img, t, a, 150)


# ------------------------------------------------------------------ VHS look for the past
def vhs(img, t, strength=1.0):
    img = img.convert("RGB")
    from PIL import ImageEnhance, ImageChops
    img = ImageEnhance.Color(img).enhance(1 - 0.28 * strength)
    img = Image.blend(img, Image.new("RGB", img.size, (120, 90, 60)), 0.10 * strength)
    r, g, b = img.split()
    r = ImageChops.offset(r, int(3 * strength), 0)
    b = ImageChops.offset(b, -int(2 * strength), 0)
    img = Image.merge("RGB", (r, g, b)).convert("RGBA")
    if "scan" not in _c:
        sl = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sl)
        for y in range(0, FH, 4):
            sd.line([(0, y), (FW, y)], fill=(0, 0, 0, 34), width=1)
        _c["scan"] = sl
    img.alpha_composite(_c["scan"])
    # a rolling tracking band + sparse noise
    rng = random.Random(int(t * 15))
    d = ImageDraw.Draw(img, "RGBA")
    by = (t * 260) % (FH + 200) - 100
    d.rectangle([0, by, FW, by + 26], fill=(255, 255, 255, int(22 * strength)))
    for _ in range(int(40 * strength)):
        x, y = rng.uniform(0, FW), rng.uniform(0, FH)
        d.line([(x, y), (x + rng.uniform(6, 30), y)], fill=(255, 255, 255, 60), width=1)
    return img


def vhs_osd(img, t, text="MAY 14 1984", play=True):
    d = ImageDraw.Draw(img)
    f = font(700, 26)
    if play:
        d.polygon([(40, 1004), (40, 1030), (62, 1017)], fill=(255, 255, 255))
        d.text((74, 1017), "PLAY", font=f, fill=(255, 255, 255), anchor="lm", stroke_width=2, stroke_fill=OL)
    d.text((40, 1056), text, font=f, fill=(255, 255, 255), anchor="lm", stroke_width=2, stroke_fill=OL)


def sheet(path):
    rows = [
        [grandad_cane(), young_grandad(), young_grandad(view="back"), young_grandad(pose="ready"), young_grandad(pose="reach"),
         young_grandad(pose="sit")],
        [coach(), young_coach(), young_coach(view="back"), young_coach(pose="run", phase=0.3), young_coach(pose="kick", phase=0.6),
         young_coach(mouth="grin")],
        [hero(gloves=True), kingston(5), kingston(8, view="back"), newcastle(7), newcastle(4, view="back"), referee()],
        [medic(), medic(skin="tan", hair="black"), hero(pose="dive", gloves=True), young_grandad(pose="dive"),
         young_grandad(blink=True, mouth="sad"), mason()],
    ]
    S = 6
    out = Image.new("RGBA", (6 * 34 * S, len(rows) * 52 * S), (90, 140, 90, 255))
    for r, row in enumerate(rows):
        for c, sp in enumerate(row):
            out.alpha_composite(big(sp, S), (c * 34 * S + 10, r * 52 * S + 10))
    out.convert("RGB").save(path)


if __name__ == "__main__":
    import sys
    sheet(sys.argv[1])
    img = old_stadium(520)
    c = Cam(camH=1.8, hor=520)
    mud_pitch(img, c, 14.0)
    goal3d(img, c, 14.0)
    vhs(img, 0.3).convert("RGB").save(sys.argv[2])
