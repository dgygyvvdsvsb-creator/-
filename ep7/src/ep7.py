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
FLASH = {8, 9, 10, 11, 12, 13, 14}                      # the 1984 tape
_vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"vo/lines_{PLATFORM}.json")
if os.path.exists(_vf):
    VOICE = [tuple(x) for x in json.load(open(_vf))]
else:
    VOICE, t0 = [], 0.05
    for i, ws in enumerate(LINES):
        d_ = max(1.3, 0.34 * len(ws) + 0.3)
        if i in (11, 12, 13):
            d_ = 1.35
        VOICE.append((t0, t0 + d_)); t0 += d_ + 0.42
STARTS = [max(0.0, a - 0.12) for a, _ in VOICE]
STARTS[0] = 0.0
TOTAL = VOICE[-1][1] + 2.2


def D(i):
    return (STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i]


fb.D = D            # the reused 1984 scenes take their spring timings from this episode's clock
fb.STARTS = STARTS
fb.UYF = UY
fb.CARD_I, fb.TODAY_I = 8, 15


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


class GoalCam(Cam):
    """camera 6.4 m behind the goal line, 3 m up, looking out over the net: world Z = metres from the goal line"""
    ZOFF = 6.4

    def p(self, X, Z, Y=0.0):
        return Cam.p(self, X, Z + self.ZOFF, Y)

    def k(self, Z):
        return Cam.k(self, Z + self.ZOFF)


KC = GoalCam(camX=0.0, camH=3.0, hor=470)
KZ = 0.5                                         # you stand half a metre off your line
KX0, FY = KC.p(0.0, KZ)
KS = 1.6 * KC.k(KZ) / 31                         # sprite scale that makes you 1.6 m at that distance


def keeper_sprite(img, pose, rot=0.0, X=0.0, Y=0.0, alpha=1.0):
    """you, from behind, at world (X, KZ, Y) — same scale as the goal"""
    sp = hero(view="back", pose=pose, gloves=True)
    sp = sp.resize((int(24 * KS), int(39 * KS)), Image.NEAREST)
    if rot:
        sp = sp.rotate(rot, expand=True, resample=Image.NEAREST)
    if alpha < 1:
        sp.putalpha(sp.split()[3].point(lambda a_: int(a_ * alpha)))
    x, y = KC.p(X, KZ, Y)
    if rot:
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2 - 0.45 * KC.k(KZ))))
    else:
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - 37 * KS)))
    return x, y


def dive_XY(ff, side):
    """one arc for every dive: push off, about 0.9 m up, land on the grass inside the post"""
    return side * 1.3 * ff, max(0.0, 0.95 * math.sin(ff * math.pi) - 0.05)


def draw_dive(img, f, side, ghosts=True, streaks=True):
    """you in the air at progress f (0 push-off .. 1 on the grass), with afterimages along the same arc"""
    if ghosts and 0.05 < f < 0.98:
        for g, ga in ((0.18, 0.2), (0.09, 0.35)):
            fg = f - g
            if fg <= 0:
                continue
            X, Yh = dive_XY(fg, side)
            keeper_sprite(img, "reach", rot=-side * 85 * min(1.0, fg * 1.6), X=X, Y=Yh, alpha=ga)
    X, Yh = dive_XY(f, side)
    pose = "reach" if f > 0.03 else "ready"
    x, y = keeper_sprite(img, pose, rot=-side * 85 * min(1.0, f * 1.6) if f > 0.03 else 0.0, X=X, Y=Yh)
    if streaks and 0.05 < f < 0.95:
        d = ImageDraw.Draw(img)
        yb = y - 0.45 * KC.k(KZ)
        for j in range(7):
            yy = yb - 30 + 10 * j
            d.line([(x - side * 70, yy), (x - side * (150 + 18 * j), yy)], fill=(255, 255, 255), width=3)
    return x, y


def turf(img, k, seed=9):
    """turf and dust thrown up at the push-off spot"""
    if not 0 < k < 1:
        return
    d = ImageDraw.Draw(img)
    rng = random.Random(seed)
    for _ in range(18):
        ang = rng.uniform(math.pi * 1.05, math.pi * 1.95)
        r_ = rng.uniform(20, 120) * ease_out(k)
        px, py = KX0 + math.cos(ang) * r_, FY + math.sin(ang) * r_ * 0.6 + 80 * k * k
        rr = rng.uniform(3, 7) * (1 - k)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(120, 90, 60) if rng.random() < 0.5 else (70, 140, 70))


def posts_fg(img, c=None):
    """the real goal in 3D, between us and you: the net box runs back toward us (roof, back wall, sides), then the
    white frame with thickness on the goal line"""
    W, H, DEP, BH = 2.5, 2.0, 1.6, 1.3              # half width, bar height, net depth, height of the back wall
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    col = (255, 255, 255, 120)
    p = KC.p
    n = 20
    for i in range(n + 1):                          # back wall (vertical plane at Z = -DEP)
        X = -W + 2 * W * i / n
        od.line([p(X, -DEP, 0), p(X, -DEP, BH)], fill=col, width=2)
    for j in range(7):
        Yv = BH * j / 6
        od.line([p(-W, -DEP, Yv), p(W, -DEP, Yv)], fill=col, width=2)
    for i in range(n + 1):                          # roof: from the bar back and down to the top of the back wall
        X = -W + 2 * W * i / n
        od.line([p(X, 0, H), p(X, -DEP, BH)], fill=col, width=2)
    for j in range(7):
        a = j / 6
        od.line([p(-W, -DEP * a, lerp(H, BH, a)), p(W, -DEP * a, lerp(H, BH, a))], fill=col, width=2)
    for sx in (-W, W):                              # side panels
        for j in range(7):
            a = j / 6
            od.line([p(sx, -DEP * a, 0), p(sx, -DEP * a, lerp(H, BH, a))], fill=col, width=2)
        for j in range(6):
            Yv = H * j / 5
            od.line([p(sx, 0, Yv), p(sx, -DEP, min(Yv, BH))], fill=col, width=2)
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    for a_, b_ in (((-W, -DEP, 0), (-W, -DEP, BH)), ((W, -DEP, 0), (W, -DEP, BH)), ((-W, -DEP, BH), (W, -DEP, BH)),
                   ((-W, 0, H), (-W, -DEP, BH)), ((W, 0, H), (W, -DEP, BH))):
        d.line([p(*a_), p(*b_)], fill=(225, 228, 236), width=4)          # the net's support bars
    pw = int(0.12 * KC.k(0))
    for a_, b_ in (((-W, 0, 0), (-W, 0, H)), ((W, 0, 0), (W, 0, H)), ((-W, 0, H), (W, 0, H))):
        d.line([p(*a_), p(*b_)], fill=OL, width=pw + 6)
    for a_, b_ in (((-W, 0, 0), (-W, 0, H)), ((W, 0, 0), (W, 0, H)), ((-W, 0, H), (W, 0, H))):
        d.line([p(*a_), p(*b_)], fill=(252, 252, 255), width=pw)
        x0, y0 = p(*a_); x1, y1 = p(*b_)
        d.line([(x0 + pw * 0.25, y0), (x1 + pw * 0.25, y1)], fill=(214, 218, 228), width=max(2, pw // 3))   # shading


def keeper_set(t):
    c = KC
    img = backdrop(470, stadium=True)
    pitch_persp(img, Cam(camX=0.0, camH=3.0, hor=470), None)      # grass all the way down to the camera
    pitch_near(img, c, 0.0)
    return img, c


RUN_PATH = [(-3.2, 15.0), (-2.2, 13.0), (-1.2, 11.0), (-0.3, 9.4), (0.3, 8.45)]   # diagonal run-up from wide left


def _path(p):
    """point and distance along the run-up for progress p 0..1"""
    pts = RUN_PATH
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg)
    d = clamp(p) * L
    acc = 0.0
    for i, sl in enumerate(seg):
        if acc + sl >= d:
            f = (d - acc) / sl
            return (lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)), d
        acc += sl
    return pts[-1], L


