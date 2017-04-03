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
        self.size = 6400, 6400
        self.pos = -3200 + (window.size[0]/2), -3200 + (window.size[1]/2)
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
            star_image.mipmap = True
            self.add_widget(star_image)
            count += 1
            if count % 10000 == 0:
                print(count)

    def on_touch_down(self, touch):
        self.old = touch.pos
        if touch.device == 'mouse':
            if touch.button == 'scrollup':
                # Actually the equivalent of scrolling down a web page, and zooming out of game
                self.size = (self.size[0]/2), (self.size[1]/2)
                pass
            if touch.button == 'left':
                print('Dank meme')

    def on_touch_move(self, touch):
        if touch.device == 'mouse':
            if touch.button == 'middle':
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
        pass
