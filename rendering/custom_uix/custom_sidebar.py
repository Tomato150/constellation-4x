from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle
from rendering.styles.css_manager import CSSManager


class CustomSidebar(StackLayout):
    local_styles = {
        'sidebar_light': {
            'canvas_color': (0.9, 0.9, 0.9, 0.7),
            'color': (0.1, 0.1, 0.1, 1)
        },
        'sidebar_dark': {
            'canvas_color': (0.1, 0.1, 0.1, 0.7),
            'color': (0.9, 0.9, 0.9, 1)
        }
    }

    def __init__(self, **kwargs):
        super(CustomSidebar, self).__init__(**kwargs)
        self.style_classes = []
        self.css = CSSManager(self)
        self.background_canvas = None

    def on_load(self, app, window):
        print("CALLED THE ON LOAD")
        window.bind(on_resize=self.resize)
        self.background_canvas = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def resize(self, *args):
        print('Called a dank meme')
        print(self.parent.height, self.parent.width)
        self.height = self.parent.height
        self.pos = self.parent.pos
        self.resize_canvas()

    def resize_canvas(self):
        self.background_canvas.pos = self.pos
        self.background_canvas.size = self.size
