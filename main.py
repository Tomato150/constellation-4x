"""
The main file to host the Kivy app.
"""

# PLAYER WORLD MODULE. HOLDS THE GAME STATE
import player_world as pw

# OTHER CUSTOM MODULES
from utils import observers

# REQUIRED FOR SAVING AND LOADING
import jsonpickle

# KIVY DEPENDENCIES
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

# CUSTOM KIVY WIDGETS. INCLUDE ALL AS KIVY USES THEM TO ASSIGN CLASSES TO WIDGETS IN .KV FILE
from rendering.custom_uix.custom_button import CustomButton
from rendering.custom_uix.custom_label import CustomLabel
from rendering.custom_uix.custom_navbar import CustomNavbar
from rendering.custom_uix.custom_sidebar import CustomSidebar
from rendering.custom_uix.custom_table import CustomTable

from rendering.custom_uix.named.game_menu import GameMenu
from rendering.custom_uix.named.galaxy_navbar import GalaxyNavbar
from rendering.custom_uix.named.galaxy_viewer import GalaxyViewer

from rendering.custom_uix.named.empire_menu_uix.empire_menu import EmpireMenu

from rendering.custom_uix.named.system_menu_uix.system_menu import SystemMenu

from rendering.custom_uix.named.colony_menu_uix.colony_menu import ColonyMenu
from rendering.custom_uix.named.colony_menu_uix.industry_window import IndustryWindow

# RENDERING CUSTOM MODULES
from rendering.styles.css_manager import CSSManager


save_file_path = "savegames/%s.sav"


# Config.set('graphics', 'width', windll.user32.GetSystemMetrics(0))
# Config.set('graphics', 'height', windll.user32.GetSystemMetrics(1))

# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'left', 0)
# Config.set('graphics', 'top', 0)

# Config.set('graphics', 'borderless', 0)
# Config.set('graphics', 'resizeable', 0)

Config.set('graphics', 'fullscreen', '0')

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.write()


class ConstellationWidget(Widget):  # Singleton/Wrapper for all objects
    """
    A singleton class that gets returned as the base widget in the kivy app
    """
    galaxy_viewer = ObjectProperty(None)
    galaxy_navbar = ObjectProperty(None)
    game_menu = ObjectProperty(None)
    screen_manager_constellation_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        initialisation for the base widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(ConstellationWidget, self).__init__()
        self.menu_visible = True
        self.css = CSSManager(self, True)
        self.screen_manager_constellation_widget.current = 'game_menu'

    def transition_screen(self):
        screen_manager = self.screen_manager_constellation_widget
        if screen_manager.current == 'game_menu':
            screen_manager.current = 'blank_screen'
            self.menu_visible = False
        else:
            screen_manager.current = 'game_menu'
            self.menu_visible = True

    def open_menu_screen(self):
        self.screen_manager_constellation_widget.current = 'game_menu'
        self.menu_visible = True


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
        self.constellation_widget = None
        self.player_world = pw.PlayerWorld()
        self.player_world.generate_mock_game()

        self.previous_timestamp = 0
        self.counter = 0

        self.render_notification = observers.Subject('render')

        # Game UI info
        self._current_colony = self.player_world.player_empire.colonies['capital']
        self.current_colony_changed = observers.Subject('current_colony_changed')

        self._current_system = self._current_colony.parent_planet.parent_star
        self.current_system_changed = observers.Subject('current_system_changed')

    @property
    def current_colony(self):
        return self._current_colony

    @current_colony.setter
    def current_colony(self, value):
        if value != self._current_colony:
            self._current_colony.unhook_all()
            self._current_colony = value
            self.current_colony_changed.notify(data={'current_colony': self._current_colony})

    @property
    def current_system(self):
        return self._current_system

    @current_system.setter
    def current_system(self, value):
        if value != self._current_system:
            self._current_system.unhook_all()
            if self._current_colony:
                self._current_colony.unhook_all()

            self._current_system = value
            self._current_colony = None

            self.constellation_widget.game_menu.update_sidebar(value)

            self.current_system_changed.notify(data={'current_system': self._current_system})

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
        self.widgets_on_load()
        Clock.schedule_once(self.delayed_on_load, 0)

        # Must be defined here, I think.
        self.ui_events['toggle_game_menu'] = self.constellation_widget.transition_screen

        print('Completed On Load')

    def delayed_on_load(self, *args):
        """
        Other on loads that need to be called a frame in advance

        :param args:
        """
        self.resize_widgets()
        self.constellation_widget.galaxy_viewer.load_stars(self.player_world.galaxy)
        Clock.schedule_once(self.game_loop)

    def game_loop(self, time_delta):
        self.previous_timestamp += time_delta
        if self.previous_timestamp >= 1:
            self.player_world.update_game_state_by_day()
            self.constellation_widget.galaxy_navbar.update_game_time(self.player_world.game_time)
            self.previous_timestamp -= 1
            print(self.counter)
            self.counter = 0
        else:
            self.counter += 1
        self.render_notification.notify()
        Clock.schedule_once(self.game_loop)

    def widgets_on_load(self, widget=None):
        """
        recursive function to load all the styles into each widget's CSS component.

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.widgets_on_load(self.constellation_widget)
            return

        try:
            widget.on_load()
        except AttributeError as e:
            print(e)

        if hasattr(widget, 'screens'):
            for child in widget.screens:
                self.widgets_on_load(child)
        else:
            for child in widget.children:
                self.widgets_on_load(child)

    def resize_widgets(self, widget=None):
        """
        Recursive function to allow for resizing widgets in a correct manner

        :param widget: = None, allows for recursion through widgets, and also set to none to allow for targeting the
        constellation_widget if not otherwise specified.
        """
        if widget is None:
            self.resize_widgets(self.constellation_widget)
            return

        if hasattr(widget, 'screens'):
            for child in widget.screens:
                self.resize_widgets(child)
        else:
            for child in widget.children:
                self.resize_widgets(child)

        try:
            widget.resize()
        except AttributeError:
            pass

    # TODO need to patch these up for implementation.
    def load_game(self, save_name):
        save_file = save_name + '.sav'
        with open(save_file, 'r') as savefile:
            unpickled_world = jsonpickle.decode(''.join(line.rstrip() for line in savefile))
        self.player_world = unpickled_world
        print("Game loaded")

    def save_game(self, save_name):
        pickled_world = jsonpickle.encode(self)
        save_file = save_name + '.sav'
        with open(save_file, 'w') as savefile:
            savefile.write(pickled_world)
        print("Save Completed, File Name:", save_file)

if __name__ == '__main__':
    LabelBase.register(
        name="Roboto",
        fn_regular="sources/font/Roboto/Roboto-Light.ttf",
        fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
        fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
        fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf"
    )
    ConstellationApp().run()
