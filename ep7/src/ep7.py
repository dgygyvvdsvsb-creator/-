"""EP7 — the last penalty (TikTok voted RIGHT), the coach sees the gloves, a 10-second 1984 flash, a call to Grandad.
TikTok layout from EP7 on: banner + captions below TikTok's top UI."""
import os, sys, json
import fb84 as fb
from fb84 import *
from persp import _c
from PIL import ImageEnhance

PLATFORM = os.environ.get("PLATFORM", "tiktok")
VOTE = os.environ.get("VOTE", "RIGHT")          # majority vote from EP6 (the shot goes to the hero's LEFT)
EP = 7
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
FOLLOW = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"
TT = PLATFORM == "tiktok"
BANNER_Y, CAP_Y, UY = (200, 236, 150) if TT else (62, 108, 0)
RIGHT = VOTE == "RIGHT"
LINES = [
    [("LAST", R_), ("KICK.", R_), ("SATURDAY'S", Y), ("SHIRT.", Y)],
    [("MOST", W), ("OF", W), ("YOU", W), ("SAID:", W), ("RIGHT." if RIGHT else "LEFT.", B if RIGHT else Y)],
    ([("YOU", W), ("GO", W), ("RIGHT.", B), ("HE", W), ("GOES", W), ("LEFT.", Y)] if RIGHT else
     [("YOU", W), ("GO", W), ("LEFT.", Y), ("SO", W), ("DOES", W), ("HE.", Y)]),
    ([("GOAL.", R_), ("THE", W), ("RESERVES", B), ("WIN.", W)] if RIGHT else [("SAVED!", G), ("FIRST", W), ("TEAM", W), ("WIN!", G)]),
    ([("SATURDAY'S", W), ("SHIRT:", W), ("DIXON.", B), ("NOT", R_), ("YOU.", R_)] if RIGHT else
     [("SATURDAY'S", W), ("SHIRT:", W), ("YOURS.", G)]),
    [("MASON", R_), ("LAUGHS.", W), ("\"TOLD", W), ("YOU.\"", R_)] if RIGHT else [("EVEN", W), ("MASON", R_), ("CLAPS.", W)],
    [("BUT", W), ("THE", W), ("COACH", W), ("ISN'T", R_), ("LOOKING", W), ("AT", W), ("DIXON.", B)] if RIGHT else
    [("BUT", W), ("THE", W), ("COACH", W), ("ISN'T", R_), ("SMILING.", W)],
    [("HE", W), ("STARES", W), ("AT", W), ("YOUR", W), ("GLOVES.", O), ("RED", R_), ("STRING.", R_)],
    [("AND", W), ("GOES", W), ("PALE.", B)],
    [("1984.", Y), ("TEN", W), ("THOUSAND", W), ("IN", W), ("THE", W), ("RAIN.", B)],
    [("IN", W), ("GOAL:", W), ("GRANDAD.", G), ("SAME", W), ("GLOVES.", O)],
    [("THE", W), ("BALL", W), ("HANGS", Y), ("IN", W), ("THE", W), ("LIGHTS.", Y)],
    [("NUMBER", W), ("NINE", B), ("JUMPS...", W)],
    [("KNEE", R_), ("FIRST.", R_)],
    [("A", W), ("STRETCHER.", W), ("SILENCE.", B)],
    [("GRANDAD", G), ("NEVER", R_), ("PLAYED", W), ("AGAIN.", R_)],
    [("TODAY.", W), ("HIS", W), ("WHISTLE", Y), ("FALLS.", R_)],
    [("HE", W), ("WALKS", W), ("AWAY.", W), ("NOT", R_), ("A", W), ("WORD.", R_)],
    [("THAT", W), ("NIGHT,", W), ("YOU", W), ("CALL", W), ("GRANDAD.", G)],
    [("\"WHO", W), ("IS", W), ("MY", W), ("COACH?\"", Y)],
    [("SILENCE.", B), ("THEN", W), ("HE", W), ("HANGS", R_), ("UP.", R_)],
    [("ONE", W), ("MESSAGE:", W), ("\"STAY", R_), ("AWAY", R_), ("FROM", W), ("HIM.\"", R_)],
    [("ASK", W), ("THE", W), ("COACH...", Y), ("OR", W), ("STAY", R_), ("AWAY?", R_)],
    [("VOTE", W), ("BELOW.", G), (FOLLOW, R_), ("FOR", W), ("PART 8.", Y)],
]
FLASH = {9, 10, 11, 12, 13, 14, 15}                      # the 1984 tape
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"vo/lines_{PLATFORM}.json")
if os.path.exists(_vf):
    VOICE = [tuple(x) for x in json.load(open(_vf))]
