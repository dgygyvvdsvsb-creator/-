"""EP5 — From Zero to Legend, remi_sport style. Scenes are timed per script line."""
import os, sys
from style import *

EP = 5
PLATFORM = os.environ.get("PLATFORM", "tiktok")

# (text with key-word colours, duration s). Word timing is spread by length inside a line.
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
LINES = [
    ([("FIRST", W), ("ACADEMY", Y), ("SHOT.", W), ("STRAIGHT", W), ("THROUGH", W), ("YOUR", W), ("GLOVES.", R_)], 3.1),
    ([("\"ZERO.", R_), ("LIKE", W), ("YOUR", W), ("SHIRT.\"", W), ("MASON.", R_)], 2.6),
    ([("RIVERSIDE", W), ("IS", W), ("HIS", R_), ("CLUB.", W)], 1.9),
    ([("TWO", Y), ("HOURS", Y), ("FROM", W), ("HOME.", W), ("A", W), ("BUNK", W), ("BED.", W), ("SIX", Y), ("A.M.", Y)], 3.8),
    ([("YOU", W), ("SAY", W), ("HI.", W), ("YOUR", W), ("ROOMMATE", W), ("TURNS", W), ("TO", W), ("THE", W), ("WALL.", R_),
      ("DIXON.", B), ("KEEPER", W), ("NUMBER", W), ("TWO.", B)], 5.4),
    ([("THREE", W), ("KEEPERS.", W), ("ONE", Y), ("YELLOW", Y), ("SHIRT.", Y)], 2.5),
    ([("OKAFOR.", Y), ("TWELVE...", W), ("AND", W), ("A", W), ("HEAD", W), ("TALLER.", Y)], 2.9),
    ([("DIXON.", B), ("NEVER", W), ("MAKES", W), ("A", W), ("MISTAKE.", B)], 2.4),
    ([("YOU.", G), ("THE", W), ("YOUNGEST.", W), ("NUMBER", W), ("THREE.", R_)], 2.7),
    ([("DAY", W), ("TWO,", W), ("YOU", W), ("LET", W), ("IN", W), ("NINE.", R_), ("DAY", W), ("THREE...", W), ("SEVEN.", R_)], 4.0),
    ([("DAY", W), ("FOUR.", W), ("MASON'S", R_), ("PENALTY.", W)], 2.3),
    ([("SAVED!", G)], 1.5),
    ([("THAT", W), ("NIGHT,", W), ("GRANDAD", B), ("CALLS.", W)], 2.1),
    ([("HE'S", W), ("HOME.", G), ("THINNER.", W), ("A", W), ("TUBE", W), ("UNDER", W), ("HIS", W), ("NOSE.", W)], 3.5),
    ([("\"THE", W), ("DERBY'S", Y), ("SATURDAY?", Y), ("I'LL", W), ("BE", W), ("THERE.", W), ("SEAT", B), ("FOURTEEN.\"", B)], 3.7),
    ([("FRIDAY.", W), ("OKAFOR", Y), ("LANDS", W), ("WRONG.", R_), ("HE", W), ("DOESN'T", W), ("GET", W), ("UP.", R_)], 3.6),
    ([("THE", W), ("COACH", W), ("CROSSES", R_), ("OUT", R_), ("HIS", W), ("NAME.", W), ("DIXON...", B), ("OR", W), ("YOU.", G)], 4.1),
    ([("THEN", W), ("MASON", R_), ("WALKS", W), ("TO", W), ("THE", W), ("COACH.", W), ("AND", W), ("WHISPERS.", R_)], 3.5),
    ([("THE", W), ("COACH", W), ("LOOKS", W), ("AT", W), ("YOU.", G), ("WRITES", W), ("NOTHING.", Y)], 3.1),
    ([("ASK", O), ("FOR", W), ("THE", W), ("SHIRT?", Y), ("OR", W), ("WAIT?", B)], 2.3),
    ([("VOTE", W), ("BELOW.", G), ("FOLLOW" if PLATFORM != "youtube" else "SUBSCRIBE", R_), ("FOR", W), ("EP.\u00a06.", Y)], 2.6),
]
GAP = 0.0
import json as _json
VOICE = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vo/lines.json")))
if PLATFORM == "youtube":   # "Subscribe for episode six" take is a little longer
    VOICE[-1] = (VOICE[-1][0], VOICE[-1][0] + 2.96)
STARTS = [max(0.0, a - 0.12) for a, _ in VOICE]
STARTS[0] = 0.0
for i in range(len(LINES)):
    nxt = STARTS[i + 1] if i + 1 < len(LINES) else VOICE[-1][1] + 0.45
    LINES[i] = (LINES[i][0], nxt - STARTS[i])
TOTAL = VOICE[-1][1] + 0.45


def word_times(i):
    words, dur = LINES[i]
    st, en = VOICE[i]
    talk = en - st
    lens = [len(w) + 2 for w, _ in words]
    tot = sum(lens)
    acc = 0
    out = []
    for (w, c), L in zip(words, lens):
        out.append((w, st + talk * acc / tot - 0.03, c))
        acc += L
    return out


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s - 0.12:
            i = k
    return i


def chunks(ws):
    """split a line into caption chunks of 1-3 words, breaking after punctuation"""
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if w[0][-1] in ".,?!\"" or w[0].endswith("...") or len(cur) == 3:
            out.append(cur)
            cur = []
    if cur:
        if out and len(cur) == 1 and len(out[-1]) < 3 and out[-1][-1][0][-1] not in ".?!":
            out[-1] += cur
        else:
            out.append(cur)
    return out


