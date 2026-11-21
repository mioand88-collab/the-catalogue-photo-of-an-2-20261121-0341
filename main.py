"""The One-Pea Toaster — catalogue photograph of an impossible gadget.

Renders a 1024x1024 studio product photo with PIL: a small polished-chrome
toaster body with only ONE comically narrow slot, from which a single green
pea pops up mid-toast on a spring, with a wisp of toast smoke and a small
golden-brown toasted patch on the pea. Exactly one accessory: a small white
plate with a single pat of butter. Clean light-grey studio gradient, soft
floor shadow, warm key light from upper left.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
OUT_NAME = "entry.png"

random.seed(42)

# ---------------------------------------------------------------- palette
BG_TOP = (240, 240, 242)
BG_MID = (221, 221, 226)
BG_BOT = (188, 188, 196)

CHROME_DARK = (104, 108, 120)
CHROME_MID = (172, 177, 190)
CHROME_LITE = (228, 232, 240)
CHROME_HI = (252, 253, 255)
SLOT_DARK = (24, 26, 30)
PEA_GREEN = (92, 172, 68)
PEA_DARK = (50, 116, 38)
PEA_LITE = (158, 216, 116)
TOAST_MARK = (178, 118, 50)
BUTTER = (252, 224, 122)
BUTTER_DARK = (224, 182, 72)
PLATE_WHITE = (250, 250, 252)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, top, mid, bot):
    """Vertical studio gradient background."""
    d = ImageDraw.Draw(img)
    for y in range(H):
        if y < H // 2:
            c = lerp(top, mid, y / (H // 2))
        else:
            c = lerp(mid, bot, (y - H // 2) / (H // 2))
        d.line([(0, y), (W, y)], fill=c)


def radial_glow(img, cx, cy, radius, color, alpha=60):
    """Soft warm glow from the key light, upper left."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(alpha * (1 - i / steps) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.alpha_composite(glow)


def soft_shadow(img, box, blur=26, alpha=110):
    """Soft elliptical contact shadow on the floor."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=(40, 42, 52, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(layer)


# ---------------------------------------------------------------- toaster body
def chrome_body(img):
    """Polished chrome toaster body: smooth gradient, soft sheen, dark base."""
    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    x0, y0, x1, y1 = 296, 496, 728, 794
    # horizontal chrome gradient across the shell: bright left, dim right
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        if t < 0.28:
            c = lerp(CHROME_LITE, CHROME_MID, t / 0.28)
        elif t < 0.62:
            c = lerp(CHROME_MID, CHROME_DARK, (t - 0.28) / 0.34)
        else:
            c = lerp(CHROME_DARK, CHROME_MID, (t - 0.62) / 0.38)
        d.line([(x, y0 + 10), (x, y1 - 10)], fill=c)
    # clip to the rounded body shape
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([x0, y0, x1, y1], radius=40, fill=255)
    shell = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shell.paste(body, (0, 0), mask)
    body = shell
    d = ImageDraw.Draw(body)
    # top face: slightly darker, receding plane
    d.rounded_rectangle([x0 + 4, y0, x1 - 4, y0 + 44], radius=20,
                        fill=(148, 153, 166, 255))
    d.line([(x0 + 10, y0 + 44), (x1 - 10, y0 + 44)], fill=(120, 124, 136, 255),
           width=2)
    # broad specular band, upper left, diagonal
    spec = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    sd.polygon([(320, 500), (470, 500), (400, 794), (306, 794)],
               fill=CHROME_HI + (120,))
    sd.polygon([(520, 500), (575, 500), (520, 794), (478, 794)],
               fill=CHROME_HI + (55,))
    spec = spec.filter(ImageFilter.GaussianBlur(8))
    body.alpha_composite(spec)
    # bottom edge shading + dark base trim
    d.rounded_rectangle([x0, y1 - 16, x1, y1], radius=12,
                        fill=(72, 76, 88, 150))
    d.rounded_rectangle([x0 + 16, y1 - 2, x1 - 16, y1 + 12], radius=8,
                        fill=(50, 53, 64, 255))
    img.alpha_composite(body)


def slot_and_pea(img):
    """The single narrow slot, the spring, and the popping pea."""
    d = ImageDraw.Draw(img)
    # one comically narrow slot, centred on the top face
    d.rounded_rectangle([494, 504, 530, 530], radius=8, fill=SLOT_DARK)
    d.rounded_rectangle([498, 508, 526, 516], radius=4, fill=(6, 6, 8))
    # spring: bright zig-zag coil rising out of the slot to the pea
    coil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(coil)
    pts = []
    y = 512
    for i in range(9):
        pts.append((512 + (17 if i % 2 == 0 else -17), y))
        y -= 9
    cd.line(pts, fill=(228, 231, 238, 255), width=7, joint="curve")
    cd.line(pts, fill=(120, 124, 134, 255), width=2, joint="curve")
    coil = coil.filter(ImageFilter.GaussianBlur(0.8))
    img.alpha_composite(coil)
    # pea: glossy sphere, bigger now, sitting on the spring mid-pop
    pea = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pea)
    cx, cy, r = 512, 372, 58
    pd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PEA_GREEN)
    # shading: darker lower right
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shade)
    for i in range(18):
        rr = r * (1 - i / 18)
        a = int(75 * (i / 18))
        shd.ellipse([cx - rr + 10, cy - rr + 12, cx + rr + 10, cy + rr + 12],
                    fill=PEA_DARK + (a,))
    shade = shade.filter(ImageFilter.GaussianBlur(3))
    pea.alpha_composite(shade)
    # golden-brown toasted patch across the pea's upper right (a toast mark,
    # not a dot — it reads as a browned cap)
    pd.pieslice([cx - r + 4, cy - r + 2, cx + r - 2, cy + r - 6],
                start=295, end=25, fill=TOAST_MARK)
    pd.pieslice([cx - r + 12, cy - r + 10, cx + r - 10, cy + r - 12],
                start=300, end=18, fill=(198, 142, 68))
    # small specular crescent, upper left
    pd.pieslice([cx - r + 6, cy - r + 8, cx + r - 26, cy + r - 30],
                start=200, end=290, fill=PEA_LITE)
    pd.ellipse([cx - 34, cy - 38, cx - 16, cy - 24], fill=(238, 252, 218))
    pea = pea.filter(ImageFilter.GaussianBlur(0.6))
    img.alpha_composite(pea)
    # motion lines: pea is mid-pop
    md = ImageDraw.Draw(img)
    for dx, ln in [(-76, 30), (-60, 44), (60, 44), (76, 30)]:
        md.line([(512 + dx, 306), (512 + dx, 306 - ln)],
                fill=(118, 122, 132, 180), width=4)


def smoke(img):
    """A thin wisp of toast smoke curling from the slot."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    for i in range(60):
        t = i / 59
        x = 566 + 30 * math.sin(t * math.pi * 2.2) * (1 - t * 0.4)
        y = 500 - t * 210
        pts.append((x, y))
    for i in range(0, len(pts) - 1, 2):
        wdt = max(3, int(18 * (1 - i / len(pts)) + 4))
        d.line([pts[i], pts[i + 1]], fill=(240, 240, 243, 175), width=wdt)
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(layer)


