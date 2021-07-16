import random

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
        # velocity_x = NumericProperty(0)
        # velocity_y = NumericProperty(0)
        # velocity = ReferenceListProperty(velocity_x, velocity_y)

    def graphical_pos_attach(self):
        self.graphical_pos = (self.actual_pos[0] - self.graphical_size[0] / 2,
                              self.actual_pos[1] - self.graphical_size[1] / 2)

    def move_to(self, x, y):
        self.actual_pos = (x, y)
        self.graphical_pos_attach()

    def move_by(self, x, y, **kwargs):
        self.move_to(self.actual_pos[0] + x, self.actual_pos[1] + y, **kwargs)

    def get_pos(self):
        return self.actual_pos

    def step_by(self, direction, **kwargs):
        self.move_by(self.actual_size[0] * direction[0],
                     self.actual_size[1] * direction[1],
                     **kwargs)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Worm(Widget):
    def __init__(self, config):
        super().__init__()
        self.cells = []
        self.config = config
        self.cell_size = config.CELL_SIZE
        self.head_init((100,100))
        for i in range(config.DEFAULT_LENGTH):
            self.lengthen()

    def destroy(self):
        for i in range(len(self.cells)):
            self.remove_widget(self.cells[i])
        self.cells = []

    def lengthen(self, pos=None, direction=(0,1)):
        if pos is None:
            px = self.cells[-1].get_pos()[0] + direction[0] * self.cell_size
            py = self.cells[-1].get_pos()[1] + direction[1] * self.cell_size
            pos = (px, py)
        self.cells.append(Cell(*pos, self.cell_size, margin=self.config.MARGIN))
        self.add_widget(self.cells[-1])

    def head_init(self, pos):
        self.lengthen(pos=pos)

    def move(self, direction):
        for i in range(len(self.cells)-1, 0, -1):
            self.cells[i].move_to(*self.cells[i-1].get_pos())
        self.cells[0].step_by(direction)




class Form(Widget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.worm = None
        self.cur_dir = (0,0)
        self.fruit = None

    def random_cell_location(self, offset):
        x_row = self.size[0] // self.config.CELL_SIZE
        x_col = self.size[1] // self.config.CELL_SIZE
        return random.randint(offset, x_row - offset), \
               random.randint(offset, x_col - offset)

    def random_location(self, offset):
        x_row, x_col = self.random_cell_location(offset)
        return self.config.CELL_SIZE * x_row, self.config.CELL_SIZE * x_col

    def fruit_dislocate(self):
        x, y = self.random_location(2)
        self.fruit.move_to(x, y)

    def start(self):
        self.fruit = Cell(0,0, self.config.APPLE_SIZE, self.config.MARGIN)
        self.worm = Worm(self.config)
        self.fruit_dislocate()
        self.add_widget(self.worm)
        self.add_widget(self.fruit)
        self.cur_dir = (1, 0)
        Clock.schedule_interval(self.update, self.config.INTERVAL)

    def update(self, _):
        # for cell in self.cells:
        #     # cell.pos = (cell.pos[0] + 2, cell.pos[1] + 3)
        #     if not hasattr(cell, "velocity"):
        #         cell.velocity = Vector(3,0).rotate(randint(0,360))
        #     cell.move()
        self.worm.move(self.cur_dir)


    def on_touch_down(self, touch):
        ws = touch.x / self.size[0]
        hs = touch.y / self.size[1]
        aws = 1 - ws
        if ws > hs and aws > hs:
            cur_dir = (0, -1)  # Down
        elif ws > hs >= aws:
            cur_dir = (1, 0)  # Right
        elif ws <= hs < aws:
            cur_dir = (-1, 0)  # Left
        else:
            cur_dir = (0, 1)  # Up
        self.cur_dir = cur_dir

class WormApp(App):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.form = Form(self.config)

    def build(self):
        self.form.start()
        return self.form


if __name__ == '__main__':
    WormApp().run()