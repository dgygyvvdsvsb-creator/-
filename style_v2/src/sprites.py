"""Characters redrawn 1:1 in the remi_sport sprite style.

Reference anatomy (measured on example_4/8 close-ups, 1 sprite px ~ 7 px at 576 w):
  * ~18 x 28 px body: big boxy head (10x9), wide square torso (10 + 2 px sleeves each side),
    short dark shorts, SHORT stubby legs mostly covered by socks, black boots.
  * one dark 1-px outline around the silhouette (near-black, not colour), one shadow tone on
    the right side of every part, a couple of light highlight pixels in the hair.
  * eyes = one white + one black pixel, brows one dark row above, tiny 2-px mouth.
  * number on the chest in a 3x5 pixel font, dark on light shirts / white on dark shirts.
"""
from PIL import Image, ImageDraw

OL = (26, 20, 30, 255)
SKIN = {"light": ((241, 196, 156), (214, 158, 120)), "tan": ((206, 146, 100), (172, 112, 74)),
        "dark": ((128, 82, 56), (98, 60, 42))}
HAIR = {"brown": ((74, 46, 30), (112, 74, 48)), "dark": ((44, 32, 30), (82, 60, 50)),
        "blond": ((238, 204, 92), (255, 236, 150)), "ginger": ((212, 98, 36), (246, 148, 70)),
        "black": ((30, 24, 28), (66, 56, 60)), "white": ((232, 232, 236), (255, 255, 255)),
        "grey": ((150, 150, 158), (196, 196, 204))}

DIG = {"0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
       "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "011", "001", "111"],
       "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
       "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
       "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"]}


def dk(c, f=0.78):
    return tuple(int(v * f) for v in c[:3])


class Look:
    def __init__(self, shirt, shorts=(32, 34, 44), socks=None, number=None, num_col=None, skin="light",
                 hair="brown", style="short", legs="kit", trousers=None, shoes=(30, 30, 34),
                 gloves=False, bracelet=False, beard=False, glasses=False, cap=None, buttons=False,
                 sock_band=(245, 245, 245)):
        self.__dict__.update(locals())
        self.socks = socks or shirt
        if num_col is None:
            lum = sum(shirt[:3]) / 3
            self.num_col = (30, 26, 34) if lum > 150 else (250, 250, 250)


W, H, OY, OX = 26, 34, 3, 4          # canvas with room for spiky hair, raised arms, ready arms


def _canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def _r(d, x0, y0, x1, y1, c):
    d.rectangle([x0 + OX, y0 + OY, x1 + OX, y1 + OY], fill=tuple(c[:3]) + (255,))


def _p(d, x, y, c):
    d.point((x + OX, y + OY), fill=tuple(c[:3]) + (255,))


def _num(d, n, cx, y, col):
    s = str(n)
    w = len(s) * 3 + (len(s) - 1)
    x = cx - w // 2
    for ch in s:
        for j, row in enumerate(DIG[ch]):
            for i, b in enumerate(row):
                if b == "1":
                    _p(d, x + i, y + j, col)
        x += 4


def _outline(img):
    """add the dark 1-px silhouette outline (outside the shape)"""
    a = img.split()[3].load()
    out = img.copy()
    px = out.load()
    for y in range(H):
        for x in range(W):
            if a[x, y]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < W and 0 <= yy < H and a[xx, yy]:
                    px[x, y] = OL
                    break
    return out


