TRANSPARENT = (0, 0, 0, 255)

class Widget:
    def __init__(self,
                 posx,
                 posy,
                 width,
                 height,
                 colors=[TRANSPARENT],
                 borders=[1],
                ):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.colors = colors
        self.borders = borders
        self.surface = None
        self.need_update = True
        self.need_animation = False
    
    def animate(self): return
    
    @property
    def dims(self):
        return self.width, self.height
    
    @property
    def collision(self):
        return (self.posx, self.posx + self.width, self.posy, self.posy + self.height)

    @property
    def pos(self):
        return self.posx, self.posy
    
class Label(Widget):
    def __init__(self, posx, posy, width, height, text, text_height, text_color, text_bg_color,  colors=[TRANSPARENT], borders=[1]):
        super().__init__(posx, posy, width, height, colors, borders)
        self.text = text
        self.text_height = text_height
        self.text_color = text_color
        self.text_bg_color = text_bg_color

class Button(Label):
    def __init__(self, posx, posy, width, height, text, text_height, text_color, text_bg_color, return_value, colors=[TRANSPARENT], borders=[1]):
        super().__init__(posx, posy, width, height, text, text_height, text_color, text_bg_color, colors, borders)
        self.return_value = return_value
        self.current_grow = 0
        self.on_grow = False
    
    def animate(self):
        grow = self.need_animation
        max = 3
        if grow and self.current_grow >= max:
            return
        if not grow and self.current_grow <= 0:
            return
        
        sign = 1 if grow else -1

        dx = 3 * sign
        dy = 3 * sign
        self.posx -= dx 
        self.posy -= dy
        self.width += dx * 2
        self.height += dy * 2
        self.text_height += dx
        self.borders = [i + sign * 0.5 for i in self.borders]

        self.current_grow += sign
        
        self.need_update = True

class Checkbox(Widget):
    def __init__(self, posx, posy, width, height, value, active_color=(0, 0, 0), colors=[TRANSPARENT], borders=[1]):
        super().__init__(posx, posy, width, height, colors, borders)
        self.state = False
        self.value = value
        self.active_color = active_color
        self.check_color = colors[-1]
    
    def switch_state(self):
        self.state = not self.state
        self.check_color = self.active_color if self.state else self.colors[-1]
        self.need_update = True
    
    def animate(self):
        if self.state == True:
            return
        if self.need_animation:
            self.check_color = (200, 200, 200)
        else:
            self.check_color = self.colors[-1]