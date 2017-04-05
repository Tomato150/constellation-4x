"""
The galaxy_navbar file, hosts relevant classes.
"""

from rendering.custom_uix.custom_navbar import CustomNavbar
from kivy.properties import ObjectProperty


class GalaxyNavbar(CustomNavbar):
    """
    A named widget, the GalaxyNavbar provides a navbar to the GalaxyViewer widget, with unique functionality past the
    base CustomNavbar class.
    """
    open_close_menu = ObjectProperty()
    empire_menu = ObjectProperty()
    system_menu = ObjectProperty()
    gap_widget = ObjectProperty()
    galaxy_view = ObjectProperty()
    system_view = ObjectProperty()

    def __init__(self, **kwargs):
        """
        initialisation for the widget, creating components necessary for it.

        :param kwargs: Any keyword args to pass back to the parent class.
        """
        super(GalaxyNavbar, self).__init__(**kwargs)
        self.ui_events = dict()

    def on_load(self, app, window):
        """
        Creates necessary bindings and other information that couldn't be created during init due to the .KV file

        :param app: Kivy App
        :param window: Kivy Window object
        """
        super(GalaxyNavbar, self).on_load(app, window)
        # TODO Implement this into every class, for communication to the base widget.
        self.ui_events = {
            'toggle_GameMenu': self.parent.ui_events['toggle_GameMenu']
        }
