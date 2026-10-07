from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

W, H = 1080, 1920
FPS = 30
DUR = 4.5
N = int(FPS*DUR)
FONT_PATH = "fonts/Anton.ttf"
NAME = "KAVIN"
os.makedirs("frames_k2", exist_ok=True)
random.seed(42)

# --- gold gradient strip (vertical) ---
def gold_gradient(h):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        p = y / h
        # top light champagne -> mid bright gold -> bottom deep bronze
        if p < 0.45:
            q = p/0.45
            c = (int(255 - 20*q), int(245 - 50*q), int(215 - 120*q))
        elif p < 0.60:
            q = (p-0.45)/0.15
            c = (255, int(195 + 40*q), int(95 + 60*q))  # bright band
        else:
            q = (p-0.60)/0.40
            c = (int(255 - 95*q), int(235 - 140*q), int(155 - 120*q))
        g.putpixel((0, y), c)
    return g

# particles: golden dust
parts = [{"x": random.uniform(0, W), "y": random.uniform(H*0.3, H*0.9),
          "r": random.uniform(1.2, 3.4), "s": random.uniform(8, 30),
          "ph": random.uniform(0, 6.28)} for _ in range(70)]

font_big = ImageFont.truetype(FONT_PATH, 210)
tmp = ImageDraw.Draw(Image.new("RGB", (W, H)))
letter_w = [tmp.textlength(ch, font=font_big) for ch in NAME]

def ease_out(p): return 1 - (1-p)**3

for i in range(N):
    t = i / FPS
    # global reveal
    ap = min(t/0.9, 1.0)
    alpha_g = ease_out(ap)
    # slow letter tracking expansion (movie style)
    tracking = 20 + 26 * (t/DUR)
    # slight global scale settle
    scale = 1.10 - 0.10 * ease_out(min(t/1.1, 1.0)) + 0.015 * (t/DUR)

    # --- text mask ---
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    total = sum(letter_w) + tracking*(len(NAME)-1)
    x = (W - total)/2
    ybase = H*0.60
    for li, ch in enumerate(NAME):
        md.text((x, ybase), ch, font=font_big, fill=255, anchor="ls")
        x += letter_w[li] + tracking
    # scale around center
    if abs(scale-1.0) > 0.001:
        sw, sh = int(W*scale), int(H*scale)
        m2 = mask.resize((sw, sh), Image.LANCZOS)
        mask = m2.crop(((sw-W)//2, (sh-H)//2, (sw-W)//2+W, (sh-H)//2+H))

    frame = Image.new("RGB", (W, H), (0, 0, 0))

    # soft warm ambient glow behind text (breathing)
    pulse = 0.75 + 0.25*math.sin(t*2.0)
    big_glow = mask.filter(ImageFilter.GaussianBlur(45))
    frame.paste(Image.new("RGB", (W, H), (120, 70, 10)),
                (0, 0), big_glow.point(lambda p: int(p*0.9*pulse*alpha_g)))

    # golden dust particles
    pd = ImageDraw.Draw(frame)
    for pt in parts:
        py = (pt["y"] - t*pt["s"]) % H
        tw = 0.5 + 0.5*math.sin(t*3 + pt["ph"])
        b = int(170 * tw * alpha_g)
        if b > 8:
            pd.ellipse([pt["x"]-pt["r"], py-pt["r"], pt["x"]+pt["r"], py+pt["r"]],
                       fill=(b, int(b*0.78), int(b*0.3)))

    # gold gradient fill through text mask
    bbox = mask.getbbox()
    if bbox:
        gh = bbox[3]-bbox[1]
        grad = gold_gradient(gh).resize((W, gh))
        gold_img = Image.new("RGB", (W, H), (0, 0, 0))
        gold_img.paste(grad, (0, bbox[1]))
        m_fade = mask.point(lambda p: int(p*alpha_g))
        # tight glow edge
        edge = mask.filter(ImageFilter.GaussianBlur(7))
        frame.paste(Image.new("RGB", (W, H), (255, 190, 80)),
                    (0, 0), edge.point(lambda p: int(p*0.55*alpha_g)))
        frame.paste(gold_img, (0, 0), m_fade)

        # --- light sweep (specular shine) twice: 1.2s and 3.0s ---
        for t0 in (1.2, 3.0):
            sp = (t - t0) / 0.7
            if 0 <= sp <= 1:
                band = Image.new("L", (W, H), 0)
                bd = ImageDraw.Draw(band)
                cx = -300 + sp * (W + 600)
                bw = 110
                for off in range(-bw, bw, 4):
                    a = int(230 * (1 - abs(off)/bw))
                    bd.line([(cx+off+300, bbox[1]-80), (cx+off-300, bbox[3]+80)],
                            fill=a, width=5)
                band = band.filter(ImageFilter.GaussianBlur(10))
                shine = Image.composite(band, Image.new("L", (W, H), 0), mask)
                frame.paste(Image.new("RGB", (W, H), (255, 252, 235)), (0, 0),
                            shine.point(lambda p: int(p*alpha_g)))

    # flare burst at reveal moment (t ~0.15-0.9): horizontal lens streak
    fb = max(0.0, 1 - abs(t-0.55)/0.45)
    if fb > 0:
        streak = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(streak)
        cy = int(H*0.60) - 70
        sd.line([(0, cy), (W, cy)], fill=int(200*fb), width=3)
        streak = streak.filter(ImageFilter.GaussianBlur(6))
        frame.paste(Image.new("RGB", (W, H), (255, 230, 170)), (0, 0), streak)

    # vignette-ish darkening on extreme top/bottom to keep focus
    # fade in/out
    if t < 0.15:
        frame = frame.point(lambda p: int(p*(t/0.15)))
    if t > DUR-0.6:
        frame = frame.point(lambda p: int(p*((DUR-t)/0.6)))
    frame.save(f"frames_k2/f{i:04d}.png")
print("frames ok")
