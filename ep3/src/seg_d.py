"""Segment D (40.13-46.53): sirens on the street, ambulance interior, hospital corridor."""
from seg_c import *

VPX, VPY = 180, 250  # street vanishing point


def blue_phase(t, rate=5.0):
    """two alternating blue beacons: returns (left, right) intensities 0..1"""
    p = (t * rate) % 1.0
    return (1.0 if p < 0.5 else 0.15) * (0.8 + 0.2 * math.sin(t * 60)), (1.0 if p >= 0.5 else 0.15)


_d = {}


def street_static():
    """terraced red-brick houses converging to the vanishing point, wet road"""
    if "s" in _d:
        return _d["s"]
    c = Image.new("RGB", (CW, CH), NIGHT)
    d = ImageDraw.Draw(c)
    for y in range(0, VPY):
        F(d, 0, y, CW, 1, mix((8, 10, 28), (40, 36, 70), y / VPY))
    # far stadium glow at the end of the street
    for r in range(60, 0, -6):
        d.ellipse([VPX - r * 1.6, VPY - 40 - r * .6, VPX + r * 1.6, VPY - 40 + r * .6], fill=mix((40, 36, 70), (150, 150, 120), 1 - r / 60))
    for x in (VPX - 30, VPX + 30):
        floodlight(d, x, VPY - 70, 0.7)
    # road (trapezoid) and pavements
    d.polygon([(VPX - 6, VPY), (VPX + 6, VPY), (CW + 140, CH), (-140, CH)], fill=(40, 42, 56))
    for side in (-1, 1):
        d.polygon([(VPX + side * 6, VPY), (VPX + side * 12, VPY), (VPX + side * 330, CH), (VPX + side * 320 - side * 0, CH)],
                  fill=(70, 70, 84))
    # kerb lines + road markings (dashes)
    for k in range(14):
        z0, z1 = 1 / (1 + k * 0.55), 1 / (1 + k * 0.55 + 0.25)
        y0 = VPY + (CH - VPY) * z0
        y1 = VPY + (CH - VPY) * z1
        w0, w1 = 3 * z0, 3 * z1
        d.polygon([(VPX - w0, y0), (VPX + w0, y0), (VPX + w1, y1), (VPX - w1, y1)], fill=(220, 220, 200))
    # terraced houses: continuous brick walls converging to the vanishing point
    def wx(side, z):
        return VPX + side * (14 + 205 * z)

    def ybot(z):
        return VPY + (600 - VPY) * z

    def ytop(z):
        return VPY - 22 - (VPY - 22 - 50) * z

    for side in (-1, 1):
        zs = [1.15] + [1 / (1 + 0.55 * k) for k in range(1, 16)] + [0.0]
        for k in range(len(zs) - 1):
            za, zb = zs[k], zs[k + 1]
            xa, xb = wx(side, za), wx(side, zb)
            brick = (150, 62, 48) if k % 2 else (136, 56, 44)
            d.polygon([(xa, ybot(za)), (xb, ybot(zb)), (xb, ytop(zb)), (xa, ytop(za))], fill=brick)
            for j in range(1, 16):  # mortar courses converge to the VP
                f = j / 16
                d.line([(xa, lerp(ybot(za), ytop(za), f)), (xb, lerp(ybot(zb), ytop(zb), f))], fill=(116, 46, 38), width=1)
            d.line([(xa, ybot(za)), (xa, ytop(za))], fill=(100, 40, 34), width=max(1, int(3 * za)))  # party wall
            if zb < 0.05:
                continue
            # windows: two floors, lit or dark, with white sills
            for fl, lit in ((0.22, (k + (side > 0)) % 3 == 0), (0.58, (k + (side > 0)) % 2 == 0)):
                u0, u1 = 0.18, 0.62
                q = []
                for u, ff in ((u0, fl), (u1, fl), (u1, fl + 0.22), (u0, fl + 0.22)):
                    z = lerp(za, zb, u)
                    q.append((wx(side, z), lerp(ybot(z), ytop(z), ff)))
                d.polygon(q, fill=OL)
                inner = [(lerp(p[0], sum(x for x, _ in q) / 4, 0.12), lerp(p[1], sum(y for _, y in q) / 4, 0.12)) for p in q]
                d.polygon(inner, fill=(255, 214, 130) if lit else (40, 48, 74))
                d.line([q[0], q[1]], fill=(230, 226, 220), width=max(1, int(3 * za)))
            # front door
            q = []
            for u, ff in ((0.74, 0.0), (0.92, 0.0), (0.92, 0.17), (0.74, 0.17)):
                z = lerp(za, zb, u)
                q.append((wx(side, z), lerp(ybot(z), ytop(z), ff)))
            d.polygon(q, fill=[(30, 60, 110), (120, 30, 40), (30, 90, 60)][k % 3], outline=OL)
            # roof edge + chimney pots
            d.polygon([(xa, ytop(za)), (xb, ytop(zb)), (xb, ytop(zb) - 14 * zb), (xa, ytop(za) - 14 * za)], fill=(48, 44, 60))
            if k % 2 == 0:
                z = lerp(za, zb, .5)
                cw = 22 * z
                x = wx(side, z)
                y = ytop(z) - 14 * z
                F(d, x - cw / 2, y - cw * 1.3, cw, cw * 1.3, (120, 50, 40))
                F(d, x - cw / 3, y - cw * 1.6, cw / 3, cw * .4, (90, 40, 34))
        # pavement edge
        d.line([(wx(side, 1.15), ybot(1.15)), (VPX + side * 14, VPY)], fill=(90, 90, 104), width=2)
        # street lamps on the kerb
        for z in (0.8, 0.45, 0.28):
            x = VPX + side * (8 + 150 * z)
            yb = VPY + (CH - VPY) * z * 0.95
            h = 420 * z
            F(d, x - 3 * z, yb - h, max(1, 6 * z), h, (30, 30, 40))
            F(d, x - 12 * z, yb - h - 6 * z, 24 * z, 7 * z, (255, 236, 170))
    # bins, a parked car on the left
    R(d, 18, 520, 26, 40, (40, 70, 50), r=3)
    R(d, 48, 528, 22, 32, (60, 60, 70), r=3)
    R(d, -40, 560, 120, 50, (60, 80, 140), r=8)
    F(d, -30, 568, 90, 14, (150, 190, 230))
    R(d, 54, 598, 18, 18, OL, r=6)
    # puddles on the road (reflections drawn dynamically)
    img = up(c)
    _d["s"] = img
    return img


