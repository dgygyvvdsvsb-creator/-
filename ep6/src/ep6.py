"""EP6 — the derby. remi_sport-style perspective match scenes."""
import os, sys, json
from persp import *
from persp import _xzy, ball_trail, pretty_arc
import build   # caption chunking + office/room helpers

PLATFORM = os.environ.get("PLATFORM", "tiktok")
EP = 6
Y, R_, B, G, O, W = C_Y, C_R, C_B, C_G, C_O, C_W
FOLLOW = "SUBSCRIBE" if PLATFORM == "youtube" else "FOLLOW"
LINES = [
    [("YOU", W), ("ASKED", W), ("FOR", W), ("THE", W), ("SHIRT.", Y)],
    [("YOU", W), ("KNOCK.", O), ("THE", W), ("COACH", W), ("LOOKS", W), ("UP.", W)],
    [("\"WEDNESDAY.", Y), ("FIRST", W), ("TEAM", W), ("AGAINST", W), ("THE", W), ("RESERVES.", B), ("PLAY", W), ("WELL...", W),
     ("YOU", W), ("START", G), ("SATURDAY.\"", Y)],
    [("MONDAY.", W), ("TRAINING.", W), ("NO", Y), ("DAYS", Y), ("OFF.", Y)],
    [("TUESDAY.", W), ("CROSSES.", B), ("YOU", W), ("CATCH", G), ("EVERY", W), ("ONE.", G)],
    [("DIXON", B), ("WATCHES.", W), ("HE", W), ("WANTS", W), ("THAT", W), ("SHIRT", Y), ("TOO.", R_)],
    [("YOU'RE", W), ("NOT", R_), ("NUMBER", W), ("ONE.", Y), ("NOT", W), ("YET.", G)],
    [("WEDNESDAY.", W), ("OKAFOR'S", Y), ("STILL", W), ("INJURED.", R_)],
    [("SO", W), ("TODAY", W), ("YOU", G), ("KEEP", G), ("FOR", W), ("THE", W), ("FIRST", Y), ("TEAM.", Y)],
    [("MINUTE", W), ("THREE.", W), ("ONE", W), ("PASS.", B), ("ONE", W), ("TOUCH.", B)],
    [("YOU", W), ("FLY...", Y), ("NOT", R_), ("ENOUGH.", R_), ("ZERO,", W), ("ONE.", R_)],
    [("MASON", R_), ("LAUGHS.", W), ("\"TOLD", W), ("YOU.\"", R_)],
    [("YOU", W), ("GET", W), ("BACK", G), ("UP.", G), ("LIKE", W), ("GRANDAD", B), ("SAID.", W)],
    [("CORNER.", W), ("HEADER.", W), ("YOU", W), ("FLY.", Y), ("SAVED!", G)],
    [("ONE", W), ("ON", W), ("ONE.", W), ("YOU", W), ("SPREAD", W), ("BIG.", Y), ("SAVED", G), ("AGAIN!", G)],
    [("THEN", W), ("MASON", R_), ("SCORES.", G), ("ONE,", W), ("ONE.", Y)],
    [("LAST", R_), ("MINUTE.", R_), ("THEIR", W), ("CAPTAIN", B), ("STEALS", R_), ("IT", W), ("FROM", W), ("MASON.", R_),
     ("FIVE", W), ("TRIPS", R_), ("HIM.", W)],
    [("YELLOW", Y), ("CARD.", Y), ("FREE", W), ("KICK.", W), ("EDGE", W), ("OF", W), ("THE", W), ("BOX.", W)],
    [("THEIR", W), ("CAPTAIN.", B), ("TOP", Y), ("CORNER.", Y)],
    [("YOU", W), ("SEE", W), ("IT", W), ("EARLY.", Y), ("YOU", W), ("PUSH", W), ("OFF.", W)],
    [("FINGERTIPS.", Y), ("CROSSBAR.", W), ("OUT!", G)],
    [("FINAL", W), ("WHISTLE.", W), ("ONE,", W), ("ONE.", Y), ("THE", W), ("COACH", W), ("WANTS", W), ("PENALTIES.", R_)],
    [("LAST", W), ("KICK.", R_), ("SAVE", G), ("IT...", W), ("AND", W), ("SATURDAY", Y), ("IS", W), ("YOURS.", Y)],
    [("LAST", W), ("TIME", W), ("HE", W), ("WENT", W), ("RIGHT.", B), ("LEFT", Y), ("OR", W), ("RIGHT?", B)],
    [("VOTE", W), ("BELOW.", G), (FOLLOW, R_), ("FOR", W), ("PART\u00a07.", Y)],
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
    """the reserves' keeper is Dixon (#2) — your rival for the shirt"""
    return dixon(**kw)


def score_state(t):
    l = 1 if t >= STARTS[15] + 0.6 * (STARTS[16] - STARTS[15]) else 0
    r = 1 if t >= STARTS[10] + 0.35 * (STARTS[11] - STARTS[10]) else 0
    return l, r


def mini_score(img, t, minute):
    l, r = score_state(t)
    d = ImageDraw.Draw(img)
    y = 290
    d.rounded_rectangle([200, y, 520, y + 56], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.rectangle([212, y + 12, 236, y + 44], fill=RS); d.rectangle([484, y + 12, 508, y + 44], fill=NF)
    d.text((360, y + 28), f"1ST  {l} - {r}  RES", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
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
    """HOOK, 3 quick shots: 1) frozen full-stretch dive, ball at the fingertips (slow-mo)
    2) whip to the score board 90' 1-1   3) the striker smashes it straight at the camera"""
    if True:                                         # the whole hook: the fingertip save in the top corner, outcome hidden
        w = u
        c = Cam(camX=1.6, camH=1.6, hor=560)
        img = backdrop(560, stadium=True)
        pitch_persp(img, c, Zgoal=6.0, box=False)
        goal3d(img, c, 6.0)
        sc = 1.6 * c.k(6.0) / 31
        sp = hero(pose="reach", gloves=True, mouth="open").resize((int(24 * sc), int(39 * sc)), Image.NEAREST).rotate(-55, expand=True, resample=Image.NEAREST)
        kx, ky = c.p(lerp(1.15, 1.3, w), 6.0, 1.15 + 0.05 * w)
        ground_shadow(img, c, 1.2, 6.0, 0.8, 70)
        img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
        bx, by = c.p(lerp(2.0, 2.15, w), lerp(5.2, 5.6, w), 1.9)
        streak = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(streak)
        for k in range(5):                           # motion streaks behind the ball
            off = (k - 2) * 9
            sd.line([(bx - 260, by + 60 + off), (bx - 20, by + off)], fill=(255, 255, 255, 120 - abs(k - 2) * 30), width=6)
        img.alpha_composite(streak)
        draw_ball(img, bx, by + 40, 3.0)
        glow_ring(img, bx, by, 80 + 12 * math.sin(t * 14), 0.75, (255, 240, 180))
        slowmo_bars(img, 1.0)
        return cam(img, 1.25 + 0.08 * w, bx - 40, by + 120, rot=-4 + 3 * w)   # frame 0: full colour, no flash
    if u < 0.55:                                     # 2) whip-pan to the clock
        w = (u - 0.42) / 0.13
        img = Image.new("RGBA", (FW, FH), (20, 22, 40, 255))
        crowd_band(img, 0, 560, seed=33, blur=1.0)
        ImageDraw.Draw(img).rectangle([0, 560, FW, FH], fill=(18, 20, 34))
        scoreboard(img, 640, "1ST", "RES", 1, 1, "90'", 1.0, t=t)
        img = cam(img, 1.3 - 0.3 * ease_out(w), 360 - 300 * (1 - ease_out(w)), 720)
        return flash(img, 0.6 * clamp(1 - w * 4))
    w = (u - 0.55) / 0.45                            # 3) shot straight at you
    img, c = keeper_view(t)
    ground_shadow(img, c, 0.4, 8.6, 0.4)
    sprite_at(img, c, opp(9, pose="kick", phase=clamp(w * 3)), 0.4, 8.6, height_m=1.55)
    pts = arc((0.2, 8.0, 0.15), (0.3, 1.5, 1.35), apex=0.6)
    a = clamp(0.15 + ease_in_out(w) * 0.85)
    ball_trail(img, c, pts, a, 0.2)
    bx, by = ball_at(img, c, *at(pts, a))
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    if a > 0.85:
        glow_ring(img, bx, by, 160, 0.6, (255, 250, 220))
    img = flash(img, 0.7 * clamp((a - 0.93) / 0.07))
    return cam(img, 1.0 + 0.12 * w, bx, by, *shake(t, T + 0.62 * (STARTS[1] - T), .3, 10))


def tactics_board(img, x0, y0, w, h, t=0):
    """whiteboard with a mini pitch, X / O and arrows"""
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(246, 246, 240), outline=(120, 124, 140), width=8)
    px0, py0, px1, py1 = x0 + 18, y0 + 18, x0 + w - 18, y0 + h - 18
    d.rectangle([px0, py0, px1, py1], fill=(70, 150, 76), outline=(250, 250, 250), width=3)
    my = (py0 + py1) / 2
    d.line([(px0, my), (px1, my)], fill=(250, 250, 250), width=3)
    d.ellipse([(px0 + px1) / 2 - 20, my - 20, (px0 + px1) / 2 + 20, my + 20], outline=(250, 250, 250), width=3)
    for yy in (py0, py1):
        sg = 1 if yy == py0 else -1
        d.rectangle(sorted_box((px0 + px1) / 2 - 45, yy, (px0 + px1) / 2 + 45, yy + sg * 32), outline=(250, 250, 250), width=3)
    f = font(800, 22)
    for fx, fy in ((0.2, 0.62), (0.4, 0.66), (0.6, 0.66), (0.8, 0.62), (0.35, 0.78), (0.65, 0.78), (0.5, 0.92)):
        d.text((lerp(px0, px1, fx), lerp(py0, py1, fy)), "O", font=f, fill=(210, 52, 56), anchor="mm")
    for fx, fy in ((0.3, 0.3), (0.5, 0.25), (0.7, 0.3), (0.5, 0.12)):
        d.text((lerp(px0, px1, fx), lerp(py0, py1, fy)), "X", font=f, fill=(30, 40, 90), anchor="mm")
    for (ax, ay), (bx, by) in (((0.35, 0.78), (0.3, 0.45)), ((0.65, 0.78), (0.75, 0.45))):
        a_ = (lerp(px0, px1, ax), lerp(py0, py1, ay)); b_ = (lerp(px0, px1, bx), lerp(py0, py1, by))
        d.line([a_, b_], fill=(250, 206, 40), width=4)
        d.polygon([b_, (b_[0] - 8, b_[1] + 12), (b_[0] + 8, b_[1] + 12)], fill=(250, 206, 40))
    d.rectangle([x0 + 20, y0 + h + 4, x0 + w - 20, y0 + h + 14], fill=(150, 150, 160))   # marker tray
    d.rectangle([x0 + 40, y0 + h, x0 + 80, y0 + h + 6], fill=(210, 52, 56))


def office(t):
    """coach's office: window onto the pitch behind the desk, tactics board on the right"""
    img = Image.new("RGBA", (FW, FH), (204, 188, 160, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, 760, 44):
        d.line([(0, y), (FW, y)], fill=(194, 178, 150), width=2)
    for r in range(14):                                   # wooden floor in perspective
        y0 = 760 + (r ** 1.35) * 14
        d.rectangle([0, y0, FW, 760 + ((r + 1) ** 1.35) * 14], fill=(150, 104, 66) if r % 2 else (138, 94, 58))
    d.rectangle([0, 752, FW, 762], fill=(120, 84, 52))
    # window with the training pitch outside (sky, trees, pitch, a goal)
    wx0, wy0, wx1, wy1 = 60, 190, 420, 520
    sky = Image.new("RGB", (wx1 - wx0, wy1 - wy0))
    sd = ImageDraw.Draw(sky)
    for y in range(wy1 - wy0):
        sd.line([(0, y), (wx1 - wx0, y)], fill=tuple(int(lerp(a_, b_, y / (wy1 - wy0))) for a_, b_ in zip((130, 170, 220), (230, 200, 150))))
    sd.ellipse([-40, 120, 420, 230], fill=(54, 100, 58))
    sd.rectangle([0, 170, wx1 - wx0, wy1 - wy0], fill=(76, 156, 74))
    for k in range(5):
        sd.rectangle([0, 190 + k * 30, wx1 - wx0, 205 + k * 30], fill=(68, 144, 66))
    sd.line([(0, 250), (wx1 - wx0, 230)], fill=(240, 244, 236), width=3)
    sd.rectangle([230, 176, 320, 214], outline=(250, 250, 252), width=4)
    img.paste(sky, (wx0, wy0))
    d.rectangle([wx0 - 10, wy0 - 10, wx1 + 10, wy1 + 10], outline=(250, 250, 250), width=12)
    d.line([((wx0 + wx1) / 2, wy0), ((wx0 + wx1) / 2, wy1)], fill=(250, 250, 250), width=8)
    d.rectangle([wx0 - 20, wy1 + 8, wx1 + 20, wy1 + 22], fill=(240, 240, 240), outline=OL, width=3)   # sill
    tactics_board(img, 450, 200, 250, 330, t)
    # trophy + clock
    d.rectangle([600, 120, 650, 170], fill=(250, 250, 250), outline=OL, width=4)
    d.line([(625, 145), (625, 128)], fill=OL, width=3); d.line([(625, 145), (638, 150)], fill=OL, width=3)
    return img


def desk_and_coach(img, t, look=0, talk=False, blink=False):
    """coach sits behind the desk: only his upper body shows above it"""
    bare = person(Kit((30, 40, 80), (30, 40, 80), (30, 30, 36)), skin="light", hair="grey", style="short",
                  pose="sit", look=look, mouth="open" if talk else "flat", blink=blink)   # cap is off, on the desk
    paste(img, bare, 16, 250, 1000)
    d = ImageDraw.Draw(img)
    d.rectangle([20, 820, 520, 1030], fill=(118, 78, 48), outline=OL, width=7)     # desk front, down to the floor
    d.rectangle([60, 860, 480, 990], outline=(96, 62, 38), width=5)                # panel detail
    d.rectangle([20, 800, 520, 830], fill=(140, 96, 60), outline=OL, width=6)      # desk top
    d.rectangle([200, 782, 290, 804], fill=(250, 246, 236), outline=OL, width=3)   # papers
    # his cap on the desk, head-sized: crown dome + brim pointing at us
    NAVY, NAVY_D = (34, 46, 96), (22, 30, 66)
    d.chord([40, 782, 200, 814], 0, 180, fill=NAVY_D, outline=OL, width=4)    # brim (drawn first)
    d.chord([50, 748, 180, 844], 180, 360, fill=NAVY, outline=OL, width=4)    # crown sits ON the brim (no gap)
    d.rectangle([54, 794, 176, 798], fill=NAVY)                               # hides the seam line
    d.line([(115, 752), (115, 792)], fill=NAVY_D, width=3)
    d.rectangle([106, 762, 124, 776], fill=(250, 206, 40), outline=OL, width=2)
    d.rectangle([300, 770, 360, 804], fill=(250, 250, 250), outline=OL, width=3)   # mug
    d.text((330, 788), "R", font=font(800, 18), fill=(210, 52, 56), anchor="mm")
    d.rectangle([400, 760, 470, 804], fill=(40, 44, 60), outline=OL, width=3)      # clipboard
    d.rectangle([410, 770, 460, 798], fill=(250, 246, 236))


def corridor(t):
    img = Image.new("RGBA", (FW, FH), (190, 198, 214, 255))
    d = ImageDraw.Draw(img)
    for r in range(14):
        y0 = 820 + (r ** 1.35) * 12
        d.rectangle([0, y0, FW, 820 + ((r + 1) ** 1.35) * 12], fill=(160, 164, 180) if r % 2 else (150, 154, 170))
    d.rectangle([0, 812, FW, 822], fill=(120, 124, 140))
    for x in (40, 600):   # team photos on the wall
        d.rectangle([x, 300, x + 90, 380], fill=(250, 250, 250), outline=OL, width=4)
        for k in range(4):
            d.rectangle([x + 12 + k * 18, 340, x + 24 + k * 18, 370], fill=(210, 52, 56))
    return img


def s_knock(t, u, T):
    if u < 0.5:   # outside: you knock on the coach's door
        img = corridor(t)
        d = ImageDraw.Draw(img)
        d.rectangle([220, 220, 500, 820], fill=(150, 100, 60), outline=OL, width=7)
        d.rectangle([240, 240, 480, 520], outline=(120, 80, 46), width=5)
        d.ellipse([450, 520, 476, 546], fill=C_Y, outline=OL, width=3)
        d.rectangle([290, 270, 430, 320], fill=(250, 246, 236), outline=OL, width=4)
        d.text((360, 295), "COACH", font=font(800, 30), fill=OL, anchor="mm")
        paste(img, hero(view="back", gloves=False), 14, 360, 1460)
        for k in range(3):
            impact_lines(img, 330, 600, T + 0.12 + k * 0.25, t, 8)
        return cam(img, 1 + 0.06 * u, 360, 600)
    # inside: we look over your shoulder from the doorway — you walk in FRONT of the desk, the coach looks up
    img = office(t)
    desk_and_coach(img, t, look=0, blink=u < 0.62)
    d = ImageDraw.Draw(img)
    k = ease_out((u - 0.5) / 0.3)
    # door frame around the camera (we are standing in the doorway)
    d.rectangle([0, 0, 46, FH], fill=(120, 80, 46), outline=OL, width=6)
    d.rectangle([FW - 46, 0, FW, FH], fill=(120, 80, 46), outline=OL, width=6)
    d.rectangle([0, 0, FW, 40], fill=(120, 80, 46), outline=OL, width=6)
    # the opened door swings to the left, close to camera
    dw = 260 * (1 - k) + 70 * k
    d.polygon([(46, 40), (46 + dw, 70), (46 + dw, FH - 20), (46, FH)], fill=(150, 100, 60), outline=OL)
    # you step in: back view, walking forward toward the desk
    step = ease_out((u - 0.5) / 0.5)
    sc_ = int(lerp(17, 13, step))
    paste(img, hero(view="back", pose="run" if step < 0.9 else "stand", phase=t * 1.6), sc_, 430, int(lerp(1500, 1330, step)))
    return cam(img, 1.0 + 0.03 * u, 360, 760)


def s_coach(t, u, T):
    img = office(t)
    desk_and_coach(img, t, look=1, talk=int(t * 7) % 2 == 0, blink=0.62 < u < 0.68)
    return cam(img, 1.25 + 0.05 * u, 280, 720)


def s_walkout(t, u, T):
    """aerial view of the whole pitch: 11 v 11 in formation, you in Riverside's goal"""
    img = Image.new("RGBA", (FW, FH), (36, 40, 66, 255))
    crowd_band(img, 0, FH, seed=44, blur=2.0)
    X0, X1, Y0, Y1 = 50, 670, 300, 1200           # pitch rectangle
    d = ImageDraw.Draw(img)
    d.rectangle([X0 - 16, Y0 - 16, X1 + 16, Y1 + 16], fill=(52, 120, 56))
    for i in range(12):                              # mowing stripes
        y = Y0 + i * (Y1 - Y0) / 12
        d.rectangle([X0, y, X1, y + (Y1 - Y0) / 12], fill=GRASS_A if i % 2 else GRASS_B)
    W_, H_ = X1 - X0, Y1 - Y0
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    L = dict(fill=LINE, width=4)
    d.rectangle([X0, Y0, X1, Y1], outline=LINE, width=4)
    d.line([(X0, cy), (X1, cy)], **L)
    d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], outline=LINE, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=LINE)
    for top in (True, False):
        yb = Y0 if top else Y1
        sg = 1 if top else -1
        d.rectangle(sorted_box(cx - 170, yb, cx + 170, yb + sg * 150), outline=LINE, width=4)    # penalty box
        d.rectangle(sorted_box(cx - 75, yb, cx + 75, yb + sg * 55), outline=LINE, width=4)       # 6-yard box
        d.ellipse([cx - 5, yb + sg * 105 - 5, cx + 5, yb + sg * 105 + 5], fill=LINE)
        d.arc([cx - 80, yb + sg * 105 - 80, cx + 80, yb + sg * 105 + 80], 35 if top else 215, 145 if top else 325, fill=LINE, width=4)
        d.rectangle(sorted_box(cx - 55, yb, cx + 55, yb - sg * 22), fill=(245, 245, 250), outline=OL, width=3)   # goal
    # formations (4-4-2), positions in pitch fractions (x 0..1, y 0..0.5 from own goal line)
    # Riverside 4-3-3, Northfield 4-1-2-1-2 (diamond)
    shapes = {
        "RIV": [(0.5, 0.045)] + [(x, 0.17) for x in (0.13, 0.37, 0.63, 0.87)] + [(x, 0.30) for x in (0.25, 0.5, 0.75)]
               + [(0.16, 0.42), (0.5, 0.445), (0.84, 0.42)],
        "NOR": [(0.5, 0.045)] + [(x, 0.17) for x in (0.13, 0.37, 0.63, 0.87)] + [(0.5, 0.25), (0.27, 0.32), (0.73, 0.32), (0.5, 0.38)]
               + [(0.36, 0.445), (0.64, 0.445)],
    }
    nums_r = [0, 2, 5, 4, 3, 6, 8, 10, 7, 9, 11]
    nums_n = [1, 2, 5, 4, 3, 6, 8, 7, 10, 9, 11]
    k = ease_out(u * 1.6)
    for team in ("NOR", "RIV"):
        for i, (fx, fy) in enumerate(shapes[team]):
            px = X0 + fx * W_
            if team == "RIV":                      # bottom half, our goal at the bottom
                py = Y1 - fy * H_
                # camera is behind our goal: we see Riverside from behind (numbers on the backs)
                if i == 0:
                    sp = hero(view="back", pose="ready", gloves=True)
                elif nums_r[i] == 9:
                    sp = mason(view="back")
                else:
                    sp = ours(nums_r[i], view="back")
            else:
                py = Y0 + fy * H_
                sp = opp_keeper() if i == 0 else opp(nums_n[i])
            py_in = lerp(cy + (40 if team == "RIV" else -40), py, k)     # players spread out to their places
            px_in = lerp(cx, px, k)
            shadow(img, px_in, py_in + 4, 40, 10, 80)
            paste(img, sp, 2, px_in, py_in + 6)
    # highlight: you, in goal
    hx, hy = cx, Y1 - 0.035 * H_
    if u > 0.45:
        ring = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse([hx - 34, hy - 6, hx + 34, hy + 16], outline=C_G + (230,), width=5)   # ring on the grass under his feet
        img.alpha_composite(ring)
    pill(img, 360, 1250, "FIRST TEAM vs RESERVES", (14, 16, 30), spring(t - T - 0.2, 13, 7), 26)
    return cam(img, 1 + 0.12 * ease_in_out(clamp((u - 0.5) / 0.5)), 360, 1180)


def sorted_box(x0, y0, x1, y1):
    return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]


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
        impact_lines(img, *c.p(0.15, 18, 0.3), T + 0.35 * (STARTS[11] - STARTS[10]), t, 10)
    striker = opp(9, view="back", pose="kick" if u > kick - 0.1 else "run", phase=clamp((u - kick + 0.1) / 0.2) if u > kick - 0.1 else t * 2)
    paste(img, striker, 11, 250, 1420)
    mini_score(img, t, "3'")
    if goal_:
        img = flash(img, 0.35 * clamp(1 - abs(u - 0.37) * 8), (255, 50, 50))
    return cam(img, 1 + (0.05 * u if not goal_ else 0.12), *c.p(0, 17, 0.8), *shake(t, T + 0.37 * (STARTS[11] - STARTS[10]), .3, 10) if goal_ else (0, 0))


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
    pitch_persp(img, c, Zgoal=10.0)
    goal3d(img, c, 10.0)
    if u < 0.45:
        draw_ball(img, *c.p(1.2, 10.9, 0), 1.0)
        sp_s = 1.6 * c.k(9.9) / 31
        sp = hero(pose="reach", gloves=True, blink=True).resize((int(24 * sp_s), int(39 * sp_s)), Image.NEAREST).rotate(90, expand=True, resample=Image.NEAREST)
        x, y = c.p(0.2, 9.9)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * sp_s)))
    else:
        ground_shadow(img, c, 0, 9.9, 0.5)
        k = ease_out((u - 0.45) / 0.25)
        sprite_at(img, c, hero(gloves=True, mouth="flat"), 0, 9.9, Y=-0.4 * (1 - k), height_m=1.6)
        draw_ball(img, *c.p(1.2, 10.9, 0), 1.0)
        glow_ring(img, *c.p(0, 9.9, 1.0), 120 * k, 0.4 * k, (255, 240, 180))
    return cam(img, 1 + 0.05 * u, 360, 900)


