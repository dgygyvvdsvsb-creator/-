"""Segment C (32.33-36.53): Grandad — 'Good dive, son. Wrong side. Next time.'"""
from seg_pen import *

RMS = ENV[0] / np.percentile(ENV[0], 98)


def rms_at(t):
    i = int(t / 0.05)
    return float(np.clip(RMS[min(i, len(RMS) - 1)], 0, 1.2))


def talk(t, ranges):
    """mouth opening from the voice envelope, only while Grandad's words are spoken"""
    for a, b in ranges:
        if a <= t <= b:
            return clamp((rms_at(t) - 0.15) * 1.6) * (0.6 + 0.4 * abs(math.sin(t * 22)))
    return 0.0


_cache = {}


def stand_bg_close():
    """blurred crowd behind Grandad (close-up)"""
    if "c" in _cache:
        return _cache["c"]
    c = Image.new("RGB", (CW, CH), (60, 44, 50))
    d = ImageDraw.Draw(c)
    stands(d, 0, 0, CW, CH, 0, rows=22, seed=21, scale=1.6)
    img = up(c).filter(ImageFilter.GaussianBlur(7))
    _cache["c"] = img
    return img


def seat_row(d, y, s, n=4, x0=-20, gap=None):
    gap = gap or 32 * s
    for k in range(n):
        x = x0 + k * gap
        R(d, x, y, 28 * s, 22 * s, RED, r=int(3 * s))
        F(d, x + 20 * s, y, 8 * s, 22 * s, RED_D)
        F(d, x + 3 * s, y + 2 * s, 4 * s, 14 * s, RED_L)


def seg_C1(t):
    """close-up: Grandad smiling, talking, thumbs up (his right hand = screen left)"""
    img = stand_bg_close().copy()
    z = 1 + 0.05 * (t - 32.33) / 2.24
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    s = 8.4
    cx, hy = 186, 220
    # seat back behind him
    R(d, cx - 120, 300, 240, 400, (150, 40, 52), r=18)
    F(d, cx + 70, 300, 50, 400, (118, 30, 42))
    F(d, cx - 108, 312, 14, 200, (180, 64, 74))
    # body: cardigan down to the bottom of the frame
    ty = hy + 17 * s
    R(d, cx - 13 * s, ty, 26 * s, 60 * s, CARD, r=int(2 * s))
    F(d, cx + 6 * s, ty, 7 * s, 60 * s, CARD_D)
    F(d, cx - 11 * s, ty + 2 * s, 2.5 * s, 40 * s, CARD_L)
    F(d, cx - 3 * s, ty, 6 * s, 5 * s, (238, 232, 214))
    F(d, cx - .5 * s, ty + 5 * s, 1 * s, 50 * s, CARD_D)
    for k in range(5):
        F(d, cx - 1.2 * s, ty + 6 * s + k * 4 * s, 2.4 * s, 2.4 * s, BTN)
    # scarf in club green (detail)
    R(d, cx - 9 * s, ty - 1 * s, 18 * s, 4 * s, GRN, r=int(s))
    F(d, cx + 2 * s, ty - 1 * s, 4 * s, 4 * s, (240, 240, 240))
    R(d, cx - 8 * s, ty + 3 * s, 4 * s, 12 * s, GRN, r=int(s))
    talk_k = talk(t, [(32.48, 33.25), (33.45, 34.0)])
    blink = 33.05 < t < 33.14
    grandad_head(d, cx, hy + math.sin(t * 2) * 0.6, s, mouth_open=talk_k, blink=blink, look=(0.2, 0))
    # thumbs-up: arm from his right shoulder (screen left) rising
    k = ease_out((t - 32.40) / 0.35)
    sh = (cx - 12 * s, ty + 6 * s)
    hx, hyy = 52, lerp(700, 330, k)
    limb(d, sh, (hx + 6, hyy + 60), 34, CARD)
    R(d, hx - 26, hyy, 52, 50, SKIN, r=8)
    F(d, hx + 12, hyy, 14, 50, SKIN_D)
    for j in range(3):
        F(d, hx - 26, hyy + 12 + j * 12, 34, 2, SKIN_D)
    R(d, hx - 22, hyy - 40, 18, 44, SKIN, r=8)  # thumb
    F(d, hx - 19, hyy - 37, 6, 12, SKIN_L)
    img = img.convert("RGBA")
    img.alpha_composite(up(c))
    rain(img, t, alpha=65)
    img = img.convert("RGB")
    img = transform(img, z, 0, 0, 380, 560)
    img = tint_vignette(img, 0.4, (10, 6, 16))
    overlay_text(img, t)
    return img


