from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty


class GalaxyViewer(RelativeLayout):  # singleton
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyViewer, self).__init__(**kwargs)
        self.stars_dict = None
        self.old = (0, 0)

    def on_load(self, app, window):
        self.size = 6000, 6000
        self.pos = -3000, -3000
        window.bind(on_resize=self.resize)

    def resize(self, window, *args):
        pass

    def load_stars(self, stars_dict):
        self.stars_dict = stars_dict
        count = 0
        for star in self.stars_dict.values():
            star_image = Image(
                source=star.file_path,
                pos=(star.coordinates[0] * 32 + 3032, star.coordinates[1] * 32 + 3032),
                size=(32, 32), size_hint=(None, None)
            )
            star_image.nocache = True
            star_image.mipmap = False
            self.add_widget(star_image)
            count += 1
            if count % 10000 == 0:
                print(count)

    def on_touch_down(self, touch):
        self.old = touch.pos
        print('touched down')
        if touch.device == 'mouse' and touch.button == 'scrollup':
            # Actually the equivalent of scrolling down a web page
            print('WOWOWOWOWOW UP IT GOES')

    def on_touch_move(self, touch):
        print('Touched moved')
        if touch.device == 'mouse' and touch.button == 'middle':
            self.middle_mouse_drag(touch)

    def middle_mouse_drag(self, touch):
        change = (
            (touch.pos[0] - self.old[0]),
            (touch.pos[1] - self.old[1])
        )
        self.pos = (
            (self.pos[0] + change[0]),
            (self.pos[1] + change[1])
        )
        self.old = touch.pos

    def on_touch_up(self, touch):
        self.mouse_pos = False
        print('Touch Up')