WATCH = [(-7.0, 23.0, "res", 4), (-5.6, 22.4, "res", 5), (-4.2, 23.4, "res", 7),
         (4.2, 23.2, "first", 4), (5.6, 22.6, "first", 5), (7.0, 23.4, "first", 6)]


def watchers(img, c, t):
    """both teams on the halfway line: nervous, never frozen — sway, shift weight, hands up / on heads"""
    for i, (X, Z, team, n) in enumerate(WATCH):
        sway = 0.18 * math.sin(t * 1.6 + i * 1.7)
        bob = 0.05 * abs(math.sin(t * 3.1 + i))
        nerv = math.sin(t * 1.2 + i * 2.3)
        pose = "celebrate" if nerv > 0.8 else ("ready" if nerv < -0.7 else "stand")
        goal_t = STARTS[3]                      # the ball crosses the line at the cut
        if t > goal_t:                       # the result lands: winners jump, losers freeze
            won = (team == "res") == RIGHT
            pose = "celebrate" if won else "stand"
            bob = 0.3 * abs(math.sin(t * 7 + i)) if won else 0.0
            sway = sway * (1.0 if won else 0.2)
        sp = (res if team == "res" else first)(n, pose=pose, blink=int(t * 3 + i) % 7 == 0, look=-1 if X > 0 else 1)
        ground_shadow(img, c, X + sway, Z, 0.3)
        sprite_at(img, c, sp, X + sway, Z, Y=bob, height_m=1.6)


def run_progress(t):
    """continuous across lines 0-2: real speed in the hook, slow motion on the vote card, last steps + kick"""
    s1, s2 = STARTS[1], STARTS[2]
    kick_t = s2 + 0.42 * D(2)
    if t < COLD + 0.45:
        return 0.0
    if t < s1:
        return 0.62 * ((t - COLD - 0.45) / (s1 - COLD - 0.45))
    if t < s2:
        return 0.62 + 0.24 * ((t - s1) / (s2 - s1))           # slow motion
    return min(1.0, 0.86 + 0.14 * ease_out((t - s2) / max(0.01, kick_t - s2)))


def taker_and_ball(img, c, t, run=None, kick=None, after=None):
    """their captain #10: diagonal run-up with a real stride (legs cycle with the distance covered), then the kick"""
    p = run_progress(t)
    (X, Z), dist = _path(p)
    stride = 1.5                                   # metres per full leg cycle
    phase = dist / stride
    bob = abs(math.sin(phase * math.pi * 2)) * 0.07
    if after is not None:                       # after the strike: foot down, then (goal) arms up
        pose, ph = "stand", 0.0                    # he watches it roll in; the celebration is in the next shot
        bob = 0.02 * abs(math.sin(t * 3))
    elif kick is not None:
        pose, ph = "strikeF", kick
        bob = 0.1 * math.sin(clamp((kick - 0.55) / 0.45) * math.pi) if kick > 0.55 else 0.0   # little hop after the strike
    elif p >= 0.999:
        pose, ph = "stand", 0.0
        bob = 0.02 * abs(math.sin(t * 3))
    else:
        pose, ph = "run", phase
    ground_shadow(img, c, X, Z, 0.4)
    sp = res(10, pose=pose, phase=ph, mouth="flat")
    if pose == "run":                               # lean into the run
        sp = sp.rotate(-6 if X < 0.2 else 0, resample=Image.NEAREST, expand=False)
    sprite_at(img, c, sp, X, Z, Y=bob, height_m=1.6)


COLD = 0.95          # cold open: the frozen dive (TikTok preview), then rewind to the run-up


def s_cold(t):
    """frame 0 = the same angle as the penalty (behind you): you are already flying RIGHT — and #10 hasn't even
    struck the ball yet. The hook: you went too early. (no outcome shown)"""
    img, c = keeper_set(t)
    watchers(img, c, t)
    ground_shadow(img, c, 0.3, 8.45, 0.4)
    sprite_at(img, c, res(10, pose="strikeF", phase=0.34, mouth="flat"), 0.3, 8.45, height_m=1.6)  # backswing, ball untouched
    ball_at(img, c, 0.0, 7.6, 0.0)
    k = clamp(t / COLD)
    f = 0.72 + 0.03 * k                                   # frozen in the dive, clear of #10 in the background
    turf(img, 0.5)
    draw_dive(img, f, 1)
    glow_ring(img, *c.p(0.0, 7.6, 0.1), 50 + 6 * math.sin(t * 18), 0.8, (255, 230, 150))   # the ball: not even kicked yet
    posts_fg(img, c)
    slowmo_bars(img, 1.0)
    shoot_bar(img)
    img = cam(img, 1.02, 360, 820)
    if t > COLD - 0.12:
        img = flash(img, (t - (COLD - 0.12)) / 0.12 * 0.8)
    return img


