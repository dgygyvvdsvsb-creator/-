"""'Start here' recap video — From Zero to Legend. Reuses the EP5 style + some EP5 scenes."""
import os, sys, json
import build
from build import *   # style helpers, sets and EP5 scenes

EP_LABEL = "START HERE"
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
RLINES = [
    [("YOU'RE", W), ("ELEVEN.", Y), ("FIRST", W), ("MATCH...", W), ("ZERO.", R_), ("TEN.", R_)],
    [("GRANDAD", B), ("GIVES", W), ("YOU", W), ("HIS", W), ("OLD", W), ("GLOVES.", O), ("TWO", W), ("SIZES", W), ("TOO", W), ("BIG.", Y)],
    [("\"KEEPERS", W), ("AREN'T", W), ("MADE", W), ("BY", W), ("SAVES.", Y), ("THEY'RE", W), ("MADE", W), ("BY", W),
     ("GETTING", W), ("BACK", G), ("UP.\"", G)],
    [("SO", W), ("YOU", W), ("DIVE.", W), ("FIVE", Y), ("HUNDRED", Y), ("TIMES.", Y)],
    [("LAST", W), ("MINUTE.", W), ("MASON'S", R_), ("PENALTY.", W), ("YOU", W), ("DIVE", W), ("RIGHT...", B)],
    [("THE", W), ("BALL", W), ("GOES", W), ("LEFT.", R_)],
    [("THEN", W), ("GRANDAD", B), ("COLLAPSES.", R_), ("SEAT", W), ("FOURTEEN.", W)],
    [("HOSPITAL...", B), ("OR", W), ("THE", W), ("ACADEMY", Y), ("TRIAL?", Y), ("THE", W), ("COMMENTS", G), ("CHOSE", W),
     ("THE", W), ("TRIAL.", Y)],
    [("TWELVE", Y), ("KEEPERS.", W), ("ONE", W), ("PLACE.", Y)],
    [("YOU", W), ("SAVE", G), ("MASON'S", R_), ("PENALTY.", W), ("THEY", W), ("SIGN", Y), ("YOU.", G)],
    [("NOW", W), ("YOU'RE", W), ("NUMBER", W), ("THREE.", R_), ("THE", W), ("YOUNGEST.", W)],
    [("THEN", W), ("THEIR", W), ("NUMBER", W), ("ONE", Y), ("GETS", W), ("INJURED.", R_)],
    [("SATURDAY'S", W), ("DERBY.", Y), ("DIXON...", B), ("OR", W), ("YOU?", G)],
    [("AND", W), ("MASON", R_), ("JUST", W), ("WHISPERED", R_), ("TO", W), ("THE", W), ("COACH.", W)],
    [("GRANDAD", B), ("WILL", W), ("BE", W), ("THERE.", W), ("SEAT", B), ("FOURTEEN.", B)],
    [("EVERY", W), ("EPISODE,", W), ("THE", W), ("COMMENTS", G), ("DECIDE", Y), ("YOUR", W), ("STORY.", W)],
    [("THIS", W), ("IS", W), ("FROM", W), ("ZERO", W), ("TO", W), ("LEGEND.", Y),
     ("SUBSCRIBE." if PLATFORM == "youtube" else "FOLLOW.", R_), ("PART", Y), ("SIX", Y), ("DECIDES.", Y)],
]
FOLLOW_AT = 51.75   # where "Follow." starts in the recap take
# voice timings (filled by align_recap.py); fallback estimate for previews
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vo/recap_lines.json")
if os.path.exists(_vf):
    _j = json.load(open(_vf))
    RV = [tuple(x) for x in _j["lines"]]
    if PLATFORM == "youtube":   # "Follow." replaced by the "Subscribe. Part six decides." take
        RV[-1] = (RV[-1][0], FOLLOW_AT + (_j["yt_tail"][1] - _j["yt_tail"][0]))
else:
    RV, t0 = [], 0.1
    for ws in RLINES:
        d = 0.34 * len(ws) + 0.4
        RV.append((t0, t0 + d)); t0 += d + 0.35
RSTARTS = [max(0.0, a - 0.12) for a, _ in RV]
RSTARTS[0] = 0.0
RTOTAL = max(RV[-1][1] + 2.2, 61.5)   # always > 60 s (monetisation)


