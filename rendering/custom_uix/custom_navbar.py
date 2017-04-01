from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
from rendering.styles.css_manager import CSSManager


class CustomNavbar(StackLayout):
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
        super(CustomNavbar, self).__init__(**kwargs)
        self.style_classes = []
        self.css = CSSManager(self)
        self.background_canvas = None

    def on_load(self, app, window):
        window.bind(on_resize=self.resize)
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def resize(self, *args):
        print(self.name)
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
        print('Gap Widget Width =', self.width, '-', widget_sizes, '=', gap_widget.width)

    def toggle_visibility(self, visibility):
        if visibility:
            self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]
        else:
            self.pos = 5000, 5000
        self.background_canvas.pos = self.pos