else:
    VOICE, t0 = [], 0.05
    for i, ws in enumerate(LINES):
        d_ = max(1.3, 0.34 * len(ws) + 0.3)
        if i in (12, 13, 14):
            d_ = 1.35
        VOICE.append((t0, t0 + d_)); t0 += d_ + 0.42
STARTS = [max(0.0, a - 0.12) for a, _ in VOICE]
STARTS[0] = 0.0
TOTAL = VOICE[-1][1] + 1.6


def D(i):
    return (STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i]


fb.D = D            # the reused 1984 scenes take their spring timings from this episode's clock
fb.STARTS = STARTS
fb.UYF = UY


def word_times(i):
    ws = LINES[i]
    st, en = VOICE[i]
    lens = [len(w) + 2 for w, _ in ws]
    tot, acc, out = sum(lens), 0, []
    for (w, c), L in zip(ws, lens):
        out.append((w, st + (en - st) * acc / tot - 0.03, c))
        acc += L
    return out


def overlay(img, t, i):
    banner(img, EP, BANNER_Y)
    if i == 0:                                   # frame 0 = TikTok preview: the whole hook line, bigger, fully lit
        ws = word_times(0)
        caption(img, [(w, -1 if t < 0.4 else s, c) for w, s, c in ws], t, size=62, wrap=700, y=CAP_Y)
        return
    ch = fb.chunks(word_times(i))
    cur = ch[0]
    for c in ch:
        if t >= c[0][1] - 0.04:
            cur = c
    caption(img, cur, t, size=56, wrap=620, y=CAP_Y)


# ------------------------------------------------------------------ present day: the training-match ground (as EP6)
NF = (80, 150, 230)            # the reserves: sky blue


def res(n, **kw):
    sk = {4: "tan", 5: "dark", 7: "light", 9: "brown", 10: "light"}.get(n, "tan")
    hr = {4: "black", 5: "black", 7: "ginger", 9: "black", 10: "dark"}.get(n, "dark")
    st = {10: "spiky"}.get(n, "short")
    return person(Kit(NF, (250, 250, 250), NF, n), skin=sk, hair=hr, style=st, **kw)


def first(n, **kw):
    sk = {4: "tan", 5: "brown", 7: "dark", 6: "light"}.get(n, "light")
    return person(Kit((210, 52, 56), (245, 245, 250), (210, 52, 56), n), skin=sk, hair={5: "black", 7: "black", 6: "ginger"}.get(n, "dark"),
                  style="short", **kw)


def shoot_bar(img, res_win=False):
    d = ImageDraw.Draw(img)
    y = 248 + UY + (60 if TT else 0)
    d.rounded_rectangle([200, y, 520, y + 50], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.text((360, y + 25), "SHOOTOUT · LAST KICK" if not res_win else "RESERVES WIN 5-4", font=font(800, 24),
           fill=(255, 255, 255) if not res_win else (140, 200, 255), anchor="mm")


def keeper_set(t):
    c = Cam(camX=0.0, camH=1.9, hor=520)
    img = backdrop(520, stadium=True)
    pitch_near(img, c, 0.0)
    return img, c


def taker_and_ball(img, c, t, run=0.0, kick=None):
    """their captain #10 runs up from the edge of the D to the ball on the spot"""
    Z = lerp(10.4, 8.25, ease_in_out(run))
    pose = "run" if run < 1 else "stand"
    ph = t * 2.6
    if kick is not None:
        pose, ph = "kick", kick
    ground_shadow(img, c, 0.35, Z, 0.4)
    sprite_at(img, c, res(10, pose=pose, phase=ph), 0.35, Z, height_m=1.6)


def s_hook(t, u, T):
    img, c = keeper_set(t)
    run = clamp(t / D(0)) * 0.55
    taker_and_ball(img, c, t, run)
    ball_at(img, c, 0.0, 7.6, 0.0)
    for k, X in enumerate((-6, -4.5, 4.6, 6.2)):            # both teams watching from the halfway line
        sprite_at(img, c, (first if k % 2 else res)((4, 5, 7, 9)[k]), X, 24, height_m=1.6)
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430 - abs(math.sin(t * 5)) * 6)
    speed_lines(img, t, 330, 1250, n=10, a=50, r0=300, r1=640)
    shoot_bar(img)
    return cam(img, 1.12 + 0.06 * clamp(t / D(0)), 360, 900)