def rword_times(i):
    ws = RLINES[i]
    st, en = RV[i]
    lens = [len(w) + 2 for w, _ in ws]
    tot, acc, out = sum(lens), 0, []
    for (w, c), L in zip(ws, lens):
        out.append((w, st + (en - st) * acc / tot - 0.03, c))
        acc += L
    return out


def roverlay(img, t, i):
    d = ImageDraw.Draw(img)
    f = font(600, 19)
    a, b = "FROM ZERO TO ", "LEGEND · START HERE"
    wa, wb = d.textlength(a, font=f), d.textlength(b, font=f)
    x = (FW - wa - wb) / 2
    for txt, col, xx in ((a, (240, 240, 245), x), (b, C_Y, x + wa)):
        d.text((xx, 62), txt, font=f, fill=col, stroke_width=3, stroke_fill=OL)
    ch = chunks(rword_times(i))
    cur = ch[0]
    for c in ch:
        if t >= c[0][1] - 0.04:
            cur = c
    if i == 0 and t < 0.4:
        cur = [(w, -1, c) for w, _, c in cur]
    caption(img, cur, t, size=56, wrap=620)


HIDE_LABELS = {"DAY 4"}   # EP5-only labels that make no sense in the recap


def reuse(k, u):
    """play EP5 scene k at relative position u (0..1)"""
    T = build.STARTS[k]
    orig = build.pill
    build.pill = lambda img, x, y, text, *a, **kw: None if text in HIDE_LABELS else orig(img, x, y, text, *a, **kw)
    try:
        return build.SCENES[k](T + u * build.LINES[k][1], u, T)
    finally:
        build.pill = orig


def hand_xy(cx, by, s, hx, hy):
    """full-res position of a sprite pixel (sprite 24x39, margin 3,10), pasted bottom-centre at (cx,by), scale s"""
    return cx - 12 * s + (hx + 3 + 0.5) * s, by - 39 * s + (hy + 10 + 0.5) * s


def glove_pair(img, x, y, sc=1.0):
    d = ImageDraw.Draw(img)
    for dx in (-17 * sc, 17 * sc):
        d.rounded_rectangle([x + dx - 15 * sc, y - 18 * sc, x + dx + 15 * sc, y + 18 * sc], int(7 * sc), fill=(252, 140, 27), outline=OL, width=4)
        d.rectangle([x + dx - 15 * sc, y + 8 * sc, x + dx + 15 * sc, y + 18 * sc], fill=(206, 98, 14), outline=OL, width=3)


def ball_into_net(img, x0, y0, x1, y1, GL, p, hit=0.6, size=5):
    """0..hit: flight to (x1,y1) in the net; then gravity drop with two small bounces onto the grass at GL"""
    if p < hit:
        q = p / hit
        draw_ball_s(img, lerp(x0, x1, q), lerp(y0, y1, q), size)
        return False
    q = (p - hit) / (1 - hit)
    h0 = GL - y1
    if q < 0.45:
        y = y1 + h0 * (q / 0.45) ** 2
    elif q < 0.7:
        y = GL - h0 * 0.25 * math.sin((q - 0.45) / 0.25 * math.pi)
    elif q < 0.85:
        y = GL - h0 * 0.07 * math.sin((q - 0.7) / 0.15 * math.pi)
    else:
        y = GL
    draw_ball_s(img, x1, y, size)
    return True


def dive(img, x0, GL, side, phase, scale=8, ball_to=None, catch=False):
    """keeper: ready (0-.2) -> airborne parabola (.2-.7) -> lands flat on the grass (.7-1).
    returns glove position. side +1 = dives to screen right."""
    D = 120
    if phase < 0.2:
        shadow(img, x0, GL, 200)
        sp = paste(img, hero(pose="ready", gloves=True), scale, x0, GL)
        return x0 + side * 90, GL - 150
    a = clamp((phase - 0.2) / 0.5)
    x = x0 + side * D * ease_out(a)
    lift = math.sin(a * math.pi) * 110
    sp = big(hero(pose="reach", gloves=True, mouth="open"), scale).rotate(-90 if side > 0 else 90, expand=True, resample=Image.NEAREST)
    yb = GL + 3 * scale - lift                      # bottom of the body
    shadow(img, x, GL, sp.width * (0.9 - 0.3 * math.sin(a * math.pi)), 30, 80)
    img.alpha_composite(sp, (int(x - sp.width / 2), int(yb - sp.height)))
    gx = x + side * (sp.width / 2 - 47)
    gy = yb - sp.height / 2 + 4
    if a >= 1 and phase < 0.78:
        impact_lines(img, x, GL - 20, 0, (phase - 0.7) * 2, 8)   # landing dust
    return gx, gy


