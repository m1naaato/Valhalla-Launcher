"""
Generate 64x64 music disc textures — vinyl style with 3D shading.
Each disc has a unique color palette matching its song theme.
Author: vyrriox
"""
from PIL import Image, ImageDraw
import os, math

OUT = os.path.dirname(os.path.abspath(__file__))
SIZE = 64
CX, CY = 32, 32  # center
R_OUTER = 30
R_LABEL = 11
R_HOLE = 2

# Theme-based palettes: (label_color, label_highlight, label_shadow, accent_dot)
DISCS = {
    # Vyrriox's songs
    "mike_le_loulou":            ((70, 130, 45),   (140, 200, 90),  (30, 70, 20),    (230, 220, 120)),  # wolf/forest green
    "vyrriox_trois_femmes":      ((180, 80, 180),  (230, 150, 230), (100, 30, 100),  (255, 200, 220)),  # violet/pink
    "vyrriox_sac_a_gros_pt1":    ((218, 165, 32),  (255, 220, 100), (130, 95, 10),   (255, 255, 200)),  # gold miser
    "vyrriox_sac_a_gros_pt2":    ((200, 145, 25),  (240, 200, 85),  (115, 80, 5),    (255, 240, 180)),  # gold miser (darker)
    "vyrriox_patee":             ((220, 90, 40),   (255, 155, 85),  (130, 40, 15),   (255, 220, 160)),  # feast orange
    "vyrriox_la_naine_pt1":      ((60, 140, 200),  (130, 210, 255), (25, 80, 130),   (200, 240, 255)),  # odyssey cyan
    "vyrriox_la_naine_pt2":      ((50, 120, 185),  (110, 190, 240), (20, 65, 115),   (180, 220, 250)),
    "vyrriox_la_naine_pt3":      ((40, 100, 170),  (95, 170, 225),  (15, 55, 100),   (160, 210, 240)),
    "vyrriox_la_femme_de_joie":  ((235, 130, 175), (255, 200, 220), (155, 70, 110),  (255, 240, 180)),  # star of joy pink
    # Peter's Trumpet (5 parts, brass gradient)
    "peter_le_frein_pt1":        ((205, 160, 55),  (245, 210, 115), (120, 90, 15),   (250, 230, 170)),
    "peter_le_frein_pt2":        ((215, 155, 40),  (250, 205, 100), (125, 85, 5),    (250, 225, 160)),
    "peter_le_frein_pt3":        ((225, 150, 30),  (255, 200, 85),  (130, 80, 0),    (255, 220, 150)),
    "peter_le_frein_pt4":        ((235, 145, 20),  (255, 195, 70),  (135, 75, 0),    (255, 215, 140)),
    "peter_le_frein_pt5":        ((240, 135, 15),  (255, 185, 55),  (140, 70, 0),    (255, 210, 130)),
    # Tavern / drinking
    "boit_ton_picher":           ((180, 100, 40),  (225, 160, 85),  (105, 55, 15),   (255, 220, 140)),  # beer amber
    "dans_la_tavern_lulu":       ((160, 50, 50),   (220, 100, 100), (95, 25, 25),    (250, 200, 150)),  # tavern red/wood
    # Misc
    "janette":                   ((240, 170, 185), (255, 215, 225), (150, 100, 115), (255, 240, 230)),  # soft pink
    "la_boulette_pt1":           ((145, 90, 50),   (195, 140, 95),  (85, 50, 25),    (230, 180, 130)),  # meatball brown
    "la_boulette_pt2":           ((135, 80, 40),   (185, 130, 85),  (75, 45, 20),    (220, 170, 120)),
    "au_pactole":                ((255, 215, 60),  (255, 245, 150), (150, 115, 10),  (255, 255, 240)),  # jackpot gold glitter
}

def rgba(c):
    return c if len(c) == 4 else (c[0], c[1], c[2], 255)

def blend(a, b, t):
    return tuple(int(a[i]*(1-t) + b[i]*t) for i in range(min(len(a), len(b))))

def in_circle(x, y, cx, cy, r):
    return (x-cx)**2 + (y-cy)**2 <= r*r

