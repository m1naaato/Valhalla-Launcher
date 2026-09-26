"""
Master generator for all Arcadia custom item textures at 64x64 with 3D pixel-art shading.
Author: vyrriox

Produces:
  - 6 keys (basic/common/rare/legendary/arcadia/vote) + token_casino
  - 20 fusion chain items + 4 incomplete transitionals
  - heart_of_arcadia
  - 14 adept items (4 armor + 10 unique)
  - 14 heretic items (4 armor + 10 unique)
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math

OUT = os.path.dirname(os.path.abspath(__file__))
SIZE = 64
CX, CY = SIZE // 2, SIZE // 2

# ============================================================
# HELPERS
# ============================================================

def new_img():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))

def px(img, x, y, c):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        img.putpixel((x, y), c)

def blend(a, b, t):
    return tuple(int(a[i]*(1-t) + b[i]*t) for i in range(len(a)))

def lerp(v0, v1, t):
    return v0 + (v1 - v0) * t

def radial_shade(img, cx, cy, r, base, lt, dk, outline=None):
    """Fill a circle with radial shading (top-left lit)."""
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            dx = x - cx
            dy = y - cy
            d = math.sqrt(dx*dx + dy*dy)
            if d <= r:
                # light from upper-left
                if d > 0:
                    nx, ny = dx / d, dy / d
                    ldot = (-0.7) * nx + (-0.7) * ny
                    if ldot > 0.3:
                        c = blend(base, lt, min(1, ldot))
                    elif ldot < -0.3:
                        c = blend(base, dk, min(1, -ldot))
                    else:
                        c = base
                else:
                    c = lt
                px(img, x, y, c)
            elif d <= r + 0.7 and outline:
                px(img, x, y, outline)

def shaded_rect(img, x1, y1, x2, y2, base, lt, dk):
    """Draw a rect with top/left highlight and bottom/right shadow."""
    d = ImageDraw.Draw(img)
    d.rectangle([x1, y1, x2, y2], fill=base)
    # top highlight
    for x in range(x1, x2 + 1):
        px(img, x, y1, lt)
    # left highlight
    for y in range(y1, y2 + 1):
        px(img, x1, y, lt)
    # bottom shadow
    for x in range(x1, x2 + 1):
        px(img, x, y2, dk)
    # right shadow
    for y in range(y1, y2 + 1):
        px(img, x2, y, dk)

def vertical_gradient(img, x1, y1, x2, y2, top, bot):
    for y in range(y1, y2 + 1):
        t = (y - y1) / max(1, (y2 - y1))
        c = blend(top, bot, t)
        for x in range(x1, x2 + 1):
            px(img, x, y, c)

# ============================================================
# KEYS
# ============================================================

def draw_key(body_col, bow_col, glow=None, name='key'):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = body_col
    lt = blend(base, (255, 255, 255, 255), 0.45)
    dk = blend(base, (0, 0, 0, 255), 0.45)
    outline = blend(base, (0, 0, 0, 255), 0.7)

    # BOW (round head, left side — angled diagonal)
    bx, by = 18, 18
    r = 11
    radial_shade(img, bx, by, r, base, lt, dk, outline)
    # inner hole
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(0, 0, 0, 255))
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(0, 0, 0, 0))
    # inner rim highlight
    px(img, bx - 3, by - 2, lt)
    px(img, bx - 2, by - 3, lt)

    # SHAFT (extending to bottom-right)
    # shaft from (bx+8, by+3) to (54, 54)
    sx1, sy1 = 27, 27
    sx2, sy2 = 52, 52
    # draw shaft as a thick diagonal line (3px thick)
    for t in range(0, 100):
        tt = t / 99
        px_ = int(lerp(sx1, sx2, tt))
        py_ = int(lerp(sy1, sy2, tt))
        # perpendicular thickness
        for dx, dy in [(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)]:
            px(img, px_ + dx, py_ + dy, base)
        # center highlight
        px(img, px_, py_, lt)
    # thicken
    for t in range(0, 100):
        tt = t / 99
        px_ = int(lerp(sx1, sx2, tt))
        py_ = int(lerp(sy1, sy2, tt))
        px(img, px_ - 1, py_, base)
        px(img, px_ + 1, py_, dk)

    # TEETH (bottom end)
    d.rectangle([50, 48, 54, 54], fill=base)
    d.rectangle([50, 48, 54, 48], fill=lt)
    d.rectangle([50, 54, 54, 54], fill=dk)
    # teeth notches
    d.rectangle([54, 52, 58, 54], fill=base)
    d.rectangle([54, 48, 56, 50], fill=base)
    d.rectangle([54, 48, 56, 48], fill=lt)
    d.rectangle([54, 52, 58, 52], fill=lt)
    d.rectangle([54, 54, 58, 54], fill=dk)

    # Bow accent gem
    d.ellipse([bx + 4, by - 2, bx + 8, by + 2], fill=bow_col)
    px(img, bx + 5, by - 1, blend(bow_col, (255, 255, 255, 255), 0.5))

    # glow sparkle
    if glow:
        for gx, gy in [(bx - 7, by - 7), (55, 45), (25, 45)]:
            px(img, gx, gy, glow)

    save(img, name)


# ============================================================
# TOKEN
# ============================================================

def draw_token():
    img = new_img()
    d = ImageDraw.Draw(img)
    gold = (218, 165, 32, 255)
    gold_lt = (255, 220, 90, 255)
    gold_dk = (130, 90, 10, 255)
    outline = (50, 30, 0, 255)

    # main coin
    radial_shade(img, CX, CY, 22, gold, gold_lt, gold_dk, outline)

    # inner ring
    for ang in range(0, 360, 10):
        a = math.radians(ang)
        x = int(CX + math.cos(a) * 18)
        y = int(CY + math.sin(a) * 18)
        px(img, x, y, gold_dk)

    # center star ($ symbol)
    d.line([CX - 2, CY - 8, CX + 2, CY + 8], fill=outline, width=2)
    d.ellipse([CX - 6, CY - 4, CX + 6, CY], fill=None, outline=outline, width=1)
    d.ellipse([CX - 6, CY, CX + 6, CY + 4], fill=None, outline=outline, width=1)
    # S shape approximation
    d.arc([CX - 6, CY - 6, CX + 6, CY + 2], 90, 270, fill=outline, width=2)
    d.arc([CX - 6, CY - 2, CX + 6, CY + 6], 270, 90, fill=outline, width=2)

    # sparkle
    px(img, CX - 10, CY - 10, (255, 255, 255, 255))
    px(img, CX + 12, CY - 8, gold_lt)

    save(img, "token_casino")


# ============================================================
# FUSION CHAIN — TIERED PALETTES
# ============================================================

def draw_ingot(palette, name, glow=False, overlay=None):
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # trapezoid ingot
    pts = [
        (14, 22), (16, 20), (48, 20), (50, 22),
        (52, 26), (52, 42), (50, 44),
        (14, 44), (12, 42), (12, 26)
    ]
    d.polygon(pts, fill=base, outline=blend(base, (0, 0, 0, 255), 0.5))
    # top highlight band
    d.rectangle([16, 21, 48, 25], fill=lt)
    d.rectangle([16, 21, 48, 22], fill=blend(lt, (255, 255, 255, 255), 0.4))
    # bottom shadow
    d.rectangle([16, 40, 48, 43], fill=dk)
    # edges
    for y in range(21, 44):
        px(img, 13, y, dk)
        px(img, 51, y, dk)
    # glow overlay
    if glow:
        for (x, y) in [(20, 26), (30, 30), (40, 27), (35, 35)]:
            px(img, x, y, (255, 255, 255, 255))
    if overlay == 'runes':
        d.rectangle([22, 29, 24, 31], fill=lt)
        d.rectangle([30, 29, 32, 31], fill=lt)
        d.rectangle([38, 29, 40, 31], fill=lt)
    save(img, name)


def draw_dust(palette, name):
    """Small pile of colored dust."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # pile shape
    pts = [(14, 48), (18, 36), (26, 28), (38, 28), (46, 36), (50, 48)]
    d.polygon(pts, fill=base, outline=blend(base, (0, 0, 0, 255), 0.4))
    # highlight band
    d.polygon([(20, 40), (26, 32), (38, 32), (44, 40), (40, 38), (32, 36), (24, 38)], fill=lt)
    # top sparkles
    for (x, y) in [(24, 26), (32, 22), (40, 26), (28, 24), (36, 24)]:
        px(img, x, y, lt)
        px(img, x + 1, y + 1, base)
    # specks
    for (x, y) in [(18, 34), (46, 34), (30, 38), (34, 42)]:
        px(img, x, y, blend(base, (255, 255, 255, 255), 0.7))
    save(img, name)


