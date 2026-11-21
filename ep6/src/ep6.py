"""EP6 — the derby. remi_sport-style perspective match scenes."""
import os, sys, json
from persp import *
from persp import _xzy, ball_trail
import build   # caption chunking + office/room helpers

PLATFORM = os.environ.get("PLATFORM", "tiktok")
EP = 6
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
FOLLOW = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"
LINES = [
    [("YOU", W), ("ASKED", W), ("FOR", W), ("THE", W), ("SHIRT.", Y)],
    [("YOU", W), ("KNOCK.", O), ("THE", W), ("COACH", W), ("LOOKS", W), ("UP.", W)],
    [("\"MASON", R_), ("SAYS", W), ("YOU'LL", W), ("CRACK.", R_), ("PROVE", W), ("HIM", W), ("WRONG.\"", G)],
    [("DERBY", Y), ("DAY.", Y), ("RIVERSIDE", R_), ("AGAINST", W), ("NORTHFIELD.", B)],
    [("GRANDAD.", B), ("SEAT", W), ("FOURTEEN.", B), ("THUMBS", G), ("UP.", G)],
    [("MINUTE", W), ("THREE.", W), ("THEIR", W), ("STRIKER.", B), ("LOW", W), ("AND", W), ("HARD.", R_)],
    [("THROUGH", W), ("YOUR", W), ("LEGS.", R_), ("ZERO,", W), ("ONE.", R_)],
    [("MASON", R_), ("LAUGHS.", W), ("\"TOLD", W), ("YOU.\"", R_)],
    [("YOU", W), ("GET", W), ("BACK", G), ("UP.", G), ("LIKE", W), ("GRANDAD", B), ("SAID.", W)],
    [("CORNER.", W), ("HEADER.", W), ("YOU", W), ("FLY.", Y), ("SAVED!", G)],
    [("ONE", W), ("ON", W), ("ONE.", W), ("YOU", W), ("SPREAD", W), ("BIG.", Y), ("SAVED", G), ("AGAIN!", G)],
    [("THEN", W), ("MASON", R_), ("SCORES.", G), ("ONE,", W), ("ONE.", Y)],
    [("LAST", R_), ("MINUTE.", R_), ("FREE", W), ("KICK.", W), ("EDGE", W), ("OF", W), ("THE", W), ("BOX.", W)],
    [("THEIR", W), ("CAPTAIN.", B), ("TOP", Y), ("CORNER.", Y)],
    [("YOU", W), ("SEE", W), ("IT", W), ("EARLY.", Y), ("YOU", W), ("PUSH", W), ("OFF.", W)],
    [("FINGERTIPS.", Y), ("CROSSBAR.", W), ("OUT!", G)],
    [("FINAL", W), ("WHISTLE.", W), ("ONE,", W), ("ONE.", Y), ("PENALTIES.", R_)],
    [("GRANDAD", B), ("STANDS", W), ("UP.", W), ("SEAT", W), ("FOURTEEN.", B)],
    [("THEIR", W), ("LAST", W), ("PENALTY.", R_), ("THEIR", W), ("CAPTAIN", B), ("AGAIN.", W)],
    [("LAST", W), ("TIME", W), ("HE", W), ("WENT", W), ("RIGHT.", B), ("LEFT", Y), ("OR", W), ("RIGHT?", B)],
    [("VOTE", W), ("BELOW.", G), (FOLLOW, R_), ("FOR", W), ("PART 7.", Y)],
]
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vo/ep6_lines.json")
if os.path.exists(_vf):
    VOICE = [tuple(x) for x in json.load(open(_vf))["lines"]]
else:   # estimated narration timing (no voice yet)
    VOICE, t0 = [], 0.05
    for ws in LINES:
        d_ = max(1.4, 0.36 * len(ws) + 0.3)
        VOICE.append((t0, t0 + d_)); t0 += d_ + 0.47
