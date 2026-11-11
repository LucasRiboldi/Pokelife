"""Bake the Tiled collision shapes and destinations into the WinUI walking grid."""
import json
from collections import deque
from math import cos, radians, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

REFERENCE = Path(__file__).parent
OUTPUT = REFERENCE.parent / "src/TaskbarHabitat.Widget/Assets/Habitats/ViridianAmpliada"
ART_SCALE = 2
FOOT_RADIUS = 5
ROOT = [(-37, -12), (-22, -27), (19, -27), (33, -13),
        (37, 0), (21, 4), (0, 0), (-24, 4), (-37, 0)]


def coordinates(layer, obj):
    return ((obj["x"] + layer.get("offsetx", 0)) / ART_SCALE,
            (obj["y"] + layer.get("offsety", 0)) / ART_SCALE)


def outline(obj):
    if "polygon" in obj:
        return [(point["x"], point["y"]) for point in obj["polygon"]]
    if obj.get("width", 0) > 0 and obj.get("height", 0) > 0 and not any(
        key in obj for key in ("ellipse", "capsule", "polyline", "text", "template", "gid")
    ):
        w, h = obj["width"], obj["height"]
        return [(0, 0), (w, 0), (w, h), (0, h)]
    raise ValueError(f'{obj["name"]}: use um polígono ou retângulo em Bloqueios.')


def reachable_cells(rows, spawn):
    visited = {spawn}
    pending = deque([spawn])
    while pending:
        x, y = pending.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (0 <= nx < len(rows[0]) and 0 <= ny < len(rows) and
                    rows[ny][nx] == "." and (nx, ny) not in visited):
                visited.add((nx, ny))
                pending.append((nx, ny))
    return visited


def main():
    tiled = json.loads((REFERENCE / "Viridian.tmj").read_text(encoding="utf-8"))
    layers = {layer["name"]: layer for layer in tiled["layers"]}
    if (tiled["orientation"] != "orthogonal" or tiled["infinite"] or
            tiled["tilewidth"] != tiled["tileheight"] or tiled["tilewidth"] % ART_SCALE):
        raise ValueError("Viridian precisa de um mapa ortogonal finito com células quadradas.")
    size = tiled["tilewidth"] // ART_SCALE
    columns, row_count = tiled["width"], tiled["height"]
    width, height = columns * size, row_count * size
    with Image.open(REFERENCE / layers["Mapa"]["image"]) as art:
        if art.size != (width * ART_SCALE, height * ART_SCALE):
            raise ValueError("A imagem e a grade do Tiled precisam ter o mesmo tamanho.")
        preview = art.convert("RGBA").resize((width, height), Image.Resampling.NEAREST)

    mask = Image.new("L", (width, height))
    draw = ImageDraw.Draw(mask)
    draw.rectangle((0, 0, width - 1, height - 1), outline=255)
    for obj in layers["Bloqueios"]["objects"]:
        x, y = coordinates(layers["Bloqueios"], obj)
        angle = radians(obj.get("rotation", 0))
        c, s = cos(angle), sin(angle)
        points = [(x + (px * c - py * s) / ART_SCALE, y + (px * s + py * c) / ART_SCALE)
                  for px, py in outline(obj)]
        if len(points) < 3:
            raise ValueError(f'{obj["name"]}: o bloqueio precisa de três pontos.')
        draw.polygon(points, fill=255)
    for obj in layers["Arvores"]["objects"]:
        x, y = coordinates(layers["Arvores"], obj)
        draw.polygon([(x + dx, y + dy) for dx, dy in ROOT], fill=255)

    # Inflate the silhouettes before blocking every cell touched by the mask.
    mask = mask.filter(ImageFilter.MaxFilter(FOOT_RADIUS * 2 + 1))
    rows = ["".join(
        "#" if mask.crop((x, y, x + size, y + size)).getbbox() else "."
        for x in range(0, width, size)) for y in range(0, height, size)]
    spawn = None
    destinations = []
    for obj in layers["Destinos"]["objects"]:
        x, y = coordinates(layers["Destinos"], obj)
        cx, cy = int(x // size), int(y // size)
        if not (0 <= cx < columns and 0 <= cy < row_count and rows[cy][cx] == "."):
            raise ValueError(f'{obj["name"]}: o ponto ({cx}, {cy}) está fora do mapa ou bloqueado.')
        cell = dict(x=cx, y=cy)
        props = {prop["name"]: prop["value"] for prop in obj.get("properties", [])}
        if props.get("spawn"):
            if spawn is not None:
                raise ValueError("Marque apenas um ponto inicial.")
            spawn = (cx, cy)
        else:
            destinations.append(dict(cell=cell, activity=props.get("activity", obj["name"]),
                                     rest=props.get("rest", False)))
    if spawn is None or not destinations:
        raise ValueError("Marque o início e pelo menos um destino em Viridian.")
    reachable = reachable_cells(rows, spawn)
    for target in destinations:
        if (target["cell"]["x"], target["cell"]["y"]) not in reachable:
            raise ValueError(f'{target["activity"]}: destino inalcançável a partir do início.')

    overlay = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(overlay)
    for cy, row in enumerate(rows):
        for cx, cell in enumerate(row):
            if cell == "#":
                x, y = cx * size, cy * size
                draw.rectangle((x, y, x + size - 1, y + size - 1), fill=(222, 55, 71, 99))
    for x in range(0, width, size):
        draw.line((x, 0, x, height), fill=(230, 240, 250, 51))
    for y in range(0, height, size):
        draw.line((0, y, width, y), fill=(230, 240, 250, 51))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    overlay.save(OUTPUT / "grade.png", optimize=True)
    preview.alpha_composite(overlay)
    markers = ImageDraw.Draw(preview)
    for cx, cy in [spawn] + [(target["cell"]["x"], target["cell"]["y"]) for target in destinations]:
        x, y = (cx + .5) * size, (cy + .5) * size
        markers.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#f7dc8f", outline="#142525", width=2)
    preview.convert("RGB").save(REFERENCE / "Viridian-Ampliada-Grade.png", optimize=True)
    data = dict(cellSize=size, rows=rows, spawn=dict(x=spawn[0], y=spawn[1]), destinations=destinations)
    (OUTPUT / "navigation.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{columns} x {row_count} cells, {len(reachable)} reachable from spawn, "
          f"{len(destinations)} reachable destinations")


if __name__ == "__main__":
    main()
