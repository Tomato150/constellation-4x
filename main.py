from kivy.app import App

from kivy.core.window import Window
from ctypes import windll

from kivy.properties import NumericProperty

from kivy.uix.widget import Widget

Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


class ConstellationWidget(Widget):
    pass


class ConstellationApp(App):
    def build(self):
        return ConstellationWidget()

if __name__ == '__main__':
    ConstellationApp().run()