STARTS = [max(0.0, a - 0.12) for a, _ in VOICE]
STARTS[0] = 0.0
TOTAL = max(VOICE[-1][1] + 1.6, 61.5)


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
    banner(img, EP)
    ch = build.chunks(word_times(i))
    cur = ch[0]
    for c in ch:
        if t >= c[0][1] - 0.04:
            cur = c
    if i == 0 and t < 0.4:
        cur = [(w, -1, c) for w, _, c in cur]
    caption(img, cur, t, size=56, wrap=620)


# ------------------------------------------------------------------ cast
NF = (80, 150, 230)            # Northfield: sky blue
RS = (210, 52, 56)             # Riverside outfield: red


def opp(n, view="front", pose="stand", **kw):
    sk = {4: "tan", 5: "dark", 7: "light", 9: "brown", 10: "light"}.get(n, "tan")
    hr = {4: "black", 5: "black", 7: "ginger", 9: "black", 10: "dark"}.get(n, "dark")
    st = {10: "spiky"}.get(n, "short")
    return person(Kit(NF, (250, 250, 250), NF, n), skin=sk, hair=hr, style=st, view=view, pose=pose, **kw)


def ours(n, **kw):
    if n == 9:
        return mason(**kw)
    sk = {4: "tan", 5: "brown", 7: "dark", 6: "light"}.get(n, "light")
    return person(Kit(RS, (245, 245, 250), RS, n), skin=sk, hair={5: "black", 7: "black", 6: "ginger"}.get(n, "dark"),
                  style="short", **kw)


def opp_keeper(**kw):
    return person(Kit((140, 70, 180), (30, 30, 40), (140, 70, 180), 1), skin="tan", hair="black", style="short", gloves=True, **kw)


def score_state(t):
    l = 1 if t >= STARTS[11] + 0.6 * (STARTS[12] - STARTS[11]) else 0
    r = 1 if t >= STARTS[6] + 0.35 * (STARTS[7] - STARTS[6]) else 0
    return l, r


def mini_score(img, t, minute):
    l, r = score_state(t)
    d = ImageDraw.Draw(img)
    y = 252
    d.rounded_rectangle([200, y, 520, y + 56], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.rectangle([212, y + 12, 236, y + 44], fill=RS); d.rectangle([484, y + 12, 508, y + 44], fill=NF)
    d.text((360, y + 28), f"RIV  {l} - {r}  NOR", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
    d.rounded_rectangle([318, y + 58, 402, y + 86], 8, fill=(210, 52, 56))
    d.text((360, y + 72), minute, font=font(800, 20), fill=(255, 255, 255), anchor="mm")


def slowmo_bars(img, k):
    if k <= 0:
        return
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, FW, int(40 * k)], fill=(0, 0, 0))
    d.rectangle([0, FH - int(40 * k), FW, FH], fill=(0, 0, 0))


# ------------------------------------------------------------------ keeper-view set (camera behind our goal line)
def keeper_view(t, hor=520):
    c = Cam(camX=0.0, camH=1.9, hor=hor)
    img = backdrop(hor, stadium=True)
    pitch_near(img, c, 0.0)
    return img, c


def shooter_view(t, Zg, camX=0.0, camH=2.6, hor=430, stadium=True):
    c = Cam(camX=camX, camH=camH, hor=hor)
    img = backdrop(hor, stadium=stadium)
    pitch_persp(img, c, Zgoal=Zg)
    return img, c


# ------------------------------------------------------------------ scenes
def s_hook(t, u, T):
    img, c = keeper_view(t)
    ground_shadow(img, c, 0.4, 8.6, 0.4)
    sprite_at(img, c, opp(9, pose="kick", phase=1.0), 0.4, 8.6, height_m=1.55)
    pts = arc((0.2, 8.0, 0.15), (0.3, 1.9, 1.35), apex=0.6)
    a = clamp(0.45 + u * 0.55)
    dotted_path(img, c, pts, 1.0, from_=a)
    bx, by = ball_at(img, c, *at(pts, a))
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    return cam(img, 1.0 + 0.03 * u, 360, 700)


