from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


class CanvasEnabled:
    """
    An abstract class that allows for implementation of a 'background canvas' to any widget.
    """
    def __init__(self):
        """
        Sets up a property for the canvas to reside in 
        """
        self.background_canvas = None

    def on_load(self):
        with self.canvas.before:
            Color(*self.canvas_color)
            self.background_canvas = Rectangle(size=self.size, pos=self.pos)

    def toggle_visibility(self, visibility):
        """
        Switches the visibility of the object.
        
        :param visibility: What state of visibility it should take.
        """
        if visibility:
            self.resize()
        else:
            self.pos = Window.size

        Clock.schedule_once(self.background_canvas_resize, 0)

    def background_canvas_resize(self, *args):
        """
        Resizes the background canvas for the widget
        
        :param args: Deals with the arguments given from the Clock scheduling.
        """
        self.background_canvas.pos = self.pos
        self.background_canvas.size = self.size
