from widgets.widgets import *

DARK_TILE = (115,149,82)
LIGHT_TILE = (235,236,208)

MENU_WIDGETS = [
    Label(100, 70, 320, 100, "Main Menu", 40, (0, 0, 0), None, 
        [(95,129,62), (115,149,82), (155,189,122), (185,189,162), (215,216,188)], [5, 5, 5, 5]),
    Label(170, 200, 180, 50, "AI     ", 30, (0, 0, 0), None, 
        [(115,149,82), (155,189,122), (185,189,162)], [3, 3, 3]),
    Checkbox(185, 208, 35, 35, "ai", (155,229,122),
        [(100, 100, 100), (220, 220, 220)], [3, 3]),
    Label(170, 260, 180, 50, "Timer", 30, (0, 0, 0), None, 
        [(125,149,82), (155,189,122), (185,189,162)], [3, 3, 3]),
    Checkbox(185, 268, 35, 35, "timer", (155,229,122),
        [(100, 100, 100), (220, 220, 220)], [3, 3]),
    Button(160, 340, 200, 80, "PLAY", 30, (0, 0, 0), None, "play",
        [(95,129,62),(115,149,82), (155,189,122)], [4, 4, 4]),
]

# Choix :
# MENU PRINCIPAL
# IA : oui/non
# timer : oui/non

class WidgetManager:
    def __init__(self, widgets, renderer):
        self.widgets = widgets
        self.renderer = renderer
        self.focused_widget = None
    
    def update(self, mouse_pos):
        mousex, mousey = mouse_pos
        for widget in self.widgets:
            x1, x2, y1, y2 = widget.collision
            widget.need_animation = False
            if x1 < mousex < x2 and y1 < mousey < y2:
                self.focused_widget = widget
                widget.need_update = True
                widget.need_animation = True
            elif isinstance(widget, Button) or isinstance(widget, Checkbox):
                widget.need_update = True
    
    def update_widget_surfaces(self):
        for widget in self.widgets:
            if not widget.need_update:
                continue
            widget.animate()
            surface = self.renderer.get_widget_render(widget)
            widget.surface = surface
            widget.need_update = False
    
    def on_click(self):
        if not self.focused_widget:
            return None
        if isinstance(self.focused_widget, Checkbox):
            self.focused_widget.switch_state()
            return None
        if not isinstance(self.focused_widget, Button):
            return
        if self.focused_widget.return_value != "play":
            return
        # get dic
        dic = {}
        for widget in self.widgets:
            if isinstance(widget, Checkbox):
                dic[widget.value] = widget.state
        return dic
        

    