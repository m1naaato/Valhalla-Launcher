"""
Generate 32x32 bridge item textures with 3D pixel-art shading.
Arcadia V2 cross-mod bridge components.
Author: vyrriox
"""
from PIL import Image, ImageDraw
import os, math, random

OUT = os.path.dirname(os.path.abspath(__file__))
SIZE = 32

def new_img():
    return Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))

def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))

def px(d, x, y, c):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        d.point((x,y), c)

def rect(d, x1, y1, x2, y2, c):
    d.rectangle([x1,y1,x2,y2], fill=c)

def blend(a, b, t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(4))

# ---------- 1. ARCANE CIRCUIT ----------
# PCB board with glowing arcane runes + gold chip + source gem
def arcane_circuit():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Base board (dark purple-blue, shaded)
    base = (38, 22, 66, 255)
    base_lt = (62, 40, 100, 255)
    base_dk = (18, 10, 36, 255)
    edge = (10, 6, 22, 255)
    # outer silhouette
    rect(d, 3, 4, 28, 27, edge)
    rect(d, 4, 5, 27, 26, base)
    # top highlight
    for x in range(4, 28):
        px(d, x, 5, base_lt)
    for y in range(5, 27):
        px(d, 4, y, base_lt)
    # bottom/right shadow
    for x in range(4, 28):
        px(d, x, 26, base_dk)
    for y in range(5, 27):
        px(d, 27, y, base_dk)

    # Golden chip in center (6x5)
    gold = (218, 176, 66, 255)
    gold_lt = (255, 232, 128, 255)
    gold_dk = (140, 100, 28, 255)
    rect(d, 12, 13, 19, 17, gold)
    rect(d, 12, 13, 19, 13, gold_lt)
    rect(d, 12, 17, 19, 17, gold_dk)
    rect(d, 19, 13, 19, 17, gold_dk)
    # chip pins
    for y in (11,12,18,19):
        for x in (13,15,17):
            px(d, x, y, (80,80,80,255))
            px(d, x, y, (80,80,80,255))
    # chip runic sigil (source gem cyan)
    cyan = (110, 230, 220, 255)
    px(d, 15, 15, cyan); px(d, 16, 15, cyan)
    px(d, 15, 14, (180,255,250,255)); px(d, 16, 14, (180,255,250,255))

    # Circuit traces (glowing cyan + magenta)
    trace = (80, 200, 210, 255)
    trace_g = (180, 240, 240, 255)
    magenta = (200, 80, 200, 255)
    # traces from chip outward
    for x in range(7, 12):
        px(d, x, 15, trace)
    for x in range(20, 25):
        px(d, x, 15, trace)
    for y in range(8, 13):
        px(d, 15, y, magenta); px(d, 16, y, magenta)
    for y in range(18, 24):
        px(d, 15, y, magenta); px(d, 16, y, magenta)
    # solder pads
    for (x,y) in [(7,15),(24,15),(15,8),(16,8),(15,23),(16,23),(6,10),(25,10),(6,20),(25,20)]:
        px(d, x, y, trace_g)

    # Corner vias
    for (x,y) in [(6,8),(25,8),(6,22),(25,22)]:
        px(d, x, y, (10,10,10,255))
        px(d, x-1, y, base_dk)
    # Decorative arcane dots (sparkle)
    px(d, 9, 12, trace_g)
    px(d, 22, 18, trace_g)
    # Top-left highlight corner
    px(d, 4, 4, (120, 90, 160, 255))
    px(d, 5, 4, base_lt)

    save(img, "arcane_circuit")

# ---------- 2. ETHEREAL ALLOY ----------
# Ghostly swirling ingot, purple-teal gradient, glowing soul wisps
def ethereal_alloy():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Ingot silhouette (tapered bar)
    dk = (22, 8, 38, 255)
    mid = (72, 36, 110, 255)
    lt = (140, 88, 180, 255)
    glow = (200, 150, 230, 255)
    teal = (80, 220, 210, 255)
    teal_lt = (180, 255, 240, 255)

    # outer outline
    pts = [
        (7,9),(8,8),(23,8),(24,9),(25,10),(25,20),(24,22),(8,22),(7,21),(7,10)
    ]
    d.polygon(pts, fill=mid, outline=dk)
    # inner highlight top
    rect(d, 9, 10, 23, 11, lt)
    rect(d, 10, 10, 22, 10, glow)
    # inner shadow bottom
    rect(d, 9, 20, 23, 21, dk)
    # rim shine
    for x in range(11, 22):
        px(d, x, 9, teal_lt)
    # swirling soul wisps (teal)
    for (x,y) in [(11,13),(12,12),(14,14),(17,13),(20,14),(22,12),(13,16),(16,17),(19,16),(21,17),(12,19),(15,18),(18,19),(20,18)]:
        px(d, x, y, teal)
    # brighter wisp core
    for (x,y) in [(14,14),(17,13),(16,17),(18,19)]:
        px(d, x, y, teal_lt)
    # ghostly sparkle floating above
    px(d, 10, 6, teal_lt)
    px(d, 22, 5, glow)
    px(d, 26, 11, teal_lt)
    px(d, 5, 15, glow)
    # bottom drip (liquid soul)
    px(d, 15, 23, glow)
    px(d, 16, 23, glow)
    px(d, 15, 24, teal_lt)
    # extra shading
    for x in range(8, 25):
        px(d, x, 22, dk)
    save(img, "ethereal_alloy")