def office(t):
    img = build.room_set("office6", wall=(200, 176, 146), floor=((176, 152, 120), (164, 140, 108))).copy()
    d = ImageDraw.Draw(img)
    d.rectangle([60, 200, 300, 380], fill=(250, 246, 236), outline=OL, width=6)     # tactics board
    for k in range(5):
        d.ellipse([90 + k * 40, 260 + (k % 2) * 40, 110 + k * 40, 280 + (k % 2) * 40], fill=(210, 52, 56))
    d.line([(100, 330), (260, 240)], fill=(40, 90, 200), width=5)
    d.rectangle([470, 160, 640, 760], fill=(150, 100, 60), outline=OL, width=6)       # door
    d.ellipse([480, 450, 500, 470], fill=C_Y, outline=OL, width=3)
    d.rectangle([520, 200, 600, 240], fill=(250, 246, 236), outline=OL, width=4)
    d.text((560, 220), "COACH", font=font(800, 20), fill=OL, anchor="mm")
    return img


def s_knock(t, u, T):
    img = office(t)
    # desk in front, coach behind it looks up; you at the open door
    paste(img, hero(look=-1), 9, 560, 760)
    paste(img, coach(look=1 if u > 0.45 else 0, blink=u < 0.45), 13, 230, 1010)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 900, 520, 1000], fill=(120, 80, 50), outline=OL, width=6)
    d.rectangle([60, 1000, 90, 1200], fill=(100, 64, 40), outline=OL, width=5)
    d.rectangle([470, 1000, 500, 1200], fill=(100, 64, 40), outline=OL, width=5)
    d.rectangle([120, 880, 260, 902], fill=(250, 246, 236), outline=OL, width=3)    # papers
    for k in range(3):
        kt = T + 0.15 + k * 0.28
        impact_lines(img, 470, 420, kt, t, 8)
    return cam(img, 1 + 0.05 * u, 360, 760)


def s_coach(t, u, T):
    img = office(t).filter(ImageFilter.GaussianBlur(4))
    talk = int(t * 7) % 2 == 0
    paste(img, coach(mouth="open" if talk else "flat", blink=0.62 < u < 0.68, look=0), 26, 360, 1560)
    return cam(img, 1.03 + 0.04 * u, 360, 800)


def s_walkout(t, u, T):
    c = Cam(camX=0.0, camH=1.9, hor=520)
    img = backdrop(520, stadium=True)
    pitch_persp(img, c, Zgoal=None)
    d = ImageDraw.Draw(img)
    x0, y0 = c.p(-40, 26); x1, y1 = c.p(40, 26)
    d.line([(x0, y0), (x1, y1)], fill=LINE, width=4)          # halfway line
    pts = [c.p(5 * math.cos(a), 26 + 5 * math.sin(a)) for a in np.linspace(0, math.tau, 50)]
    d.line(pts, fill=LINE, width=3)
    walk = u * 3
    for i, n in enumerate((4, 5, 7, 10, 9)):          # Northfield lined up on their half
        X = -4 + i * 2
        ground_shadow(img, c, X, 30, 0.35)
        sprite_at(img, c, opp(n), X, 30, height_m=1.55)
    for i, n in enumerate((4, 6, 9, 7, 5)):           # Riverside walking out
        X = -4.2 + i * 2.1
        Z = 14 - walk + (i % 2) * 0.6
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, ours(n, view="back", pose="run", phase=t * 1.6 + i * 0.3), X, Z, height_m=1.55)
    paste(img, hero(view="back", pose="run", phase=t * 1.6, gloves=True), 13, 360, 1500 + abs(math.sin(t * 5)) * 10)
    sk = spring(t - T - 0.2, 13, 7)
    if sk > 0.05:
        d = ImageDraw.Draw(img)
        w = 520 * sk
        d.rounded_rectangle([360 - w / 2, 840, 360 + w / 2, 910], 14, fill=(14, 16, 30), outline=C_Y, width=4)
        if sk > 0.6:
            d.text((360, 875), "RIVERSIDE  vs  NORTHFIELD", font=font(800, 30), fill=(255, 255, 255), anchor="mm")
    return cam(img, 1 + 0.04 * u, 360, 900)


