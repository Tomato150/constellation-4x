from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.properties import ObjectProperty

import random
import math


class GalaxyViewer(ScatterLayout):  # singleton
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyViewer, self).__init__(**kwargs)
        self.galaxy = None
        self.old = None

    def on_load(self, app, window):
        self.size = (6000*32), (6000*32)
        self.center = [window.size[0]/2, window.size[1]/2]
        window.bind(on_resize=self.resize)

    def resize(self, window, *args):
        pass

    def load_stars(self, galaxy):
        self.galaxy = galaxy
        count = 0
        textures = {
            'Blue Dwarf': [Image(source='sources/images/stars/B_D_1.png').texture],
            'Blue Giant': [Image(source='sources/images/stars/B_G_1.png').texture],
            'Blue Main': [Image(source='sources/images/stars/B_M_1.png').texture],
            'Red Dwarf': [Image(source='sources/images/stars/R_D_1.png').texture],
            'Red Giant': [Image(source='sources/images/stars/R_G_1.png').texture],
            'Red Main': [Image(source='sources/images/stars/R_M_1.png').texture],
            'Red Super Giant': [Image(source='sources/images/stars/R_SG_1.png').texture],
            'Yellow Main': [Image(source='sources/images/stars/Y_M_1.png').texture]
        }
        with self.canvas.before:
            for star in self.galaxy.world_objects['stars'].values():
                Rectangle(
                    texture=random.choice(textures[star.star_type]),
                    pos=(star.coordinates[0] * 32 + (3000*32), star.coordinates[1] * 32 + (3000*32)),
                    size=[32, 32]
                )
                count += 1
                if count % 10000 == 0:
                    print(count)

    def on_touch_down(self, touch):
        self.old = touch.pos
        if touch.device == 'mouse':
            if touch.button == 'scrollup':
                self.scroll_on_galaxy('zoom_out', touch)
            elif touch.button == 'scrolldown':
                self.scroll_on_galaxy('zoom_in', touch)
            elif touch.button == 'left':
                mouse_pos = [
                    math.floor((-self.pos[0] + touch.pos[0]) / 32) - 3000,
                    math.floor((-self.pos[1] + touch.pos[1]) / 32) - 3000
                ]
                for star in self.galaxy.world_objects['stars'].values():
                    if star.coordinates == mouse_pos:
                        # Do stuff with star
                        break

    def scroll_on_galaxy(self, scroll_type, touch):
        old_scale = self.scale

        percent_from_edge_x = ((-self.pos[0] + touch.pos[0]) - (-self.pos[0] + self.center[0])) / (3200 * self.scale)
        percent_from_edge_y = ((-self.pos[1] + touch.pos[1]) - (-self.pos[1] + self.center[1])) / (3200 * self.scale)

        if scroll_type == 'zoom_in':
            self.scale = min(2, self.scale + 0.1)
        elif scroll_type == 'zoom_out':
            self.scale = max(0.1, self.scale - 0.1)

        if not -0.05 < (self.scale - old_scale) < 0.05:  # I.E., If it has changed.
            if scroll_type == 'zoom_in':
                self.center = [
                    self.center_x - (percent_from_edge_x * 320),
                    self.center_y - (percent_from_edge_y * 320)
                ]
            elif scroll_type == 'zoom_out':
                self.center = [
                    self.center_x + (percent_from_edge_x * 320),
                    self.center_y + (percent_from_edge_y * 320)
                ]

    def on_touch_move(self, touch):
        if touch.device == 'mouse':
            if touch.button == 'middle':
                self.middle_mouse_drag(touch)

    def middle_mouse_drag(self, touch):
        if self.old is None:
            self.old = touch.pos
        change = (
            (touch.pos[0] - self.old[0]),
            (touch.pos[1] - self.old[1])
        )
        self.pos = (
            (self.pos[0] + change[0]),
            (self.pos[1] + change[1])
        )
        self.old = touch.pos

    def on_touch_up(self, touch):
        self.old = None
