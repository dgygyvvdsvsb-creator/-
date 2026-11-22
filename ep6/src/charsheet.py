import os
os.environ.setdefault("PLATFORM","tiktok")
import ep6
from ep6 import *

W, H = 1080, 1920
def page_bg():
    bg = navy_bg().resize((W, H), Image.NEAREST)
    return bg

def tile(img, x, y, w, h, sprite, scale, label, sub="", rot=0, field=True, by_off=0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + w, y + h], 18, fill=(14, 20, 50), outline=(60, 80, 140), width=3)
    if field:
        for k in range(6):
            yy = y + h * 0.55 + k * (h * 0.45 - 60) / 6
            d.rectangle([x + 6, yy, x + w - 6, yy + (h * 0.45 - 60) / 6], fill=(42, 150, 72) if k % 2 else (36, 132, 60))
    s = big(sprite, scale)
    if rot:
        s = s.rotate(rot, expand=True, resample=Image.NEAREST)
    cx, by = x + w / 2, y + h - 70 + by_off
    shadow(img, cx, by, s.width * 0.55, 18, 80)
    img.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height)))
    d = ImageDraw.Draw(img)
    d.text((x + w / 2, y + h - 44), label, font=font(800, 24), fill=C_Y, anchor="mm")
    if sub:
        d.text((x + w / 2, y + h - 18), sub, font=font(700, 16), fill=(210, 215, 235), anchor="mm")

def header(img, title, subtitle):
    d = ImageDraw.Draw(img)
    d.text((W / 2, 70), "FROM ZERO TO LEGEND", font=font(800, 30), fill=C_Y, anchor="mm")
    d.text((W / 2, 130), title, font=font(800, 64), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=OL)
    d.text((W / 2, 185), subtitle, font=font(700, 24), fill=(200, 205, 225), anchor="mm")

def grid(img, items, cols=4, top=230, cell_h=400, gap=16):
    cw = (W - gap * (cols + 1)) / cols
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        x = gap + c * (cw + gap); y = top + r * (cell_h + gap)
        tile(img, x, y, cw, cell_h, *it)

def save(img, name):
    img.convert("RGB").save(name)

coach_nocap = lambda **k: person(Kit((30, 40, 80), (30, 40, 80), (30, 30, 36)), skin="light", hair="grey", style="short", **k)
mum = lambda **k: person(Kit((70, 108, 189), (45, 75, 140), (45, 75, 140)), hair="brown", style="pony", **k)
alfie = lambda **k: person(Kit((60, 120, 210), (245, 245, 250), (60, 120, 210), 7), skin="light", hair="ginger", style="curly", **k)

# PAGE 1 — the hero
p = page_bg(); header(p, "THE HERO", "Number 0 · goalkeeper · 11 · Grandad's orange gloves · red bracelet (right wrist)")
grid(p, [
    (hero(), 9, "FRONT", "no gloves"),
    (hero(view="back"), 9, "BACK", "over-the-shoulder"),
    (hero(gloves=True, pose="ready"), 9, "READY", "keeper stance"),
    (hero(gloves=True, pose="catch"), 9, "CATCH", "ball at chest"),
    (hero(gloves=True, pose="celebrate", mouth="grin"), 9, "CELEBRATE", "arms up"),
    (hero(pose="run", phase=0.25), 9, "RUN", ""),
    (hero(pose="sit", gloves=True), 9, "SIT", "bench"),
    (hero(gloves=True, pose="reach", mouth="open"), 6, "DIVE RIGHT", "full stretch", -90),
    (hero(gloves=True, pose="reach", mouth="open"), 6, "DIVE LEFT", "full stretch", 90),
    (hero(mouth="smile"), 9, "HAPPY", ""),
    (hero(mouth="sad"), 9, "SAD", ""),
    (hero(mouth="shock" if False else "open"), 9, "SHOCKED", ""),
])
save(p, "frames6/chars_1_hero.png")