def stands(t, grandad_pose="sit", u=0.0):
    img = Image.new("RGBA", (FW, FH), (60, 46, 60, 255))
    crowd_band(img, 0, 640, seed=21, blur=3.5)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 640, FW, FH], fill=(78, 80, 100))
    for x in (-60, 200, 460):
        d.rounded_rectangle([x, 640, x + 220, 960], 22, fill=(170, 40, 52), outline=OL, width=6)
        d.rounded_rectangle([x, 940, x + 220, 1030], 16, fill=(140, 30, 44), outline=OL, width=6)
    d.rounded_rectangle([270, 660, 380, 720], 10, fill=(245, 236, 220), outline=OL, width=4)
    d.text((325, 692), "14", font=font(800, 40), fill=(170, 30, 40), anchor="mm")
    # Mum next to him, green scarves
    paste(img, person(Kit((70, 108, 189), (45, 75, 140), (45, 75, 140)), hair="brown", style="pony", mouth="smile",
                      pose="sit", blink=int(t * 2) % 7 == 0), 10, 560, 1090)
    if grandad_pose == "sit":
        paste(img, grandad(pose="sit", mouth="smile", tube=True, blink=int(t * 2.3) % 6 == 0), 11, 310, 1090)
    else:
        rise = ease_out(u * 2)
        paste(img, grandad(pose="stand" if rise > 0.5 else "sit", mouth="open", tube=True), 11, 310, 1090 - 30 * rise)
    paste(img, cane(26), 9, 160, 1120)
    return img


def s_grandad(t, u, T):
    img = stands(t)
    # thumbs up: his hand raised beside his face
    k = ease_out((u - 0.5) / 0.2)
    if k > 0:
        d = ImageDraw.Draw(img)
        hx, hy = 430, 800 - 60 * k
        d.rounded_rectangle([hx - 24, hy, hx + 24, hy + 44], 10, fill=SKIN["old"][0], outline=OL, width=4)
        d.rounded_rectangle([hx - 22, hy - 38, hx - 6, hy + 6], 8, fill=SKIN["old"][0], outline=OL, width=4)
    return cam(img, 1.02 + 0.05 * u, 330, 880)


def s_strike(t, u, T, goal_=False):
    """behind their #9: low hard shot through our keeper's legs"""
    img, c = shooter_view(t, 17)
    goal3d(img, c, 17)
    pts = arc((0.2, 2.6, 0.12), (0.15, 18.0, 0.22), apex=0.08)
    kick = 0.35
    if not goal_:
        a = clamp((u - kick) / (1 - kick)) * 0.55
    else:
        a = 0.55 + 0.45 * clamp(u / 0.35)
    # our keeper: ready, legs apart; after the goal he turns, hands on head
    ground_shadow(img, c, 0, 17, 0.45)
    sprite_at(img, c, hero(pose="ready" if not goal_ or u < 0.35 else "stand", gloves=True, mouth="open" if goal_ else "flat"), 0, 17, height_m=1.6)
    for i, (X, Z, n) in enumerate(((-3, 12, 4), (2.6, 11, 5))):
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, ours(n, view="back", pose="run", phase=t * 2 + i), X, Z, height_m=1.55)
    if a > 0:
        if not goal_:
            dotted_path(img, c, pts, 0.55, from_=a)
        ball_trail(img, c, pts, a, 0.1)
        ball_at(img, c, *at(pts, a))
    else:
        ball_at(img, c, *pts[0])
    if goal_ and u > 0.35:
        impact_lines(img, *c.p(0.15, 18, 0.3), T + 0.35 * (STARTS[7] - STARTS[6]), t, 10)
    striker = opp(9, view="back", pose="kick" if u > kick - 0.1 else "run", phase=clamp((u - kick + 0.1) / 0.2) if u > kick - 0.1 else t * 2)
    paste(img, striker, 11, 250, 1420)
    mini_score(img, t, "3'")
    if goal_:
        img = flash(img, 0.35 * clamp(1 - abs(u - 0.37) * 8), (255, 50, 50))
    return cam(img, 1 + (0.05 * u if not goal_ else 0.12), *c.p(0, 17, 0.8), *shake(t, T + 0.37 * (STARTS[7] - STARTS[6]), .3, 10) if goal_ else (0, 0))