def arrow_on_grass(img, side, k, col, lab, bg, t, T0):
    d = ImageDraw.Draw(img)
    x0, y0 = 330 + side * 120, 1060
    x1, y1 = 360 + side * 230, 820
    pts = [(lerp(x0, x1, a), lerp(y0, y1, a) - 120 * math.sin(a * math.pi)) for a in np.linspace(0, k, 24)]
    for j in range(0, len(pts) - 1, 2):
        d.line([pts[j], pts[j + 1]], fill=OL, width=18)
        d.line([pts[j], pts[j + 1]], fill=col, width=11)
    if k >= 1:
        pill(img, x1, y1 - 60, lab, bg, spring(t - T0, 13, 7), 40)


def s_vote(t, u, T):
    img, c = keeper_set(t)
    taker_and_ball(img, c, t, 0.55 + 0.25 * u)
    ball_at(img, c, 0.0, 7.6, 0.0)
    side = 1 if RIGHT else -1          # the hero's right = screen right (we see his back)
    arrow_on_grass(img, side, clamp((u - 0.1) / 0.4), C_B if RIGHT else C_Y, "RIGHT" if RIGHT else "LEFT",
                   (40, 110, 200) if RIGHT else (200, 160, 20), t, T + 0.5 * D(1))
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    pill(img, 360, 420 + UY + (60 if TT else 0), "YOU VOTED", (40, 150, 80), spring(t - T - 0.1, 13, 7), 30)
    shoot_bar(img)
    return cam(img, 1.04 + 0.04 * u, 360, 800)


def s_kick(t, u, T):
    """he strikes it to your LEFT. Wrong vote: you dive right, it goes in. Right vote: you dive left and save."""
    img, c = keeper_set(t)
    kick = 0.18
    taker_and_ball(img, c, t, 1.0, kick=clamp((u - kick + 0.1) / 0.16) if u > kick - 0.1 else None)
    a = clamp((u - kick) / 0.32)                                  # ~0.7 s ball flight
    dive = ease_out(clamp((u - kick + 0.04) / 0.3))
    side = 1 if RIGHT else -1
    sp = hero(view="back", pose="reach" if dive > 0.05 else "ready", gloves=True, mouth="open")
    kx = 330 + side * 260 * dive
    ky = 1430 - 230 * math.sin(dive * math.pi * 0.8)
    paste(img, sp, 13, kx, ky, rot=-side * 80 * dive)
    if u < kick:
        ball_at(img, c, 0.0, 7.6, 0.0)
    else:
        sx, sy = c.p(0.0, 7.6)
        ex, ey = 80, 1020
        if not RIGHT:                                             # saved: it hits the gloves at full stretch
            ex, ey = kx - 150, ky - 250
        bx, by = lerp(sx, ex, a), lerp(sy - 12, ey, a) - 60 * math.sin(a * math.pi)
        if a < 1:
            draw_ball(img, bx, by, lerp(1.0, 3.2, a ** 1.5))
        elif not RIGHT:
            b = clamp((u - kick - 0.32) / 0.3)
            draw_ball(img, lerp(ex, -60, b), lerp(ey, ey - 260, b), 3.2)
            glow_ring(img, ex, ey, 80 + 200 * b, 0.8 * (1 - b), (255, 255, 200))
        if a >= 1 and RIGHT:
            img = flash(img, 0.4 * clamp(1 - (u - kick - 0.32) * 8), (255, 50, 50))
    shoot_bar(img)
    return cam(img, 1.04, 360, 800, *shake(t, T + (kick + 0.32) * D(2), .3, 12))


