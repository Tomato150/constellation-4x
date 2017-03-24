from kivy.uix.stacklayout import StackLayout
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Rectangle
from rendering.styles.css_manager import CSSManager


class CustomNavbar(StackLayout):
	local_styles = {
		'navbar_light': {
			'canvas_color': (0.5, 0.5, 0.5, 0.5),
			'color': (0.1, 0.1, 0.1, 1)
		},
		'navbar_dark': {
			'canvas_color': (0, 0, 1, 1),
			'color': (0.9, 0.9, 0.9, 1)
		}
	}

	def __init__(self, **kwargs):
		super(CustomNavbar, self).__init__(**kwargs)
		self.style_classes = []
		self.css = CSSManager(self)

	def on_load(self, app, window):
		window.bind(on_resize=self.resize)
		try:
			with self.canvas.before:
				Color(*self.canvas_color)
				Rectangle(size=self.size, pos=self.pos)
		except Exception as e:
			print('CANVAS ERROR:', e)

	def resize(self, *args):
		print(self.name)
		self.resize_navbar()
		widget_sizes = 0
		gap_widget = None
		for child in self.children:
			try:
				if child.gap_widget:
					gap_widget = child
					continue
			except AttributeError:
				widget_sizes += child.width

		gap_widget_size = self.width - widget_sizes
		if gap_widget_size >= 0:
			gap_widget.width = gap_widget_size
		else:
			# TODO Make the thing here for that drop down navbar
			pass
		print('Gap Widget Width =', self.width, '-', widget_sizes, '=', gap_widget.width)

	def toggle_visibility(self, visibility):
		if visibility:
			self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]
		else:
			self.pos = 5000, 5000
		self.toggle_canvas_visibility(visibility)

	def resize_navbar(self):
		self.canvas.before.children[2].size = self.size = self.parent.width, 50
		self.canvas.before.children[2].pos = self.pos = self.parent.pos[0], self.parent.height - self.height + self.parent.pos[1]

	def toggle_canvas_visibility(self, visibility):
		if visibility:
			self.canvas.before.children[2].pos = self.pos
		else:
			self.canvas.before.children[2].pos = 5000, 5000