def s_goal(t, u, T):
    return s_strike(t, u, T, goal_=True)


def s_mason(t, u, T):
    img, c = shooter_view(t, 30)
    img = img.filter(ImageFilter.GaussianBlur(3))
    paste(img, mason(mouth="grin" if int(t * 6) % 2 else "smile", look=-1), 26, 360, 1560)
    return cam(img, 1.02 + 0.05 * u, 360, 820)


def s_getup(t, u, T):
    """close, low: you lie in the net... and get back up"""
    c = Cam(camX=0, camH=1.6, hor=470)
    img = backdrop(470, stadium=True)
    pitch_persp(img, c, Zgoal=6.5)
    goal3d(img, c, 6.5)
    if u < 0.45:
        draw_ball(img, *c.p(1.2, 7.4, 0), 1.0)
        sp_s = 1.6 * c.k(6.4) / 31
        sp = hero(pose="reach", gloves=True, blink=True).resize((int(24 * sp_s), int(39 * sp_s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
        x, y = c.p(0.2, 6.4)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * sp_s)))
    else:
        ground_shadow(img, c, 0, 6.4, 0.5)
        k = ease_out((u - 0.45) / 0.25)
        sprite_at(img, c, hero(gloves=True, mouth="flat"), 0, 6.4, Y=-0.4 * (1 - k), height_m=1.6)
        draw_ball(img, *c.p(1.2, 7.4, 0), 1.0)
        glow_ring(img, *c.p(0, 6.4, 1.0), 120 * k, 0.4 * k, (255, 240, 180))
    return cam(img, 1 + 0.05 * u, 360, 900)


def s_header(t, u, T):
    img, c = shooter_view(t, 11, camX=-0.5, camH=2.2, hor=470)
    goal3d(img, c, 11)
    cross = arc((-14, 9.5, 0.3), (0.4, 8.2, 2.0), apex=3.5)
    head = arc((0.4, 8.2, 2.0), (-2.0, 11.0, 1.7), apex=0.3)
    jump = math.sin(clamp((u - 0.25) / 0.35) * math.pi) * 0.55
    ground_shadow(img, c, 0.4, 8.2, 0.35)
    sprite_at(img, c, opp(5, view="back", pose="celebrate" if jump > 0.1 else "stand"), 0.4, 8.2, Y=jump, height_m=1.55)
    phase = clamp((u - 0.38) / 0.62)
    gx, gy = keeper_world(img, c, 0, 11, -1, phase)
    if u < 0.4:
        a = u / 0.4
        dotted_path(img, c, cross, 1.0, from_=a)
        ball_trail(img, c, cross, a, 0.1)
        ball_at(img, c, *at(cross, a))
    elif phase < 0.45:
        a = clamp((u - 0.4) / 0.25)
        ball_trail(img, c, head, a, 0.25)
        ball_at(img, c, *at(head, a))
        impact_lines(img, *c.p(0.4, 8.2, 2.1), T + 0.4 * (STARTS[10] - T), t, 8)
    else:
        draw_ball(img, gx, gy + 12, 0.9)
        if phase < 0.6:
            glow_ring(img, gx, gy, 50, 0.8, (255, 255, 200))
    mini_score(img, t, "34'")
    return cam(img, 1.05 + 0.04 * u, 360, 640)


