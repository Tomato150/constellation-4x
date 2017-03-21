from kivy.uix.stacklayout import StackLayout


class CustomNavbar(StackLayout):
	def __init__(self, **kwargs):
		super(CustomNavbar, self).__init__(**kwargs)

	def on_load(self):
		for child in self.children:
			try:
				child.on_load()
			except AttributeError:
				pass
		self.resize()
		self.reset_navbar_spacing(self.width)

	def reset_navbar_spacing(self, width):
		self.width = width
		widget_sizes = 0
		gap_widget = None
		extra_widgets_overflow = 0
		for child in self.children:
			print('With Child:', child.name)
			try:
				if child.gap_widget:
					print('Assigned as gap widget')
					gap_widget = child
					continue
			except AttributeError:
				if gap_widget is None:
					print('Added to extention widget')
					extra_widgets_overflow += child.width
				print('Added to total widget sizes')
				widget_sizes += child.width
			print('+-----------------------------------------------------+')
		print('Gap Widget Width =', self.width, '-', widget_sizes)
		gap_widget.width = self.width - widget_sizes


	def resize(self):
		self.size = self.parent.width, 50
		self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]