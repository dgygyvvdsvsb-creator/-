"""Characters for EP3 rework — blocky chibi style matching the original episode.
All functions take a PIL ImageDraw on the 360x640 canvas, foot-centre (cx, fy) or
head-centre coordinates, and s = canvas pixels per design unit."""
import math
from lib import *


def limb(d, p0, p1, w, fill, ow=1):
    d.line([p0, p1], fill=OL, width=int(w + 2 * ow))
    for p in (p0, p1):
        r = (w + 2 * ow) / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=OL)
    d.line([p0, p1], fill=fill, width=int(w))
    for p in (p0, p1):
        r = w / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill)


def eye(d, x, y, s, look=(0, 0), blink=False, big=False):
    w, h = (3.2 * s, 4 * s) if big else (2.6 * s, 3.2 * s)
    if blink:
        F(d, x - w / 2, y + h * 0.4, w, max(1, 0.7 * s), OL)
        return
    F(d, x - w / 2, y - h / 2, w, h, WHT, r=int(0.6 * s))
    pw, ph = w * 0.62, h * 0.72
    px = x - pw / 2 + look[0] * (w - pw) / 2
    py = y - ph / 2 + look[1] * (h - ph) / 2 + 0.2 * s
    F(d, px, py, pw, ph, OL, r=int(0.4 * s))
    F(d, px + pw * 0.15, py + ph * 0.12, max(1, pw * 0.35), max(1, ph * 0.3), WHT)


def mouth(d, cx, y, s, kind):
    if kind == "smile":
        F(d, cx - 3 * s, y, 6 * s, 1 * s, OL)
        F(d, cx - 4 * s, y - 1 * s, 1.2 * s, 1.2 * s, OL)
        F(d, cx + 2.8 * s, y - 1 * s, 1.2 * s, 1.2 * s, OL)
    elif kind == "open":
        F(d, cx - 2.5 * s, y - 1 * s, 5 * s, 3.2 * s, (120, 30, 40), r=int(0.8 * s))
        F(d, cx - 1.8 * s, y - 1 * s, 3.6 * s, 0.9 * s, WHT)
    elif kind == "talk":
        F(d, cx - 2 * s, y - 0.5 * s, 4 * s, 2 * s, (120, 30, 40), r=int(0.5 * s))
    elif kind == "sad":
        F(d, cx - 2.5 * s, y, 5 * s, 1 * s, OL)
        F(d, cx - 3.5 * s, y + 1 * s, 1.2 * s, 1 * s, OL)
        F(d, cx + 2.3 * s, y + 1 * s, 1.2 * s, 1 * s, OL)
    elif kind == "smirk":
        F(d, cx - 2 * s, y, 5 * s, 1 * s, OL)
        F(d, cx + 3 * s, y - 1 * s, 1.2 * s, 1.2 * s, OL)
    elif kind == "shock":
        F(d, cx - 1.5 * s, y - 1 * s, 3 * s, 3.5 * s, (90, 20, 30), r=int(1 * s))
    else:  # flat / determined
        F(d, cx - 2 * s, y, 4 * s, 1 * s, (150, 60, 60))