def overlay(img, t):
    banner(img, EP)
    i = line_at(t)
    ws = word_times(i)
    ch = chunks(ws)
    cur = ch[0]
    for c in ch:
        if t >= c[0][1] - 0.04:
            cur = c
    if i == 0 and t < 0.4:  # frame 0 = TikTok preview: first chunk fully lit
        cur = [(w, -1, c) for w, _, c in cur]
    caption(img, cur, t, size=56, wrap=620)


def draw_ball_s(img, x, y, size=6):
    draw_ball(img, x, y, size)


# ------------------------------------------------------------------ sets
def pitch_set(key="pitch", rainy=True):
    if key not in BG:
        img = sky_trees(top=(132, 160, 196), bot=(190, 206, 222), key="overcast").convert("RGBA")
        crowd_band(img, 430, 520, seed=4)
        adboards(img, 520, 30)
        pitch(img, 550)
        BG[key] = img
    return BG[key].copy()


BG = {}


def room_set(key, wall=(236, 238, 244), floor=((222, 226, 234), (204, 210, 222)), night=False):
    if key in BG:
        return BG[key].copy()
    img = Image.new("RGBA", (FW, FH), wall + (255,))
    d = ImageDraw.Draw(img)
    for y in range(0, 760, 40):  # wall panels
        d.line([(0, y), (FW, y)], fill=shade(wall, 0.96), width=2)
    # checker floor in light perspective
    for r in range(14):
        y0 = 760 + (r ** 1.35) * 14
        y1 = 760 + ((r + 1) ** 1.35) * 14
        n = 12
        for c in range(n):
            x0 = -100 + c * (FW + 200) / n
            col = floor[(r + c) % 2]
            d.rectangle([x0, y0, x0 + (FW + 200) / n, y1], fill=col)
    d.rectangle([0, 752, FW, 762], fill=shade(wall, 0.8))
    if night:
        img = Image.blend(img, Image.new("RGBA", img.size, (30, 36, 70, 255)), 0.45)
    BG[key] = img
    return img.copy()


def window(img, x, y, w, h, night=False, t=0):
    d = ImageDraw.Draw(img)
    d.rectangle([x - 6, y - 6, x + w + 6, y + h + 6], fill=OL)
    top, bot = ((20, 26, 60), (60, 60, 110)) if night else ((130, 160, 200), (180, 200, 220))
    for yy in range(h):
        d.line([(x, y + yy), (x + w, y + yy)], fill=tuple(int(lerp(a, b, yy / h)) for a, b in zip(top, bot)))
    d.rectangle([x + w / 2 - 3, y, x + w / 2 + 3, y + h], fill=(240, 240, 245))
    rng = random.Random(2)
    for _ in range(26):  # rain on the glass
        rx, ry = rng.uniform(x, x + w), rng.uniform(y, y + h)
        yy = y + (ry - y + t * 160) % h
        d.line([(rx, yy), (rx - 2, yy + 14)], fill=(210, 224, 255), width=2)


# ------------------------------------------------------------------ scenes (u = 0..1 inside the line)
def s01(t, u, T):
    """hook: keeper flying flat, arms out — the ball squirms between the oversized gloves"""
    img = pitch_set()
    goal(img, 360, 900, 600, 300)
    speed_lines(img, t, 330, 690, n=12, a=70, r0=330, r1=700)   # behind the action
    # keeper: arms-up sprite turned exactly 90 degrees -> clean horizontal dive to the right
    kx = lerp(320, 380, ease_out(u * 1.3))
    ky = 740 - math.sin(clamp(u * 1.2) * math.pi) * 25
    sp = big(hero(pose="reach", gloves=True, mouth="open"), 8).rotate(-90, expand=True, resample=Image.NEAREST)
    shadow(img, kx, 900, 300, 34, 70)
    img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
    gx = kx + sp.width / 2 - 47           # gloves (front end of the body)
    # ball: arrives at the gloves at frame 0, slips through and on into the net
    bu = ease_in_out(clamp(u / 0.55))
    bx = min(640, gx + 25 + 60 * bu)
    by = ky + 4 + 100 * bu
    if u < 0.12:
        glow_ring(img, gx + 25, ky + 4, 70, 0.5, (255, 250, 210))
    draw_ball_s(img, bx, by + 35, 5)
    impact_lines(img, gx + 25, ky + 15, T - 0.05, t, 12)
    if u > 0.5:
        impact_lines(img, bx, by, T + 0.5 * LINES[0][1], t, 10)
    pill(img, 360, 1180, "YOU CHOSE: ACADEMY", (40, 150, 80), 1.0, 30)
    rain(img, t, a=55, n=90)
    img = cam(img, 1.06 - 0.05 * u, 380, 760, *shake(t, T + 0.5 * LINES[0][1], 0.3, 10))
    return img


def s02(t, u, T):
    img = pitch_set()
    img = img.filter(ImageFilter.GaussianBlur(3))
    paste(img, mason(mouth="grin" if u > 0.2 else "smile", look=-1), 26, 400, 1500)
    bubble(img, 250, 520, "ZERO.\nLIKE YOUR SHIRT.", spring(t - T - 0.1, 13, 7), 34)
    pill(img, 560, 1180, "MASON · #9", (210, 52, 56), spring(t - T - 0.9, 13, 7), 30)
    rain(img, t)
    return cam(img, 1 + 0.06 * u, 360, 800)


