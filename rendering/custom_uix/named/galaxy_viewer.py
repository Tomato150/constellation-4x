"""
The GalaxyViewer file, hosts the class
"""

import random
import math

from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty

from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout


class GalaxyViewer(ScatterLayout):
    """
    A named widget, the GalaxyViewer hosts all the stars from the game world, and handles events from it.
    """
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        """
        Init for the galaxy canvas, creating any components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(GalaxyViewer, self).__init__(**kwargs)
        self.galaxy = None
        self.old = None
        self.load_complete = False

    def on_load(self):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param Window: Kivy Window object
        """
        self.size = (6000*32), (6000*32)
        self.center = [Window.size[0] / 2, Window.size[1] / 2]

    def load_stars(self, galaxy):
        """
        Loads and creates the stars from the player_world, and saves the galaxy reference to the local instance.

        :param galaxy: a Galaxy object, fully initialized and saved under a player_world.
        """
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
            'Yellow Main': [Image(source='sources/images/stars/Y_M_1.png').texture],
            'Star Blur': [Image(source='sources/images/experiment.png').texture]
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
        self.load_complete = True

    def on_touch_down(self, touch):
        """
        Handles Kivy on_touch_down event, currently for all mouse events

        :param touch: A Kivy touch object.
        """
        self.old = touch.pos
        if touch.device == 'mouse' and self.load_complete and not self.parent.game_menu.visible:
            if touch.button == 'scrollup':
                self.scroll_on_galaxy('zoom_out', touch)
            elif touch.button == 'scrolldown':
                self.scroll_on_galaxy('zoom_in', touch)
            elif touch.button == 'left':
                mouse_pos = [
                    math.floor((-self.pos[0] + touch.pos[0]) / 32) - 3000,
                    math.floor((-self.pos[1] + touch.pos[1]) / 32) - 3000
                ]
                found_star = False
                for star in self.galaxy.world_objects['stars'].values():
                    if star.coordinates == mouse_pos:
                        found_star = True
                        print('Found Star:', star.name, star.coordinates)
                        # Do stuff with star
                        break
                if not found_star:
                    print('Not found star')

    def scroll_on_galaxy(self, scroll_type, touch):
        """
        zooms the galaxy in and out due to a mouse scroll

        :param scroll_type: 'zoom_in' or 'zoom_out', depending on the necessary choice for the method
        :param touch: A Kivy touch object, allows to track the position of the mouse.
        """
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
        """
        Fires an event when the mouse is moved, while some button is pressed on the canvas

        :param touch: A kivy touch object, allows for tracking the mouse
        """
        if touch.device == 'mouse' and self.load_complete and not self.parent.game_menu.visible:
            if touch.button == 'middle':
                self.middle_mouse_drag(touch)

    def middle_mouse_drag(self, touch):
        """
        Allows for the panning of the mouse.

        :param touch: A Kivy touch event, allows for tracking the mouse.
        """
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
        """
        Resets the touch details for the next events

        :param touch: Kivy touch event. Handled due to the arg being passed
        """
        self.old = None