def s_header(t, u, T):
    img, c = shooter_view(t, 11, camX=-0.5, camH=2.2, hor=470)
    goal3d(img, c, 11)
    cross = arc((-14, 9.5, 0.3), (1.8, 8.6, 2.0), apex=3.5)
    head = arc((1.8, 8.6, 2.0), (-2.0, 11.0, 1.7), apex=0.3)
    jump = math.sin(clamp((u - 0.25) / 0.35) * math.pi) * 0.55
    ground_shadow(img, c, 1.8, 8.6, 0.35)
    sprite_at(img, c, opp(5, view="back", pose="celebrate" if jump > 0.1 else "stand"), 1.8, 8.6, Y=jump, height_m=1.55)
    phase = clamp((u - 0.38) / 0.62)
    gx, gy = keeper_world(img, c, 0, 11, -1, phase)
    if u < 0.4:
        a = u / 0.4
        dotted_path(img, c, cross, 1.0, from_=a)
        ball_trail(img, c, cross, a, 0.1)
        ball_at(img, c, *at(cross, a))
    elif phase < 0.33:
        a = clamp((u - 0.4) / 0.2)
        ball_trail(img, c, head, a, 0.25)
        ball_at(img, c, *at(head, a))
        impact_lines(img, *c.p(1.8, 8.6, 2.1), T + 0.4 * (STARTS[14] - T), t, 8)
    else:
        draw_ball(img, gx, gy + 12, 0.9)
        if phase < 0.45:
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
    return cam(img, 1 + 0.04 * u, 360, 800, *shake(t, T + 0.75 * (STARTS[15] - T), .3, 12))


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
        impact_lines(img, x, y, T + (kick + 0.3) * (STARTS[16] - T), t, 10)
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
    scoreboard(img, 640, "1ST", "RES", l, r, "90'", spring(t - T, 12, 7), t=t)
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
        impact_lines(img, *c.p(2.25, 6.0, 2.0), T + hit * (STARTS[21] - T), t, 12)
        glow_ring(img, *c.p(2.25, 6.0, 2.0), 60 + 160 * clamp((u - hit) * 3), 0.9 * (1 - clamp((u - hit) * 2)), (255, 255, 210))
    slowmo_bars(img, 1 - ease_out((u - hit) * 3) if u > hit else 1)
    img = flash(img, 0.45 * clamp(1 - abs(u - hit) * 14))
    return cam(img, 1.05, 420, 720, *shake(t, T + hit * (STARTS[21] - T), .35, 14))


