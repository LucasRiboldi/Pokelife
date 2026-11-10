"""Gera as três camadas da Floresta de Viridian. Requer Pillow."""

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parents[1] / "src/TaskbarHabitat.Widget/Assets/Habitats"
SIZE = (384, 216)
WATER_BOX = (248, 0, 384, 216)
DISPLAY_SCALE = 3


def polygon(draw, color, *points):
    draw.polygon(points, fill=color)


def rgba(color):
    return tuple(bytes.fromhex(color[1:])) + (255,)


def flecks(image, area, ground, palette, count, seed):
    rng = Random(seed)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = area
    for _ in range(count):
        x = rng.randrange(left, right - 3)
        y = rng.randrange(top, bottom - 1)
        length = rng.randint(1, 4)
        if all(image.getpixel((x + i, y)) in ground for i in range(length)):
            draw.line((x, y, x + length - 1, y), fill=rng.choice(palette))


def rock(draw, x, y, scale=1):
    def face(color, *points):
        polygon(draw, color, *((x + a * scale, y + b * scale) for a, b in points))

    face("#3c5750", (-7, 0), (-5, -5), (1, -7), (6, -4), (7, 0), (3, 2), (-5, 2))
    face("#72746a", (-6, -1), (-4, -5), (1, -6), (5, -4), (5, -2), (0, 0))
    face("#aaa18a", (-4, -4), (0, -6), (4, -4), (1, -3), (-3, -3))
    face("#83935c", (-5, -3), (-2, -4), (0, -4), (-2, -2), (-5, -2))


