from rendering.custom_uix.custom_navbar import CustomNavbar
from kivy.properties import ObjectProperty


class GalaxyNavbar(CustomNavbar):  # Singleton
    open_close_menu = ObjectProperty()
    empire_menu = ObjectProperty()
    system_menu = ObjectProperty()
    gap_widget = ObjectProperty()
    galaxy_view = ObjectProperty()
    system_view = ObjectProperty()

    def __init__(self, **kwargs):
        super(GalaxyNavbar, self).__init__(**kwargs)
        self.ui_events = dict()

    def on_load(self, app, window):
        super(GalaxyNavbar, self).on_load(app, window)
        # TODO Implement this into every class, for communication to the base widget.
        self.ui_events = {
            'toggle_GameMenu': self.parent.ui_events['toggle_GameMenu']
        }
