"""Over-the-shoulder penalty set (keeper's view) used by segments A and B."""
from chars import *

YH = 214        # horizon on canvas
FOC = 330.0
CAMH = 1.3


def proj(X, Z, Yw=0.0):
    return 180 + X * FOC / Z, YH + (CAMH - Yw) * FOC / Z


_bg = {}


def far_bg():
    """static far layer: sky, floodlights, big stand, ad boards (blurred = depth of field)"""
    if "far" in _bg:
        return _bg["far"]
    c = Image.new("RGB", (CW, CH), NIGHT)
    d = ImageDraw.Draw(c)
    for y in range(0, 70):
        F(d, 0, y, CW, 1, mix((10, 14, 36), (34, 34, 66), y / 70))
    # roof
    F(d, 0, 52, CW, 8, (40, 42, 60))
    F(d, 0, 58, CW, 2, (90, 92, 120))
    for x in (40, 130, 230, 320):
        floodlight(d, x, 40, 1.1)
    stands(d, 0, 60, CW, YH - 72, 0, rows=13, seed=3, scale=0.85)
    # ad boards along the far touchline
    cols = [(220, 40, 50), (240, 200, 40), (40, 150, 80), (40, 90, 200)]
    labels = ["PIE SHOP", "BUS 42", "GO KEEPERS", "RIVERSIDE"]
    x = -10
    k = 0
    while x < CW:
        F(d, x, YH - 12, 70, 9, cols[k % 4])
        k += 1
        x += 70
    F(d, 0, YH - 3, CW, 3, (30, 90, 40))
    big = up(c).filter(ImageFilter.GaussianBlur(3.2))
    # crisp-ish text on ad boards (still slightly soft)
    dd = ImageDraw.Draw(big)
    x = -20
    k = 0
    f = font(700, 13)
    while x < FW:
        dd.text((x + 70 - dd.textlength(labels[k % 4], font=f) / 2, (YH - 11) * 2), labels[k % 4], font=f, fill=(255, 255, 255))
        k += 1
        x += 140
    big = big.filter(ImageFilter.GaussianBlur(0.8))
    floods = []
    _bg["far"] = big
    return big


def pitch_layer(t, extra=None):
    """ground plane in perspective (canvas). returns canvas RGBA (transparent above horizon)"""
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # mowing stripes running toward the vanishing point (bands in depth)
    zs = [200, 60, 40, 30, 23, 18, 14.5, 12, 10, 8.5, 7.2, 6.2, 5.4, 4.7, 4.1, 3.6, 3.1, 2.7, 2.3, 2.0, 1.7, 1.45, 1.2, 1.0, 0.8, 0.6, 0.4]
    for i in range(len(zs) - 1):
        y0 = proj(0, zs[i])[1]
        y1 = proj(0, zs[i + 1])[1]
        col = (64, 140, 64) if i % 2 else (56, 128, 58)
        # atmospheric fade far away
        far = clamp((y0 - YH) / 120)
        col = mix((70, 110, 90), col, 0.35 + 0.65 * far)
        d.rectangle([0, round(y0), CW, round(y1) + 1], fill=col)
    ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(-14, 14, 2):
        X0, X1 = i * 2.6, (i + 1) * 2.6
        p = [proj(X0 * .55, 0.4), proj(X1 * .55, 0.4), proj(X1 * .55, 200), proj(X0 * .55, 200)]
        od.polygon(p, fill=(0, 30, 0, 26))
    c.alpha_composite(ov)
    d = ImageDraw.Draw(c)
    # lines (lateral cheat 0.55 so box edges converge on screen)
    lw = lambda z: max(1, round(2.6 * 8 / z))
    def line3(p, q, w=None):
        (X0, Z0), (X1, Z1) = p, q
        n = 24
        pts = []
        for k in range(n + 1):
            a = k / n
            X, Z = lerp(X0, X1, a) * 0.55, lerp(Z0, Z1, a)
            pts.append(proj(X, Z))
        for k in range(n):
            Z = lerp(Z0, Z1, k / n)
            d.line([pts[k], pts[k + 1]], fill=(236, 240, 236), width=w or lw(Z))
    WL = (236, 240, 236)
    line3((-30, 2.0), (30, 2.0))                 # goal line (near, mostly off-screen)
    line3((-9.2, 2.0), (-9.2, 7.5)); line3((9.2, 2.0), (9.2, 7.5)); line3((-9.2, 7.5), (9.2, 7.5))
    line3((-20.2, 2.0), (-20.2, 18.5)); line3((20.2, 2.0), (20.2, 18.5)); line3((-20.2, 18.5), (20.2, 18.5))
    # penalty arc
    pts = []
    for k in range(25):
        a = math.pi * (0.2 + 0.6 * k / 24)
        X, Z = 9.15 * math.cos(a), 13 + 9.15 * math.sin(a)
        if Z >= 18.5:
            pts.append(proj(X * 0.55, Z))
    if len(pts) > 1:
        d.line(pts, fill=WL, width=1)
    line3((-40, 54), (40, 54), 1)  # halfway line
    # centre circle hint
    pts = [proj(9.15 * math.cos(a) * .55, 54 + 9.15 * math.sin(a) * .9) for a in np.linspace(0, math.tau, 40)]
    d.line(pts, fill=(200, 215, 200), width=1)
    # penalty spot
    x, y = proj(0, 13)
    F(d, x - 2, y - 1, 4, 2, WL)
    # mud patches (perspective ellipses)
    rng = random.Random(11)
    for _ in range(9):
        X, Z = rng.uniform(-6, 6), rng.uniform(9, 30)
        x, y = proj(X * .55, Z)
        rw = rng.uniform(0.6, 1.3) * FOC / Z
        d.ellipse([x - rw, y - rw * 0.25, x + rw, y + rw * 0.25], fill=(92, 92, 52) if rng.random() < .5 else (100, 84, 52))
    # big worn goalmouth patch + puddle near keeper
    rng2 = random.Random(5)
    for _ in range(18):
        X, Z = rng2.uniform(-3, 3), rng2.uniform(1.0, 4.0)
        x, y = proj(X * .55, Z)
        rw = rng2.uniform(.2, .45) * FOC / Z
        col = rng2.choice([(104, 86, 54), (118, 98, 62), (92, 76, 48), (84, 100, 56)])
        d.ellipse([x - rw, y - rw * .3, x + rw, y + rw * .3], fill=col)
    for _ in range(60):  # grass tufts / studs marks
        X, Z = rng2.uniform(-6, 6), rng2.uniform(0.8, 9)
        x, y = proj(X * .55, Z)
        F(d, x, y, max(1, 3 / Z), max(1, 6 / Z), (40, 96, 44))
    # kit bag, water bottle & towel by the near post (props)
    x, y = proj(-3.9 * .55, 1.6)
    R(d, x - 16, y - 12, 32, 14, (30, 34, 60), r=4); F(d, x - 12, y - 10, 10, 3, GRN)
    R(d, x + 20, y - 18, 6, 16, (90, 180, 240), r=2); F(d, x + 21, y - 21, 4, 3, (240, 240, 240))
    x, y = proj(3.9 * .55, 1.8)
    R(d, x - 12, y - 6, 26, 7, (240, 240, 240), r=2); F(d, x - 12, y - 3, 26, 1, GRN)
    for X, Z, r in ((-2.4, 6.5, 1.0), (3.1, 9.5, .8), (-1.0, 16, .9)):
        x, y = proj(X * .55, Z)
        rw = r * FOC / Z
        d.ellipse([x - rw, y - rw * .22, x + rw, y + rw * .22], fill=(84, 112, 140))
        F(d, x - rw * .4, y - 1, rw * .5, 1, (200, 220, 240))  # floodlight reflection
    # tiny far goal
    for X in (-3.66, 3.66):
        x0, y0 = proj(X * .55, 105)
        x1, y1 = proj(X * .55, 105, 2.44)
        d.line([(x0, y0), (x1, y1)], fill=WL, width=1)
    a, b = proj(-3.66 * .55, 105, 2.44), proj(3.66 * .55, 105, 2.44)
    d.line([a, b], fill=WL, width=1)
    return c