def tree(image, x, y, size, seed, pine=False):
    rng = Random(seed)
    draw = ImageDraw.Draw(image)
    h = size
    w = size // 2
    polygon(draw, "#395942c0", (x-w//2, y+2), (x-2, y-2), (x+w+7, y-3),
            (x+w+9, y+1), (x+w-2, y+5), (x-w//3, y+5))
    polygon(draw, "#513b34", (x-7, y), (x-3, y-5), (x-4, y-h//2), (x+5, y-h//2),
            (x+4, y-6), (x+8, y-1), (x+4, y+2), (x-5, y+2))
    draw.line((x-2, y-18, x-2, y-4, x-5, y), fill="#aa7949", width=2)
    if pine:
        for level in range(3):
            top = y-h + level*h//5
            half = w * (level+2) // 5
            polygon(draw, "#20483d", (x, top), (x+3, top+3), (x+half, top+h//2),
                    (x+half-3, top+h//2+3), (x-half, top+h//2+3), (x-half, top+h//2))
            polygon(draw, "#36724b", (x-1, top+4), (x+1, top+5), (x+4, top+h//2-4),
                    (x-half+3, top+h//2), (x-half+3, top+h//2-3))
            draw.line((x-half+6, top+h//2-4, x-3, top+h//2-5), fill="#64965a")
        return

    canopy = Image.new("RGBA", image.size)
    foliage = ImageDraw.Draw(canopy)
    for dx, dy, radius in ((-10, -19, 12), (9, -20, 13), (-15, -30, 12),
                           (11, -33, 12), (0, -39, 14), (-5, -28, 15)):
        cx, cy = x + dx*size//50, y + dy*size//50
        r = max(4, radius*size//50)
        polygon(foliage, "#244c3a", (cx-r, cy-2), (cx-r+3, cy-r//2), (cx-3, cy-r),
                (cx+3, cy-r), (cx+r-2, cy-r//2), (cx+r, cy+2), (cx+r-3, cy+r//2),
                (cx+3, cy+r-2), (cx-5, cy+r), (cx-r+2, cy+r//2))
        polygon(foliage, rng.choice(("#3a6f46", "#427a4a", "#4a824a")),
                (cx-r+2, cy-3), (cx-r+5, cy-r//2), (cx-2, cy-r+2), (cx+3, cy-r+2),
                (cx+r-3, cy-r//2), (cx+r-2, cy), (cx+4, cy+r//2), (cx-4, cy+r-2),
                (cx-r+3, cy+r//2))
        polygon(foliage, rng.choice(("#699450", "#77a257", "#5e8f50")),
                (cx-r+4, cy-3), (cx-r+6, cy-r//2), (cx-2, cy-r+2), (cx+3, cy-r+2),
                (cx+r//2, cy-r//2), (cx+3, cy-2), (cx-2, cy-2), (cx-3, cy+1))
        for _ in range(7):
            a, b = cx+rng.randint(-r//2, r//3), cy+rng.randint(-r//2, 1)
            if 0 <= a < SIZE[0] and 0 <= b < SIZE[1] and canopy.getpixel((a, b))[3]:
                foliage.point((a, b), fill=rng.choice(("#86ab5b", "#588751", "#467646")))
    image.alpha_composite(canopy)


def draw_land():
    base = Image.new("RGBA", SIZE, "#779c55")
    d = ImageDraw.Draw(base)
    polygon(d, "#5c854d", (0, 0), (175, 0), (157, 34), (118, 57), (106, 89),
            (73, 119), (45, 126), (0, 152))
    polygon(d, "#86a95d", (89, 137), (129, 112), (175, 103), (209, 119), (248, 125),
            (269, 154), (237, 177), (209, 193), (145, 205), (103, 200), (76, 172))
    polygon(d, "#628b50", (0, 176), (55, 161), (82, 179), (124, 204), (174, 214),
            (221, 203), (233, 216), (0, 216))
    polygon(d, "#52764b", (322, 74), (384, 58), (384, 216), (315, 216),
            (317, 185), (343, 159), (352, 115))
    grass = ("#779c55", "#5c854d", "#86a95d", "#628b50", "#52764b")
    flecks(base, (0, 0, *SIZE), {rgba(color) for color in grass},
           ("#719653", "#739a55", "#7da25b", "#8eae63", "#6e9555", "#799a56"), 5100, 24)

    # Ridge top and alternating faces set the height of the cave and the fall.
    polygon(d, "#4c5546", (105, 95), (112, 68), (125, 55), (130, 36), (147, 20),
            (175, 19), (188, 5), (222, 3), (241, 0), (352, 0), (369, 27),
            (354, 57), (339, 71), (328, 99), (307, 117), (270, 114), (242, 120),
            (219, 109), (199, 101), (173, 104), (148, 100), (125, 110))
    polygon(d, "#8b806d", (107, 92), (118, 69), (138, 57), (151, 43), (178, 43),
            (199, 32), (225, 35), (249, 27), (274, 29), (297, 42), (323, 33),
            (349, 36), (335, 65), (323, 75), (311, 105), (288, 109), (269, 105),
            (244, 114), (223, 103), (201, 96), (170, 97), (150, 94), (126, 103))
    polygon(d, "#bbb18e", (111, 87), (121, 67), (137, 52), (141, 36), (153, 24),
            (177, 24), (191, 11), (228, 7), (247, 0), (351, 0), (365, 26), (351, 44),
            (329, 48), (316, 64), (289, 59), (265, 69), (242, 57), (216, 63),
            (201, 57), (175, 65), (153, 61), (134, 80))
    polygon(d, "#62894c", (135, 58), (145, 42), (146, 34), (157, 26), (179, 27),
            (193, 15), (222, 12), (248, 0), (344, 0), (357, 22), (348, 34),
            (326, 39), (315, 52), (292, 49), (268, 59), (247, 48), (224, 53),
            (202, 49), (178, 58), (155, 54))
    for color, points in (
        ("#726657", ((126, 76), (136, 73), (130, 91), (121, 97), (122, 86))),
        ("#a39878", ((144, 66), (155, 61), (160, 63), (153, 80), (140, 86))),
        ("#726657", ((204, 63), (219, 61), (215, 80), (224, 102), (210, 96), (201, 81))),
        ("#a69a7b", ((222, 64), (238, 61), (247, 69), (240, 83), (243, 101), (230, 95))),
        ("#706956", ((247, 73), (257, 70), (265, 76), (261, 89), (266, 106), (252, 111), (252, 92))),
        ("#716959", ((315, 73), (329, 67), (320, 91), (308, 108), (309, 90))),
    ):
        polygon(d, color, *points)
    flecks(base, (105, 0, 365, 118),
           {rgba(c) for c in ("#bbb18e", "#8b806d", "#726657", "#a39878", "#62894c")},
           ("#9d9078", "#a6987e", "#766e5c", "#8f876b", "#66834f"), 980, 42)
    for x, y, length in ((134,74,13), (148,57,16), (195,54,13), (219,57,24),
                         (242,57,18), (265,64,17), (330,51,16), (342,44,15)):
        d.line((x+5, y-3, x, y, x-1, y+length), fill="#626e48")
        d.line((x+4, y-3, x-2, y+2, x-2, y+length-2), fill="#778d51", width=2)
        for offset in range(2, length-1, 5):
            d.line((x-4, y+offset, x, y+offset-1), fill="#879d59")
    for x, y in ((142,85), (210,75), (228,84), (235,69), (255,93), (326,83)):
        d.line((x+4, y, x+1, y+4, x+1, y+8, x-2, y+11), fill="#736b59")

    # Cave lintel, interior and stone sill.
    polygon(d, "#675e50", (147, 96), (150, 84), (157, 71), (167, 66), (181, 65),
            (193, 73), (201, 85), (206, 98), (190, 101), (160, 100))
    polygon(d, "#c6b795", (148, 93), (153, 82), (159, 72), (170, 67), (183, 68),
            (190, 73), (190, 77), (177, 73), (168, 75), (158, 84), (156, 94))
    polygon(d, "#252e31", (154, 96), (159, 85), (166, 77), (172, 74), (181, 74),
            (188, 78), (195, 86), (199, 96), (192, 99), (160, 99))
    polygon(d, "#38403a", (158, 96), (171, 90), (183, 89), (195, 95), (193, 99), (160, 99))
    polygon(d, "#a39777", (156, 98), (172, 97), (185, 98), (199, 97), (199, 100),
            (185, 104), (165, 103), (156, 101))

    # Split trails fade into the meadow. The Pokémon also crosses open grass.
    for path in (
        [(72,155),(95,154),(119,143),(137,130),(154,115),(166,106),(179,102)],
        [(157,114),(178,114),(199,111),(220,122),(242,132),(261,142)],
        [(113,146),(108,158),(117,169),(134,177),(150,183),(171,181)],
    ):
        for width, color in ((11, "#91a363"), (8, "#b6ab70"), (5, "#c8b781")):
            d.line(path, fill=color, width=width, joint="curve")
    flecks(base, (70, 100, 270, 194),
           {rgba(c) for c in ("#b6ab70", "#c8b781", "#91a363")},
           ("#a89d68", "#d4c48d", "#bdb27c"), 460, 5)
    return base


def draw_water(base):
    d = ImageDraw.Draw(base)
    downstream = ((282, 106), (299, 99), (320, 105), (335, 116), (340, 131),
                  (328, 148), (329, 162), (342, 177), (338, 194), (318, 215),
                  (311, 216), (264, 216), (270, 203), (290, 189), (292, 176),
                  (278, 163), (274, 150), (273, 139), (262, 130), (265, 117))
    upstream = ((306, 0), (333, 0), (329, 13), (310, 26), (309, 38), (320, 49),
                (318, 60), (310, 68), (282, 70), (278, 59), (288, 50), (294, 40),
                (292, 24), (295, 12))
    polygon(d, "#9f9768", *downstream)
    polygon(d, "#377d7d", (282, 111), (300, 103), (319, 109), (332, 119), (335, 131),
            (323, 149), (325, 164), (337, 178), (333, 193), (314, 214), (307, 216),
            (269, 216), (274, 205), (294, 191), (297, 176), (283, 161), (279, 150),
            (278, 137), (268, 129), (270, 120))
    polygon(d, "#236477", (283, 118), (306, 110), (323, 116), (330, 127), (320, 142),
            (317, 151), (322, 169), (331, 180), (327, 192), (308, 214), (278, 216),
            (283, 208), (300, 193), (303, 174), (290, 158), (285, 145), (286, 135), (276, 127))
    polygon(d, "#388183", *upstream)
    polygon(d, "#2b6e7e", (313, 0), (328, 0), (322, 13), (304, 24), (303, 40),
            (314, 50), (312, 61), (287, 66), (287, 59), (299, 46), (299, 26), (301, 13))
    waterfall = ((283, 66), (300, 65), (315, 60), (317, 67), (314, 77),
                 (315, 91), (316, 110), (323, 119), (311, 125), (288, 123),
                 (274, 119), (281, 111), (283, 89))
    polygon(d, "#64bcc0", *waterfall)
    polygon(d, "#3f95a3", (285, 68), (290, 68), (292, 109), (288, 118),
            (280, 119), (284, 104))
    polygon(d, "#87d6cd", (292, 69), (302, 66), (303, 78), (300, 95), (302, 112),
            (306, 119), (293, 121), (295, 112), (293, 97))
    polygon(d, "#438f9e", (308, 66), (315, 63), (313, 86), (315, 110), (319, 118),
            (308, 120), (306, 111), (307, 95))
    polygon(d, "#b5e7d3", (283, 67), (292, 65), (300, 65), (309, 62), (315, 60),
            (315, 63), (307, 66), (302, 67), (290, 69), (283, 69))
    polygon(d, "#9bded3", (275, 119), (282, 115), (290, 117), (297, 115), (304, 116),
            (314, 115), (322, 119), (320, 122), (308, 124), (291, 124), (281, 122))
    return waterfall


def decorate(base, water_colors):
    d = ImageDraw.Draw(base)
    rng = Random(73)
    for x, y in ((126, 97), (135, 87), (145, 109), (211, 99), (230, 107), (251, 112),
                 (266, 116), (263, 126), (275, 140), (279, 159), (282, 175), (273, 199),
                 (331, 146), (341, 173), (331, 201), (255, 177), (204, 153), (109, 115),
                 (80, 133), (177, 191), (68, 192), (117, 202), (301, 148), (312, 180)):
        rock(d, x, y, 2 if (x, y) in ((251,112), (331,146), (282,175)) else 1)
    for _ in range(240):
        x, y = rng.randrange(1, 381), rng.randrange(16, 215)
        if base.getpixel((x, y)) in water_colors or not (
            x < 105 or y > 121 and x < 261 or y < 50 and x < 275 or x > 345
        ):
            continue
        r, g, b, _ = base.getpixel((x, y))
        if g < r + 6 or g < b + 24:
            continue
        d.line((x, y, x, y-2, x-1, y-3), fill="#4f7948")
        d.line((x+1, y, x+2, y-2), fill="#a7b96b")
        if rng.randrange(5) == 0:
            d.point((x-1, y-3), fill=rng.choice(("#f7e1aa", "#f3cb72", "#e9a487")))
    for x, y in ((96,126),(125,159),(158,144),(194,138),(229,148),
                 (153,194),(211,182),(236,174),(251,167),(79,143)):
        for _ in range(6):
            fx, fy = x+rng.randrange(-5,6), y+rng.randrange(-4,5)
            d.line((fx, fy, fx, fy-3), fill="#577a45")
            d.line((fx-1, fy-3, fx+1, fy-3), fill=rng.choice(("#f4dc92", "#e4ac83", "#e7dfa5")))
    for i, (x, y, size) in enumerate(((3,33,46),(26,39,47),(48,32,45),(78,28,55),
            (102,45,53),(125,31,45),(148,18,40),(173,16,45),(224,16,45),(255,14,45),
            (274,25,45),(350,28,53),(379,40,56),(4,79,61),(29,76,45),(55,68,54),
            (80,61,43),(105,72,49),(16,115,60),(47,105,52),(71,95,49),
            (88,118,47),(372,83,55),(354,111,46),(376,134,58),(353,158,47),
            (15,156,57),(45,141,50),(6,191,51),(38,195,52),(373,204,53))):
        tree(base, x, y, size, 120+i, pine=i % 4 == 0)


def water_atlas(base, water_colors, waterfall):
    left, top, right, bottom = WATER_BOX
    width, height = right-left, bottom-top
    atlas = Image.new("RGBA", (width*4, height*2))
    rng = Random(123)
    currents = [(rng.randrange(269, 338), rng.randrange(5, 217), rng.randrange(3, 11))
                for _ in range(190)]
    strands = [(rng.randrange(285, 315), rng.randrange(0, 48), rng.randrange(3, 13))
               for _ in range(60)]
    mask = Image.new("1", SIZE)
    ImageDraw.Draw(mask).polygon(waterfall, fill=1)
    for frame in range(8):
        effect = Image.new("RGBA", SIZE)
        d = ImageDraw.Draw(effect)
        for x, y, length in currents:
            phase = (y + frame*2) % 16
            ay = y - y % 16 + phase
            opacity = min(174, phase*42, (15-phase)*42)
            for i in range(length):
                ax = x + i + phase//3
                if ay < SIZE[1] and base.getpixel((ax, ay)) in water_colors:
                    color = (117,187,180) if y % 3 else (166,214,198)
                    d.point((ax, ay), fill=(*color, opacity))
        for x, offset, length in strands:
            for i in range(length):
                y = 66 + (offset + frame*6 + i) % 48
                if mask.getpixel((x, y)):
                    d.point((x, y), fill="#cff5debc" if offset % 4 == 0 else "#b3ecda75")
        for i, x in enumerate(range(276, 323, 3)):
            phase = (frame + i*3) % 8
            y = 118 + phase
            if phase < 6:
                d.line((x, y, x+2, y), fill="#d6f3d7" if phase < 3 else "#a9dfd3")
            if i % 3 == 0 and phase < 5:
                d.point((x+phase//2, 114-phase), fill="#d3f5dcb0")
        atlas.paste(effect.crop(WATER_BOX), (frame%4*width, frame//4*height))
    return atlas


def save_layer(image, name):
    width, height = image.size
    image.resize((width*DISPLAY_SCALE, height*DISPLAY_SCALE), Image.Resampling.NEAREST).save(
        ASSETS / name, optimize=True
    )


def main():
    base = draw_land()
    waterfall = draw_water(base)
    water_colors = {rgba(c) for c in ("#377d7d", "#236477", "#388183", "#2b6e7e")}
    decorate(base, water_colors)
    foreground = Image.new("RGBA", SIZE)
    for seed, (x, y, size) in enumerate(((10,218,60), (61,211,50), (91,222,56),
                                         (207,226,50), (354,214,62), (384,212,50))):
        tree(foreground, x, y, size, 301+seed, pine=seed in (0, 2, 5))
    save_layer(base.convert("RGB"), "viridian-valley.png")
    save_layer(foreground, "viridian-foreground.png")
    save_layer(water_atlas(base, water_colors, waterfall), "viridian-water.png")


if __name__ == "__main__":
    main()