PUDDLES = [(250, 1000, 150, 26), (470, 1130, 190, 30), (330, 820, 90, 14), (130, 1180, 120, 22)]


def ambulance(d, cx, by, s, bl, br):
    """front view of an ambulance (canvas units)"""
    w, h = 70 * s, 64 * s
    x0, y0 = cx - w / 2, by - h
    R(d, x0, y0 + 10 * s, w, h - 10 * s, (245, 245, 240), r=int(4 * s))
    F(d, x0, y0 + 40 * s, w, 8 * s, (40, 160, 80))          # green battenburg band
    for k in range(0, 8):
        if k % 2 == 0:
            F(d, x0 + k * w / 8, y0 + 40 * s, w / 8, 8 * s, (250, 210, 40))
    R(d, x0 + 8 * s, y0 + 16 * s, w - 16 * s, 20 * s, (50, 80, 120), r=int(2 * s))  # windscreen
    F(d, x0 + 12 * s, y0 + 18 * s, 12 * s, 4 * s, (120, 170, 220))
    # wipers
    d.line([(x0 + 18 * s, y0 + 35 * s), (x0 + 32 * s, y0 + 22 * s)], fill=OL, width=max(1, int(s)))
    # roof light bar
    R(d, x0 + 10 * s, y0 + 4 * s, w - 20 * s, 6 * s, (40, 40, 60), r=int(s))
    F(d, x0 + 12 * s, y0 + 5 * s, 18 * s, 4 * s, mix((30, 40, 90), (120, 200, 255), bl))
    F(d, x0 + w - 30 * s, y0 + 5 * s, 18 * s, 4 * s, mix((30, 40, 90), (120, 200, 255), br))
    # headlights + grille
    for sx in (x0 + 6 * s, x0 + w - 16 * s):
        R(d, sx, y0 + 50 * s, 10 * s, 5 * s, (255, 250, 220), r=int(s))
    F(d, cx - 10 * s, y0 + 50 * s, 20 * s, 5 * s, (40, 40, 50))
    F(d, cx - 12 * s, y0 + 57 * s, 24 * s, 4 * s, (200, 200, 210))
    # wheels
    for sx in (x0 + 2 * s, x0 + w - 12 * s):
        R(d, sx, by - 4 * s, 10 * s, 6 * s, (20, 20, 26), r=int(2 * s))
    # AMBULANCE mirrored text bar
    F(d, x0 + 14 * s, y0 + 11 * s, w - 28 * s, 4 * s, (40, 160, 80))