def s_1v1(t, u, T):
    img, c = keeper_view(t)
    Z = lerp(13, 4.0, ease_in_out(clamp(u / 0.6)))
    ground_shadow(img, c, 0.2, Z, 0.4)
    sprite_at(img, c, opp(7, pose="run" if u < 0.6 else "kick", phase=t * 2.4 if u < 0.6 else 1.0), 0.2, Z, height_m=1.55)
    for X, Z2, n in ((-3.5, Z + 3, 5), (3.2, Z + 4, 4)):
        ground_shadow(img, c, X, Z2, 0.35)
        sprite_at(img, c, ours(n, pose="run", phase=t * 2.4), X, Z2, height_m=1.55)
    if u < 0.6:
        ball_at(img, c, 0.4, Z - 0.6, 0.11)
    else:
        a = clamp((u - 0.6) / 0.15)
        if a < 1:
            ball_at(img, c, lerp(0.4, 0.1, a), lerp(Z - 0.6, 1.3, a), lerp(0.1, 1.0, a))
        else:   # blocked: ball balloons away to the side
            b = clamp((u - 0.75) / 0.25)
            ball_at(img, c, lerp(0.1, 4.0, b), lerp(1.3, 3.5, b), 1.0 + 1.6 * math.sin(b * math.pi))
            glow_ring(img, 330, 1080, 120 * (1 - b) + 40, 0.7 * (1 - b), (255, 255, 200))
    big_pose = "celebrate" if u > 0.55 else "ready"
    paste(img, hero(view="back", pose=big_pose, gloves=True), 13, 330, 1430)
    mini_score(img, t, "61'")
    return cam(img, 1 + 0.04 * u, 360, 800, *shake(t, T + 0.75 * (STARTS[11] - T), .3, 12))


def s_mason_goal(t, u, T):
    img, c = shooter_view(t, 15, camX=0.4)
    goal3d(img, c, 15)
    pts = arc((0.3, 2.6, 0.12), (1.9, 15.6, 0.6), apex=0.6, curve=0.6)
    kick = 0.3
    a = clamp((u - kick) / 0.3)
    phase = clamp((u - kick) / 0.5) * 0.7 + 0.2 if u > kick else 0.0
    ground_shadow(img, c, 0, 15, 0.45)
    if u < kick:
        sprite_at(img, c, opp_keeper(pose="ready"), 0, 15, height_m=1.6)
    else:   # their keeper dives the wrong way
        s = 1.6 * c.k(15) / 31
        sp = opp_keeper(pose="celebrate").resize((int(24 * s), int(39 * s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
        x, y = c.p(-1.2 * ease_out(clamp((u - kick) / 0.4)), 15, 0.4 * math.sin(clamp((u - kick) / 0.4) * math.pi))
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height)))
    if a < 1:
        if u > kick:
            dotted_path(img, c, pts, 1.0, from_=a)
            ball_trail(img, c, pts, a, 0.15)
        ball_at(img, c, *at(pts, a))
    else:
        b = clamp((u - kick - 0.3) / 0.3)
        x, y = c.p(1.9, 15.8, 0.6 * (1 - b))
        draw_ball(img, x, y + 10, 0.8)
        impact_lines(img, x, y, T + (kick + 0.3) * (STARTS[12] - T), t, 10)
    paste(img, mason(view="back", pose="kick" if u > kick - 0.1 else "run", phase=clamp((u - kick + 0.1) / 0.2) if u > kick - 0.1 else t * 2), 11, 240, 1330)
    mini_score(img, t, "78'")
    if a >= 1:
        img = flash(img, 0.3 * clamp(1 - (u - kick - 0.3) * 6), (110, 230, 120))
    return cam(img, 1.03 + 0.04 * u, 380, 760)


def s_board(t, u, T):
    img = Image.new("RGBA", (FW, FH), (24, 26, 44, 255))
    crowd_band(img, 0, 560, seed=33, blur=1.0)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(18, 20, 34))
    l, r = score_state(t)
    scoreboard(img, 640, "RIV", "NOR", l, r, "90'", spring(t - T, 12, 7), t=t)
    for k in range(3):  # flashing "LAST MINUTE" lights
        if int(t * 4 + k) % 2:
            d.ellipse([170 + k * 180, 900, 200 + k * 180, 930], fill=(240, 80, 80))
    return cam(img, 1 + 0.05 * u, 360, 700)


FK = arc((0.6, 3.2, 0.1), (2.05, 19.0, 1.8), apex=2.6, curve=-1.2)   # free kick to the top right corner


