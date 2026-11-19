import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CW, CH = 360, 640          # drawing canvas
FW, FH = 720, 1280         # output
FPS = 30
FONTDIR = "/tmp/claude-0/-home-user--/67093071-fe87-56fe-a818-3433aa12d626/scratchpad/fonts/"

# ---------------- palette (sampled from the original EP3) ----------------
OL = (23, 20, 30)
SKIN, SKIN_D, SKIN_L = (240, 198, 162), (207, 172, 139), (248, 214, 184)
DSKIN, DSKIN_D = (150, 98, 66), (118, 74, 48)
HAIR, HAIR_L = (56, 38, 31), (92, 66, 52)
GRN, GRN_D, GRN_L = (41, 167, 74), (26, 117, 52), (96, 206, 124)
ORG, ORG_D, ORG_L = (252, 140, 27), (206, 98, 14), (255, 186, 92)
WHT, WHT_D = (250, 250, 252), (200, 204, 216)
BLOND, BLOND_D, BLOND_L = (244, 212, 102), (214, 172, 64), (255, 236, 150)
RED, RED_D, RED_L = (203, 51, 54), (148, 30, 40), (232, 92, 92)
CARD, CARD_D, CARD_L = (171, 117, 79), (130, 80, 38), (196, 146, 104)
BEARD, BEARD_D = (245, 242, 248), (205, 205, 222)
BTN = (237, 202, 119)
MUMH, BLUE, BLUE_D = (114, 62, 43), (70, 108, 189), (45, 75, 140)
GINGER = (226, 112, 44)
NIGHT = (16, 22, 49)
BRACE = (225, 30, 40)

# caption colours
C_W, C_Y, C_R, C_B, C_G = (250, 250, 250), (250, 210, 35), (238, 78, 79), (91, 198, 251), (110, 222, 120)
C_DIM, C_STROKE = (148, 155, 172), (12, 10, 22)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


def spring(t, k=10.0, damp=5.0):
    """overshoot pop-in 0->1"""
    if t <= 0:
        return 0.0
    return 1 - math.exp(-damp * t) * math.cos(k * t)


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, clamp(t))) for a, b in zip(c1, c2))


def R(d, x, y, w, h, fill, ol=OL, ow=1, r=0):
    """outlined (optionally rounded) rect; coords floats ok"""
    x0, y0 = round(x), round(y)
    x1, y1 = round(x + w) - 1, round(y + h) - 1
    if x1 < x0 or y1 < y0:
        return
    if ol is not None:
        if r:
            d.rounded_rectangle([x0 - ow, y0 - ow, x1 + ow, y1 + ow], r + ow, fill=ol)
        else:
            d.rectangle([x0 - ow, y0 - ow, x1 + ow, y1 + ow], fill=ol)
    if r:
        d.rounded_rectangle([x0, y0, x1, y1], r, fill=fill)
    else:
        d.rectangle([x0, y0, x1, y1], fill=fill)


def F(d, x, y, w, h, fill, r=0):
    R(d, x, y, w, h, fill, ol=None, r=r)


# ---------------- fonts / captions ----------------
_fonts = {}


def font(w, size):
    k = (w, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FONTDIR + f"Poppins-{w}.ttf", size)
    return _fonts[k]


def draw_banner(img, ep=3):
    d = ImageDraw.Draw(img)
    f = font(600, 21)
    a, b = f"EP. {ep} · FROM ZERO TO ", "LEGEND"
    wa = d.textlength(a, font=f)
    wb = d.textlength(b, font=f)
    x = (FW - wa - wb) / 2
    y = 85
    for txt, col, xx in ((a, (250, 250, 250), x), (b, C_Y, x + wa)):
        d.text((xx, y), txt, font=f, fill=col, stroke_width=3, stroke_fill=C_STROKE)


def draw_caption(img, words, t):
    """words: list of (text, start, colour). Karaoke: dim until spoken."""
    if not words:
        return
    d = ImageDraw.Draw(img)
    f = font(700, 47)
    sp = d.textlength(" ", font=f)
    # wrap to lines
    lines, cur, cw = [], [], 0
    for w in words:
        ww = d.textlength(w[0], font=f)
        if cur and cw + sp + ww > 560:
            lines.append(cur)
            cur, cw = [], 0
        cw = cw + (sp if cur else 0) + ww
        cur.append((w, ww))
    lines.append(cur)
    y = 140
    for ln in lines:
        tot = sum(ww for _, ww in ln) + sp * (len(ln) - 1)
        x = (FW - tot) / 2
        for (txt, st, col), ww in ln:
            on = t >= st
            c = col if on else C_DIM
            # small pop on activation
            d.text((x, y), txt, font=f, fill=c, stroke_width=6, stroke_fill=C_STROKE)
            x += ww + sp
        y += 57