def draw_crystal(palette, name, tall=False, glow=True):
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    if tall:
        # vertical diamond
        pts = [(32, 12), (46, 26), (46, 42), (32, 54), (18, 42), (18, 26)]
    else:
        pts = [(32, 16), (50, 32), (32, 48), (14, 32)]
    d.polygon(pts, fill=base, outline=blend(base, (0, 0, 0, 255), 0.55))
    # facets
    # inner line highlights
    d.line([(20, 28), (32, 18)], fill=lt, width=2)
    d.line([(32, 18), (44, 28)], fill=blend(lt, base, 0.3), width=2)
    d.line([(20, 36), (32, 46)], fill=dk, width=2)
    d.line([(32, 46), (44, 36)], fill=dk, width=1)
    d.line([(32, 18), (32, 46)], fill=blend(lt, base, 0.2), width=1)

    if glow:
        # center bright
        d.ellipse([29, 29, 35, 35], fill=blend(lt, (255, 255, 255, 255), 0.7))
        # sparkles
        for (x, y) in [(18, 20), (46, 20), (20, 46), (46, 46)]:
            px(img, x, y, blend(lt, (255, 255, 255, 255), 0.5))
    save(img, name)


def draw_plate(palette, name, riveted=False):
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # rectangular plate
    shaded_rect(img, 10, 16, 54, 48, base, lt, dk)
    # inner panel
    shaded_rect(img, 14, 20, 50, 44, blend(base, lt, 0.2), lt, dk)
    # rivets
    if riveted:
        for (x, y) in [(16, 22), (48, 22), (16, 42), (48, 42), (32, 32)]:
            radial_shade(img, x, y, 2, dk, base, (0, 0, 0, 255))
    save(img, name)