# ------------------------------------------------------------------ HERO
def hero_back(d, cx, fy, s, arms=1.0, lean=0.0, crouch=0.0, gloves=True, t=0.0, look=0.0):
    """Keeper seen from behind (over-the-shoulder). arms: 0 down .. 1 ready-wide. look: -1..1 head turn"""
    br = math.sin(t * 2.4) * 0.4 * s  # breathing
    cy = fy - crouch * 4 * s
    hx = cx + lean * 2 * s
    # legs
    lx, rx = cx - 5.5 * s, cx + 5.5 * s
    spread = 1 * s + crouch * 2 * s
    for x, sgn in ((lx, -1), (rx, 1)):
        xx = x + sgn * spread
        R(d, xx - 3 * s, cy - 11 * s, 6 * s, 6 * s, SKIN)
        F(d, xx + 1 * s, cy - 11 * s, 2 * s, 6 * s, SKIN_D)
        R(d, xx - 3 * s, cy - 6 * s, 6 * s, 4 * s, GRN)
        F(d, xx - 3 * s, cy - 5 * s, 6 * s, 0.8 * s, WHT)
        R(d, xx - 3.5 * s, cy - 2.2 * s, 7 * s, 2.6 * s, (30, 28, 36))
        F(d, xx - 3.5 * s, cy + 0.1 * s, 7 * s, 0.6 * s, (90, 90, 100))
    # shorts
    R(d, hx - 11 * s, cy - 18 * s, 22 * s, 8 * s, WHT, r=int(s))
    F(d, hx + 4 * s, cy - 18 * s, 7 * s, 8 * s, WHT_D)
    F(d, hx - 0.5 * s, cy - 14 * s, 1 * s, 4 * s, WHT_D)
    # torso
    ty = cy - 35 * s + br
    R(d, hx - 12 * s, ty, 24 * s, 18 * s, GRN, r=int(1.5 * s))
    F(d, hx + 5 * s, ty, 7 * s, 18 * s, GRN_D)
    F(d, hx - 10 * s, ty + 2 * s, 3 * s, 12 * s, GRN_L)
    # number 0
    nx, ny, nw, nh = hx - 4.5 * s, ty + 3 * s, 9 * s, 12 * s
    F(d, nx, ny, nw, nh, WHT)
    F(d, nx + 2.6 * s, ny + 2.6 * s, nw - 5.2 * s, nh - 5.2 * s, GRN if True else GRN)
    # arms + gloves
    for sgn in (-1, 1):
        sh = (hx + sgn * 11 * s, ty + 3 * s)
        if arms > 1.0:  # 1..2 : raise toward overhead (dive)
            a2 = arms - 1.0
            gx = hx + sgn * lerp(21 * s, 7 * s, a2)
            gy = ty + lerp(8 * s, -26 * s, a2)
        else:
            gx = hx + sgn * lerp(14 * s, 21 * s, arms)
            gy = ty + lerp(17 * s, 8 * s, arms)
        limb(d, sh, (lerp(sh[0], gx, 0.55), lerp(sh[1], gy, 0.55)), 6 * s, GRN if sgn < 0 else GRN_D)
        limb(d, (lerp(sh[0], gx, 0.5), lerp(sh[1], gy, 0.5)), (gx, gy), 4.6 * s, SKIN)
        if sgn > 0:  # red string bracelet on the RIGHT wrist (screen right from behind)
            bx, by = lerp(sh[0], gx, 0.82), lerp(sh[1], gy, 0.82)
            F(d, bx - 2.6 * s, by - 0.8 * s, 5.2 * s, 1.6 * s, BRACE)
        if gloves:
            R(d, gx - 5 * s, gy - 4 * s, 10 * s, 9 * s, ORG, r=int(2 * s))
            F(d, gx - 5 * s, gy + 2 * s, 10 * s, 3 * s, ORG_D)
            F(d, gx - 4 * s, gy - 3 * s, 3 * s, 2 * s, ORG_L)
        else:
            R(d, gx - 2.5 * s, gy - 2.5 * s, 5 * s, 5 * s, SKIN, r=int(s))
    # head (back): hair covers almost everything
    hy = ty - 20 * s + br * 0.5
    hxx = hx + look * 1.5 * s
    R(d, hxx - 3.5 * s, hy + 16 * s, 7 * s, 5 * s, SKIN_D)  # neck
    for sgn in (-1, 1):  # ears
        ex = hxx + sgn * 11.2 * s - (1.6 * s if sgn > 0 else 1.6 * s)
        if (look > 0.3 and sgn < 0) or (look < -0.3 and sgn > 0):
            continue
        R(d, ex, hy + 8 * s, 3.2 * s, 5 * s, SKIN)
    R(d, hxx - 10 * s, hy, 20 * s, 18 * s, HAIR, r=int(3 * s))
    F(d, hxx - 7 * s, hy + 2 * s, 6 * s, 2.5 * s, HAIR_L)
    F(d, hxx + 3 * s, hy + 4 * s, 5 * s, 8 * s, (44, 30, 25))
    F(d, hxx - 6 * s, hy + 15 * s, 12 * s, 3 * s, SKIN_D)  # nape
    if abs(look) > 0.3:  # cheek visible when turning
        sx = hxx + (8 if look > 0 else -11) * s
        R(d, sx, hy + 9 * s, 3 * s, 6 * s, SKIN)


