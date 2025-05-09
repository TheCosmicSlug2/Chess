import pygame as pg


# Events :
QUIT = 1
VIDEORESIZE = 2
CTRL = 10
F = 11
LEFTCLICK = 12
LEFTCLICK_RELEASE = 13

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
                    current_events[LEFTCLICK] = self.clamp_screen(event.pos)
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    current_events[LEFTCLICK_RELEASE] = self.clamp_screen(event.pos)
        
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

    def clamp_screen(self, pos):
        x, y = pos
        x = max(0, min(x, self.cstmana.SCREENDIMS[0] - 1))
        y = max(0, min(y, self.cstmana.SCREENDIMS[1] - 1))
        return (x, y)

    
    def get_mouse_pos(self):
        return self.clamp_screen(pg.mouse.get_pos())