# ---------- 3. INDUSTRIAL HEART ----------
# Mechanical heart with gears, pistons, red glow core
def industrial_heart():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Heart silhouette: brass/steel
    steel_dk = (44, 44, 52, 255)
    steel = (96, 96, 108, 255)
    steel_lt = (160, 160, 172, 255)
    brass_dk = (110, 80, 30, 255)
    brass = (180, 140, 60, 255)
    brass_lt = (240, 210, 110, 255)
    red_dk = (120, 20, 20, 255)
    red = (220, 40, 40, 255)
    red_lt = (255, 140, 80, 255)
    red_g = (255, 220, 180, 255)

    # heart outline (rough 16-wide)
    heart_pixels = []
    rows = [
        "..XX...XX..",
        ".XXXXXXXXX.",
        "XXXXXXXXXXX",
        "XXXXXXXXXXX",
        "XXXXXXXXXXX",
        ".XXXXXXXXX.",
        "..XXXXXXX..",
        "...XXXXX...",
        "....XXX....",
        ".....X....."
    ]
    ox, oy = 10, 7
    for j,row in enumerate(rows):
        for i,ch in enumerate(row):
            if ch == 'X':
                heart_pixels.append((ox+i, oy+j))
    # fill heart base steel
    for (x,y) in heart_pixels:
        px(d, x, y, steel)
    # top-left highlight
    for (x,y) in heart_pixels:
        if (x-1,y-1) not in heart_pixels and (x-1,y) in heart_pixels:
            px(d, x, y, steel_lt)
    # edge dark outline
    for (x,y) in heart_pixels:
        for (dx,dy) in [(-1,0),(1,0),(0,-1),(0,1)]:
            if (x+dx, y+dy) not in heart_pixels and 0<=x+dx<SIZE and 0<=y+dy<SIZE:
                img.putpixel((x+dx,y+dy), steel_dk)

    # Brass gears on heart (top-left, top-right)
    def gear(cx, cy, r, col_mid, col_lt, col_dk):
        for y in range(cy-r, cy+r+1):
            for x in range(cx-r, cx+r+1):
                dd = (x-cx)**2 + (y-cy)**2
                if dd <= r*r:
                    px(d, x, y, col_mid)
        # teeth
        for (dx,dy) in [(-r-1,0),(r+1,0),(0,-r-1),(0,r+1),(-r,-r),(r,-r),(-r,r),(r,r)]:
            px(d, cx+dx, cy+dy, col_mid)
        # highlight
        px(d, cx-1, cy-1, col_lt)
        px(d, cx-2, cy-1, col_lt)
        # shadow
        px(d, cx+1, cy+1, col_dk)
        # center bolt
        px(d, cx, cy, col_dk)
    gear(12, 10, 2, brass, brass_lt, brass_dk)
    gear(19, 10, 2, brass, brass_lt, brass_dk)

    # Red glowing core (inner) + pipes
    core = [(14,12),(15,12),(16,12),(14,13),(15,13),(16,13),(17,13),(14,14),(15,14),(16,14),(15,15)]
    for (x,y) in core:
        px(d, x, y, red)
    px(d, 15, 13, red_g)
    px(d, 15, 12, red_lt)
    px(d, 16, 13, red_lt)

    # Piston detail at bottom
    px(d, 14, 16, brass)
    px(d, 16, 16, brass)
    px(d, 15, 16, brass_lt)

    # Wires (copper) trailing
    cop = (200, 120, 60, 255)
    for y in range(13, 16):
        px(d, 10, y, cop)
        px(d, 21, y, cop)
    # Sparks
    px(d, 9, 9, red_g)
    px(d, 22, 9, red_g)
    save(img, "industrial_heart")