def s03(t, u, T):
    """Riverside Academy: Mason at home, crest + banner"""
    img = sky_trees(top=(132, 160, 196), bot=(190, 206, 222), key="overcast").convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 700, FW, FH], fill=(150, 156, 170))
    d.rectangle([60, 360, 660, 760], fill=(232, 234, 240), outline=OL, width=6)
    d.rectangle([60, 330, 660, 380], fill=(30, 40, 80), outline=OL, width=6)
    d.text((360, 356), "RIVERSIDE ACADEMY", font=font(800, 34), fill=(250, 206, 40), anchor="mm")
    for r in range(2):
        for c in range(5):
            d.rectangle([100 + c * 110, 420 + r * 120, 170 + c * 110, 490 + r * 120], fill=(130, 170, 220), outline=OL, width=4)
    d.rectangle([320, 640, 400, 760], fill=(40, 50, 90), outline=OL, width=5)
    for x in (110, 610):  # flags
        d.rectangle([x, 220, x + 6, 360], fill=(80, 80, 90))
        w = math.sin(t * 6 + x) * 8
        d.polygon([(x + 6, 224), (x + 70, 236 + w), (x + 6, 262)], fill=(210, 52, 56), outline=OL)
    paste(img, mason(mouth="smile"), 11, 360 + lerp(-60, 0, ease_out(u * 2)), 1170)
    pill(img, 360, 1210, "HIS CLUB", (210, 52, 56), spring(t - T - 0.5, 13, 7), 30)
    rain(img, t)
    return cam(img, 1.0 + 0.05 * u, 360, 800)


def dorm(t, night=False):
    img = room_set("dorm_n" if night else "dorm", wall=(220, 226, 240), night=night)
    window(img, 420, 230, 220, 260, night=night, t=t)
    d = ImageDraw.Draw(img)
    # bunk bed (left)
    d.rectangle([40, 360, 64, 1000], fill=(120, 80, 50), outline=OL, width=4)
    d.rectangle([330, 360, 354, 1000], fill=(120, 80, 50), outline=OL, width=4)
    for y in (520, 860):
        d.rectangle([40, y, 354, y + 40], fill=(120, 80, 50), outline=OL, width=4)
        d.rectangle([64, y - 34, 330, y], fill=(240, 240, 248), outline=OL, width=4)
        d.rectangle([64, y - 34, 130, y - 10], fill=(255, 255, 255), outline=OL, width=3)
    # poster
    d.rectangle([440, 560, 560, 700], fill=(250, 206, 40), outline=OL, width=5)
    d.text((500, 630), "SAVE", font=font(800, 26), fill=OL, anchor="mm")
    return img


def in_bed(img, sprite, x0, top, scale, blanket):
    """character lying in a bunk: head on the pillow (left), blanket over the body"""
    sp = big(sprite, scale).rotate(90, expand=True, resample=Image.NEAREST)
    img.alpha_composite(sp, (int(x0), int(top - sp.height + 26)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0 + 92, top - 98, 336, top + 6], 18, fill=blanket, outline=OL, width=5)
    d.line([(x0 + 112, top - 50), (330, top - 50)], fill=shade(blanket, 0.8), width=4)


def s04(t, u, T):
    img = dorm(t)
    d = ImageDraw.Draw(img)
    on = int(t * 4) % 2 == 0
    d.rounded_rectangle([470, 760, 650, 840], 12, fill=(20, 20, 30), outline=OL, width=5)
    d.text((560, 800), "06:00", font=font(800, 48), fill=(255, 70, 70) if on else (120, 40, 40), anchor="mm")
    # Dixon asleep in the top bunk, you wake up in the bottom bunk
    in_bed(img, dixon(blink=True, gloves=False), 58, 486, 5, (60, 110, 200))
    in_bed(img, hero(blink=u < 0.45, mouth="flat", bracelet=False), 58, 826, 5, (40, 150, 80))
    if u < 0.5:
        pill(img, 360, 1150, "MONDAY", (40, 90, 200), spring(t - T, 13, 7), 32)
        pill(img, 360, 1215, "2 HRS FROM HOME", (60, 60, 80), spring(t - T - 0.4, 13, 7), 26)
    return cam(img, 1 + 0.05 * u, 360, 700) if u < 0.5 else cam(img, 1.6 + 0.08 * u, 0, 1280, *shake(t, T + 0.5 * LINES[3][1], .25, 8))


def s05(t, u, T):
    img = dorm(t)
    d = ImageDraw.Draw(img)
    # bottom bunk now empty (you got up), blanket thrown back
    d.rounded_rectangle([230, 728, 336, 832], 18, fill=(40, 150, 80), outline=OL, width=5)
    d.line([(244, 776), (330, 776)], fill=shade((40, 150, 80), 0.8), width=4)
    # you stand on the floor and say hi; Dixon stays lying in the top bunk and turns to the wall
    paste(img, hero(mouth="smile", bracelet=True, look=-1), 9, 580, 1080)
    turned = u > 0.35
    in_bed(img, dixon(view="back" if turned else "front", look=1, gloves=False), 58, 486, 5, (60, 110, 200))
    bubble(img, 600, 785, "HI!", spring(t - T - 0.1, 13, 7), 36)
    if u > 0.62:
        pill(img, 200, 600, "DIXON · KEEPER #2", (40, 90, 200), spring(t - T - 0.62 * LINES[4][1], 13, 7), 26)
    return cam(img, 1.03 + 0.05 * u, 360, 760) if u < 0.35 else cam(img, 1.6 + 0.08 * u, 0, 450)