REWIND = 0.45


def s_hook(t, u, T):
    if t < COLD:
        return s_cold(t)
    img, c = keeper_set(t)
    watchers(img, c, t)
    if t < COLD + REWIND:                       # rewind: everything slides back, #10 reverses to his mark
        r = (t - COLD) / REWIND
        f = 0.74 * (1 - ease_in_out(r))
        p = 1.0 - ease_in_out(r)
        (X, Z), _ = _path(p)
        ground_shadow(img, c, X, Z, 0.4)
        sprite_at(img, c, res(10, pose="run", phase=-t * 6), X, Z, height_m=1.6)
        ball_at(img, c, 0.0, 7.6, 0.0)
        draw_dive(img, f, 1, ghosts=False, streaks=False)
        posts_fg(img, c)
        shoot_bar(img)
        img = cam(img, 1.02, 360, 820)
        img = vhs(img, t, 1.4)
        d = ImageDraw.Draw(img)
        for xo in (0, 46):
            d.polygon([(330 + xo, 640), (380 + xo, 610), (380 + xo, 670)], fill=(255, 255, 255))
        return img
    taker_and_ball(img, c, t)
    ball_at(img, c, 0.0, 7.6, 0.0)
    keeper_sprite(img, "ready", Y=0.03 * abs(math.sin(t * 5)))
    posts_fg(img, c)
    shoot_bar(img)
    return cam(img, 1.02, 360, 820)


def arrow_on_grass(img, side, k, col, lab, bg, t, T0):
    d = ImageDraw.Draw(img)
    x0, y0 = KC.p(side * 0.5, KZ + 0.6)
    x1, y1 = KC.p(side * 2.0, KZ, 1.5)
    pts = [(lerp(x0, x1, a), lerp(y0, y1, a) - 120 * math.sin(a * math.pi)) for a in np.linspace(0, k, 24)]
    for j in range(0, len(pts) - 1, 2):
        d.line([pts[j], pts[j + 1]], fill=OL, width=18)
        d.line([pts[j], pts[j + 1]], fill=col, width=11)
    if k >= 1:
        pill(img, min(560, max(160, x1)), 560, lab, bg, spring(t - T0, 13, 7), 40)      # above the crossbar


def s_vote(t, u, T):
    img, c = keeper_set(t)
    watchers(img, c, t)
    taker_and_ball(img, c, t)
    ball_at(img, c, 0.0, 7.6, 0.0)
    side = 1 if RIGHT else -1          # the hero's right = screen right (we see his back)
    arrow_on_grass(img, side, clamp((u - 0.1) / 0.4), C_B if RIGHT else C_Y, "RIGHT" if RIGHT else "LEFT",
                   (40, 110, 200) if RIGHT else (200, 160, 20), t, T + 0.5 * D(1))
    keeper_sprite(img, "ready", Y=0.03 * abs(math.sin(t * 5)))
    posts_fg(img, c)
    pill(img, 165, 560, "YOU VOTED", (40, 150, 80), spring(t - T - 0.1, 13, 7), 30)
    shoot_bar(img)
    return cam(img, 1.02 + 0.02 * u, 360, 820)



def eyes_gloves(img, push=0.0, t=0.0):
    """your own gloves at the bottom of the frame (first person). push 0 ready .. 1 flying to the right"""
    d = ImageDraw.Draw(img)
    bob = math.sin(t * 3) * 4 * (1 - push)
    for side in (-1, 1):
        gx = 360 + side * 230 + push * 300
        gy = 1080 + bob - push * (420 if side > 0 else 170)
        s_ = 1.0 + 0.3 * push
        d.rounded_rectangle([gx - 80 * s_, gy - 90 * s_, gx + 80 * s_, gy + 90 * s_], int(36 * s_), fill=(252, 140, 27), outline=OL, width=8)
        d.rectangle([gx - 80 * s_, gy + 40 * s_, gx + 80 * s_, gy + 90 * s_], fill=(206, 98, 14), outline=OL, width=6)
        for f in range(4):
            fx = gx - 54 * s_ + f * 36 * s_
            d.line([(fx, gy - 86 * s_), (fx, gy - 40 * s_)], fill=(206, 98, 14), width=6)
        d.rectangle([gx - 80 * s_, gy + 90 * s_, gx + 80 * s_, gy + 130 * s_], fill=(40, 168, 74), outline=OL, width=6)
        if side < 0:     # your right wrist is on the left of the frame when you look down at your own hands? no: palms out -> right glove on the right
            pass
        else:
            d.rectangle([gx - 70 * s_, gy + 96 * s_, gx + 70 * s_, gy + 110 * s_], fill=(225, 30, 40))   # red string, right wrist


def pov_dive(t, v, T):
    """first person: you throw yourself right, the world tilts, the ball screams past on the LEFT"""
    c = Cam(camX=0.0, camH=1.5, hor=520, f=1400)
    img = backdrop(520, stadium=True)
    pitch_near(img, c, 0.0)
    watchers(img, c, t)
    ground_shadow(img, c, 0.3, 8.3, 0.4)
    sprite_at(img, c, res(10, mouth="open"), 0.3, 8.3, height_m=1.6)
    push = ease_out(clamp(v / 0.7))
    # the ball: from the spot, growing, sweeping past the left edge with a long trail
    a = clamp((v - 0.1) / 0.75)
    sx, sy = c.p(0.0, 7.6)
    bx, by = lerp(sx, 40, a ** 1.6), lerp(sy, 980, a ** 1.6)
    size = lerp(1.2, 14.0, a ** 2.0)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for j in range(7):
        f0 = max(0.0, a - 0.04 * (j + 1))
        px, py = lerp(sx, 40, f0 ** 1.6), lerp(sy, 980, f0 ** 1.6)
        od.line([(px, py), (bx, by)], fill=(255, 255, 255, 120 - j * 14), width=int(size * 6 * (1 - j * 0.1)))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6)))
    draw_ball(img, bx, by + size * 6.5, size)
    eyes_gloves(img, push, t)
    slowmo_bars(img, 1.0)
    vignette(img, 0.4 + 0.3 * push)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(1 - 0.35 * push).convert("RGBA")
    return cam(img, 1.35 + 0.2 * push, 360 + 60 * push, 760 - 40 * push, rot=-16 * push)


