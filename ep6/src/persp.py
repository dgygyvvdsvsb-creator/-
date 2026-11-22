"""Perspective match engine (EP6+): golden-hour pitch, 3D goal, world-space players, ball arcs.
World: X metres right, Z metres away from the camera, Y metres up."""
import math, random
from style import *

def mix(c1, c2, t):
    return tuple(int(lerp(a, b, clamp(t))) for a, b in zip(c1, c2))


def glow(img, x, y, r, color, a=0.5):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color + (int(255 * a / 10 * 1.6),))
    img.alpha_composite(ov)


HOR = 470          # horizon on screen
FOC = 900.0        # focal length (px)


class Cam:
    def __init__(self, camX=0.0, camH=1.7, hor=HOR, f=FOC):
        self.camX, self.camH, self.hor, self.f = camX, camH, hor, f

    def p(self, X, Z, Y=0.0):
        Z = max(Z, 0.05)
        return FW / 2 + (X - self.camX) * self.f / Z, self.hor + (self.camH - Y) * self.f / Z

    def k(self, Z):
        return self.f / max(Z, 0.05)


_c = {}

SKY_T, SKY_B = (52, 70, 128), (246, 182, 112)


def backdrop(hor=HOR, sun=(560, 300), stadium=False):
    key = ("bd", hor, sun, stadium)
    if key in _c:
        return _c[key].copy()
    img = Image.new("RGB", (FW, FH))
    d = ImageDraw.Draw(img)
    for y in range(hor + 40):
        d.line([(0, y), (FW, y)], fill=tuple(int(lerp(a, b, clamp(y / (hor + 40)) ** 1.3)) for a, b in zip(SKY_T, SKY_B)))
    img = img.convert("RGBA")
    glow(img, sun[0], sun[1], 70, (255, 236, 170), 0.95)
    for r, a in ((220, 70), (140, 90)):
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([sun[0] - r, sun[1] - r, sun[0] + r, sun[1] + r], fill=(255, 210, 140, a))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r / 3)))
    # pixel tree line (drawn at 1/4 res, upscaled NEAREST)
    lw, lh = FW // 4, (hor + 10) // 4
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    rng = random.Random(9)
    base = lh - 6
    x = -6
    while x < lw + 6:
        w = rng.randint(14, 24)
        h = rng.randint(18, 30)
        tx = x + w // 2
        ld.rectangle([tx - 1, base - 8, tx + 1, base], fill=(70, 46, 34, 255))       # trunk
        for k in range(4):                                                               # leafy blobs
            cx_ = tx + rng.randint(-w // 3, w // 3)
            cy_ = base - 8 - rng.randint(4, h - 6)
            r = rng.randint(5, 8)
            ld.ellipse([cx_ - r, cy_ - r, cx_ + r, cy_ + r], fill=(46, 92, 52, 255))
        ld.ellipse([tx - w // 2, base - h, tx + w // 2, base - 8], fill=(40, 84, 48, 255))
        for k in range(5):  # sunlit leaves on the sun side
            px = tx + rng.randint(0, w // 2)
            py = base - h + rng.randint(2, h // 2)
            ld.point((px, py), fill=(120, 150, 70, 255))
            ld.point((px + 1, py), fill=(150, 170, 80, 255))
        x += w - 4
    big_ = lay.resize((lw * 4, lh * 4), Image.NEAREST)
    img.alpha_composite(big_, (0, 0))
    if stadium:   # stand full of fans in front of the trees
        crowd_band(img, hor - 150, hor - 24, seed=hor, blur=1.2)
        img_d = ImageDraw.Draw(img)
        img_d.rectangle([0, hor - 30, FW, hor - 22], fill=(40, 36, 60))
    # fence with posts in front of the trees
    d = ImageDraw.Draw(img)
    fy = hor - 30
    if stadium:
        _ads(img, hor - 22, hor + 4)
        _c[key] = img
        return img.copy()
    d.rectangle([0, fy, FW, hor + 4], fill=(110, 116, 140))
    for xx in range(0, FW, 10):
        d.line([(xx, fy), (xx + 10, hor + 4)], fill=(150, 156, 176), width=1)
        d.line([(xx + 10, fy), (xx, hor + 4)], fill=(150, 156, 176), width=1)
    for xx in range(0, FW, 60):
        d.rectangle([xx, fy - 6, xx + 4, hor + 4], fill=(70, 74, 92))
    d.rectangle([0, fy - 6, FW, fy - 3], fill=(70, 74, 92))
    _c[key] = img
    return img.copy()


def _ads(img, y0, y1):
    d = ImageDraw.Draw(img)
    cols = [(210, 52, 56), (40, 90, 200), (246, 206, 40), (40, 150, 80)]
    labs = ["RIVERSIDE", "PIE SHOP", "BUS 42", "GO KEEPERS"]
    for k in range(6):
        x = k * 140 - 30
        d.rectangle([x, y0, x + 140, y1], fill=cols[k % 4])
        d.text((x + 70, (y0 + y1) / 2), labs[k % 4], font=font(800, 16), fill=(255, 255, 255), anchor="mm")


GRASS_A, GRASS_B = (56, 142, 78), (48, 128, 70)     # deep green, like the reference
LINE = (240, 244, 236)


def pitch_near(img, cam, G=0.0):
    """lines when the camera is behind OUR goal line (keeper's view): box extends away from the camera"""
    pitch_persp(img, cam, None)
    d = ImageDraw.Draw(img)

    def L(X0, Z0, X1, Z1):
        Z0, Z1 = max(Z0, 0.4), max(Z1, 0.4)
        n = 24
        pts = [cam.p(lerp(X0, X1, i / n), lerp(Z0, Z1, i / n)) for i in range(n + 1)]
        d.line(pts, fill=LINE, width=max(2, int(0.08 * cam.k((Z0 + Z1) / 2))))
    L(-14, G + 11, 14, G + 11); L(-14, G + 0.4, -14, G + 11); L(14, G + 0.4, 14, G + 11)
    L(-6, G + 4, 6, G + 4); L(-6, G + 0.4, -6, G + 4); L(6, G + 0.4, 6, G + 4)
    x, y = cam.p(0, G + 8)
    r = cam.k(G + 8) * 0.12
    d.ellipse([x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6], fill=LINE)
    L(-40, G + 26, 40, G + 26)


def pitch_persp(img, cam, Zgoal=None, box=True, centre=None, warm=True):
    """mowing stripes in depth + lines; Zgoal = goal line distance (goal on the far side)"""
    d = ImageDraw.Draw(img)
    # stripes: bands of 3 m in Z from far to near
    zs = [200, 120, 80, 60, 48] + [44 - 3 * i for i in range(14)] + [2.2, 1.4, 0.9, 0.6, 0.35]
    zs = [z for z in zs if z > 0.3]
    for i in range(len(zs) - 1):
        y0 = cam.p(0, zs[i])[1]
        y1 = cam.p(0, zs[i + 1])[1]
        col = GRASS_A if i % 2 else GRASS_B
        far = clamp((y0 - cam.hor) / 160)
        col = mix((150, 170, 110), col, 0.45 + 0.55 * far) if warm else col
        d.rectangle([0, int(y0), FW, int(y1) + 1], fill=col)
    if Zgoal is None:
        return

    def L(X0, Z0, X1, Z1, w=None):
        n = 18
        pts = [cam.p(lerp(X0, X1, i / n), lerp(Z0, Z1, i / n)) for i in range(n + 1)]
        ww = w or max(2, int(0.09 * cam.k((Z0 + Z1) / 2)))
        d.line(pts, fill=LINE, width=ww)
    G = Zgoal
    L(-40, G, 40, G)                       # goal line
    if box:
        L(-14, G, -14, G - 11); L(14, G, 14, G - 11); L(-14, G - 11, 14, G - 11)   # penalty box (youth)
        L(-6, G, -6, G - 4); L(6, G, 6, G - 4); L(-6, G - 4, 6, G - 4)               # 6-yard box
        if G - 8 > 6:
            x, y = cam.p(0, G - 8)
            r = max(2, cam.k(G - 8) * 0.12)
            d.ellipse([x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6], fill=LINE)      # spot
        pts = [cam.p(6 * math.cos(a), G - 8 - 6 * math.sin(a)) for a in np.linspace(0.6, math.pi - 0.6, 20)]
        pts = [p for p, a in zip(pts, np.linspace(0.6, math.pi - 0.6, 20)) if G - 8 - 6 * math.sin(a) < G - 11]
        if len(pts) > 1:
            d.line(pts, fill=LINE, width=3)


def goal3d(img, cam, Zg, X=0.0, w=5.0, h=2.0, depth=1.4, back=True):
    """goal at distance Zg; back=True: net behind the goal line (seen from the pitch)"""
    d = ImageDraw.Draw(img, "RGBA")
    zb = Zg + depth if back else Zg - depth
    pf = [cam.p(X - w / 2, Zg), cam.p(X + w / 2, Zg), cam.p(X + w / 2, Zg, h), cam.p(X - w / 2, Zg, h)]
    pb = [cam.p(X - w / 2, zb), cam.p(X + w / 2, zb), cam.p(X + w / 2, zb, h * 0.75), cam.p(X - w / 2, zb, h * 0.75)]
    net = (255, 255, 255, 55)
    nn = max(5, min(12, int(w * cam.k(Zg) / 40)))
    # back + sides + roof of the net
    for i in range(nn + 1):
        a = i / nn
        d.line([(lerp(pb[0][0], pb[1][0], a), lerp(pb[0][1], pb[1][1], a)), (lerp(pb[3][0], pb[2][0], a), lerp(pb[3][1], pb[2][1], a))], fill=net, width=1)
        d.line([(lerp(pf[3][0], pf[2][0], a), lerp(pf[3][1], pf[2][1], a)), (lerp(pb[3][0], pb[2][0], a), lerp(pb[3][1], pb[2][1], a))], fill=net, width=1)
    for i in range(7):
        a = i / 6
        d.line([(lerp(pb[0][0], pb[3][0], a), lerp(pb[0][1], pb[3][1], a)), (lerp(pb[1][0], pb[2][0], a), lerp(pb[1][1], pb[2][1], a))], fill=net, width=1)
        for s0, s1, s2, s3 in ((pf[0], pf[3], pb[0], pb[3]), (pf[1], pf[2], pb[1], pb[2])):
            d.line([(lerp(s0[0], s1[0], a), lerp(s0[1], s1[1], a)), (lerp(s2[0], s3[0], a), lerp(s2[1], s3[1], a))], fill=net, width=1)
    for s0, s1 in ((pf[0], pb[0]), (pf[1], pb[1]), (pf[3], pb[3]), (pf[2], pb[2])):
        d.line([s0, s1], fill=(230, 230, 236, 200), width=2)
    pw = max(3, int(0.12 * cam.k(Zg)))
    for a, b in ((pf[0], pf[3]), (pf[1], pf[2]), (pf[3], pf[2])):
        d.line([a, b], fill=OL, width=pw + 4)
    for a, b in ((pf[0], pf[3]), (pf[1], pf[2]), (pf[3], pf[2])):
        d.line([a, b], fill=(252, 252, 255), width=pw)


def sprite_at(img, cam, sprite, X, Z, Y=0.0, height_m=1.6, rot=0, flip=False):
    """place a person sprite standing at world (X,Z) feet height Y; returns screen bbox centre"""
    hpx = height_m * cam.k(Z)
    s = hpx / 31.0
    w, h = max(1, int(24 * s)), max(1, int(39 * s))
    sp = sprite.resize((w, h), Image.NEAREST)
    if flip:
        sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
    x, y = cam.p(X, Z, Y)
    if rot:
        sp = sp.rotate(rot, expand=True, resample=Image.NEAREST)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2 - hpx * 0.3)))
        return x, y - hpx * 0.3
    img.alpha_composite(sp, (int(x - w / 2), int(y - 37 * s)))
    return x, y - hpx / 2


def ground_shadow(img, cam, X, Z, r=0.45, a=90):
    x, y = cam.p(X, Z)
    k = cam.k(Z)
    shadow(img, x, y, r * 2 * k, r * 0.5 * k, a)


def ball_at(img, cam, X, Z, Y, shadow_=True):
    k = cam.k(Z)
    r = max(6, 0.16 * k)          # stylised: a bit bigger than real so it reads well
    if shadow_:
        sx, sy = cam.p(X, Z)
        shadow(img, sx, sy, r * 2.2 / (1 + Y * 0.6), r * 0.6, 70)
    x, y = cam.p(X, Z, Y)
    draw_ball(img, x, y + r, r / 6.5)
    return x, y


def arc(P0, P1, apex=1.0, curve=0.0, n=40):
    """world points of a shot: P=(X,Z,Y); apex extra height; curve = sideways bend (m)"""
    pts = []
    for i in range(n + 1):
        a = i / n
        X = lerp(P0[0], P1[0], a) + curve * math.sin(a * math.pi)
        Z = lerp(P0[1], P1[1], a)
        Y = lerp(P0[2], P1[2], a) + apex * math.sin(a * math.pi)
        pts.append((X, Z, Y))
    return pts


def at(pts, a):
    a = clamp(a) * (len(pts) - 1)
    i = min(int(a), len(pts) - 2)
    f = a - i
    return tuple(lerp(pts[i][k], pts[i + 1][k], f) for k in range(3))


def dotted_path(img, cam, pts, upto=1.0, col=(250, 206, 40), from_=0.0):
    """even dashes in screen space along the projected path between from_ and upto"""
    d = ImageDraw.Draw(img)
    dense = [cam.p(*_xzy(at(pts, lerp(from_, upto, i / 300)))) for i in range(301)]
    zs = [at(pts, lerp(from_, upto, i / 300))[1] for i in range(301)]
    acc, on = 0.0, True
    seg = [dense[0]]
    for i in range(1, len(dense)):
        l = math.dist(dense[i - 1], dense[i])
        acc += l
        seg.append(dense[i])
        lim = 16 if on else 12
        if acc >= lim:
            if on and len(seg) > 1:
                w = int(clamp(0.035 * cam.k(zs[i]), 3, 7))
                d.line(seg, fill=OL, width=w + 3)
                d.line(seg, fill=col, width=w)
            on = not on
            acc = 0
            seg = [dense[i]]


def _xzy(p):
    return p[0], p[1], p[2]


def ring_on_grass(img, cam, X, Z, r=0.8, col=(250, 206, 40), w=4):
    pts = [cam.p(X + r * math.cos(a), Z + r * 0.6 * math.sin(a)) for a in np.linspace(0, math.tau, 40)]
    ImageDraw.Draw(img).line(pts, fill=col, width=w)


def scoreboard(img, y, left, right, sl, sr, minute, k=1.0, flash_side=None, t=0):
    if k <= 0.02:
        return
    d = ImageDraw.Draw(img)
    w = 560 * k
    x0 = FW / 2 - w / 2
    d.rounded_rectangle([x0, y, x0 + w, y + 120], 18, fill=(14, 16, 30), outline=OL, width=5)
    f = font(800, 84)
    cl = C_G if flash_side == "L" and int(t * 8) % 2 else C_Y
    cr = C_R if flash_side == "R" and int(t * 8) % 2 else C_Y
    d.text((FW / 2 - 70, y + 60), str(sl), font=f, fill=cl, anchor="mm")
    d.text((FW / 2, y + 60), "-", font=f, fill=C_Y, anchor="mm")
    d.text((FW / 2 + 70, y + 60), str(sr), font=f, fill=cr, anchor="mm")
    d.rectangle([x0 + 24, y + 26, x0 + 104, y + 94], fill=(210, 52, 56), outline=OL, width=4)
    d.text((x0 + 64, y + 60), left, font=font(800, 22), fill=(255, 255, 255), anchor="mm")
    d.rectangle([x0 + w - 104, y + 26, x0 + w - 24, y + 94], fill=(80, 150, 230), outline=OL, width=4)
    d.text((x0 + w - 64, y + 60), right, font=font(800, 22), fill=(255, 255, 255), anchor="mm")
    d.text((FW / 2, y + 150), minute, font=font(800, 36), fill=(240, 80, 80), anchor="mm")


def keeper_world(img, cam, X, Z, side, phase, height_m=1.6, sprite=None):
    """animated save on the goal line at (X,Z):
       0.00-0.12 set (knees bend)  0.12-0.30 explosive push + flight to the ball (fast)
       0.30-0.38 catch at full stretch   0.38-0.55 falls under gravity onto the grass, small bounce
       0.55-1.00 lies on the grass, ball held, slight breathing. returns glove (x, y) on screen."""
    k = cam.k(Z)
    s = height_m * k / 31.0
    if phase < 0.12:                                   # set position, sinking a little
        dip = math.sin(phase / 0.12 * math.pi) * 0.08
        ground_shadow(img, cam, X, Z, 0.45)
        sprite_at(img, cam, sprite or hero(pose="ready", gloves=True), X, Z, Y=-dip, height_m=height_m)
        x, y = cam.p(X + side * 0.7, Z, 1.1)
        return x, y
    if phase < 0.38:                                   # take-off and flight (ease-out = fast start)
        a = ease_out((phase - 0.12) / 0.26)
        Xc = X + side * 1.5 * a
        Yc = 0.35 + 0.55 * math.sin(a * math.pi * 0.5)  # rises to the ball
        rot = 90 * ease_out(min(1.0, a * 1.6))
    elif phase < 0.55:                                 # gravity: drop to the grass, small bounce
        f = (phase - 0.38) / 0.17
        Xc = X + side * (1.5 + 0.25 * f)
        Yc = 0.9 * (1 - f) ** 2 + 0.08 * abs(math.sin(f * math.pi * 2)) * (1 - f)
        rot = 90
    elif phase < 0.68:                                 # short moment on the grass
        Xc = X + side * 1.75
        Yc = 0.0
        rot = 90
    else:                                              # gets straight back up, ball in his hands
        Xu = X + side * 1.75
        f = ease_out((phase - 0.68) / 0.14)
        if f < 1:
            ground_shadow(img, cam, Xu, Z, 0.45)
            sprite_at(img, cam, hero(pose="sit", gloves=True), Xu, Z, Y=-0.25 * (1 - f), height_m=height_m * (0.8 + 0.2 * f))
        else:
            ground_shadow(img, cam, Xu, Z, 0.45)
            sprite_at(img, cam, hero(pose="catch", gloves=True, mouth="smile"), Xu, Z, height_m=height_m)
        x, y = cam.p(Xu, Z, 1.0 if f >= 1 else 0.6)
        return x, y
    sp = (sprite or hero(pose="reach", gloves=True, mouth="open" if phase < 0.55 else "smile"))
    sp = sp.resize((max(1, int(24 * s)), max(1, int(39 * s))), Image.NEAREST)
    sp = sp.rotate(-rot if side > 0 else rot, expand=True, resample=Image.NEAREST)
    ground_shadow(img, cam, Xc, Z, 0.55 + 0.35 * clamp(1 - Yc), 80)
    gx, gy = cam.p(Xc, Z, Yc)
    body_h = 9 * s                                     # half thickness of the lying body
    yb = gy + body_h * 0.6
    img.alpha_composite(sp, (int(gx - sp.width / 2), int(yb - sp.height)))
    if 0.38 <= phase < 0.6 and Yc < 0.12:              # landing dust
        impact_lines(img, gx, cam.p(Xc, Z)[1], 0.0, (phase - 0.5) * 3, 8)
    hand_x = gx + side * (sp.width / 2 - 6 * s)
    return hand_x, yb - sp.height / 2

def ball_trail(img, cam, pts, a, length=0.12, n=4):
    """motion streaks that trail the ball along its own flight path (they show where it came from)"""
    if a <= 0.01:
        return
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    bx, by = cam.p(*at(pts, a))
    r = max(3, 0.11 * cam.k(at(pts, a)[1]))
    tx, ty = cam.p(*at(pts, max(0, a - length)))
    dx, dy = bx - tx, by - ty
    L = math.hypot(dx, dy) + 1e-3
    nx, ny = -dy / L, dx / L
    for i in range(n):
        off = (i - (n - 1) / 2) * r * 0.55
        sx, sy = bx + nx * off, by + ny * off
        ex, ey = tx + nx * off * 0.4, ty + ny * off * 0.4
        for k in range(6):   # tapered: thick and bright near the ball, fading behind it
            f0, f1 = k / 6, (k + 1) / 6
            d.line([(lerp(sx, ex, f0), lerp(sy, ey, f0)), (lerp(sx, ex, f1), lerp(sy, ey, f1))],
                   fill=(255, 255, 255, int(170 * (1 - f0))), width=max(1, int(r * 0.35 * (1 - f0))))
    img.alpha_composite(ov)


def pretty_arc(img, cam, pts, upto=1.0, from_=0.0, col=(255, 214, 60)):
    """smooth glowing shot curve: soft glow + dark edge + bright core, tapering with distance, arrow head at the end"""
    n = 120
    sp = [cam.p(*at(pts, lerp(from_, upto, i / n))) for i in range(n + 1)]
    zs = [at(pts, lerp(from_, upto, i / n))[1] for i in range(n + 1)]
    if len(sp) < 2:
        return
    wid = [clamp(0.06 * cam.k(z), 4, 14) for z in zs]
    glow_l = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_l)
    for i in range(n):
        gd.line([sp[i], sp[i + 1]], fill=col + (150,), width=int(wid[i] * 3.2))
    img.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(img)
    for i in range(n):
        d.line([sp[i], sp[i + 1]], fill=OL, width=int(wid[i] + 6))
    for i in range(n):
        d.line([sp[i], sp[i + 1]], fill=col, width=int(wid[i]))
    for i in range(n):
        d.line([sp[i], sp[i + 1]], fill=(255, 250, 220), width=max(1, int(wid[i] * 0.35)))
    for i in range(n + 1):   # round joints
        r = wid[i] / 2
        d.ellipse([sp[i][0] - r, sp[i][1] - r, sp[i][0] + r, sp[i][1] + r], fill=col)
    if upto >= 0.999:   # arrow head at the target
        (x0, y0), (x1, y1) = sp[-6], sp[-1]
        ang = math.atan2(y1 - y0, x1 - x0)
        hs = wid[-1] * 2.6 + 10
        tri = [(x1 + math.cos(ang) * hs * 0.6, y1 + math.sin(ang) * hs * 0.6),
               (x1 + math.cos(ang + 2.5) * hs, y1 + math.sin(ang + 2.5) * hs),
               (x1 + math.cos(ang - 2.5) * hs, y1 + math.sin(ang - 2.5) * hs)]
        d.polygon(tri, fill=col, outline=OL, width=4)
