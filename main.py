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

from rendering.styles.css_manager import CSSManager


# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


# TODO Implement this when not a lazy fuck
def big_on_load(app, window, widget):
    load_styles(app, window, widget)
    update_and_apply_styles(app, window, widget)
    widget_on_load(app, window, widget)
    resize_widgets(app, window, widget)


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
    for child in widget.children:
        resize_widgets(app, window, child)
    try:
        widget.resize(window, window.size[0], window.size[1])
    except AttributeError:
        pass


class GalaxyViewer(Widget):  # singleton
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyViewer, self).__init__(**kwargs)
        self.size = Window.size[0], Window.size[1]

    def on_load(self, app, window):
        try:
            super(GalaxyViewer, self).on_load(app, window)
        except AttributeError:
            pass
        window.bind(on_resize=self.resize)

    def resize(self, window, width, height):
        self.size = window.size


class GalaxyNavbar(CustomNavbar):  # Singleton
    open_close_menu = ObjectProperty()
    empire_menu = ObjectProperty()
    system_menu = ObjectProperty()
    gap_widget = ObjectProperty()
    galaxy_view = ObjectProperty()
    system_view = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyNavbar, self).__init__(**kwargs)
        self.ui_events = dict()

    def on_load(self, app, window):
        super(GalaxyNavbar, self).on_load(app, window)
        # TODO Implement this into every class, for communication to the base widget.
        self.ui_events = {
            'toggle_GameMenu': self.parent.ui_events['toggle_GameMenu']
        }

    def toggle_game_menu(self):
        self.parent.toggle_menu()


class GameMenu(BoxLayout):  # Singleton
    custom_navbar_game_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameMenu, self).__init__(**kwargs)
        window_size = Window.size
        self.border = 20
        self.navbar_height = 50

        self.visible = True
        self.resize(None, window_size[0], window_size[1])

    def on_load(self, app, window):
        try:
            super(GameMenu, self).on_load(app, window)
        except AttributeError:
            pass
        window.bind(on_resize=self.resize)

    # TODO which is then recived from the base widgets here.
    def toggle_menu(self, window=Window, width=Window.size[0], height=Window.size[1]):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        self.resize(window, width, height)
        for child in self.children:
            try:
                child.toggle_visibility(self.visible)
            except AttributeError as e:
                print(e)

    def resize(self, window, width, height):
        self.size = width - self.border * 2, height - (self.border * 2 + self.navbar_height)

        if self.visible:
            self.pos = self.border, self.border
        else:
            self.pos = Window.size


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
        print('Window Size', Window.size)
        load_styles(self, Window, self.constellation_widget)
        update_and_apply_styles(self, Window, self.constellation_widget)
        widget_on_load(self, Window, self.constellation_widget)
        print('Completed On Load')
        resize_widgets(self, Window, self.constellation_widget)


if __name__ == '__main__':
    LabelBase.register(
        name="Roboto",
        fn_regular="sources/font/Roboto/Roboto-Light.ttf",
        fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
        fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
        fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf"
    )
    ConstellationApp().run()