def keepers_line(img, t, sel=None, hero_scale=8):
    xs = [(170, okafor(look=1), 10), (370, dixon(), 9), (560, hero(gloves=True, pose="stand"), hero_scale)]
    for x, sp, s in xs:
        shadow(img, x, 1060, 120)
        paste(img, sp, s, x, 1060)


def s06(t, u, T):
    img = pitch_set()
    goal(img, 360, 650, 520, 230)
    keepers_line(img, t)
    # the yellow #1 shirt floating above, glowing
    k = clamp(spring(t - T - 0.9, 12, 6), 0, 1.15)
    if k > 0.05:
        glow_ring(img, 360, 470, 120 * k, 0.6, (255, 230, 120))
        d = ImageDraw.Draw(img)
        s_ = 10 * k
        cx, cy = 360, 470 + math.sin(t * 3) * 6
        d.arc([cx - 2 * s_, cy - 9 * s_, cx + 2 * s_, cy - 5 * s_], 180, 360, fill=(200, 200, 210), width=max(2, int(s_ * .6)))
        d.line([(cx - 9 * s_, cy - 2 * s_), (cx, cy - 5 * s_), (cx + 9 * s_, cy - 2 * s_)], fill=(200, 200, 210), width=max(2, int(s_ * .6)))
        body = [(cx - 6 * s_, cy - 3 * s_), (cx - 11 * s_, cy), (cx - 9 * s_, cy + 3 * s_), (cx - 6 * s_, cy + 2 * s_),
                (cx - 6 * s_, cy + 9 * s_), (cx + 6 * s_, cy + 9 * s_), (cx + 6 * s_, cy + 2 * s_), (cx + 9 * s_, cy + 3 * s_),
                (cx + 11 * s_, cy), (cx + 6 * s_, cy - 3 * s_), (cx + 2 * s_, cy - 3 * s_), (cx, cy - 1 * s_), (cx - 2 * s_, cy - 3 * s_)]
        d.polygon(body, fill=(246, 206, 40), outline=OL, width=max(2, int(s_ * .5)))
        d.text((cx, cy + 4 * s_), "1", font=font(800, max(8, int(9 * s_))), fill=OL, anchor="mm")
    pill(img, 360, 1170, "3 KEEPERS · 1 SHIRT", (60, 60, 80), spring(t - T, 13, 7), 30)
    return cam(img, 1 + 0.04 * u, 360, 800)


def s07(t, u, T):
    """Okafor: low angle, huge; hero tiny next to him"""
    img = pitch_set().filter(ImageFilter.GaussianBlur(2))
    G = 1220
    shadow(img, 220, G, 300); shadow(img, 540, G, 260)
    so = paste(img, okafor(mouth="flat", look=1), 14, 220, G)
    sh_ = paste(img, hero(gloves=True, look=-1), 12, 540, G)
    d = ImageDraw.Draw(img)
    top_o = G - so.height + 10 * 14 - 14   # top of the hair rows (sprite has a 10-row margin)
    top_h = G - sh_.height + 10 * 12 - 12
    for y, x0, x1 in ((top_o, 120, 690), (top_h, 380, 690)):
        for x in range(x0, x1, 28):
            d.line([(x, y), (x + 14, y)], fill=(255, 255, 255), width=4)
    k = clamp((u - 0.35) / 0.2)
    if k > 0:
        d.line([(680, top_o), (680, top_o + (top_h - top_o) * k)], fill=C_Y, width=8)
        if k >= 1:
            pill(img, 600, (top_o + top_h) / 2, "+1 HEAD", (200, 160, 20), spring(t - T - 0.55 * LINES[6][1], 13, 7), 26)
    pill(img, 220, top_o - 60, "OKAFOR · 12", (200, 160, 20), spring(t - T - 0.1, 13, 7), 30)
    return cam(img, 1.04 - 0.04 * u, 360, 900)


def s08(t, u, T):
    img = pitch_set()
    GL = 1060
    goal(img, 360, GL, 640, 330)
    # Dixon on his goal line catches cleanly, chest height
    caught = u > 0.4
    shadow(img, 360, GL, 200)
    sp_d = paste(img, dixon(pose="catch" if u > 0.34 else "ready"), 9, 360, GL)
    k = clamp(u / 0.4)
    gy = GL - sp_d.height + (10 + 13) * 9
    bx, by = lerp(800, 366, k), lerp(500, gy + 30, k)
    draw_ball_s(img, bx, by)
    if u > 0.4:
        glow_ring(img, 366, gy - 10, 70, 0.7)
    pill(img, 360, 1230, "DIXON · 0 MISTAKES", (40, 90, 200), spring(t - T - 0.3, 13, 7), 28)
    return cam(img, 1 + 0.05 * u, 360, 900)


def s09(t, u, T):
    img = pitch_set().filter(ImageFilter.GaussianBlur(2.5))
    paste(img, hero(gloves=True, mouth="flat", blink=0.5 < u < 0.58), 24, 360, 1500)
    pill(img, 360, 470, "YOU · 11 · NO. 3", (200, 50, 60), spring(t - T - 0.5, 13, 7), 34)
    rain(img, t)
    return cam(img, 1.08 - 0.05 * u, 360, 800)


