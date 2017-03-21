from kivy.app import App
import os
import math

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
from ctypes import windll
from kivy.config import Config

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout

from rendering.custom_uix.custom_button import CustomButton
from rendering.custom_uix.custom_navbar import CustomNavbar

# Window.size = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


class GalaxyViewer(Widget):  # singleton
	navbar = ObjectProperty()

	def __init__(self, **kwargs):
		super(GalaxyViewer, self).__init__(**kwargs)
		self.size = Window.size[0], Window.size[1]

	def on_load(self):
		pass

	def resize(self, width, height):
		self.size = width, height


class GalaxyNavbar(CustomNavbar):  # Singleton
	open_close_menu = ObjectProperty()
	empire_menu = ObjectProperty()
	system_menu = ObjectProperty()
	gap_widget = ObjectProperty()
	galaxy_view = ObjectProperty()
	system_view = ObjectProperty()

	def __init__(self, **kwargs):
		super(GalaxyNavbar, self).__init__(**kwargs)

	def toggle_menu(self):
		self.parent.toggle_menu_app()


class GameMenu(RelativeLayout):  # Singleton
	box_layout = ObjectProperty(None)
	test_button = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(GameMenu, self).__init__(**kwargs)
		window_size = Window.size
		self.border = 20
		self.navbar_height = 50

		self.visible = True
		self.resize(window_size[0], window_size[1])

	def on_load(self):
		pass

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
		else:
			self.pos = Window.size


class ConstellationWidget(Widget):  # Singleton/Wrapper for all objects
	galaxy_viewer = ObjectProperty(None)
	galaxy_navbar = ObjectProperty(None)
	game_menu = ObjectProperty(None)

	def on_load(self, *args):
		for child in self.children:
			try:
				child.on_load()
			except AttributeError:
				pass

	def toggle_menu_app(self):
		self.game_menu.reposition(True)


class ConstellationApp(App):  # Singleton/app class.
	constellation_widget = ObjectProperty(None)

	def window_resize(self, window, width, height):
		self.constellation_widget.game_menu.resize(width, height)
		self.constellation_widget.galaxy_viewer.resize(width, height)
		self.constellation_widget.galaxy_navbar.reset_navbar_spacing(width)

	def build(self):
		Window.bind(on_resize=self.window_resize)
		self.constellation_widget = ConstellationWidget()

		return self.constellation_widget

	def on_start(self):
		print('Window Size', Window.size)
		Clock.schedule_once(self.constellation_widget.on_load, )

if __name__ == '__main__':
	LabelBase.register(name="Roboto",
					   fn_regular="sources/font/Roboto/Roboto-Light.ttf",
					   fn_italic="sources/font/Roboto/Roboto-LightItalic.ttf",
					   fn_bold="sources/font/Roboto/Roboto-Medium.ttf",
					   fn_bolditalic="sources/font/Roboto/Roboto-MediumItalic.ttf")
	ConstellationApp().run()