def hero_front(d, cx, fy, s, pose="stand", expr="flat", look=(0, 0), blink=False, t=0.0,
               gloves=False, tear=False, arms="down", phone=False):
    """front view, chibi. pose: stand | sit"""
    br = math.sin(t * 2.4) * 0.35 * s
    sit = pose == "sit"
    if sit:
        # thighs toward camera (both), shins down, shoes
        for sgn in (-1, 1):
            x = cx + sgn * 5 * s
            R(d, x - 3.5 * s, fy - 13 * s, 7 * s, 5 * s, WHT)
            R(d, x - 3 * s, fy - 8 * s, 6 * s, 5 * s, SKIN)
            R(d, x - 3 * s, fy - 4 * s, 6 * s, 2.5 * s, GRN)
            R(d, x - 3.5 * s, fy - 1.8 * s, 7 * s, 2.4 * s, (30, 28, 36))
        base = fy - 12 * s
    else:
        for sgn in (-1, 1):
            x = cx + sgn * 4.5 * s
            R(d, x - 3 * s, fy - 10 * s, 6 * s, 5 * s, SKIN)
            R(d, x - 3 * s, fy - 5 * s, 6 * s, 3.4 * s, GRN)
            R(d, x - 3.5 * s, fy - 2 * s, 7 * s, 2.4 * s, (30, 28, 36))
        R(d, cx - 10 * s, fy - 16 * s, 20 * s, 7 * s, WHT, r=int(s))
        F(d, cx + 4 * s, fy - 16 * s, 6 * s, 7 * s, WHT_D)
        base = fy - 15 * s
    ty = base - 16 * s + br
    R(d, cx - 11 * s, ty, 22 * s, 17 * s, GRN, r=int(1.5 * s))
    F(d, cx + 5 * s, ty, 6 * s, 17 * s, GRN_D)
    F(d, cx - 9 * s, ty + 2 * s, 2.5 * s, 10 * s, GRN_L)
    F(d, cx - 3 * s, ty, 6 * s, 2 * s, WHT)  # collar
    # arms
    for sgn in (-1, 1):
        sh = (cx + sgn * 10 * s, ty + 3 * s)
        if arms == "lap" or phone:
            hand = (cx + sgn * 4 * s, ty + 15 * s)
        elif arms == "hug":
            hand = (cx - sgn * 4 * s, ty + 8 * s)
        else:
            hand = (cx + sgn * 13 * s, ty + 15 * s)
        limb(d, sh, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), 5.5 * s, GRN if sgn < 0 else GRN_D)
        limb(d, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), hand, 4.2 * s, SKIN)
        if sgn < 0:  # hero's right hand = screen left in front view
            bx, by = lerp(sh[0], hand[0], .8), lerp(sh[1], hand[1], .8)
            F(d, bx - 2.4 * s, by - .8 * s, 4.8 * s, 1.6 * s, BRACE)
        if gloves:
            R(d, hand[0] - 4.5 * s, hand[1] - 3.5 * s, 9 * s, 8 * s, ORG, r=int(2 * s))
            F(d, hand[0] - 4.5 * s, hand[1] + 2 * s, 9 * s, 2.5 * s, ORG_D)
        else:
            R(d, hand[0] - 2.4 * s, hand[1] - 2.4 * s, 4.8 * s, 4.8 * s, SKIN, r=int(s))
    if phone:
        R(d, cx - 3.5 * s, ty + 9 * s, 7 * s, 10 * s, (30, 32, 44), r=int(s))
        F(d, cx - 2.5 * s, ty + 10 * s, 5 * s, 8 * s, (120, 190, 255))
    # head
    hy = ty - 19 * s + br * 0.5
    R(d, cx - 3 * s, hy + 16 * s, 6 * s, 4 * s, SKIN_D)
    for sgn in (-1, 1):
        R(d, cx + sgn * 10.5 * s - 1.5 * s, hy + 8 * s, 3 * s, 5 * s, SKIN)
    R(d, cx - 10 * s, hy, 20 * s, 18 * s, SKIN, r=int(2.5 * s))
    F(d, cx + 4 * s, hy + 3 * s, 6 * s, 14 * s, SKIN_D)
    # hair: top + fringe strand
    R(d, cx - 10.5 * s, hy - 1.5 * s, 21 * s, 7 * s, HAIR, r=int(2.5 * s))
    F(d, cx - 10.5 * s, hy + 4 * s, 3 * s, 5 * s, HAIR)
    F(d, cx + 7.5 * s, hy + 4 * s, 3 * s, 5 * s, HAIR)
    F(d, cx - 3 * s, hy + 4.5 * s, 4 * s, 2 * s, HAIR)
    F(d, cx - 7 * s, hy, 6 * s, 1.5 * s, HAIR_L)
    # face
    ey = hy + 10 * s
    for sgn in (-1, 1):
        eye(d, cx + sgn * 4.5 * s, ey, s, look, blink)
        bw = 4 * s
        tilt = {"sad": (1 if sgn < 0 else -1), "determined": (-1 if sgn < 0 else 1), "worried": (1 if sgn < 0 else -1)}.get(expr, 0)
        bx = cx + sgn * 4.5 * s - bw / 2
        by = ey - 4 * s
        F(d, bx, by + (0.6 * s if tilt > 0 and sgn > 0 or tilt < 0 and sgn < 0 else 0), bw, 0.9 * s, HAIR)
    F(d, cx - 0.5 * s, ey + 2.5 * s, 1.2 * s, 1.2 * s, SKIN_D)  # nose
    F(d, cx - 8 * s, ey + 2.5 * s, 2.2 * s, 1 * s, (240, 150, 150))
    F(d, cx + 6 * s, ey + 2.5 * s, 2.2 * s, 1 * s, (230, 150, 140))
    mouth(d, cx, ey + 5 * s, s * 0.8, {"flat": "flat", "sad": "sad", "smile": "smile", "shock": "shock",
                                         "worried": "flat", "determined": "flat", "talk": "talk"}.get(expr, "flat"))
    if tear:
        F(d, cx - 6 * s, ey + 2.5 * s + (t * 6 % 4) * s, 1.4 * s, 2.2 * s, (120, 190, 255))