# ---------------------------------------------------------------- new scenes
def r_zero_ten(t, u, T):
    img = pitch_set()
    GL = 1040
    goal(img, 360, GL, 600, 300)
    k = int(u * 10)
    n = min(10, k + 1)
    phase = (u * 10) % 1
    side = 1 if k % 2 else -1
    for j in range(n - 1):   # balls already in the net, lying on the grass
        draw_ball_s(img, 110 + (j * 53) % 500, GL - 4 - (j % 2) * 6, 4)
    dive(img, 360, GL, -side, phase)              # wrong way every time
    ball_into_net(img, 360, 1300, 360 + side * 220, GL - 160, GL - 4, phase, 0.6, 5)
    score_bar(img, 1110, "YOU", "RIVERS", f"0 - {n if phase > 0.6 else n - 1}", "1ST MATCH")
    img = flash(img, 0.25 * clamp(1 - abs(phase - 0.62) * 12), (255, 60, 60))
    return cam(img, 1 + 0.04 * u, 360, 900)


def r_gloves(t, u, T):
    img = sky_trees(top=(150, 150, 190), bot=(200, 196, 214), key="dusk").convert("RGBA")
    crowd_band(img, 430, 520, seed=8); pitch(img, 520)
    shadow(img, 230, 1120, 260); shadow(img, 470, 1120, 220)
    paste(img, cane(), 12, 102, 1120)
    paste(img, grandad(pose="stand", mouth="smile"), 12, 230, 1120)
    paste(img, hero(mouth="smile", look=-1), 10, 470, 1120)
    g = hand_xy(230, 1120, 12, 16, 15)      # Grandad's hand (screen right)
    h = hand_xy(470, 1120, 10, 1, 15)       # your hand (screen left)
    k = ease_in_out(clamp((u - 0.2) / 0.35))
    gx, gy = lerp(g[0] + 10, h[0] - 10, k), lerp(g[1] - 10, h[1] - 10, k)
    if 0 < k < 1:
        glow_ring(img, gx, gy, 60, 0.5, (255, 200, 120))
    glove_pair(img, gx, gy, 1.0)
    if u > 0.6:
        pill(img, 360, 470, "2 SIZES TOO BIG", (200, 120, 20), spring(t - T - 0.6 * (RV[1][1] - RV[1][0]), 13, 7), 30)
    return cam(img, 1 + 0.05 * u, 360, 900)


def r_quote(t, u, T):
    img = sky_trees(top=(150, 150, 190), bot=(200, 196, 214), key="dusk").convert("RGBA")
    crowd_band(img, 430, 520, seed=8); pitch(img, 520)
    img = img.filter(ImageFilter.GaussianBlur(3))
    talk = "open" if int(t * 7) % 2 else "smile"
    paste(img, grandad(pose="stand", mouth=talk, blink=(u % 0.4) > 0.37), 24, 360, 1560)
    bubble(img, 360, 560, "KEEPERS AREN'T MADE BY SAVES.\nTHEY'RE MADE BY GETTING BACK UP.", spring(t - T - 0.1, 13, 7), 26)
    return cam(img, 1.03 + 0.04 * u, 360, 800)


