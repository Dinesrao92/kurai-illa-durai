from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

W, H = 1080, 1920
FPS = 30
DUR = 4.0
N = int(FPS * DUR)
FONT = "fonts/Anton.ttf"

def render(name, color_main, color_glow, style, outdir):
    os.makedirs(outdir, exist_ok=True)
    font = ImageFont.truetype(FONT, 190)
    # measure
    tmp = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(tmp)
    # letter positions with tracking
    tracking = 18
    widths = [d.textlength(ch, font=font) for ch in name]
    total = sum(widths) + tracking * (len(name) - 1)
    x0 = (W - total) / 2
    ybase = H * 0.62  # lower-third-ish
    random.seed(7)

    for i in range(N):
        t = i / FPS
        img = Image.new("RGB", (W, H), (0, 0, 0))
        txt = Image.new("L", (W, H), 0)
        td = ImageDraw.Draw(txt)

        x = x0
        for li, ch in enumerate(name):
            # per-letter reveal timing
            if style == "smooth":
                start = 0.25 + li * 0.14
                prog = min(max((t - start) / 0.45, 0), 1)
                ease = 1 - (1 - prog) ** 3
                if prog > 0:
                    dy = (1 - ease) * 140
                    alpha = int(255 * ease)
                    tmpl = Image.new("L", (W, H), 0)
                    ImageDraw.Draw(tmpl).text((x, ybase + dy), ch, font=font, fill=alpha, anchor="ls")
                    txt = Image.composite(Image.new("L",(W,H),255), txt, tmpl.point(lambda p: p))
                    txt.paste(tmpl, (0,0), tmpl)
            else:  # slam
                start = 0.25 + li * 0.10
                prog = min(max((t - start) / 0.22, 0), 1)
                if prog > 0:
                    scale_over = 1 + (1 - prog) * 0.9
                    fsz = int(190 * scale_over)
                    f2 = ImageFont.truetype(FONT, fsz)
                    alpha = int(255 * min(prog * 1.6, 1))
                    # flicker after landing
                    if prog >= 1 and random.random() < 0.06:
                        alpha = 150
                    jx = random.uniform(-2.5, 2.5) if prog >= 1 else 0
                    jy = random.uniform(-2.5, 2.5) if prog >= 1 else 0
                    cx = x + widths[li] / 2
                    tmpl = Image.new("L", (W, H), 0)
                    ImageDraw.Draw(tmpl).text((cx + jx, ybase + jy), ch, font=f2, fill=alpha, anchor="ms")
                    txt.paste(tmpl, (0,0), tmpl)
            x += widths[li] + tracking

        # glow pulse
        pulse = 0.65 + 0.35 * math.sin(t * 2.6)
        glow = txt.filter(ImageFilter.GaussianBlur(22))
        glow2 = txt.filter(ImageFilter.GaussianBlur(6))

        base = Image.new("RGB", (W, H), (0, 0, 0))
        g_layer = Image.new("RGB", (W, H), color_glow)
        base.paste(g_layer, (0,0), glow.point(lambda p: int(p * 0.8 * pulse)))
        base.paste(g_layer, (0,0), glow2.point(lambda p: int(p * 0.6)))
        m_layer = Image.new("RGB", (W, H), color_main)
        base.paste(m_layer, (0,0), txt)

        # fade out last 0.5s
        if t > DUR - 0.5:
            f = (DUR - t) / 0.5
            base = base.point(lambda p: int(p * f))
        base.save(f"{outdir}/f{i:04d}.png")

render("KAVIN",  (255, 236, 190), (255, 150, 30),  "smooth", "frames_kavin")
render("MAARAN", (255, 225, 220), (200, 15, 15),   "slam",   "frames_maaran")
print("frames done")
