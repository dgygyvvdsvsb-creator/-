"""Segment F (57.60-63.60): end card — follow/subscribe + vote call to action.
PLATFORM env var: "tiktok" (FOLLOW) or "youtube" (SUBSCRIBE)."""
import os
import lib
import seg_e
from seg_e import *

PLATFORM = os.environ.get("PLATFORM", "tiktok")
T0, T1 = 57.60, 63.60
TAP = 59.55

BTN = "SUBSCRIBE" if PLATFORM == "youtube" else "+ FOLLOW"
BTN_DONE = "SUBSCRIBED" if PLATFORM == "youtube" else "FOLLOWING"
VERB = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"

lib.PHRASES += [
    (57.60, [("YOUR", 57.62, C_W), ("VOTE", 57.80, C_W), ("DECIDES", 57.98, C_W), ("EP. 4.", 58.20, C_Y)]),
    (59.50, [(VERB, 59.52, C_R), ("SO", 59.80, C_W), ("YOU", 59.92, C_W), ("DON'T", 60.05, C_W), ("MISS", 60.20, C_W), ("IT.", 60.34, C_W)]),
    (61.10, [("COMMENT:", 61.12, C_G), ("GRANDAD", 61.45, C_B), ("OR", 61.75, C_W), ("TRIAL?", 61.90, C_Y)]),
]


def bell(d, cx, cy, s, col):
    d.pieslice([cx - 14 * s, cy - 16 * s, cx + 14 * s, cy + 12 * s], 180, 360, fill=col)
    d.rectangle([cx - 14 * s, cy - 2 * s, cx + 14 * s, cy + 8 * s], fill=col)
    d.polygon([(cx - 18 * s, cy + 12 * s), (cx + 18 * s, cy + 12 * s), (cx + 14 * s, cy + 6 * s), (cx - 14 * s, cy + 6 * s)], fill=col)
    d.ellipse([cx - 5 * s, cy + 12 * s, cx + 5 * s, cy + 20 * s], fill=col)


def tick(d, x, y, s, col):
    d.line([(x - 10 * s, y), (x - 3 * s, y + 8 * s), (x + 12 * s, y - 9 * s)], fill=col, width=int(6 * s))


def glove_cursor(d, x, y, s=1.0):
    """Grandad's orange keeper glove as the tapping finger (plant: the gloves)"""
    d.rounded_rectangle([x - 34 * s, y + 20 * s, x + 34 * s, y + 96 * s], int(16 * s), fill=OL)
    d.rounded_rectangle([x - 30 * s, y + 24 * s, x + 30 * s, y + 92 * s], int(14 * s), fill=ORG)
    d.rounded_rectangle([x - 12 * s, y - 6 * s, x + 12 * s, y + 40 * s], int(10 * s), fill=OL)
    d.rounded_rectangle([x - 8 * s, y - 2 * s, x + 8 * s, y + 38 * s], int(8 * s), fill=ORG)  # finger
    d.rectangle([x - 30 * s, y + 70 * s, x + 30 * s, y + 92 * s], fill=ORG_D)
    d.rectangle([x - 22 * s, y + 30 * s, x - 10 * s, y + 40 * s], fill=ORG_L)
    d.rectangle([x - 30 * s, y + 92 * s, x + 30 * s, y + 104 * s], fill=BRACE)  # red string at the wrist


def burst(d, cx, cy, k):
    rng = random.Random(4)
    for i in range(18):
        a = i / 18 * math.tau + rng.random() * .3
        r = 40 + 170 * ease_out(k)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * .8
        sz = 10 * (1 - k) + 2
        col = rng.choice([C_Y, C_G, C_B, C_R, (255, 255, 255)])
        d.rectangle([x - sz, y - sz, x + sz, y + sz], fill=col)


