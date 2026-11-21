from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

W, H = 1200, 675
random.seed(6)

# ---------- sunset sky ----------
sky = Image.new('RGB', (W, H))
px = sky.load()
# vertical gradient: deep purple -> magenta -> orange -> gold
stops = [(0.0, (26, 8, 60)), (0.35, (96, 20, 90)), (0.58, (196, 40, 90)), (0.75, (248, 110, 60)), (0.88, (255, 180, 80)), (1.0, (255, 220, 130))]
for y in range(H):
    t = y / H
    # find segment
    for i in range(len(stops)-1):
        t0, c0 = stops[i]; t1, c1 = stops[i+1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            col = tuple(int(c0[k] + (c1[k]-c0[k]) * f) for k in range(3))
            break
    else:
        col = stops[-1][1]
    for x in range(W):
        px[x, y] = col

d = ImageDraw.Draw(sky, 'RGBA')
# sun
sun_cx, sun_cy, sun_r = 600, 400, 110
for r in range(sun_r, 0, -1):
    a = int(255 * (1 - r / sun_r) * 0.35)
    d.ellipse([sun_cx-r, sun_cy-r, sun_cx+r, sun_cy+r], fill=(255, 230, 150, a))
d.ellipse([sun_cx-sun_r, sun_cy-sun_r, sun_cx+sun_r, sun_cy+sun_r], fill=(255, 236, 170, 255))
# sun slats (retro)
for i, yy in enumerate(range(sun_cy+10, sun_cy+sun_r, 18)):
    d.rectangle([sun_cx-sun_r, yy, sun_cx+sun_r, yy+6], fill=(248, 110, 60, 255))

# ocean (bottom)
ocean_y = 470
d.rectangle([0, ocean_y, W, H], fill=(16, 10, 46))
# sun reflection streak
for i in range(40):
    x = sun_cx + random.randint(-70, 70)
    y = ocean_y + random.randint(5, H-ocean_y-8)
    w = random.randint(30, 120)
    d.rectangle([x, y, x+w, y+3], fill=(255, 170, 90, random.randint(60, 160)))

# skyline silhouette (dark)
def skyline(y_base, h_min, h_max, color):
    x = 0
    while x < W:
        bw = random.randint(40, 110)
        bh = random.randint(h_min, h_max)
        d.rectangle([x, y_base-bh, x+bw, y_base], fill=color)
        # antenna
        if random.random() < 0.4:
            d.rectangle([x+bw//2-2, y_base-bh-22, x+bw//2+2, y_base-bh], fill=color)
        # lit windows
        for _ in range(random.randint(2, 8)):
            wx = x + random.randint(4, max(5, bw-10))
            wy = y_base - random.randint(10, max(11, bh-8))
            d.rectangle([wx, wy, wx+5, wy+7], fill=(255, 200, 90, 255))
        x += bw + random.randint(2, 14)
skyline(ocean_y, 40, 130, (24, 8, 48))
# palm trees
def palm(x, y, s, color=(12, 6, 30)):
    d.line([x, y, x+6*s, y-70*s], fill=color, width=max(3, int(5*s)))
    for ang in range(-70, 71, 28):
        rad = math.radians(ang - 90)
        ex = x + 6*s + math.cos(rad) * 55*s
        ey = y - 70*s + math.sin(rad) * 28*s
        d.line([x+6*s, y-70*s, ex, ey], fill=color, width=max(2, int(4*s)))
        # droop
        d.line([ex, ey, ex+8*s, ey+18*s], fill=color, width=max(2, int(3*s)))
palm(90, ocean_y+6, 1.0)
palm(1080, ocean_y+4, 0.85)
palm(1010, ocean_y+8, 0.6)

# ---------- make.fun ghost badge (circular crop of icon) ----------
icon = Image.open('/home/hatch/workspace/makefun/gta6-meme-x-01/assets/icon-512.png').convert('RGBA')
# icon is a magenta circle on white; make a circular mask centred on it
mask = Image.new('L', icon.size, 0)
md = ImageDraw.Draw(mask)
md.ellipse([18, 18, 494, 494], fill=255)
badge = Image.new('RGBA', icon.size, (0,0,0,0))
badge.paste(icon, (0,0), mask)
badge = badge.resize((300, 300), Image.LANCZOS)
# soft shadow
shadow = Image.new('RGBA', (W, H), (0,0,0,0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([905, 150, 905+300, 150+300], fill=(0,0,0,110))
shadow = shadow.filter(ImageFilter.GaussianBlur(14))
sky = Image.alpha_composite(sky.convert('RGBA'), shadow)
sky.paste(badge, (905, 140), badge)

# ---------- meme text (bold white, black outline) ----------
def text_outline(draw, xy, text, font, fill=(255,255,255), outline=(0,0,0), width=6):
    x, y = xy
    for dx in range(-width, width+1):
        for dy in range(-width, width+1):
            if dx*dx + dy*dy <= width*width:
                draw.text((x+dx, y+dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)

def load_font(size, bold=True):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
    except Exception:
        return ImageFont.load_default()

d = ImageDraw.Draw(sky)
f_top = load_font(64)
f_bot = load_font(64)
f_small = load_font(34)

top1 = "WAITED 13 YEARS"
top2 = "FOR GTA 6"
# centre top lines
for i, line in enumerate([top1, top2]):
    bb = d.textbbox((0,0), line, font=f_top)
    tw = bb[2]-bb[0]
    text_outline(d, ((W-tw)//2, 28 + i*72), line, f_top)
bot1 = "MY AGENT GOT"
bot2 = "PAID FIRST"
for i, line in enumerate([bot1, bot2]):
    bb = d.textbbox((0,0), line, font=f_bot)
    tw = bb[2]-bb[0]
    text_outline(d, ((W-tw)//2, H-168 + i*72), line, f_bot)

# make.fun wordmark bottom-left, on a dark pill
wm = "make.fun"
bb = d.textbbox((0,0), wm, font=f_small)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
pill = Image.new('RGBA', (tw+44, th+26), (0,0,0,0))
pd = ImageDraw.Draw(pill)
pd.rounded_rectangle([0,0,tw+44, th+26], radius=13, fill=(0,0,0,170))
pd.text((22, 12), wm, font=f_small, fill=(255,255,255))
sky.paste(pill, (24, H-58), pill)
# small ghost badge next to wordmark? keep clean: add tiny star
d = ImageDraw.Draw(sky)

out = '/home/hatch/workspace/makefun/gta6-meme-x-01/meme.jpg'
sky.convert('RGB').save(out, 'JPEG', quality=90)
print('saved', out)
from PIL import Image as I
im = I.open(out); print(im.size)
import os; print(os.path.getsize(out), 'bytes')