# full-episode caption timeline (taken from the original burned-in captions)
Wc, Y, Rr, B, G = C_W, C_Y, C_R, C_B, C_G
PHRASES = [
    (3.63, [("YOU", 3.70, Wc), ("CHOSE", 3.87, Wc), ("RIGHT.", 4.20, B)]),
    (4.90, [("SO", 4.93, Wc), ("YOU'LL", 5.13, Wc), ("DIVE", 5.60, Wc), ("RIGHT.", 5.93, B)]),
    (6.93, [("GRANDAD'S", 6.95, Y), ("WATCHING", 7.5, Wc), ("FROM", 7.97, Wc), ("SEAT", 8.27, Wc)]),
    (8.50, [("FOURTEEN.", 8.52, Y)]),
    (9.60, [("YOUR", 9.70, Wc), ("HEART.", 9.95, Rr)]),
    (10.77, [("LOUDER", 10.95, Wc), ("THAN", 11.17, Wc), ("THE", 11.43, Wc), ("CROWD.", 11.67, Wc)]),
    (12.50, [("HE", 12.53, Wc), ("LOOKS", 12.75, Wc), ("LEFT.", 13.03, Y)]),
    (13.30, [("HE", 13.33, Wc), ("LOOKS", 13.60, Wc), ("RIGHT.", 13.95, B)]),
    (14.47, [("YOU", 14.50, Wc), ("DIVE.", 14.80, Wc)]),
    (15.30, [("RIGHT.", 15.33, B)]),
    (16.67, [("THE", 16.70, Wc), ("BALL", 16.90, Wc), ("GOES", 17.17, Wc), ("LEFT.", 17.43, Y)]),
    (18.13, [("GOAL.", 18.15, Rr)]),
    (31.17, [("THUMBS", 31.20, G), ("UP.", 31.60, G)]),
    (32.47, [("GOOD", 32.50, Wc), ("DIVE,", 32.75, Wc)]),
    (33.47, [("SON.", 33.50, Wc)]),
    (34.57, [("WRONG", 34.60, Rr), ("SIDE.", 35.03, Wc)]),
    (36.03, [("NEXT", 36.07, Wc), ("TIME.", 36.33, Wc)]),
    (36.67, [("YOU", 36.70, Wc), ("SMILE", 36.95, G), ("BACK.", 37.3, Wc)]),
    (39.27, [("GRANDAD", 39.30, Wc), ("GOES", 39.70, Wc), ("DOWN.", 39.97, Rr)]),
    (40.27, [("SIRENS.", 40.30, B)]),
    (40.63, [("RAIN.", 40.67, Wc)]),
    (40.93, [("BLUE", 40.97, Wc), ("LIGHTS", 41.23, Wc), ("ON", 41.60, Wc), ("WET", 41.77, Wc)]),
    (41.97, [("BRICKS.", 42.00, Wc)]),
    (42.63, [("YOU", 42.70, Wc), ("RIDE", 42.95, Wc), ("WITH", 43.25, Wc), ("HIM.", 43.50, Wc)]),
    (44.40, [("WHITE", 44.43, Wc), ("LIGHTS.", 44.75, Wc)]),
    (45.30, [("WAITING.", 45.35, B)]),
    (46.63, [("THEN", 46.67, Wc), ("YOUR", 46.97, Wc), ("PHONE", 47.23, Wc), ("BUZZES.", 47.57, Y)]),
    (48.60, [("TRIAL.", 48.63, Y)]),
    (49.53, [("SATURDAY.", 49.57, Y)]),
    (50.67, [("SCOUTS", 50.70, Wc), ("ARE", 51.03, Wc), ("WATCHING.", 51.23, Y)]),
    (52.37, [("YOUR", 52.40, Wc), ("DREAM.", 52.63, Y)]),
    (53.37, [("OR", 53.40, Wc), ("YOUR", 53.60, Wc), ("GRANDAD.", 53.90, B)]),
    (54.80, [("WHAT", 54.85, Wc), ("DO", 55.13, Wc), ("YOU", 55.33, Wc), ("DO?", 55.57, Wc)]),
    (55.77, [("COMMENT", 55.80, G), ("BELOW.", 56.27, Wc)]),
]


def caption_at(t):
    cur = None
    for st, ws in PHRASES:
        if t >= st:
            cur = ws
    return cur


def overlay_text(img, t):
    draw_banner(img)
    draw_caption(img, caption_at(t), t)


# ---------------- effects ----------------
_rng = random.Random(7)
RAIN = [(_rng.uniform(0, FW), _rng.uniform(0, FH), _rng.uniform(0.6, 1.0)) for _ in range(140)]


def rain(img, t, speed=900, alpha=70, slant=-0.12, length=26):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x, y, s in RAIN:
        yy = (y + t * speed * s) % (FH + 60) - 30
        xx = (x + yy * slant) % FW
        L = length * s
        d.line([(xx, yy), (xx + L * slant, yy + L)], fill=(210, 220, 255, int(alpha * s)), width=2)
    img.alpha_composite(ov) if img.mode == "RGBA" else img.paste(ov, (0, 0), ov)