def s10(t, u, T):
    """try-fail montage: balls fly past, counters"""
    img = pitch_set()
    GL = 1040
    goal(img, 360, GL, 600, 300)
    ws = word_times(9)
    sw = clamp((ws[6][1] - 0.04 - T) / LINES[9][1] + 0.005)      # caption "DAY THREE" starts here
    if u < sw:
        shot, phase = int(u / (sw / 2)), (u % (sw / 2)) / (sw / 2)
    else:
        v = (u - sw) / (1 - sw)
        shot, phase = (2, v / 0.38) if v < 0.38 else (3, (v - 0.38) / 0.62)
    shot = min(shot, 3)
    side = [-1, 1, 1, -1][shot]
    save = shot == 2                      # Day 3, first shot: you finally stop one
    dive_side = -side if save else side   # wrong way on the goals, right way on the save
    kx = 360 + dive_side * 150 * ease_out(phase)
    bk = clamp(phase / 0.55)
    bx = lerp(360 - side * 40, 360 - side * 230, bk)
    by = lerp(1380, GL - (250 if shot == 3 else 190), bk)
    if save and bk >= 1:
        bx, by = kx - side * 0 + (-side) * (-1) * 0 + (360 - side * 230 - kx) * 0.0 + (kx - 360) * 0.0 + (-(dive_side) * 0) + (kx + dive_side * 150 - kx), GL - 200
    shadow(img, kx, GL, 200)
    if phase > 0.3:
        sp = big(hero(pose="reach", gloves=True, mouth="open"), 8).rotate(-90 if dive_side > 0 else 90, expand=True, resample=Image.NEAREST)
        ky = GL - 170 - math.sin(clamp(phase) * math.pi) * 40
        img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
        if save:
            bx, by = (kx + dive_side * (sp.width / 2 - 40), ky + 30) if bk >= 0.85 else (bx, by)
    else:
        paste(img, hero(pose="ready", gloves=True), 8, kx, GL)
    draw_ball_s(img, bx, by, 6)
    if bk >= 1 and not save:
        impact_lines(img, bx, by - 40, t - (phase - 0.55) * 0.5, t, 10)
    if save and bk >= 0.85:
        glow_ring(img, bx, by - 40, 80, 0.8, (255, 255, 200))
        pill(img, 360, 520, "SAVE!", (40, 150, 80), spring(t - (T + (sw + (1 - sw) * 0.85 * 0.5 * 0.8) * LINES[9][1]), 13, 7), 40)
    day2 = u < sw
    scored = bk >= 1 and not save
    n = [[7, 8], [8, 9], [6, 6], [6, 7]][shot][1 if scored else 0]
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([200, 1100, 520, 1230], 18, fill=(16, 18, 36), outline=C_R, width=5)
    d.text((360, 1135), "DAY 2" if day2 else "DAY 3", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    d.text((360, 1192), f"CONCEDED {n}", font=font(800, 36), fill=C_R, anchor="mm")
    img = flash(img, 0.18 * clamp(1 - abs(phase - 0.9) * 12), (60, 255, 120) if save else (255, 60, 60))
    return cam(img, 1 + 0.03 * u, 360, 900)


PEN = {}


def s11(t, u, T):
    """day four: Mason's penalty — keeper's view, Mason runs up"""
    img = pitch_set()
    paste(img, mason(pose="run" if u > 0.3 else "stand", phase=t * 2.5, mouth="smile"), 9, 360, lerp(760, 820, u))
    draw_ball_s(img, 380, 840)
    paste(img, hero(view="back", pose="ready", gloves=True), 22, 330, 1600)
    pill(img, 600, 560, "DAY 4", (60, 60, 80), spring(t - T, 13, 7), 30)
    d = ImageDraw.Draw(img, "RGBA")
    vig = clamp(u)
    return cam(img, 1 + 0.12 * ease_in_out(u), 360, 820)


def s12(t, u, T):
    img = pitch_set()
    goal(img, 360, 860, 600, 300)
    speed_lines(img, t, 250, 700, n=18, a=90, r0=300, r1=700)
    sp = big(hero(pose="reach", gloves=True, mouth="open"), 8).rotate(90, expand=True, resample=Image.NEAREST)
    kx = lerp(430, 380, ease_out(u * 2))
    ky = 700 - math.sin(clamp(u * 1.5) * math.pi) * 20
    shadow(img, kx, 860, 300, 34, 70)
    img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
    gx = kx - sp.width / 2 + 55
    glow_ring(img, gx - 45, ky, 80 + 30 * u, 0.9, (255, 255, 200))
    draw_ball_s(img, gx - 45, ky + 36, 5)
    pill(img, 360, 1150, "SAVED!", (40, 150, 80), spring(t - T - 0.05, 13, 7), 48)
    paste(img, coach(look=-1), 6, 620, 1250)
    img = flash(img, 0.7 * clamp(1 - u * 5))
    return cam(img, 1.05, 360, 800, *shake(t, T, .3, 12))


def phone_frame(img, cx, cy, w, h):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w / 2 - 14, cy - h / 2 - 14, cx + w / 2 + 14, cy + h / 2 + 14], 40, fill=(24, 26, 36), outline=OL, width=6)
    return (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))