def fk_scene(img, c, t, u, kick_at, a_ball, keeper_phase, wall_jump=0.0, show_path=True):
    goal3d(img, c, 19)
    gx = gy = None
    gx, gy = keeper_world(img, c, -0.2, 19, 1, keeper_phase)
    for i, X in enumerate((-1.6, -0.9, -0.2, 0.5)):
        ground_shadow(img, c, X, 12.5, 0.3)
        sprite_at(img, c, ours((4, 5, 9, 7)[i], pose="celebrate" if wall_jump > 0.05 else "stand"), X, 12.5, Y=wall_jump, height_m=1.55)
    if show_path:
        dotted_path(img, c, FK, 0.97, from_=max(0.0, a_ball))
    ball_trail(img, c, FK, a_ball, 0.08)
    ball_at(img, c, *at(FK, max(0.0, a_ball)))
    return gx, gy


def s_fk(t, u, T):
    img, c = shooter_view(t, 19)
    kick = 0.62
    a = clamp((u - kick) / 0.6) * 0.3 if u > kick else 0.0
    fk_scene(img, c, t, u, kick, a, 0.0, wall_jump=0.4 * math.sin(clamp((u - kick) / 0.3) * math.pi) if u > kick else 0)
    ring_on_grass(img, c, 0.6, 3.2, 0.7, C_Y)
    paste(img, opp(10, view="back", pose="kick" if u > kick - 0.1 else "stand", phase=clamp((u - kick + 0.1) / 0.2)), 11, 230, 1330)
    mini_score(img, t, "90'")
    return cam(img, 1 + 0.04 * u, 360, 640)


def s_slowmo(t, u, T):
    img, c = shooter_view(t, 19, camX=0.8, camH=2.2, hor=460)
    a = 0.3 + 0.45 * u
    phase = 0.2 + 0.45 * u
    fk_scene(img, c, t, u, 0, a, phase, show_path=True)
    tx, ty = c.p(2.05, 19, 1.8)
    glow_ring(img, tx, ty, 40, 0.5 + 0.3 * math.sin(t * 8), C_Y)
    slowmo_bars(img, ease_out(u * 4))
    x, y = c.p(*_xzy(at(FK, a)))
    return cam(img, 1.25 + 0.35 * u, lerp(360, x, 0.5), lerp(640, y, 0.5))


def s_finger(t, u, T):
    """close-up at the top corner: fingertips push it onto the crossbar and over"""
    c = Cam(camX=1.6, camH=1.6, hor=560)
    img = backdrop(560, stadium=True)
    pitch_persp(img, c, Zgoal=6.0, box=False)
    goal3d(img, c, 6.0)
    k_ = c.k(6.0)
    sc = 1.6 * k_ / 31
    sp = hero(pose="reach", gloves=True, mouth="open").resize((int(24 * sc), int(39 * sc)), Image.NEAREST)
    sp = sp.rotate(-55, expand=True, resample=Image.NEAREST)
    fly = clamp(u / 0.5)
    kx, ky = c.p(lerp(0.9, 1.35, fly), 6.0, lerp(1.05, 1.25, math.sin(fly * math.pi)))
    ground_shadow(img, c, 1.2, 6.0, 0.8, 70)
    img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
    hit = 0.35
    if u < hit:
        a = u / hit
        bx, by = c.p(lerp(1.5, 2.25, a), lerp(3.0, 6.0, a), lerp(1.75, 1.9, a))
    else:
        b = clamp((u - hit) / 0.65)
        bx, by = c.p(2.25 + 0.4 * b, 6.0 + 1.5 * b, 2.05 + 1.0 * math.sin(b * math.pi * 0.8))
    draw_ball(img, bx, by, 1.6)
    if u >= hit:
        impact_lines(img, *c.p(2.25, 6.0, 2.0), T + hit * (STARTS[16] - T), t, 12)
        glow_ring(img, *c.p(2.25, 6.0, 2.0), 60 + 160 * clamp((u - hit) * 3), 0.9 * (1 - clamp((u - hit) * 2)), (255, 255, 210))
    slowmo_bars(img, 1 - ease_out((u - hit) * 3) if u > hit else 1)
    img = flash(img, 0.45 * clamp(1 - abs(u - hit) * 14))
    return cam(img, 1.05, 420, 720, *shake(t, T + hit * (STARTS[16] - T), .35, 14))


