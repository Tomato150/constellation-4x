"""
The Industry tab for the game menu
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class IndustryTab(BoxLayout):
    """
    The industry tab class, found in the game menu hierarchy
    """
    def __init__(self, **kwargs):
        """
        IndustryTab's init function, calls super and initialises the relevant properties

        :param kwargs: Keyword arguments to pass into super function
        """
        super(IndustryTab, self).__init__(**kwargs)

    def on_load(self, *args):
        Window.bind(on_resize=self.resize)

    def resize(self, *args):
        pass

    def toggle_visibility(self, visibility):
        if visibility:
            self.resize()
        else:
            self.pos = Window.size