def s13(t, u, T):
    img = dorm(t, night=True)
    k = ease_out(u * 1.5)
    box = phone_frame(img, 360, 800, 360, 620)
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=(26, 34, 70))
    d.text((360, 640), "GRANDAD", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((360, 690), "video call...", font=font(600, 26), fill=(180, 190, 220), anchor="mm")
    paste(img, grandad(mouth="smile"), 6, 360, 900)
    for x, c in ((270, (230, 60, 60)), (450, (60, 200, 90))):
        r = 34 + (6 * math.sin(t * 12) if c[1] > 100 else 0)
        d.ellipse([x - r, 1000 - r, x + r, 1000 + r], fill=c, outline=OL, width=5)
    jx = math.sin(t * 120) * 6 if int(t * 3) % 2 == 0 else 0
    return cam(img, 1, 360 + jx, 800)


def home_call(t, u, mouth="smile", ui=True):
    img = Image.new("RGBA", (FW, FH), (20, 22, 40, 255))
    box = phone_frame(img, 360, 760, 500, 860)
    scr = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (226, 200, 170, 255))
    sd = ImageDraw.Draw(scr)
    W_, H_ = scr.size
    sd.rectangle([0, 0, W_, H_ * 0.55], fill=(214, 190, 160))  # wallpaper
    for x in range(0, W_, 40):
        sd.line([(x, 0), (x, H_ * 0.55)], fill=(200, 176, 146), width=4)
    sd.rectangle([30, 40, 150, 140], fill=(255, 236, 160), outline=OL, width=5)  # lamp-lit frame
    # armchair + Grandad big
    sd.rounded_rectangle([60, H_ * 0.45, W_ - 60, H_], 30, fill=(150, 46, 52), outline=OL, width=6)
    paste(scr, grandad(mouth=mouth, tube=True, blink=(u % 0.5) > 0.46), 16, W_ / 2, H_ + 120)
    paste(scr, cane(), 9, 60, H_ - 10)
    # thin nasal cannula: under the nostrils, round both cheeks, over the ears
    top = H_ + 120 - 39 * 16
    ny = top + 14 * 16 + 10
    ey = top + 12 * 16
    cx = W_ / 2
    # oxygen bottle beside the chair, tube runs up to his ears and under the nose
    sd.rounded_rectangle([8, H_ - 330, 58, H_ - 160], 16, fill=(60, 170, 90), outline=OL, width=5)
    sd.rectangle([22, H_ - 350, 44, H_ - 330], fill=(200, 200, 210), outline=OL, width=4)
    sd.text((33, H_ - 245), "O2", font=font(800, 20), fill=(255, 255, 255), anchor="mm")
    for sgn in (-1, 1):
        pts = [(cx + sgn * 4, ny + 4), (cx + sgn * 30, ny + 10), (cx + sgn * 70, ny), (cx + sgn * 90, ey)]
        sd.line(pts, fill=(150, 215, 250), width=4)
    sd.line([(cx - 90, ey), (cx - 110, ey + 80), (33, H_ - 350)], fill=(150, 215, 250), width=4)
    img.alpha_composite(scr, (box[0], box[1]))
    d = ImageDraw.Draw(img)
    if not ui:
        return img
    d.rounded_rectangle([box[0] + 20, box[1] + 20, box[0] + 280, box[1] + 64], 12, fill=(16, 18, 36))
    d.text((box[0] + 150, box[1] + 42), "HOME · OUT OF HOSPITAL", font=font(800, 18), fill=C_G, anchor="mm")
    # small self view (hero)
    d.rounded_rectangle([box[2] - 130, box[3] - 190, box[2] - 20, box[3] - 20], 14, fill=(40, 50, 80), outline=(255, 255, 255), width=3)
    paste(img, hero(mouth="smile"), 4, box[2] - 75, box[3] - 24)
    return img


def s14(t, u, T):
    img = home_call(t, u, "smile")
    if u > 0.65:
        k = spring(t - T - 0.65 * LINES[13][1], 13, 7)
        d = ImageDraw.Draw(img)
        if k > 0.5:
            d.line([(250, 1010), (352, 925)], fill=(255, 255, 255), width=5)
        pill(img, 200, 1040, "OXYGEN", (40, 90, 200), k, 26)
    return cam(img, 1 + 0.06 * u, 360, 700)


def s15(t, u, T):
    img = home_call(t, u, "open" if int(t * 7) % 2 else "smile", ui=u < 0.45)
    bubble(img, 380, 768, "I'LL BE THERE.\nSEAT 14.", spring(t - T - 0.8, 13, 7), 32)
    if u > 0.6:  # ticket
        k = spring(t - T - 0.6 * LINES[14][1], 13, 7)
        d = ImageDraw.Draw(img)
        x0, y0 = 420, 1080
        d.rounded_rectangle([x0, y0, x0 + 250 * k, y0 + 110 * k], 14, fill=(250, 240, 210), outline=OL, width=5)
        if k > 0.5:
            d.text((x0 + 125, y0 + 34), "DERBY · SAT", font=font(800, 24), fill=OL, anchor="mm")
            d.text((x0 + 125, y0 + 76), "SEAT 14", font=font(800, 34), fill=(210, 52, 56), anchor="mm")
    return cam(img, 1.06 + 0.04 * u, 360, 700) if u < 0.45 else cam(img, 1.55 + 0.06 * u, 330, 760)


