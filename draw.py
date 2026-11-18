# draw.py — draws entry.png: a 1024x1024 world-news infographic for
# Wednesday 18 November 2026. Four stories, 2x2 grid, flat PIL icons.
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")

def starburst(draw, cx, cy, r_out, r_in, points, fill):
    """Simple star polygon (explosion burst) centred at cx, cy."""
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)

def icon_gulf(draw, x0, y0, x1, y1):
    # Dark sea, tan island, yellow explosion burst, small jet triangle.
    sky = (253, 240, 228)
    draw.rectangle([x0, y0, x1, y1], fill=sky)
    sea_y = y0 + int((y1 - y0) * 0.55)
    draw.rectangle([x0, sea_y, x1, y1], fill=(23, 68, 110))
    draw.ellipse([x0 + 150, sea_y - 14, x1 - 150, sea_y + 26], fill=(210, 180, 130))
    cx = (x0 + x1) // 2
    starburst(draw, cx, sea_y - 34, 34, 16, 9, (245, 197, 24))
    starburst(draw, cx, sea_y - 34, 18, 9, 9, (232, 90, 20))
    jx, jy = x0 + 52, y0 + 16
    draw.polygon([(jx, jy), (jx + 46, jy + 10), (jx, jy + 20)], fill=(30, 30, 30))

def icon_bridge(draw, x0, y0, x1, y1):
    # Water, bridge deck, one intact arch, one collapsed arch.
    draw.rectangle([x0, y0, x1, y1], fill=(227, 237, 247))
    water_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, water_y, x1, y1], fill=(38, 110, 180))
    deck_y = y0 + 26
    draw.rectangle([x0 + 10, deck_y, x0 + 210, deck_y + 12], fill=(90, 96, 104))
    draw.rectangle([x0 + 280, deck_y, x1 - 10, deck_y + 12], fill=(90, 96, 104))
    # Intact arch under the left deck span.
    draw.arc([x0 + 40, deck_y - 6, x0 + 180, deck_y + 62],
             0, 180, fill=(90, 96, 104), width=9)
    # Collapsed span: tilted segment falling into the water.
    draw.polygon([(x0 + 290, deck_y + 12), (x0 + 330, deck_y + 12),
                  (x0 + 356, water_y + 22), (x0 + 318, water_y + 28)],
                 fill=(120, 126, 134))
    draw.ellipse([x0 + 320, water_y + 12, x0 + 360, water_y + 34],
                 fill=(255, 255, 255))

def icon_summit(draw, x0, y0, x1, y1):
    # Three small flags side by side (US, China, Russia), three figures below.
    draw.rectangle([x0, y0, x1, y1], fill=(234, 245, 234))
    fw, fh = 132, 50
    gap = 18
    total = fw * 3 + gap * 2
    sx = x0 + (x1 - x0 - total) // 2
    fy = y0 + 6
    # US flag: red/white stripes + blue canton with dots.
    ux = sx
    for i in range(7):
        draw.rectangle([ux, fy + i * 7, ux + fw, fy + (i + 1) * 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([ux, fy, ux + 52, fy + 22], fill=(30, 60, 140))
    for r in range(2):
        for c in range(4):
            draw.ellipse([ux + 6 + c * 12, fy + 4 + r * 9,
                          ux + 10 + c * 12, fy + 8 + r * 9], fill=(255, 255, 255))
    # China flag: red field, one big yellow star + small stars.
    cx = sx + fw + gap
    draw.rectangle([cx, fy, cx + fw, fy + fh], fill=(222, 41, 16))
    starburst(draw, cx + 22, fy + 18, 11, 5, 5, (255, 222, 0))
    for sx2, sy2 in [(cx + 48, fy + 9), (cx + 60, fy + 20), (cx + 54, fy + 32)]:
        starburst(draw, sx2, sy2, 5, 2, 5, (255, 222, 0))
    # Russia flag: white / blue / red horizontal bands.
    rx = sx + 2 * (fw + gap)
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([rx, fy + i * 17, rx + fw, fy + (i + 1) * 17], fill=col)
    # Three figures (heads + shoulders) under the flags, inside the band.
    for i, col in enumerate([(30, 60, 140), (222, 41, 16), (0, 57, 166)]):
        hx = sx + fw // 2 + i * (fw + gap)
        draw.ellipse([hx - 9, fy + fh + 4, hx + 9, fy + fh + 22], fill=(245, 200, 160))
        draw.pieslice([hx - 17, fy + fh + 20, hx + 17, fy + fh + 44],
                      180, 360, fill=col)

def icon_measles(draw, x0, y0, x1, y1):
    # Red virus circle with radiating spikes, plus a shield with a cross.
    draw.rectangle([x0, y0, x1, y1], fill=(253, 236, 234))
    cx, cy = x0 + 120, y0 + 52
    import math
    for k in range(12):
        a = 2 * math.pi * k / 12
        x2 = cx + 52 * math.cos(a)
        y2 = cy + 52 * math.sin(a)
        draw.line([cx, cy, x2, y2], fill=(185, 28, 28), width=6)
        draw.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(185, 28, 28))
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(220, 38, 38))
    for dx, dy in [(-14, -10), (12, -14), (-8, 12), (16, 8)]:
        draw.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                     fill=(185, 28, 28))
    # Shield with a white cross, right side.
    sx, sy = x1 - 150, y0 + 12
    draw.polygon([(sx, sy), (sx + 76, sy), (sx + 76, sy + 44),
                  (sx + 38, sy + 74), (sx, sy + 44)], fill=(22, 101, 52))
    draw.rectangle([sx + 32, sy + 12, sx + 44, sy + 48], fill=(255, 255, 255))
    draw.rectangle([sx + 18, sy + 24, sx + 58, sy + 36], fill=(255, 255, 255))

