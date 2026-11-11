"""Rebuild the playable Viridian art from the local reference and reusable sprites."""
import json
from math import sin
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

REFERENCE = Path(__file__).parent
ASSETS = REFERENCE.parent / "src/TaskbarHabitat.Widget/Assets/Habitats"
OUTPUT = ASSETS / "ViridianAmpliada"
SIZE = (1536, 1024)
WEST = 256
NEAREST = Image.Resampling.NEAREST


def cutout(source, outline, keep):
    x, y = map(min, zip(*outline))
    right, bottom = map(max, zip(*outline))
    piece = source.crop((x, y, right + 1, bottom + 1)).convert("RGBA")
    mask = Image.new("L", piece.size)
    ImageDraw.Draw(mask).polygon([(px - x, py - y) for px, py in outline], fill=255)
    for py in range(piece.height):
        for px in range(piece.width):
            if not keep(piece.getpixel((px, py)), y + py):
                mask.putpixel((px, py), 0)
    piece.putalpha(mask)
    return piece, (x, y)


def sway(piece, lean):
    frame = Image.new("RGBA", (piece.width + 8, piece.height))
    for y in range(piece.height):
        dx = round(lean * (1 - y / piece.height) ** 2)
        frame.paste(piece.crop((0, y, piece.width, y + 1)), (4 + dx, y))
    return frame


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(REFERENCE / "MAPA FINAL 1.png").convert("RGB").resize((1024, 1024), NEAREST)
    ground_sample = source.crop((335, 214, 588, 373))
    ground = Image.new("RGB", SIZE)
    for y in range(0, ground.height, ground_sample.height):
        for x in range(0, ground.width, ground_sample.width):
            patch = ground_sample if x // ground_sample.width % 2 == 0 else ImageOps.mirror(ground_sample)
            if y // ground_sample.height % 2:
                patch = ImageOps.flip(patch)
            ground.paste(patch, (x, y))
    meadow = ground.copy()
    ground.paste(source, (WEST, 0))
    # Make the western passage continuous across the original edge.
    for y in range(633, 800):
        for x in range(68):
            r, g, b = source.getpixel((x, y))
            if g < 147 or r < 49:
                ground.putpixel((WEST + x, y), meadow.getpixel((WEST + x, y)))

    tree_outline = [
        (381, 702), (385, 652), (411, 617), (428, 580), (462, 566), (490, 538),
        (544, 538), (575, 556), (611, 594), (645, 641), (653, 694), (626, 723),
        (570, 730), (546, 748), (544, 775), (575, 809), (481, 822), (453, 803),
        (483, 773), (480, 744), (453, 727), (401, 733),
    ]
    tree, (tree_x, tree_y) = cutout(
        source, tree_outline,
        lambda rgb, y: (rgb[1] < 153 or rgb[0] > rgb[1] * .87) if y < 738
        else rgb[0] > rgb[1] * .82 or rgb[1] < 54,
    )
    cabin_outline = [
        (80, 248), (142, 156), (158, 156), (244, 210), (323, 258),
        (322, 301), (343, 303), (337, 364), (234, 419), (200, 415),
        (132, 357), (86, 318),
    ]
    cabin, cabin_origin = cutout(
        source, cabin_outline, lambda rgb, _: rgb[1] < 79 or rgb[0] >= rgb[1] * .87,
    )
    for piece, (x, y) in [(tree, (tree_x, tree_y)), (cabin, cabin_origin)]:
        box = (WEST + x, y, WEST + x + piece.width, y + piece.height)
        grass = meadow.crop(box)
        if piece is tree:
            # Keep the shade under the roots while restoring grass under the crown.
            shade = Image.new("L", piece.size)
            ImageDraw.Draw(shade).ellipse((55, 220, 248, 301), fill=125)
            grass = Image.composite(ImageEnhance.Brightness(grass).enhance(.52), grass, shade)
        ground.paste(grass, box[:2], piece.getchannel("A"))

    ground.resize((SIZE[0] * 2, SIZE[1] * 2), NEAREST).save(OUTPUT / "solo.png", optimize=True)
    preview = ground.convert("RGBA")
    objects, textures = [], {}

    def atlas(name, frames):
        textures[name] = frames[0]
        strip = Image.new("RGBA", (frames[0].width * len(frames), frames[0].height))
        for index, frame in enumerate(frames):
            strip.paste(frame, (index * frame.width, 0))
        strip.save(OUTPUT / (name + ".png"), optimize=True)
        return len(frames)

    def place(name, x, y, depth, frames=1, frame_ms=0, phase=0):
        width, height = textures[name].size
        objects.append(dict(file=f"ViridianAmpliada/{name}.png", x=x, y=y, width=width,
                            height=height, depth=depth, frames=frames, frameMs=frame_ms, phase=phase))

    # The crown and its fruit share a pivot, while the trunk stays on the ground.
    split = 721 - tree_y
    crown = tree.crop((0, 0, tree.width, split))
    trunk = tree.crop((0, split, tree.width, tree.height))
    atlas("frutifera-tronco", [trunk])
    wind = (0, 2, 3, 1)
    atlas("frutifera-copa", [sway(crown, lean) for lean in wind])
    fruit = Image.new("RGBA", crown.size)
    draw = ImageDraw.Draw(fruit)
    for x, y in ((84, 106), (128, 78), (150, 117), (191, 91), (218, 132), (105, 155)):
        draw.ellipse((x, y, x + 6, y + 6), fill="#8c3429")
        draw.ellipse((x + 1, y, x + 5, y + 4), fill="#d96036")
        draw.point((x + 2, y + 1), fill="#f7b64d")
    atlas("frutifera-frutos", [sway(fruit, lean) for lean in wind])
    depth = 813 * 4
    place("frutifera-tronco", WEST + tree_x, 721, depth)
    place("frutifera-copa", WEST + tree_x - 4, tree_y, depth + 1, 4, 250)
    place("frutifera-frutos", WEST + tree_x - 4, tree_y, depth + 2, 4, 250)
    atlas("cabana", [cabin])
    place("cabana", WEST + cabin_origin[0], cabin_origin[1], 401 * 4)

    # Smaller trees share the same silhouette and have two leaf palettes.
    for variant, scale in enumerate((.62, .76)):
        small_crown = crown.resize((round(crown.width * scale), round(crown.height * scale)), NEAREST)
        small_crown = ImageEnhance.Brightness(small_crown).enhance((.74, .57)[variant])
        small_trunk = trunk.resize((small_crown.width, round(trunk.height * scale)), NEAREST)
        atlas(f"copa-{variant}", [sway(small_crown, lean) for lean in wind])
        atlas(f"tronco-{variant}", [small_trunk])
        shade = Image.new("RGBA", (round(133 * scale), round(55 * scale)))
        brush = ImageDraw.Draw(shade)
        brush.ellipse((0, 0, shade.width - 1, shade.height - 1), fill=(16, 49, 31, 53))
        brush.ellipse((9, 5, shade.width - 11, shade.height - 6), fill=(16, 49, 31, 84))
        atlas(f"sombra-{variant}", [shade])

    tiled = json.loads((REFERENCE / "Viridian.tmj").read_text(encoding="utf-8"))
    forest = next(layer for layer in tiled["layers"] if layer["name"] == "Arvores")
    for index, tree_object in enumerate(forest["objects"]):
        x = round((tree_object["x"] + forest.get("offsetx", 0)) / 2)
        y = round((tree_object["y"] + forest.get("offsety", 0)) / 2)
        variant = next(p["value"] for p in tree_object["properties"] if p["name"] == "variant")
        trunk_name, crown_name = f"tronco-{variant}", f"copa-{variant}"
        trunk_width, trunk_height = textures[trunk_name].size
        crown_width, crown_height = textures[crown_name].size
        shade_name = f"sombra-{variant}"
        shade_width, shade_height = textures[shade_name].size
        place(shade_name, x - shade_width // 2, y - shade_height // 2, -1)
        place(trunk_name, x - trunk_width // 2, y - trunk_height + 2, y * 4)
        place(crown_name, x - crown_width // 2, y - trunk_height - crown_height + 2,
              y * 4 + 1, 4, 245 + variant * 35, index % 4)

    rng = Random(65)
    for name in ("grama", "flores"):
        strip = Image.open(ASSETS / "Viridian" / (name + ".png")).convert("RGBA")
        width = strip.width // 4
        atlas(name, [ImageEnhance.Brightness(strip.crop((i * width, 0, (i + 1) * width, strip.height)))
                     .enhance(.74) for i in range(4)])
    for x in range(48, 1520, 45):
        for y in range(190, 1000, 39):
            if 305 < x < 1290 or rng.random() < .46:
                continue
            name = rng.choice(("grama", "grama", "flores"))
            place(name, x + rng.randint(-16, 16), y + rng.randint(-14, 14), 0, 4, 260, rng.randrange(4))

    # Animate selected blue pixels in the original river and waterfall.
    left = 613
    water = source.crop((left, 0, 1024, 1024))
    ripples = [(x, y, (r, g, b)) for y in range(water.height) for x in range(water.width)
               for r, g, b in [water.getpixel((x, y))]
               if b > r + 36 and g > r + 25 and b > g + 4 and
               ((x + y * 13) % 39 < 7 or (x > 291 and y < 360 and x % 11 < 3))]
    frames = []
    for i in range(8):
        frame = Image.new("RGBA", water.size)
        for x, y, color in ripples:
            highlight = round(18 * sin((x * .08 + y * .2 - i) * .785398))
            frame.putpixel((x, y), tuple(max(0, min(c + highlight, 255)) for c in color) + (255,))
        frames.append(frame)
    atlas("corrente", frames)
    place("corrente", WEST + left, 0, -1, 8, 120)

    for item in sorted(objects, key=lambda item: item["depth"]):
        preview.alpha_composite(textures[Path(item["file"]).stem], (item["x"], item["y"]))
    preview.convert("RGB").resize((SIZE[0] * 2, SIZE[1] * 2), NEAREST).save(
        REFERENCE / "Viridian-Ampliada.png", optimize=True)
    (OUTPUT / "layout.json").write_text(
        '{\n  "objects": [\n' + ",\n".join("    " + json.dumps(item) for item in objects) + "\n  ]\n}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