def s16(t, u, T):
    """Friday: Okafor jumps for a cross and lands wrong"""
    img = pitch_set()
    G = 1060
    goal(img, 360, G, 600, 300)
    pill(img, 130, 470, "FRIDAY", (60, 60, 80), spring(t - T, 13, 7), 30)
    if u < 0.3:
        k = u / 0.3
        y = G - math.sin(k * math.pi) * 150
        shadow(img, 360, G, 180 * (1 - 0.4 * math.sin(k * math.pi)))
        paste(img, okafor(pose="celebrate"), 8, 360, y)
        draw_ball_s(img, lerp(780, 380, k), lerp(560, y - 300, k), 5)
    elif u < 0.38:  # bad landing: knee buckles
        shadow(img, 360, G, 180)
        paste(img, okafor(pose="stand", mouth="open"), 8, 380, G, rot=-18)
        draw_ball_s(img, 450, G - 10, 5)
    else:
        rock = math.sin(t * 7) * 4
        shadow(img, 360, G, 220)
        paste(img, okafor(pose="hurt", blink=int(t * 3) % 3 == 0, mouth="open"), 8, 340, G + 40 + rock * 0.4, rot=-90)
        bk = clamp((u - 0.38) / 0.5)
        draw_ball_s(img, lerp(450, 620, ease_out(bk)), G - 10, 5)
        if int(t * 6) % 2:
            glow_ring(img, 246, G - 42, 24, 0.8, (255, 60, 60))
        if u < 0.55:
            impact_lines(img, 360, G - 100, T + 0.3 * LINES[15][1], t, 12)
        pill(img, 360, 1210, "INJURED", (200, 40, 50), spring(t - T - 0.45 * LINES[15][1], 13, 7), 30)
    img = flash(img, 0.45 * clamp(1 - abs(u - 0.32) * 10), (255, 40, 40))
    return cam(img, 1.0 + 0.08 * u, 360, 950, *shake(t, T + 0.3 * LINES[15][1], .35, 14))


def team_sheet(img, u, cross_k, gk="?"):
    d = ImageDraw.Draw(img)
    d.rectangle([90, 380, 630, 1180], fill=(250, 246, 236), outline=OL, width=6)
    d.ellipse([350, 390, 370, 410], fill=(220, 40, 40), outline=OL, width=3)
    d.text((360, 450), "DERBY · TEAM SHEET", font=font(800, 34), fill=OL, anchor="mm")
    rows = [("GK", "OKAFOR"), ("DF", "WALSH"), ("DF", "PATEL"), ("MF", "HUGHES"), ("FW", "MASON (C)")]
    for i, (p, n) in enumerate(rows):
        y = 540 + i * 100
        d.text((140, y), p, font=font(800, 34), fill=(120, 120, 140), anchor="lm")
        d.text((240, y), n, font=font(800, 40), fill=OL, anchor="lm")
    if cross_k > 0:
        d.line([(230, 540), (230 + 230 * cross_k, 540)], fill=(220, 40, 40), width=10)


def s17(t, u, T):
    img = room_set("office", wall=(206, 182, 150), floor=((180, 156, 124), (168, 144, 112)))
    team_sheet(img, u, ease_out((u - 0.1) / 0.3))
    if u > 0.55:  # Dixon OR you cards
        k = spring(t - T - 0.55 * LINES[16][1], 13, 7)
        ov = Image.new("RGBA", img.size, (10, 12, 30, int(150 * clamp(k))))
        img.alpha_composite(ov)
        if k > 0.2:
            ImageDraw.Draw(img).rounded_rectangle([70, 490, 650, 900], 26, fill=(14, 16, 36), outline=(255, 255, 255), width=4)
        for x, sp, lab, c in ((220, dixon(), "DIXON", C_B), (500, hero(gloves=True), "YOU", C_G)):
            d = ImageDraw.Draw(img)
            w, h = 220 * k, 300 * k
            if k > 0.1:
                d.rounded_rectangle([x - w / 2, 720 - h / 2, x + w / 2, 720 + h / 2], 20, fill=(16, 18, 36), outline=c, width=6)
                if k > 0.6:
                    paste(img, sp, 6, x, 790)
                    d.text((x, 830), lab, font=font(800, 34), fill=c, anchor="mm")
        if k > 0.6:
            ImageDraw.Draw(img).text((360, 720), "OR", font=font(800, 40), fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=OL)
    # coach's arm + pen on the cross-out
    if u < 0.5:
        d = ImageDraw.Draw(img)
        px = 230 + 230 * ease_out((u - 0.1) / 0.3)
        d.line([(px + 20, 560), (FW + 40, 760)], fill=(30, 40, 80), width=60)
        d.ellipse([px - 6, 530, px + 40, 580], fill=SKIN["light"][0], outline=OL, width=5)
    return cam(img, 1 + 0.05 * u, 360, 760)


def s18(t, u, T):
    img = pitch_set()
    shadow(img, 630, 860, 90)
    paste(img, hero(gloves=True, look=-1), 5, 630, 860)  # you, far away on the right, watching
    pill(img, 630, 680, "YOU", (40, 150, 80), 1, 22)
    x = lerp(-160, 300, clamp(u / 0.58))
    shadow(img, 480, 1130, 260)
    paste(img, coach(look=-1), 12, 480, 1130)
    walking = u < 0.58
    shadow(img, x, 1130, 260)
    paste(img, mason(pose="run" if walking else "whisper", phase=t * 1.6, mouth="smile", look=1), 12, x,
          1130 - (abs(math.sin(t * 1.6 * math.pi)) * 8 if walking else 0))
    if u > 0.62:
        bubble(img, 390, 520, "psst...", spring(t - T - 0.62 * LINES[17][1], 13, 7), 32)
    return cam(img, 1.02 + 0.06 * u, 400, 950)


def s19(t, u, T):
    img = pitch_set().filter(ImageFilter.GaussianBlur(2))
    paste(img, coach(look=-1, mouth="flat", blink=0.55 < u < 0.62), 24, 400, 1500)
    d = ImageDraw.Draw(img)
    # empty clipboard
    d.rounded_rectangle([60, 860, 300, 1200], 14, fill=(250, 246, 236), outline=OL, width=6)
    d.rectangle([130, 845, 230, 880], fill=(120, 120, 130), outline=OL, width=4)
    d.text((180, 950), "GK:", font=font(800, 40), fill=OL, anchor="mm")
    d.text((180, 1030), "?", font=font(800, 80), fill=(220, 40, 40), anchor="mm")
    return cam(img, 1 + 0.06 * u, 360, 800)


