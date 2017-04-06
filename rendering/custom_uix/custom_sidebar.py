"""
The CustomSidebar file, hosts the CustomSidebar class.
"""

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from kivy.uix.stacklayout import StackLayout

from rendering.helper_classes import background_canvas_resize, handle_visibility
from rendering.styles.css_manager import CSSManager


class CustomSidebar(StackLayout):
    """
    A custom sidebar widget, for use in any other parent widget
    """
    local_styles = {
        'sidebar_light': {
            'canvas_color': (0.9, 0.9, 0.9, 0.9),
            'color': (0.1, 0.1, 0.1, 1)
        },
        'sidebar_dark': {
            'canvas_color': (0, 0, 0, 0.9),
            'color': (0.9, 0.9, 0.9, 1)
        }
    }

    def __init__(self, **kwargs):
        """
        initialisation for the widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(CustomSidebar, self).__init__(**kwargs)
        self.style_classes = []
        self.css = CSSManager(self)
        self.background_canvas = None
        self.visibility = True

    def on_load(self):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param window: Kivy Window object
        """
        Window.bind(on_resize=self.resize)
        self.background_canvas = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def resize(self, *args):
        """
        Resizes the widget appropriately for it's needs

        :param args: Deals with any arguments handed by the kivy binding.
        """
        self.height = self.parent.height
        self.pos = self.parent.pos

        Clock.schedule_once(self.background_canvas_resize, 0)

    def toggle_visibility(self, visibility):
        """
        Toggles the visibility of widget, clearing away the canvas as well if it's present.

        :param visibility: What state the visibility is in from the parent widget.
        """
        if visibility:
            self.resize()
        else:
            self.background_canvas.pos = self.pos = 5000, 5000

CustomSidebar.background_canvas_resize = background_canvas_resize
