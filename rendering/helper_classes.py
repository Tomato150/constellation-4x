from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


class CanvasEnabled:
    """
    An abstract class that allows for implementation of a 'background canvas' to any widget.
    """
    def __init__(self, widget):
        """
        Sets up a property for the canvas to reside in 
        """
        self.background_canvas = None
        self.widget = widget

    def on_load(self):
        with self.widget.canvas.before:
            Color(*self.widget.canvas_color)
            self.background_canvas = Rectangle(size=self.widget.size, pos=self.widget.pos)

    def background_canvas_resize(self, *args):
        """
        Resizes the background canvas for the widget
        
        :param args: Deals with the arguments given from the Clock scheduling.
        """
        self.background_canvas.pos = self.widget.pos
        self.background_canvas.size = self.widget.size