def s_result(t, u, T):
    """reverse angle from behind the penalty spot: the ball in the net (or out), keeper on the grass"""
    c = Cam(camX=0.0, camH=1.7, hor=470)
    img = backdrop(470, stadium=True)
    pitch_persp(img, c, Zgoal=9.0)
    goal3d(img, c, 9.0)
    s = 1.6 * c.k(9.0) / 31
    # from this side the hero's right is screen LEFT
    kx_side = -1.7 if RIGHT else 1.7
    sp = hero(pose="reach", gloves=True, blink=RIGHT, mouth="sad" if RIGHT else "grin").resize((int(24 * s), int(39 * s)), Image.NEAREST)
    sp = sp.rotate(90 if RIGHT else -90, expand=True, resample=Image.NEAREST)
    x, y = c.p(kx_side, 9.0)
    if RIGHT or u < 0.4:
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * s)))
    if RIGHT:
        bx, by = c.p(1.8, 9.9, 0.3)
        draw_ball(img, bx, by + 10, 1.0)
        impact_lines(img, bx, by, T, t, 12)
        for k, (X, Z) in enumerate(((-3.4, 6.2), (3.2, 6.6), (2.0, 5.4))):    # the reserves run off celebrating
            ground_shadow(img, c, X, Z, 0.35)
            sprite_at(img, c, res((10, 5, 7)[k], pose="celebrate", mouth="grin"), X + math.sin(t * 6 + k) * 0.1, Z,
                      Y=abs(math.sin(t * 7 + k)) * 0.25, height_m=1.6)
        img = flash(img, 0.25 * clamp(1 - u * 5), (255, 50, 50))
    else:
        if u >= 0.4:
            ground_shadow(img, c, 1.2, 9.0, 0.45)
            sprite_at(img, c, hero(pose="celebrate", gloves=True, mouth="grin"), 1.2, 9.0,
                      Y=abs(math.sin(t * 7)) * 0.3, height_m=1.6)
        for k, X in enumerate((-2.6, 2.8)):
            sprite_at(img, c, first((4, 6)[k], pose="run", phase=t * 2.4), X, lerp(4.0, 7.5, u), height_m=1.6)
    shoot_bar(img, res_win=RIGHT)
    return cam(img, 1.1 + 0.05 * u, 360, 640)


def s_sheet(t, u, T):
    """the coach's clipboard: GK for Saturday"""
    img, c = fb.present_pitch(t)
    img = img.filter(ImageFilter.GaussianBlur(5))
    paste(img, coach(look=-1, mouth="flat", blink=0.6 < u < 0.63), 22, 300, 1500)
    d = ImageDraw.Draw(img)
    x, y = 420, 900
    d.rounded_rectangle([x, y, x + 260, y + 300], 14, fill=(250, 246, 236), outline=OL, width=6)
    d.rectangle([x + 85, y - 16, x + 175, y + 20], fill=(120, 120, 130), outline=OL, width=4)
    d.text((x + 130, y + 60), "SATURDAY", font=font(800, 28), fill=OL, anchor="mm")
    d.text((x + 70, y + 140), "GK:", font=font(800, 34), fill=OL, anchor="mm")
    k = clamp((u - 0.25) / 0.4)
    name = "DIXON" if RIGHT else "#0"
    d.text((x + 120, y + 140), name[:int(len(name) * k + 0.999)] if k > 0 else "", font=font(800, 34),
           fill=(40, 90, 200) if RIGHT else (40, 150, 80), anchor="lm")
    if k > 0 and k < 1:            # the pen moves along the line
        px = x + 120 + 18 * len(name) * k
        d.line([(px, y + 150), (px + 70, y + 230)], fill=(30, 30, 40), width=10)
    return cam(img, 1.0 + 0.05 * u, 360, 860)


def s_stare(t, u, T):
    """the coach's eyes: fixed on your gloves, not on the celebrations"""
    img, c = fb.present_pitch(t)
    for k, (X, Z) in enumerate(((-2.0, 6.0), (2.4, 6.5))):
        sprite_at(img, c, (res if RIGHT else first)((5, 7)[k], pose="celebrate"), X, Z, Y=abs(math.sin(t * 7 + k)) * 0.2, height_m=1.6)
    sprite_at(img, c, hero(gloves=True, look=1), 0.0, 8.5, height_m=1.6)
    img = img.filter(ImageFilter.GaussianBlur(3))
    paste(img, coach(look=1, mouth="flat", blink=False), 26, 380, 1640)
    # a slow push-in toward his eyes
    return cam(img, 1.0 + 0.3 * ease_in_out(u), 380, 860)


def s_flash84(t, u, T):
    """quick: MAY 1984 card, then the standing terrace"""
    if u < 0.45:
        return fb.s_card(t, 0.2 + u / 0.45 * 0.8, T)
    return fb.s_terrace(t, (u - 0.45) / 0.55, T)


