"""Segment E (46.53-57.60): phone buzzes, trial message, final choice at the crossroads."""
from seg_d import *


def seg_E1(t):
    """46.53-48.60 corridor mid-shot, phone buzzes in his lap"""
    img = corridor_static().copy()
    img = transform(img, 1.9, 0, -40, 180, 1060).filter(ImageFilter.GaussianBlur(2.5))
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    buzz = 47.55 <= t < 48.45
    jx = (math.sin(t * 160) * 2.5) if buzz else 0
    look = (0, 1) if t > 47.6 else (0.3, 0.2)
    hero_front(d, 180, 690, 7.6, pose="sit", expr="sad" if t < 47.6 else "shock", look=look, t=t,
               gloves=False, arms="lap", blink=(46.9 < t < 47.0))
    # gloves resting on the next chair
    R(d, 300, 560, 46, 40, ORG, r=10)
    F(d, 300, 586, 46, 14, ORG_D)
    # phone in his hands
    px, py = 180 + jx, 588
    R(d, px - 26, py - 40, 52, 80, (28, 30, 42), r=8)
    lit = t > 47.55
    F(d, px - 21, py - 34, 42, 68, (110, 180, 250) if lit else (20, 24, 36), r=4)
    img = img.convert("RGBA")
    img.alpha_composite(up(c))
    if lit:
        glow(img, int(px * 2), int((py - 70) * 2), 260, (120, 190, 255), 0.35)
        dd = ImageDraw.Draw(img)
        for k in range(3):  # buzz lines
            if buzz:
                for sgn in (-1, 1):
                    x = px * 2 + sgn * (70 + k * 18)
                    dd.line([(x, py * 2 - 40 - k * 6), (x, py * 2 + 40 + k * 6)], fill=(255, 255, 255), width=5)
    img = img.convert("RGB")
    img = transform(img, 1 + 0.06 * (t - 46.53) / 2, *shake(t, 47.55, 0.3, 4), 360, 1100)
    img = tint_vignette(img, 0.45, (10, 16, 30))
    overlay_text(img, t)
    return img


def notif(img, x, y, w, h, k, title, body, color, icon=None):
    if k <= 0.01:
        return
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(250, 250, 252, 248))
    d.rounded_rectangle([18, 18, 18 + h - 36, h - 18], 14, fill=color)
    if icon:
        icon(d, 18 + (h - 36) / 2, h / 2)
    d.text((h + 4, h * 0.36), title, font=font(800, 22), fill=(120, 124, 140), anchor="lm")
    d.text((h + 4, h * 0.66), body, font=font(800, 27), fill=(20, 22, 34), anchor="lm")
    sc = k
    card = card.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR)
    img.paste(card, (int(x + w / 2 - card.width / 2), int(y + h / 2 - card.height / 2)), card)


def ico_ball(d, cx, cy):
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 255, 255), outline=OL, width=3)
    d.regular_polygon((cx, cy, 9), 5, fill=OL)


def ico_cal(d, cx, cy):
    d.rounded_rectangle([cx - 22, cy - 20, cx + 22, cy + 22], 6, fill=(255, 255, 255))
    d.rectangle([cx - 22, cy - 20, cx + 22, cy - 8], fill=(238, 78, 79))
    d.text((cx, cy + 8), "SAT", font=font(800, 15), fill=OL, anchor="mm")


def ico_eye(d, cx, cy):
    d.ellipse([cx - 24, cy - 13, cx + 24, cy + 13], fill=(255, 255, 255))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=OL)


