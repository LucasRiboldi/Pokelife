"""Gera o cenário, as peças e a prévia de Viridian. Requer Pillow."""

import json
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw


from viridian_arte import canopy, charmander_frames, cottage, fallen_log, fruits, meadow_piece, sway, trunk


ASSETS = Path(__file__).resolve().parents[1] / "src/TaskbarHabitat.Widget/Assets/Habitats"
SIZE = (512, 288)
WATER_BOX = (248, 0, 384, SIZE[1])
CAMERA = {"x": 40, "y": 58, "width": 342, "height": 192}
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


def draw_land():
    base = Image.new("RGBA", SIZE, "#83ae57")
    d = ImageDraw.Draw(base)
    polygon(d, "#63944d", (0, 0), (175, 0), (157, 34), (118, 57), (106, 89),
            (73, 119), (45, 126), (0, 152))
    polygon(d, "#96bc61", (89, 137), (129, 112), (175, 103), (209, 119), (248, 125),
            (269, 154), (237, 177), (209, 193), (145, 205), (103, 200), (76, 172))
    polygon(d, "#6b9e54", (0, 176), (55, 161), (82, 179), (124, 204), (174, 214),
            (221, 203), (233, 216), (0, 216))
    polygon(d, "#61904d", (322, 74), (384, 58), (384, 216), (315, 216),
            (317, 185), (343, 159), (352, 115))
    polygon(d, "#96bc61", (62, 173), (116, 156), (173, 165), (215, 153),
            (274, 158), (290, 188), (259, 218), (269, 249), (236, 273), (170, 275),
            (101, 257), (69, 233), (52, 205))
    polygon(d, "#6b9e54", (372, 0), (511, 0), (511, 287), (389, 287),
            (381, 252), (399, 219), (422, 168), (396, 130), (386, 64))
    polygon(d, "#63944d", (0, 197), (38, 208), (49, 241), (87, 262), (116, 287), (0, 287))
    grass = ("#83ae57", "#63944d", "#96bc61", "#6b9e54", "#61904d")
    flecks(base, (0, 0, *SIZE), {rgba(color) for color in grass},
           ("#7ca552", "#80aa55", "#8ab25b", "#9ec265", "#79a453", "#86ad5d"), 7400, 24)

    # Horizontal ledges expose a frontal rock wall below the upper grass.
    polygon(d, "#4d4c42", (105,99),(109,81),(121,73),(121,54),(139,43),(139,24),
            (164,14),(198,14),(212,0),(352,0),(366,20),(363,42),(348,53),
            (347,74),(333,80),(333,98),(318,110),(289,115),(272,111),(253,117),
            (233,110),(219,110),(204,104),(169,106),(152,103),(131,111),(115,108))
    polygon(d, "#8b806d", (110,98),(114,84),(127,76),(128,55),(145,46),(146,25),
            (164,17),(199,17),(216,1),(350,1),(361,21),(358,41),(343,51),
            (341,72),(328,77),(327,96),(313,105),(290,111),(273,105),(253,113),
            (234,105),(221,105),(203,98),(167,100),(151,97),(130,105),(116,103))
    polygon(d, "#b9aa82", (114,89),(131,74),(131,53),(147,44),(147,25),(165,17),
            (201,17),(215,0),(350,0),(360,23),(356,42),(339,52),(338,66),
            (317,68),(311,63),(281,64),(274,70),(251,70),(246,63),(218,63),
            (209,67),(183,67),(175,62),(151,62),(149,73),(137,77),(126,94))
    polygon(d, "#73994a", (134,55),(151,44),(151,29),(167,21),(202,21),(216,0),
            (347,0),(357,24),(351,41),(335,49),(332,59),(314,61),(306,56),
            (283,57),(271,64),(252,64),(248,58),(218,58),(208,62),(184,62),
            (175,57),(150,57),(144,63),(134,63))
    d.line((151,56,175,56,184,61,208,61,218,57,248,57,252,63,271,63,283,56),
           fill="#a6b963", width=2)
    for color, points in (
        ("#726657", ((127,80),(136,75),(135,92),(129,92),(127,100),(119,102),(121,88))),
        ("#ab9a73", ((139,76),(148,71),(151,64),(161,65),(160,80),(153,81),(152,91),(140,95))),
        ("#6c6153", ((205,67),(215,66),(216,81),(221,83),(222,104),(211,101),(207,92))),
        ("#a69a7b", ((222,65),(238,65),(240,75),(236,83),(239,101),(228,100),(225,89))),
        ("#706354", ((246,72),(254,74),(269,73),(269,86),(263,88),(265,103),(257,111),
                     (250,109),(250,95),(245,92))),
        ("#a39472", ((273,74),(281,67),(288,68),(290,84),(284,84),(286,105),(277,108),(274,93))),
        ("#706354", ((319,73),(331,69),(331,79),(326,81),(325,94),(313,104),(309,102),(315,88))),
    ):
        polygon(d, color, *points)
    flecks(base, (105, 0, 365, 118),
           {rgba(c) for c in ("#b9aa82", "#8b806d", "#726657", "#6c6153", "#73994a")},
           ("#a49270", "#a6987e", "#766e5c", "#8f876b", "#66834f"), 980, 42)
    for x, y, length in ((134,74,13), (148,65,16), (195,64,13), (219,61,24),
                         (242,61,18), (265,68,17), (330,62,16), (342,55,15)):
        d.line((x+5, y-3, x, y, x-1, y+length), fill="#626e48")
        d.line((x+4, y-3, x-2, y+2, x-2, y+length-2), fill="#778d51", width=2)
        for offset in range(2, length-1, 5):
            d.line((x-4, y+offset, x, y+offset-1), fill="#879d59")
    for x, y in ((142,85), (210,75), (228,84), (235,69), (255,93), (326,83)):
        d.line((x+4, y, x+1, y+4, x+1, y+8, x-2, y+11), fill="#736b59")

    # Cave lintel, interior and stone sill.
    polygon(d, "#675e50", (147,97),(147,86),(153,85),(153,76),(161,76),(161,69),
            (187,68),(187,73),(195,73),(196,81),(201,82),(201,91),(206,92),(206,99),
            (190,101),(160,100))
    polygon(d, "#c6b795", (148,94),(148,87),(154,87),(154,77),(162,77),(162,71),
            (185,70),(185,75),(167,75),(167,81),(160,81),(160,89),(155,89),(155,96))
    polygon(d, "#252e31", (154,96),(154,90),(160,90),(160,82),(167,82),(167,76),
            (185,75),(185,79),(192,79),(192,86),(197,86),(197,92),(200,92),(200,98),(160,99))
    polygon(d, "#38403a", (158, 96), (171, 90), (183, 89), (195, 95), (193, 99), (160, 99))
    polygon(d, "#a39777", (156, 98), (172, 97), (185, 98), (199, 97), (199, 100),
            (185, 104), (165, 103), (156, 101))

    return base


