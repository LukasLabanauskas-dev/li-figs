from PIL import Image, ImageDraw, ImageFont
import sys

OUT = sys.argv[1]
W, H = 1080, 1350
BG = (14, 74, 74)        # deep teal
PANEL = (10, 58, 58)
WHITE = (240, 246, 244)
MUTED = (160, 196, 190)
GRID = (40, 104, 102)
AMBER = (255, 176, 32)

B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda p, s: ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text(xy, s, font, fill=WHITE, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

M = 60
text((M, 52), "Rivian R2 on a 400 V pack", f(B, 50))
text((M, 118), "Power comes from current. Current meets the adapter.", f(R, 30), MUTED)

# ---------- Panel 1: power vs SOC ----------
p1 = (M - 20, 180, W - M + 20, 760)
d.rounded_rectangle(p1, 22, fill=PANEL)
text((M, 205), "Charge power vs state of charge", f(B, 34))
text((M, 250), "10-80% in 26.9 min, ABB A400, CCS via 500 A adapter", f(R, 26), MUTED)

x0, x1 = 150, 1000        # SOC 10..80
y0, y1 = 700, 400         # kW 0..250
sx = lambda soc: x0 + (soc - 10) / 70 * (x1 - x0)
sy = lambda kw: y0 - kw / 250 * (y0 - y1)
lab = f(R, 24)
for kw in (0, 50, 100, 150, 200, 250):
    y = sy(kw)
    d.line([(x0, y), (x1, y)], fill=GRID, width=2)
    text((x0 - 14, y), str(kw), lab, MUTED, "rm")
for soc in (10, 20, 30, 40, 50, 60, 70, 80):
    text((sx(soc), y0 + 14), f"{soc}%", lab, MUTED, "ma")
text((x0 - 14, y1 - 30), "kW", lab, MUTED, "rb")

pts = [(31, 226), (45, 171), (60, 135), (70, 116), (80, 68)]
xy = [(sx(s), sy(k)) for s, k in pts]
d.line(xy, fill=AMBER, width=7, joint="curve")
vf = f(B, 30)
offs = {31: (0, -26, "mb"), 45: (14, -18, "lb"), 60: (14, -18, "lb"),
        70: (-10, 18, "rt"), 80: (-16, 22, "rt")}
for (s, k), (x, y) in zip(pts, xy):
    d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=AMBER, outline=PANEL, width=3)
    dx, dy, an = offs[s]
    text((x + dx, y + dy), f"{k} kW", vf, WHITE, an)
text((sx(31), sy(226) - 62), "peak at 31%", f(R, 24), MUTED, "mb")

# ---------- Panel 2: currents to scale ----------
p2 = (M - 20, 790, W - M + 20, 1220)
d.rounded_rectangle(p2, 22, fill=PANEL)
text((M, 815), "Current, drawn to scale (0 to 630 A)", f(B, 34))

bx0, bx1 = M, W - M - 150   # 0..630 A maps here
scale = (bx1 - bx0) / 630
rows = [
    (375, "Station NACS cable cap", False),
    (500, "Adapter rating", False),
    (600, "Can pull, per RivianTrackr", True),
    (630, "R2 maximum, per Rivian", False),
]
ry = 880
for amps, label, hot in rows:
    text((bx0, ry), label, f(R, 26), WHITE)
    top = ry + 38
    w = amps * scale
    d.rectangle([bx0, top, bx0 + w, top + 34], fill=AMBER if hot else MUTED)
    text((bx0 + w + 16, top + 17), ("600+ A" if amps == 600 else f"{amps} A"), f(B, 30), WHITE, "lm")
    ry += 82
# 500 A rating line through the bars
xr = bx0 + 500 * scale
for yy in range(915, ry - 8, 14):
    d.line([(xr, yy), (xr, yy + 7)], fill=WHITE, width=3)

# ---------- Footer ----------
text((M, 1250), "Data: State of Charge (Tom Moloughney), July 2026, as reported by RivianTrackr", f(R, 22), MUTED)
text((M, 1280), "and InsideEVs. Drawn from reported numbers.", f(R, 22), MUTED)

img.save(OUT)
img.convert("RGB").save(OUT.rsplit(".", 1)[0] + "_view.jpg", quality=85)
print(img.size)