def make_disc(label_c, label_hi, label_sh, accent, name):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()

    # Vinyl body colors (near black with subtle blue tint)
    vinyl_dark = (8, 8, 14, 255)
    vinyl_mid = (24, 22, 32, 255)
    vinyl_lt = (68, 62, 78, 255)
    vinyl_edge = (3, 3, 6, 255)

    # Draw the disc base with radial shading
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CX
            dy = y - CY
            d2 = dx*dx + dy*dy
            r = math.sqrt(d2)
            if r <= R_OUTER:
                # base vinyl
                # shading: top-left bright, bottom-right dark (pseudo 3D)
                # also faint concentric rings at certain radii
                ring = int(r) % 3  # groove pattern every ~3px
                base = vinyl_mid

                # light direction dot product (unit vector from upper-left)
                # normalize (dx,dy), shade based on (-0.7, -0.7) dot
                if r > 0.1:
                    nx = dx / r
                    ny = dy / r
                    ldot = (-0.7)*nx + (-0.7)*ny  # range [-1, 1]
                    if ldot > 0.4:
                        base = vinyl_lt
                    elif ldot > 0.0:
                        base = blend(vinyl_mid, vinyl_lt, ldot*1.5)
                    elif ldot > -0.4:
                        base = blend(vinyl_mid, vinyl_dark, -ldot*1.5)
                    else:
                        base = vinyl_dark

                # groove darker lines
                if ring == 0 and r > R_LABEL + 1 and r < R_OUTER - 1:
                    base = blend(base, vinyl_edge, 0.45)

                px[x, y] = base

    # Outer rim highlight (thin light ring at r ~ 29.5, upper-left side)
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CX
            dy = y - CY
            d2 = dx*dx + dy*dy
            r = math.sqrt(d2)
            if R_OUTER - 1 <= r <= R_OUTER:
                # outline dark
                px[x, y] = vinyl_edge
            elif R_OUTER - 2 <= r < R_OUTER - 1:
                # inner ring light on top-left
                if dx + dy < -8:
                    px[x, y] = (120, 115, 135, 255)

    # Draw label (colored center) with shading
    label_r = R_LABEL
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CX
            dy = y - CY
            d2 = dx*dx + dy*dy
            r = math.sqrt(d2)
            if r <= label_r:
                base = label_c
                if r > 0.1:
                    nx = dx / r
                    ny = dy / r
                    ldot = (-0.7)*nx + (-0.7)*ny
                    if ldot > 0.3:
                        base = blend(label_c, label_hi, ldot)
                    elif ldot < -0.3:
                        base = blend(label_c, label_sh, -ldot)
                px[x, y] = rgba(base)
            elif label_r < r <= label_r + 1:
                # label ring outline
                px[x, y] = rgba(label_sh)

    # Accent sparkles on label (small decorative dots, 4 symmetrically placed)
    for ang_deg in (45, 135, 225, 315):
        a = math.radians(ang_deg)
        sx = int(CX + math.cos(a) * 6.5)
        sy = int(CY + math.sin(a) * 6.5)
        if 0 <= sx < SIZE and 0 <= sy < SIZE:
            px[sx, sy] = rgba(accent)

    # Center hole (punched through)
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CX
            dy = y - CY
            r2 = dx*dx + dy*dy
            if r2 <= R_HOLE * R_HOLE:
                px[x, y] = (0, 0, 0, 255)
            elif R_HOLE * R_HOLE < r2 <= (R_HOLE + 1) * (R_HOLE + 1):
                # hole rim highlight
                px[x, y] = rgba(label_hi)

    # Subtle brand tick marks on label (2 small dashes at top and bottom)
    px[CX, CY - label_r + 2] = rgba(label_hi)
    px[CX + 1, CY - label_r + 2] = rgba(label_hi)
    px[CX, CY + label_r - 2] = rgba(label_sh)
    px[CX - 1, CY + label_r - 2] = rgba(label_sh)

    # Outer shadow on bottom-right (soft drop-shadow effect)
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CX
            dy = y - CY
            r = math.sqrt(dx*dx + dy*dy)
            if R_OUTER < r <= R_OUTER + 1.5 and dx + dy > 6:
                px[x, y] = (0, 0, 0, 80)

    img.save(os.path.join(OUT, f"music_disc_{name}.png"))


if __name__ == "__main__":
    for name, (lc, lh, ls, acc) in DISCS.items():
        make_disc(lc, lh, ls, acc, name)
    print(f"generated {len(DISCS)} disc textures (64x64)")
