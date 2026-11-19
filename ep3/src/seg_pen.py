"""Segments A (3.53-6.83) and B (9.50-18.13): keeper's-view penalty."""
from pitch import *

ENV = np.load("env.npy")  # rms, lo, hi at 50 ms
LO = ENV[1] / np.percentile(ENV[1], 99)


def lo_at(t):
    i = int(t / 0.05)
    return float(np.clip(LO[min(i, len(LO) - 1)], 0, 1.4))


def keeper_layer(t, x, fy, s, arms=1.0, lean=0.0, crouch=0.3, rot=0.0, look=0.0):
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if rot == 0:
        hero_back(d, x, fy, s, arms=arms, lean=lean, crouch=crouch, t=t, look=look)
        return lay
    # draw centred in a temp layer then rotate around body centre
    tmp = Image.new("RGBA", (CW * 2, CH * 2), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    hero_back(td, CW, CH + 28 * s, s, arms=arms, lean=lean, crouch=crouch, t=t, look=look)
    tmp = tmp.rotate(rot, resample=Image.NEAREST, center=(CW, CH))
    lay.paste(tmp, (int(x - CW), int(fy - 28 * s - CH)), tmp)
    return lay


def compose(t, mason=None, keeper=None, ballp=None, zoom=1.0, zc=(360, 470), shake_xy=(0, 0), extra_canvas=None,
            motion_blur_keeper=False):
    img = far_bg().copy().convert("RGBA")
    pc = pitch_static().copy()
    d = ImageDraw.Draw(pc)
    if mason:
        mason_at(d, t, **mason)
    if ballp:
        bx, by, br, sh_xy, spin = ballp
        if sh_xy:
            sx, sy, sr = sh_xy
            d.ellipse([sx - sr, sy - sr * .3, sx + sr, sy + sr * .3], fill=(30, 60, 32))
        ball(d, bx, by, br, spin)
    if extra_canvas:
        extra_canvas(d)
    img.alpha_composite(up(pc))
    if keeper is not None:
        kl = up(keeper)
        img.alpha_composite(kl)
    img = img.convert("RGB")
    img = transform(img, zoom, shake_xy[0], shake_xy[1], zc[0], zc[1])
    return img


# ----------------------------------------------------------------- SEGMENT A
def poll_card(img, t, t0=3.70, tout=4.95):
    """in-world poll result card. slams in at t0, flies into keeper at tout"""
    if t < t0:
        return
    k = spring(t - t0, 14, 7)
    fly = ease_in_out((t - tout) / 0.45) if t > tout else 0
    if fly >= 1:
        return
    W_, H_ = 560, 300
    sc = k * (1 - 0.8 * fly)
    cx = 360 + fly * 120
    cy = 560 + fly * 420
    card = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 26, fill=(14, 18, 44, 235), outline=(250, 210, 35), width=5)
    f1, f2 = font(800, 30), font(700, 34)
    d.text((W_ / 2, 40), "YOUR VOTES · EP. 2", font=f1, fill=(250, 210, 35), anchor="mm")
    # row 1 DIVE RIGHT
    fill_k = ease_out((t - 3.95) / 0.5)
    for i, (lab, pct, col) in enumerate((("DIVE RIGHT", 100, C_B), ("DIVE LEFT", 0, (120, 126, 150)))):
        y = 90 + i * 100
        d.rounded_rectangle([24, y, W_ - 24, y + 80], 16, fill=(30, 36, 76, 255), outline=(250, 210, 35) if i == 0 else (60, 66, 110), width=4)
        d.text((48, y + 40), lab, font=f2, fill=(255, 255, 255) if i == 0 else (150, 155, 175), anchor="lm")
        bw = 150 * (pct / 100) * fill_k
        d.rounded_rectangle([300, y + 30, 450, y + 50], 10, fill=(50, 56, 96))
        if bw > 4:
            d.rounded_rectangle([300, y + 30, 300 + bw, y + 50], 10, fill=col)
        d.text((W_ - 44, y + 40), f"{int(pct * fill_k)}%", font=f2, fill=col if i == 0 else (150, 155, 175), anchor="rm")
        if i == 1 and t > 4.2:  # crossed out
            kk = ease_out((t - 4.2) / 0.2)
            d.line([(40, y + 44), (40 + (W_ - 100) * kk, y + 36)], fill=(238, 78, 79), width=7)
    if t > 4.2:  # check stamp
        kk = spring(t - 4.2, 16, 8)
        r = 34 * kk
        d.ellipse([W_ - 70 - r, 70 - r + 60, W_ - 70 + r, 70 + r + 60], fill=(110, 222, 120))
        if kk > .5:
            d.line([(W_ - 86, 130), (W_ - 74, 142), (W_ - 52, 116)], fill=(255, 255, 255), width=8)
    card = card.resize((max(1, int(W_ * sc)), max(1, int(H_ * sc))), Image.BILINEAR)
    img.paste(card, (int(cx - card.width / 2), int(cy - card.height / 2)), card)


