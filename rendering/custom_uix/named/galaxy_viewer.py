from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty


class GalaxyViewer(ScatterLayout):  # singleton
    navbar = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyViewer, self).__init__(**kwargs)
        self.stars_dict = None
        self.old = None

    def on_load(self, app, window):
        self.size = (6000*32), (6000*32)
        self.center = [window.size[0]/2, window.size[1]/2]
        window.bind(on_resize=self.resize)

    def resize(self, window, *args):
        pass

    def load_stars(self, stars_dict):
        self.stars_dict = stars_dict
        count = 0
        for star in self.stars_dict.values():
            star_image = Image(
                source=star.file_path,
                pos=(star.coordinates[0] * 32 + (3000*32), star.coordinates[1] * 32 + (3000*32)),
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
                self.scroll_on_galaxy('zoom_out', touch)
            elif touch.button == 'scrolldown':
                self.scroll_on_galaxy('zoom_in', touch)
            elif touch.button == 'left':
                pass

    def scroll_on_galaxy(self, scroll_type, touch):
        old_scale = self.scale

        percent_from_edge_x = ((-self.pos[0] + touch.pos[0]) - (-self.pos[0] + self.center[0])) / (3200 * self.scale)
        percent_from_edge_y = ((-self.pos[1] + touch.pos[1]) - (-self.pos[1] + self.center[1])) / (3200 * self.scale)

        if scroll_type == 'zoom_in':
            self.scale = min(2, self.scale + 0.1)
        elif scroll_type == 'zoom_out':
            self.scale = max(0.1, self.scale - 0.1)

        if not -0.05 < (self.scale - old_scale) < 0.05:  # I.E., If it has changed.
            if scroll_type == 'zoom_in':
                self.center = [
                    self.center_x - (percent_from_edge_x * 320),
                    self.center_y - (percent_from_edge_y * 320)
                ]
            elif scroll_type == 'zoom_out':
                self.center = [
                    self.center_x + (percent_from_edge_x * 320),
                    self.center_y + (percent_from_edge_y * 320)
                ]

    def on_touch_move(self, touch):
        if touch.device == 'mouse':
            if touch.button == 'middle':
                self.middle_mouse_drag(touch)

    def middle_mouse_drag(self, touch):
        if self.old is None:
            self.old = touch.pos
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
        self.old = None