def seg_D1(t):
    """40.13-42.63 street: sirens, rain, blue lights on wet bricks"""
    img = street_static().copy().convert("RGBA")
    bl, br = blue_phase(t)
    # puddles with reflections (on the road, under everything)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x, y, w, h in PUDDLES:
        od.ellipse([x - w, y - h, x + w, y + h], fill=(30, 40, 70, 200))
        od.ellipse([x - w * .6, y - h * .4, x + w * .2, y + h * .3], fill=(90, 170, 255, int(150 * max(bl, br))))
        od.line([(x - w * .5, y), (x + w * .4, y)], fill=(255, 240, 200, 150), width=3)
    img.alpha_composite(ov)
    # blue light washing over the brick walls: tint only brick-red pixels, alternating sides
    arr = np.asarray(img).astype(np.float32)
    r, g, b_ = arr[..., 0], arr[..., 1], arr[..., 2]
    brick = ((r > 100) & (r > g * 1.8) & (r > b_ * 1.8)).astype(np.float32)
    xs = np.linspace(0, 1, FW)[None, :]
    wash = brick * (bl * (xs < 0.5) + br * (xs >= 0.5)) * 0.55
    tint = np.array([70, 140, 255], np.float32)
    arr[..., :3] = arr[..., :3] * (1 - wash[..., None]) + tint * wash[..., None]
    img = Image.fromarray(arr.astype(np.uint8), "RGBA")
    u = ease_out((t - 40.13) / 0.82)
    sc = lerp(0.9, 2.35, u)
    by = lerp(400, 560, u)
    if t > 40.95:  # brake lurch
        by += 3 * math.exp(-(t - 40.95) * 8) * math.sin((t - 40.95) * 40)
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    ambulance(d, 182, by, sc, bl, br)
    if t > 41.3:  # paramedics bring the stretcher round
        k = ease_out((t - 41.3) / 1.0)
        px = lerp(300, 262, k)
        person_front(d, px - 62, 620, 2.2, (40, 140, 90), (25, 100, 60), skin=DSKIN, skin_d=DSKIN_D, hair=(25, 20, 20), t=t, look=(1, 0))
        person_front(d, px + 62, 620, 2.2, (40, 140, 90), (25, 100, 60), hair=(120, 80, 50), t=t, look=(-1, 0))
        for x in (px - 40, px + 36):
            F(d, x, 586, 3, 30, (160, 160, 170))
        R(d, px - 46, 576, 92, 10, (230, 232, 240), r=3)
        R(d, px - 14, 566, 58, 12, (70, 110, 200), r=3)
        grandad_head(d, px - 26, 546, 1.3, blink=True, smile=False)
    hero_back(d, 70, 720, 3.0, arms=0.1, t=t, look=0.5)
    img.alpha_composite(up(c))
    glow(img, int((182 - 22 * sc) * 2), int((by - 58 * sc) * 2), 90 * sc, (80, 160, 255), 0.45 * bl)
    glow(img, int((182 + 22 * sc) * 2), int((by - 58 * sc) * 2), 90 * sc, (80, 160, 255), 0.45 * br)
    rain(img, t, alpha=95, speed=1100)
    dd = ImageDraw.Draw(img)
    # location label
    lk = spring(t - 40.3, 14, 7)
    if lk > 0.05:
        f = font(800, 24)
        dd.rounded_rectangle([420, 300, 690, 344], 8, fill=(30, 60, 150), outline=OL, width=4)
        dd.text((555, 322), "RIVERSIDE ROAD", font=f, fill=(255, 255, 255), anchor="mm")
    img = img.convert("RGB")
    img = transform(img, 1.0 + 0.06 * (t - 40.13) / 2.5, *shake(t, 40.95, 0.25, 6), 360, 900)
    img = tint_vignette(img, 0.5, (4, 6, 20))
    overlay_text(img, t)
    return img


