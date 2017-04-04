from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
from rendering.styles.css_manager import CSSManager


class CustomNavbar(StackLayout):
    """
    A custom navbar widget for use in any other parent widget.
    """
    local_styles = {
        'navbar_light': {
            'canvas_color': (0.9, 0.9, 0.9, 0.9),
            'color': (0.1, 0.1, 0.1, 1)
        },
        'navbar_dark': {
            'canvas_color': (0, 0, 0, 0.9),
            'color': (0.9, 0.9, 0.9, 1)
        }
    }

    def __init__(self, **kwargs):
        """
        initialisation for the widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(CustomNavbar, self).__init__(**kwargs)
        self.style_classes = []
        self.css = CSSManager(self)
        self.background_canvas = None

    def on_load(self, app, window):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param window: Kivy Window object
        """
        window.bind(on_resize=self.resize)
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def resize(self, *args):
        """
        Resizes the widget appropriately for it's needs

        :param args: Deals with any arguments handed by the kivy binding.
        """
        self.background_canvas.size = self.size = self.parent.width, 50
        self.background_canvas.pos = self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]
        widget_sizes = 0
        gap_widget = None
        for child in self.children:
            try:
                if child.gap_widget:
                    gap_widget = child
                    continue
            except AttributeError:
                widget_sizes += child.width

        gap_widget_size = self.width - widget_sizes
        if gap_widget_size >= 0:
            gap_widget.width = gap_widget_size
        else:
            # TODO Make the thing here for that drop down navbar
            pass

    def toggle_visibility(self, visibility):
        """
        Toggles the visibility of widget, clearing away the canvas as well if it's present.

        :param visibility: What state the visibility is in from the parent widget.
        """
        if visibility:
            self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]
        else:
            self.pos = 5000, 5000
        self.background_canvas.pos = self.pos

