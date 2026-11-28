import sys
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
BG=(234,236,238); INK=(28,32,38); GREY=(96,102,110); COAT=(204,208,214); HATCH=(186,191,198)
PART=(150,156,166); FOIL=(120,126,136); AMBER=(232,150,30)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=lambda s,b=False: ImageFont.truetype(FB if b else F,s)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((60,56),"LMFP CATHODE ON BARE ALUMINIUM FOIL",font=f(26,True),fill=GREY)
d.text((60,96),"Denser calendering, more foil contact",font=f(44,True),fill=INK)
for i,l in enumerate(["Schematic, not to scale. Same particle size in both panels. The",
 "bottom-row contacts cover the foil share measured by SEM (amber).",
 "Real embedment is under 100 nm on a 15 µm foil, too small to draw."]):
    d.text((60,164+i*34),l,font=f(26),fill=GREY)
def panel(y0,dens,frac,thick,note,nparts):
    x0,x1=60,1020; width=x1-x0
    d.text((x0,y0),f"{dens} g/cm³",font=f(40,True),fill=INK)
    d.text((x0+260,y0+10),f"coating about {thick} µm thick",font=f(28),fill=GREY)
    ctop=y0+60; foil_top=ctop+int(thick*2.6)
    hh=foil_top-ctop
    tile=Image.new('RGB',(width+1,hh+1),COAT); td=ImageDraw.Draw(tile)
    for k in range(-hh,width,28): td.line([(k,0),(k+hh,hh)],fill=HATCH,width=2)
    im.paste(tile,(x0,ctop))
    d.text((x0+20,ctop+14),"Cathode coating",font=f(26,True),fill=GREY)
    # contact footprints
    contact=frac*width; base=contact/nparts; gap=(width-contact)/nparts
    x=x0+gap/2; r=base/2
    for i in range(nparts):
        d.pieslice([x,foil_top-r,x+base,foil_top+r],180,360,fill=PART,outline=(110,116,126))
        d.rectangle([x,foil_top-1,x+base,foil_top+7],fill=AMBER)
        x+=base+gap
    d.rectangle([x0,foil_top+8,x1,foil_top+78],fill=FOIL)
    d.text((x0+20,foil_top+26),"Al foil, 15 µm",font=f(28,True),fill=(245,246,248))
    by=foil_top+104
    d.text((x0,by-8),f"{int(round(frac*100))}%",font=f(64,True),fill=INK)
    d.text((x0+170,by+4),"of the foil surface touched",font=f(30,True),fill=INK)
    d.text((x0+170,by+42),note,font=f(25),fill=GREY)
panel(300,"1.95",0.28,75,"Bare-Al interface resistance too high to measure",7)
panel(800,"2.75",0.83,50,"Bare-Al interface resistance: 0.21 Ω·cm² at 2.7 g/cm³",20)
d.text((60,1272),"Data: Sellers, Proprentner, Dahari et al., Advanced Science (2026),",font=f(20),fill=GREY)
d.text((60,1300),"DOI 10.1002/advs.78510, CC BY 4.0. Drawn from reported numbers, not the authors' figure.",font=f(20),fill=GREY)
im.save(sys.argv[1])