def seg_D2(t):
    """42.63-44.40 inside the ambulance, looking toward the cab; hero holds Grandad's hand"""
    c = Image.new("RGB", (CW, CH), (196, 204, 214))
    d = ImageDraw.Draw(c)
    vx, vy = 180, 300
    # back wall (cab partition) with a small window to the windscreen
    F(d, 110, 200, 140, 170, (176, 184, 196))
    R(d, 150, 220, 60, 40, (30, 40, 70), r=4)
    bl, br = blue_phase(t, 4)
    F(d, 152, 222, 56, 6, mix((30, 40, 70), (90, 160, 255), max(bl, br)))
    # ceiling, floor, side walls (one-point perspective)
    d.polygon([(0, 0), (CW, 0), (250, 200), (110, 200)], fill=(214, 220, 230))
    d.polygon([(0, CH), (CW, CH), (250, 370), (110, 370)], fill=(120, 126, 140))
    d.polygon([(0, 0), (110, 200), (110, 370), (0, CH)], fill=(186, 194, 206))
    d.polygon([(CW, 0), (250, 200), (250, 370), (CW, CH)], fill=(176, 184, 198))
    # floor grip lines
    for k in range(1, 8):
        d.line([(110 + k * 20, 370), (k * 51, CH)], fill=(108, 114, 128), width=1)
    # ceiling lights
    for k in range(3):
        z = 1 - k * 0.3
        w = 60 * z
        y = 200 - 170 * z + 10
        F(d, 180 - w / 2, y, w, 8 * z, (255, 255, 250))
    # cabinets with coloured labels on both walls (like the original, now in perspective)
    cols = [(220, 60, 70), (60, 120, 220), (240, 190, 40), (60, 170, 90)]
    for side in (-1, 1):
        for k in range(4):
            z0, z1 = 1 - k * 0.2, 1 - (k + 1) * 0.2
            xa = 180 + side * (70 + 110 * z0)
            xb = 180 + side * (70 + 110 * z1)
            ya, yb = 60 + (1 - z0) * 140, 60 + (1 - z1) * 140
            ha, hb = 120 * z0, 120 * z1
            d.polygon([(xa, ya), (xb, yb), (xb, yb + hb * .5), (xa, ya + ha * .5)], fill=(236, 240, 246), outline=(150, 156, 170))
            d.line([(lerp(xa, xb, .2), ya + ha * .08), (lerp(xa, xb, .7), yb + hb * .08)], fill=cols[(k + (side > 0)) % 4], width=max(2, int(6 * z0)))
    # heart monitor on the right wall
    R(d, 262, 150, 74, 48, (20, 26, 40), r=4)
    pts = []
    for i in range(0, 64, 2):
        x = 267 + i
        ph = (t * 1.1 + i / 64) % 1
        y = 180 - (14 if 0.45 < ph < 0.5 else (-6 if 0.5 < ph < 0.54 else 0))
        pts.append((x, y))
    d.line(pts, fill=(90, 230, 120), width=2)
    d.text((268, 154), "HR 58", fill=(90, 230, 120))
    # oxygen bottle
    R(d, 18, 300, 22, 90, (60, 170, 90), r=8)
    F(d, 22, 294, 14, 8, (200, 200, 210))
    # stretcher in the centre along the depth, feet near camera
    d.polygon([(110, 640), (250, 640), (220, 340), (140, 340)], fill=OL)
    d.polygon([(114, 640), (246, 640), (217, 344), (143, 344)], fill=(240, 242, 248))
    d.polygon([(118, 640), (242, 640), (214, 380), (146, 380)], fill=(70, 110, 200))  # blanket
    d.polygon([(118, 640), (150, 640), (156, 380), (146, 380)], fill=(56, 92, 176))
    for x in (150, 210):
        d.ellipse([x - 22, 590, x + 22, 640], fill=(60, 100, 190))  # feet bumps
    breathe = math.sin(t * 2.0) * 2
    d.polygon([(140, 420 - breathe), (220, 420 - breathe), (214, 380), (146, 380)], fill=(84, 124, 214))
    # pillow + Grandad's head at the far end (eyes closed, oxygen mask)
    R(d, 146, 318, 68, 30, (250, 250, 252), r=8)
    grandad_head(d, 180, 312, 1.9, blink=True, smile=False)
    R(d, 172, 336, 16, 10, (180, 220, 240), r=3)
    d.line([(188, 342), (250, 300)], fill=(160, 200, 220), width=2)
    # hero on the left bench, leaning in, holding his hand
    hero_front(d, 66, 520, 3.2, pose="sit", expr="worried", look=(1, 0.3), t=t, gloves=False, arms="lap",
               blink=(43.4 < t < 43.5))
    # Grandad's hand + hero's hand clasped (red bracelet visible)
    limb(d, (112, 470), (140, 452), 10, SKIN)
    R(d, 126, 444, 18, 16, SKIN, r=4)
    F(d, 104, 466, 14, 5, BRACE)
    # paramedic on the right bench
    person_front(d, 296, 520, 3.0, (40, 140, 90), (25, 100, 60), skin=DSKIN, skin_d=DSKIN_D, hair=(25, 20, 20),
                 t=t, look=(-1, 0))
    img = up(c).convert("RGBA")
    # blue light through the rear windows (we're at the doors): sweep on walls
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.polygon([(0, 0), (220, 400), (220, 740), (0, 1280)], fill=(60, 140, 255, int(50 * bl)))
    od.polygon([(720, 0), (500, 400), (500, 740), (720, 1280)], fill=(60, 140, 255, int(50 * br)))
    img.alpha_composite(ov)
    img = img.convert("RGB")
    sway = math.sin(t * 3.1) * 4
    img = transform(img, 1.04 + 0.04 * (t - 42.63) / 1.8, sway, math.sin(t * 5.3) * 2, 360, 700)
    img = tint_vignette(img, 0.35, (10, 14, 30))
    overlay_text(img, t)
    return img