def dashed_arrow(img, pts, t0, dur, color, width=10, label=None, label_t=None, head=True, dash=26):
    """draw a dashed polyline progressively (full-res coords)"""
    if not pts or img is None:
        return
    d = ImageDraw.Draw(img)
    # resample path
    seg = []
    L = 0
    for a, b in zip(pts, pts[1:]):
        l = math.dist(a, b)
        seg.append((a, b, l))
        L += l
    prog = L * clamp(t0 if dur == 0 else t0 / dur)
    acc = 0
    end = None
    for a, b, l in seg:
        s0 = acc
        acc += l
        k = s0
        while k < min(acc, prog):
            u0 = (k - s0) / l
            u1 = min((min(k + dash * .6, acc, prog) - s0) / l, 1)
            p0 = (lerp(a[0], b[0], u0), lerp(a[1], b[1], u0))
            p1 = (lerp(a[0], b[0], u1), lerp(a[1], b[1], u1))
            d.line([p0, p1], fill=OL, width=width + 6)
            d.line([p0, p1], fill=color, width=width)
            k += dash
        if prog <= acc:
            u = (prog - s0) / l if l else 0
            end = ((lerp(a[0], b[0], u), lerp(a[1], b[1], u)), math.atan2(b[1] - a[1], b[0] - a[0]))
            break
    if end is None:
        a, b, l = seg[-1]
        end = (b, math.atan2(b[1] - a[1], b[0] - a[0]))
    if head and prog > 10:
        (x, y), ang = end
        hs = width * 2.6
        p = [(x + math.cos(ang) * hs, y + math.sin(ang) * hs),
             (x + math.cos(ang + 2.4) * hs, y + math.sin(ang + 2.4) * hs),
             (x + math.cos(ang - 2.4) * hs, y + math.sin(ang - 2.4) * hs)]
        d.polygon(p, fill=color, outline=OL, width=4)


def pill_label(img, x, y, text, color, k=1.0, size=40, fg=(255, 255, 255)):
    if k <= 0.02:
        return
    f = font(800, int(size * max(.1, k)))
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=f)
    h = size * k
    d.rounded_rectangle([x - w / 2 - 18 * k, y - h * .75, x + w / 2 + 18 * k, y + h * .75], int(14 * k), fill=color, outline=OL, width=5)
    d.text((x, y), text, font=f, fill=fg, anchor="mm", stroke_width=3, stroke_fill=OL)


def seg_A(t):
    # Mason far away places the ball, keeper ready; poll card; then RIGHT arrow on the grass
    lean = 0.0
    if t > 5.6:
        lean = ease_in_out((t - 5.6) / 0.6) * 1.5
    keeper = keeper_layer(t, 128 + lean * 6, 760, 5.4, arms=0.85 + 0.1 * math.sin(t * 3), lean=lean, crouch=.5)
    mode = "stand"
    mz = 13.9
    img = compose(t, mason={"mode": mode, "Z": 12.6, "X": 0.4, "expr": "smirk"},
                  ballp=(*proj(0, 13), 3.2, None, 0) if True else None,
                  keeper=keeper, zoom=1.0 + 0.05 * (t - 3.53) / 3.3, zc=(360, 500))
    img = img.convert("RGBA")
    # arrow from keeper's right glove toward the right post (on the grass)
    if t > 5.40:
        k = (t - 5.40) / 0.5
        pts = [(470, 1080), (580, 960), (650, 840), (670, 740)]
        dashed_arrow(img, pts, clamp(k), 1, C_B, width=12)
    if t > 5.93:
        pill_label(img, 590, 680, "RIGHT", (40, 120, 200), spring(t - 5.93, 14, 7), 48)
    poll_card(img, t)
    rain(img, t)
    img = img.convert("RGB")
    img = flash(img, 0.35 * clamp(1 - (t - 3.70) / 0.12) if t >= 3.70 else 0)
    img = tint_vignette(img, 0.45, (5, 6, 20))
    overlay_text(img, t)
    return img