def seg_E2(t):
    """48.60-52.37 close-up: phone in his hands, messages pop in"""
    img = corridor_static().copy()
    img = transform(img, 1.5, 0, 0, 360, 700).filter(ImageFilter.GaussianBlur(9))
    img = Image.blend(img, Image.new("RGB", img.size, (20, 26, 40)), 0.45).convert("RGBA")
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # hands + wrists holding the phone (bracelet on his RIGHT wrist = screen left when we look over his hands)
    for sgn in (-1, 1):
        limb(d, (180 + sgn * 150, 700), (180 + sgn * 112, 560), 40, SKIN)
    F(d, 52, 600, 40, 14, BRACE)
    # phone body
    pw, ph = 236, 440
    px, py = 180 - pw / 2, 150
    R(d, px, py, pw, ph, (24, 26, 36), r=26, ow=2)
    F(d, px + 10, py + 12, pw - 20, ph - 24, (14, 20, 46), r=18)
    # fingers over the edges
    for sgn in (-1, 1):
        for k in range(3):
            R(d, 180 + sgn * (pw / 2 + 2) - (14 if sgn > 0 else 0), 420 + k * 34, 16, 26, SKIN, r=6)
    R(d, 180 - pw / 2 - 18, 540, 40, 30, SKIN, r=8)
    R(d, 180 + pw / 2 - 22, 540, 40, 30, SKIN, r=8)
    img.alpha_composite(up(c))
    dd = ImageDraw.Draw(img)
    # lock screen
    sx0, sy0 = (px + 10) * 2, (py + 12) * 2
    swid = (pw - 20) * 2
    dd.text((360, sy0 + 110), "23:12", font=font(700, 92), fill=(255, 255, 255), anchor="mm")
    dd.text((360, sy0 + 178), "Thursday", font=font(600, 28), fill=(200, 210, 240), anchor="mm")
    # mini week strip with Saturday circled (from 49.57)
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for i, dname in enumerate(days):
        x = sx0 + 36 + i * (swid - 72) / 6
        y = sy0 + 236
        col = (238, 78, 79) if i == 5 else (190, 196, 220)
        dd.text((x, y), dname, font=font(700, 24), fill=col, anchor="mm")
        if i == 3:
            dd.rounded_rectangle([x - 22, y + 18, x + 22, y + 42], 8, fill=(80, 90, 140))
            dd.text((x, y + 30), "NOW", font=font(800, 13), fill=(255, 255, 255), anchor="mm")
    if t > 49.57:
        k = clamp((t - 49.57) / 0.35)
        x = sx0 + 36 + 5 * (swid - 72) / 6
        y = sy0 + 236
        dd.arc([x - 34, y - 32, x + 34, y + 32], -90, -90 + 360 * k, fill=(238, 78, 79), width=6)
    # notifications
    notif(img, 150, sy0 + 320, 420, 108, spring(t - 48.65, 14, 7), "RIVERSIDE ACADEMY", "TRIAL", (40, 150, 80), ico_ball)
    notif(img, 150, sy0 + 444, 420, 108, spring(t - 49.57, 14, 7), "REMINDER", "SAT · 10:00", (238, 78, 79), ico_cal)
    notif(img, 150, sy0 + 568, 420, 108, spring(t - 50.72, 14, 7), "COACH", "Scouts are watching.", (40, 90, 200), ico_eye)
    # countdown badge
    if t > 51.5:
        pill_label(img, 560, sy0 + 40, "2 DAYS LEFT", (200, 50, 60), spring(t - 51.5, 14, 7), 28)
    glow(img, 360, 640, 360, (110, 160, 255), 0.18)
    img = img.convert("RGB")
    jx = math.sin(t * 150) * 3 if 48.6 <= t < 48.9 else 0
    img = transform(img, 1.0 + 0.05 * (t - 48.6) / 3.8, jx, 0, 360, 700)
    img = tint_vignette(img, 0.45, (6, 8, 20))
    overlay_text(img, t)
    return img


_e = {}


