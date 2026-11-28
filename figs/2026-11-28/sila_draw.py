import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = (74, 102, 84)        # muted sage green
PANEL = (61, 86, 70)
INK = (243, 235, 216)     # cream text
DIM = (196, 206, 190)
AMBER = (242, 169, 59)
CARBON = (40, 48, 44)
PORE = (92, 120, 101)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def f(s, b=False): return ImageFont.truetype(FB if b else F, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def ctext(x, y, s, font, fill=INK):
    w = d.textlength(s, font=font)
    d.text((x - w / 2, y), s, font=font, fill=fill)

# Title
d.text((60, 50), "Where does 280% go?", font=f(62, True), fill=INK)
d.text((60, 130), "Silicon volume x3.8 on full lithiation, so diameter x1.56", font=f(29), fill=DIM)

# ---- Panel A: bare particle, to scale ----
d.rounded_rectangle((40, 195, 1040, 595), 24, fill=PANEL)
d.text((70, 215), "A. Bare silicon particle", font=f(34, True), fill=INK)
d.text((70, 258), "To scale", font=f(26), fill=DIM)
r0 = 80
r1 = r0 * (3.8 ** (1 / 3))   # 280% volume growth -> x3.8 volume
cy = 425
# before
bx = 270
d.ellipse((bx - r0, cy - r0, bx + r0, cy + r0), fill=INK)
ctext(bx, cy + r1 + 8 - 0, "Before", f(28))
# after
ax = 720
d.ellipse((ax - r1, cy - r1, ax + r1, cy + r1), fill=AMBER)
# ghost outline of original size
for a in range(0, 360, 12):
    t0, t1 = math.radians(a), math.radians(a + 6)
    d.arc((ax - r0, cy - r0, ax + r0, cy + r0), a, a + 6, fill=CARBON, width=4)
ctext(ax, cy + r1 + 8, "Fully lithiated", f(28))
# arrow between
d.line((bx + r0 + 30, cy, ax - r1 - 30, cy), fill=INK, width=5)
d.polygon([(ax - r1 - 30, cy), (ax - r1 - 50, cy - 12), (ax - r1 - 50, cy + 12)], fill=INK)

# ---- Panel B: scaffold, schematic ----
d.rounded_rectangle((40, 620, 1040, 1042), 24, fill=PANEL)
d.text((70, 640), "B. Silicon inside a porous carbon scaffold", font=f(34, True), fill=INK)
d.text((70, 683), "Schematic, not to scale", font=f(26), fill=DIM)

R = 118
cyB = 862
random.seed(4)
# pore centres on a hex-ish grid inside the particle
pores = []
rp = 19
step = 2 * rp + 12
for iy in range(-6, 7):
    for ix in range(-6, 7):
        x = ix * step + (step / 2 if iy % 2 else 0)
        y = iy * step * 0.87
        if math.hypot(x, y) < R - rp - 14:
            pores.append((x, y))

def scaffold(cx, lith):
    # shell
    d.ellipse((cx - R - 9, cyB - R - 9, cx + R + 9, cyB + R + 9), fill=INK)
    d.ellipse((cx - R, cyB - R, cx + R, cyB + R), fill=CARBON)
    rs = rp / (3.8 ** (1 / 3))  # Si sized so its x3.8 volume just fills the pore
    for (x, y) in pores:
        px, py = cx + x, cyB + y
        # Si deposited on the pore wall (CVD); spare void in the pore centre
        d.ellipse((px - rp, py - rp, px + rp, py + rp), fill=AMBER)
        if not lith:
            ri = rp * math.sqrt(1 - 1 / 3.8)  # wall layer area = pore area / 3.8 (2D schematic)
            d.ellipse((px - ri, py - ri, px + ri, py + ri), fill=PORE)

lx, rx = 270, 720
scaffold(lx, False)
scaffold(rx, True)
d.line((lx + R + 40, cyB, rx - R - 40, cyB), fill=INK, width=5)
d.polygon([(rx - R - 40, cyB), (rx - R - 60, cyB - 12), (rx - R - 60, cyB + 12)], fill=INK)
ctext(lx, cyB + R + 22, "Si lines pore walls, void left", f(26))
ctext(rx, cyB + R + 22, "Si fills pores (design intent)", f(26))

# legend row
ly = 688
lx0 = 470
for name, col in [("Silicon", AMBER), ("Void", PORE), ("Carbon", CARBON), ("Shell", INK)]:
    d.ellipse((lx0, ly, lx0 + 24, ly + 24), fill=col, outline=INK if col == CARBON else None, width=2)
    d.text((lx0 + 32, ly - 3), name, font=f(24), fill=INK)
    lx0 += 32 + d.textlength(name, font=f(24)) + 30

# ---- Panel C: measured electrode growth ----
d.rounded_rectangle((40, 1060, 1040, 1265), 24, fill=PANEL)
d.text((70, 1075), "C. Electrode growth, first charge to full-cell capacity", font=f(28, True), fill=INK)
rows = [("Graphite", 19, DIM), ("Si/C", 28, AMBER), ("Micro-Si", 39, DIM)]
x0, scale = 250, 15.0     # px per %
for i, (name, v, col) in enumerate(rows):
    y = 1125 + i * 44
    d.text((70, y), name, font=f(28), fill=INK)
    d.rectangle((x0, y + 4, x0 + v * scale, y + 32), fill=col)
    d.text((x0 + v * scale + 14, y), f"{v}%", font=f(28, True), fill=INK)

# footer
d.text((60, 1280), "Drawn from reported numbers. Credit: Sila patent US 10,374,221,",
       font=f(22), fill=DIM)
d.text((60, 1310), "Dickmanns et al., J. Electrochem. Soc. 2026 (panel C, half-cell electrodes).", font=f(22), fill=DIM)

import sys
img.save(sys.argv[1])
img.convert("RGB").save(sys.argv[1].replace(".png",".jpg"), quality=85)
print(img.size, r1 / r0)
