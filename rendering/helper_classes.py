from kivy.clock import Clock
from kivy.core.window import Window


def handle_visibility(self, visibility):
    if visibility:
        self.resize()
    else:
        self.pos = Window.size

    Clock.schedule_once(self.background_canvas_resize, 0)


def background_canvas_resize(self, *args):
    """
    Resizes the background canvas for the navbar
    
    :param args: Deals with the arguments given from the Clock scheduling.
    """
    self.background_canvas.pos = self.pos
    self.background_canvas.size = self.size
