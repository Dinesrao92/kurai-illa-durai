from PIL import Image, ImageDraw, ImageFont

# ============ SHOT STATUS — update this set as gens complete ============
DONE = {"01", "02", "03", "04", "05", "06", "11", "12", "13", "14"}
# ========================================================================

F = lambda s, b=True: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", s)
GOLD=(212,175,55); RED=(200,40,40); WHITE=(240,240,240); GRAY=(150,150,158)
GREEN=(70,180,110); ORANGE=(235,150,50); BLUE=(90,150,230)
BG=(13,13,18); CARD=(22,22,29)

TB="trailer_board/"; SV="scenes_v4/"
panels=[
 ("01","0:00-0:04","COLD OPEN","refs/brickfields_street.jpg","EDIT 0cr",BLUE,"Black + sound - still flashes"),
 ("02","0:04-0:07","THE HANDS",TB+"s1_A_hands_jasmine_dawn.png","FILM GEN",GREEN,'Macro push-in - "Naan Durai."'),
 ("03","0:07-0:10","DURAI REVEAL",TB+"durai_reveal_poster.png","FILM GEN",GREEN,"Lateral track - eyes up last"),
 ("04","0:10-0:14","KAVIN",TB+"intro_kavin.png","EXISTING VID",BLUE,'"Enna, anna-ku attendance...?"'),
 ("05","0:14-0:18","TEN YEARS",TB+"s2_E_montage_garland_teaching.png","FILM GEN",GREEN,"Match cut - Pathu varusham"),
 ("06","0:18-0:22","JOHOR ARRIVES",TB+"s3_B_maaran_entrance.png","FILM GEN",GREEN,"Wheel > shoe > crane up"),
 ("07","0:22-0:26","THE PACKAGE",TB+"s3_D_packet_smile.png","EDIT 0cr",BLUE,"Rack focus packet > jasmine"),
 ("08","0:26-0:30","THE LINE",TB+"s1_E_idhu_brickfields_stare.png","FILM GEN",GREEN,'"Naan Maaran illa. Idhu Brickfields."'),
 ("09","0:30-0:34","RAHIM'S SHOP",TB+"s4_G_durai_rahim_envelope.png","FILM GEN",GREEN,'Envelope lands - "Monthly."'),
 ("10","0:34-0:39","LORRY ATTACK",TB+"s5_E_lorry_ambush.png","FILM GEN",GREEN,"Brake whip - petals scatter"),
 ("11","0:39-0:43","THE STILL MAN",TB+"s5_J_durai_unmoved_stare.png","FILM GEN",GREEN,'"Manushan-a illa..." THE HEART'),
 ("12","0:43-0:47","DURAI MOVES",SV+"s11_A_wrist_catch.png","T-GEN 2",ORANGE,"One wrist catch - walks past"),
 ("13","0:47-0:51","KAVIN'S SECRET",SV+"s8_C_lights_on_aftermath.png","FILM GEN",GREEN,"One eye visible - CUT TO BLACK"),
 ("14","0:51-0:54","MAARAN RAGES",TB+"intro_maaran.png","T-GEN 3",ORANGE,"Glass shatters - real anger"),
 ("15","0:54-0:56","BIGGER SHADOW",SV+"s12_H_mysterious_man.png","FILM GEN",GREEN,"Hand + phone only - NO FACE"),
 ("16","0:56-0:58","FINAL COLLISION",SV+"s12_B_ropes_fall.png","FILM GEN",GREEN,"0.4s cuts - cause > effect"),
 ("17","0:58-1:00","TITLE SMASH","posters/final_cast_poster_v3.png","EDIT 0cr",BLUE,'"Kurai illa... Durai."'),
]

PW,TH,CH,GAP,M=370,460,140,16,44
COLS=6; ROWS=3
W=M*2+COLS*PW+(COLS-1)*GAP
HDR=210; FTR=70
H=HDR+ROWS*(TH+CH)+(ROWS-1)*GAP+FTR+M
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