def s_whistle(t, u, T):
    img = Image.new("RGBA", (FW, FH), (24, 26, 44, 255))
    crowd_band(img, 0, 560, seed=34, blur=1.0)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(18, 20, 34))
    scoreboard(img, 640, "RIV", "NOR", 1, 1, "FULL TIME", 1.0, t=t)
    if u > 0.55:
        pill(img, 360, 1000, "PENALTIES", (200, 40, 50), spring(t - T - 0.55 * (STARTS[17] - T), 13, 7), 56)
    return cam(img, 1 + 0.05 * u, 360, 760)


def s_grandad_up(t, u, T):
    img = stands(t, "stand", u)
    return cam(img, 1.02 + 0.06 * u, 330, 860)


def s_pen(t, u, T, choice=False):
    img, c = keeper_view(t)
    ground_shadow(img, c, 0.0, 8.3, 0.4)
    sprite_at(img, c, opp(10, mouth="flat"), 0.0, 8.3, height_m=1.55)
    ball_at(img, c, 0.0, 7.6, 0.0)
    if choice:
        d = ImageDraw.Draw(img)
        for side, col, bg, lab in ((-1, C_Y, (200, 160, 20), "LEFT"), (1, C_B, (40, 110, 200), "RIGHT")):
            k = clamp((u - (0.05 if side < 0 else 0.25)) / 0.3)
            if k <= 0:
                continue
            x0, y0 = 330 + side * 120, 1060
            x1, y1 = 360 + side * 300, 820
            pts = [(lerp(x0, x1, a), lerp(y0, y1, a) - 120 * math.sin(a * math.pi)) for a in np.linspace(0, k, 24)]
            for j in range(0, len(pts) - 1, 2):
                d.line([pts[j], pts[j + 1]], fill=OL, width=18)
                d.line([pts[j], pts[j + 1]], fill=col, width=11)
            if k >= 1:
                pill(img, x1, y1 - 60, lab, bg, spring(t - T - (0.35 if side < 0 else 0.55) * (STARTS[20] - T), 13, 7), 40)
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([210, 252, 510, 308], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.text((360, 280), "PENALTIES  4 - 4", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
    return cam(img, 1 + 0.04 * u, 360, 800)


def s_choice(t, u, T):
    return s_pen(t, u, T, choice=True)


def s_end(t, u, T):
    img = s_pen(t, 1.0, T, choice=True).convert("RGB")
    img = Image.blend(img, Image.new("RGB", img.size, (10, 12, 30)), 0.55 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420, clamp(k, 0, 1.2))
    d.rounded_rectangle([60, py, 660, py + 520], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="smile", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 180, py + 330 - abs(math.sin(t * 3)) * 8)
    d.text((440, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((440, py + 150), "PART 7", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
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
        gx = lerp(760, bx + 100, ease_in_out((t - T) / 0.8)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, cc in ((230, "LEFT", C_Y), (490, "RIGHT", C_B)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 100, py + 400 - hop, x + 100, py + 470 - hop], 18, fill=(30, 36, 76), outline=cc, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 36), fill=cc, anchor="mm")
    return img


SCENES = [s_hook, s_knock, s_coach, s_walkout, s_grandad, s_strike, s_goal, s_mason, s_getup, s_header, s_1v1,
          s_mason_goal, s_board, s_fk, s_slowmo, s_finger, s_whistle, s_grandad_up, s_pen, s_choice, s_end]


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s:
            i = k
    return i


def frame(t):
    i = line_at(t)
    T = STARTS[i]
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    u = clamp((t - T) / max(0.1, end - T))
    img = SCENES[i](t, u, T).convert("RGBA")
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
