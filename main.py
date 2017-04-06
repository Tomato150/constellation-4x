"""
The main file to host the Kivy app.
"""

import player_world

from kivy.app import App
import os
import math

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from ctypes import windll
from kivy.config import Config

from kivy.properties import ObjectProperty

from kivy.uix.widget import Widget

from rendering.custom_uix.custom_button import CustomButton
from rendering.custom_uix.custom_navbar import CustomNavbar
from rendering.custom_uix.custom_sidebar import CustomSidebar

from rendering.custom_uix.named.game_menu import GameMenu
from rendering.custom_uix.named.galaxy_navbar import GalaxyNavbar
from rendering.custom_uix.named.galaxy_viewer import GalaxyViewer

from rendering.custom_uix.named.menu_uix.industry_tab import IndustryTab

from rendering.styles.css_manager import CSSManager


# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

player_world = player_world.PlayerWorld()
player_world.generate_mock_game()

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.update()


class ConstellationWidget(Widget):  # Singleton/Wrapper for all objects
    """
    A singleton class that gets returned as the base widget in the kivy app
    """
    galaxy_viewer = ObjectProperty(None)
    galaxy_navbar = ObjectProperty(None)
    game_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        initialisation for the base widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(ConstellationWidget, self).__init__(**kwargs)
        self.css = CSSManager(self, True)

class ConstellationApp(App):
    """
    A singleton class that is the app for the entire kivy project.
    """
    constellation_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        The base init function, to create properties for the app

        :param kwargs: Keyword args to pass into super function
        """
        super(ConstellationApp, self).__init__(**kwargs)
        self.ui_events = dict()

    def build(self):
        """
        Builds the app, loading the window. Fires the local on_start method
        """
        self.constellation_widget = ConstellationWidget()

        return self.constellation_widget

    def on_start(self):
        """
        Schedules an event for the next frame, allowing Kivy to finish it's load functions.
        """
        Clock.schedule_once(self.on_load, 0)

    def on_load(self, *args):
        """
        Starts the recursive functions to handle creating and initialising objects

        :param args: Handles any args given by the Kivy Clock scheduling.
        """
        self.load_styles()
        self.update_and_apply_styles()
        self.widget_on_load()
        Clock.schedule_once(self.delayed_on_load, 0)

        self.ui_events['toggle_game_menu'] = self.constellation_widget.game_menu.toggle_menu

        print('Completed On Load')

    def delayed_on_load(self, *args):
        """
        Other on loads that need to be called a frame in advance

        :param args:
        """
        self.resize_widgets()
        self.constellation_widget.galaxy_viewer.load_stars(player_world.galaxy)

    def load_styles(self, widget=None):
        """
        recursive function to load all the styles into each widget's CSS component.

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.load_styles(self.constellation_widget)
            return
        try:
            widget.css.load_styles()
        except AttributeError as e:
            print(e)
        for child in widget.children:
            self.load_styles(child)
            
    def update_and_apply_styles(self, widget=None):
        """
        recursive function to reload any special keywords (inherit, etc.) with their actual values, and then applies all
        the data needed.

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.update_and_apply_styles(self.constellation_widget)
            return
        try:
            widget.css.apply_styles()
        except AttributeError as e:
            print(e)
        for child in widget.children:
            self.update_and_apply_styles(child)
            
    def widget_on_load(self, widget=None):
        """
        recursive function to fire the widget's on_load functions.

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.widget_on_load(self.constellation_widget)
            return
        try:
            widget.on_load(self, Window)
        except AttributeError:
            pass
        for child in widget.children:
            self.widget_on_load(child)
            
    def resize_widgets(self, widget=None):
        """
        Recursive function to allow for resizing widgets in a correct manner

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.resize_widgets(self.constellation_widget)
            return
        for child in widget.children:
            self.resize_widgets(child)
        try:
            widget.resize()
        except AttributeError:
            pass


if __name__ == '__main__':
    LabelBase.register(
        name="Roboto",
        fn_regular="sources/font/Roboto/Roboto-Light.ttf",
        fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
        fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
        fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf"
    )
    ConstellationApp().run()
