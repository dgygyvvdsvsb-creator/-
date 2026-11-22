"""EP4 cast on top of the EP5/EP6 style engine."""
from style import *

RS = (210, 52, 56)           # Riverside academy: red
TRI = (150, 156, 172)        # trialists: grey shirts


def mum(**kw):
    """Mum: long brown hair (ponytail), blue top, dark trousers"""
    return person(Kit((70, 108, 189), (40, 44, 70), (40, 44, 70)), skin="light", hair="brown", style="pony",
                  trousers=True, **kw)


def doctor(**kw):
    """doctor: white coat over blue scrubs, stethoscope"""
    def steth(d, ox, oy):
        P = lambda x, y, c: d.point((ox + x, oy + y), fill=c)
        for x, y in ((6, 9), (6, 10), (7, 11), (8, 12), (9, 12), (10, 11), (11, 10), (11, 9)):
            P(x, y, (60, 64, 80))
        P(8, 13, (190, 196, 210))
        d.rectangle([ox + 7, oy + 8, ox + 10, oy + 8], fill=(90, 130, 200))      # scrubs at the neck
    return person(Kit((246, 246, 250), (90, 130, 200), (90, 130, 200)), skin="brown", hair="black", style="short",
                  trousers=True, extra=[steth], **kw)


def academy(n, **kw):
    if n == 9:
        return mason(**kw)
    sk = {7: "dark", 4: "tan", 5: "light", 8: "brown"}.get(n, "light")
    hr = {7: "black", 4: "black", 5: "ginger", 8: "black"}.get(n, "dark")
    return person(Kit(RS, (245, 245, 250), RS, n), skin=sk, hair=hr, style="short", **kw)


def trialist(n, **kw):
    sk = {3: "tan", 5: "brown", 6: "light", 8: "dark"}.get(n, "light")
    hr = {3: "black", 5: "black", 6: "blond", 8: "black"}.get(n, "brown")
    return person(Kit(TRI, (40, 44, 60), TRI, n, num_col=(40, 44, 60)), skin=sk, hair=hr, style="short", **kw)


def grandad_cane(pose="stand", mouth="smile", blink=False, look=0, cane_up=0.0):
    """Grandad standing with the cane in his right hand (screen-left). cane_up 0..1 raises it over his head."""
    g = grandad(pose=pose, mouth=mouth, blink=blink, look=look)
    W, H = 30, 48
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ox, oy = 6, 9
    if cane_up <= 0:
        c = cane(11)
        im.alpha_composite(c, (ox + 1, oy + 22))
        im.alpha_composite(g, (ox, oy))
        # hand over the handle
        d = ImageDraw.Draw(im)
        sk = SKIN["old"][0]
        d.rectangle([ox + 3, oy + 24, ox + 5, oy + 26], fill=sk)
        d.rectangle([ox + 2, oy + 24, ox + 2, oy + 26], fill=OL)
    else:
        im.alpha_composite(g, (ox, oy))
        c = cane(14).rotate(180, expand=True, resample=Image.NEAREST)
        im.alpha_composite(c, (ox - 3, max(0, oy + 22 - int(22 * cane_up))))
    return im


def sheet(path):
    rows = [
        [hero(), hero(view="back", gloves=True), hero(pose="run", phase=0.25, gloves=True), hero(pose="sit"),
         hero(pose="celebrate", gloves=True), hero(pose="ready", gloves=True)],
        [grandad(pose="sit"), grandad(pose="stand"), grandad_cane(), grandad_cane(cane_up=1.0), mum(), mum(pose="phone")],
        [doctor(), doctor(pose="run", phase=0.3), coach(), coach(mouth="open"), mason(mouth="grin"), mason(view="back", pose="kick", phase=0.6)],
        [academy(7), academy(7, pose="run", phase=0.5), trialist(3), trialist(5, view="back"), okafor(), dixon()],
    ]
    S = 6
    out = Image.new("RGBA", (6 * 34 * S, len(rows) * 52 * S), (90, 140, 90, 255))
    for r, row in enumerate(rows):
        for c, sp in enumerate(row):
            out.alpha_composite(big(sp, S), (c * 34 * S + 10, r * 52 * S + 10))
    out.convert("RGB").save(path)


if __name__ == "__main__":
    import sys
    sheet(sys.argv[1])
