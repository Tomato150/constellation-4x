from kivy.uix.stacklayout import StackLayout


class CustomNavbar(StackLayout):
	def __init__(self, **kwargs):
		super(CustomNavbar, self).__init__(**kwargs)

	def on_load(self):
		pass

	def reset_navbar_spacing(self, width):
		self.width = width
		widget_sizes = self.empire_menu.width + self.system_menu.width + self.galaxy_view.width + self.system_view.width
		if widget_sizes < self.width:
			self.gap_widget.width = self.width - widget_sizes - (self.galaxy_view.width + self.system_view.width) + 32
		else:
			self.gap_widget.width = 0

	def resize(self):
		self.size = self.parent.width, 50
		self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]