# PAGE 2 — family & staff
p = page_bg(); header(p, "FAMILY & STAFF", "Grandad (ex-keeper, cane, cardigan) · Mum · Coach")
grid(p, [
    (grandad(pose="stand", mouth="smile"), 9, "GRANDAD", "standing"),
    (grandad(pose="sit", mouth="smile"), 9, "GRANDAD", "seat 14"),
    (grandad(pose="sit", mouth="smile", tube=True), 9, "GRANDAD", "after hospital"),
    (cane(26), 9, "CANE", "always with him"),
    (mum(mouth="smile"), 9, "MUM", ""),
    (mum(pose="sit", mouth="smile"), 9, "MUM", "in the stand"),
    (coach(), 9, "COACH", "on the pitch"),
    (coach_nocap(mouth="open"), 9, "COACH", "in his office"),
    (alfie(mouth="grin"), 9, "ALFIE", "best friend"),
    (alfie(view="back"), 9, "ALFIE", "back"),
])
save(p, "frames6/chars_2_family.png")

# PAGE 3 — squad & rivals
p = page_bg(); header(p, "SQUAD & RIVALS", "Riverside first team (red) · keepers · reserves (blue)")
grid(p, [
    (mason(mouth="grin"), 7, "MASON #9", "rival · striker"),
    (mason(view="back"), 7, "MASON #9", "back"),
    (mason(pose="kick", phase=0.8), 7, "MASON", "shooting"),
    (okafor(), 7, "OKAFOR #1", "first-choice keeper"),
    (okafor(pose="hurt", mouth="open"), 5, "OKAFOR", "injured", -90),
    (dixon(), 7, "DIXON #2", "rival for the shirt"),
    (dixon(view="back"), 7, "DIXON #2", "back"),
    (ours(4), 7, "#4", "defender"),
    (ours(5), 7, "#5", "defender"),
    (ours(6), 7, "#6", "midfielder"),
    (ours(7), 7, "#7", "winger"),
    (opp(10), 7, "CAPTAIN #10", "reserves"),
    (opp(9), 7, "#9", "reserves striker"),
    (opp(7), 7, "#7", "reserves"),
    (opp(7, view="back", pose="kickL", phase=0.8), 7, "LEFT-FOOT", "curler"),
    (opp_keeper(), 7, "RES. KEEPER", "Dixon in their goal"),
], cell_h=330)
save(p, "frames6/chars_3_squad.png")

# PAGE 4 — close-ups
p = page_bg(); header(p, "CLOSE-UPS", "faces for reactions")
d = ImageDraw.Draw(p)
items = [(hero(mouth="flat", gloves=True), "HERO · FOCUSED", "angry"), (hero(mouth="grin"), "HERO · JOY", None),
         (mason(mouth="grin"), "MASON · MOCKING", "angry"), (dixon(mouth="smile"), "DIXON · SMIRK", "angry"),
         (grandad(mouth="smile"), "GRANDAD · PROUD", None), (coach_nocap(mouth="open"), "COACH · TALKING", None)]
for i, (sp, lab, br) in enumerate(items):
    r, c = divmod(i, 2)
    x, y, w, h = 30 + c * 520, 240 + r * 550, 500, 520
    d.rounded_rectangle([x, y, x + w, y + h], 18, fill=(14, 20, 50), outline=(60, 80, 140), width=3)
    tilecanvas = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    face_closeup(tilecanvas, sp, 24, 360, 1500, brows=br, sweat=1 if "FOCUSED" in lab else 0)
    crop = tilecanvas.crop((60, 700, 660, 1300)).resize((w - 20, h - 80), Image.NEAREST)
    p.alpha_composite(crop, (int(x + 10), int(y + 10)))
    d = ImageDraw.Draw(p)
    d.text((x + w / 2, y + h - 34), lab, font=font(800, 26), fill=C_Y, anchor="mm")
save(p, "frames6/chars_4_faces.png")
print("ok")
