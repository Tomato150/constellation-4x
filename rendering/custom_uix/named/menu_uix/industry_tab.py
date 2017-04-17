"""
The Industry tab for the game menu
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from game_code.game_data.constants.construction_constants import building_costs


class IndustryTab(BoxLayout):
    """
    The industry tab class, found in the game menu hierarchy
    """
    def submit_construction_project_details(self, building_type, building_runs, buildings_factories, colony_instance):
        from main import get_app
        if building_type in building_costs:
            get_app().player_world.galaxy.create_new_construction_project(building_type,
                                                                          building_runs,
                                                                          buildings_factories,
                                                                          colony_instance)