def s_whistle(t, u, T):
    img = Image.new("RGBA", (FW, FH), (24, 26, 44, 255))
    crowd_band(img, 0, 560, seed=34, blur=1.0)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(18, 20, 34))
    scoreboard(img, 640, "1ST", "RES", 1, 1, "FULL TIME", 1.0, t=t)
    if u > 0.55:
        pill(img, 360, 1000, "SHOOTOUT", (200, 40, 50), spring(t - T - 0.55 * (STARTS[22] - T), 13, 7), 56)
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
                pill(img, x1, y1 - 60, lab, bg, spring(t - T - (0.35 if side < 0 else 0.55) * (STARTS[24] - T), 13, 7), 40)
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([210, 252, 510, 308], 12, fill=(14, 16, 30), outline=OL, width=4)
    d.text((360, 280), "SHOOTOUT · LAST KICK", font=font(800, 26), fill=(255, 255, 255), anchor="mm")
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


def s_training(t, u, T):
    """Monday training: cones, bibs, you dive and CATCH, then land"""
    img, c = shooter_view(t, 8.5, camH=2.2, hor=470, stadium=False)
    goal3d(img, c, 8.5)
    d = ImageDraw.Draw(img)
    for X, Z in ((-5, 4), (-2.5, 3.5), (2.5, 3.5), (5, 4)):     # cones
        x, y = c.p(X, Z); r = 0.18 * c.k(Z)
        d.polygon([(x - r, y), (x + r, y), (x, y - r * 2.2)], fill=(252, 140, 27), outline=OL)
    k = int(u * 3); phase = (u * 3) % 1
    side = 1 if k % 2 else -1
    gx, gy = keeper_world(img, c, 0, 8.5, side, phase)
    shot = arc((-0.05, 2.4, 0.0), (side * 1.5, 8.5, 0.95), apex=0.45)   # starts at Dixon's boot
    if phase < 0.33:                                       # fast shot, arrives at full stretch
        a = phase / 0.33
        ball_trail(img, c, shot, a, 0.15)
        ball_at(img, c, *at(shot, a))
    else:
        draw_ball(img, gx, gy + 14, 0.16 * c.k(8.5) / 6.5)
        if phase < 0.42:
            glow_ring(img, gx, gy, 55, 0.8, (255, 255, 210))       # caught: same size as in flight at the goal
    ground_shadow(img, c, -3.6, 7.2, 0.4)
    sprite_at(img, c, coach(look=1), -3.6, 7.2, height_m=1.75)   # beside the goal, watching
    paste(img, dixon(view="back", pose="kick" if phase < 0.25 else "stand", phase=clamp(phase / 0.2), gloves=False), 11, 300, 1330)  # Dixon takes the shots
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([200, 252, 520, 308], 12, fill=(14, 16, 30), outline=C_Y, width=4)
    d.text((360, 280), f"CATCHES {int(1 + 60 * u)}", font=font(800, 28), fill=C_Y, anchor="mm")
    return cam(img, 1 + 0.03 * u, 360, 700)


