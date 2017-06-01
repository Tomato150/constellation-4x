"""
The galaxy_navbar file, hosts relevant classes.
"""

from kivy.core.window import Window
from rendering.custom_uix.custom_navbar import CustomNavbar
from kivy.properties import ObjectProperty

months = {
    '1': 'Jan',
    '2': 'Feb',
    '3': 'Mar',
    '4': 'Apr',
    '5': 'May',
    '6': 'Jun',
    '7': 'Jul',
    '8': 'Aug',
    '9': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}


class GalaxyNavbar(CustomNavbar):
    """
    A named widget, the GalaxyNavbar provides a navbar to the GalaxyViewer widget, with unique functionality past the
    base CustomNavbar class.
    """
    open_close_menu = ObjectProperty()
    empire_menu = ObjectProperty()
    system_menu = ObjectProperty()
    gap_widget = ObjectProperty()
    game_time_widget = ObjectProperty()

    def handle_menu_transition(self, menu_name):
        game_menu = self.parent.game_menu
        game_menu.screen_manager_game_menu.current = menu_name

        Window.dispatch("on_resize", 0, 0)

    def update_game_time(self, game_time):
        self.game_time_widget.text = "Time: " + str(game_time.day) + '-' + months[str(game_time.month)] + '-' + str(game_time.year)

        Window.dispatch("on_resize", 0, 0)
