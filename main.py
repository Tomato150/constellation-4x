from kivy.app import App

from kivy.core.window import Window
from ctypes import windll
from kivy.config import Config

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout

# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


class GalaxyViewer(Widget):
	navbar = ObjectProperty()

	def __init__(self, **kwargs):
		super(GalaxyViewer, self).__init__(**kwargs)
		self.size = Window.size[0], Window.size[1]

	def resize(self, width, height):
		self.size = width, height

	def toggle_menu(self):
		self.parent.toggle_menu_app()


class GameMenu(RelativeLayout):
	box_layout = ObjectProperty(None)
	test_button = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(GameMenu, self).__init__(**kwargs)
		window_size = Window.size
		self.border = 20
		self.navbar_height = 50

		self.visible = True
		self.resize(window_size[0], window_size[1])

	def resize(self, width, height):
		self.size = width - self.border * 2, height - (self.border * 2 + self.navbar_height)
		self.reposition()

	def reposition(self, change=False):
		if change:
			if self.visible:
				self.visible = False
			else:
				self.visible = True

		if self.visible:
			self.pos = self.border, self.border
		elif not self.visible:
			self.pos = Window.size


class ConstellationWidget(Widget):
	galaxy_viewer = ObjectProperty(None)
	game_menu = ObjectProperty(None)

	def toggle_menu_app(self):
		self.game_menu.reposition(True)


class ConstellationApp(App):
	constellation_widget = ObjectProperty(None)

	def window_resize(self, window, width, height):
		self.constellation_widget.game_menu.resize(width, height)
		self.constellation_widget.galaxy_viewer.resize(width, height)

	def build(self):
		Window.bind(on_resize=self.window_resize)
		self.constellation_widget = ConstellationWidget()

		return self.constellation_widget


if __name__ == '__main__':
	ConstellationApp().run()
