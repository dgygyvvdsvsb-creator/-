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
    [("\"WEDNESDAY.", Y), ("A", W), ("FRIENDLY.", W), ("PLAY", W), ("WELL...", W), ("YOU", W), ("START", G), ("SATURDAY.\"", Y)],
    [("MONDAY.", W), ("TRAINING.", W), ("NO", Y), ("DAYS", Y), ("OFF.", Y)],
    [("YOU'RE", W), ("NOT", R_), ("NUMBER", W), ("ONE.", Y), ("NOT", W), ("YET.", G)],
    [("WEDNESDAY.", W), ("OKAFOR'S", Y), ("STILL", W), ("INJURED.", R_)],
    [("SO", W), ("YOU", G), ("START.", G), ("FIRST", Y), ("TEAM.", Y)],
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
    return person(Kit((140, 70, 180), (30, 30, 40), (140, 70, 180), 1), skin="tan", hair="black", style="short", gloves=True, **kw)


def score_state(t):
    l = 1 if t >= STARTS[13] + 0.6 * (STARTS[14] - STARTS[13]) else 0
    r = 1 if t >= STARTS[8] + 0.35 * (STARTS[9] - STARTS[8]) else 0
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
    d.chord([50, 736, 180, 832], 180, 360, fill=NAVY, outline=OL, width=4)
    d.line([(115, 740), (115, 784)], fill=NAVY_D, width=3)
    d.rectangle([106, 754, 124, 768], fill=(250, 206, 40), outline=OL, width=2)
    d.chord([40, 772, 200, 812], 0, 180, fill=NAVY_D, outline=OL, width=4)
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
    # inside: the door opens, you step in, the coach looks up from his desk
    img = office(t)
    d = ImageDraw.Draw(img)
    open_k = ease_out((u - 0.5) / 0.25)
    d.rectangle([560, 180, 700, 760], fill=(90, 96, 116), outline=OL, width=6)         # doorway (corridor behind)
    d.polygon([(560, 180), (560 + 140 * (1 - open_k) + 20 * open_k, 180 + 30 * open_k),
               (560 + 140 * (1 - open_k) + 20 * open_k, 760 - 30 * open_k), (560, 760)], fill=(150, 100, 60), outline=OL)
    paste(img, hero(look=-1), 9, 640, 770)
    desk_and_coach(img, t, look=1 if u > 0.75 else 0, blink=u < 0.7)
    return cam(img, 1.0 + 0.03 * u, 360, 700)


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
    pill(img, 360, 1250, "FRIENDLY · RIVERSIDE vs NORTHFIELD", (14, 16, 30), spring(t - T - 0.2, 13, 7), 26)
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
        impact_lines(img, *c.p(0.15, 18, 0.3), T + 0.35 * (STARTS[9] - STARTS[8]), t, 10)
    striker = opp(9, view="back", pose="kick" if u > kick - 0.1 else "run", phase=clamp((u - kick + 0.1) / 0.2) if u > kick - 0.1 else t * 2)
    paste(img, striker, 11, 250, 1420)
    mini_score(img, t, "3'")
    if goal_:
        img = flash(img, 0.35 * clamp(1 - abs(u - 0.37) * 8), (255, 50, 50))
    return cam(img, 1 + (0.05 * u if not goal_ else 0.12), *c.p(0, 17, 0.8), *shake(t, T + 0.37 * (STARTS[9] - STARTS[8]), .3, 10) if goal_ else (0, 0))


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
        impact_lines(img, *c.p(0.4, 8.2, 2.1), T + 0.4 * (STARTS[12] - T), t, 8)
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
    return cam(img, 1 + 0.04 * u, 360, 800, *shake(t, T + 0.75 * (STARTS[13] - T), .3, 12))


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
        impact_lines(img, x, y, T + (kick + 0.3) * (STARTS[14] - T), t, 10)
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
        impact_lines(img, *c.p(2.25, 6.0, 2.0), T + hit * (STARTS[18] - T), t, 12)
        glow_ring(img, *c.p(2.25, 6.0, 2.0), 60 + 160 * clamp((u - hit) * 3), 0.9 * (1 - clamp((u - hit) * 2)), (255, 255, 210))
    slowmo_bars(img, 1 - ease_out((u - hit) * 3) if u > hit else 1)
    img = flash(img, 0.45 * clamp(1 - abs(u - hit) * 14))
    return cam(img, 1.05, 420, 720, *shake(t, T + hit * (STARTS[18] - T), .35, 14))


def s_whistle(t, u, T):
    img = Image.new("RGBA", (FW, FH), (24, 26, 44, 255))
    crowd_band(img, 0, 560, seed=34, blur=1.0)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(18, 20, 34))
    scoreboard(img, 640, "RIV", "NOR", 1, 1, "FULL TIME", 1.0, t=t)
    if u > 0.55:
        pill(img, 360, 1000, "SHOOTOUT", (200, 40, 50), spring(t - T - 0.55 * (STARTS[19] - T), 13, 7), 56)
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
                pill(img, x1, y1 - 60, lab, bg, spring(t - T - (0.35 if side < 0 else 0.55) * (STARTS[21] - T), 13, 7), 40)
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
    img, c = shooter_view(t, 12, camH=2.2, hor=470, stadium=False)
    goal3d(img, c, 12)
    d = ImageDraw.Draw(img)
    for X, Z in ((-6, 6), (-3, 5), (3, 5), (6, 6), (-4, 9), (4, 9)):     # cones
        x, y = c.p(X, Z); r = 0.18 * c.k(Z)
        d.polygon([(x - r, y), (x + r, y), (x, y - r * 2.2)], fill=(252, 140, 27), outline=OL)
    k = int(u * 3); phase = (u * 3) % 1
    side = 1 if k % 2 else -1
    gx, gy = keeper_world(img, c, 0, 12, side, phase)
    shot = arc((0.0, 2.5, 0.1), (side * 1.55, 12, 1.0), apex=0.8)
    if phase < 0.45:
        a = phase / 0.45
        ball_trail(img, c, shot, a, 0.12)
        ball_at(img, c, *at(shot, a))
    else:
        draw_ball(img, gx, gy + 10, 0.7)
    ground_shadow(img, c, -1.8, 7.0, 0.4)
    sprite_at(img, c, coach(look=1), -1.8, 7.0, height_m=1.75)
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
    for dx in (0, 22):
        d.line([(470 + dx, 1060), (440 + dx, 700)], fill=(180, 180, 190), width=10)
    paste(img, hero(gloves=True, look=-1), 9, 560, 1060)
    return cam(img, 1 + 0.05 * u, 360, 860)


SCENES = [s_hook, s_knock, s_coach, s_training, s_notyet, s_okafor, s_walkout, s_strike, s_goal, s_mason, s_getup,
          s_header, s_1v1, s_mason_goal, s_board, s_fk, s_slowmo, s_finger, s_whistle, s_pen, s_choice, s_end]


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
