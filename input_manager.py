import pygame as pg


# Events :
QUIT = 1
VIDEORESIZE = 2
CTRL = 10
F = 11
LEFTCLICK = 12

class InputManager:
    def __init__(self, cst_manager):
        self.cstmana = cst_manager
        self.last_events = {}
    
    def get_pg_events(self):
        current_events = {}
        for event in pg.event.get():
            if event.type == pg.QUIT:
                current_events[QUIT] = True
            if event.type == pg.VIDEORESIZE:
                current_events[VIDEORESIZE] = event.size
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    current_events[LEFTCLICK] = event.pos
        
        desired_keys = {
            pg.K_LCTRL: CTRL,
            pg.K_RCTRL: CTRL,
            pg.K_f: F
        }
        keys = pg.key.get_pressed()
        for key, value in desired_keys.items():
            if keys[key]:
                current_events[value] = True
        
        
        return current_events