# ------------------------------------------------------------------ MASON
def mason_front(d, cx, fy, s, phase=0.0, mode="stand", expr="smirk", look=(0, 0), t=0.0, kick=0.0):
    """mode: stand | run (phase cycles) | kick (kick 0..1 leg swing)"""
    br = math.sin(t * 2.2) * 0.3 * s
    # legs
    for i, sgn in enumerate((-1, 1)):
        x = cx + sgn * 4.5 * s
        lift = 0
        if mode == "run":
            lift = max(0, math.sin(phase * math.tau + i * math.pi)) * 4 * s
        if mode == "kick" and sgn > 0:
            lift = math.sin(clamp(kick) * math.pi) * 5 * s
        R(d, x - 3 * s, fy - 10 * s - lift, 6 * s, 5 * s, SKIN)
        R(d, x - 3 * s, fy - 5 * s - lift, 6 * s, 3.4 * s, RED)
        R(d, x - 3.5 * s, fy - 2 * s - lift, 7 * s, 2.4 * s, (240, 240, 245))
    R(d, cx - 10 * s, fy - 16 * s, 20 * s, 7 * s, (32, 33, 44), r=int(s))
    ty = fy - 31 * s + br
    R(d, cx - 11 * s, ty, 22 * s, 16 * s, RED, r=int(1.5 * s))
    F(d, cx + 5 * s, ty, 6 * s, 16 * s, RED_D)
    F(d, cx - 9 * s, ty + 2 * s, 2.5 * s, 10 * s, RED_L)
    F(d, cx - 3 * s, ty, 6 * s, 2 * s, WHT)
    for i, sgn in enumerate((-1, 1)):
        sw = math.sin(phase * math.tau + i * math.pi) * 4 * s if mode == "run" else 0
        sh = (cx + sgn * 10 * s, ty + 3 * s)
        hand = (cx + sgn * 13 * s, ty + 14 * s + sw)
        limb(d, sh, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), 5.5 * s, RED if sgn < 0 else RED_D)
        limb(d, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), hand, 4.2 * s, SKIN)
        R(d, hand[0] - 2.4 * s, hand[1] - 2.4 * s, 4.8 * s, 4.8 * s, SKIN, r=int(s))
    hy = ty - 19 * s
    R(d, cx - 3 * s, hy + 16 * s, 6 * s, 4 * s, SKIN_D)
    R(d, cx - 10 * s, hy, 20 * s, 18 * s, SKIN, r=int(2.5 * s))
    F(d, cx + 4 * s, hy + 3 * s, 6 * s, 14 * s, SKIN_D)
    # blond spiky quiff
    R(d, cx - 10.5 * s, hy - 2 * s, 21 * s, 7 * s, BLOND, r=int(2 * s))
    for k in range(4):
        F(d, cx - 8 * s + k * 4.5 * s, hy - 4 * s + (k % 2) * s, 3.5 * s, 3 * s, BLOND)
    F(d, cx - 10.5 * s, hy + 4 * s, 2.5 * s, 4 * s, BLOND)
    F(d, cx + 8 * s, hy + 4 * s, 2.5 * s, 4 * s, BLOND_D)
    F(d, cx - 6 * s, hy - 1 * s, 6 * s, 1.5 * s, BLOND_L)
    ey = hy + 10 * s
    for sgn in (-1, 1):
        eye(d, cx + sgn * 4.5 * s, ey, s, look)
        # sharp brows angled down to the centre
        bx = cx + sgn * 4.5 * s - 2 * s
        F(d, bx, ey - 4 * s, 4 * s, 0.9 * s, (150, 120, 40))
        F(d, cx + sgn * 2.5 * s - .6 * s, ey - 3.3 * s, 1.2 * s, 0.9 * s, (150, 120, 40))
    F(d, cx - 0.5 * s, ey + 2.5 * s, 1.2 * s, 1.2 * s, SKIN_D)
    mouth(d, cx, ey + 5 * s, s * 0.8, expr)