def choice_cards(img, t, T0, sel=None):
    d = ImageDraw.Draw(img)
    cards = [(190, "ASK", "KNOCK ON HIS DOOR", C_O), (530, "WAIT", "WAIT YOUR TURN", C_B)]
    for i, (x, lab, sub, c) in enumerate(cards):
        k = spring(t - T0 - i * 0.15, 13, 7)
        if k < 0.05:
            continue
        hl = 0.5 + 0.5 * math.sin(t * 3.2 + i * math.pi)
        w, h = 300 * k * (1 + 0.04 * hl), 420 * k * (1 + 0.04 * hl)
        y = 760 - 10 * hl
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 24, fill=(16, 18, 36), outline=c, width=7)
        if k > 0.6:
            if lab == "ASK":
                d.rectangle([x - 70, y - 160, x + 30, y + 20], fill=(150, 100, 60), outline=OL, width=5)  # door
                d.ellipse([x + 10, y - 70, x + 22, y - 58], fill=C_Y)
                paste(img, hero(look=-1), 5, x + 70, y + 40)
            else:
                for bx_ in (x - 96, x + 84):
                    d.rectangle([bx_, y - 2, bx_ + 12, y + 44], fill=(110, 70, 40), outline=OL, width=4)   # bench legs
                d.rectangle([x - 110, y - 16, x + 110, y - 2], fill=(150, 100, 60), outline=OL, width=5)  # seat
                d.rectangle([x - 110, y + 44, x + 110, y + 48], fill=(60, 66, 110))  # floor line
                paste(img, hero(pose="sit", gloves=True), 5, x, y + 44)
            d.text((x, y + 110), lab, font=font(800, 50), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            d.text((x, y + 165), sub, font=font(700, 20), fill=(220, 224, 240), anchor="mm")


def choice_bg():
    img = Image.new("RGBA", (FW, FH), (20, 26, 70, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, FH, 60):
        for x in range(0, FW, 60):
            if (x // 60 + y // 60) % 2:
                d.rectangle([x, y, x + 60, y + 60], fill=(24, 32, 82))
    return img


def s20(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 0.35)
    return cam(img, 1.0 + 0.03 * u, 360, 760)


def typing_box(img, t, T0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 452, 630, 522], 18, fill=(16, 18, 36), outline=(255, 255, 255), width=3)
    words = ["ASK", "WAIT"]
    k = (t - T0) / 1.2
    w = words[min(1, int(k))]
    n = int(len(w) * clamp((k - min(1, int(k))) * 2)) if k < 2 else len(w)
    d.text((120, 487), w[:n] + ("|" if int(t * 4) % 2 else ""), font=font(800, 30), fill=(255, 255, 255), anchor="lm")


def s21(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 10)
    typing_box(img, t, T)
    pill(img, 360, 1120, "VOTE BEFORE SATURDAY", (200, 50, 60), spring(t - T - 0.3, 13, 7), 26)
    return img


def s22(t, u, T):
    img = choice_bg()
    choice_cards(img, t, T - 10)
    img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (10, 12, 30)), 0.5 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 560], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 150), "EP. 6", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
    tap = T + 0.8
    after = t > tap
    label = ("SUBSCRIBED" if after else "SUBSCRIBE") if PLATFORM == "youtube" else ("FOLLOWING" if after else "+ FOLLOW")
    pul = 1 + (0.05 * math.sin(t * 9) if not after else 0)
    bw, bh = 330 * pul, 96 * pul
    bx, by = 440, py + 280
    d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], 22,
                        fill=(60, 64, 90) if after else (234, 46, 72), outline=OL, width=5)
    d.text((bx, by), label, font=font(800, 36 if after else 40), fill=(255, 255, 255), anchor="mm")
    if after and t < tap + 0.5:
        glow_ring(img, bx, by, 60 + 300 * (t - tap), 0.8 * (1 - (t - tap) / 0.5), C_Y)
    if t < tap + 0.4:  # Grandad's orange glove taps it
        gx = lerp(760, bx + 100, ease_in_out((t - T) / 0.8))
        gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, c in ((230, "ASK", C_O), (490, "WAIT", C_B)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 100, py + 400 - hop, x + 100, py + 470 - hop], 18, fill=(30, 36, 76), outline=c, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 36), fill=c, anchor="mm")
    d.text((360, py + 520), "VOTE IN THE COMMENTS", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    return img


SCENES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s22]


def frame(t):
    i = line_at(t) if t >= STARTS[0] else 0
    T = STARTS[i]
    dur = LINES[i][1]
    u = clamp((t - T) / dur)
    img = SCENES[i](t, u, T)
    img = img.convert("RGBA")
    # cut flash (first 2 frames of every scene except the hook)
    if i > 0 and t - (T - 0.12) < 0.07:
        img = flash(img, 0.35)
    overlay(img, t)
    return img.convert("RGB")


if __name__ == "__main__":
    ts = [float(x) for x in sys.argv[1].split(",")]
    ims = [frame(t).resize((240, 427)) for t in ts]
    out = Image.new("RGB", (240 * min(6, len(ims)), 427 * ((len(ims) + 5) // 6)))
    for k, im in enumerate(ims):
        out.paste(im, (240 * (k % 6), 427 * (k // 6)))
    out.save(sys.argv[2])
    print("TOTAL", TOTAL)