def corridor_static():
    if "cor" in _d:
        return _d["cor"]
    c = Image.new("RGB", (CW, CH), (226, 234, 228))
    d = ImageDraw.Draw(c)
    vx, vy = 180, 300
    # far wall with double doors RESUS
    F(d, 130, 250, 100, 100, (206, 216, 210))
    R(d, 146, 268, 32, 82, (120, 170, 200))
    R(d, 182, 268, 32, 82, (120, 170, 200))
    F(d, 152, 280, 20, 14, (210, 236, 250))
    F(d, 188, 280, 20, 14, (210, 236, 250))
    R(d, 152, 254, 56, 10, (200, 40, 50), r=2)
    # ceiling / floor / walls
    d.polygon([(0, 0), (CW, 0), (230, 250), (130, 250)], fill=(236, 240, 238))
    d.polygon([(0, CH), (CW, CH), (230, 350), (130, 350)], fill=(170, 186, 184))
    d.polygon([(0, 0), (130, 250), (130, 350), (0, CH)], fill=(196, 222, 206))
    d.polygon([(CW, 0), (230, 250), (230, 350), (CW, CH)], fill=(186, 214, 198))
    # floor tiles (converging + horizontal)
    for k in range(-6, 7):
        d.line([(180 + k * 9, 350), (180 + k * 70, CH)], fill=(156, 172, 170), width=1)
    for k in range(1, 12):
        z = 1 / (1 + k * 0.45)
        y = 350 + (CH - 350) * z
        d.line([(0, y), (CW, y)], fill=(156, 172, 170), width=1)
    # handrails + skirting on walls
    for side in (-1, 1):
        x_far = 180 + side * 50
        d.line([(x_far, 318), (180 + side * 180, 520)], fill=(140, 120, 100), width=4)
        d.line([(x_far, 346), (180 + side * 180, 632)], fill=(120, 140, 136), width=6)
        # doors along the walls
        for k in range(3):
            z0, z1 = 1 / (1 + k * 0.9 + .3), 1 / (1 + k * 0.9 + .65)
            xa = 180 + side * (50 + 130 * z0 * 1.4)
            xb = 180 + side * (50 + 130 * z1 * 1.4)
            ya_b = 350 + (290 * z0 * 1.4)
            yb_b = 350 + (290 * z1 * 1.4)
            ha, hb = 380 * z0 * 1.2, 380 * z1 * 1.2
            d.polygon([(xa, ya_b), (xb, yb_b), (xb, yb_b - hb), (xa, ya_b - ha)], fill=(150, 180, 210), outline=(110, 130, 150))
            d.polygon([(lerp(xa, xb, .25), ya_b - ha * .85), (lerp(xa, xb, .75), lerp(ya_b, yb_b, .75) - lerp(ha, hb, .75) * .85),
                       (lerp(xa, xb, .75), lerp(ya_b, yb_b, .75) - lerp(ha, hb, .75) * .6), (lerp(xa, xb, .25), ya_b - ha * .6)],
                      fill=(220, 236, 244))
    # wall clock (left wall) and vending machine (right)
    R(d, 40, 140, 44, 44, (250, 250, 250), r=20)
    # vending machine
    d.polygon([(300, 300), (360, 250), (360, 560), (300, 520)], fill=(200, 40, 50))
    d.polygon([(306, 312), (350, 276), (350, 420), (306, 440)], fill=(240, 240, 200))
    # row of plastic chairs on the left
    for k in range(4):
        x = 20 + k * 52
        R(d, x, 470, 44, 36, (60, 110, 190), r=6)
        R(d, x, 506, 44, 12, (50, 96, 170), r=4)
        F(d, x + 4, 518, 4, 40, (90, 90, 100))
        F(d, x + 36, 518, 4, 40, (90, 90, 100))
    # wet footprints on the floor
    for k in range(6):
        x, y = 250 - k * 14, 620 - k * 30
        d.ellipse([x - 6, y - 3, x + 6, y + 3], fill=(150, 166, 170))
    img = up(c)
    _d["cor"] = img
    return img