def mason_portrait(d, cx, cy, s, look=0.0, blink=False, t=0.0):
    """big close-up head + shoulders; look -1 (screen left) .. 1 (screen right)"""
    # shoulders / shirt
    R(d, cx - 30 * s, cy + 16 * s, 60 * s, 30 * s, RED, r=int(5 * s))
    F(d, cx + 12 * s, cy + 16 * s, 18 * s, 30 * s, RED_D)
    F(d, cx - 6 * s, cy + 16 * s, 12 * s, 3 * s, WHT)
    R(d, cx - 5 * s, cy + 8 * s, 10 * s, 9 * s, SKIN_D)
    hx = cx + look * 1.2 * s
    for sgn in (-1, 1):
        R(d, hx + sgn * 17 * s - 2.5 * s, cy - 4 * s, 5 * s, 8 * s, SKIN)
    R(d, hx - 16 * s, cy - 18 * s, 32 * s, 28 * s, SKIN, r=int(4 * s))
    F(d, hx + 7 * s, cy - 14 * s, 9 * s, 24 * s, SKIN_D)
    R(d, hx - 17 * s, cy - 22 * s, 34 * s, 10 * s, BLOND, r=int(3 * s))
    for k in range(5):
        F(d, hx - 15 * s + k * 6.5 * s, cy - 25 * s + (k % 2) * 1.5 * s, 5 * s, 5 * s, BLOND)
    F(d, hx - 17 * s, cy - 13 * s, 4 * s, 7 * s, BLOND)
    F(d, hx + 13 * s, cy - 13 * s, 4 * s, 7 * s, BLOND_D)
    F(d, hx - 11 * s, cy - 21 * s, 10 * s, 2 * s, BLOND_L)
    ey = cy - 3 * s
    for sgn in (-1, 1):
        ex = hx + sgn * 7 * s
        if blink:
            F(d, ex - 2.6 * s, ey, 5.2 * s, 1 * s, OL)
        else:
            F(d, ex - 2.8 * s, ey - 3.4 * s, 5.6 * s, 6.8 * s, WHT, r=int(s))
            px = ex - 1.6 * s + look * 1.2 * s
            F(d, px, ey - 2.4 * s, 3.2 * s, 5 * s, OL, r=int(.6 * s))
            F(d, px + .6 * s, ey - 2 * s, 1.2 * s, 1.4 * s, WHT)
        # narrowed lid
        F(d, ex - 3 * s, ey - 3.8 * s, 6 * s, 1.2 * s, SKIN_D)
        # brows: sharp, angled toward the nose
        F(d, ex - 3.5 * s, ey - 6.5 * s, 7 * s, 1.5 * s, (170, 130, 40))
        F(d, hx + sgn * 3.6 * s - 1 * s, ey - 5.3 * s, 2 * s, 1.5 * s, (170, 130, 40))
    F(d, hx - 1 * s, ey + 4 * s, 2 * s, 2 * s, SKIN_D)
    F(d, hx - 3 * s, ey + 9 * s, 7 * s, 1.4 * s, OL)
    F(d, hx + 4 * s, ey + 8 * s, 1.4 * s, 1.4 * s, OL)
    F(d, hx - 12 * s, ey + 4 * s, 3 * s, 1.4 * s, (240, 150, 150))
    F(d, hx + 9 * s, ey + 4 * s, 3 * s, 1.4 * s, (230, 150, 140))