def s_notyet(t, u, T):
    """locker room: the yellow #1 shirt on its hook; you look at it from behind"""
    img = build.room_set("locker6", wall=(110, 130, 170), floor=((150, 150, 170), (140, 140, 160))).copy()
    d = ImageDraw.Draw(img)
    for i in range(5):                                         # lockers
        x = 20 + i * 140
        if i == 2:
            continue
        d.rectangle([x, 160, x + 130, 760], fill=(70, 90, 140), outline=OL, width=5)
        for yy in (250, 280):
            d.line([(x + 30, yy), (x + 100, yy)], fill=(50, 66, 110), width=4)
    # the middle locker is open: dark inside, door swung to the right, the #1 shirt on a hanger inside
    x = 300
    d.rectangle([x, 160, x + 130, 760], fill=(30, 34, 52), outline=OL, width=5)
    d.polygon([(x + 130, 160), (x + 190, 140), (x + 190, 780), (x + 130, 760)], fill=(84, 106, 160), outline=OL)
    d.line([(x + 10, 230), (x + 120, 230)], fill=(170, 170, 180), width=6)          # rail
    d.rectangle([x + 4, 640, x + 126, 650], fill=(60, 64, 84))                     # shelf
    d.rectangle([x + 20, 610, x + 70, 640], fill=(252, 140, 27), outline=OL, width=3)  # spare gloves on the shelf
    cx, cy = x + 65, 400 + math.sin(t * 2) * 2
    glow_ring(img, cx, cy, 90, 0.35 + 0.15 * math.sin(t * 4), (255, 230, 120))
    d = ImageDraw.Draw(img)
    s_ = 8
    d.line([(cx, 230), (cx, cy - 3 * s_)], fill=(200, 200, 210), width=4)          # hanger hook
    d.line([(cx - 8 * s_, cy - 2 * s_), (cx, cy - 4 * s_), (cx + 8 * s_, cy - 2 * s_)], fill=(200, 200, 210), width=5)
    body = [(cx - 6 * s_, cy - 3 * s_), (cx - 11 * s_, cy), (cx - 9 * s_, cy + 3 * s_), (cx - 6 * s_, cy + 2 * s_),
            (cx - 6 * s_, cy + 9 * s_), (cx + 6 * s_, cy + 9 * s_), (cx + 6 * s_, cy + 2 * s_), (cx + 9 * s_, cy + 3 * s_),
            (cx + 11 * s_, cy), (cx + 6 * s_, cy - 3 * s_), (cx + 2 * s_, cy - 3 * s_), (cx, cy - 1 * s_), (cx - 2 * s_, cy - 3 * s_)]
    d.polygon(body, fill=(246, 206, 40), outline=OL, width=4)
    d.text((cx, cy + 4 * s_), "1", font=font(800, 64), fill=OL, anchor="mm")
    d.rectangle([0, 760, FW, 800], fill=(150, 100, 60), outline=OL, width=5)   # bench
    paste(img, hero(view="back", gloves=True), 15, 360, 1500)
    return cam(img, 1 + 0.05 * u, 365, 560)


def s_okafor(t, u, T):
    """Okafor on the bench, ice on his knee; the kit bag with the keeper gloves"""
    img, c = shooter_view(t, 30, camH=1.7, hor=520)
    d = ImageDraw.Draw(img)
    d.rectangle([60, 900, 660, 940], fill=(150, 100, 60), outline=OL, width=6)      # bench
    for x in (90, 610):
        d.rectangle([x, 940, x + 24, 1060], fill=(110, 70, 40), outline=OL, width=5)
    paste(img, okafor(pose="sit", mouth="sad", blink=int(t * 2) % 5 == 0, gloves=False), 9, 300, 1000)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([248, 896, 300, 930], 10, fill=(170, 220, 250), outline=OL, width=4)   # ice pack on the knee
    # crutches leaning on the bench
    for dx in (0, 22):   # crutches leaning on the bench, on Okafor's other side
        d.line([(150 + dx, 1060), (180 + dx, 700)], fill=OL, width=14)
        d.line([(150 + dx, 1060), (180 + dx, 700)], fill=(180, 180, 190), width=8)
    paste(img, hero(gloves=True, look=-1), 9, 560, 1060)
    return cam(img, 1 + 0.05 * u, 360, 860)


def _lin(keys, v):
    """piecewise-linear interpolation of (v, (X, Z)) keyframes"""
    if v <= keys[0][0]:
        return keys[0][1]
    for (v0, p0), (v1, p1) in zip(keys, keys[1:]):
        if v0 <= v <= v1:
            f = ease_in_out((v - v0) / max(1e-6, v1 - v0))
            return tuple(lerp(a, b, f) for a, b in zip(p0, p1))
    return keys[-1][1]


