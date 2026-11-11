"""Peças em pixel art de Viridian, desenhadas na resolução nativa."""

from random import Random

from PIL import Image, ImageDraw


def canopy(size, palette, seed):
    image = Image.new("RGBA", (size, size - 8))
    draw = ImageDraw.Draw(image)
    rng = Random(seed)
    outline, shade, leaf, light, gleam = palette
    lean = seed % 3 - 1

    def crown(color, points):
        draw.polygon([((x + lean * (90 - y) // 15) * size // 100, y * image.height // 100)
                      for x, y in points], fill=color)

    crown(outline, ((4,53),(8,48),(9,39),(17,35),(19,28),(27,29),(30,21),(40,21),
                    (45,14),(57,15),(60,19),(70,18),(77,25),(84,26),(86,33),(92,35),
                    (93,45),(97,50),(96,62),(91,67),(90,75),(82,78),(76,84),(64,83),
                    (57,88),(47,86),(40,89),(31,85),(22,84),(19,79),(11,77),(10,69),
                    (5,66),(6,60),(3,58)))
    crown(shade, ((6,53),(11,48),(12,40),(21,36),(22,30),(29,30),(34,23),(43,23),
                  (46,17),(56,18),(59,22),(70,21),(77,28),(83,29),(85,36),(90,39),
                  (91,47),(94,52),(93,62),(88,67),(86,75),(79,75),(73,81),(63,80),
                  (56,85),(46,82),(40,86),(33,82),(24,81),(20,75),(13,73),(13,65),
                  (8,64),(8,58)))
    crown(leaf, ((7,52),(14,48),(13,41),(21,36),(24,30),(32,30),(35,24),(43,25),
                 (47,17),(56,19),(59,24),(68,22),(75,27),(80,31),(78,36),(88,40),
                 (90,46),(85,53),(89,59),(82,61),(81,67),(73,66),(69,73),(62,71),
                 (56,77),(47,72),(41,77),(34,72),(24,73),(22,67),(15,65),(14,60),(8,58)))
    crown(light, ((12,48),(16,40),(26,37),(24,32),(34,30),(39,25),(46,26),(48,19),
                  (55,20),(57,28),(65,24),(74,29),(78,35),(70,38),(73,44),(65,47),
                  (58,45),(55,53),(47,52),(41,58),(34,53),(26,56),(21,51),(14,54)))
    crown(light, ((21,64),(29,61),(34,63),(38,58),(46,61),(49,66),(41,70),(34,67),(28,70)))
    crown(gleam, ((21,37),(29,37),(36,31),(43,32),(47,26),(54,29),(49,36),(40,36),
                  (35,42),(28,42),(24,45),(18,43)))

    # Break the broad shade shapes into small clusters without softening the edges.
    accents = {tuple(bytes.fromhex(source[1:])) + (255,): accent
               for source, accent in ((shade, leaf), (leaf, shade), (light, gleam), (gleam, light))}
    for _ in range(size * 2):
        x, y = rng.randrange(3, size - 6), rng.randrange(5, image.height - 4)
        color = image.getpixel((x, y))
        if color not in accents:
            continue
        for dx, dy in ((0, 1), (1, 0), (2, 0), (3, 0), (2, -1)):
            if image.getpixel((x + dx, y + dy)) == color:
                draw.point((x + dx, y + dy), fill=accents[color])
    return image


def trunk(size):
    image = Image.new("RGBA", (size, size // 2))
    draw = ImageDraw.Draw(image)
    x, y = size // 2, image.height - 6
    w = max(4, size // 10)
    draw.ellipse((x-w*2, y-4, x+w*3, y+4), fill="#38523d")
    draw.polygon([(x-w*2,y+1),(x-w,y-5),(x-w+1,y-12),(x-w,12),(x-w*2,4),
                  (x-w,2),(x,11),(x+3,11),(x+w*2,2),(x+w*2+2,6),(x+w,15),
                  (x+w-2,y-10),(x+w,y-6),(x+w*2+2,y-1),(x+w*2,y+1),
                  (x+w,y),(x+w+2,y+4),(x+2,y+2),(x-w+1,y+4),(x-w+1,y+1)], fill="#49382e")
    draw.polygon([(x-w-1,y),(x-w+2,y-6),(x-w+3,y-12),(x-w+1,13),(x-w-5,6),
                  (x-2,13),(x+3,16),(x+w+5,8),(x+w-1,17),(x+w-4,y-8),
                  (x+w-2,y-4),(x+w+3,y-1),(x+2,y-1),(x-2,y+2),(x-4,y-2)], fill="#a66a38")
    draw.line((x-w+2,y-7,x-w+3,y-12,x-w+3,16,x-w+1,10), fill="#d69c53", width=2)
    draw.line((x+3,y-3,x+1,y-9,x+4,18,x+w+4,9), fill="#6d452b", width=2)
    draw.line((x-1,y-5,x+1,y-13,x-1,17), fill="#bd8347")
    return image


def fruits():
    image = Image.new("RGBA", (96, 88))
    draw = ImageDraw.Draw(image)
    for x, y in ((25,33), (48,24), (65,31), (80,41), (37,43),
                 (54,48), (18,49), (28,58), (68,59), (48,66)):
        draw.line((x+1,y-4,x,y-1), fill="#624427")
        draw.ellipse((x-3,y-2,x+3,y+4), fill="#85313b")
        draw.ellipse((x-2,y-2,x+2,y+2), fill="#e54f3f")
        draw.point((x-1,y-1), fill="#ffb05d")
    return image


def fallen_log():
    image = Image.new("RGBA", (32, 16))
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 8, 30, 15), fill="#496b40")
    draw.polygon([(3,8),(6,3),(25,1),(29,3),(30,7),(27,11),(9,14),(4,12)], fill="#513526")
    draw.polygon([(7,4),(25,2),(28,4),(27,7),(9,10)], fill="#a66a38")
    draw.line((10,6,26,3), fill="#db9b50")
    draw.line((12,10,27,7), fill="#6d452b")
    draw.ellipse((3,5,12,13), fill="#c38a4c")
    draw.ellipse((5,7,10,11), outline="#80522f")
    return image


def sway(image, lean, foot):
    frame = Image.new("RGBA", image.size)
    for y in range(image.height):
        offset = round(lean * max(0, foot-y) / foot)
        frame.paste(image.crop((0, y, image.width, y+1)), (offset, y))
    return frame


def meadow_piece(kind, lean):
    image = Image.new("RGBA", (18, 14))
    draw = ImageDraw.Draw(image)
    if kind == "shrub":
        draw.ellipse((2,9,16,13), fill="#517c42")
        for x, y, r in ((5,8,4), (11,7,5), (8,5,4)):
            draw.ellipse((x-r,y-r,x+r,y+r), fill="#32634a")
            draw.ellipse((x-r+1,y-r+1,x+r-1,y+r-1), fill="#69a84b")
            draw.line((x-2,y-2,x,y-3,x+1,y-3), fill="#a4c956")
        return sway(image, lean, 12)

    for x, top, spread in ((4,6,-2), (7,3,-1), (9,5,2), (12,6,3)):
        tip = x + spread + lean
        draw.line((x,12,x,9,tip,top), fill="#42734a")
        draw.line((x+1,11,x+1,9,tip+1,top+1), fill="#91ba56")
        if kind == "flower" and x in (7, 12):
            draw.line((tip-1,top,tip+2,top), fill="#ffe3a2")
            draw.line((tip,top-1,tip,top+1), fill="#ff9d91")
            draw.point((tip,top), fill="#fff1b8")
    return image


def cottage():
    image = Image.new("RGBA", (94, 83))
    d = ImageDraw.Draw(image)
    d.polygon([(8,70),(76,68),(84,73),(83,78),(74,81),(11,81),(5,77)], fill="#45634a")
    d.rectangle((7,40,71,76), fill="#4d3734")
    d.rectangle((10,45,68,70), fill="#edc58b")
    d.rectangle((10,45,68,51), fill="#be8968")
    d.rectangle((10,70,68,74), fill="#947160")
    for y in (53, 59, 65):
        d.line((11,y,67,y), fill="#d1a179")
    d.rectangle((10,48,13,70), fill="#ae7958")
    d.rectangle((65,48,68,70), fill="#ae7958")

    d.polygon([(3,39),(13,13),(17,10),(61,10),(65,13),(75,39),(75,45),(3,45)], fill="#72383a")
    d.polygon([(6,38),(16,14),(62,14),(72,38)], fill="#d5674b")
    for y in (18, 23, 28, 33, 38):
        margin = (38 - y) * 10 // 24
        d.line((8+margin,y,70-margin,y), fill="#ae4a41")
        for x in range(11 + margin + (y % 2) * 4, 68 - margin, 8):
            d.line((x,y-3,x,y), fill="#ae4a41")
            d.line((x+1,y-3,x+4,y-3), fill="#ec8858")
    d.line((16,13,62,13), fill="#ffad68", width=2)
    d.rectangle((4,39,74,42), fill="#ed8452")
    d.line((4,42,74,42), fill="#9e493c")
    d.rectangle((53,13,63,30), fill="#754940")
    d.rectangle((54,14,60,28), fill="#bd7056")
    d.rectangle((51,11,63,15), fill="#e7a274")

    for x in (16, 50):
        d.rectangle((x,52,x+11,65), fill="#604443")
        d.rectangle((x+2,54,x+9,62), fill="#5a849e")
        d.line((x+2,54,x+8,54), fill="#b6dcdd")
        d.line((x+5,55,x+5,62), fill="#e9b979")
        d.rectangle((x-1,65,x+12,67), fill="#b66a47")
    d.rectangle((32,53,45,74), fill="#65453e")
    d.rectangle((34,55,43,73), fill="#946145")
    d.rectangle((36,56,41,60), fill="#86aaa6")
    d.point((41,66), fill="#ffd276")
    d.rectangle((31,74,46,76), fill="#dbb188")
    d.rectangle((30,77,47,79), fill="#997b64")
    return image


def charmander(view, step=0, pose="walk"):
    """Draw one pose with the sole anchored at y=28."""
    image = Image.new("RGBA", (32, 32))
    d = ImageDraw.Draw(image)
    outline, shade, orange, light, cream = "#572e37", "#c94f35", "#f77d38", "#ffae55", "#ffe19b"
    stride = (-2, 0, 2, 0)[step] if pose == "walk" else 0
    head_x = 11 if view == "side" else 14
    head_y = {"lower": 4, "sit": 6, "tuck": 8, "sleep": 11, "breathe": 12}.get(pose, 0)
    lying = pose in ("sleep", "breathe")
    tip = 25 + (step % 2 if pose == "walk" else int(pose == "breathe"))
    tail_y = 20 if lying else 15
    d.line([(18,24),(22,26),(26,24),(tip+1,tail_y)], fill=outline, width=4)
    d.line([(18,24),(22,25),(25,23),(tip+1,tail_y)], fill=shade, width=2)
    d.line((23,25,25,23,tip+1,tail_y), fill=orange)
    d.polygon([(tip-3,tail_y-1),(tip-2,tail_y-6),(tip,tail_y-4),(tip+2,tail_y-9),
               (tip+3,tail_y-5),(tip+5,tail_y-2),(tip+4,tail_y+1),(tip,tail_y+2)], fill="#a93739")
    d.polygon([(tip-2,tail_y-1),(tip-1,tail_y-5),(tip+1,tail_y-3),(tip+2,tail_y-7),
               (tip+3,tail_y-3),(tip+4,tail_y-1),(tip+2,tail_y+1),(tip,tail_y+1)], fill="#ff8d31")
    d.polygon([(tip,tail_y),(tip,tail_y-3),(tip+1,tail_y-1),(tip+2,tail_y-4),
               (tip+3,tail_y-1),(tip+2,tail_y+1)], fill="#ffe45d")
    body = (9, 19 if lying else 13 + head_y//2, 21, 27)
    d.ellipse(body, fill=outline)
    d.ellipse((10,body[1]+1,20,26), fill=shade)
    d.ellipse((10,body[1]+1,18,24), fill=orange)
    if view != "back":
        d.ellipse((10,body[1]+3,16 if view == "side" else 18,26), fill=cream)
        d.line((11,24,15,25), fill="#efb567")
    for foot_x in (10 + stride, 17 - stride):
        d.ellipse((foot_x-2,24,foot_x+3,28), fill=outline)
        d.line((foot_x-1,26,foot_x+2,26), fill=orange)
        d.point((foot_x-1,27), fill=light)
    if lying:
        y = 19 + int(pose == "breathe")
        d.polygon([(3,25),(5,y+3),(9,y),(14,y),(18,y+3),(19,25),(17,28),(6,28)], fill=outline)
        d.polygon([(4,25),(6,y+3),(9,y+1),(14,y+1),(17,y+3),(18,25),(16,27),(6,27)], fill=shade)
        d.polygon([(5,25),(8,y+3),(10,y+1),(14,y+1),(17,y+4),(16,26),(7,26)], fill=orange)
        d.line((8,y+3,10,y+2,13,y+2), fill=light)
        d.line((7,24,10,24), fill=outline)
        d.point((5,25), fill=light)
        return image

    for arm_x in ((10,19) if view != "side" else (17,)):
        arm_y = 18 + head_y//3 + (stride//2 if arm_x > 14 else -stride//2)
        d.line((arm_x,arm_y,arm_x-1,arm_y+3), fill=outline, width=3)
        d.line((arm_x,arm_y,arm_x-1,arm_y+2), fill=orange)
    x, y = head_x, 3 + head_y + (step % 2 if pose == "walk" else 0)
    d.polygon([(x-6,y+2),(x-3,y),(x+3,y),(x+6,y+3),(x+7,y+7),
               (x+5,y+11),(x+1,y+13),(x-4,y+12),(x-7,y+9),(x-8,y+6)], fill=outline)
    d.polygon([(x-6,y+3),(x-3,y+1),(x+3,y+1),(x+5,y+3),(x+6,y+7),
               (x+4,y+10),(x+1,y+12),(x-4,y+11),(x-6,y+9),(x-7,y+6)], fill=shade)
    d.polygon([(x-5,y+3),(x-2,y+1),(x+2,y+1),(x+5,y+4),(x+4,y+8),
               (x+1,y+10),(x-4,y+10),(x-6,y+7)], fill=orange)
    d.line((x-4,y+3,x-2,y+2,x+1,y+2), fill=light)
    if view != "back":
        eyes = (x-4,x+3) if view == "front" else (x-3,)
        for eye in eyes:
            if pose == "tuck":
                d.line((eye-1,y+7,eye+1,y+7), fill=outline)
            else:
                d.rectangle((eye,y+4,eye+1,y+7), fill="#302a41")
                d.point((eye,y+4), fill="#fff5c7")
                d.point((eye+1,y+7), fill="#69ac98")
        d.line((x-5,y+9,x-2,y+10,x+1,y+9), fill="#a7483a")
        d.point((x-6,y+8), fill=light)
    return image


def charmander_frames():
    frames = [charmander(view, step) for view in ("front", "side", "back") for step in range(4)]
    frames.extend(charmander(view, pose="idle") for view in ("front", "side", "back"))
    frames.extend(charmander("front", pose=pose) for pose in ("lower", "sit", "tuck", "sleep", "breathe"))
    return frames