def cross_static():
    """night street outside the hospital: hospital on the left, road to the floodlit stadium on the right"""
    if "x" in _e:
        return _e["x"]
    c = Image.new("RGB", (CW, CH), NIGHT)
    d = ImageDraw.Draw(c)
    for y in range(0, 330):
        F(d, 0, y, CW, 1, mix((8, 10, 28), (36, 34, 66), y / 330))
    # stadium glow far right
    for r in range(80, 0, -6):
        d.ellipse([290 - r * 1.4, 250 - r * .5, 290 + r * 1.4, 250 + r * .5], fill=mix((36, 34, 66), (190, 190, 150), 1 - r / 80))
    for x in (250, 330):
        F(d, x - 1, 196, 2, 60, (40, 40, 60))
        floodlight(d, x, 192, 0.9)
    F(d, 230, 252, 120, 30, (60, 60, 80))  # stadium stand silhouette
    # hospital building on the left (big, in perspective)
    d.polygon([(0, 60), (150, 170), (150, 380), (0, 470)], fill=(200, 206, 214))
    for r_ in range(6):
        for col in range(5):
            u0, u1 = col / 5 + .04, (col + 1) / 5 - .04
            ft, fb = 0.1 + r_ * 0.13, 0.1 + r_ * 0.13 + 0.08
            def P(u, f):
                x = lerp(0, 150, u)
                yt = lerp(60, 170, u)
                yb = lerp(470, 380, u)
                return (x, lerp(yt, yb, f))
            lit = (r_ * 5 + col) % 4 != 0
            if r_ == 3 and col == 3:
                colr = (255, 236, 160)  # Grandad's room
            else:
                colr = (190, 220, 240) if lit else (70, 80, 110)
            d.polygon([P(u0, ft), P(u1, ft), P(u1, fb), P(u0, fb)], fill=colr)
    # red H sign + name
    R(d, 112, 300, 26, 26, (220, 40, 50), r=4)
    F(d, 118, 305, 3, 16, WHT)
    F(d, 128, 305, 3, 16, WHT)
    F(d, 118, 311, 13, 3, WHT)
    # entrance canopy glowing
    d.polygon([(40, 400), (150, 352), (150, 380), (40, 440)], fill=(255, 240, 200))
    # road splitting: left to hospital doors, right to the stadium
    d.polygon([(0, CH), (CW, CH), (330, 300), (250, 300), (160, 380), (60, 450)], fill=(40, 42, 56))
    d.polygon([(250, 300), (330, 300), (360, 330), (360, 300)], fill=(40, 42, 56))
    # pavement / kerbs
    d.polygon([(0, 470), (60, 450), (160, 380), (150, 382), (0, 480)], fill=(90, 90, 104))
    # parked ambulance by the entrance
    ambulance(d, 96, 452, 0.9, 0.2, 0.2)
    # puddles
    for x, y, w, h in ((120, 560, 60, 10), (260, 520, 40, 7), (200, 610, 80, 12)):
        d.ellipse([x - w, y - h, x + w, y + h], fill=(30, 40, 70))
        F(d, x - w * .5, y - 1, w * .7, 2, (200, 210, 240))
    # street lamps
    for x, y, h in ((180, 380, 120), (320, 330, 70)):
        F(d, x - 1, y - h, 3, h, (30, 30, 40))
        F(d, x - 8, y - h - 4, 16, 5, (255, 236, 170))
    img = up(c)
    _e["x"] = img
    return img


def choice_card(img, x, y, w, h, title, sub, color, k, icon_fn, glowk=0.0):
    if k <= 0.01:
        return
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(14, 18, 44, 240), outline=color, width=6 + int(4 * glowk))
    icon_fn(d, w / 2, h * 0.36)
    d.text((w / 2, h * 0.70), title, font=font(800, 38), fill=color, anchor="mm", stroke_width=3, stroke_fill=OL)
    d.text((w / 2, h * 0.86), sub, font=font(700, 19), fill=(220, 224, 240), anchor="mm")
    sc = k * (1 + 0.05 * glowk * math.sin(glowk * 10))
    card = card.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR)
    img.paste(card, (int(x - card.width / 2), int(y - card.height / 2)), card)


def ico_bed(d, cx, cy):
    d.rounded_rectangle([cx - 70, cy - 10, cx + 70, cy + 22], 6, fill=(230, 232, 240))
    d.rounded_rectangle([cx - 70, cy - 22, cx - 34, cy - 4], 6, fill=(255, 255, 255))
    d.rounded_rectangle([cx - 30, cy - 18, cx + 70, cy + 4], 6, fill=(70, 110, 200))
    d.ellipse([cx - 62, cy - 40, cx - 34, cy - 14], fill=SKIN)
    d.rounded_rectangle([cx - 62, cy - 26, cx - 36, cy - 12], 6, fill=BEARD)
    # heart
    hx, hy = cx + 50, cy - 46
    d.ellipse([hx - 16, hy - 12, hx, hy + 4], fill=(238, 78, 79))
    d.ellipse([hx - 2, hy - 12, hx + 14, hy + 4], fill=(238, 78, 79))
    d.polygon([(hx - 16, hy - 2), (hx + 14, hy - 2), (hx - 1, hy + 16)], fill=(238, 78, 79))


