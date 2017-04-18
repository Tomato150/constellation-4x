from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class IndustryWindow(BoxLayout):
    def on_load(self):
        Window.bind(on_resize=self.resize)
        self.resize()

    def resize(self, *args):
        height = 0
        for child in self.children:
            height += child.height
        self.size = self.size[0], height
        self.top = self.parent.top
        print("WOWOWOWOWOWOWOWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

    def dank(self):
        print("wow")