def r_dives(t, u, T):
    img = sky_trees(top=(120, 150, 200), bot=(186, 206, 230), key="day2").convert("RGBA")
    crowd_band(img, 430, 520, seed=5); pitch(img, 520)
    GL = 1040
    goal(img, 360, GL, 600, 300)
    k = int(u * 4)
    phase = (u * 4) % 1
    side = 1 if k % 2 else -1
    gx, gy = dive(img, 360, GL, side, phase)
    if phase < 0.45:   # ball flying to where the gloves will be
        tx, ty = 360 + side * 200, GL - 150
        bp = clamp(phase / 0.45)
        draw_ball_s(img, lerp(360 - side * 60, tx, bp), lerp(1320, ty, bp), 5)
    else:              # caught: ball stays in the gloves, through the landing
        draw_ball_s(img, gx, gy + 34, 5)
        if phase < 0.55:
            glow_ring(img, gx, gy, 60, 0.6, (255, 255, 200))
    n = int(1 + 499 * ease_in_out(u))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([180, 1100, 540, 1230], 18, fill=(16, 18, 36), outline=C_Y, width=5)
    d.text((360, 1135), "NO DAYS OFF", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
    d.text((360, 1192), f"DIVES {n}", font=font(800, 40), fill=C_Y, anchor="mm")
    return cam(img, 1 + 0.03 * u, 360, 900)


def r_wrong(t, u, T):
    img = pitch_set()
    GL = 1040
    goal(img, 360, GL, 600, 300)
    dive(img, 360, GL, 1, clamp(u * 1.1))          # dives RIGHT and lands
    bx, by = 160, GL - 170
    k = clamp((u - 0.1) / 0.4)
    ball_into_net(img, 380, 1320, bx, by, GL - 4, clamp((u - 0.1) / 0.9), 0.45, 5)   # ball goes LEFT into the net
    if k >= 1:
        impact_lines(img, bx, by - 30, T + 0.5 * (RSTARTS[6] - T), t, 12)
        pill(img, 360, 520, "GOAL · 0-1", (200, 40, 50), spring(t - T - 0.5 * (RSTARTS[6] - T), 13, 7), 36)
    img = flash(img, 0.4 * clamp(1 - abs(u - 0.5) * 10), (255, 50, 50))
    return cam(img, 1.03, 360, 860, *shake(t, T + 0.5 * (RSTARTS[6] - T), .3, 12))


def r_collapse(t, u, T):
    img = Image.new("RGBA", (FW, FH), (40, 30, 44, 255))
    crowd_band(img, 0, 700, seed=14, blur=4)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 700, FW, FH], fill=(70, 72, 90))
    for x in (40, 260, 480):   # seats
        d.rounded_rectangle([x, 620, x + 200, 900], 20, fill=(170, 40, 52), outline=OL, width=6)
        d.rounded_rectangle([x, 880, x + 200, 960], 14, fill=(140, 30, 44), outline=OL, width=6)
    d.rounded_rectangle([320, 650, 400, 700], 8, fill=(245, 236, 220), outline=OL, width=4)
    d.text((360, 676), "14", font=font(800, 34), fill=(170, 30, 40), anchor="mm")
    # the cane falls (gravity + bounce)
    k = clamp(u / 0.5)
    ang = 90 * ease_in_out(k) ** 2
    c = big(cane(26), 9).rotate(-ang, expand=True, resample=Image.NEAREST)
    img.alpha_composite(c, (int(330 + ang * 1.2), int(1180 - c.height)))
    # blue lights
    if u > 0.35:
        p = (t * 5) % 1
        ov = Image.new("RGBA", img.size, (60, 140, 255, int(90 if p < 0.5 else 20)))
        img.alpha_composite(ov)
    pill(img, 360, 1230, "AMBULANCE", (40, 90, 200), spring(t - T - 0.5, 13, 7), 30) if u > 0.4 else None
    return cam(img, 1 + 0.06 * u, 360, 800, *shake(t, T + 0.5 * 2, .3, 10))


