"""
The game_menu file, hosts the relevant class.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class GameMenu(BoxLayout):
    """
    A named widget, the GameMenu hosts the game's main menu, and handles all relevant events to it.
    """
    screen_manager_game_menu = ObjectProperty(None)
    game_menu_sidebar = ObjectProperty(None)

    def update_sidebar(self, system):
        for planet in system.planets.values():
            for colony_id, colony in planet.colonies.items():
                pass