_pl = {}


def pitch_static():
    if "p" not in _pl:
        _pl["p"] = pitch_layer(0)
    return _pl["p"]


def mason_at(d, t, mode="stand", phase=0, kick=0, Z=13.6, X=0.0, expr="smirk", look=(0, 0)):
    x, y = proj(X * .55, Z)
    s = 1.8 * FOC / Z / 50 * 1.75
    # shadow
    d.ellipse([x - 12 * s, y - 2.5 * s, x + 12 * s, y + 2.5 * s], fill=(40, 70, 40))
    mason_front(d, x, y, s, mode=mode, phase=phase, kick=kick, expr=expr, look=look, t=t)
    return x, y, s


def ball(d, x, y, r, spin=0.0):
    r = max(1.2, r)
    d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill=OL)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 250, 250))
    if r > 2.5:
        for k in range(3):
            a = spin + k * math.tau / 3
            px, py = x + math.cos(a) * r * .55, y + math.sin(a) * r * .55
            pr = r * .28
            d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(40, 40, 50))
    else:
        F(d, x - r * .3, y - r * .3, max(1, r * .6), max(1, r * .6), (60, 60, 70))


def net_overlay(img, alpha=40, bulge=None, cell=34, width=2, offset=(0, 0)):
    """net mesh at full res; bulge=(x,y,amount) pushes mesh lines outward from point"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    col = (235, 240, 250, alpha)
    ox, oy = offset

    def disp(x, y):
        if not bulge:
            return x, y
        bx, by, a = bulge
        dx, dy = x - bx, y - by
        r = math.hypot(dx, dy) + 1e-3
        k = a * math.exp(-(r / 220) ** 2)
        return x + dx / r * k * 60, y + dy / r * k * 60
    for gx in range(-2, FW // cell + 3):
        pts = [disp(gx * cell + ox + (gy * cell) * 0.0, gy * cell + oy) for gy in range(-2, FH // cell + 3)]
        # diamond mesh: diagonal lines
    for k in range(-40, 80):
        p1 = [disp(k * cell + ox + j * cell, j * cell + oy) for j in range(-2, FH // cell + 3)]
        p2 = [disp(k * cell + ox - j * cell, j * cell + oy) for j in range(-2, FH // cell + 3)]
        d.line(p1, fill=col, width=width)
        d.line(p2, fill=col, width=width)
    img.paste(ov, (0, 0), ov)