def shot_reverse(t, w, t_hit):
    """EPIC: camera behind our net, low. Keeper's back fills the frame, #9 strikes,
    the ball comes at us in slow motion between his legs and bulges the net."""
    c = Cam(camX=0.6, camH=1.05, hor=600)
    img = backdrop(600, stadium=True)
    pitch_persp(img, c, None)
    d = ImageDraw.Draw(img)
    for (X0, Z0, X1, Z1) in ((-30, 4.3, 30, 4.3), (-6, 4.3, -6, 8.3), (6, 4.3, 6, 8.3), (-6, 8.3, 6, 8.3), (-14, 15.3, 14, 15.3)):
        pts = [c.p(lerp(X0, X1, i / 20), lerp(Z0, Z1, i / 20)) for i in range(21)]
        d.line(pts, fill=LINE, width=max(2, int(0.07 * c.k((Z0 + Z1) / 2))))
    kick = 0.18
    # #9 strikes from the edge of the box
    ground_shadow(img, c, 1.3, 11.0, 0.4)
    sprite_at(img, c, opp(9, pose="kick" if w > kick - 0.08 else "run", phase=clamp((w - kick + 0.08) / 0.1) if w > kick - 0.08 else t * 2.6), 1.3, 11.0, height_m=1.55)
    # slow motion: the ball travels its path slowly, fast again at the end
    a = 0.0 if w < kick else clamp(((w - kick) / (0.72 - kick)) ** 1.6)
    path = arc((1.0, 10.7, 0.1), (0.0, 2.6, 0.22), apex=0.12)
    if a < 1:
        dotted_path(img, c, path, 1.0, from_=a)
    # keeper: back view, legs apart, on the goal line between the posts
    ground_shadow(img, c, 0, 4.6, 0.5)
    ball_first = at(path, a)[1] > 4.6
    if ball_first and a > 0:
        ball_trail(img, c, path, a, 0.1)
        ball_at(img, c, *at(path, a))
    sprite_at(img, c, hero(view="back", pose="ready", gloves=True), 0, 4.6, height_m=1.6)
    if not ball_first and a < 0.97:
        ball_trail(img, c, path, a, 0.1)
        bx, by = ball_at(img, c, *at(path, min(a, 0.97)), shadow_=False)
    # goal frame around us (we are behind the net)
    pl, pr = c.p(-2.5, 4.3), c.p(2.5, 4.3)
    tl, tr = c.p(-2.5, 4.3, 2.0), c.p(2.5, 4.3, 2.0)
    for a_, b_ in ((pl, tl), (pr, tr), (tl, tr)):
        d = ImageDraw.Draw(img)
        d.line([a_, b_], fill=OL, width=30); d.line([a_, b_], fill=(250, 250, 252), width=22)
    bul = None
    if a >= 0.97:
        bul = (*c.p(0.0, 2.6, 0.22), clamp((w - 0.72) / 0.06))
    import build as _b
    net = Image.new("RGBA", img.size, (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    cell = 46

    def disp(x, y):
        if not bul:
            return x, y
        bx_, by_, k = bul
        dx, dy = x - bx_, y - by_
        r = math.hypot(dx, dy) + 1e-3
        f = k * 70 * math.exp(-(r / 230) ** 2)
        return x - dx / r * f * 0.2, y - dy / r * f * 0.2 + f * 0.4
    for kk in range(-30, 50):
        p1 = [disp(kk * cell + j * cell, j * cell) for j in range(-2, 32)]
        p2 = [disp(kk * cell - j * cell, j * cell) for j in range(-2, 32)]
        nd.line(p1, fill=(240, 244, 250, 90), width=3)
        nd.line(p2, fill=(240, 244, 250, 90), width=3)
    img.alpha_composite(net)
    if bul:
        draw_ball(img, bul[0], bul[1] + 50, 3.2)
        impact_lines(img, bul[0], bul[1], t_hit, t, 14)
    slowmo_bars(img, 1.0 if 0.1 < w < 0.75 else 0.0)
    img = flash(img, 0.45 * clamp(1 - abs(w - 0.75) * 10), (255, 50, 50))
    mini_score(img, t, "3'")
    zoom = 1.0 + 0.12 * ease_in_out(clamp(w / 0.7))
    return cam(img, zoom, 330, 820, *shake(t, t_hit, .35, 14))


def s_attack(t, u, T):
    """lines 7+8 as ONE continuous move: one-two around our two defenders, low shot through your legs, goal"""
    A0, A1 = STARTS[9], STARTS[11]
    v = clamp((t - A0) / (A1 - A0))
    vs = clamp((STARTS[10] - A0) / (A1 - A0) - 0.03)        # the shot lands on "THROUGH YOUR LEGS"
    GZ = 22.0
    p7 = [(0.0, (-1.3, 7.5)), (0.20, (-1.3, 9.5)), (0.42, (-1.1, 12.0)), (0.52, (-0.9, 13.4)), (1.0, (-0.8, 15.5))]
    p9 = [(0.0, (1.5, 9.0)), (0.22, (1.8, 10.2)), (0.40, (1.8, 12.5)), (0.55, (0.9, 14.5)), (vs - 0.08, (0.5, 16.0)), (1.0, (0.4, 16.8))]
    d4 = [(0.0, (-0.9, 14.0)), (0.45, (-1.1, 12.9)), (0.6, (-1.6, 12.4)), (1.0, (-1.7, 12.0))]     # beaten by the one-two
    d5 = [(0.0, (1.4, 14.0)), (0.30, (1.6, 12.6)), (0.38, (2.0, 12.3)), (1.0, (2.4, 11.9))]        # beaten by the dribble
    # ball: with #7 -> pass to #9 -> dribble -> back to #7 -> through ball to #9 -> shot
    b7 = lambda vv: (_lin(p7, vv)[0] + 0.42, _lin(p7, vv)[1] + 0.15)
    b9 = lambda vv: (_lin(p9, vv)[0] - 0.42, _lin(p9, vv)[1] + 0.15)
    passes = [(0.17, 0.25, b7, b9), (0.42, 0.50, b9, b7), (0.53, 0.60, b7, b9)]
    owner = None
    ball = None
    if v < 0.17:
        ball = b7(v)
    elif v < 0.25:
        f = (v - 0.17) / 0.08; ball = tuple(lerp(a, b, f) for a, b in zip(b7(0.17), b9(0.25)))
    elif v < 0.42:
        ball = b9(v)
    elif v < 0.50:
        f = (v - 0.42) / 0.08; ball = tuple(lerp(a, b, f) for a, b in zip(b9(0.42), b7(0.50)))
    elif v < 0.53:
        ball = b7(v)
    elif v < 0.60:
        f = (v - 0.53) / 0.07; ball = tuple(lerp(a, b, f) for a, b in zip(b7(0.53), b9(0.60)))
    elif v < vs:
        ball = b9(v)
    shot = arc((b9(vs)[0], b9(vs)[1], 0.1), (0.05, GZ + 0.6, 0.18), apex=0.05)
    if vs - 0.05 <= v < vs + 0.24:
        return shot_reverse(t, (v - (vs - 0.05)) / 0.29, A0 + (vs + 0.13) * (A1 - A0))
    # camera follows the move
    cz = lerp(0.0, 7.0, ease_in_out(clamp(v / vs)))
    cx = lerp(0.0, 0.5, clamp(v / vs))
    c = Cam(camX=cx, camH=2.4, hor=440)
    img = backdrop(440, stadium=True)

    class Shift:  # world shift so the camera can move forward
        def __init__(s_, c_, z): s_.c, s_.z = c_, z
        def p(s_, X, Z, Y=0.0): return s_.c.p(X, Z - s_.z, Y)
        def k(s_, Z): return s_.c.k(Z - s_.z)
        hor = 440
    sc = Shift(c, cz)
    pitch_persp(img, sc, Zgoal=GZ)
    goal3d(img, sc, GZ)
    after = v >= vs
    # our keeper on the goal line
    ground_shadow(img, sc, 0, GZ, 0.45)
    sprite_at(img, sc, hero(pose="ready" if not after or v < vs + 0.12 else "stand", gloves=True, mouth="open" if after else "flat"), 0, GZ, height_m=1.6)
    # draw far to near
    ppl = []
    for keys, sp_fn in ((d4, lambda: ours(4, pose="run", phase=t * 2.4)), (d5, lambda: ours(5, pose="run", phase=t * 2.4)),
                        (p7, lambda: opp(7, view="back", pose="run", phase=t * 2.6)), (p9, lambda: opp(9, view="back", pose="kick" if abs(v - vs) < 0.05 else "run", phase=clamp((v - vs + 0.05) / 0.06) if abs(v - vs) < 0.05 else t * 2.6))):
        X, Z = _lin(keys, v)
        ppl.append((Z, X, sp_fn))
    for Z, X, sp_fn in sorted(ppl, key=lambda q: -q[0]):
        if Z - cz < 0.8:
            continue
        ground_shadow(img, sc, X, Z, 0.35)
        sprite_at(img, sc, sp_fn(), X, Z, height_m=1.55)
    # tactical overlay: rings under the two attackers, dashed pass line for the next pass
    if not after:
        for keys in (p7, p9):
            X, Z = _lin(keys, v)
            ring_on_grass(img, sc, X, Z, 0.55, C_Y, 3)
        for (v0, v1, fa, fb) in passes:
            if v0 - 0.07 <= v < v1:
                path = [(fa(v0)[0], fa(v0)[1], 0.05), (fb(v1)[0], fb(v1)[1], 0.05)]
                dotted_path(img, sc, arc(path[0], path[1], apex=0.0), 1.0, from_=clamp((v - v0) / (v1 - v0)))
        if 0.28 <= v < 0.42:   # dribble arrow around #5
            pts = [sc.p(1.8 + 0.8 * math.sin(a * math.pi), lerp(10.4, 13.2, a)) for a in np.linspace(0, 1, 16)]
            dd = ImageDraw.Draw(img)
            for j in range(0, 15, 2):
                dd.line([pts[j], pts[j + 1]], fill=OL, width=9); dd.line([pts[j], pts[j + 1]], fill=C_Y, width=5)
        if ball:
            ball_at(img, sc, ball[0], ball[1], 0.11)
        if vs - 0.1 <= v:
            dotted_path(img, sc, shot, 1.0, from_=0.0)
    else:
        a = clamp((v - vs) / 0.12)
        if a < 1:
            ball_trail(img, sc, shot, a, 0.12)
            ball_at(img, sc, *at(shot, a))
        else:
            b = clamp((v - vs - 0.12) / 0.2)
            x, y = sc.p(0.05, GZ + 1.0, 0.18 * (1 - b))
            draw_ball(img, x, y + 6, 0.55)
            impact_lines(img, x, y, A0 + (vs + 0.12) * (A1 - A0), t, 10)
    mini_score(img, t, "3'")
    if after:
        img = flash(img, 0.35 * clamp(1 - abs(v - vs - 0.12) * 10), (255, 50, 50))
    zoom = 1.0 + 0.25 * ease_in_out(clamp((v - vs + 0.05) / 0.15))
    kx, ky = sc.p(0, GZ, 0.8)
    return cam(img, zoom, kx, ky, *shake(t, A0 + (vs + 0.12) * (A1 - A0), .3, 10))


def s_attackA(t, u, T):
    """lines 7+8: pass, first-time curler into the top corner, full-stretch dive falls short"""
    import attack2
    A0, A1 = STARTS[9], STARTS[11]
    w = clamp((t - A0) / (A1 - A0))
    img = attack2.variant_A(t, w).convert("RGBA")
    mini_score(img, t, "3'")
    return img



# ---------------- free kick through the keeper's eyes
FKP = (-3.2, 16.6)                        # ball spot (their #10 behind it)
FK_EYES = arc((-3.2, 16.2, 0.1), (-2.3, 2.6, 1.9), apex=2.0, curve=0.9)   # over the wall, toward your top-right corner


def eyes_gloves(img, push=0.0, t=0.0):
    """your own gloves at the bottom of the frame (first person). push 0 ready .. 1 flying to the right"""
    d = ImageDraw.Draw(img)
    bob = math.sin(t * 3) * 4 * (1 - push)
    for side in (-1, 1):
        gx = 360 + side * 230 - push * 260
        gy = 1090 + bob - push * (380 if side < 0 else 150)
        s_ = 1.0 + 0.25 * push
        d.rounded_rectangle([gx - 80 * s_, gy - 90 * s_, gx + 80 * s_, gy + 90 * s_], int(36 * s_), fill=(252, 140, 27), outline=OL, width=8)
        d.rectangle([gx - 80 * s_, gy + 40 * s_, gx + 80 * s_, gy + 90 * s_], fill=(206, 98, 14), outline=OL, width=6)
        for f in range(4):
            fx = gx - 54 * s_ + f * 36 * s_
            d.line([(fx, gy - 86 * s_), (fx, gy - 40 * s_)], fill=(206, 98, 14), width=6)
        d.rectangle([gx - 80 * s_, gy + 90 * s_, gx + 80 * s_, gy + 120 * s_], fill=(40, 168, 74), outline=OL, width=6)  # sleeve
        if side < 0:
            d.rectangle([gx - 70 * s_, gy + 96 * s_, gx + 70 * s_, gy + 108 * s_], fill=(225, 30, 40))   # red bracelet (right wrist... seen from inside)


def eyes_set(t):
    c = Cam(camX=0.0, camH=1.5, hor=520, f=1500)          # longer lens: wall and kicker big, like through your eyes
    img = backdrop(520, stadium=True)
    pitch_near(img, c, 0.0)
    return img, c


def fk_wall_and_kicker(img, c, t, kick_pose=None, kp=0.0, peek=0.0):
    # their captain behind the wall: you only catch a glimpse of him between two heads
    ground_shadow(img, c, FKP[0] - 0.55, FKP[1] + 0.6, 0.35)
    sprite_at(img, c, opp(10, pose=kick_pose or "stand", phase=kp), FKP[0] - 0.55 + peek, FKP[1] + 0.6, height_m=1.55)
    ball_at(img, c, FKP[0], FKP[1] - 0.2, 0.0)
    for i, X in enumerate((-1.1, -0.35, 0.4, 1.15)):      # OUR wall, backs to you, arms crossed
        ground_shadow(img, c, X, 9.15, 0.32)
        sprite_at(img, c, ours((4, 5, 9, 6)[i], view="back"), X, 9.15, height_m=1.55)


def s_fk(t, u, T):
    """'Their captain. Top corner.' — your eyes: the wall, a glimpse of #10, and where you think it will go"""
    img, c = eyes_set(t)
    fk_wall_and_kicker(img, c, t, peek=0.25 * math.sin(t * 2))
    # imagined flight: a faint ghost curve that draws itself, and a ring where you expect it
    k = ease_out(clamp((u - 0.25) / 0.5))
    if k > 0:
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        pretty_arc(ov, c, FK_EYES[:int(len(FK_EYES) * 0.92)], k, 0.0, col=(235, 240, 255))
        ov.putalpha(ov.split()[3].point(lambda v: int(v * 0.55)))
        img.alpha_composite(ov)
        if k > 0.95:
            tx, ty = c.p(*at(FK_EYES, 0.92))
            glow_ring(img, tx, ty, 46 + 6 * math.sin(t * 6), 0.7, (235, 240, 255))
    eyes_gloves(img, 0.0, t)
    mini_score(img, t, "90'")
    return cam(img, 1.0 + 0.05 * u, 360, 760)


def s_slowmo(t, u, T):
    """'You see it early. You push off.' — he strikes, it rises over the wall; you WAIT, then go late"""
    img, c = eyes_set(t)
    kick = 0.12
    kp = clamp((u - kick + 0.06) / 0.1)
    fk_wall_and_kicker(img, c, t, kick_pose="kick" if u > kick - 0.06 else None, kp=kp)
    a = 0.0 if u < kick else 0.85 * ((u - kick) / (1 - kick)) ** 1.25     # slow motion, speeding up at the end
    wall_jump = 0.35 * math.sin(clamp((u - kick) / 0.35) * math.pi) if u > kick else 0
    if a > 0:
        if a < 0.85:
            ball_trail(img, c, FK_EYES, a, 0.06)
        ball_at(img, c, *at(FK_EYES, a))
    push = ease_in_out(clamp((u - 0.62) / 0.38))      # you only push off once it has cleared the wall
    eyes_gloves(img, push, t)
    slowmo_bars(img, 1.0 if kick < u < 0.98 else 0.0)
    mini_score(img, t, "90'")
    return cam(img, 1.0 + 0.18 * push, 360 - 160 * push, 700 - 120 * push)


def s_crosses(t, u, T):
    """Tuesday: crosses from the wing, you rise above everyone and catch"""
    k = min(1, int(u * 2)); ph = (u * 2) % 1 if u < 1 else 1.0
    # two different crosses: 1) floated from the LEFT wing, 2) whipped in from the RIGHT, he steps across
    V = [dict(camX=-1.0, camH=2.0, kx=0.3, src=(-11.0, 5.5, 0.3), apex=3.0, mates=((1.4, 7.0, 5), (-0.9, 6.8, 7))),
         dict(camX=1.2, camH=2.6, kx=1.1, src=(10.5, 4.0, 0.2), apex=1.4, mates=((-0.6, 6.4, 4), (2.3, 7.2, 6)))][k]
    img, c = shooter_view(t, 8.5, camX=V["camX"], camH=V["camH"], hor=470, stadium=False)
    goal3d(img, c, 8.5)
    KX = lerp(0.3, V["kx"], ease_out(clamp(ph / 0.4))) if k == 1 else 0.3
    cross = arc(V["src"], (V["kx"], 8.35, 1.6 * 0.66 + 0.75), apex=V["apex"])
    # an attacker (Dixon in a bib) and a defender jump too, you jump highest
    jump = math.sin(clamp((ph - 0.35) / 0.4) * math.pi)
    for X, Z, n in V["mates"]:
        sp = ours(n, view="back", pose="celebrate" if jump > 0.2 else "stand")
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, sp, X, Z, Y=0.35 * jump, height_m=1.55)
    ground_shadow(img, c, KX, 8.4, 0.45)
    hy = 0.75 * jump
    caught = ph >= 0.55
    fx, fy = c.p(KX, 8.4, hy)                   # feet on screen
    sc = 1.6 * c.k(8.4) / 31.0
    hands_y = fy - 37 * sc + 11.5 * sc           # glove row of the arms-up pose
    r_ball = 0.16 * c.k(8.4)
    sprite_at(img, c, hero(pose="celebrate" if (jump > 0.15 or caught) else "ready", gloves=True,
                           mouth="open" if jump > 0.5 else "flat"), KX, 8.4, Y=hy, height_m=1.6)
    if caught:   # ball IN FRONT of him, clasped by both gloves above his head
        rb = max(r_ball, 3.6 * sc)
        bx_, by_ = fx - 0.5 * sc, hands_y - 6.0 * sc          # held up above his head, clearly in front
        draw_ball(img, bx_, by_ + rb, rb / 6.5)
        r_ball = rb
        dg = ImageDraw.Draw(img)
        for sg in (-1, 1):
            gx_ = bx_ + sg * (r_ball + 0.4 * sc)
            gy_ = by_ + 0.8 * sc
            dg.line([(gx_, gy_ + 2 * sc), (bx_ + sg * 5.5 * sc, hands_y + 4 * sc)], fill=OL, width=int(3.0 * sc))   # forearms up to the ball
            dg.line([(gx_, gy_ + 2 * sc), (bx_ + sg * 5.5 * sc, hands_y + 4 * sc)], fill=SKIN["light"][0], width=int(1.8 * sc))
            dg.rounded_rectangle([gx_ - 1.5 * sc, gy_ - 2.0 * sc, gx_ + 1.5 * sc, gy_ + 2.0 * sc], int(0.8 * sc), fill=(252, 140, 27), outline=OL, width=max(2, int(sc * 0.5)))
    if not caught:
        a = ph / 0.55
        if a > 0.05:
            pretty_arc(img, c, cross, 1.0, from_=a)
        ball_trail(img, c, cross, a, 0.08)
        ball_at(img, c, *at(cross, a))
    elif ph < 0.68:
        glow_ring(img, fx - 1 * sc, hands_y, 50, 0.8, (255, 255, 210))
    return cam(img, 1.05 + 0.03 * u, 380, 700)


def s_dixon_watch(t, u, T):
    """Dixon by the post, arms folded, staring at you"""
    img, c = shooter_view(t, 8.5, camH=1.7, hor=500, stadium=False)
    goal3d(img, c, 8.5)
    ph = (t * 0.8) % 1
    sd_ = 1 if int(t * 0.8) % 2 else -1
    gx, gy = keeper_world(img, c, 0.0, 8.5, sd_, ph)
    shot = arc((0.4, 1.8, 0.1), (sd_ * 1.5, 8.5, 0.95), apex=0.45)
    if ph < 0.33:
        ball_trail(img, c, shot, ph / 0.33, 0.15)
        ball_at(img, c, *at(shot, ph / 0.33))
    else:
        draw_ball(img, gx, gy + 14, 0.16 * c.k(8.5) / 6.5)
    img = img.filter(ImageFilter.GaussianBlur(3))
    paste(img, dixon(mouth="flat", look=1, gloves=True, blink=0.6 < u < 0.66), 24, 230, 1560)
    d = ImageDraw.Draw(img)   # folded arms across his chest
    d.rounded_rectangle([90, 1040, 380, 1110], 22, fill=(60, 120, 210), outline=OL, width=6)
    for x in (110, 330):
        d.rounded_rectangle([x - 34, 1036, x + 34, 1112], 16, fill=(252, 140, 27), outline=OL, width=5)
    return cam(img, 1.02 + 0.05 * u, 300, 820)


def s_1v1_v2(t, u, T):
    """ONE ON ONE, broadcast angle: #7 breaks through, you rush out and spread big, the shot hits your leg and flies wide"""
    c = Cam(camX=0.9, camH=3.4, hor=420)
    img = backdrop(420, stadium=True)
    GZ = 17.0
    pitch_persp(img, c, Zgoal=GZ)
    goal3d(img, c, GZ)
    shot_t, hit_t = 0.52, 0.62
    # attacker run with the ball
    rz = lerp(6.0, 12.2, ease_in_out(clamp(u / shot_t)))
    rx = lerp(1.4, 0.6, clamp(u / shot_t))
    # chasing defenders (beaten)
    for X, Z0, n in ((3.4, 5.2, 4), (-2.6, 5.6, 5)):
        Z = lerp(Z0, Z0 + 5.0, clamp(u / 0.7))
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, ours(n, pose="run", phase=t * 2.6), X, Z, height_m=1.55)
    # you: rush out from the line, then spread big
    kz = lerp(GZ, 13.6, ease_out(clamp(u / shot_t)))
    spread = u > shot_t - 0.08
    ground_shadow(img, c, 0.0, kz, 0.55)
    sprite_at(img, c, hero(pose="ready" if spread else "run", phase=t * 2.6, gloves=True, mouth="open" if spread else "flat"),
              0.0, kz, height_m=1.6 * (1.08 if spread else 1.0))
    ground_shadow(img, c, rx, rz, 0.35)
    sprite_at(img, c, opp(7, view="back", pose="kick" if u > shot_t - 0.05 and u < shot_t + 0.1 else "run",
                         phase=clamp((u - shot_t + 0.05) / 0.1) if u > shot_t - 0.05 else t * 2.6), rx, rz, height_m=1.55)
    if u < shot_t:
        ring_on_grass(img, c, rx, rz, 0.6, C_Y, 4)
        run_path = arc((rx + 0.45, rz + 0.22, 0.0), (0.6, 12.8, 0.0), apex=0.0)
        dotted_path(img, c, run_path, 1.0, from_=0.0)
        ball_at(img, c, rx + 0.45, rz + 0.22, 0.11)        # at his right boot, in front
    else:
        shot = arc((0.55, 12.6, 0.1), (-0.25, kz - 0.05, 0.45), apex=0.1)
        defl = arc((-0.25, kz - 0.05, 0.45), (5.8, 18.5, 0.6), apex=1.7)
        if u < hit_t:
            a = (u - shot_t) / (hit_t - shot_t)
            ball_trail(img, c, shot, a, 0.3)
            ball_at(img, c, *at(shot, a))
        else:
            a = clamp((u - hit_t) / 0.3)
            pretty_arc(img, c, defl, 1.0, from_=a)
            ball_trail(img, c, defl, a, 0.12)
            ball_at(img, c, *at(defl, a))
            hx, hy = c.p(-0.25, kz - 0.05, 0.45)
            impact_lines(img, hx, hy, T + hit_t * (STARTS[15] - T), t, 12)
            glow_ring(img, hx, hy, 50 + 150 * a, 0.9 * (1 - a), (255, 255, 210))
    slowmo_bars(img, 1.0 if shot_t - 0.06 < u < hit_t + 0.15 else 0.0)
    img = flash(img, 0.5 * clamp(1 - abs(u - hit_t) * 16))
    fx, fy = c.p(0.2, lerp(9, 13.0, clamp(u / hit_t)), 0.8)
    zoom = 1.0 + 0.35 * ease_in_out(clamp((u - 0.2) / 0.45))
    out = cam(img, zoom, fx, fy, *shake(t, T + hit_t * (STARTS[15] - T), .3, 12)).convert("RGBA")
    mini_score(out, t, "61'")
    return out


