from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window


class GameMenu(BoxLayout):  # Singleton
    custom_navbar_game_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameMenu, self).__init__(**kwargs)
        self.border = 20
        self.navbar_height = 50
        self.visible = True

    def on_load(self, app, window):
        self.resize(window)
        window.bind(on_resize=self.resize)

    # TODO which is then recived from the base widgets here.
    def toggle_menu(self, window=Window, *args):
        if self.visible:
            self.visible = False
        else:
            self.visible = True

        for child in self.children:
            self.children_visibility_loop(child)
        self.resize(window)

        print(self.pos)

    def resize(self, window, *args):
        self.size = window.width - self.border * 2, window.height - (self.border * 2 + self.navbar_height)

        if self.visible:
            self.pos = self.border, self.border
        else:
            self.pos = window.size

    def children_visibility_loop(self, widget):
        try:
            widget.toggle_visibility(self.visible)
        except AttributeError as e:
            print(e)
        for child in widget.children:
            self.children_visibility_loop(child)
