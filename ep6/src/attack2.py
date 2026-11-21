"""Two camera variants of the same move: #7 passes to #9, first-time shot, curved arc, goal."""
from ep6 import *
from ep6 import _xzy
from persp import pretty_arc


def _move(w):
    """shared timeline. returns dict with ball pos (world), phase flags"""
    P7, P9 = (-1.6, 9.0), (1.3, 12.5)
    GZ = 20.0
    pas = arc((P7[0] + 0.4, P7[1] + 0.1, 0.05), (P9[0] - 0.4, P9[1] - 0.1, 0.05), apex=0.0)
    shot = arc((P9[0] - 0.4, P9[1] - 0.1, 0.1), (-2.2, GZ + 0.3, 1.7), apex=0.45, curve=-1.4)   # curling into the top-left corner
    return P7, P9, GZ, pas, shot


def variant_A(t, w):
    """their angle: behind the attackers, our goal in the distance"""
    P7, P9, GZ, pas, shot = _move(w)
    c = Cam(camX=0.2, camH=2.5, hor=430)
    img = backdrop(430, stadium=True)
    pitch_persp(img, c, Zgoal=GZ)
    goal3d(img, c, GZ)
    scored = w >= 0.78
    kick9 = 0.38
    # our keeper: ready, then a full-stretch dive to his LEFT (screen left) that falls just short
    dive = clamp((w - (kick9 + 0.06)) / 0.5)
    if dive <= 0:
        ground_shadow(img, c, 0, GZ, 0.45)
        sprite_at(img, c, hero(pose="ready", gloves=True), 0, GZ, height_m=1.6)
    else:
        k_ = c.k(GZ); sc_ = 1.6 * k_ / 31
        sp = hero(pose="reach", gloves=True, mouth="open").resize((int(24 * sc_), int(39 * sc_)), Image.NEAREST)
        lift = 0.55 * math.sin(min(dive, 0.6) / 0.6 * math.pi / 2) * (1 - clamp((dive - 0.75) / 0.25))
        X = -1.4 * ease_out(dive)
        rot = 70 * ease_out(min(1, dive * 1.4))      # stretched out, tilting up toward the corner
        sp = sp.rotate(rot, expand=True, resample=Image.NEAREST)
        ground_shadow(img, c, X, GZ, 0.9, 80)
        x, y = c.p(X, GZ, 0.45 + lift)
        img.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
    for X, Z, n in ((-2.6, 10.5, 4), (3.0, 11.5, 5)):          # our two defenders, already beaten
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, ours(n, pose="run", phase=t * 2.4), X, Z, height_m=1.55)
    ground_shadow(img, c, *P9, 0.35)
    sprite_at(img, c, opp(9, view="back", pose="kickL" if w > kick9 - 0.06 else "stand", phase=clamp((w - kick9 + 0.06) / 0.1)), *P9, height_m=1.55)   # left foot curler
    ground_shadow(img, c, *P7, 0.35)
    sprite_at(img, c, opp(7, view="back", pose="kick" if w < 0.12 else "stand", phase=clamp(w / 0.1)), *P7, height_m=1.55)
    if w < kick9:                      # the pass, with its dashed line
        a = clamp((w - 0.06) / (kick9 - 0.06))
        dotted_path(img, c, pas, 1.0, from_=a)
        ball_trail(img, c, pas, a, 0.2)
        ball_at(img, c, *at(pas, a))
        if w > 0.24:                   # the shot curve draws itself just before he strikes
            pretty_arc(img, c, shot, ease_out((w - 0.24) / (kick9 - 0.24)), 0.0)
    elif not scored:
        a = clamp((w - kick9) / (0.78 - kick9))
        pretty_arc(img, c, shot, 1.0, from_=a)
        ball_trail(img, c, shot, a, 0.12)
        ball_at(img, c, *at(shot, a))
    else:
        b = clamp((w - 0.78) / 0.15)
        bx, by = c.p(-2.2, GZ + 0.9, 1.7 * (1 - b) ** 2)   # ONE ball: hits the net, drops onto the grass
        draw_ball(img, bx, by + 6, 0.6)
        impact_lines(img, *c.p(-2.2, GZ + 0.6, 1.7), 0.78, w, 10)
    img = flash(img, 0.4 * clamp(1 - abs(w - 0.8) * 10), (255, 50, 50))
    zoom = 1.0 + 0.6 * ease_in_out(clamp((w - kick9) / 0.4))
    return cam(img, zoom, *c.p(-0.9, GZ, 0.9))


