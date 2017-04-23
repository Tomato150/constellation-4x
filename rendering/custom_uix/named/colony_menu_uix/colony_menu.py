from kivy.uix.screenmanager import Screen
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


class ColonyMenu(Screen):
    screen_manager_colony_menu = ObjectProperty(None)

    def handle_transition(self, screen_name):
        current_index = screen_order.index(self.screen_manager_colony_menu.current)
        given_index = screen_order.index(screen_name)
        if current_index > given_index:
            self.screen_manager_colony_menu.transition.direction = "right"
        else:
            self.screen_manager_colony_menu.transition.direction = "left"
        self.screen_manager_colony_menu.current = screen_name