def s_grandad84(t, u, T):
    if u < 0.5:
        return fb.s_grandad_intro(t, u / 0.5, T)
    return fb.s_same(t, (u - 0.5) / 0.5, T)


def s_walk(t, u, T):
    """the coach walks off; you are left alone in the goalmouth"""
    c = Cam(camX=0.0, camH=1.7, hor=470)
    img = backdrop(470, stadium=True)
    pitch_persp(img, c, Zgoal=9.0)
    goal3d(img, c, 9.0)
    sprite_at(img, c, hero(gloves=True, look=-1), 0.3, 9.0, height_m=1.6)
    Z = lerp(4.5, 14.0, ease_in_out(u))
    X = lerp(-1.4, -3.0, ease_in_out(u))
    ground_shadow(img, c, X, Z, 0.4)
    sprite_at(img, c, coach(view="back", pose="run", phase=t * 1.3), X, Z, height_m=1.75)
    return cam(img, 1.08 + 0.04 * u, 360, 660)


def dorm_night(t):
    img = Image.new("RGBA", (FW, FH), (36, 40, 74, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, 760, 40):
        d.line([(0, y), (FW, y)], fill=(40, 44, 80), width=2)
    for r in range(14):
        y0 = 760 + (r ** 1.35) * 14
        d.rectangle([0, y0, FW, 760 + ((r + 1) ** 1.35) * 14], fill=(50, 54, 84) if r % 2 else (44, 48, 78))
    wx, wy, ww, wh = 420, 220, 220, 260                         # window: night, rain
    d.rectangle([wx - 6, wy - 6, wx + ww + 6, wy + wh + 6], fill=OL)
    for yy in range(wh):
        d.line([(wx, wy + yy), (wx + ww, wy + yy)], fill=tuple(int(lerp(a, b, yy / wh)) for a, b in zip((14, 18, 46), (40, 40, 80))))
    d.rectangle([wx + ww / 2 - 3, wy, wx + ww / 2 + 3, wy + wh], fill=(220, 220, 230))
    rng = random.Random(2)
    for _ in range(26):
        rx, ry = rng.uniform(wx, wx + ww), rng.uniform(wy, wy + wh)
        yy = wy + (ry - wy + t * 160) % wh
        d.line([(rx, yy), (rx - 2, yy + 14)], fill=(170, 184, 230), width=2)
    # bunk beds (the dorm from EP5)
    d.rectangle([40, 360, 64, 1000], fill=(90, 60, 40), outline=OL, width=4)
    d.rectangle([330, 360, 354, 1000], fill=(90, 60, 40), outline=OL, width=4)
    for y in (520, 860):
        d.rectangle([40, y, 354, y + 40], fill=(90, 60, 40), outline=OL, width=4)
        d.rectangle([64, y - 34, 330, y], fill=(180, 180, 200), outline=OL, width=4)
    d.rectangle([440, 560, 560, 700], fill=(200, 166, 40), outline=OL, width=5)
    d.text((500, 630), "SAVE", font=font(800, 26), fill=OL, anchor="mm")
    return img


def phone_ui(img, cx, cy, state, t, k=1.0):
    """state: 'calling', 'talk', 'silent', 'ended'"""
    w, h = 380 * k, 640 * k
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w / 2 - 14, cy - h / 2 - 14, cx + w / 2 + 14, cy + h / 2 + 14], 44, fill=(24, 26, 36), outline=OL, width=6)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 34, fill=(20, 30, 60))
    if k < 0.6:
        return
    paste(img, grandad(mouth="flat", blink=state == "silent" and int(t * 2) % 4 == 0), 8, cx, cy + 40)
    d = ImageDraw.Draw(img)
    d.text((cx, cy - 250), "GRANDAD", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    sub = {"calling": "calling...", "talk": "00:0" + str(int(t * 2) % 10), "silent": "00:1" + str(int(t * 2) % 10),
           "ended": "CALL ENDED", "msg": "1 NEW MESSAGE"}[state]
    d.text((cx, cy - 200), sub, font=font(600 if state != "ended" else 800, 26), fill=(180, 190, 220) if state != "ended" else (240, 80, 80), anchor="mm")
    # voice wave: moving while you talk, a flat line in the silence
    y0 = cy + 120
    pts = []
    for i in range(41):
        x = cx - 150 + i * 7.5
        amp = 26 * math.sin(i * 0.9 + t * 14) * math.sin(i / 40 * math.pi) if state == "talk" else 0
        pts.append((x, y0 + amp))
    if state != "msg":
        d.line(pts, fill=(110, 222, 120) if state == "talk" else (120, 130, 160), width=5)
    for x, col in ((cx - 90, (230, 60, 60)), (cx + 90, (60, 200, 90))):
        if state in ("ended", "msg"):
            continue
        r = 34 + (6 * math.sin(t * 12) if state == "calling" and x > cx else 0)
        d.ellipse([x - r, cy + 230 - r, x + r, cy + 230 + r], fill=col, outline=OL, width=5)


def s_night(t, u, T):
    img = dorm_night(t)
    paste(img, hero(pose="phone", mouth="flat"), 11, 200, 1200)
    phone_ui(img, 470, 820, "calling" if u < 0.6 else "talk", t, spring(t - T - 0.2, 13, 7))
    return cam(img, 1.0 + 0.04 * u, 360, 760)


def s_ask(t, u, T):
    img = dorm_night(t).filter(ImageFilter.GaussianBlur(4))
    phone_ui(img, 360, 820, "talk", t)
    return cam(img, 1.0 + 0.06 * u, 360, 820)


def s_hangup(t, u, T):
    img = dorm_night(t).filter(ImageFilter.GaussianBlur(4))
    phone_ui(img, 360, 820, "silent" if u < 0.62 else "ended", t)
    if u > 0.62:
        img = flash(img, 0.3 * clamp(1 - (u - 0.62) * 8), (255, 60, 60))
    vignette(img, 0.3 + 0.3 * u)
    return cam(img, 1.0 + 0.1 * ease_in_out(u), 360, 820)


def s_mason(t, u, T):
    img = backdrop(470, stadium=True).filter(ImageFilter.GaussianBlur(4))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 470, FW, FH], fill=(78, 140, 76))
    paste(img, mason(mouth="grin" if (int(t * 6) % 2 and RIGHT) else "smile", look=-1), 26, 360, 1520)
    if not RIGHT:      # he claps, unwillingly
        k = abs(math.sin(t * 8))
        for sx in (-1, 1):
            ImageDraw.Draw(img).rounded_rectangle([360 + sx * 40 * k - 30, 1150, 360 + sx * 40 * k + 30, 1230], 12,
                                                  fill=SKIN["light"][0], outline=OL, width=5)
    return cam(img, 1.0 + 0.06 * u, 360, 800)