# ------------------------------------------------------------------ GRANDAD
def grandad_head(d, cx, hy, s, mouth_open=0.0, blink=False, look=(0, 0), wink=False, smile=True):
    for sgn in (-1, 1):
        R(d, cx + sgn * 10.5 * s - 1.5 * s, hy + 8 * s, 3 * s, 5 * s, SKIN)
    R(d, cx - 10 * s, hy, 20 * s, 18 * s, SKIN, r=int(3 * s))
    F(d, cx + 4 * s, hy + 2 * s, 6 * s, 15 * s, SKIN_D)
    F(d, cx - 6 * s, hy + 1.5 * s, 5 * s, 2 * s, SKIN_L)  # bald shine
    # white side tufts
    for sgn in (-1, 1):
        R(d, cx + sgn * 10 * s - (4 * s if sgn > 0 else 0), hy + 4 * s, 4 * s, 7 * s, BEARD, r=int(1.5 * s))
    ey = hy + 9 * s
    # glasses
    for sgn in (-1, 1):
        ex = cx + sgn * 4.6 * s
        R(d, ex - 3.4 * s, ey - 2.6 * s, 6.8 * s, 5.2 * s, (230, 238, 248), r=int(.8 * s))
        if blink or (wink and sgn > 0):
            F(d, ex - 2 * s, ey + .4 * s, 4 * s, .9 * s, OL)
        else:
            F(d, ex - 1.3 * s + look[0] * .8 * s, ey - 1.4 * s, 2.6 * s, 3 * s, OL)
            F(d, ex - .8 * s + look[0] * .8 * s, ey - 1.1 * s, .9 * s, .9 * s, WHT)
        F(d, ex - 3 * s, ey - 4.6 * s, 6 * s, 1.2 * s, BEARD_D)  # bushy brows
    F(d, cx - 1.2 * s, ey - .6 * s, 2.4 * s, .8 * s, OL)  # bridge
    F(d, cx - 1 * s, ey + 3 * s, 2.2 * s, 2 * s, SKIN_D)  # nose
    # beard
    R(d, cx - 10 * s, ey + 4.5 * s, 20 * s, 11 * s, BEARD, r=int(4 * s))
    F(d, cx + 4 * s, ey + 6 * s, 5 * s, 8 * s, BEARD_D)
    R(d, cx - 5 * s, ey + 4 * s, 10 * s, 3 * s, BEARD, ol=None)  # moustache
    mo = mouth_open
    if mo > 0.1:
        F(d, cx - 2.5 * s, ey + 7.5 * s, 5 * s, (1 + 2.5 * mo) * s, (110, 40, 40), r=int(.6 * s))
    elif smile:
        F(d, cx - 3 * s, ey + 8 * s, 6 * s, 1 * s, (110, 40, 40))
        F(d, cx - 3.6 * s, ey + 7.2 * s, 1 * s, 1 * s, (110, 40, 40))
        F(d, cx + 2.6 * s, ey + 7.2 * s, 1 * s, 1 * s, (110, 40, 40))
    F(d, cx - 8.5 * s, ey + 2.5 * s, 2.2 * s, 1 * s, (240, 150, 150))
    F(d, cx + 6.3 * s, ey + 2.5 * s, 2.2 * s, 1 * s, (230, 150, 140))


