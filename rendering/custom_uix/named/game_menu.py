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

    def on_load(self):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param window: Kivy Window object
        """
        self.resize(Window)
        Window.bind(on_resize=self.resize)

    def toggle_menu(self, *args):
        """
        Toggles the visibility of the widget, and recursively for all it's children.

        :param args: Present to deal with anything kivy throws at it.
        """
        if self.visible:
            self.visible = False
        else:
            self.visible = True

        self.resize(Window)

        Clock.schedule_once(self.toggle_children_visibility, -1)

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

    def toggle_children_visibility(self, *args):
        """
        the beginning function for a recursive function that loops through all children and hides them.
        
        :param args: Handles Kivy clock args.
        """
        self.__toggle_children_visibility()

    def __toggle_children_visibility(self, widget=None):
        """
        A recursive function that toggles the visibility of every child widget.
        
        :param widget: = None, clean method for starting on self.
        :return: 
        """
        if widget is None:
            widget = self
        try:
            widget.toggle_visibility(self.visible)
        except AttributeError as e:
            print(e)
        for child in widget.children:
            self.__toggle_children_visibility(child)
