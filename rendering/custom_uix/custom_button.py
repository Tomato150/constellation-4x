from kivy.uix.button import Button
import math

from rendering.styles.global_styles import colors, fonts
from rendering.styles.css_manager import CSSManager


def fourthroot(num):
    return math.sqrt(math.sqrt(num))


class CustomButton(Button):
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
        super(CustomButton, self).__init__(**kwargs)
        self.css = CSSManager(self)
        self.up = True

    def on_load(self, app, window):
        pass

    def resize(self, *args):
        self.texture_update()
        self.size = self.texture_size[0] + 16, self.parent.height

    def button_pressed(self):
        print(self.color)
        if self.up:
            self.up = False
            self.color = fourthroot(self.color[0]), fourthroot(self.color[1]), fourthroot(self.color[2]), self.color[3]
        else:
            self.up = True
            self.color = self.color[0] ** 4, self.color[1] ** 4, self.color[2] ** 4, self.color[3]
        print(self.color)