def s_fk_tease(t, u, T):
    """'Last minute. Free kick. Edge of the box.' — straight in: your eyes, the wall, their captain over the ball"""
    img, c = eyes_set(t)
    fk_wall_and_kicker(img, c, t, peek=0.15 * math.sin(t * 2))
    eyes_gloves(img, 0.0, t)
    out = cam(img, 1.08 - 0.06 * u, 360, 760).convert("RGBA")
    mini_score(out, t, "90'")
    return out


def s_foul(t, u, T):
    """flashback, 20 seconds earlier: Mason loses it, their captain breaks, our #5 trips him at the edge of the box"""
    c = Cam(camX=0.6, camH=3.2, hor=420)
    img = backdrop(420, stadium=True)
    GZ = 22.0
    pitch_persp(img, c, Zgoal=GZ)
    goal3d(img, c, GZ)
    ground_shadow(img, c, 0.0, GZ, 0.45)
    sprite_at(img, c, hero(pose="ready", gloves=True), 0.0, GZ, height_m=1.6)
    lose, foul = 0.3, 0.68
    # Mason dribbles forward; their captain closes in from the side and STEALS it with a tackle; Mason goes down
    mz = lerp(5.6, 7.0, clamp(u / lose))
    mx = -0.5
    if u < lose:
        ground_shadow(img, c, mx, mz, 0.35)
        sprite_at(img, c, mason(view="back", pose="run", phase=t * 2.4), mx, mz, height_m=1.55)
    else:
        fk = clamp((u - lose) / 0.15)
        k = 1.55 * c.k(mz) / 31
        spm = mason(view="back", pose="stand", mouth="open").resize((int(24 * k), int(39 * k)), Image.NEAREST).rotate(80 * ease_out(fk), expand=True, resample=Image.NEAREST)
        x, y = c.p(mx - 0.4 * fk, mz)
        ground_shadow(img, c, mx - 0.4 * fk, mz, 0.5)
        img.alpha_composite(spm, (int(x - spm.width / 2), int(y - spm.height + 6)))
    # captain: before the steal he runs in from the right toward Mason's ball, after it he carries it at the box
    if u < lose:
        cx = lerp(1.6, mx + 0.6, ease_in_out(u / lose)); cz = lerp(8.5, mz + 0.4, ease_in_out(u / lose))
    else:
        cx = lerp(mx + 0.6, 0.4, clamp((u - lose) / (foul - lose))); cz = lerp(mz + 0.4, 10.3, ease_in_out(clamp((u - lose) / (foul - lose))))
    tripped = u > foul
    # our #5 slides in from the right
    sz = lerp(12.0, 10.6, ease_out(clamp((u - 0.35) / (foul - 0.35))))
    sx = lerp(3.4, 1.0, ease_out(clamp((u - 0.35) / (foul - 0.35))))
    ground_shadow(img, c, sx, sz, 0.45)
    if u > 0.45:   # slide tackle: lying on his side, feet first
        k = 1.55 * c.k(sz) / 31
        sp = ours(5, pose="reach").resize((int(24 * k), int(39 * k)), Image.NEAREST).rotate(-95, expand=True, resample=Image.NEAREST)
        x, y = c.p(sx, sz)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height * 0.8)))
    else:
        sprite_at(img, c, ours(5, pose="run", phase=t * 2.6), sx, sz, height_m=1.55)
    # their captain: runs, then goes flying
    ground_shadow(img, c, cx, cz, 0.35)
    if not tripped:
        sprite_at(img, c, opp(10, view="back" if u > lose else "front", pose="kick" if abs(u - lose) < 0.04 else "run", phase=t * 2.8), cx, cz, height_m=1.55)
        if u > lose:
            ball_at(img, c, cx + 0.45, cz + 0.22, 0.11)
        else:
            ball_at(img, c, mx + 0.45, mz + 0.22, 0.11)
    else:
        f = clamp((u - foul) / 0.25)
        k = 1.55 * c.k(cz) / 31
        sp = opp(10, view="back", pose="celebrate", mouth="open").resize((int(24 * k), int(39 * k)), Image.NEAREST).rotate(-75 * ease_out(f), expand=True, resample=Image.NEAREST)
        x, y = c.p(cx + 0.4 * f, cz + 0.6 * f, 0.5 * math.sin(f * math.pi))
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height)))
        ball_at(img, c, cx + 0.3 + 1.5 * f, cz + 1.2 + 2.0 * f, 0.11)
        hx, hy = c.p(0.8, 10.4, 0.3)
        impact_lines(img, hx, hy, T + foul * (STARTS[17] - T), t, 12)
        glow_ring(img, hx, hy, 70, 0.8 * (1 - f), (255, 70, 70))
        # referee's whistle -> yellow card
        if u > foul + 0.15:
            kk = spring(t - T - (foul + 0.15) * (STARTS[17] - T), 13, 7)
            d = ImageDraw.Draw(img)
            w_, h_ = 70 * kk, 100 * kk
            d.rounded_rectangle([560 - w_ / 2, 820 - h_ / 2, 560 + w_ / 2, 820 + h_ / 2], 8, fill=(250, 210, 40), outline=OL, width=5)
            pill(img, 360, 1020, "FREE KICK", (200, 40, 50), kk, 40)
    if lose - 0.02 < u < lose + 0.12:
        impact_lines(img, *c.p(mx + 0.45, mz + 0.22, 0.2), T + lose * (STARTS[17] - T), t, 10)
    fx, fy = c.p(0.6, lerp(8, 10.4, clamp(u / foul)), 0.6)
    out = cam(img, 1.15 + 0.2 * ease_in_out(clamp(u / foul)), fx, fy, *shake(t, T + foul * (STARTS[17] - T), .3, 12)).convert("RGBA")
    mini_score(out, t, "89'")
    return out