def up(canvas):
    return canvas.resize((FW, FH), Image.NEAREST)


def vignette(img, strength=0.55, color=(0, 0, 0)):
    yy, xx = np.mgrid[0:FH, 0:FW]
    r = np.sqrt(((xx - FW / 2) / (FW / 2)) ** 2 + ((yy - FH / 2) / (FH / 2)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * strength
    ov = np.zeros((FH, FW, 4), np.uint8)
    ov[..., :3] = color
    ov[..., 3] = (a * 255).astype(np.uint8)
    o = Image.fromarray(ov, "RGBA")
    img.paste(o, (0, 0), o)


_vig_cache = {}


def vig_mask(strength):
    k = round(strength, 3)
    if k not in _vig_cache:
        yy, xx = np.mgrid[0:FH, 0:FW]
        r = np.sqrt(((xx - FW / 2) / (FW / 2)) ** 2 + ((yy - FH / 2) / (FH / 2)) ** 2)
        _vig_cache[k] = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * strength
    return _vig_cache[k]


def tint_vignette(img, strength, color):
    a = vig_mask(strength)[..., None]
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    arr = arr * (1 - a) + np.array(color, np.float32) * a
    return Image.fromarray(arr.astype(np.uint8))


def shake(t, t0, dur=0.25, amp=6):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        return (math.sin(t * 90) * amp * k, math.cos(t * 77) * amp * k)
    return (0, 0)


def flash(img, a):
    if a <= 0:
        return img
    return Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (255, 255, 255)), clamp(a))


def transform(img, zoom=1.0, dx=0, dy=0, cx=FW / 2, cy=FH / 2):
    """push-in around (cx,cy) + translate, keeps size"""
    if zoom == 1.0 and dx == 0 and dy == 0:
        return img
    w, h = img.size
    nw, nh = w / zoom, h / zoom
    x0 = cx - nw * (cx / w) - dx / zoom
    y0 = cy - nh * (cy / h) - dy / zoom
    return img.transform((w, h), Image.EXTENT, (x0, y0, x0 + nw, y0 + nh), Image.BILINEAR)


# ---------------- crowd / stands ----------------
CROWD_COLS = [GRN, GRN, (230, 230, 235), RED, GRN_D, (240, 200, 60), RED_D]
SKINS = [SKIN, (224, 172, 128), DSKIN, (120, 80, 56), (246, 210, 178)]
HAIRS = [HAIR, (30, 24, 22), BLOND, GINGER, (150, 150, 150), (90, 60, 40)]


def stands(d, x0, y0, w, h, t, rows=9, seed=1, scale=1.0, base=(74, 54, 56), seat=(150, 46, 62), wave=0.0):
    """tiers of seats with fans; perspective: rows grow toward bottom"""
    rng = random.Random(seed)
    F(d, x0, y0, w, h, base)
    y = y0
    for r in range(rows):
        rh = max(4, int((6 + r * 1.2) * scale))
        F(d, x0, y, w, max(1, rh // 3), seat)
        F(d, x0, y + rh // 3, w, 1, (60, 34, 44))
        fw = max(3, int(rh * 0.75))
        x = x0 + rng.randint(0, fw)
        while x < x0 + w - fw:
            if rng.random() < 0.82:
                bob = int(1.5 * math.sin(t * (3 + rng.random() * 3) + rng.random() * 9) * (1 if rng.random() < 0.3 + wave else 0))
                c = rng.choice(CROWD_COLS)
                sk = rng.choice(SKINS)
                hc = rng.choice(HAIRS)
                hy = y - fw + bob
                F(d, x, hy + fw * 0.55, fw, fw * 0.75, c)                # body
                F(d, x + fw * 0.15, hy, fw * 0.7, fw * 0.6, sk)          # head
                F(d, x + fw * 0.15, hy, fw * 0.7, max(1, fw * 0.22), hc)   # hair
                if rng.random() < 0.12:  # scarf / flag
                    F(d, x - 1, hy + fw * 0.5, fw + 2, max(1, fw * 0.18), rng.choice([GRN_L, WHT, (240, 200, 60)]))
            x += fw + rng.randint(1, 3)
        y += rh
    return y


def floodlight(d, x, y, s=1.0, t=0):
    F(d, x - 9 * s, y - 5 * s, 18 * s, 10 * s, (60, 64, 80), r=int(2 * s))
    for i in range(3):
        for j in range(2):
            F(d, x - 7 * s + i * 5 * s, y - 3 * s + j * 4 * s, 4 * s, 3 * s, (255, 250, 220))


def glow(img, x, y, r, color, a=0.5):
    """additive radial glow at full-res coords"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    steps = 10
    for i in range(steps, 0, -1):
        rr = r * i / steps
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color + (int(255 * a / steps * 1.6),))
    img.paste(ov, (0, 0), ov)
