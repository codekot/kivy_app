from random import randint

from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector

class Config:
    DEFAULT_LENGTH = 20
    CELL_SIZE = 25
    APPLE_SIZE = 35
    MARGIN = 4
    INTERVAL = 0.2
    DEAD_CELL = (1,0,0,1)
    APPLE_COLOR = (1,1,0,1)


class Cell(Widget):
    graphical_size = ListProperty([1,1])
    graphical_pos = ListProperty([1,1])

    def __init__(self, x, y, size, margin=4):
        super().__init__()
        self.actual_size = (size, size)
        self.graphical_size = (size - margin, size - margin)
        self.margin = margin
        self.actual_pos = (x, y)
        self.graphical_pos_attach()
        velocity_x = NumericProperty(0)
        velocity_y = NumericProperty(0)
        velocity = ReferenceListProperty(velocity_x, velocity_y)

    def graphical_pos_attach(self):
        self.graphical_pos = (self.actual_pos[0] - self.graphical_size[0] / 2,
                              self.actual_pos[1] - self.graphical_size[1] / 2)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Form(Widget):
    def __init__(self):
        super().__init__()
        self.cell1 = Cell(100,100,30)
        self.cell2 = Cell(130,100,30)
        self.add_widget(self.cell1)
        self.add_widget(self.cell2)
        # self.cells = []

    def start(self):
        Clock.schedule_interval(self.update, 0.01)

    def update(self, _):
        # for cell in self.cells:
        #     # cell.pos = (cell.pos[0] + 2, cell.pos[1] + 3)
        #     if not hasattr(cell, "velocity"):
        #         cell.velocity = Vector(3,0).rotate(randint(0,360))
        #     cell.move()
        pass


    # def on_touch_down(self, touch):
    #     cell = Cell(touch.x, touch.y, 30)
    #     self.add_widget(cell)
    #     self.cells.append(cell)

class WormApp(App):
    def build(self):
        self.form = Form()
        self.form.start()
        return self.form


if __name__ == '__main__':
    WormApp().run()