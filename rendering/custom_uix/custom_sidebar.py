from kivy.uix.stacklayout import StackLayout

from rendering.styles.css_manager import CSSManager


class CustomSidebar(StackLayout):
    def __init__(self, **kwargs):
        super(CustomSidebar, self).__init__(**kwargs)
        self.css = CSSManager(self)

    def on_load(self, app, window):
        print("CALLED THE ON LOAD")
        window.bind(on_resize=self.resize)

    def resize(self, *args):
        print('Called a dank meme')
        self.height = self.parent.height
        self.pos = self.parent.pos
