from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

screen_order = [
    'overview',
    'economy',
    'industry',
    'fleets',
    'population',
    'politics',
    'diplomacy',
    'research'
]


class ColonyMenu(BoxLayout):
    ScrMan_colony_menu = ObjectProperty(None)

    def handle_transition(self, screen_name):
        current_index = screen_order.index(self.screen_manager_game_menu.current)
        given_index = screen_order.index(screen_name)
        if current_index > given_index:
            self.screen_manager_game_menu.transition.direction = "right"
        else:
            self.screen_manager_game_menu.transition.direction = "left"
        self.screen_manager_game_menu.current = screen_name