STORIES = [
    ("MIDDLE EAST", (154, 52, 18), icon_gulf,
     "US strikes Iran; Iran hits Bahrain and Kuwait",
     "US jets hit a Revolutionary Guard missile site on Qeshm Island; "
     "Iran fired drones at Bahrain and Kuwait."),
    ("EUROPE", (30, 64, 175), icon_bridge,
     "Crimea bridge partly collapses",
     "A Ukrainian drone and missile strike partly destroyed the Kerch "
     "bridge; one arch fell into the strait. Zelensky confirmed it."),
    ("DIPLOMACY", (22, 101, 52), icon_summit,
     "Trump flies to China for Xi–Putin talks",
     "President Trump left the Philippines and headed to China for a "
     "three-way meeting with Xi Jinping and Vladimir Putin in Shenzhen."),
    ("HEALTH", (185, 28, 28), icon_measles,
     "US loses measles-free status",
     "Worst outbreak in 30 years — 5,400+ cases and 10 deaths. The US "
     "loses the measles elimination status it held for 26 years."),
]

PANEL_BG = [(253, 240, 228), (227, 237, 247), (234, 245, 234), (253, 236, 234)]

def draw_panel(draw, x, y, w, h, idx):
    tag, accent, icon_fn, headline, body = STORIES[idx]
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG[idx])
    pad = 18
    inner = w - 2 * pad
    # Tag line.
    draw.text((x + pad, y + 14), tag, font=font(BOLD, 22), fill=accent)
    # Icon band.
    iy0, iy1 = y + 44, y + 132
    icon_fn(draw, x + pad, iy0, x + w - pad, iy1)
    # Headline, 38px bold, up to 3 lines.
    hf = font(BOLD, 38)
    lines = wrap(draw, headline, hf, inner)
    hy = iy1 + 12
    for ln in lines:
        draw.text((x + pad, hy), ln, font=hf, fill=(20, 20, 20))
        hy += 45
    # Body, 24px, up to 4 lines.
    bf = font(REG, 24)
    blines = wrap(draw, body, bf, inner)
    by = hy + 8
    for ln in blines:
        draw.text((x + pad, by), ln, font=bf, fill=(50, 50, 50))
        by += 30

def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Header band.
    draw.rectangle([0, 0, W, 148], fill=(16, 38, 59))
    center(draw, W // 2, 16, "WORLD NEWS", font(BOLD, 72), (255, 255, 255))
    center(draw, W // 2, 100, "WEDNESDAY 18 NOVEMBER 2026",
           font(BOLD, 34), (245, 197, 24))
    # 2x2 grid of story panels.
    gx, gy = 8, 156
    pw, ph, gap = 500, 404, 8
    for i in range(4):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, i)
    # Footer strip.
    draw.rectangle([0, 980, W, H], fill=(16, 38, 59))
    center(draw, W // 2, 990, "Sources: major wire and newspaper roundups, 18 Nov 2026",
           font(REG, 20), (200, 210, 220))
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()

