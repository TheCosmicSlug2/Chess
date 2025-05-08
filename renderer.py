import pygame as pg
from settings import FPS
from random import randint
from textures import get_texture_dic


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DARK_TILE = (115,149,82)
LIGHT_TILE = (235,236,208)

class Renderer:
    def __init__(self, cst_manager):
        pg.init()
        self.cstman = cst_manager
        self.DISPLAY = pg.display.set_mode((self.cstman.SCREENDIMS), pg.RESIZABLE)
        pg.display.set_caption("Chess Window")
        self.CLOCK = pg.time.Clock()
        self.dic_textures = {}
        self.load_textures()
    
    @staticmethod
    def get_fullscreen_dims():
        info = pg.display.Info()
        return (info.current_w, info.current_h)
    
    @staticmethod
    def get_cell(gridpos, dims):
        x = dims[0] * gridpos[0]
        y = dims[1] * gridpos[1]
        return pg.Rect((x, y), dims)
    
    def resize_display(self):
        self.DISPLAY = pg.display.set_mode(self.cstman.SCREENDIMS, pg.RESIZABLE)
    
    def go_fullscreen(self):
        pg.display.set_mode((0, 0), pg.FULLSCREEN)
    
    def load_textures(self):
        self.dic_textures = get_texture_dic(self.cstman.cell_dims)
    
    def render_on_screen(self, datamas):
        self.DISPLAY.fill(RED)
        for row in range(8):
            for column in range(8):
                color = LIGHT_TILE if (row + column) % 2 == 1 else DARK_TILE
                check_positions = []
                for item in datamas.check_data.values():
                    if isinstance(item, tuple):
                        check_positions.extend(item)
                    else:
                        check_positions.append(item)
                if (column, row) in check_positions:
                    color = (200, 0, 0)

                if datamas.selected_piece == (column, row):
                    color = color_clamp((color[0] + 50, color[1] + 50, color[2] + 50))

                square = self.get_cell((column, row), self.cstman.cell_dims)
                pg.draw.rect(self.DISPLAY, color, square)

                piece = datamas.get_at((column, row))
                if piece is None:
                    continue

                self.DISPLAY.blit(self.dic_textures[piece], (column * self.cstman.cell_width, row * self.cstman.cell_height))
    
    def update_display(self):
        pg.display.flip()
        self.CLOCK.tick(FPS)

def color_clamp(color):
    """Force chaque composante R, G, B à rester entre 0 et 255."""
    r = min(max(0, color[0]), 255)
    g = min(max(0, color[1]), 255)
    b = min(max(0, color[2]), 255)
    return (r, g, b)