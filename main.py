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

def load_styles(app, window, widget):
    try:
        widget.css.load_styles()
    except AttributeError:
        pass
    for child in widget.children:
        load_styles(app, window, child)


def update_and_apply_styles(app, window, widget):
    try:
        widget.css.apply_styles()
    except AttributeError as e:
        print(e)
    for child in widget.children:
        update_and_apply_styles(app, window, child)


def widget_on_load(app, window, widget):
    try:
        widget.on_load(app, window)
    except AttributeError:
        pass
    for child in widget.children:
        widget_on_load(app, window, child)


def resize_widgets(app, window, widget):
    try:
        widget.resize(window, window.size[0], window.size[1])
    except AttributeError:
        pass
    for child in widget.children:
        resize_widgets(app, window, child)
    try:
        widget.resize(window, window.size[0], window.size[1])
    except AttributeError:
        pass


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
        Clock.schedule_once(self.on_load, 0)

    def on_load(self, *args):
        load_styles(self, Window, self.constellation_widget)
        update_and_apply_styles(self, Window, self.constellation_widget)
        widget_on_load(self, Window, self.constellation_widget)
        print('Completed On Load')
        Clock.schedule_once(
            self.resize_widgets, 0
        )

    def resize_widgets(self, *args):
        resize_widgets(self, Window, self.constellation_widget)


if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular="sources/font/Roboto/Roboto-Light.ttf",
        fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
        fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
        fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf"
    )
    ConstellationApp().run()