def lever_and_mark(img):
    """Side lever (pressed down) and the tiny PEA-1 brand mark."""
    d = ImageDraw.Draw(img)
    # vertical slider track on the right face, knob pressed low
    d.rounded_rectangle([700, 580, 716, 690], radius=8,
                        fill=(88, 92, 104, 255))
    d.rounded_rectangle([688, 652, 728, 686], radius=12,
                        fill=(44, 46, 56, 255))
    d.ellipse([696, 660, 720, 678], fill=(214, 218, 228, 255))
    # brand mark, small, on the chrome front
    try:
        font = ImageFont.load_default(30)
    except Exception:
        font = ImageFont.load_default()
    d.text((512, 724), "PEA-1", font=font, fill=(56, 58, 68, 255),
           anchor="mm")


def plate_and_butter(img):
    """The ONE accessory: a small white plate with a single pat of butter."""
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    cx, cy = 842, 748
    # plate ellipse: rim, face, well
    d.ellipse([cx - 108, cy - 34, cx + 108, cy + 34], fill=(226, 227, 232, 255))
    d.ellipse([cx - 100, cy - 30, cx + 100, cy + 30], fill=PLATE_WHITE)
    d.ellipse([cx - 70, cy - 20, cx + 70, cy + 20], fill=(236, 237, 242, 255))
    # butter pat: glossy little cube, lit top face, shaded side faces
    d.polygon([(cx - 30, cy - 24), (cx + 10, cy - 38), (cx + 40, cy - 22),
               (cx + 34, cy + 4), (cx - 24, cy + 4)], fill=BUTTER)
    d.polygon([(cx - 30, cy - 24), (cx + 10, cy - 38), (cx + 40, cy - 22),
               (cx + 34, cy - 10), (cx - 24, cy - 10)], fill=(254, 238, 156))
    d.polygon([(cx + 34, cy - 10), (cx + 40, cy - 22), (cx + 34, cy + 4),
               (cx + 34, cy - 10)], fill=BUTTER_DARK)
    d.line([(cx - 30, cy - 24), (cx - 24, cy + 4)], fill=BUTTER_DARK, width=2)
    plate = plate.filter(ImageFilter.GaussianBlur(0.5))
    img.alpha_composite(plate)


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    vgrad(img, BG_TOP, BG_MID, BG_BOT)
    radial_glow(img, 300, 180, 520, (255, 244, 214), alpha=55)
    # floor shadows under toaster and plate
    soft_shadow(img, [286, 792, 744, 836], blur=22, alpha=120)
    soft_shadow(img, [740, 770, 956, 794], blur=14, alpha=70)
    chrome_body(img)
    slot_and_pea(img)
    smoke(img)
    lever_and_mark(img)
    plate_and_butter(img)
    # gentle vignette to focus the hero
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, H], outline=(60, 62, 72, 60), width=26)
    vig = vig.filter(ImageFilter.GaussianBlur(30))
    img.alpha_composite(vig)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isdir(outdir):
        outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, OUT_NAME)
    img.convert("RGB").save(path, format="PNG", optimize=True)
    print(f"wrote {path} {W}x{H} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