def r_choice(t, u, T):
    img = choice_bg()
    d = ImageDraw.Draw(img)
    cards = [(190, "HOSPITAL", "41%", C_B), (530, "TRIAL", "59%", C_Y)]
    for i, (x, lab, pct, c) in enumerate(cards):
        k = spring(t - T - i * 0.15, 13, 7)
        if k < 0.05:
            continue
        win = i == 1 and u > 0.55
        w, h = 300 * k * (1.06 if win else 1), 400 * k * (1.06 if win else 1)
        d.rounded_rectangle([x - w / 2, 760 - h / 2, x + w / 2, 760 + h / 2], 24, fill=(16, 18, 36), outline=c, width=9 if win else 6)
        if k > 0.6:
            if lab == "HOSPITAL":
                d.rounded_rectangle([x - 70, 620, x + 70, 720], 10, fill=(240, 240, 248), outline=OL, width=5)
                d.rectangle([x - 10, 640, x + 10, 700], fill=(220, 40, 50)); d.rectangle([x - 30, 660, x + 30, 680], fill=(220, 40, 50))
            else:
                goal(img, x, 730, 180, 100)
                paste(img, hero(pose="ready", gloves=True), 3, x, 730)
            d.text((x, 830), lab, font=font(800, 44), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            if u > 0.55:
                d.text((x, 890), pct, font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    if u > 0.55:
        pill(img, 530, 520, "THE COMMENTS CHOSE", (40, 150, 80), spring(t - T - 0.55 * 3.8, 13, 7), 26)
    return cam(img, 1 + 0.03 * u, 360, 760)


def r_twelve(t, u, T):
    img = pitch_set()
    kits = [(246, 206, 40), (60, 120, 210), (210, 52, 56), (130, 60, 170), (240, 140, 40), (240, 240, 245)]
    # two rows of six, back row smaller and higher, staggered: every face stays visible
    order = list(range(12))
    pos = {}
    for i in order:
        row = 0 if i < 6 else 1               # 0 = back row
        col = i % 6
        if row == 0:
            pos[i] = (118 + col * 97, 960, 4)
        else:
            pos[i] = (70 + col * 116, 1170, 5)
    for i in order:                            # back row first, front row on top
        x, y, sc = pos[i]
        sk = ["light", "tan", "brown", "dark"][i % 4]
        if i == 8:
            sp = hero(gloves=True)
        else:
            sp = person(Kit(kits[i % 6], (30, 30, 40), kits[i % 6], [1,2,3,4,5,6,7,8,0,9,4,6][i]), skin=sk, hair=["dark", "blond", "black", "ginger"][i % 4],
                        style=["short", "spiky", "curly", "short"][i % 4], gloves=False)
        shadow(img, x, y, 70 if sc == 4 else 90)
        paste(img, sp, sc, x, y + math.sin(t * 4 + i) * 2)
    pill(img, 360, 560, "12 KEEPERS · 1 PLACE", (60, 60, 80), spring(t - T, 13, 7), 32)
    k = clamp((u - 0.4) / 0.3)
    if k > 0:
        glow_ring(img, pos[8][0], pos[8][1] - 110, 80, 0.7 * k, C_Y)
    return cam(img, 1 + 0.03 * u, 360, 1060)


def r_signed(t, u, T):
    img = pitch_set()
    GL = 1040
    goal(img, 360, GL, 600, 300)
    phase = clamp(u * 1.25)
    gx, gy = dive(img, 360, GL, 1, phase)
    if phase < 0.45:
        bp = clamp(phase / 0.45)
        draw_ball_s(img, lerp(380, 360 + 200, bp), lerp(1320, GL - 150, bp), 5)
    else:
        draw_ball_s(img, gx, gy + 34, 5)
        if phase < 0.6:
            glow_ring(img, gx, gy, 70, 0.7, (255, 255, 200))
    shadow(img, 620, 1250, 90)
    paste(img, coach(look=-1), 5, 620, 1250)
    if u > 0.55:
        k = spring(t - T - 0.55 * (RSTARTS[10] - T), 13, 7)
        d = ImageDraw.Draw(img)
        w, h = 420 * k, 200 * k
        d.rounded_rectangle([360 - w / 2, 560 - h / 2, 360 + w / 2, 560 + h / 2], 18, fill=(250, 246, 236), outline=OL, width=6)
        if k > 0.6:
            d.text((360, 520), "RIVERSIDE ACADEMY", font=font(800, 26), fill=(30, 40, 80), anchor="mm")
            d.text((360, 590), "SIGNED", font=font(800, 52), fill=(40, 150, 80), anchor="mm")
    return cam(img, 1.02, 360, 900)


def r_comments(t, u, T):
    img = choice_bg()
    d = ImageDraw.Draw(img)
    msgs = [("TRIAL!! 🔥".replace("🔥", ""), C_Y), ("DIVE RIGHT", C_B), ("GOALKEEPER!", C_G), ("ASK FOR THE SHIRT", C_O),
            ("WAIT...", C_B), ("GO TO GRANDAD", C_R)]
    for i, (m, c) in enumerate(msgs):
        k = spring(t - T - i * 0.28, 13, 7)
        if k < 0.05:
            continue
        y = 360 + i * 140
        x = 120 if i % 2 == 0 else 220
        w = 480 * k
        d.rounded_rectangle([x, y, x + w, y + 110], 22, fill=(250, 250, 252), outline=OL, width=4)
        if k > 0.6:
            d.ellipse([x + 16, y + 25, x + 76, y + 85], fill=c, outline=OL, width=3)
            d.text((x + 96, y + 36), "viewer", font=font(700, 20), fill=(120, 124, 140), anchor="lm")
            d.text((x + 96, y + 74), m, font=font(800, 30), fill=(20, 22, 34), anchor="lm")
            d.text((x + w - 30, y + 74), "♥".replace("♥", "+1"), font=font(800, 24), fill=C_R, anchor="rm")
    return img


def r_end(t, u, T):
    img = choice_bg()
    d = ImageDraw.Draw(img)
    k = spring(t - T, 14, 7)
    py = lerp(1400, 400, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 600], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 80), "FROM ZERO", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 140), "TO LEGEND", font=font(800, 56), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
    tap = T + 1.2
    after = t > tap
    label = ("SUBSCRIBED" if after else "SUBSCRIBE") if PLATFORM == "youtube" else ("FOLLOWING" if after else "+ FOLLOW")
    pul = 1 + (0.05 * math.sin(t * 9) if not after else 0)
    bw, bh = 330 * pul, 96 * pul
    bx, by = 440, py + 280
    d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], 22, fill=(60, 64, 90) if after else (234, 46, 72), outline=OL, width=5)
    d.text((bx, by), label, font=font(800, 36 if after else 40), fill=(255, 255, 255), anchor="mm")
    if after and t < tap + 0.5:
        glow_ring(img, bx, by, 60 + 300 * (t - tap), 0.8 * (1 - (t - tap) / 0.5), C_Y)
    if t < tap + 0.4:
        gx = lerp(760, bx + 100, ease_in_out((t - T) / 1.2)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 1.2))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    d.text((360, py + 420), "PART 6 · YOUR VOTE DECIDES", font=font(800, 28), fill=C_G, anchor="mm")
    for x, lab, c in ((230, "ASK", C_O), (490, "WAIT", C_B)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 100, py + 470 - hop, x + 100, py + 540 - hop], 18, fill=(30, 36, 76), outline=c, width=5)
        d.text((x, py + 505 - hop), lab, font=font(800, 36), fill=c, anchor="mm")
    return img


