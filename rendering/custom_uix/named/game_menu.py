"""
The game_menu file, hosts the relevant class.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock


class GameMenu(BoxLayout):
    """
    A named widget, the GameMenu hosts the game's main menu, and handles all relevant events to it.
    """
    custom_navbar_game_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        initialisation for the widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(GameMenu, self).__init__(**kwargs)
        self.border = 20
        self.navbar_height = 50
        self.visible = True

    def on_load(self, app, window):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param window: Kivy Window object
        """
        self.resize(window)
        window.bind(on_resize=self.resize)

    def toggle_menu(self, window=Window, *args):
        """
        Toggles the visibility of the widget, and recursively for all it's children.

        :param window: = Window, The kivy window object
        :param args: Present to deal with anything kivy throws at it.
        """
        if self.visible:
            self.visible = False
        else:
            self.visible = True

        self.resize(window)
        Clock.schedule_once(self.run_children_loop, -1)

    def resize(self, *args):
        """
        Resizes the widget appropriately for it's needs

        :param args: Deals with any arguments handed by the kivy binding.
        """
        self.size = Window.width - self.border * 2, Window.height - (self.border * 2 + self.navbar_height)

        if self.visible:
            self.pos = self.border, self.border
        else:
            self.pos = Window.size

    def run_children_loop(self, *args):
        for child in self.children:
            self.children_visibility_loop(child)

    def children_visibility_loop(self, widget):
        """
        Recursive function to hide the widget and all it's children

        :param widget: The widget it is currently looping over.
        """
        try:
            widget.toggle_visibility(self.visible)
        except AttributeError as e:
            print(e)
        self.run_children_loop()