def fluoro(t):
    """fluorescent flicker events at 45.0 and 45.85 (sound hits)"""
    for t0 in (45.0, 45.85):
        if t0 <= t < t0 + 0.18:
            return 0.35 if int((t - t0) * 40) % 2 == 0 else 1.0
    return 1.0


def seg_D3(t):
    """44.40-46.53 hospital corridor: white lights, waiting"""
    img = corridor_static().copy()
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    fl = fluoro(t)
    # ceiling light panels (converging)
    for k in range(5):
        z = 1 / (1 + k * 0.6)
        w = 80 * z
        y = 250 - 230 * z + 8
        F(d, 180 - w / 2, y, w, 14 * z, mix((150, 156, 160), (255, 255, 252), fl if k == 1 else 1.0))
    # clock hands (moving second hand)
    cx, cy = 62, 162
    ang = (t * 6) % 360
    d.line([(cx, cy), (cx + 12 * math.sin(math.radians(ang)), cy - 12 * math.cos(math.radians(ang)))], fill=(220, 40, 40), width=1)
    d.line([(cx, cy), (cx + 8, cy - 4)], fill=OL, width=2)
    d.line([(cx, cy), (cx - 2, cy - 14)], fill=OL, width=2)
    # IN USE light over doors (blinking)
    if int(t * 2) % 2 == 0:
        F(d, 176, 240, 8, 6, (255, 80, 80))
    # nurse crossing far end
    nk = (t - 45.1) / 1.4
    if 0 <= nk <= 1:
        person_front(d, lerp(120, 250, nk), 352, 1.6, (90, 150, 220), (60, 110, 180), hair=(60, 40, 30), t=t,
                     hairstyle="pony")
    # hero alone on a chair: small, head down, gloves in lap (high-angle feeling)
    hero_front(d, 92, 552, 2.8, pose="sit", expr="sad", look=(0, 1), t=t, gloves=True, arms="lap",
               blink=(45.6 < t < 45.75))
    img = img.convert("RGBA")
    img.alpha_composite(up(c))
    if fl < 1:
        img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (30, 40, 40)), 0.25).convert("RGBA")
    dd = ImageDraw.Draw(img)
    dd.text((360, 518), "RESUS", font=font(800, 18), fill=(255, 255, 255), anchor="mm")
    img = img.convert("RGB")
    img = transform(img, 1.0 + 0.07 * ease_in_out((t - 44.4) / 2.1), 0, 0, 200, 1000)
    img = tint_vignette(img, 0.5, (20, 30, 40))
    overlay_text(img, t)
    return img


def seg_D(t):
    if t < 42.63:
        return seg_D1(t)
    if t < 44.40:
        return seg_D2(t)
    return seg_D3(t)