def draw_circuit_card(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # card
    shaded_rect(img, 10, 12, 54, 52, base, lt, dk)
    shaded_rect(img, 12, 14, 52, 50, blend(base, dk, 0.3), lt, dk)

    # gold pads (chips)
    gold = (220, 180, 80, 255)
    gold_lt = (255, 230, 140, 255)
    gold_dk = (140, 100, 30, 255)
    # chip 1
    shaded_rect(img, 18, 20, 30, 28, gold, gold_lt, gold_dk)
    # chip 2
    shaded_rect(img, 36, 20, 46, 26, gold, gold_lt, gold_dk)
    # connectors (side pads)
    for y in range(32, 46, 4):
        shaded_rect(img, 16, y, 22, y + 2, gold, gold_lt, gold_dk)
        shaded_rect(img, 42, y, 48, y + 2, gold, gold_lt, gold_dk)
    # traces (bright)
    trace = blend(lt, (180, 255, 255, 255), 0.5)
    d.line([(32, 28), (32, 46)], fill=trace, width=1)
    d.line([(22, 30), (42, 30)], fill=trace, width=1)
    d.line([(22, 40), (42, 40)], fill=trace, width=1)
    # sparkle center
    px(img, 32, 34, (255, 255, 255, 255))
    save(img, name)


def draw_cell(palette, name):
    """Plasma cell — cylindrical container with glow."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # frame
    steel = (90, 90, 100, 255)
    steel_lt = (160, 160, 170, 255)
    steel_dk = (40, 40, 50, 255)
    # top cap
    shaded_rect(img, 22, 12, 42, 18, steel, steel_lt, steel_dk)
    # bottom cap
    shaded_rect(img, 22, 46, 42, 52, steel, steel_lt, steel_dk)
    # body (cylindrical)
    for y in range(18, 46):
        for x in range(22, 43):
            # vertical stripe gradient
            t = abs(x - 32) / 10
            c = blend(base, dk, t * 0.6)
            if t < 0.3:
                c = blend(c, lt, 0.3)
            px(img, x, y, c)
    # glass shine (vertical line)
    for y in range(18, 46):
        px(img, 26, y, blend(lt, (255, 255, 255, 255), 0.4))
    # plasma glow (inner)
    for y in range(20, 44):
        for x in range(28, 37):
            t = abs(x - 32) / 6 + abs(y - 32) / 15
            c = blend(lt, base, min(1, t))
            px(img, x, y, c)
    # sparkles
    for (x, y) in [(30, 22), (34, 28), (31, 36), (33, 42)]:
        px(img, x, y, (255, 255, 255, 255))
    save(img, name)


def draw_casing(palette, name):
    """Reinforced casing — industrial box."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # frame border
    shaded_rect(img, 8, 8, 56, 56, dk, blend(dk, lt, 0.3), blend(dk, (0, 0, 0, 255), 0.5))
    # inner
    shaded_rect(img, 11, 11, 53, 53, base, lt, dk)
    # inner inner panel
    shaded_rect(img, 18, 18, 46, 46, blend(base, dk, 0.4), lt, dk)
    # corner bolts
    for (x, y) in [(12, 12), (52, 12), (12, 52), (52, 52)]:
        radial_shade(img, x, y, 2, blend(base, (60, 60, 70, 255), 0.4), lt, dk)
    # center X brace
    d.line([(18, 18), (46, 46)], fill=lt, width=1)
    d.line([(46, 18), (18, 46)], fill=lt, width=1)
    save(img, name)


def draw_sphere(palette, name, symbol=None, glow_inner=True):
    """Reactor/matrix sphere."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    r = 24
    radial_shade(img, CX, CY, r, base, lt, dk, outline=blend(base, (0, 0, 0, 255), 0.6))
    # inner dark core
    radial_shade(img, CX, CY, 10, blend(base, dk, 0.7), base, blend(base, (0, 0, 0, 255), 0.6))
    # core glow
    if glow_inner:
        radial_shade(img, CX, CY, 5, blend(lt, (255, 255, 255, 255), 0.6), (255, 255, 255, 255), blend(lt, dk, 0.3))
    # equator ring
    for x in range(CX - r, CX + r + 1):
        dx = x - CX
        if abs(dx) <= r:
            dy = int(math.sqrt(r * r - dx * dx) - 2)
            if dy >= 0:
                px(img, x, CY + dy - 1, lt)
                px(img, x, CY - dy + 1, dk)
    # highlight
    for x in range(CX - 10, CX - 2):
        px(img, x, CY - 14, blend(lt, (255, 255, 255, 255), 0.5))
    if symbol == 'star':
        # nether star glimmer
        for (x, y) in [(CX, CY - 8), (CX - 8, CY), (CX + 8, CY), (CX, CY + 8)]:
            px(img, x, y, (255, 255, 255, 255))
    save(img, name)


def draw_reflector(palette, name):
    """Neutron reflector — mirrored dish."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette
    # dish outer
    d.pieslice([6, 10, 58, 54], 0, 180, fill=base, outline=blend(base, (0, 0, 0, 255), 0.5))
    # rim
    d.arc([6, 10, 58, 54], 0, 180, fill=dk, width=2)
    # inner reflective surface (gradient)
    for y in range(32, 48):
        for x in range(12, 53):
            # radial from (32, 32)
            dx = x - 32
            dy = y - 32
            dd = math.sqrt(dx * dx + dy * dy)
            if dd < 20:
                t = dd / 20
                c = blend(lt, base, t * 0.6)
                px(img, x, y, c)
    # base (rectangle under dish)
    shaded_rect(img, 22, 48, 42, 56, dk, base, blend(dk, (0, 0, 0, 255), 0.5))
    # sparkles on surface
    for (x, y) in [(24, 38), (32, 36), (40, 38), (32, 42)]:
        px(img, x, y, (255, 255, 255, 255))
    save(img, name)


def draw_fusion_core():
    """The ultimate core."""
    img = new_img()
    d = ImageDraw.Draw(img)
    # outer metallic ring
    steel = (100, 100, 120, 255)
    steel_lt = (200, 200, 220, 255)
    steel_dk = (40, 40, 60, 255)
    radial_shade(img, CX, CY, 28, steel, steel_lt, steel_dk, blend(steel, (0, 0, 0, 255), 0.7))
    # inner dark void
    radial_shade(img, CX, CY, 22, (10, 5, 25, 255), (30, 15, 60, 255), (0, 0, 0, 255))
    # plasma swirl (orange-red)
    plasma = (255, 130, 40, 255)
    plasma_lt = (255, 230, 150, 255)
    plasma_white = (255, 255, 255, 255)
    radial_shade(img, CX, CY, 14, plasma, plasma_lt, blend(plasma, (60, 0, 0, 255), 0.6))
    radial_shade(img, CX, CY, 8, plasma_lt, plasma_white, plasma)
    radial_shade(img, CX, CY, 3, plasma_white, plasma_white, plasma_lt)
    # outer spokes
    for ang in [0, 60, 120, 180, 240, 300]:
        a = math.radians(ang)
        for r in range(22, 28):
            x = int(CX + math.cos(a) * r)
            y = int(CY + math.sin(a) * r)
            px(img, x, y, steel_lt)
    # corner sparkles
    for (x, y) in [(10, 10), (54, 10), (10, 54), (54, 54)]:
        px(img, x, y, plasma_white)
    save(img, "fusion_core")


def draw_heart_of_arcadia():
    img = new_img()
    d = ImageDraw.Draw(img)
    # heart shape with golden glow
    gold = (220, 180, 60, 255)
    gold_lt = (255, 240, 140, 255)
    gold_dk = (130, 90, 15, 255)
    red = (220, 40, 40, 255)
    red_lt = (255, 120, 80, 255)
    # heart pixels (20x18)
    rows = [
        ".XX...XX.",
        "XXXXXXXXX",
        "XXXXXXXXX",
        "XXXXXXXXX",
        ".XXXXXXX.",
        "..XXXXX..",
        "...XXX...",
        "....X....",
    ]
    ox, oy = 18, 18
    scale = 3
    # scale heart up
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == 'X':
                for sy in range(scale):
                    for sx in range(scale):
                        x = ox + i * scale + sx
                        y = oy + j * scale + sy
                        if 0 <= x < SIZE and 0 <= y < SIZE:
                            px(img, x, y, gold)
    # highlight
    for j, row in enumerate(rows[:3]):
        for i, ch in enumerate(row):
            if ch == 'X':
                x = ox + i * scale
                y = oy + j * scale
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    px(img, x, y, gold_lt)
                    px(img, x + 1, y, gold_lt)
    # inner glow (pulsing red center)
    radial_shade(img, CX, CY + 2, 5, red, red_lt, blend(red, (0, 0, 0, 255), 0.4))
    # outer aura sparkles
    for (x, y) in [(10, 14), (54, 14), (14, 50), (50, 50)]:
        px(img, x, y, gold_lt)
    save(img, "heart_of_arcadia")


# ============================================================
# ADEPT / HERETIC PALETTES
# ============================================================

ADEPT = {
    'base': (140, 90, 180, 255),      # purple
    'lt': (210, 160, 240, 255),
    'dk': (70, 40, 100, 255),
    'accent': (255, 240, 140, 255),   # gold accent
    'outline': (30, 15, 50, 255),
    'cloth': (80, 50, 120, 255),
    'cloth_lt': (130, 90, 170, 255),
    'cloth_dk': (45, 25, 70, 255),
}

HERETIC = {
    'base': (170, 30, 40, 255),       # blood red
    'lt': (220, 70, 70, 255),
    'dk': (80, 15, 20, 255),
    'accent': (30, 30, 30, 255),      # dark obsidian
    'outline': (40, 5, 10, 255),
    'cloth': (60, 15, 20, 255),
    'cloth_lt': (110, 40, 50, 255),
    'cloth_dk': (30, 8, 12, 255),
}

# ============================================================
# ARMOR ICONS (flat representations)
# ============================================================

def draw_armor_helmet(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['cloth']
    lt = palette['cloth_lt']
    dk = palette['cloth_dk']
    accent = palette['accent']
    ol = palette['outline']
    # hood shape
    pts = [(18, 20), (22, 14), (42, 14), (46, 20), (48, 28), (48, 42),
           (44, 48), (20, 48), (16, 42), (16, 28)]
    d.polygon(pts, fill=base, outline=ol)
    # top hood point
    d.polygon([(30, 14), (32, 8), (34, 14)], fill=dk)
    # face opening (dark inside)
    d.ellipse([22, 26, 42, 46], fill=(10, 10, 15, 255))
    # accent trim around face
    d.arc([21, 25, 43, 47], 0, 360, fill=accent, width=1)
    # eye glow
    px(img, 28, 34, palette['lt'])
    px(img, 36, 34, palette['lt'])
    # hood highlights
    d.line([(20, 20), (30, 14)], fill=lt, width=1)
    save(img, name)


def draw_armor_chestplate(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['cloth']
    lt = palette['cloth_lt']
    dk = palette['cloth_dk']
    accent = palette['accent']
    ol = palette['outline']
    # robe shape
    pts = [(18, 12), (46, 12), (50, 20), (52, 52), (42, 56), (22, 56), (12, 52), (14, 20)]
    d.polygon(pts, fill=base, outline=ol)
    # shoulder pads
    d.rectangle([14, 14, 22, 22], fill=dk)
    d.rectangle([42, 14, 50, 22], fill=dk)
    d.rectangle([14, 14, 22, 14], fill=lt)
    d.rectangle([42, 14, 50, 14], fill=lt)
    # front split
    d.rectangle([31, 20, 33, 54], fill=dk)
    # belt
    d.rectangle([18, 38, 46, 42], fill=dk)
    d.rectangle([18, 38, 46, 38], fill=accent)
    # central emblem
    d.ellipse([28, 26, 36, 34], fill=accent)
    d.ellipse([30, 28, 34, 32], fill=ol)
    # cloth folds (light)
    d.line([(20, 20), (20, 52)], fill=lt, width=1)
    d.line([(44, 20), (44, 52)], fill=lt, width=1)
    save(img, name)


def draw_armor_leggings(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['cloth']
    lt = palette['cloth_lt']
    dk = palette['cloth_dk']
    accent = palette['accent']
    ol = palette['outline']
    # two legs
    # left leg
    pts_left = [(18, 8), (30, 8), (30, 56), (24, 58), (18, 56)]
    pts_right = [(34, 8), (46, 8), (46, 56), (40, 58), (34, 56)]
    d.polygon(pts_left, fill=base, outline=ol)
    d.polygon(pts_right, fill=base, outline=ol)
    # knee highlights
    d.line([(19, 8), (19, 56)], fill=lt, width=1)
    d.line([(35, 8), (35, 56)], fill=lt, width=1)
    # knee accent bands
    for y in [30, 32]:
        d.rectangle([18, y, 30, y], fill=accent)
        d.rectangle([34, y, 46, y], fill=accent)
    save(img, name)


def draw_armor_boots(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['cloth']
    lt = palette['cloth_lt']
    dk = palette['cloth_dk']
    accent = palette['accent']
    ol = palette['outline']
    # two boots
    for bx in [16, 36]:
        # upper ankle
        d.rectangle([bx, 20, bx + 12, 44], fill=base, outline=ol)
        # foot (extends right)
        d.polygon([(bx, 44), (bx + 16, 44), (bx + 16, 52), (bx, 52)], fill=base, outline=ol)
        # sole
        d.rectangle([bx, 52, bx + 16, 54], fill=dk)
        # strap
        d.rectangle([bx, 34, bx + 12, 36], fill=accent)
        # highlight
        d.line([(bx + 1, 20), (bx + 1, 52)], fill=lt, width=1)
    save(img, name)


# ============================================================
# ADEPT UNIQUE ITEMS
# ============================================================

def draw_book(palette, name, emblem='pentagram'):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['base']
    lt = palette['lt']
    dk = palette['dk']
    accent = palette['accent']
    ol = palette['outline']
    # book body
    shaded_rect(img, 10, 10, 54, 54, base, lt, dk)
    # spine
    shaded_rect(img, 10, 10, 16, 54, dk, base, blend(dk, (0, 0, 0, 255), 0.4))
    # pages (white edge on right)
    shaded_rect(img, 50, 12, 54, 52, (230, 220, 200, 255), (255, 250, 230, 255), (160, 150, 120, 255))
    # cover outline
    d.rectangle([10, 10, 54, 54], outline=ol, width=1)
    # emblem in center
    if emblem == 'pentagram':
        cx, cy = 32, 32
        r = 10
        # pentagram (5-point star)
        pts = []
        for i in range(5):
            a = math.radians(-90 + i * 72)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        # connect each point to two others skipping one (star)
        for i in range(5):
            j = (i + 2) % 5
            d.line([pts[i], pts[j]], fill=accent, width=1)
    elif emblem == 'eye':
        d.ellipse([22, 26, 42, 38], outline=accent, width=1)
        d.ellipse([29, 28, 35, 34], fill=accent)
        d.ellipse([30, 29, 33, 32], fill=ol)
        # tear
        px(img, 32, 40, palette['lt'])
    elif emblem == 'skull':
        d.ellipse([22, 22, 42, 42], fill=(240, 230, 210, 255), outline=ol)
        d.ellipse([26, 28, 30, 32], fill=ol)
        d.ellipse([34, 28, 38, 32], fill=ol)
        d.rectangle([28, 36, 30, 38], fill=ol)
        d.rectangle([32, 36, 36, 38], fill=ol)
    # sparkle
    px(img, 14, 14, lt)
    save(img, name)


def draw_pendant(palette, name, gem_col=None):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['base']
    lt = palette['lt']
    dk = palette['dk']
    accent = palette['accent']
    ol = palette['outline']
    gem = gem_col or palette['base']
    gem_lt = blend(gem, (255, 255, 255, 255), 0.5)
    # chain (arc)
    for ang in range(170, 370, 8):
        a = math.radians(ang)
        x = int(32 + math.cos(a) * 22)
        y = int(24 + math.sin(a) * 14)
        if 0 <= x < SIZE and 0 <= y < SIZE:
            px(img, x, y, accent)
            px(img, x, y - 1, blend(accent, (255, 255, 255, 255), 0.4))
    # pendant body (lower)
    radial_shade(img, 32, 42, 12, accent, blend(accent, (255, 255, 255, 255), 0.5), blend(accent, (0, 0, 0, 255), 0.5), ol)
    # inset gem
    radial_shade(img, 32, 42, 6, gem, gem_lt, blend(gem, (0, 0, 0, 255), 0.5))
    px(img, 30, 40, (255, 255, 255, 255))
    save(img, name)


def draw_candle(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    # candle body
    wax = (240, 230, 200, 255)
    wax_lt = (255, 250, 235, 255)
    wax_dk = (180, 160, 120, 255)
    # body
    shaded_rect(img, 26, 24, 38, 54, palette['cloth'], palette['cloth_lt'], palette['cloth_dk'])
    # base plate
    shaded_rect(img, 22, 52, 42, 56, palette['accent'], blend(palette['accent'], (255, 255, 255, 255), 0.5), palette['outline'])
    # wick
    d.rectangle([31, 18, 33, 24], fill=(60, 40, 20, 255))
    # flame (colored by theme)
    flame = palette['lt']
    flame_lt = blend(flame, (255, 255, 180, 255), 0.5)
    pts = [(32, 6), (36, 12), (36, 18), (32, 22), (28, 18), (28, 12)]
    d.polygon(pts, fill=flame, outline=blend(flame, (0, 0, 0, 255), 0.3))
    d.polygon([(32, 10), (34, 14), (32, 18), (30, 14)], fill=flame_lt)
    # wax drip
    px(img, 28, 40, palette['cloth_lt'])
    px(img, 38, 46, palette['cloth_lt'])
    save(img, name)


def draw_incense(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['accent']
    lt = blend(base, (255, 255, 255, 255), 0.5)
    dk = blend(base, (0, 0, 0, 255), 0.5)
    # holder
    shaded_rect(img, 14, 46, 50, 54, base, lt, dk)
    # sticks
    for x in [22, 32, 42]:
        d.rectangle([x, 20, x + 1, 48], fill=(80, 50, 20, 255))
        # embers
        px(img, x, 18, palette['lt'])
        px(img, x + 1, 19, (255, 240, 180, 255))
    # smoke wisps
    for (x, y) in [(22, 14), (32, 10), (42, 14), (26, 6), (38, 6)]:
        px(img, x, y, palette['lt'])
        px(img, x + 1, y - 1, palette['base'])
    save(img, name)


def draw_staff(palette, name, gem_shape='sphere'):
    img = new_img()
    d = ImageDraw.Draw(img)
    wood = (80, 50, 30, 255)
    wood_lt = (140, 100, 60, 255)
    wood_dk = (40, 25, 15, 255)
    # shaft
    d.line([(18, 50), (46, 14)], fill=wood, width=3)
    d.line([(18, 50), (46, 14)], fill=wood_lt, width=1)
    # gem holder at top
    d.polygon([(46, 14), (52, 14), (52, 20), (46, 20)], fill=palette['accent'], outline=palette['outline'])
    # gem
    if gem_shape == 'sphere':
        radial_shade(img, 46, 12, 6, palette['base'], palette['lt'], palette['dk'])
    elif gem_shape == 'crystal':
        pts = [(46, 6), (52, 12), (46, 18), (40, 12)]
        d.polygon(pts, fill=palette['base'], outline=palette['outline'])
        d.line([(46, 6), (46, 18)], fill=palette['lt'], width=1)
    # grip wrap
    d.rectangle([22, 36, 28, 46], fill=palette['cloth_dk'])
    for y in [37, 40, 43]:
        d.line([(22, y), (28, y)], fill=palette['accent'], width=1)
    save(img, name)


def draw_seal(palette, name):
    """Wax seal."""
    img = new_img()
    d = ImageDraw.Draw(img)
    radial_shade(img, CX, CY, 22, palette['base'], palette['lt'], palette['dk'], palette['outline'])
    # embossed sigil
    d.line([(22, 32), (42, 32)], fill=palette['dk'], width=1)
    d.line([(32, 22), (32, 42)], fill=palette['dk'], width=1)
    for i in range(4):
        a = math.radians(45 + i * 90)
        x1 = int(CX + math.cos(a) * 8)
        y1 = int(CY + math.sin(a) * 8)
        x2 = int(CX + math.cos(a) * 14)
        y2 = int(CY + math.sin(a) * 14)
        d.line([(x1, y1), (x2, y2)], fill=palette['dk'], width=1)
    # center gem
    d.ellipse([30, 30, 34, 34], fill=palette['accent'])
    save(img, name)


def draw_chalice(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['accent']
    lt = blend(base, (255, 255, 255, 255), 0.5)
    dk = blend(base, (0, 0, 0, 255), 0.5)
    # stem
    shaded_rect(img, 30, 30, 34, 48, base, lt, dk)
    # base (foot)
    shaded_rect(img, 22, 48, 42, 54, base, lt, dk)
    # cup (wider)
    d.polygon([(18, 12), (46, 12), (42, 30), (22, 30)], fill=base, outline=palette['outline'])
    # liquid inside
    d.polygon([(22, 14), (42, 14), (40, 18), (24, 18)], fill=palette['base'])
    # liquid shine
    px(img, 26, 15, lt)
    px(img, 36, 16, lt)
    # cup edges
    d.line([(18, 12), (22, 30)], fill=lt, width=1)
    d.line([(46, 12), (42, 30)], fill=dk, width=1)
    save(img, name)


def draw_orb(palette, name):
    img = new_img()
    # floating orb with glow halo
    # halo
    for r in range(28, 14, -1):
        alpha = int(255 * (1 - (r - 14) / 14) * 0.3)
        for y in range(CY - r, CY + r + 1):
            for x in range(CX - r, CX + r + 1):
                dx = x - CX
                dy = y - CY
                d = math.sqrt(dx * dx + dy * dy)
                if r - 1 <= d < r:
                    existing = list(img.getpixel((x, y)))
                    new_c = (*palette['lt'][:3], alpha)
                    if existing[3] < new_c[3]:
                        px(img, x, y, new_c)
    # solid orb
    radial_shade(img, CX, CY, 14, palette['base'], palette['lt'], palette['dk'], palette['outline'])
    # inner bright core
    radial_shade(img, CX, CY, 5, palette['lt'], (255, 255, 255, 255), palette['base'])
    # sparkles around
    for (x, y) in [(12, 12), (52, 14), (10, 50), (54, 50), (32, 6), (32, 58)]:
        px(img, x, y, palette['lt'])
    save(img, name)


def draw_scroll(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    paper = (235, 215, 165, 255)
    paper_lt = (255, 245, 200, 255)
    paper_dk = (170, 140, 90, 255)
    accent = palette['accent']
    # scroll body
    shaded_rect(img, 12, 20, 52, 44, paper, paper_lt, paper_dk)
    # rolled ends
    shaded_rect(img, 10, 18, 16, 46, paper_dk, paper, (80, 60, 30, 255))
    shaded_rect(img, 48, 18, 54, 46, paper_dk, paper, (80, 60, 30, 255))
    # text lines
    for y in [26, 30, 34, 38]:
        d.line([(18, y), (46, y)], fill=(120, 80, 40, 255), width=1)
    # red ribbon
    d.rectangle([28, 16, 36, 48], fill=accent)
    d.rectangle([28, 16, 36, 17], fill=blend(accent, (255, 255, 255, 255), 0.5))
    # wax seal
    radial_shade(img, 32, 32, 4, palette['base'], palette['lt'], palette['dk'])
    save(img, name)


def draw_relic(palette, name):
    """Mysterious relic — ornate artifact."""
    img = new_img()
    d = ImageDraw.Draw(img)
    # ornate frame
    base = palette['accent']
    lt = blend(base, (255, 255, 255, 255), 0.5)
    dk = blend(base, (0, 0, 0, 255), 0.5)
    ol = palette['outline']
    # outer diamond frame
    pts = [(32, 6), (58, 32), (32, 58), (6, 32)]
    d.polygon(pts, fill=base, outline=ol)
    # inner dark
    pts_inner = [(32, 16), (48, 32), (32, 48), (16, 32)]
    d.polygon(pts_inner, fill=dk)
    # center gem
    radial_shade(img, CX, CY, 8, palette['base'], palette['lt'], palette['dk'])
    radial_shade(img, CX, CY, 3, palette['lt'], (255, 255, 255, 255), palette['base'])
    # edge highlights
    d.line([(32, 6), (58, 32)], fill=lt, width=1)
    d.line([(32, 6), (6, 32)], fill=lt, width=1)
    d.line([(58, 32), (32, 58)], fill=dk, width=1)
    d.line([(6, 32), (32, 58)], fill=dk, width=1)
    # corner sparkles
    for (x, y) in [(32, 4), (60, 32), (32, 60), (4, 32)]:
        px(img, x, y, (255, 255, 255, 255))
    save(img, name)


def draw_vial(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    glass = (200, 230, 230, 255)
    glass_lt = (255, 255, 255, 255)
    # cork
    shaded_rect(img, 28, 10, 36, 16, (140, 80, 40, 255), (200, 140, 80, 255), (70, 40, 15, 255))
    # neck
    shaded_rect(img, 30, 16, 34, 22, glass, glass_lt, (120, 160, 160, 255))
    # body (bulb)
    radial_shade(img, CX, 38, 14, glass, glass_lt, (120, 160, 160, 255), palette['outline'])
    # liquid inside
    radial_shade(img, CX, 40, 10, palette['base'], palette['lt'], palette['dk'])
    # shine
    px(img, 26, 30, glass_lt)
    px(img, 27, 31, glass_lt)
    save(img, name)


def draw_dagger(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    steel = (180, 180, 200, 255)
    steel_lt = (240, 240, 255, 255)
    steel_dk = (90, 90, 110, 255)
    # blade (diagonal)
    pts = [(20, 52), (14, 46), (40, 14), (48, 22), (46, 26)]
    d.polygon(pts, fill=steel, outline=steel_dk)
    # blade edge highlight
    d.line([(16, 48), (42, 16)], fill=steel_lt, width=1)
    d.line([(18, 50), (44, 20)], fill=steel_dk, width=1)
    # crossguard
    pts2 = [(12, 54), (8, 50), (20, 38), (24, 42)]
    d.polygon(pts2, fill=palette['accent'], outline=palette['outline'])
    # handle grip
    pts3 = [(16, 58), (10, 52), (14, 48), (20, 54)]
    d.polygon(pts3, fill=palette['cloth_dk'], outline=palette['outline'])
    # pommel (gem)
    radial_shade(img, 14, 58, 3, palette['base'], palette['lt'], palette['dk'])
    # blood drips
    px(img, 44, 16, palette['base'])
    px(img, 46, 20, palette['lt'])
    save(img, name)


def draw_chain(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    base = palette['accent']
    lt = blend(base, (255, 255, 255, 255), 0.5)
    dk = blend(base, (0, 0, 0, 255), 0.5)
    # 5 chain links diagonal
    for i, (cx, cy) in enumerate([(16, 52), (26, 42), (36, 32), (46, 22), (56, 12)]):
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=base, width=2)
        # highlight
        d.arc([cx - 5, cy - 5, cx + 5, cy + 5], 135, 225, fill=lt, width=1)
    # pendant gem at bottom link
    radial_shade(img, 16, 60, 3, palette['base'], palette['lt'], palette['dk'])
    save(img, name)


def draw_skull_totem(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    bone = (230, 220, 180, 255)
    bone_lt = (255, 250, 220, 255)
    bone_dk = (150, 140, 100, 255)
    # stick
    d.rectangle([30, 40, 34, 62], fill=(80, 50, 20, 255))
    d.rectangle([30, 40, 30, 62], fill=(130, 90, 40, 255))
    # wraps
    for y in [46, 52, 58]:
        d.rectangle([28, y, 36, y + 1], fill=palette['accent'])
    # skull
    d.ellipse([16, 8, 48, 40], fill=bone, outline=bone_dk)
    # shading
    d.arc([16, 8, 48, 40], 180, 360, fill=bone_lt, width=1)
    d.arc([16, 8, 48, 40], 0, 180, fill=bone_dk, width=1)
    # eye sockets (glowing)
    radial_shade(img, 24, 22, 3, palette['base'], palette['lt'], palette['dk'])
    radial_shade(img, 40, 22, 3, palette['base'], palette['lt'], palette['dk'])
    # nose
    d.polygon([(32, 26), (30, 30), (34, 30)], fill=bone_dk)
    # teeth
    for x in [20, 24, 28, 32, 36, 40]:
        d.rectangle([x, 32, x + 2, 36], fill=bone_lt)
        d.rectangle([x + 2, 32, x + 2, 36], fill=bone_dk)
    save(img, name)


def draw_icon(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    # framed icon (like a religious painting)
    frame_col = (140, 100, 40, 255)
    frame_lt = (210, 170, 90, 255)
    frame_dk = (80, 55, 20, 255)
    # outer frame
    shaded_rect(img, 8, 8, 56, 56, frame_col, frame_lt, frame_dk)
    shaded_rect(img, 12, 12, 52, 52, palette['cloth_dk'], palette['cloth'], palette['outline'])
    # figure silhouette (bust)
    d.ellipse([24, 18, 40, 34], fill=palette['base'], outline=palette['outline'])  # head
    d.polygon([(18, 44), (26, 32), (38, 32), (46, 44), (46, 50), (18, 50)], fill=palette['base'], outline=palette['outline'])  # body
    # halo
    d.arc([20, 14, 44, 38], 180, 360, fill=palette['accent'], width=1)
    # eye glow
    px(img, 30, 26, palette['lt'])
    px(img, 34, 26, palette['lt'])
    save(img, name)


def draw_bone_charm(palette, name):
    img = new_img()
    d = ImageDraw.Draw(img)
    bone = (240, 230, 200, 255)
    bone_lt = (255, 250, 230, 255)
    bone_dk = (160, 145, 110, 255)
    # cross bone
    # horizontal bone
    d.ellipse([8, 26, 24, 38], fill=bone, outline=bone_dk)
    d.rectangle([20, 28, 44, 36], fill=bone, outline=bone_dk)
    d.ellipse([40, 26, 56, 38], fill=bone, outline=bone_dk)
    # highlights
    d.arc([8, 26, 24, 38], 180, 360, fill=bone_lt, width=1)
    d.arc([40, 26, 56, 38], 180, 360, fill=bone_lt, width=1)
    # cord
    for ang in range(0, 180, 15):
        a = math.radians(ang)
        x = int(32 + math.cos(a) * 18)
        y = int(22 - math.sin(a) * 6)
        px(img, x, y, palette['outline'])
    # rune engraving
    d.line([(28, 30), (32, 34)], fill=palette['base'], width=1)
    d.line([(32, 30), (32, 34)], fill=palette['base'], width=1)
    save(img, name)


def draw_flask(palette, name):
    """Poison flask."""
    img = new_img()
    d = ImageDraw.Draw(img)
    glass = (140, 180, 140, 255)  # greenish glass for poison
    glass_lt = (200, 240, 200, 255)
    # cork
    shaded_rect(img, 28, 12, 36, 18, (100, 60, 30, 255), (160, 110, 60, 255), (50, 30, 10, 255))
    # skull warning
    d.rectangle([30, 10, 34, 12], fill=(230, 230, 230, 255))
    # neck
    shaded_rect(img, 30, 18, 34, 24, glass, glass_lt, (80, 120, 80, 255))
    # bulb
    radial_shade(img, CX, 40, 16, glass, glass_lt, (80, 120, 80, 255), palette['outline'])
    # liquid (color)
    radial_shade(img, CX, 42, 11, palette['base'], palette['lt'], palette['dk'])
    # bubbles
    for (x, y) in [(26, 36), (36, 40), (30, 44)]:
        px(img, x, y, palette['lt'])
    # shine
    px(img, 24, 34, glass_lt)
    save(img, name)


def draw_mark(palette, name):
    """Heretic's mark — branded sigil."""
    img = new_img()
    d = ImageDraw.Draw(img)
    # leather patch
    leather = (110, 70, 40, 255)
    leather_lt = (160, 110, 70, 255)
    leather_dk = (60, 35, 15, 255)
    pts = [(14, 14), (50, 14), (54, 18), (54, 50), (50, 54), (14, 54), (10, 50), (10, 18)]
    d.polygon(pts, fill=leather, outline=leather_dk)
    # stitches around edge
    for x in range(12, 54, 4):
        px(img, x, 12, leather_lt)
        px(img, x, 55, leather_lt)
    for y in range(16, 54, 4):
        px(img, 11, y, leather_lt)
        px(img, 54, y, leather_lt)
    # branded sigil (pentagram inverted)
    cx, cy = 32, 34
    r = 12
    pts = []
    for i in range(5):
        a = math.radians(90 + i * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(5):
        j = (i + 2) % 5
        d.line([pts[i], pts[j]], fill=palette['base'], width=1)
    # glow center
    radial_shade(img, cx, cy, 3, palette['lt'], (255, 255, 255, 255), palette['base'])
    save(img, name)


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    # ==== KEYS ====
    draw_key((120, 120, 130, 255), (180, 180, 190, 255), name='basic_key')
    draw_key((110, 180, 100, 255), (255, 255, 255, 255), name='common_key')
    draw_key((80, 140, 220, 255), (200, 230, 255, 255), name='rare_key')
    draw_key((180, 80, 220, 255), (240, 180, 255, 255), glow=(255, 255, 255, 255), name='legendary_key')
    draw_key((240, 180, 40, 255), (255, 255, 200, 255), glow=(255, 240, 180, 255), name='arcadia_key')
    draw_key((230, 80, 100, 255), (255, 200, 220, 255), name='vote_key')
    draw_token()

    # ==== FUSION CHAIN ====
    # Tier 0 - base materials
    draw_ingot(((120, 120, 140, 255), (200, 200, 220, 255), (60, 60, 80, 255)), 'alloy_blend')
    draw_crystal(((90, 200, 255, 255), (200, 240, 255, 255), (30, 80, 150, 255)), 'diamond_matrix', glow=True)
    draw_ingot(((180, 140, 100, 255), (250, 210, 150, 255), (100, 70, 40, 255)), 'infused_steel', overlay='runes')
    draw_dust(((180, 60, 60, 255), (255, 130, 100, 255), (100, 20, 20, 255)), 'nether_concentrate')
    draw_dust(((255, 180, 40, 255), (255, 240, 150, 255), (140, 90, 10, 255)), 'energized_dust')
    draw_plate(((150, 100, 60, 255), (220, 170, 110, 255), (80, 50, 25, 255)), 'wiring_bundle', riveted=False)

    # Tier 1 - refined
    draw_ingot(((200, 200, 220, 255), (255, 255, 255, 255), (100, 100, 130, 255)), 'refined_alloy_ingot', glow=True)
    draw_ingot(((70, 70, 90, 255), (140, 140, 170, 255), (20, 20, 40, 255)), 'hardened_steel_compound', overlay='runes')
    draw_crystal(((255, 200, 60, 255), (255, 250, 180, 255), (130, 90, 10, 255)), 'energized_crystal', tall=True, glow=True)
    draw_plate(((100, 180, 220, 255), (170, 230, 255, 255), (40, 90, 130, 255)), 'treated_composite_plate', riveted=True)

    # Tier 2 - advanced
    draw_circuit_card(((40, 80, 140, 255), (100, 160, 220, 255), (15, 35, 70, 255)), 'quantum_circuit')
    draw_cell(((255, 120, 40, 255), (255, 220, 120, 255), (140, 40, 10, 255)), 'plasma_cell')
    draw_casing(((100, 100, 130, 255), (180, 180, 210, 255), (40, 40, 70, 255)), 'reinforced_casing')
    draw_plate(((200, 60, 60, 255), (255, 150, 140, 255), (110, 20, 20, 255)), 'thermal_conductor', riveted=True)

    # Tier 2 transitionals (incomplete)
    # We reuse the Tier 2 shapes but darker/desaturated
    draw_cell(((100, 60, 40, 255), (150, 110, 80, 255), (50, 30, 20, 255)), 'incomplete_plasma_cell')
    draw_casing(((60, 60, 70, 255), (100, 100, 120, 255), (25, 25, 35, 255)), 'incomplete_reinforced_casing')
    draw_sphere(((80, 60, 90, 255), (130, 110, 140, 255), (40, 30, 50, 255)), 'incomplete_neutron_reflector')

    # Tier 3 - elite
    draw_sphere(((180, 100, 255, 255), (240, 180, 255, 255), (90, 30, 140, 255)), 'fusion_matrix', symbol='star')
    draw_sphere(((255, 200, 100, 255), (255, 250, 200, 255), (130, 80, 20, 255)), 'containment_field_generator', glow_inner=True)
    draw_reflector(((140, 200, 220, 255), (220, 250, 255, 255), (60, 100, 140, 255)), 'neutron_reflector')

    # Final
    draw_fusion_core()

    # Heart of Arcadia
    draw_heart_of_arcadia()

    # ==== ADEPT ARMOR ====
    draw_armor_helmet(ADEPT, 'adept_helmet')
    draw_armor_chestplate(ADEPT, 'adept_chestplate')
    draw_armor_leggings(ADEPT, 'adept_leggings')
    draw_armor_boots(ADEPT, 'adept_boots')

    # ==== HERETIC ARMOR ====
    draw_armor_helmet(HERETIC, 'heretic_helmet')
    draw_armor_chestplate(HERETIC, 'heretic_chestplate')
    draw_armor_leggings(HERETIC, 'heretic_leggings')
    draw_armor_boots(HERETIC, 'heretic_boots')

    # ==== ADEPT UNIQUE (10) ====
    draw_book(ADEPT, 'adept_grimoire', emblem='pentagram')
    draw_pendant(ADEPT, 'adept_pendant', gem_col=(180, 100, 220, 255))
    draw_candle(ADEPT, 'adept_candle')
    draw_incense(ADEPT, 'adept_incense')
    draw_staff(ADEPT, 'adept_staff', gem_shape='sphere')
    draw_seal(ADEPT, 'adept_seal')
    draw_chalice(ADEPT, 'adept_chalice')
    draw_orb(ADEPT, 'adept_orb')
    draw_scroll(ADEPT, 'adept_scroll')
    draw_relic(ADEPT, 'adept_relic')

    # ==== HERETIC UNIQUE (10) ====
    draw_book(HERETIC, 'heretic_tome', emblem='skull')
    draw_vial(HERETIC, 'heretic_blood_vial')
    draw_dagger(HERETIC, 'heretic_dagger')
    draw_chain(HERETIC, 'heretic_chain')
    draw_skull_totem(HERETIC, 'heretic_skull_totem')
    draw_icon(HERETIC, 'heretic_icon')
    draw_crystal((HERETIC['base'], HERETIC['lt'], HERETIC['dk']), 'heretic_crystal', tall=True, glow=True)
    draw_bone_charm(HERETIC, 'heretic_bone_charm')
    draw_flask(HERETIC, 'heretic_poison_flask')
    draw_mark(HERETIC, 'heretic_mark')

    print('generated 58 textures at 64x64 with 3D shading')