d.text((M,52),"KURAI ILLA, DURAI",font=F(72),fill=GOLD)
d.text((M+2,140),"60-SECOND MASTER TRAILER  ·  STORYBOARD  ·  DIRECTED BY DR",font=F(30),fill=WHITE)
lx=W-M-1060
for tag,col in [("FILM GEN 0cr",GREEN),("T-GEN 30cr",ORANGE),("EDIT 0cr",BLUE)]:
    d.rounded_rectangle([lx,95,lx+34,117],6,fill=col)
    d.text((lx+44,96),tag,font=F(24),fill=WHITE); lx+=d.textlength(tag,font=F(24))+90
n_done=len(DONE)
d.text((W-M-1060,140),f"SHOT PROGRESS: {n_done}/17  ·  EXTRA COST: 2 x 30cr = 60cr",font=F(26),fill=GOLD)
d.line([M,HDR-18,W-M,HDR-18],fill=(60,60,70),width=2)

def crop_fit(p,w,h):
    im=Image.open(p).convert("RGB"); iw,ih=im.size
    s=max(w/iw,h/ih); im=im.resize((int(iw*s)+1,int(ih*s)+1))
    iw,ih=im.size; x=(iw-w)//2; y=(ih-h)//3
    return im.crop((x,y,x+w,y+h))

for i,(num,tc,title,path,tag,col,cap) in enumerate(panels):
    r,c=divmod(i,COLS)
    x=M+c*(PW+GAP); y=HDR+r*(TH+CH+GAP)
    done=num in DONE
    d.rounded_rectangle([x,y,x+PW,y+TH+CH],10,fill=CARD)
    th=crop_fit(path,PW-12,TH-12); img.paste(th,(x+6,y+6))
    d.rectangle([x+6,y+6,x+PW-6,y+TH-6],outline=GREEN if done else (50,50,60),width=6 if done else 2)
    tw=d.textlength(tag,font=F(19)); d.rounded_rectangle([x+PW-tw-40,y+16,x+PW-16,y+46],8,fill=col)
    d.text((x+PW-tw-28,y+21),tag,font=F(19),fill=(10,10,14))
    if done:
        bw=d.textlength("SHOT  DONE",font=F(24))+56
        d.rounded_rectangle([x+16,y+TH-66,x+16+bw,y+TH-22],10,fill=GREEN)
        d.text((x+34,y+TH-59),"SHOT  DONE",font=F(24),fill=(8,20,12))
    ty=y+TH+8
    d.text((x+14,ty),f"SHOT {num}",font=F(26),fill=GREEN if done else GOLD)
    d.text((x+160,ty+5),tc,font=F(20,False),fill=GRAY)
    d.text((x+14,ty+38),title,font=F(28),fill=WHITE)
    d.text((x+14,ty+76),cap[:42],font=F(21,False),fill=GRAY)

x=M+5*(PW+GAP); y=HDR+2*(TH+CH+GAP)
d.rounded_rectangle([x,y,x+PW,y+TH+CH],10,fill=(26,20,20),outline=RED,width=3)
cy=y+34
d.text((x+28,cy),"ONE-BUDGET RULE",font=F(32),fill=RED); cy+=70
for ln in ["13 film hero gens","   = trailer backbone","   (pay once, use twice)","2 trailer-only gens","   T2 Durai wrist catch","   T3 Maaran rage","Cold open stills = 0cr","Kavin intro vid = 0cr","Stills + titles = 0cr","","TRAILER EXTRA COST:","60cr = still RM4.90"]:
    f=F(30) if "RM4.90" in ln or "COST" in ln else F(26,False)
    d.text((x+28,cy),ln,font=f,fill=GOLD if ("RM" in ln or "COST" in ln) else WHITE); cy+=38

d.text((M,H-FTR-10),"CANON LOCKS:  anna-thambi only  ·  no police  ·  no undercover reveal  ·  Mysterious Man face never shown  ·  Durai = stillness, not flash",font=F(24,False),fill=GRAY)
d.text((W-M-620,H-FTR-10),"CHAPTER 1  ·  MALAYSIAN INDIAN TAMIL DRAMA",font=F(24),fill=GOLD)

img.save("docs/STORYBOARD_60S_SHEET.png")
print("saved", img.size, "| done:", sorted(DONE))