def split_panel(t, v, T):
    """comic split: top — your face in the air, eyes on the ball; bottom — grass level, the ball spins over the line"""
    img = Image.new("RGBA", (FW, FH), (0, 0, 0, 255))
    # --- top panel
    top = backdrop(520, stadium=True).filter(ImageFilter.GaussianBlur(7))
    speed_lines(top, t, 380, 520, n=22, a=110, r0=230, r1=620)
    face = big(hero(pose="reach", gloves=True, mouth="open", look=-1), 24)
    face = big(hero(pose="reach", gloves=True, mouth="open", look=-1), 20)
    face = face.crop((0, 0, face.width, 21 * 20)).rotate(-14 + 4 * v, expand=True, resample=Image.NEAREST)
    top.alpha_composite(face, (int(380 - face.width / 2 + 30 * v), int(430 - face.height / 2)))
    d = ImageDraw.Draw(top)
    for k, (x0, y0) in enumerate(((560, 420), (590, 470), (540, 360))):          # sweat flying off
        yy = y0 - 40 * ((v * 2 + k * 0.3) % 1)
        d.ellipse([x0 + 30 * v, yy, x0 + 14 + 30 * v, yy + 22], fill=(190, 230, 255), outline=OL, width=2)
    # --- bottom panel: ground level at the goal line
    bot = Image.new("RGBA", (FW, FH), (70, 140, 74, 255))
    bd = ImageDraw.Draw(bot)
    for y in range(640, FH, 60):
        bd.rectangle([0, y, FW, y + 30], fill=(64, 132, 68))
    rng = random.Random(3)
    for _ in range(260):                                   # grass blades in the foreground
        x, y = rng.uniform(0, FW), rng.uniform(1000, FH)
        bd.line([(x, y), (x + rng.uniform(-6, 6), y - rng.uniform(14, 40))], fill=(46, 110, 52), width=4)
    for x in range(-40, FW, 40):                           # the net behind the line
        bd.line([(x, 640), (x + 60, 900)], fill=(230, 236, 240), width=3)
        bd.line([(x + 60, 640), (x, 900)], fill=(230, 236, 240), width=3)
    bd.rectangle([600, 600, 640, 960], fill=(250, 250, 252), outline=OL, width=5)   # the post
    bd.rectangle([0, 930, FW, 960], fill=(244, 248, 240))                          # the goal line
    a = ease_in_out(clamp(v / 0.85))
    bx, by, sz = lerp(200, 330, a), lerp(1150, 900, a), lerp(9.0, 6.0, a)
    for j in range(4):
        bd.arc([bx - 70 - j * 18, by - sz * 6.5 - 70 - j * 18, bx + 70 + j * 18, by - sz * 6.5 + 70 + j * 18], 150 + t * 900 % 360, 210 + t * 900 % 360,
               fill=(255, 255, 255), width=4)               # spin
    draw_ball(bot, bx, by, sz)
    if a > 0.95:
        impact_lines(bot, bx, by - sz * 6.5, T, T + 0.1, 12)
    # compose along a diagonal cut
    mask = Image.new("L", (FW, FH), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (FW, 0), (FW, 620), (0, 740)], fill=255)
    img.paste(bot, (0, 0))
    img.paste(top, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.line([(0, 740), (FW, 620)], fill=(255, 255, 255), width=14)
    d.line([(0, 752), (FW, 632)], fill=OL, width=4)
    slowmo_bars(img, 1.0)
    return img


def net_impact(t, v, t_hit):
    """from inside the goal: the ball rips into the net right at the lens"""
    c = Cam(camX=0.0, camH=1.0, hor=600)
    img = backdrop(600, stadium=True)
    pitch_persp(img, c, None)
    s = 1.6 * c.k(3.6) / 31
    sp = hero(view="back", pose="reach", gloves=True).resize((int(24 * s), int(39 * s)), Image.NEAREST).rotate(-90, expand=True, resample=Image.NEAREST)
    x, y = c.p(0.45, 3.6)                                   # you, on the grass (your right = screen right from in here)
    img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * s)))
    img = img.filter(ImageFilter.GaussianBlur(2))
    hit = 0.35
    a = clamp(v / hit)
    bx, by = lerp(320, 190, a), lerp(760, 720, a)
    bul = 0.0 if v < hit else math.exp(-(v - hit) * 5) * (1 + 0.3 * math.sin((v - hit) * 40))
    if v < hit:
        draw_ball(img, bx, by, lerp(1.0, 7.0, a ** 2))
    net = Image.new("RGBA", img.size, (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    cell = 52

    def disp(px, py):
        if bul <= 0:
            return px, py
        dx, dy = px - bx, py - by
        r = math.hypot(dx, dy) + 1e-3
        f = bul * 110 * math.exp(-(r / 260) ** 2)
        return px + dx / r * f * 0.5, py + dy / r * f * 0.5
    for kk in range(-30, 50):
        p1 = [disp(kk * cell + j * cell, j * cell) for j in range(-2, 32)]
        p2 = [disp(kk * cell - j * cell, j * cell) for j in range(-2, 32)]
        nd.line(p1, fill=(250, 250, 255, 170), width=4)
        nd.line(p2, fill=(250, 250, 255, 170), width=4)
    img.alpha_composite(net)
    if v >= hit:
        draw_ball(img, bx, by - 20, 7.0 + 2.5 * bul)
        impact_lines(img, bx, by - 60, t_hit, t, 16)
    img = flash(img, 0.55 * clamp(1 - abs(v - hit) * 8), (255, 40, 40))
    return cam(img, 1.05 + 0.1 * v, 360, 720, *shake(t, t_hit, .45, 22))



def taker_face(t, v, T):
    """close-up: in the stutter of his run-up #10 glances into YOUR right corner (screen right) — the bait"""
    img = backdrop(560, stadium=True).filter(ImageFilter.GaussianBlur(6))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, FW, FH], fill=(78, 140, 76))
    turn = clamp((v - 0.25) / 0.2)
    sp = res(10, mouth="smile" if v > 0.55 else "flat", blink=False)
    sp = sp.rotate(-5 * turn, resample=Image.NEAREST, expand=False)
    S = 30
    top = 1400 - 39 * S
    paste(img, sp, S, 360 + 12 * turn, 1400)
    d = ImageDraw.Draw(img)
    for ex in (6, 10):                            # redraw the eyes: whites 2 px wide, pupils pushed to screen right
        x0 = 360 + 12 * turn - 12 * S + (3 + ex) * S
        y0 = top + (10 + 3) * S
        d.rectangle([x0, y0, x0 + 2 * S - 1, y0 + 2 * S - 1], fill=(250, 250, 250))
        px = x0 + (S if turn > 0.5 else S // 2)
        d.rectangle([px, y0, px + S - 1, y0 + 2 * S - 1], fill=OL)
    if turn > 0.5:                                 # the beam of his look sweeps out to screen right (your right corner)
        ex_ = 360 + 12 * turn - 12 * S + (3 + 11) * S + S // 2
        ey_ = top + 14 * S
        L = ease_out(clamp((v - 0.45) / 0.35))
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        tx, ty = lerp(ex_, 760, L), lerp(ey_, 380, L)
        od.polygon([(ex_, ey_ - 12), (ex_, ey_ + 12), (tx, ty + 80 * L), (tx, ty - 80 * L)], fill=(255, 235, 120, 190))
        od.polygon([(ex_, ey_ - 4), (ex_, ey_ + 4), (tx, ty + 24 * L), (tx, ty - 24 * L)], fill=(255, 255, 230, 230))
        img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(4)))
        glow_ring(img, ex_, ey_, 34 + 8 * math.sin(t * 20), 0.85, (255, 255, 220))
    vignette(img, 0.5)
    return cam(img, 1.0 + 0.12 * v, 400, 800)