_c2 = {}


def c2_bg():
    if "bg" in _c2:
        return _c2["bg"]
    c = Image.new("RGB", (CW, CH), NIGHT)
    d = ImageDraw.Draw(c)
    for x in (60, 300):
        floodlight(d, x, 30, 1.4)
    stands(d, 0, 46, CW, 250, 0, rows=12, seed=9, scale=1.2)
    img = up(c).filter(ImageFilter.GaussianBlur(3.5))
    _c2["bg"] = img
    return img


def seg_C2(t):
    """low angle from the pitch: the hero (back) looks up at Grandad in the front row"""
    img = c2_bg().copy()
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # front row: concrete step, seats, Mum + Grandad (seated)
    F(d, 0, 300, CW, 120, (58, 60, 78))
    F(d, 0, 300, CW, 4, (90, 92, 110))
    seat_row(d, 250, 2.6, n=5, x0=-40, gap=88)
    person_front(d, 286, 384, 3.0, BLUE, BLUE_D, hair=MUMH, hairstyle="pony", expr="smile", t=t,
                 blink=(35.6 < t < 35.7), look=(-1, 0))
    gx = 176
    grandad_body(d, gx, 300, 3.0)
    F(d, 0, 352, CW, 32, (60, 62, 80))
    F(d, 0, 352, CW, 3, (84, 86, 104))
    wink = t > 36.15
    grandad_head(d, gx, 246, 3.0, mouth_open=talk(t, [(34.6, 35.4), (36.03, 36.5)]), wink=wink, look=(-.6, .3))
    # cane raised, pointing to the screen-left (the side the ball went)
    pk = ease_out((t - 34.62) / 0.3)
    ang = math.radians(lerp(80, 155, pk))
    hx, hy = gx - 44, 318
    ex, ey = hx + math.cos(ang) * 100, hy - math.sin(ang) * 100
    limb(d, (gx - 30, 316), (hx, hy), 14, CARD)
    d.line([(hx, hy), (ex, ey)], fill=OL, width=8)
    d.line([(hx, hy), (ex, ey)], fill=(130, 80, 38), width=5)
    R(d, hx - 6, hy - 6, 12, 12, SKIN, r=3)
    # railing + ad board (foreground of the stand)
    F(d, 0, 384, CW, 6, (220, 224, 236))
    for x in range(0, CW, 22):
        F(d, x, 390, 4, 40, (200, 204, 220))
    F(d, 0, 426, CW, 30, (240, 200, 40))
    F(d, 120, 426, 120, 30, (40, 150, 80))
    F(d, 240, 426, 120, 30, (220, 40, 50))
    # pitch strip
    F(d, 0, 456, CW, CH - 456, (56, 128, 58))
    for k in range(4):
        F(d, 0, 470 + k * 44, CW, 22, (62, 136, 62))
    d.ellipse([-40, 540, 400, 700], fill=(104, 86, 54))
    d.ellipse([20, 500, 120, 520], fill=(84, 112, 140))
    F(d, 40, 508, 40, 2, (200, 220, 240))
    for x in (300, 314):
        R(d, x, 468, 8, 20, (90, 180, 240), r=2)
    R(d, 20, 470, 40, 16, (30, 34, 60), r=4)
    F(d, 26, 473, 14, 3, GRN)
    # hero from behind, big, bottom-right, gloves on
    hero_back(d, 250, 760, 4.6, arms=0.25, crouch=0.0, t=t, look=-0.2 if t > 34.7 else 0)
    img = img.convert("RGBA")
    img.alpha_composite(up(c))
    dd = ImageDraw.Draw(img)
    f = font(800, 30)
    for x, lab in ((120, "GO KEEPERS"), (360, "RIVERSIDE"), (600, "PIE SHOP")):
        dd.text((x, 882), lab, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=OL)
    if t > 34.62:
        dashed_arrow(img, [(250, 560), (150, 600), (60, 660)], clamp((t - 34.62) / 0.3), 1, C_R, width=12)
        pill_label(img, 160, 470, "WRONG SIDE", (200, 50, 60), spring(t - 34.65, 14, 7), 34)
    if t > 36.07:
        pill_label(img, 470, 470, "NEXT TIME", (40, 150, 80), spring(t - 36.07, 14, 7), 34)
    rain(img, t, alpha=70)
    img = img.convert("RGB")
    img = transform(img, 1 + 0.05 * (t - 34.57) / 2, 0, 0, 440, 640)
    img = tint_vignette(img, 0.45, (6, 6, 20))
    overlay_text(img, t)
    return img


def seg_C(t):
    return seg_C1(t) if t < 34.57 else seg_C2(t)