RSCENES = [
    r_zero_ten, r_gloves, r_quote, r_dives,
    lambda t, u, T: reuse(10, u),          # Mason's penalty (keeper's view)
    r_wrong, r_collapse, r_choice, r_twelve, r_signed,
    lambda t, u, T: reuse(8, u),           # you, number three
    lambda t, u, T: reuse(15, u),          # Okafor injured
    lambda t, u, T: reuse(16, 0.55 + 0.45 * u),   # Dixon or you
    lambda t, u, T: reuse(17, u),          # Mason whispers
    lambda t, u, T: reuse(14, u),          # Grandad, seat 14
    r_comments, r_end,
]


def rline_at(t):
    i = 0
    for k, s in enumerate(RSTARTS):
        if t >= s:
            i = k
    return i


def rframe(t):
    i = rline_at(t)
    T = RSTARTS[i]
    end = RSTARTS[i + 1] if i + 1 < len(RSTARTS) else RTOTAL
    u = clamp((t - T) / max(0.1, end - T))
    img = RSCENES[i](t, u, T).convert("RGBA")
    if i > 0 and t - T < 0.07:
        img = flash(img, 0.35)
    roverlay(img, t, i)
    return img.convert("RGB")


if __name__ == "__main__":
    ts = [float(x) for x in sys.argv[1].split(",")]
    ims = [rframe(x).resize((240, 427)) for x in ts]
    out = Image.new("RGB", (240 * min(6, len(ims)), 427 * ((len(ims) + 5) // 6)))
    for k, im in enumerate(ims):
        out.paste(im, (240 * (k % 6), 427 * (k // 6)))
    out.save(sys.argv[2])
    print("RTOTAL", RTOTAL, [round(s, 1) for s in RSTARTS])
