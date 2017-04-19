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

    def handle_menu_transition(self, menu_name):
        self.parent.game_menu.screen_manager_game_menu.current = menu_name