def grandad_body(d, cx, ty, s, sitting=True):
    R(d, cx - 12 * s, ty, 24 * s, 18 * s, CARD, r=int(2 * s))
    F(d, cx + 5 * s, ty, 7 * s, 18 * s, CARD_D)
    F(d, cx - 10 * s, ty + 2 * s, 2.5 * s, 12 * s, CARD_L)
    F(d, cx - 3 * s, ty, 6 * s, 5 * s, (238, 232, 214))  # shirt
    F(d, cx - .5 * s, ty + 5 * s, 1 * s, 13 * s, CARD_D)
    for k in range(3):
        F(d, cx - 1.2 * s, ty + 6 * s + k * 4 * s, 2.4 * s, 2.4 * s, BTN)
    F(d, cx - 9 * s, ty + 11 * s, 5 * s, 3 * s, CARD_D)  # pocket


# ------------------------------------------------------------------ misc people
def person_front(d, cx, fy, s, shirt, shirt_d, skin=SKIN, skin_d=SKIN_D, hair=HAIR, pants=(40, 44, 60),
                 expr="flat", look=(0, 0), blink=False, t=0.0, cap=None, hairstyle="short"):
    br = math.sin(t * 2.2 + cx) * 0.3 * s
    for sgn in (-1, 1):
        x = cx + sgn * 4.5 * s
        R(d, x - 3 * s, fy - 12 * s, 6 * s, 10 * s, pants)
        R(d, x - 3.5 * s, fy - 2.4 * s, 7 * s, 2.4 * s, (30, 28, 36))
    ty = fy - 29 * s + br
    R(d, cx - 11 * s, ty, 22 * s, 18 * s, shirt, r=int(1.5 * s))
    F(d, cx + 5 * s, ty, 6 * s, 18 * s, shirt_d)
    for sgn in (-1, 1):
        sh = (cx + sgn * 10 * s, ty + 3 * s)
        hand = (cx + sgn * 13 * s, ty + 15 * s)
        limb(d, sh, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), 5.5 * s, shirt if sgn < 0 else shirt_d)
        limb(d, (lerp(sh[0], hand[0], .45), lerp(sh[1], hand[1], .45)), hand, 4.2 * s, skin)
    hy = ty - 19 * s
    R(d, cx - 3 * s, hy + 16 * s, 6 * s, 4 * s, skin_d)
    R(d, cx - 10 * s, hy, 20 * s, 18 * s, skin, r=int(2.5 * s))
    F(d, cx + 4 * s, hy + 3 * s, 6 * s, 14 * s, skin_d)
    if hairstyle == "pony":
        R(d, cx - 11 * s, hy - 1.5 * s, 22 * s, 8 * s, hair, r=int(3 * s))
        F(d, cx - 11 * s, hy + 4 * s, 3 * s, 8 * s, hair)
        F(d, cx + 8 * s, hy + 4 * s, 3 * s, 8 * s, hair)
    else:
        R(d, cx - 10.5 * s, hy - 1.5 * s, 21 * s, 6 * s, hair, r=int(2 * s))
    if cap:
        R(d, cx - 11 * s, hy - 3 * s, 22 * s, 6 * s, cap, r=int(2 * s))
        F(d, cx - 13 * s, hy + 2 * s, 12 * s, 2 * s, cap)
    ey = hy + 10 * s
    for sgn in (-1, 1):
        eye(d, cx + sgn * 4.5 * s, ey, s, look, blink)
        F(d, cx + sgn * 4.5 * s - 2 * s, ey - 4 * s, 4 * s, .9 * s, hair if hair != BEARD else BEARD_D)
    F(d, cx - .5 * s, ey + 2.5 * s, 1.2 * s, 1.2 * s, skin_d)
    mouth(d, cx, ey + 5 * s, s * .8, expr)
