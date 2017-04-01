from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
from rendering.styles.css_manager import CSSManager


class CustomSidebar(StackLayout):
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
        super(CustomSidebar, self).__init__(**kwargs)
        self.style_classes = []
        self.css = CSSManager(self)
        self.background_canvas = None
        self.visibility = True

    def on_load(self, app, window):
        window.bind(on_resize=self.resize)
        self.background_canvas = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def resize(self, *args):
        print(self.parent.height, self.parent.width)
        self.height = self.parent.height
        self.pos = self.parent.pos
        self.background_canvas.size = self.size
        self.background_canvas.pos = self.pos
        print('CANVAS POS:', self.background_canvas.pos)

    def toggle_visibility(self, visibility):
        if visibility:
            self.resize()
        else:
            self.background_canvas.pos = self.pos = 5000, 5000
