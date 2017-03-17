from kivy.app import App

from kivy.core.window import Window
from ctypes import windll
from kivy.config import Config

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from kivy.uix.widget import Widget

# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


class GalaxyViewer(Widget):
	pass


class GameMenu(Widget):
	box_layout = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(GameMenu, self).__init__(**kwargs)
		self.size = Window.size[0], Window.size[1]

	def resize(self, width, height):
		self.size = width, height

	def move_to_right(self, *args):
		print(self.box_layout.pos)
		self.box_layout.pos = self.box_layout.pos[0] + 10, self.box_layout .pos[1]
		print(self.box_layout.pos)
		print("Test for move to right function")


class ConstellationWidget(Widget):
	galaxy_viewer = ObjectProperty(None)
	game_menu = ObjectProperty(None)
	pass


class ConstellationApp(App):
	constellation_widget = ObjectProperty(None)

	def window_resize(self, window, width, height):
		self.constellation_widget.game_menu.resize(width, height)

	def build(self):
		Window.bind(on_resize=self.window_resize)
		self.constellation_widget = ConstellationWidget()

		return self.constellation_widget

if __name__ == '__main__':
	ConstellationApp().run()