def seg_F(t):
    # crossroads scene keeps living underneath (rain, hero looking around), without its captions
    keep = seg_e.overlay_text
    seg_e.overlay_text = lambda img, tt: None
    try:
        base = seg_E3(t)
    finally:
        seg_e.overlay_text = keep
    k_dim = ease_out((t - 57.95) / 0.35)
    img = Image.blend(base, Image.new("RGB", base.size, (6, 8, 22)), 0.55 * k_dim).convert("RGBA")
    d = ImageDraw.Draw(img)
    # panel slides up
    k = spring(t - 57.95, 11, 6)
    py = lerp(1400, 470, clamp(k, 0, 1.2))
    if t > 57.95:
        d.rounded_rectangle([50, py, 670, py + 520], 34, fill=(14, 18, 44), outline=C_Y, width=6)
        # series badge + hero face in the panel (keeps the anchors: green shirt, dark hair)
        c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        cd = ImageDraw.Draw(c)
        after = t > TAP
        hero_front(cd, 92, int(py / 2) + 140, 2.3, expr="smile" if after else "determined", t=t,
                   gloves=True, blink=(60.9 < t < 61.0))
        img.alpha_composite(up(c))
        d = ImageDraw.Draw(img)
        d.text((410, py + 70), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
        d.text((410, py + 122), "EP. 4", font=font(800, 64), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
        # the button
        pulse = 1 + 0.05 * math.sin(t * 9) if not after else 1.0
        press = 1 - 0.12 * math.exp(-((t - TAP) * 14) ** 2)
        bw, bh = 360 * pulse * press, 100 * pulse * press
        bx, by = 450, py + 250
        col = (60, 64, 90) if after else (234, 46, 72)
        d.rounded_rectangle([bx - bw / 2 - 5, by - bh / 2 - 5, bx + bw / 2 + 5, by + bh / 2 + 5], 26, fill=OL)
        d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], 22, fill=col)
        label = BTN_DONE if after else BTN
        f = font(800, int(44 * pulse * press if not after else 38))
        if PLATFORM == "youtube" and not after:
            bell(d, bx - bw / 2 + 52, by - 4, 1.6, (255, 255, 255))
            d.text((bx + 24, by + 2), label, font=f, fill=(255, 255, 255), anchor="mm")
        elif after:
            tick(d, bx - bw / 2 + 50, by, 1.5, C_G)
            d.text((bx + 20, by + 2), label, font=f, fill=(255, 255, 255), anchor="mm")
        else:
            d.text((bx, by + 2), label, font=f, fill=(255, 255, 255), anchor="mm")
        if after and t < TAP + 0.6:
            burst(d, bx, by, (t - TAP) / 0.6)
        # glove taps the button
        if 58.6 < t < TAP + 0.7:
            u = ease_in_out((t - 58.6) / (TAP - 58.6))
            gx = lerp(640, bx + 110, u)
            gy = lerp(1300, by - 6, u) + (10 if abs(t - TAP) < 0.08 else 0)
            glove_cursor(d, gx, gy, 1.0)
        # vote chips + arrow down to the comments
        if t > 61.05:
            kk = spring(t - 61.05, 13, 7)
            for x, lab, cc in ((215, "GRANDAD", C_B), (525, "TRIAL", C_Y)):
                w = 200 * kk
                hop = 8 * math.sin((t - 61.05) * 8 + (0 if x < 400 else 1.5)) if t > 61.6 else 0
                d.rounded_rectangle([x - w / 2, py + 360 - hop, x + w / 2, py + 432 - hop], 20, fill=(30, 36, 76),
                                    outline=cc, width=5)
                if kk > .4:
                    d.text((x, py + 396 - hop), lab, font=font(800, int(34 * min(kk, 1))), fill=cc, anchor="mm")
            d.text((370, py + 396), "or", font=font(700, 28), fill=(200, 204, 220), anchor="mm")
            # arrow pointing to the comments button area (bottom right on both apps)
            ay = py + 470 + 10 * math.sin(t * 8)
            d.text((360, ay), "VOTE IN THE COMMENTS", font=font(800, 30), fill=(255, 255, 255), anchor="mm",
                   stroke_width=3, stroke_fill=OL)
    rain(img, t, alpha=50)
    img = img.convert("RGB")
    overlay_text(img, t)
    return img
