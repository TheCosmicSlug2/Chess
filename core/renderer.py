import pygame as pg
from settings import FPS
from core.textures import get_texture_dic
from core.audio_manager import MixerPlay
from core.utils import color_clamp, get_dtuple, add_tuples
from widgets.widgets import *

# Type Hinting
from core.cst_manager import CstManager
from core.data_manager import DataManager

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DARK_TILE = (115,149,82)
LIGHT_TILE = (235,236,208)

class Renderer:
    def __init__(self, cst_manager: CstManager):
        pg.init()
        self.cstman = cst_manager
        self.DISPLAY = pg.display.set_mode((self.cstman.SCREENDIMS), pg.RESIZABLE)
        pg.display.set_caption("Chess Window")
        self.CLOCK = pg.time.Clock()
        self.dic_textures = {}
        self.load_textures()
        
        self.ennemy_animation = {
            "tick": 0,
            "piece": None,
            "current": None,
            "end": None,
            "dpos": None
        }
        self.fonts = {}
        self.menu_bg = None

    def add_font(self, height):
        self.fonts[height] = pg.font.SysFont("Times New Roman", height)

    def set_window_title(self, title: str):
        pg.display.set_caption(title)

    @property
    def on_oppopent_animation(self):
        return self.ennemy_animation["tick"] > 0
    
    @staticmethod
    def get_fullscreen_dims():
        info = pg.display.Info()
        return (info.current_w, info.current_h)
    
    @staticmethod
    def get_cell(gridpos, dims):
        x = dims[0] * gridpos[0]
        y = dims[1] * gridpos[1]
        return pg.Rect((x, y), dims)
    
    def draw_cell(self, gridpos, color):
        square = self.get_cell(gridpos, self.cstman.cell_dims)
        pg.draw.rect(self.DISPLAY, color, square)
    
    def resize_display(self):
        self.DISPLAY = pg.display.set_mode(self.cstman.SCREENDIMS, pg.RESIZABLE)
    
    def go_fullscreen(self):
        pg.display.set_mode((0, 0), pg.FULLSCREEN)
    
    def load_textures(self):
        self.dic_textures = get_texture_dic(self.cstman.cell_dims)
    
    def setup_opponent_animation(self, pos1, pos2, piece):
        dpos = get_dtuple(pos1, pos2)
        t = 8
        dpos = (dpos[0] / t, dpos[1] / t)
        self.ennemy_animation = {
            "tick": t,
            "piece": piece,
            "current": pos1,
            "end": pos2,
            "dpos": dpos
        }

    # Widgets
    def get_widget_render(self, widget):
        # Get main surface
        width, height = widget.dims
        tot_borx = 0
        tot_borh = 0
        outer_surface = pg.Surface(widget.dims, pg.SRCALPHA)
        for color, border in zip(widget.colors, widget.borders):
            width = width - 2 * border
            height = height - 2 * border
            tot_borx += border
            tot_borh += border
            inner_surface = pg.Surface((width, height), pg.SRCALPHA)
            inner_surface.fill(color)
            outer_surface.blit(inner_surface, (tot_borx, tot_borh))
        if isinstance(widget, Label) or isinstance(widget, Button):
            if widget.text_height not in self.fonts:
                self.add_font(widget.text_height)
            font = self.fonts[widget.text_height]
            text_render = font.render(widget.text, False, widget.text_color, widget.text_bg_color)
            
            half_x = (widget.width - text_render.get_width()) / 2
            half_y = (widget.height - text_render.get_height()) / 2
            outer_surface.blit(text_render, (half_x, half_y))
        if isinstance(widget, Checkbox):
            inner_surface.fill(widget.check_color)
            outer_surface.blit(inner_surface, (tot_borx, tot_borh))
        return outer_surface
    
    def render_on_screen(self, datamas: DataManager, mouse_pos):
        mouse_gridpos = self.cstman.get_gridpos(mouse_pos)
        # Board render
        for row in range(8):
            for column in range(8):
                if datamas.color == "w":
                    color = LIGHT_TILE if (row + column) % 2 == 0 else DARK_TILE
                else:
                    color = LIGHT_TILE if (row + column) % 2 == 1 else DARK_TILE

                if datamas.selected_piece_pos == (column, row):
                    color = color_clamp(color, 50)
                if (column, row) == mouse_gridpos:
                    color = color_clamp(color, 20)
                self.draw_cell((column, row), color)

        # Opponent ending position
        if self.on_oppopent_animation:
            self.draw_cell(self.ennemy_animation["end"], (200, 200, 0))
        
        # Check positions colors
        check_positions = []
        for item in datamas.check_data.values():
            if isinstance(item, tuple):
                check_positions.extend(item)
            else:
                check_positions.append(item)
        for gridpos in check_positions:
            if not gridpos:
                continue
            self.draw_cell(gridpos, (200, 0, 0))
        
        # Unmoving Pieces
        for row in range(8):
            for column in range(8):
                # Opponent animation ignored
                if self.on_oppopent_animation and (column, row) == self.ennemy_animation["end"]:
                    continue
                # Grabbed piece ignored
                if (column, row) == datamas.selected_piece_pos:
                    continue
                piece = datamas.get_at((column, row))
                if piece is None:
                    continue
                piece_pos = (column * self.cstman.cell_width, row * self.cstman.cell_height)
                self.DISPLAY.blit(self.dic_textures[piece], (piece_pos))
        
        for pos in datamas.possible_moves:
            half_width = self.cstman.cell_width // 2
            half_height = self.cstman.cell_height // 2
            wrapper = pg.Rect(
                pos[0] * self.cstman.cell_width + half_width // 2,
                pos[1] * self.cstman.cell_height + half_height // 2,
                half_width,
                half_height
            )
            ellipse_surf = pg.Surface((wrapper.width, wrapper.height), pg.SRCALPHA)
            pg.draw.ellipse(ellipse_surf, (0, 0, 0, 100), ellipse_surf.get_rect())
            self.DISPLAY.blit(ellipse_surf, (wrapper.x, wrapper.y))
        
        if datamas.selected_piece_pos:
            piece = datamas.get_at(datamas.selected_piece_pos)
            piece_pos = (mouse_pos[0] - self.cstman.cell_width // 2, mouse_pos[1] - self.cstman.cell_height // 2)
            self.DISPLAY.blit(self.dic_textures[piece], piece_pos)
        
        # Ennemy animation
        if self.on_oppopent_animation:
            self.DISPLAY.blit(
                self.dic_textures[self.ennemy_animation["piece"]],
                (
                    self.ennemy_animation["current"][0] * self.cstman.cell_width,
                    self.ennemy_animation["current"][1] * self.cstman.cell_height
                ))
            self.ennemy_animation["current"] = add_tuples(
                self.ennemy_animation["current"],
                self.ennemy_animation["dpos"]
            )
            self.ennemy_animation["tick"] -= 1
            if not self.on_oppopent_animation:
                MixerPlay(1)

        # Finally, cursor sprites
        if datamas.selected_piece_pos:
            # closed hand
            pg.mouse.set_visible(False)
            visible_pos = (mouse_pos[0] - 8, mouse_pos[1] - 8)
            self.DISPLAY.blit(self.dic_textures["grab"], visible_pos)
        elif datamas.get_color_at(mouse_gridpos) == datamas.color:
            # Open hand
            pg.mouse.set_visible(True)
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_visible(True)
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
    

    def get_menu_bg(self):
        new_dims = self.cstman.SCREENDIMS[0] + 20, self.cstman.SCREENDIMS[0] + 20
        surface = pg.Surface(new_dims)
        cell_width = new_dims[0] // 16
        cell_height = new_dims[1] // 16
        for row_idx in range(16):
            for column_idx in range(16):
                dcenter = ((8-row_idx)**2 + (8-column_idx)**2) / 1.5
                cell = pg.Rect(column_idx * cell_width, row_idx * cell_height, cell_width, cell_height)
                color = (245,249,222) if (row_idx + column_idx) % 2 == 0 else (185,219,152)
                color = color_clamp(color, -dcenter)
                pg.draw.rect(surface, color, cell)
        return surface

    def render_menu(self, widgets):
        if not self.menu_bg:
            self.menu_bg = self.get_menu_bg()
        self.DISPLAY.blit(self.menu_bg, (-10, -10))
        for widget in widgets:
            self.DISPLAY.blit(widget.surface, widget.pos)
    
    def update_display(self):
        pg.display.flip()
        self.CLOCK.tick(FPS)