def s_message(t, u, T):
    img = dorm_night(t).filter(ImageFilter.GaussianBlur(4))
    phone_ui(img, 360, 820, "msg", t)
    k = spring(t - T - 0.2, 13, 7)
    if k > 0.05:      # the text bubble from GRANDAD
        d = ImageDraw.Draw(img)
        w, h = 330 * min(1.05, k), 120 * min(1.05, k)
        x0, y0 = 360 - w / 2, 960 - h / 2
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 26, fill=(250, 250, 252), outline=OL, width=5)
        if k > 0.6:
            d.text((360, 940), "Stay away", font=font(800, 34), fill=(200, 40, 50), anchor="mm")
            d.text((360, 984), "from him.", font=font(800, 34), fill=(200, 40, 50), anchor="mm")
    vignette(img, 0.5)
    return cam(img, 1.0 + 0.12 * ease_in_out(u), 360, 900)


CARDS = [(190, "ASK COACH", "KNOCK ON HIS DOOR", C_Y), (530, "STAY AWAY", "LISTEN TO GRANDAD", C_R)]


def choice_cards(img, t, T0):
    d = ImageDraw.Draw(img)
    for i, (x, lab, sub, c) in enumerate(CARDS):
        k = spring(t - T0 - i * 0.15, 13, 7)
        if k < 0.05:
            continue
        hl = 0.5 + 0.5 * math.sin(t * 3.2 + i * math.pi)
        w, h = 310 * k * (1 + 0.04 * hl), 440 * k * (1 + 0.04 * hl)
        y = 700 + UY * 0.4 - 10 * hl
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 24, fill=(16, 18, 36), outline=c, width=7)
        if k > 0.6:
            if i == 0:
                d.rectangle([x - 80, y - 170, x + 20, y + 10], fill=(150, 100, 60), outline=OL, width=5)    # door
                d.rectangle([x - 60, y - 150, x, y - 120], fill=(250, 246, 236), outline=OL, width=3)
                d.text((x - 30, y - 135), "COACH", font=font(800, 12), fill=OL, anchor="mm")
                paste(img, hero(look=-1, gloves=True), 4, x + 70, y + 40)
            else:
                d.rounded_rectangle([x - 60, y - 190, x + 60, y + 20], 18, fill=(24, 26, 36), outline=OL, width=5)  # phone
                d.rounded_rectangle([x - 48, y - 176, x + 48, y + 6], 12, fill=(20, 30, 60))
                d.rounded_rectangle([x - 44, y - 120, x + 44, y - 60], 10, fill=(250, 250, 252))
                d.text((x, y - 98), "Stay away", font=font(800, 14), fill=(200, 40, 50), anchor="mm")
                d.text((x, y - 80), "from him.", font=font(800, 14), fill=(200, 40, 50), anchor="mm")
            d = ImageDraw.Draw(img)
            d.text((x, y + 110), lab, font=font(800, 36), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            d.text((x, y + 160), sub, font=font(700, 19), fill=(220, 224, 240), anchor="mm")


def typing_box(img, t, T0):
    d = ImageDraw.Draw(img)
    y = 980 + UY * 0.4
    d.rounded_rectangle([90, y, 630, y + 70], 18, fill=(16, 18, 36), outline=(255, 255, 255), width=3)
    words = ["ASK COACH", "STAY AWAY"]
    k = (t - T0) / 1.1
    wi = min(1, int(k))
    w = words[wi]
    n = int(len(w) * clamp((k - wi) * 2)) if k < 2 else len(w)
    d.text((120, y + 35), w[:n] + ("|" if int(t * 4) % 2 else ""), font=font(800, 30), fill=(255, 255, 255), anchor="lm")


def s_choice(t, u, T):
    img = fb.choice_bg()
    choice_cards(img, t, T - 0.2)
    typing_box(img, t, T + 0.3)
    pill(img, 360, 340 + UY, "VOTE BEFORE FRIDAY", (200, 50, 60), spring(t - T - 0.3, 13, 7), 28)
    return cam(img, 1.0 + 0.02 * u, 360, 760)


def s_end(t, u, T):
    img = fb.choice_bg()
    img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (10, 12, 30)), 0.88 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420 + UY * 0.4, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 560], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 150), "PART 8", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
    tap = T + 0.8
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
        gx = lerp(640, bx + 100, ease_in_out((t - T) / 0.8)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, cc in ((230, "ASK COACH", C_Y), (490, "STAY AWAY", C_R)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 115, py + 400 - hop, x + 115, py + 470 - hop], 18, fill=(30, 36, 76), outline=cc, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 30), fill=cc, anchor="mm")
    d.text((360, py + 520), "VOTE IN THE COMMENTS", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    return img


SCENES = [s_hook, s_vote, s_kick, s_result, s_sheet, s_mason, s_stare, fb.s_glove, fb.s_pale, s_flash84, s_grandad84,
          fb.s_hang, fb.s_jump, fb.s_impact, fb.s_stretcher, fb.s_mud, fb.s_today, s_walk, s_night, s_ask, s_hangup,
          s_message, s_choice, s_end]
assert len(SCENES) == len(LINES)


def grade(img):
    img = ImageEnhance.Color(img).enhance(0.9)
    return Image.blend(img, Image.new("RGB", img.size, (60, 50, 70)), 0.04)


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s:
            i = k
    return i


def frame(t):
    i = line_at(t)
    T = STARTS[i]
    u = clamp((t - T) / max(0.1, D(i)))
    img = SCENES[i](t, u, T).convert("RGB")
    img = grade(img).convert("RGBA")
    if i in FLASH:
        img = vhs(img, t, 0.8)
        vhs_osd(img, t, "MAY 14 1984")
    if i > 0 and t - T < 0.07:
        img = flash(img, 0.3)
    overlay(img, t, i)
    return img.convert("RGB")


if __name__ == "__main__":
    ts = [float(x) for x in sys.argv[1].split(",")]
    ims = [frame(x).resize((240, 427)) for x in ts]
    out = Image.new("RGB", (240 * min(6, len(ims)), 427 * ((len(ims) + 5) // 6)))
    for k, im in enumerate(ims):
        out.paste(im, (240 * (k % 6), 427 * (k // 6)))
    out.save(sys.argv[2])
    print("TOTAL", round(TOTAL, 2), [round(s, 1) for s in STARTS])