def draw_water(base):
    d = ImageDraw.Draw(base)
    downstream = ((282, 106), (299, 99), (320, 105), (335, 116), (340, 131),
                  (328, 148), (329, 162), (342, 177), (338, 194), (318, 215),
                  (318, 235), (334, 253), (335, 268), (325, 288), (277, 288),
                  (289, 268), (286, 253), (271, 234), (264, 216), (270, 203), (290, 189), (292, 176),
                  (278, 163), (274, 150), (273, 139), (262, 130), (265, 117))
    upstream = ((306, 0), (333, 0), (329, 13), (310, 26), (309, 38), (320, 49),
                (318, 60), (310, 68), (282, 70), (278, 59), (288, 50), (294, 40),
                (292, 24), (295, 12))
    polygon(d, "#9f9768", *downstream)
    polygon(d, "#398f9a", (282, 111), (300, 103), (319, 109), (332, 119), (335, 131),
            (323, 149), (325, 164), (337, 178), (333, 193), (314, 214), (314, 237),
            (330, 254), (330, 267), (320, 288), (282, 288), (293, 269), (290, 251),
            (275, 232), (269, 216), (274, 205), (294, 191), (297, 176), (283, 161), (279, 150),
            (278, 137), (268, 129), (270, 120))
    polygon(d, "#285f8c", (283, 118), (306, 110), (323, 116), (330, 127), (320, 142),
            (317, 151), (322, 169), (331, 180), (327, 192), (308, 214), (309, 239),
            (324, 256), (324, 267), (315, 288), (289, 288), (299, 270), (297, 252), (283, 232), (278, 216),
            (283, 208), (300, 193), (303, 174), (290, 158), (285, 145), (286, 135), (276, 127))
    polygon(d, "#489ca0", *upstream)
    polygon(d, "#326c94", (313, 0), (328, 0), (322, 13), (304, 24), (303, 40),
            (314, 50), (312, 61), (287, 66), (287, 59), (299, 46), (299, 26), (301, 13))
    waterfall = ((283, 66), (300, 65), (315, 60), (317, 67), (314, 77),
                 (315, 91), (316, 110), (323, 119), (311, 125), (288, 123),
                 (274, 119), (281, 111), (283, 89))
    polygon(d, "#63bdd2", *waterfall)
    polygon(d, "#4696ba", (285, 68), (290, 68), (292, 109), (288, 118),
            (280, 119), (284, 104))
    polygon(d, "#99dddc", (292, 69), (302, 66), (303, 78), (300, 95), (302, 112),
            (306, 119), (293, 121), (295, 112), (293, 97))
    polygon(d, "#468ba8", (308, 66), (315, 63), (313, 86), (315, 110), (319, 118),
            (308, 120), (306, 111), (307, 95))
    polygon(d, "#b5e7d3", (283, 67), (292, 65), (300, 65), (309, 62), (315, 60),
            (315, 63), (307, 66), (302, 67), (290, 69), (283, 69))
    polygon(d, "#b0e8df", (275, 119), (282, 115), (290, 117), (297, 115), (304, 116),
            (314, 115), (322, 119), (320, 122), (308, 124), (291, 124), (281, 122))
    return waterfall


