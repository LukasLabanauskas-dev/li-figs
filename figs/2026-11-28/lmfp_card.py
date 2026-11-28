import random, sys
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
BG=(236,238,240); INK=(28,32,38); GREY=(110,116,124); PART=(196,200,206); PEDGE=(150,156,164)
FOIL=(168,174,182); AMBER=(232,150,30); PORE=(72,78,88)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda s,b=False: ImageFont.truetype(FB if b else F,s)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((60,56),"LMFP CATHODE ON BARE ALUMINIUM FOIL",font=f(26,True),fill=(150,90,10))
d.text((60,96),"Denser calendering, more foil contact",font=f(44,True),fill=INK)
d.text((60,160),"Schematic. Amber = share of the foil surface touched by LMFP",font=f(26),fill=GREY)
d.text((60,194),"particles (SEM, Sellers et al.). Flat contact: real embedment",font=f(26),fill=GREY)
d.text((60,228),"is under 100 nm on a 15 µm foil, too small to draw here.",font=f(26),fill=GREY)
def panel(y0, dens, frac, poro, seed, label_res, thick, n):
    random.seed(seed)
    x0,x1=60,1020; foil_top=y0+60+int(thick*2.6); foil_h=70
    d.text((x0,y0),f"{dens} g/cm³",font=f(40,True),fill=INK)
    d.text((x0+260,y0+10),f"{poro}% porosity, coating about {thick} µm",font=f(28),fill=GREY)
    # coating box background (pore phase)
    d.rectangle([x0,y0+60,x1,foil_top],fill=PORE)
    # particles: dense packing scaled by porosity
    placed=[]
    tries=0
    while len(placed)<n and tries<40000:
        tries+=1
        r=random.uniform(9,17); x=random.uniform(x0+r,x1-r); y=random.uniform(y0+60+r,foil_top-r)
        if all((x-a)**2+(y-b)**2>(r+c-1.5)**2 for a,b,c in placed): placed.append((x,y,r))
    # bottom contact row: particles resting on foil only over the contact fraction
    width=x1-x0; contact_len=frac*width
    # build contact segments: alternating, total exactly contact_len
    segs=[]; nseg=12; seglen=contact_len/nseg; gap=(width-contact_len)/nseg
    x=x0+gap/2
    for i in range(nseg): segs.append((x,x+seglen)); x+=seglen+gap
    # remove particles overlapping bottom band, then add touching particles in segments
    placed=[p for p in placed if p[1]+p[2]<foil_top-14]
    for a,b in segs:
        xx=a
        while xx<b-6:
            r=min(13,(b-xx)/2)
            if r<5: break
            placed=[p for p in placed if (p[0]-(xx+r))**2+(p[1]-(foil_top-r))**2>(p[2]+r)**2]
            placed.append((xx+r,foil_top-r,r)); xx+=2*r
    for x,y,r in placed:
        d.ellipse([x-r,y-r,x+r,y+r],fill=PART,outline=PEDGE)
    d.rectangle([x0,foil_top,x1,foil_top+foil_h],fill=FOIL)
    d.text((x0+20,foil_top+18),"Al foil",font=f(28,True),fill=INK)
    for a,b in segs: d.rectangle([a,foil_top-2,b,foil_top+6],fill=AMBER)
    # contact bar
    by=foil_top+foil_h+28
    d.rectangle([x0,by,x1,by+30],fill=(214,217,221))
    d.rectangle([x0,by,x0+frac*width,by+30],fill=AMBER)
    d.text((x0,by+40),f"Foil surface touched by particles: {int(frac*100)}%",font=f(30,True),fill=INK)
    d.text((x0,by+80),label_res,font=f(26),fill=GREY)
panel(300,"1.95",0.28,42,3,"Bare-Al interface resistance too high to measure below 2.15 g/cm³",75,300)
panel(820,"2.75",0.83,18,5,"Bare-Al interface resistance: 0.21 Ω·cm² at 2.7 g/cm³ (10.4 at 2.15)",50,420)
d.text((60,1272),"Data: Sellers, Proprentner, Dahari et al., Advanced Science (2026),",font=f(20),fill=GREY)
d.text((60,1300),"DOI 10.1002/advs.78510, CC BY 4.0. Drawn from reported numbers, not the authors' figure.",font=f(20),fill=GREY)
im.save(sys.argv[1])
