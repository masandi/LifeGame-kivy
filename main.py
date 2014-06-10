#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.config import Config


class Cell(Widget):
    status = NumericProperty(0)
    rule = [['die', 'die', 'die', 'live', 'die', 'die', 'die', 'die', 'die'],
            ['die', 'die', 'live', 'live', 'die', 'die', 'die', 'die', 'die']]

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.neighborhood = []
        self.next_status = 0

    def on_status(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            Color(*(value ^ 1,) * 3)
            Rectangle(size=self.size, pos=self.pos)

    def reload(self):
        self.status = self.next_status

    def live(self):
        self.next_status = 1

    def die(self):
        self.next_status = 0

    def evolve(self):
        total = sum((cell.status for cell in self.neighborhood))
        return getattr(self, self.rule[self.status][total])()

    def set_neighborhood(self, grid_pos, grid):
        for x_offset, y_offset in itertools.product(range(-1, 2), repeat=2):
            try:
                self.neighborhood.append(
                        grid[grid_pos[1] + y_offset][grid_pos[0] + x_offset])
            except IndexError: continue
        self.neighborhood.remove(self)


class CellGrid(GridLayout):
    steps = NumericProperty(0)

    def reload(self, dt):
        for cell in self.children: cell.evolve()
        for cell in self.children: cell.reload()
        self.steps += 1

    def clear(self):
        for cell in self.children: cell.status = 0
        self.steps = 0

    def build(self):
        for i in range(self.rows * self.cols): self.add_widget(Cell())
        #Transform 2d grid
        grid = [list(reversed(self.children[self.cols*i:self.cols*(i+1)]))
                for i in reversed(range(self.rows))]
        for y in range(self.rows):
            for x in range(self.cols):
                grid[y][x].set_neighborhood((x, y), grid)


class LifeGame(BoxLayout):
    cellgrid = ObjectProperty(None)

    def start(self, interval):
        self.pause()
        Clock.schedule_interval(self.cellgrid.reload, interval)

    def pause(self):
        Clock.unschedule(self.cellgrid.reload)

    def reset(self):
        self.pause()
        self.cellgrid.clear()


class LifeGameApp(App):
    use_kivy_settings = False

    def build_config(self, config):
        config.read(self.get_application_config())

    def build_settings(self, settings):
        settings.add_json_panel(
                "Conway's Life Game", self.config,
                filename="./lifegame_panel.json")

    def build(self):
        lifegame = LifeGame()
        lifegame.cellgrid.build()
        return lifegame


if __name__ == '__main__':
    #Fixed window
    Config.set('graphics', 'width', 1024)
    Config.set('graphics', 'height', 768)
    Config.set('graphics', 'resizable', 0)

    LifeGameApp().run()