def variant_B(t, w):
    """our angle: behind our keeper, the attackers come at us"""
    P7, P9, GZ, pas, shot = _move(w)
    # mirror the move into keeper space: Z' = GZ - Z
    m = lambda p: (-p[0], GZ - p[1], p[2])
    pas_m = [m(p) for p in pas]
    shot_m = [m(p) for p in shot]
    Q7, Q9 = (-P7[0], GZ - P7[1]), (-P9[0], GZ - P9[1])
    c = Cam(camX=0.0, camH=1.9, hor=520)
    img = backdrop(520, stadium=True)
    pitch_near(img, c, 0.0)
    for X, Z, n in ((2.6, 9.5, 4), (-3.0, 8.5, 5)):
        ground_shadow(img, c, X, Z, 0.35)
        sprite_at(img, c, ours(n, view="back", pose="run", phase=t * 2.4), X, Z, height_m=1.55)
    kick9 = 0.38
    ground_shadow(img, c, *Q7, 0.35)
    sprite_at(img, c, opp(7, pose="kick" if w < 0.12 else "stand", phase=clamp(w / 0.1)), *Q7, height_m=1.55)
    ground_shadow(img, c, *Q9, 0.35)
    sprite_at(img, c, opp(9, pose="kick" if w > kick9 - 0.06 else "stand", phase=clamp((w - kick9 + 0.06) / 0.1)), *Q9, height_m=1.55)
    scored = w >= 0.78
    if w < kick9:
        a = clamp((w - 0.06) / (kick9 - 0.06))
        dotted_path(img, c, pas_m, 1.0, from_=a)
        ball_trail(img, c, pas_m, a, 0.2)
        ball_at(img, c, *at(pas_m, a))
        if w > 0.24:
            dotted_path(img, c, shot_m, 0.93, from_=0.0, col=(255, 255, 255))
    elif not scored:
        a = clamp((w - kick9) / (0.78 - kick9))
        dotted_path(img, c, shot_m, 0.93, from_=a)
        ball_trail(img, c, shot_m, min(a, 0.93), 0.12)
        ball_at(img, c, *at(shot_m, min(a, 0.93)))
    paste(img, hero(view="back", pose="ready", gloves=True), 13, 330, 1430)
    if scored:
        glow_ring(img, 330, 1180, 120, 0.6 * clamp(1 - (w - 0.78) * 4), (255, 80, 80))
        impact_lines(img, 330, 1180, 0.78, w, 12)
    img = flash(img, 0.4 * clamp(1 - abs(w - 0.8) * 10), (255, 50, 50))
    zoom = 1.0 + 0.15 * ease_in_out(clamp((w - kick9) / 0.4))
    return cam(img, zoom, 340, 900)


if __name__ == "__main__":
    for name, fn in (("A", variant_A),):
        ws = (0.1, 0.3, 0.45, 0.6, 0.72, 0.9)
        ims = []
        for w in ws:
            im = fn(1.0 + w, w).convert("RGBA")
            caption(im, [("VARIANT", -1, C_Y), (name, -1, C_W)], 9, size=50)
            ims.append(im.convert("RGB").resize((270, 480)))
        o = Image.new("RGB", (270 * 6, 480))
        for i, im in enumerate(ims):
            o.paste(im, (270 * i, 0))
        o.save(f"frames6/EP6_variant_{name}.png")