def water_atlas(base, water_colors, waterfall):
    left, top, right, bottom = WATER_BOX
    width, height = right-left, bottom-top
    atlas = Image.new("RGBA", (width*4, height*2))
    rng = Random(123)
    currents = [(rng.randrange(269, 338), rng.randrange(5, SIZE[1]), rng.randrange(3, 11))
                for _ in range(270)]
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


def make_objects(terrain):
    pieces = {}
    objects = []
    rng = Random(73)

    def add(name, frames):
        pieces[name] = frames
        width, height = frames[0].size
        strip = Image.new("RGBA", (width * len(frames), height))
        for index, frame in enumerate(frames):
            assert frame.size == (width, height), name
            strip.paste(frame, (index * width, 0))
        save_layer(strip, f"Viridian/{name}.png")

    def place(name, x, y, depth, phase=0, frame_ms=0):
        width, height = pieces[name][0].size
        assert 0 <= phase < len(pieces[name]) and (frame_ms > 0) == (len(pieces[name]) > 1), name
        objects.append(dict(file=f"Viridian/{name}.png", x=x, y=y, width=width, height=height,
                            depth=depth, frames=len(pieces[name]), phase=phase, frameMs=frame_ms))

    def wind(name, art, foot):
        add(name, [sway(art, lean, foot) for lean in (0, 1, 2, 1)])

    palettes = (
        ("#254c39", "#3a723d", "#568d3c", "#77a949", "#99bf54"),
        ("#264a39", "#3d6b3f", "#5b9445", "#86af4d", "#a2bf59"),
        ("#2b5338", "#4c793e", "#70a544", "#9abb50", "#b9ce60"),
    )
    tree_sizes = (50, 58, 64)
    for i, (size, palette) in enumerate(zip(tree_sizes, palettes)):
        add(f"tronco-{i}", [trunk(size)])
        wind(f"copa-{i}", canopy(size, palette, 30+i), size-11)

    add("tronco-frutifera", [trunk(96)])
    wind("copa-frutifera", canopy(96, palettes[2], 39), 85)
    wind("frutos", fruits(), 85)
    add("casa", [cottage()])
    add("tronco-caido", [fallen_log()])
    for name, scale in (("pedra", 1), ("rocha", 2)):
        art = Image.new("RGBA", (16 * scale, 12 * scale))
        rock(ImageDraw.Draw(art), 8 * scale, 8 * scale, scale)
        add(name, [art])
    for kind, name in (("grass", "grama"), ("flower", "flores"), ("shrub", "arbusto")):
        add(name, [meadow_piece(kind, lean) for lean in (0, 1, 2, 1)])

    def tree(x, y, variant, phase):
        size = tree_sizes[variant]
        depth = y * 4
        place(f"tronco-{variant}", x-size//2, y-size//2+6, depth)
        place(f"copa-{variant}", x-size//2, y-size, depth+1, phase, 205 + variant*35)

    forest = (
        (2,39),(31,32),(63,39),(93,36),(118,27),(156,18),(187,20),(226,17),(258,14),
        (279,24),(355,29),(380,42),(411,35),(441,29),(474,35),(504,28),
        (5,73),(37,75),(66,68),(96,61),(119,56),(372,80),(403,71),(437,68),(478,72),(509,65),
        (5,111),(36,108),(61,98),(400,111),(431,101),(465,111),(503,110),
        (2,148),(28,145),(369,135),(408,150),(446,143),(475,153),(511,146),
        (5,184),(36,178),(382,176),(414,190),(454,181),(488,192),(513,184),
        (9,222),(36,210),(394,210),(433,227),(470,220),(501,223),
        (4,264),(38,254),(67,265),(370,246),(403,258),(441,268),(481,259),(512,262),
        (8,296),(52,298),(90,300),(134,301),(209,307),(257,306),(369,300),(415,306),(461,301),(502,299),
    )
    for x, y in forest:
        tree(x, y, rng.randrange(3), rng.randrange(4))

    place("casa", 53, 75, 153*4)
    place("tronco-frutifera", 185, 148, 190*4)
    place("copa-frutifera", 185, 94, 190*4+1, 1, 250)
    place("frutos", 185, 94, 190*4+2, 1, 250)
    place("tronco-caido", 51, 222, 235*4)
    place("tronco-caido", 350, 187, 200*4)
    for i, (x, y) in enumerate(((133,98),(211,101),(252,117),(267,131),(277,156),(282,174),
                               (270,196),(280,239),(296,271),(337,151),(349,178),(349,206),
                               (336,240),(333,270),(66,202),(80,230),(134,263),(173,255),
                               (241,254),(245,192),(391,227))):
        name = "rocha" if i % 4 == 0 else "pedra"
        width, height = pieces[name][0].size
        place(name, x-width//2, y-height+3, y*4)

    for i, (x, y) in enumerate(((47,167),(64,172),(113,159),(136,177),(200,187),
                               (245,164),(278,174),(255,239),(225,250),(195,266),
                               (104,250),(78,209),(76,182),(363,155),(364,216),(353,254))):
        place("arbusto", x-9, y-12, y*4, i%4, 230+i%5*30)

    meadow = {rgba(color) for color in ("#83ae57", "#96bc61", "#6b9e54", "#63944d", "#61904d",
                                        "#7ca552", "#80aa55", "#8ab25b", "#9ec265", "#79a453", "#86ad5d")}
    for y in range(113, 285, 12):
        for x in range(10, 510, 15):
            px, py = x + rng.randrange(-4, 5), y + rng.randrange(-4, 5)
            if terrain.getpixel((px, py)) not in meadow or (60 < px < 140 and py < 158):
                continue
            if rng.randrange(5) == 0:
                continue
            kind = "flores" if rng.randrange(6) == 0 else "grama"
            place(kind, px-9, py-12, 1, rng.randrange(4), rng.randrange(150, 285, 15))
    return pieces, objects


def compose_preview(terrain, water, pieces, objects, frame, pokemon):
    preview = terrain.copy()
    width, height = WATER_BOX[2] - WATER_BOX[0], SIZE[1]
    x, y = frame % 4 * width, frame // 4 * height
    preview.alpha_composite(water.crop((x, y, x+width, y+height)), (WATER_BOX[0], 0))
    foot_x, foot_y = 166 + frame * 3, 199 + frame
    actors = sorted(objects, key=lambda item: item["depth"])
    split = next((i for i, piece in enumerate(actors) if piece["depth"] > foot_y * 4 + 3), len(actors))
    for piece in actors[:split]:
        draw_piece(preview, pieces, piece, frame)
    ImageDraw.Draw(preview).ellipse((foot_x-6, foot_y-1, foot_x+6, foot_y+2), fill="#688a4e")
    preview.alpha_composite(pokemon[4 + frame % 4].transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                            (foot_x-16, foot_y-28))
    for piece in actors[split:]:
        draw_piece(preview, pieces, piece, frame)
    return preview.convert("RGB")


def draw_piece(preview, pieces, item, frame):
    variants = pieces[Path(item["file"]).stem]
    index = ((frame * 110 // item["frameMs"] + item["phase"]) % len(variants)
             if item["frameMs"] else 0)
    preview.alpha_composite(variants[index], (item["x"], item["y"]))


def main():
    left, top = CAMERA["x"], CAMERA["y"]
    width, height = CAMERA["width"], CAMERA["height"]
    assert 0 <= left < left + width <= SIZE[0] and 0 <= top < top + height <= SIZE[1]
    (ASSETS / "Viridian").mkdir(exist_ok=True)
    terrain = draw_land()
    waterfall = draw_water(terrain)
    water_colors = {rgba(c) for c in ("#398f9a", "#285f8c", "#489ca0", "#326c94")}
    water = water_atlas(terrain, water_colors, waterfall)
    pieces, objects = make_objects(terrain)
    (ASSETS / "Viridian" / "layout.json").write_text(
        '{\n  "camera": ' + json.dumps(CAMERA) + ',\n  "objects": [\n'
        + ",\n".join("    " + json.dumps(item) for item in objects) + "\n  ]\n}\n", encoding="utf-8")

    pokemon = charmander_frames()
    atlas = Image.new("RGBA", (128, 160))
    for i, frame in enumerate(pokemon):
        atlas.paste(frame, (i % 4 * 32, i // 4 * 32))
    atlas.resize((atlas.width * DISPLAY_SCALE, atlas.height * DISPLAY_SCALE), Image.Resampling.NEAREST).save(
        ASSETS.parent / "Sprites" / "charmander-habitat.png", optimize=True)
    save_layer(terrain.convert("RGB"), "viridian-valley.png")
    save_layer(water, "viridian-water.png")

    crop = (left, top, left + width, top + height)
    preview = [compose_preview(terrain, water, pieces, objects, i, pokemon).crop(crop) for i in range(8)]
    preview[0].resize((width * DISPLAY_SCALE, height * DISPLAY_SCALE), Image.Resampling.NEAREST).save(
        Path(__file__).with_name("Viridian-Viva.png"), optimize=True)
    preview[0].save(Path(__file__).with_name("Viridian-Cachoeira.gif"), save_all=True,
                    append_images=preview[1:], duration=110, loop=0, optimize=True)
    sequence = pokemon[:12] + [pokemon[i] for i in (12, 15, 16, 17, 18, 19, 17, 16, 15, 12)]
    enlarged = [frame.resize((128, 128), Image.Resampling.NEAREST) for frame in sequence]
    enlarged[0].save(Path(__file__).with_name("Charmander-Animacao.gif"), save_all=True,
                     append_images=enlarged[1:], duration=155, loop=0, disposal=2)


if __name__ == "__main__":
    main()
