"""Segment H (0.00-3.53): new hook. Frame 0 already in action.
'LAST MINUTE. ONE KICK. EVERYTHING.'"""
import subprocess
import lib
import seg_e
import seg_d
import seg_pen
from seg_e import *

KICK_T = 1.55

# hook caption: words never dim (frame 0 is the preview), key words take colour when spoken
lib.PHRASES.insert(0, (0.0, [("LAST", 0.0, C_W), ("MINUTE.", 0.0, C_W), ("ONE", 0.0, C_W), ("KICK.", 1.60, C_R),
                             ("EVERYTHING.", 2.55, C_Y)]))
_orig_draw = lib.draw_caption


def _draw_caption(img, words, t):
    if words and words[0][0] == "LAST":
        # before its time a key word is white (not dim); at frame 0 everything is already coloured
        ww = [(w, -1, c if (t < 0.25 or t >= st) else C_W)
              for w, st, c in words]
        lib.WRAP = 660
        try:
            return _orig_draw(img, ww, t)
        finally:
            lib.WRAP = 560
    return _orig_draw(img, words, t)


lib.draw_caption = _draw_caption

_src = {}


def src_frame(t):
    """a frame of the ORIGINAL episode (used for the montage; Grandad stays the original design)"""
    k = round(t, 3)
    if k not in _src:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", "src.mp4", "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _src[k] = Image.frombytes("RGB", (FW, FH), raw)
    return _src[k]


def no_caps(fn, t, clean=False):
    mods = [seg_e, seg_d, seg_pen, lib]
    saved = [m.overlay_text for m in mods]
    extra = (seg_pen.pill_label, seg_pen.dashed_arrow, seg_pen.ecg)
    for m in mods:
        m.overlay_text = lambda img, tt: None
    if clean:  # no LEFT/arrows/heart monitor: keep the hook spoiler-free
        seg_pen.pill_label = lambda *a, **k: None
        seg_pen.dashed_arrow = lambda *a, **k: None
        seg_pen.ecg = lambda *a, **k: None
    try:
        return fn(t)
    finally:
        for m, s in zip(mods, saved):
            m.overlay_text = s
        seg_pen.pill_label, seg_pen.dashed_arrow, seg_pen.ecg = extra


def score_bar(img, t, y=300):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, y, 630, y + 64], 14, fill=(14, 16, 30), outline=(255, 255, 255), width=3)
    d.rectangle([96, y + 6, 112, y + 58], fill=GRN)
    d.rectangle([608, y + 6, 624, y + 58], fill=RED)
    d.text((130, y + 32), "YOU", font=font(800, 30), fill=(255, 255, 255), anchor="lm")
    d.text((590, y + 32), "RIVERS", font=font(800, 30), fill=(255, 255, 255), anchor="rm")
    d.rounded_rectangle([300, y + 8, 420, y + 56], 8, fill=(255, 255, 255))
    d.text((360, y + 32), "0 - 0", font=font(800, 32), fill=OL, anchor="mm")
    blink = int(t * 4) % 2 == 0
    d.rounded_rectangle([308, y + 60, 412, y + 96], 8, fill=(220, 40, 50) if blink else (170, 30, 40))
    d.text((360, y + 78), "90+3'", font=font(800, 26), fill=(255, 255, 255), anchor="mm")


def shot1(t):
    """0.00-0.55 frozen mid-dive behind the net: ball at the fingertips. Saved or not?"""
    # reuse the behind-the-net set at a moment where the ball is right at the glove
    base = no_caps(seg_pen.seg_B4, 17.55 + t * 0.35, clean=True)
    img = transform(base, 1.18 + 0.12 * t, -40 * t, 0, 300, 560)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(int(t * 60))
    for _ in range(26):  # speed streaks
        y = rr.uniform(300, 1200)
        x = rr.uniform(0, 720)
        d.line([(x, y), (x + rr.uniform(80, 220), y - 30)], fill=(255, 255, 255, 70), width=3)
    score_bar(img, t, 290)
    img = img.convert("RGB")
    return img