def s_finger_v2(t, u, T):
    """FINGERTIPS. CROSSBAR. OUT! — telephoto from behind the taker: the wall jumps, the ball curls over it into the
    top corner (shooter's right), you fly across, fingertips push it onto the bar and over."""
    c = Cam(camX=1.2, camH=3.2, hor=470, f=1750)
    img = backdrop(470, stadium=True)
    GZ = 19.0
    pitch_persp(img, c, Zgoal=GZ, box=False)
    goal3d(img, c, GZ)
    contact, bar = 0.42, 0.55
    # --- ball: curling path into the top right corner (slow motion until the touch)
    path = arc((3.2, 2.4, 0.1), (2.25, GZ, 1.85), apex=2.2, curve=-0.6)
    over = arc((2.25, GZ, 1.85), (2.35, GZ, 2.02), apex=0.0)            # tipped up onto the bar
    out_ = arc((2.35, GZ, 2.02), (2.9, GZ + 2.5, 0.2), apex=1.6)        # over the bar, out
    # --- keeper flight (his left = screen right), launches before the frame starts so we see him in the air
    f = clamp((u + 0.25) / (contact + 0.25))
    kxw = lerp(0.2, 1.55, ease_out(f))
    kyw = lerp(0.6, 1.35, math.sin(f * math.pi / 2)) if u <= contact else 1.35 - 1.3 * ((u - contact) / (1 - contact)) ** 2
    if u > contact:
        kxw = 1.55 + 0.35 * (u - contact)
    sc = 1.6 * c.k(GZ) / 31.0
    rot = -70 if u <= contact + 0.1 else -70 - 25 * clamp((u - contact - 0.1) / 0.3)
    sp = hero(pose="reach", gloves=True, mouth="open").resize((int(24 * sc), int(39 * sc)), Image.NEAREST)
    sp = sp.rotate(rot, expand=True, resample=Image.NEAREST)
    kx, ky = c.p(kxw, GZ, kyw)
    ground_shadow(img, c, kxw, GZ, 0.8, 80)
    img.alpha_composite(sp, (int(kx - sp.width / 2), int(ky - sp.height / 2)))
    ang = math.radians(-rot)
    gx = kx + 16.5 * sc * math.sin(ang)        # fingertips (end of the stretched arms)
    gy = ky - 16.5 * sc * math.cos(ang)
    # --- the ball
    if u < contact:
        a = 0.45 + 0.55 * (u / contact) ** 1.3
        pretty_arc(img, c, path, 1.0, from_=a)
        ball_trail(img, c, path, a, 0.05)
        ball_at(img, c, *at(path, a), shadow_=False)
    elif u < bar:
        a = (u - contact) / (bar - contact)
        ball_at(img, c, *at(over, a), shadow_=False)
    else:
        a = clamp((u - bar) / (1 - bar))
        ball_trail(img, c, out_, a, 0.12)
        ball_at(img, c, *at(out_, a), shadow_=False)
    # --- impacts: fingertip touch, then the crossbar
    tx, ty = c.p(2.25, GZ, 1.85)
    if contact - 0.02 < u < contact + 0.25:
        k = (u - contact) / 0.25
        glow_ring(img, tx, ty, 30 + 120 * k, 0.95 * (1 - k), (255, 245, 190))
        impact_lines(img, tx, ty, 0.0, k * 0.25, 12)
    bx_, by_ = c.p(2.35, GZ, 2.0)
    if bar < u < bar + 0.25:
        k = (u - bar) / 0.25
        impact_lines(img, bx_, by_, 0.0, k * 0.25, 10)
        ImageDraw.Draw(img).line([c.p(-2.5, GZ, 2.0), c.p(2.5, GZ, 2.0)], fill=(255, 255, 210), width=6)   # bar rings
    # --- our wall in the foreground, jumping (front view: they face the taker = the camera)
    jump = 0.4 * math.sin(clamp((u + 0.6) / 0.9) * math.pi)
    for i, X in enumerate((-0.6, -0.05, 0.5, 1.05)):
        ground_shadow(img, c, X, 11.55, 0.32)
        sprite_at(img, c, ours((4, 5, 9, 6)[i], pose="celebrate" if jump > 0.1 else "stand"), X, 11.55, Y=jump, height_m=1.55)
    slowmo_bars(img, 1.0 if u < bar else 1 - clamp((u - bar) * 4))
    img = flash(img, 0.55 * clamp(1 - abs(u - contact) * 18))
    zoom = 1.0 + 0.2 * ease_in_out(clamp(u / contact))
    out = cam(img, zoom, lerp(360, tx, 0.5), lerp(760, ty, 0.5), *shake(t, T + bar * (STARTS[22] - T), .35, 14)).convert("RGBA")
    mini_score(out, t, "90'")
    return out


from PIL import ImageEnhance


def grade(img):
    """muted reference look: less saturation, slightly softer contrast, warm evening tint"""
    img = ImageEnhance.Color(img).enhance(0.9)
    img = Image.blend(img, Image.new("RGB", img.size, (60, 50, 70)), 0.04)
    w, h = img.size                                     # uniform pixel grid over EVERYTHING (reference look)
    return img.resize((w // 3, h // 3), Image.NEAREST).resize((w, h), Image.NEAREST)   # crisp, no smearing


SCENES = [s_hook, s_knock, s_coach, s_training, s_crosses, s_dixon_watch, s_notyet, s_okafor, s_walkout, s_attackA, s_attackA, s_mason, s_getup,
          s_header, s_1v1_v2, s_mason_goal, s_foul, s_fk_tease, s_fk, s_slowmo, s_finger_v2, s_whistle, s_pen, s_choice, s_end]


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
    img = SCENES[i](t, u, T).convert("RGB")
    img = grade(img).convert("RGBA")
    if i > 0 and t - T < 0.07 and SCENES[i] is not SCENES[i - 1]:
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
