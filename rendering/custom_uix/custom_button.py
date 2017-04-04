from kivy.uix.button import Button
import math

from rendering.styles.global_styles import colors, fonts
from rendering.styles.css_manager import CSSManager


class CustomButton(Button):
    """
    A custom button, allows to be placed in any other parent widget that can support it
    """
    local_styles = {
        'button': {

        },
        'link': {
            'background_color': colors['opaque'],
            'font_size': fonts['sizes']['standard'],
            'color': 'inherit'
        },
        'link_nav_header': {'font_size': fonts['sizes']['h5']},
        'primary': {'color': colors['primary']}
    }

    def __init__(self, **kwargs):
        """
        initialisation for the widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(CustomButton, self).__init__(**kwargs)
        self.css = CSSManager(self)
        self.up = True

    def on_load(self, app, window):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param window: Kivy Window object
        """
        window.bind(on_resize=self.resize)

    def resize(self, *args):
        """
        Resizes the widget appropriately for it's needs

        :param args: Deals with any arguments handed by the kivy binding.
        """
        self.texture_update()
        height = 50
        if self.parent.__class__.__name__ == 'CustomSidebar':
            height = self.texture_size[1] + 16
        self.size = self.texture_size[0] + 16, height

    def button_pressed(self):
        """
        A method that runs when the button receives a state change.
        """
        if self.up:
            self.up = False
            self.color = min(1, self.color[0] + 0.2), min(1, self.color[1] + 0.2), min(1, self.color[2] + 0.2), self.color[3]
        else:
            self.up = True
            self.color = self.css.styles['color']