def corner_insert(t, v):
    """what you see: the corner he just looked at — YOUR right corner lights up. You believe him."""
    c = Cam(camX=1.6, camH=1.2, hor=560)
    img = backdrop(560, stadium=True)
    pitch_persp(img, c, Zgoal=3.4, box=False)
    goal3d(img, c, 3.4, X=0.0, w=5.0, h=2.0, back=True)
    gx, gy = c.p(2.1, 3.5, 1.2)
    glow_ring(img, gx, gy, 90 + 60 * ease_out(v) + 8 * math.sin(t * 18), 0.85, (255, 230, 140))
    glow(img, gx, gy, 220, (255, 230, 140), 0.35 * (1 - v * 0.5))
    vignette(img, 0.45)
    return cam(img, 1.05 + 0.1 * v, gx, gy + 120)


def strike_insert(t, v, T, t_contact):
    c2 = Cam(camX=0.0, camH=0.5, hor=640)
    img = backdrop(640, stadium=True)
    pitch_persp(img, c2, None)
    ph = clamp(v)
    shadow(img, 360, 1150, 300, 50, 100)
    hop = 30 * math.sin(clamp((ph - 0.55) / 0.45) * math.pi) if ph > 0.55 else 0
    paste(img, res(10, pose="strikeF", phase=ph, mouth="flat"), 17, 360, 1160 - hop)
    contact = 0.45
    if ph < contact:
        draw_ball(img, 330, 1150, 4.0)
    else:                                         # calm side-foot: rolls away low to screen LEFT (his right = YOUR left)
        w_ = (ph - contact) / (1 - contact)
        draw_ball(img, lerp(330, 90, w_), lerp(1150, 1170, w_), lerp(4.0, 4.6, w_))
        impact_lines(img, 330, 1110, t_contact, t, 12)
    shoot_bar(img)
    slowmo_bars(img, 1.0 if 0.35 < ph < 0.6 else 0.0)
    return cam(img, 1.0, 360, 800, *shake(t, t_contact, .15, 6))


def s_kick(t, u, T):
    """he baits you: a glance to your right, you go early — then he rolls it calmly into the other corner"""
    G0, C0, GO, K0, K1 = 0.12, 0.19, 0.19, 0.42, 0.54   # glance | his corner | you commit | strike close-up | your view
    if u < G0:
        return taker_face(t, u / G0, T)
    if u < C0:
        return corner_insert(t, (u - G0) / (C0 - G0))
    if K0 <= u < K1:
        return strike_insert(t, (u - K0) / (K1 - K0), T, T + (K0 + 0.45 * (K1 - K0)) * D(2))
    img, c = keeper_set(t)
    watchers(img, c, t)
    if u < K0:                                   # he is still arriving at the ball
        taker_and_ball(img, c, t)
    else:
        taker_and_ball(img, c, t, after=clamp((u - K1) / (1 - K1)))
    side = 1 if RIGHT else -1
    dv = clamp((u - GO) / 0.21)                  # one continuous flight, ~0.6 s from push-off to landing
    f = ease_in_out(dv)
    # the ball: after the strike it rolls slowly into the empty LEFT corner, over the line, into the net
    ball_world = None
    if u < K1:
        ball_at(img, c, 0.0, 7.6, 0.0)
    else:
        a = clamp((u - K1) / (1 - K1))
        bxw, bzw = lerp(0.0, -2.0, a), lerp(7.6, -0.6, a)
        ball_world = (bxw, bzw)
        if bzw > KZ:                             # still in front of you: draw it before you
            ball_at(img, c, bxw, bzw, 0.0)
    turf(img, dv / 0.6 if dv < 0.6 else 0.0)
    draw_dive(img, f if dv > 0 else 0.0, side)
    if ball_world and ball_world[1] <= KZ:
        ball_at(img, c, ball_world[0], ball_world[1], 0.0)
    posts_fg(img, c)
    shoot_bar(img)
    return cam(img, 1.03, 360, 820, *shake(t, T + (GO + 0.21) * D(2), .25, 8))


def top_down_you(t, v):
    img = Image.new("RGBA", (FW, FH), (74, 138, 72, 255))
    d = ImageDraw.Draw(img)
    for k in range(10):
        d.rectangle([0, k * 140, FW, k * 140 + 70], fill=(68, 130, 66))
    d.rectangle([0, 380, FW, 396], fill=(240, 244, 236))                     # the goal line
    for x in range(0, FW, 36):                                               # the net's shadow behind it
        d.line([(x, 300), (x + 36, 380)], fill=(60, 110, 60), width=3)
    sp = big(hero(pose="reach", gloves=True, blink=0.55 < v < 0.62, mouth="sad"), 15).rotate(-90, expand=True, resample=Image.NEAREST)
    img.alpha_composite(sp, (int(300 - sp.width / 2), int(760 - sp.height / 2)))
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for k in range(3):                                                       # shadows of the winners running past
        x = lerp(-200, 900, (v * 1.3 + k * 0.35) % 1.3 / 1.3)
        y = 560 + k * 180
        od.ellipse([x - 90, y - 40, x + 90, y + 40], fill=(0, 0, 0, 90))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6)))
    vignette(img, 0.45)
    return cam(img, 1.0 + 0.12 * v, 400, 760)


