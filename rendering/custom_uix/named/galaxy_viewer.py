from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class GalaxyViewer(Widget):  # singleton
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyViewer, self).__init__(**kwargs)

    def on_load(self, app, window):
        self.size = window.size[0], window.size[1]
        window.bind(on_resize=self.resize)

    def resize(self, window, *args):
        self.size = window.size
