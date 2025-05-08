import pygame as pg
from pathlib import Path

DEFAULT_FOLDER = r"rsc\textures\pieces\01_classic"

def get_texture_dic(size, folder=DEFAULT_FOLDER):
    names = {
        "king": '1',
        "queen": "2",
        "pawn": "3",
        "bishop": "4",
        "knight": "5",
        "rook": "6",
    }
    dic_textures = {}
    path = Path(folder)
    png_files = list(path.glob("*.png"))
    for png_file in png_files:
        filename = png_file.name.lower()
        texture = pg.transform.scale(pg.image.load(png_file), size)
        color = "w" if "W" in png_file.name else "b"
        for key, value in names.items():
            if key in filename:
                dic_textures[value + color] = texture
    return dic_textures

