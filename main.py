import player_world

from kivy.app import App
import os
import math

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from ctypes import windll
from kivy.config import Config

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

from rendering.custom_uix.custom_button import CustomButton
from rendering.custom_uix.custom_navbar import CustomNavbar
from rendering.custom_uix.custom_sidebar import CustomSidebar

from rendering.custom_uix.named.game_menu import GameMenu
from rendering.custom_uix.named.galaxy_navbar import GalaxyNavbar
from rendering.custom_uix.named.galaxy_viewer import GalaxyViewer

from rendering.styles.css_manager import CSSManager


# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

player_world = player_world.PlayerWorld()
player_world.generate_mock_game()

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.update()


class ConstellationWidget(Widget):  # Singleton/Wrapper for all objects
    galaxy_viewer = ObjectProperty(None)
    galaxy_navbar = ObjectProperty(None)
    game_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ConstellationWidget, self).__init__(**kwargs)
        self.css = CSSManager(self, True)
        # TODO after spits it back out to other widgets defind from here.
        self.ui_events = {
            'toggle_GameMenu': self.game_menu.toggle_menu
        }


class ConstellationApp(App):  # Singleton/app class.
    constellation_widget = ObjectProperty(None)

    def build(self):
        self.constellation_widget = ConstellationWidget()

        return self.constellation_widget

    def on_start(self):
        """
        Schedules an event for the next frame, allowing Kivy to finish it's load functions.
        """
        Clock.schedule_once(self.on_load, 0)

    def on_load(self, *args):
        """
        Arguments: Accepts no arguments.
        
        Completes the initialisation of Kivy apps once the .kv file has loaded all previous presets.
        
        Completes these functions in order:
        - self.load_styles()
        - self.update_and_apply_styles()
        - self.widgets_on_load()
        - ... galaxy_viewer.load_stars()
        - self.resize_widgets()
        """
        self.load_styles()
        self.update_and_apply_styles()
        self.widget_on_load()
        self.constellation_widget.galaxy_viewer.load_stars(player_world.galaxy.world_objects['stars'])
        print('Completed On Load')
        Clock.schedule_once(
            self.resize_widgets, 0
        )

    def resize_widgets(self, *args):
        """
        Arguments: Accepts no arguments.
        
        Fires a resize widget function for the clock.
        """
        self.resize_widgets()
        
    def load_styles(self, widget=None):
        """
        Keyword arguments:
        - widget=None: Takes a widget to cycle through.
        
        A recursive function that goes through and calls the load function for any CSS component it finds.
        """
        if widget is None:
            self.load_styles(self.constellation_widget)
        try:
            widget.css.load_styles()
        except AttributeError:
            pass
        for child in widget.children:
            self.load_styles(Window, child)
            
    def update_and_apply_styles(self, widget=None):
        if widget is None:
            self.load_styles(self.constellation_widget)
        try:
            widget.css.apply_styles()
        except AttributeError as e:
            print(e)
        for child in widget.children:
            self.update_and_apply_styles(child)
            
    def widget_on_load(self, widget=None):
        if widget is None:
            self.widget_on_load(self.constellation_widget)
        try:
            widget.on_load(app, window)
        except AttributeError:
            pass
        for child in widget.children:
            self.widget_on_load(child)
            
    def resize_widgets(self, widget=None):
        if widget is None:
            self.resize_widgets(self.constellation_widget)
        try:
            widget.resize(window, window.size[0], window.size[1])
        except AttributeError:
            pass
        for child in widget.children:
            self.resize_widgets(child)
        try:
            widget.resize(window, window.size[0], window.size[1])
        except AttributeError:
            pass


if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular="sources/font/Roboto/Roboto-Light.ttf",
        fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
        fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
        fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf"
    )
    ConstellationApp().run()