def ico_goal(d, cx, cy):
    d.rectangle([cx - 70, cy - 36, cx + 70, cy + 24], outline=(255, 255, 255), width=5)
    for k in range(1, 7):
        d.line([(cx - 70 + k * 20, cy - 36), (cx - 70 + k * 20, cy + 24)], fill=(160, 170, 200), width=1)
    for k in range(1, 3):
        d.line([(cx - 70, cy - 36 + k * 20), (cx + 70, cy - 36 + k * 20)], fill=(160, 170, 200), width=1)
    d.ellipse([cx + 20, cy - 20, cx + 44, cy + 4], fill=(255, 255, 255), outline=OL, width=2)
    # scouts with clipboards
    for k, x in enumerate((cx - 50, cx - 20)):
        d.ellipse([x - 8, cy + 30, x + 8, cy + 46], fill=SKIN)
        d.rectangle([x - 10, cy + 46, x + 10, cy + 64], fill=(40, 44, 70))


def seg_E3(t):
    """52.37-57.60 the choice: GRANDAD (left, hospital) or TRIAL (right, stadium)"""
    img = cross_static().copy().convert("RGBA")
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # hero in the middle, back view, looking left/right on "WHAT DO YOU DO?"
    look = 0.0
    if t > 54.85:
        look = math.sin((t - 54.85) * 4.2) * 1.0
    elif t > 53.4:
        look = -0.8
    elif t > 52.6:
        look = 0.8
    hero_back(d, 180, 712, 3.6, arms=0.15, t=t, look=look)
    img.alpha_composite(up(c))
    # trajectories drawn on the wet road
    if t > 52.45:
        dashed_arrow(img, [(360, 860), (300, 780), (210, 730), (130, 700)], clamp((t - 52.45) / 0.45), 1, C_B, width=12)
        dashed_arrow(img, [(360, 860), (430, 760), (520, 680), (590, 600)], clamp((t - 52.45) / 0.45), 1, C_Y, width=12)
    gk = clamp((t - 53.9) / 0.4) * (1 if t < 54.8 else 0.4)
    tk = clamp((t - 52.63) / 0.3) * (1 if t < 53.4 else 0.4)
    choice_card(img, 170, 540, 290, 260, "GRANDAD", "STAY AT THE HOSPITAL", C_B, spring(t - 52.45, 13, 7), ico_bed, gk)
    choice_card(img, 550, 470, 290, 260, "TRIAL", "PLAY FOR THE SCOUTS", C_Y, spring(t - 52.55, 13, 7), ico_goal, tk)
    # deadline badge
    if t > 52.7:
        pill_label(img, 360, 330, "VOTE BEFORE SATURDAY", (200, 50, 60), spring(t - 52.7, 14, 7), 30)
    # mock comment box sliding up
    if t > 55.77:
        k = ease_out((t - 55.77) / 0.35)
        y = lerp(1300, 1090, k)
        dd = ImageDraw.Draw(img)
        dd.rounded_rectangle([40, y, 680, y + 150], 26, fill=(250, 250, 252), outline=OL, width=4)
        dd.ellipse([64, y + 30, 124, y + 90], fill=(110, 222, 120))
        dd.text((94, y + 60), "U", font=font(800, 30), fill=(255, 255, 255), anchor="mm")
        dd.text((144, y + 40), "you", font=font(700, 22), fill=(120, 124, 140), anchor="lm")
        msg = "GRANDAD... or TRIAL?"
        n = int(len(msg) * clamp((t - 56.0) / 1.0))
        dd.text((144, y + 80), msg[:n] + ("|" if int(t * 4) % 2 == 0 else ""), font=font(800, 32), fill=(20, 22, 34), anchor="lm")
        dd.text((144, y + 122), "Comment your choice below", font=font(600, 22), fill=(110, 116, 140), anchor="lm")
    rain(img, t, alpha=80)
    img = img.convert("RGB")
    img = transform(img, 1.0 + 0.04 * (t - 52.37) / 5.2, *shake(t, 52.45, 0.25, 7), 360, 800)
    img = flash(img, 0.4 * clamp(1 - (t - 52.45) / 0.1) if t >= 52.45 else 0)
    img = tint_vignette(img, 0.45, (4, 6, 20))
    overlay_text(img, t)
    return img


def seg_E(t):
    if t < 48.60:
        return seg_E1(t)
    if t < 52.37:
        return seg_E2(t)
    return seg_E3(t)