def person(lk, view="front", pose="stand", mouth="flat", eyes="open", step=0):
    img = _canvas()
    d = ImageDraw.Draw(img)
    sk, skd = SKIN[lk.skin]
    hr, hl = HAIR.get(lk.hair, HAIR["brown"])
    sh, shd = lk.shirt, dk(lk.shirt)
    back = view == "back"

    # ---------------- legs / shorts (rows 18..27)
    if lk.legs == "kit":
        _r(d, 4, 18, 13, 20, lk.shorts); _r(d, 11, 18, 13, 20, dk(lk.shorts))
        _r(d, 8, 20, 9, 20, (0, 0, 0, 0)) if False else None
    else:                                   # trousers (family / staff)
        _r(d, 4, 18, 13, 19, lk.trousers); _r(d, 11, 18, 13, 19, dk(lk.trousers))
    sit = pose == "sit"
    bot = 23 if sit else 26
    for i, (x0, x1) in enumerate(((5, 7), (10, 12))):
        lift = 0
        if pose == "run":
            lift = 2 if (i == step % 2) else 0
        top = 21 if lk.legs == "kit" else 20
        b = bot - lift
        if lk.legs == "kit":
            _r(d, x0, top, x1, b, lk.socks); _p(d, x1, top + 1, dk(lk.socks))
            _r(d, x0, top, x1, top, sk)                                   # knee
            _r(d, x0, top + 1, x1, top + 1, lk.sock_band)                 # sock band
            _r(d, x1, top + 2, x1, b, dk(lk.socks))
        else:
            _r(d, x0, top, x1, b, lk.trousers); _r(d, x1, top, x1, b, dk(lk.trousers))
        bx0, bx1 = (x0 - 1, x1) if i == 0 else (x0, x1 + 1)
        _r(d, bx0, b + 1, bx1, b + 1, lk.shoes)
        _p(d, bx0 + 1 if i == 0 else bx0 + 1, b + 1, (96, 96, 104) if lk.shoes == (30, 30, 34) else dk(lk.shoes, 1.25))

    # ---------------- torso (rows 9..17)
    _r(d, 4, 9, 13, 17, sh); _r(d, 12, 10, 13, 17, shd)
    _r(d, 7, 9, 10, 9, dk(sh, 0.62) if not back else sh)                  # collar
    if lk.buttons:
        for y in (11, 13, 15):
            _p(d, 8, y, (240, 214, 120))
        _r(d, 9, 10, 9, 17, dk(sh, 0.7))
    if lk.number is not None:
        _num(d, lk.number, 9, 11 if not back else 10, lk.num_col)
        if back:
            pass

    # ---------------- arms
    def arm(side, mode):
        xs = (2, 3) if side == 0 else (14, 15)
        if mode == "down":
            _r(d, xs[0], 9, xs[1], 11, sh if side == 0 else shd)
            _r(d, xs[0], 12, xs[1], 15, sk if side == 0 else skd)
            hand = (xs[0], 16, xs[1], 16)
        elif mode == "out":                                              # keeper ready
            ox = -2 if side == 0 else 2
            _r(d, xs[0], 9, xs[1], 11, sh if side == 0 else shd)
            _r(d, xs[0] + ox, 11, xs[1] + ox, 14, sk if side == 0 else skd)
            hand = (xs[0] + ox, 15, xs[1] + ox, 15)
        elif mode == "up":
            _r(d, xs[0], 8, xs[1], 10, sh if side == 0 else shd)
            _r(d, xs[0], 3, xs[1], 7, sk if side == 0 else skd)
            hand = (xs[0], 2, xs[1], 2)
        elif mode == "swing":
            _r(d, xs[0], 9, xs[1], 11, sh if side == 0 else shd)
            _r(d, xs[0], 12, xs[1], 13, sk if side == 0 else skd)
            hand = (xs[0], 14, xs[1], 14)
        if lk.gloves:
            gx0, gy0, gx1, gy1 = hand
            _r(d, gx0 - 1 if side == 0 else gx0, gy0 - 1, gx1 if side == 0 else gx1 + 1, gy1 + 1, (250, 140, 30))
            _r(d, gx1 if side == 0 else gx1 + 1, gy0 - 1, gx1 if side == 0 else gx1 + 1, gy1 + 1, (214, 104, 20))
        else:
            _r(d, *hand, sk if side == 0 else skd)
        if lk.bracelet and side == 1:                                    # right wrist (viewer's left in front view)
            pass
        if lk.bracelet and ((side == 0 and not back) or (side == 1 and back)):
            gx0, gy0, gx1, gy1 = hand
            _r(d, gx0, gy0 - (2 if lk.gloves else 1), gx1, gy0 - (2 if lk.gloves else 1), (220, 30, 40))

    modes = {"stand": ("down", "down"), "ready": ("out", "out"), "celebrate": ("up", "up"),
             "sit": ("down", "down"), "run": ("swing", "down") if step % 2 == 0 else ("down", "swing"),
             "dive": ("up", "up"), "wave": ("down", "up")}[pose]
    arm(0, modes[0]); arm(1, modes[1])

    # ---------------- head (rows 0..8)
    _r(d, 4, 1, 13, 8, sk); _r(d, 13, 2, 13, 8, skd)
    _p(d, 3, 5, sk); _p(d, 14, 5, skd)                                    # ears
    if back:
        _r(d, 4, 0, 13, 7, hr); _r(d, 12, 1, 13, 7, dk(hr, 0.8))
        _p(d, 6, 1, hl); _p(d, 9, 1, hl)
        if lk.style == "bald":
            _r(d, 5, 0, 12, 5, sk); _r(d, 12, 0, 12, 5, skd); _r(d, 4, 4, 13, 7, hr)
        if lk.style == "pony":
            _r(d, 8, 8, 9, 11, hr)
    else:
        st = lk.style
        if st in ("short", "spiky", "curly", "pony", "cap"):
            _r(d, 4, 0, 13, 2, hr); _r(d, 4, 3, 4, 4, hr); _r(d, 13, 3, 13, 4, dk(hr, 0.8))
            _p(d, 6, 0, hl); _p(d, 7, 1, hl); _p(d, 10, 0, hl)
        if st == "spiky":
            for x in (4, 6, 8, 10, 12):
                _p(d, x, -1, hr); _p(d, x + 1, -2, hr) if x < 12 else None
            _p(d, 9, -1, hl)
        if st == "curly":
            _r(d, 3, -1, 14, 2, hr); _r(d, 3, 3, 3, 6, hr); _r(d, 14, 3, 14, 6, dk(hr, 0.8))
            for x in (4, 7, 10, 13):
                _p(d, x, -1, hl)
            for x in (5, 8, 11):
                _p(d, x, 1, dk(hr, 0.75))
        if st == "pony":
            _r(d, 13, 3, 14, 9, hr); _r(d, 14, 6, 15, 11, hr); _r(d, 4, 3, 4, 6, hr)
        if st == "bald":
            _p(d, 6, 1, (255, 222, 190)); _p(d, 7, 1, (255, 222, 190))
            _r(d, 4, 3, 4, 5, hr); _r(d, 13, 3, 13, 5, hr)
        if st == "cap":
            c = lk.cap
            _r(d, 4, -1, 13, 2, c); _r(d, 12, -1, 13, 2, dk(c))
            _r(d, 3, 3, 10, 3, dk(c, 0.7)); _p(d, 8, 0, (250, 210, 60))
        # face
        _r(d, 6, 4, 7, 4, dk(hr, 0.7) if lk.hair not in ("white", "blond") else (120, 90, 60))
        _r(d, 10, 4, 11, 4, dk(hr, 0.7) if lk.hair not in ("white", "blond") else (120, 90, 60))
        if lk.hair in ("white", "grey"):
            _r(d, 6, 4, 7, 4, (200, 200, 205)); _r(d, 10, 4, 11, 4, (200, 200, 205))
        if eyes == "closed":
            _r(d, 6, 5, 7, 5, (60, 40, 40)); _r(d, 10, 5, 11, 5, (60, 40, 40))
        else:
            _p(d, 6, 5, (255, 255, 255)); _p(d, 7, 5, (20, 16, 22))
            _p(d, 10, 5, (255, 255, 255)); _p(d, 11, 5, (20, 16, 22))
        if lk.glasses:
            for x0 in (5, 9):
                _p(d, x0, 5, (70, 70, 82)); _p(d, x0 + 3, 5, (70, 70, 82))
                _r(d, x0 + 1, 6, x0 + 2, 6, (70, 70, 82))
            _p(d, 4, 5, (70, 70, 82)); _p(d, 13, 5, (70, 70, 82))
        if lk.beard:
            _r(d, 4, 7, 13, 9, HAIR["white"][0]); _p(d, 4, 6, HAIR["white"][0]); _p(d, 13, 6, HAIR["white"][0]); _r(d, 5, 10, 12, 10, HAIR["white"][0])
            _r(d, 12, 7, 13, 9, (204, 204, 210))
        mc = (156, 66, 66)
        if mouth == "flat":
            _r(d, 8, 7, 9, 7, mc)
        elif mouth == "smile":
            _r(d, 8, 7, 9, 7, mc); _p(d, 7, 6, mc); _p(d, 10, 6, mc)
        elif mouth == "open":
            _r(d, 8, 7, 9, 8, (90, 30, 34))
        elif mouth == "grin":
            _r(d, 7, 7, 10, 7, (255, 255, 255)); _r(d, 7, 8, 10, 8, (150, 50, 54))
        elif mouth == "sad":
            _r(d, 8, 7, 9, 7, mc); _p(d, 7, 8, mc); _p(d, 10, 8, mc)
    return _outline(img)