def s_result(t, u, T):
    """reverse angle from behind the penalty spot: the ball in the net (or out), keeper on the grass"""
    c = Cam(camX=0.0, camH=1.7, hor=470)
    img = backdrop(470, stadium=True)
    pitch_persp(img, c, Zgoal=9.0)
    goal3d(img, c, 9.0)
    s = 1.6 * c.k(9.0) / 31
    # from this side the hero's right is screen LEFT
    kx_side = -1.4 if RIGHT else 1.4
    sp = hero(pose="reach", gloves=True, blink=RIGHT, mouth="sad" if RIGHT else "grin").resize((int(24 * s), int(39 * s)), Image.NEAREST)
    sp = sp.rotate(90 if RIGHT else -90, expand=True, resample=Image.NEAREST)
    x, y = c.p(kx_side, 9.0)
    if RIGHT or u < 0.4:
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height + 3 * s)))
    if RIGHT and u < 0.4:
        return net_impact(t, u / 0.4, T + 0.35 * 0.4 * D(3))
    if RIGHT and u < 0.7:
        return top_down_you(t, (u - 0.4) / 0.3)
    if RIGHT:
        if u >= 0.7:      # cut: the reserves celebrate, spread out, in front of the stand
            img = backdrop(600, stadium=True)
            c2 = Cam(camX=0.0, camH=1.6, hor=600)
            pitch_persp(img, c2, None)
            for k, (X, Z) in enumerate(((0.0, 5.0), (-1.7, 5.8), (1.7, 5.8))):
                ground_shadow(img, c2, X, Z, 0.4)
                sprite_at(img, c2, res((10, 5, 4)[k], pose="celebrate", mouth="grin"), X, Z,
                          Y=abs(math.sin(t * 7 + k * 1.3)) * 0.3, height_m=1.6)
            shoot_bar(img, res_win=True)
            return cam(img, 1.0 + 0.05 * u, 360, 860)
        bx, by = c.p(1.8, 9.9, 0.3)
        draw_ball(img, bx, by + 10, 1.0)
    else:
        if u >= 0.4:
            ground_shadow(img, c, 1.2, 9.0, 0.45)
            sprite_at(img, c, hero(pose="celebrate", gloves=True, mouth="grin"), 1.2, 9.0,
                      Y=abs(math.sin(t * 7)) * 0.3, height_m=1.6)
        for k, X in enumerate((-2.6, 2.8)):
            sprite_at(img, c, first((4, 6)[k], pose="run", phase=t * 2.4), X, lerp(4.0, 7.5, u), height_m=1.6)
    shoot_bar(img, res_win=RIGHT)
    return cam(img, 1.15 + 0.05 * u, 360, 640)


def s_sheet(t, u, T):
    """the coach's clipboard: GK for Saturday"""
    img, c = fb.present_pitch(t)
    img = img.filter(ImageFilter.GaussianBlur(5))
    CB = 1500
    paste(img, coach(look=1, mouth="flat", blink=0.6 < u < 0.63), 22, 230, CB)
    top = CB - 39 * 22
    d = ImageDraw.Draw(img)
    x, y = 330, 880
    d.rounded_rectangle([x, y, x + 260, y + 300], 14, fill=(250, 246, 236), outline=OL, width=6)
    d.rectangle([x + 85, y - 16, x + 175, y + 20], fill=(120, 120, 130), outline=OL, width=4)
    d.text((x + 130, y + 60), "SATURDAY", font=font(800, 28), fill=OL, anchor="mm")
    d.text((x + 70, y + 140), "GK:", font=font(800, 34), fill=OL, anchor="mm")
    k = clamp((u - 0.25) / 0.4)
    name = "DIXON" if RIGHT else "#0"
    d.text((x + 120, y + 140), name[:int(len(name) * k + 0.999)] if k > 0 else "", font=font(800, 34),
           fill=(40, 90, 200) if RIGHT else (40, 150, 80), anchor="lm")
    # his left hand holds the board's bottom edge; his right arm comes across from the shoulder with the pen
    shoulder = (230 - 12 * 22 + 16 * 22, top + 19 * 22)
    px = x + 120 + 18 * len(name) * k if u > 0.15 else x + 110
    hand = (px + 30, y + 190)
    d.line([shoulder, ((shoulder[0] + hand[0]) / 2, hand[1] + 40), hand], fill=OL, width=40)
    d.line([shoulder, ((shoulder[0] + hand[0]) / 2, hand[1] + 40), hand], fill=(30, 40, 80), width=30)
    d.line([(px, y + 150), (hand[0] + 4, hand[1] - 6)], fill=(30, 30, 40), width=10)
    d.rounded_rectangle([hand[0] - 26, hand[1] - 26, hand[0] + 26, hand[1] + 26], 12, fill=SKIN["light"][0], outline=OL, width=5)
    d.rounded_rectangle([x - 10, y + 270, x + 50, y + 320], 12, fill=SKIN["light"][0], outline=OL, width=5)
    return cam(img, 1.0 + 0.05 * u, 360, 860)


def s_stare(t, u, T):
    """Dixon (blue #2) waves at the coach — the coach's head turns away from him, to YOU, alone and downcast"""
    img, c = fb.present_pitch(t)
    ground_shadow(img, c, 1.3, 8.6, 0.4)
    sprite_at(img, c, hero(gloves=True, look=-1, mouth="sad", blink=int(t * 2) % 5 == 0), 1.3, 8.6,
              Y=0.015 * math.sin(t * 2.5), height_m=1.6)
    ground_shadow(img, c, -1.05, 5.8, 0.4)
    wave = int(t * 4) % 2 == 0 and u < 0.6
    sprite_at(img, c, dixon(pose="celebrate" if wave else "stand", mouth="grin" if u < 0.6 else "flat"), -1.05, 5.8,
              Y=0.15 * abs(math.sin(t * 7)) if u < 0.6 else 0.0, height_m=1.6)
    turn = ease_in_out(clamp((u - 0.25) / 0.25))
    cb = coach(view="back")
    paste(img, cb, 24, 420, 1560)
    d = ImageDraw.Draw(img)
    k = ease_in_out(clamp((u - 0.45) / 0.55))
    hx, hy = c.p(1.3, 8.6, 0.9)
    return cam(img, 1.0 + 0.8 * k, lerp(360, hx, k), lerp(820, hy, k))