# ---------- 4. RUNE MATRIX ----------
# 3x3 rune grid with amethyst center, gold frame, glowing purple runes
def rune_matrix():
    img = new_img()
    d = ImageDraw.Draw(img)
    gold_dk = (120, 88, 28, 255)
    gold = (200, 160, 60, 255)
    gold_lt = (255, 225, 130, 255)
    bg = (28, 14, 52, 255)
    bg_lt = (60, 34, 96, 255)
    purple = (168, 94, 224, 255)
    purple_lt = (222, 178, 255, 255)
    amethyst = (178, 128, 234, 255)
    amethyst_lt = (240, 208, 255, 255)
    amethyst_dk = (90, 50, 140, 255)

    # outer gold frame 26x26 centered
    rect(d, 3, 3, 28, 28, gold_dk)
    rect(d, 4, 4, 27, 27, gold)
    rect(d, 5, 5, 26, 26, bg)
    # gold highlight
    for x in range(4, 28):
        px(d, x, 4, gold_lt)
    for y in range(4, 28):
        px(d, 4, y, gold_lt)
    # corner gems
    for (cx,cy) in [(3,3),(28,3),(3,28),(28,28)]:
        px(d, cx, cy, purple_lt)

    # 3x3 grid of rune cells, each 6x6 with 1px gap
    # grid starts at (5,5), cell size 7, gap 1 -> 3 cells = 21px. Fits 5..25
    cells = []
    for gy in range(3):
        for gx in range(3):
            x1 = 5 + gx*7
            y1 = 5 + gy*7
            x2 = x1 + 6
            y2 = y1 + 6
            cells.append((x1,y1,x2,y2,gx,gy))
    for (x1,y1,x2,y2,gx,gy) in cells:
        rect(d, x1, y1, x2, y2, bg_lt)
        rect(d, x1+1, y1+1, x2-1, y2-1, bg)

    # Center cell = amethyst gem (index 4: gx=1,gy=1)
    cx1,cy1,cx2,cy2 = 5+7, 5+7, 5+7+6, 5+7+6
    # Amethyst facets
    rect(d, cx1+1, cy1+1, cx2-1, cy2-1, amethyst)
    px(d, cx1+2, cy1+2, amethyst_lt)
    px(d, cx1+3, cy1+2, amethyst_lt)
    px(d, cx2-2, cy2-2, amethyst_dk)
    px(d, cx2-3, cy2-2, amethyst_dk)
    px(d, cx1+2, cy2-2, amethyst_dk)
    # facet line
    px(d, cx1+3, cy1+3, amethyst_lt)
    px(d, cx1+4, cy1+3, (255,255,255,255))

    # 8 surrounding runes (purple glyphs)
    runes = [
        # 3x3 rune templates (6x6 with 5x5 inner)
        [(0,0),(1,0),(2,0),(0,2),(2,2),(0,4),(1,4),(2,4)],  # H
        [(0,0),(1,1),(2,2),(3,1),(4,0),(2,0),(2,4)],          # sigil
        [(0,0),(0,4),(4,0),(4,4),(2,2)],                       # X dot
        [(2,0),(0,2),(4,2),(2,4),(1,1),(3,1),(1,3),(3,3)],    # diamond
        [(0,0),(1,0),(2,0),(3,0),(4,0),(0,4),(4,4),(2,2)],    # T
        [(0,4),(1,3),(2,2),(3,1),(4,0),(0,0),(4,4)],           # slash
        [(2,0),(1,1),(3,1),(0,2),(4,2),(1,3),(3,3),(2,4)],    # circle
        [(0,0),(1,0),(2,0),(0,1),(0,2),(0,3),(0,4),(4,4),(3,4),(2,4)]  # L
    ]
    # map to grid positions excluding center (index 4)
    grid_positions = [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2)]
    for idx, (gx,gy) in enumerate(grid_positions):
        x1 = 5 + gx*7 + 1
        y1 = 5 + gy*7 + 1
        for (rx,ry) in runes[idx % len(runes)]:
            px(d, x1+rx, y1+ry, purple)
            if (rx+ry) % 2 == 0:
                px(d, x1+rx, y1+ry, purple_lt)

    save(img, "rune_matrix")

if __name__ == "__main__":
    arcane_circuit()
    ethereal_alloy()
    industrial_heart()
    rune_matrix()
    print("generated 4 bridge textures (32x32)")