def big(s, k):
    return s.resize((s.width * k, s.height * k), Image.NEAREST)


# ------------------------------------------------------------------ the cast (series anchors kept)
def hero(**kw):
    g = kw.pop("gloves", False)
    return person(Look((44, 170, 76), (245, 245, 250), (44, 170, 76), 0, skin="light", hair="brown",
                       gloves=g, bracelet=True, sock_band=(245, 245, 245)), **kw)

def grandad(**kw):
    return person(Look((128, 80, 44), legs="trousers", trousers=(88, 88, 96), shoes=(70, 44, 30), skin="light",
                       hair="white", style="bald", beard=True, glasses=True, buttons=True), **kw)

def mum(**kw):
    return person(Look((74, 112, 196), legs="trousers", trousers=(52, 66, 110), shoes=(240, 240, 240), skin="light",
                       hair="brown", style="pony"), **kw)

def coach(**kw):
    return person(Look((34, 44, 86), legs="trousers", trousers=(30, 34, 52), skin="light", hair="grey",
                       style="cap", cap=(30, 40, 84)), **kw)

def alfie(**kw):
    return person(Look((62, 124, 214), (245, 245, 250), (62, 124, 214), 7, skin="light", hair="ginger",
                       style="curly"), **kw)

def mason(**kw):
    return person(Look((214, 52, 58), (245, 245, 250), (214, 52, 58), 9, skin="light", hair="blond",
                       style="spiky"), **kw)

def okafor(**kw):
    return person(Look((248, 206, 44), (30, 30, 36), (248, 206, 44), 1, skin="dark", hair="black",
                       gloves=True), **kw)

def dixon(**kw):
    return person(Look((62, 124, 214), (30, 34, 50), (62, 124, 214), 2, skin="tan", hair="brown",
                       style="curly", gloves=True), **kw)

def red(n, skin="tan", hair="dark", style="short", **kw):
    return person(Look((214, 52, 58), (245, 245, 250), (214, 52, 58), n, skin=skin, hair=hair, style=style), **kw)

def blue(n, skin="light", hair="dark", style="short", **kw):
    return person(Look((88, 160, 232), (245, 245, 250), (88, 160, 232), n, skin=skin, hair=hair, style=style), **kw)