def s_flash84(t, u, T):
    """quick: MAY 1984 card, then the standing terrace"""
    if u < 0.45:
        return fb.s_card(t, 0.2 + u / 0.45 * 0.8, T)
    return fb.s_terrace(t, (u - 0.45) / 0.55, T)


def s_grandad84(t, u, T):
    if u < 0.5:
        return fb.s_grandad_intro(t, u / 0.5, T)
    return fb.s_same(t, (u - 0.5) / 0.5, T)


def face_frame(sprite, t, v, bg):
    img = bg.copy()
    paste(img, sprite, 26, 360, 1460 + 20 * v)
    vignette(img, 0.55)
    return cam(img, 1.0 + 0.15 * ease_in_out(v), 360, 800)


def s_reveal(t, u, T):
    """stretcher -> push in on young #9's face -> the tape glitches -> the SAME face, today: the coach"""
    if u < 0.45:
        return fb.s_stretcher(t, u / 0.45, T)
    bg84 = old_stadium(560).filter(ImageFilter.GaussianBlur(6))
    ImageDraw.Draw(bg84).rectangle([0, 560, FW, FH], fill=(60, 90, 56))
    if u < 0.75:
        v = (u - 0.45) / 0.3
        img = face_frame(young_coach(mouth="flat", look=0, blink=0.6 < v < 0.66), t, v, bg84)
        rain84(img, t, 110)
        return img
    v = (u - 0.75) / 0.25
    bg = fb.present_pitch(t)[0].filter(ImageFilter.GaussianBlur(6))
    img = face_frame(coach(mouth="flat", look=0), t, 1.0, bg)
    img = ImageEnhance.Color(img.convert("RGB")).enhance(0.45).convert("RGBA")
    if v < 0.3:                                   # the tape tears between the two faces
        img = vhs(img, t, 2.0)
        rng = random.Random(int(t * 30))
        for _ in range(10):
            y = rng.uniform(0, FH); hgt = rng.uniform(8, 50)
            band = img.crop((0, int(y), FW, int(y + hgt)))
            img.paste(band, (int(rng.uniform(-50, 50)), int(y)))
    return img