# ----------------------------------------------------------------- SEGMENT B
def ecg(img, t, beat):
    """heart monitor strip at the bottom"""
    d = ImageDraw.Draw(img)
    y0 = 640
    X0, X1 = 400, 690
    d.rounded_rectangle([X0, y0 - 46, X1, y0 + 40], 14, fill=(8, 10, 24), outline=(238, 78, 79), width=3)
    pts = []
    for i in range(0, X1 - X0 - 20, 3):
        x = X0 + 10 + i
        tt = t - (X1 - X0 - 20 - i) / (X1 - X0 - 20) * 1.6
        v = lo_at(max(0, tt))
        y = y0 + 22 - v * 40 * (1 if (i // 3) % 2 else 0.5)
        pts.append((x, y))
    d.line(pts, fill=(238, 78, 79), width=4)
    f = font(800, 26)
    bpm = 120 + int(60 * min(1, (t - 9.5) / 4))
    d.text((640, y0 - 32), f"♥ {bpm}", font=f, fill=(238, 78, 79), anchor="ra") if False else d.text((X1 - 12, y0 - 40), f"{bpm} BPM", font=f, fill=(238, 78, 79), anchor="ra")


def seg_B1(t):
    """9.50-12.40 keeper's view, heartbeat"""
    beat = lo_at(t)
    zoom = 1.0 + 0.10 * ease_in_out((t - 9.5) / 2.9) + 0.025 * beat
    keeper = keeper_layer(t, 128, 760, 5.4, arms=0.9 + 0.05 * beat, crouch=.5 + .05 * beat)
    img = compose(t, mason={"mode": "stand", "Z": 12.6, "X": 0.5, "expr": "smirk"},
                  ballp=(*proj(0, 13), 3.2, None, 0), keeper=keeper, zoom=zoom, zc=(380, 470))
    img = img.convert("RGBA")
    rain(img, t)
    img = img.convert("RGB")
    img = tint_vignette(img, 0.35 + 0.35 * beat, (120, 0, 10))
    img = img.convert("RGBA")
    ecg(img, t, beat)
    img = img.convert("RGB")
    overlay_text(img, t)
    return img


def seg_B2(t):
    """12.40-13.85 Mason close-up, low angle, eyes LEFT then RIGHT"""
    img = far_bg().crop((0, 60, 720, 440)).resize((FW, FH), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
    img = transform(img, 1.0 + 0.04 * (t - 12.4), 0, 0)
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    if t < 12.75:
        look = 0.0
    elif t < 13.33:
        look = -ease_out((t - 12.75) / 0.15)
    else:
        look = -1 + 2 * ease_out((t - 13.6) / 0.15) if t > 13.6 else -1
    blink = 13.2 < t < 13.28
    z = 1 + 0.06 * (t - 12.4)
    mason_portrait(d, 180, 420, 4.9 * z, look=look, blink=blink, t=t)
    img = img.convert("RGBA")
    img.alpha_composite(up(c))
    rain(img, t, alpha=55)
    # tactical arrows: LEFT? then RIGHT?
    if t > 12.95:
        k = ease_out((t - 12.95) / 0.3)
        pts = [(330, 1190), (220, 1120), (120, 1010)]
        dashed_arrow(img, pts, k, 1, C_Y, width=12)
        pill_label(img, 140, 960, "LEFT?", (200, 160, 20), spring(t - 13.03, 14, 7), 40)
    if t > 13.85 - 0.0 or t > 13.85:
        pass
    if t > 13.87:
        k = ease_out((t - 13.87) / 0.3)
        pts = [(390, 1190), (500, 1120), (600, 1010)]
        dashed_arrow(img, pts, k, 1, C_B, width=12)
        pill_label(img, 580, 960, "RIGHT?", (40, 120, 200), spring(t - 13.95, 14, 7), 40)
    img = img.convert("RGB")
    img = tint_vignette(img, 0.5, (8, 4, 16))
    overlay_text(img, t)
    return img


KICK = 14.30
DIVE = 14.50
SLOW0 = 14.62  # slow-motion begins
NET = 18.08


def story_time(t):
    """real-time until SLOW0 then 0.22x slow motion (for the ball + keeper physics)"""
    if t < SLOW0:
        return t
    return SLOW0 + (t - SLOW0) * 0.22


def ball_state(t):
    """ball world position after the kick: from spot toward keeper's LEFT (screen left)"""
    st = story_time(t)
    if st < KICK:
        return 0.0, 13.0, 0.0
    u = (st - KICK) / 0.95  # 0..1 to reach the goal line in story time
    X = lerp(0, -4.2, u)
    Z = lerp(13.0, 2.0, u)
    Y = 0.55 * math.sin(clamp(u) * math.pi * 0.85) + 0.1 * u
    return X, Z, Y


def seg_B3(t):
    """13.85-16.67 keeper's view: run-up, kick, you dive right (slow motion)"""
    st = story_time(t)
    # Mason run-up 13.85 -> 14.30
    if t < KICK:
        u = (t - 14.0) / (KICK - 14.0)
        mz = lerp(15.0, 12.4, ease_in_out(u))
        mx = lerp(-1.6, -0.6, u)
        mason = {"mode": "run", "phase": u * 3, "Z": mz, "X": mx, "expr": "flat"}
    else:
        mason = {"mode": "kick", "kick": clamp((st - KICK) / 0.25), "Z": 12.4, "X": -0.5, "expr": "flat"}
    # keeper dive (story time)
    dv = clamp((st - DIVE) / 0.55)
    kx = 128 + 170 * ease_out(dv)
    lift = math.sin(min(dv, 1) * math.pi * 0.7) * 260
    rot = -62 * ease_out(dv * 1.3)
    keeper = keeper_layer(t, kx, 760 - lift, lerp(5.4, 4.3, ease_out(dv)), arms=lerp(0.9, 2.0, ease_out(dv * 1.6)), crouch=0.5 * (1 - dv), rot=rot)
    # ball
    X, Z, Yb = ball_state(t)
    bx, by = proj(X * 0.55 if Z > 5 else X * 0.55 * (1 + (5 - Z) * 0.4), Z, Yb)
    br = 0.11 * FOC / Z
    sx, sy = proj(X * .55, Z)
    spin = st * 30
    zoom = 1.0 + 0.06 * clamp((t - 14.0) / 2.6)
    img = compose(t, mason=mason, keeper=keeper, ballp=(bx, by, br * 1.3, (sx, sy, br), spin), zoom=zoom,
                  zc=(360, 520), shake_xy=shake(t, KICK, 0.2, 7))
    img = img.convert("RGBA")
    # ball trail in slow motion
    if st > KICK:
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(1, 7):
            X2, Z2, Y2 = ball_state(t - k * 0.06)
            if Z2 >= 13:
                break
            x2, y2 = proj(X2 * .55, Z2, Y2)
            r2 = 0.11 * FOC / Z2 * 2.2
            d.ellipse([x2 * 2 - r2, y2 * 2 - r2, x2 * 2 + r2, y2 * 2 + r2], fill=(255, 255, 255, 50 - k * 7))
    # speed lines once slow-mo starts
    if t > SLOW0:
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(int(t * 30))
        for _ in range(16):
            y = rr.uniform(300, 1240)
            x = rr.uniform(0, 720)
            d.line([(x, y), (x + rr.uniform(60, 160), y)], fill=(255, 255, 255, 40), width=2)
    # "slow motion" letterbox bars
    if t > SLOW0:
        k = ease_out((t - SLOW0) / 0.3)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 720, int(36 * k)], fill=(0, 0, 0))
        d.rectangle([0, 1280 - int(70 * k), 720, 1280], fill=(0, 0, 0))
    # dive arrow
    if t > DIVE:
        k = clamp((t - DIVE) / 0.5)
        dashed_arrow(img, [(260, 1060), (420, 900), (600, 830)], k, 1, C_B, width=10)
    rain(img, st, alpha=60)
    img = img.convert("RGB")
    img = flash(img, 0.6 * clamp(1 - (t - KICK) / 0.1) if t >= KICK else 0)
    img = tint_vignette(img, 0.5, (6, 6, 20))
    overlay_text(img, t)
    return img


def seg_B4(t):
    """16.67-18.13 behind the net: keeper flying right, ball comes LEFT into the net"""
    # local slow-mo then snap to real speed for the impact
    u = clamp((t - 16.67) / (NET - 16.67))
    img = far_bg().copy().convert("RGB")
    img = transform(img, 1.15, 0, 40, 360, 400)
    pc = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(pc)
    # ground seen from just behind the goal line (closer, lower)
    for i, (y0, col) in enumerate([(214, (60, 130, 60)), (260, (56, 124, 58)), (320, (64, 138, 64)), (400, (56, 124, 58)), (500, (104, 86, 54))]):
        F(d, 0, y0, CW, CH - y0, col)
    d.ellipse([20, 420, 340, 560], fill=(118, 98, 62))
    F(d, 0, 470, CW, 3, (236, 240, 236))  # goal line
    # posts + crossbar seen from behind (big, near)
    R(d, 4, 96, 10, 380, (245, 245, 250))
    R(d, 346, 96, 10, 380, (245, 245, 250))
    R(d, 4, 92, 352, 10, (245, 245, 250))
    # Mason far, frozen after the kick
    mason_front(d, 180, 268, 1.1, mode="kick", kick=1.0, expr="smirk", t=t)
    # keeper flying right in mid-air (back view, rotated)
    kl = Image.new("RGBA", (CW * 2, CH * 2), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kl)
    hero_back(kd, CW, CH + 28 * 2.6, 2.6, arms=2.0, crouch=0, t=t)
    kl = kl.rotate(-70 - 8 * u, resample=Image.NEAREST, center=(CW, CH))
    kx = 250 + 30 * u
    ky = 330 + 40 * u * u
    pc.paste(kl, (int(kx - CW), int(ky - CH)), kl)
    # ball path: from far (centre) toward camera on the LEFT side
    bu = ease_in_out(u) ** 1.6
    bx = lerp(185, 90, bu)
    by = lerp(300, 330, bu)
    br = lerp(3, 26, bu ** 2)
    spin = t * 8
    # shadow
    d.ellipse([bx - br, 470 - br * .2 + bu * 40, bx + br, 470 + br * .2 + bu * 40], fill=(40, 60, 36))
    ball(d, bx, by, br, spin)
    img = img.convert("RGBA")
    img.alpha_composite(up(pc))
    # big LEFT arrow along the ball path
    if t > 17.43:
        dashed_arrow(img, [(370, 600), (260, 640), (190, 690)], clamp((t - 17.43) / .3), 1, C_Y, width=12)
        pill_label(img, 210, 520, "LEFT", (200, 160, 20), spring(t - 17.43, 14, 7), 46)
    # net in the foreground (we are behind it), bulging when the ball hits
    bul = None
    if t > NET - 0.06:
        a = clamp((t - (NET - .06)) / .06)
        bul = (bx * 2, by * 2, a * 1.0)
    net_overlay(img, alpha=60, bulge=bul, cell=52, width=3)
    rain(img, t * 0.3, alpha=60)
    img = img.convert("RGB")
    img = transform(img, 1.0 + 0.08 * u, *shake(t, NET - .03, .2, 9), 200, 660)
    img = flash(img, 0.5 * clamp(1 - (t - NET) / .08) if t >= NET else 0)
    d = ImageDraw.Draw(img)
    k = 1
    d.rectangle([0, 0, 720, 36], fill=(0, 0, 0))
    d.rectangle([0, 1210, 720, 1280], fill=(0, 0, 0))
    img = tint_vignette(img, 0.5, (6, 6, 20))
    overlay_text(img, t)
    return img


def seg_B(t):
    if t < 12.40:
        return seg_B1(t)
    if t < 14.0:
        return seg_B2(t)
    if t < 16.67:
        return seg_B3(t)
    return seg_B4(t)