def shot2(t):
    """0.55-1.10 keeper's view: snap-zoom onto Mason starting his run-up"""
    u = (t - 0.55) / 0.55
    base = no_caps(seg_pen.seg_B1, 9.6 + u * 0.5, clean=True)
    z = 1.0 + 0.9 * ease_out(u * 1.4)
    img = transform(base, z, 0, 0, 362, 470)
    img = img.convert("RGBA")
    score_bar(img, t, 1040)
    return img.convert("RGB")


def boot_layer(t):
    """extreme close-up: Mason's boot smashes the ball (contact at KICK_T)"""
    c = Image.new("RGB", (CW, CH), (50, 110, 52))
    d = ImageDraw.Draw(c)
    # wet grass close-up with blades, chalk spot, mud
    rng = random.Random(3)
    for y in range(300, CH, 6):
        F(d, 0, y, CW, 3, (46, 104, 48) if (y // 6) % 2 else (56, 122, 58))
    for _ in range(260):
        x, y = rng.uniform(0, CW), rng.uniform(320, CH)
        h = rng.uniform(6, 22)
        d.line([(x, y), (x + rng.uniform(-4, 4), y - h)], fill=rng.choice([(70, 150, 70), (40, 96, 44), (90, 170, 90)]), width=2)
    d.ellipse([100, 470, 270, 520], fill=(236, 240, 236))  # penalty spot (huge, close)
    d.ellipse([10, 520, 140, 580], fill=(104, 86, 54))
    # blurred stadium band behind
    F(d, 0, 0, CW, 300, (40, 30, 46))
    stands(d, 0, 40, CW, 260, t, rows=10, seed=31, scale=1.5)
    F(d, 0, 296, CW, 10, (240, 200, 40))
    k = t - KICK_T
    # ball: sits, squashes on contact, then flies toward camera
    if k < 0:
        bx, by, r, sq = 190, 440, 64, 1.0
    else:
        u = clamp(k / 0.55)
        bx = lerp(190, 180, u)
        by = lerp(430, 330, u)
        r = 64 + 900 * u ** 2.2
        sq = 1 - 0.35 * math.exp(-k * 30)
    return c, (bx, by, r, sq)


def shot3(t):
    c, (bx, by, r, sq) = boot_layer(t)
    bg = up(c).filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")
    big = ImageDraw.Draw(bg)
    # back of the scene: blur the stand only
    top = bg.crop((0, 0, FW, 600)).filter(ImageFilter.GaussianBlur(6))
    bg.paste(top, (0, 0))
    d = ImageDraw.Draw(bg)
    k = t - KICK_T
    # boot swinging in from the right
    swing = clamp((t - 1.10) / (KICK_T - 1.10))
    bx0 = lerp(980, 520, ease_in_out(swing)) - (max(0, k) * 300)
    byy = lerp(700, 880, ease_in_out(swing))
    ang = lerp(-0.5, 0.0, swing)
    # sock (red) + boot (black with white stripes) as a rotated polygon
    def rot(px, py):
        ca, sa = math.cos(ang), math.sin(ang)
        return (bx0 + px * ca - py * sa, byy + px * sa + py * ca)
    sock = [rot(60, -420), rot(260, -420), rot(220, -60), rot(40, -40)]
    d.polygon(sock, fill=OL)
    d.polygon([rot(70, -410), rot(250, -410), rot(212, -66), rot(50, -50)], fill=RED)
    d.polygon([rot(70, -300), rot(240, -300), rot(232, -250), rot(64, -250)], fill=(250, 250, 250))
    boot = [rot(-210, 30), rot(-150, -90), rot(40, -100), rot(240, -60), rot(250, 70), rot(-200, 90)]
    d.polygon(boot, fill=OL)
    d.polygon([rot(-196, 24), rot(-142, -80), rot(40, -88), rot(230, -52), rot(238, 58), rot(-186, 78)], fill=(30, 30, 38))
    for j in range(3):
        d.line([rot(-20 + j * 50, -84), rot(20 + j * 50, 50)], fill=(250, 250, 250), width=14)
    for j in range(5):  # studs
        sx, sy = rot(-150 + j * 80, 92)
        d.rectangle([sx - 12, sy - 4, sx + 12, sy + 16], fill=(200, 200, 210))
    # ball (full-res), squash on contact
    R2 = r * 2
    cx, cy = bx * 2, by * 2
    if R2 < 2400:
        d.ellipse([cx - R2 / sq - 6, cy - R2 * sq - 6, cx + R2 / sq + 6, cy + R2 * sq + 6], fill=OL)
        d.ellipse([cx - R2 / sq, cy - R2 * sq, cx + R2 / sq, cy + R2 * sq], fill=(250, 250, 250))
        for j in range(5):
            a = j * math.tau / 5 + t * 12
            px, py = cx + math.cos(a) * R2 * .55, cy + math.sin(a) * R2 * .55 * sq
            pr = R2 * .22
            d.regular_polygon((px, py, pr), 5, rotation=math.degrees(a), fill=(30, 30, 40))
        d.regular_polygon((cx, cy, R2 * .25), 5, rotation=t * 500, fill=(30, 30, 40))
    if k >= 0:
        # shockwave ring + water spray
        rr_ = 80 + 900 * clamp(k / 0.35)
        a = int(200 * (1 - clamp(k / 0.35)))
        ov = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        od.ellipse([cx - rr_, cy - rr_ * .6, cx + rr_, cy + rr_ * .6], outline=(255, 255, 255, a), width=14)
        rng = random.Random(9)
        for _ in range(40):
            ang2 = rng.uniform(math.pi * 0.9, math.pi * 2.1)
            v = rng.uniform(300, 900)
            px = cx + math.cos(ang2) * v * k * 1.4
            py = cy + math.sin(ang2) * v * k + 900 * k * k
            od.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(190, 220, 255, max(0, 220 - int(k * 400))))
        bg.alpha_composite(ov)
    img = bg.convert("RGB")
    img = transform(img, 1.0 + 0.08 * clamp((t - 1.1) / 1.1), *shake(t, KICK_T, 0.3, 14), 380, 860)
    img = flash(img, 0.7 * clamp(1 - k / 0.08) if k >= 0 else 0)
    if t > 2.12:
        img = flash(img, clamp((t - 2.12) / 0.08))
    return img


MONTAGE = [  # (start, kind, source time)
    (2.20, "src", 7.30),     # Grandad in seat 14 (original design)
    (2.53, "e2", 51.80),     # "Scouts are watching."
    (2.86, "d1", 41.40),     # ambulance, blue lights on wet bricks
    (3.20, "src", 2.90),     # your face, sweat — back to the penalty
]


def shot4(t):
    for i, (st, kind, srct) in enumerate(MONTAGE):
        nxt = MONTAGE[i + 1][0] if i + 1 < len(MONTAGE) else 3.54
        if st <= t < nxt:
            u = (t - st) / (nxt - st)
            if kind == "src":
                base = src_frame(srct + u * 0.3)
                z, cy = 1.42 + 0.12 * u, 900  # crop away the old burned-in caption
            elif kind == "e2":
                base = no_caps(seg_E2, srct + u * 0.3)
                z, cy = 1.15 + 0.12 * u, 900
            else:
                base = no_caps(seg_d.seg_D1, srct + u * 0.3)
                z, cy = 1.15 + 0.12 * u, 900
            img = transform(base, z, 0, 0, 360, cy)
            img = flash(img, 0.6 * clamp(1 - u / 0.25))
            # glitch slice for the cut
            if u < 0.18:
                arr = np.asarray(img).copy()
                for s in range(5):
                    y0 = (s * 211 + int(t * 997)) % 1200
                    arr[y0:y0 + 40] = np.roll(arr[y0:y0 + 40], 40 - s * 16, axis=1)
                img = Image.fromarray(arr)
            return img
    return src_frame(3.5)


def seg_H(t):
    if t < 0.55:
        img = shot1(t)
    elif t < 1.10:
        img = shot2(t)
    elif t < 2.20:
        img = shot3(t)
    else:
        img = shot4(t)
    img = tint_vignette(img, 0.4, (4, 4, 16))
    overlay_text(img, t)
    return img