def s_walk(t, u, T):
    """the coach walks off without looking back; you stay in the goalmouth"""
    c = Cam(camX=0.0, camH=1.7, hor=470)
    img = backdrop(470, stadium=True)
    pitch_persp(img, c, Zgoal=9.0)
    goal3d(img, c, 9.0)
    ground_shadow(img, c, 0.3, 9.0, 0.4)
    sprite_at(img, c, hero(gloves=True, look=1 if u < 0.8 else 0, mouth="sad", blink=int(t * 2) % 5 == 0), 0.3, 9.0,
              Y=0.04 * abs(math.sin(t * 2.5)), height_m=1.6)
    w = ease_in_out(u)
    Z = lerp(3.2, 6.0, w)                          # stays in front of the goal line (Z 9)
    X = lerp(0.95, 4.6, w)                         # away to the side, out of frame right — you stay in view
    if True:
        ground_shadow(img, c, X, Z, 0.4)
        sprite_at(img, c, coach(view="back", pose="run", phase=t * 1.2), X, Z, height_m=1.75)
    return cam(img, 1.05 + 0.05 * u, 360, 680)


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
    paste(img, grandad(mouth="flat", blink=state == "silent" and int(t * 2) % 4 == 0), 8, cx, cy + 120)
    d = ImageDraw.Draw(img)
    d.text((cx, cy - 275), "GRANDAD", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    sec = max(0, int(t - STARTS[17] - 1.2))
    sub = {"calling": "calling...", "talk": f"00:{sec:02d}", "silent": f"00:{sec:02d}",
           "ended": "CALL ENDED", "msg": "1 NEW MESSAGE"}[state]
    d.text((cx, cy - 232), sub, font=font(600 if state != "ended" else 800, 26), fill=(180, 190, 220) if state != "ended" else (240, 80, 80), anchor="mm")
    # voice wave: moving while you talk, a flat line in the silence
    y0 = cy + 170
    pts = []
    for i in range(41):
        x = cx - 150 + i * 7.5
        amp = 26 * math.sin(i * 0.9 + t * 14) * math.sin(i / 40 * math.pi) if state == "talk" else 0
        pts.append((x, y0 + amp))
    if state != "msg":
        d.line(pts, fill=(110, 222, 120) if state == "talk" else (120, 130, 160), width=5)
    if state not in ("ended", "msg"):      # outgoing call: one red hang-up button
        r = 36
        d.ellipse([cx - r, cy + 250 - r, cx + r, cy + 250 + r], fill=(230, 60, 60), outline=OL, width=5)


def s_night(t, u, T):
    img = dorm_night(t)
    paste(img, hero(pose="whisper", mouth="flat", blink=int(t * 2) % 6 == 0), 11, 120, 1200 - 6 * abs(math.sin(t * 2)))
    ImageDraw.Draw(img).rounded_rectangle([120 + 3 * 11, 1200 - 39 * 11 + 13 * 11, 120 + 6 * 11, 1200 - 39 * 11 + 19 * 11], 6,
                                          fill=(24, 26, 36), outline=OL, width=3)          # the phone at his ear
    phone_ui(img, 400, 820, "calling" if u < 0.6 else "talk", t, 0.9 * spring(t - T - 0.2, 13, 7))
    return cam(img, 1.0 + 0.04 * u, 360, 760)


def s_ask(t, u, T):
    img = dorm_night(t).filter(ImageFilter.GaussianBlur(4))
    phone_ui(img, 330, 820, "talk" if u < 0.7 else "silent", t)
    return cam(img, 1.0 + 0.15 * ease_in_out(u), 360, 760)


def s_hangup(t, u, T):
    img = dorm_night(t).filter(ImageFilter.GaussianBlur(4))
    phone_ui(img, 330, 820, "silent" if u < 0.62 else "ended", t)
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
    phone_ui(img, 330, 820, "msg", t)
    d = ImageDraw.Draw(img)
    typing = u < 0.3 and not (0.12 < u < 0.18)
    if typing:                                     # "..." Grandad is typing (phone UI, no bubble)
        for j in range(3):
            r = 10 + 4 * abs(math.sin(t * 8 + j))
            d.ellipse([290 + j * 40 - r, 960 - r, 290 + j * 40 + r, 960 + r], fill=(200, 205, 225))
    land = T + 0.3 * D(20)
    if u >= 0.3:
        n = int(clamp((t - land) / 0.5) * 19)
        msg = "STAY AWAY FROM HIM."
        l1, l2 = msg[:10], msg[10:]
        d.text((330, 950), l1[:n], font=font(800, 40), fill=(255, 90, 90), anchor="mm", stroke_width=3, stroke_fill=OL)
        if n > 10:
            d.text((330, 1000), l2[:n - 10], font=font(800, 40), fill=(255, 90, 90), anchor="mm", stroke_width=3, stroke_fill=OL)
    vignette(img, 0.5)
    return cam(img, 1.0 + 0.12 * ease_in_out(u), 360, 900, *shake(t, land, .25, 6))


CARDS = [(170, "ASK COACH", "KNOCK ON HIS DOOR", C_Y), (450, "STAY AWAY", "LISTEN TO GRANDAD", C_R)]


def choice_cards(img, t, T0):
    d = ImageDraw.Draw(img)
    for i, (x, lab, sub, c) in enumerate(CARDS):
        k = spring(t - T0 - i * 0.15, 13, 7)
        if k < 0.05:
            continue
        hl = 0.5 + 0.5 * math.sin(t * 3.2 + i * math.pi)
        w, h = 262 * k * (1 + 0.03 * hl), 440 * k * (1 + 0.03 * hl)
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
                d.text((x, y - 98), "STAY AWAY", font=font(800, 15), fill=(255, 90, 90), anchor="mm")
                d.text((x, y - 78), "FROM HIM.", font=font(800, 15), fill=(255, 90, 90), anchor="mm")
            d = ImageDraw.Draw(img)
            d.text((x, y + 110), lab, font=font(800, 31), fill=c, anchor="mm", stroke_width=4, stroke_fill=OL)
            d.text((x, y + 160), sub, font=font(700, 17), fill=(220, 224, 240), anchor="mm")


def typing_box(img, t, T0):
    d = ImageDraw.Draw(img)
    y = 930 + UY * 0.4
    d.rounded_rectangle([50, y, 590, y + 70], 18, fill=(16, 18, 36), outline=(255, 255, 255), width=3)
    words = ["ASK COACH", "STAY AWAY"]
    k = (t - T0) / 1.1
    wi = min(1, int(k))
    w = words[wi]
    n = int(len(w) * clamp((k - wi) * 2)) if k < 2 else len(w)
    d.text((80, y + 35), w[:n] + ("|" if int(t * 4) % 2 else ""), font=font(800, 30), fill=(255, 255, 255), anchor="lm")


def s_choice(t, u, T):
    img = fb.choice_bg()
    choice_cards(img, t, T - 0.2)
    typing_box(img, t, T + 0.3)
    pill(img, 310, 340 + UY, "VOTE BEFORE FRIDAY", (200, 50, 60), spring(t - T - 0.3, 13, 7), 28)
    return cam(img, 1.0 + 0.02 * u, 360, 760)


def s_end(t, u, T):
    img = fb.choice_bg()
    img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (10, 12, 30)), 0.88 * clamp((t - T) / 0.3)).convert("RGBA")
    d = ImageDraw.Draw(img)
    k = spring(t - T, 16, 7)
    py = lerp(1400, 420 + UY * 0.4, clamp(k, 0, 1.2))
    d.rounded_rectangle([24, py, 600, py + 560], 34, fill=(14, 18, 44), outline=C_Y, width=6)
    paste(img, hero(mouth="flat", gloves=True, blink=int(t * 2.3) % 5 == 0), 9, 140, py + 330)
    d.text((390, py + 90), "DON'T MISS", font=font(800, 40), fill=(255, 255, 255), anchor="mm")
    d.text((390, py + 150), "PART 8", font=font(800, 70), fill=C_Y, anchor="mm", stroke_width=4, stroke_fill=OL)
    tap = T + 0.8
    after = t > tap
    label = ("SUBSCRIBED" if after else "SUBSCRIBE") if PLATFORM == "youtube" else ("FOLLOWING" if after else "+ FOLLOW")
    pul = 1 + (0.05 * math.sin(t * 9) if not after else 0)
    bw, bh = 300 * pul, 96 * pul
    bx, by = 390, py + 280
    d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], 22, fill=(60, 64, 90) if after else (234, 46, 72), outline=OL, width=5)
    d.text((bx, by), label, font=font(800, 36 if after else 40), fill=(255, 255, 255), anchor="mm")
    if after and t < tap + 0.5:
        glow_ring(img, bx, by, 60 + 300 * (t - tap), 0.8 * (1 - (t - tap) / 0.5), C_Y)
    if t < tap + 0.4:
        gx = lerp(540, bx + 90, ease_in_out((t - T) / 0.8)); gy = by - 20 + 60 * (1 - ease_in_out((t - T) / 0.8))
        d.rounded_rectangle([gx - 40, gy, gx + 40, gy + 90], 18, fill=(252, 140, 27), outline=OL, width=5)
        d.rounded_rectangle([gx - 12, gy - 40, gx + 12, gy + 20], 10, fill=(252, 140, 27), outline=OL, width=5)
        d.rectangle([gx - 40, gy + 90, gx + 40, gy + 104], fill=(225, 30, 40), outline=OL, width=3)
    for x, lab, cc in ((180, "ASK COACH", C_Y), (440, "STAY AWAY", C_R)):
        hop = 5 * math.sin(t * 5 + x)
        d.rounded_rectangle([x - 118, py + 400 - hop, x + 118, py + 470 - hop], 18, fill=(30, 36, 76), outline=cc, width=5)
        d.text((x, py + 435 - hop), lab, font=font(800, 30), fill=cc, anchor="mm")
    d.text((312, py + 520), "VOTE IN THE COMMENTS", font=font(800, 28), fill=(255, 255, 255), anchor="mm")
    return img


SCENES = [s_hook, s_vote, s_kick, s_result, s_sheet, s_stare, fb.s_glove, fb.s_pale, s_flash84, s_grandad84,
          fb.s_hang, fb.s_jump, fb.s_impact, s_reveal, fb.s_mud, fb.s_today, s_walk, s_night, s_ask, s_hangup,
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
    if i in FLASH and not (SCENES[i] is s_reveal and u >= 0.75):
        img = vhs(img, t, 0.8)
        if not (i == 9 and u > 0.5):
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
