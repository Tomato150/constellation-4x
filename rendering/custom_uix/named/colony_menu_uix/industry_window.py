from kivy.uix.screenmanager import Screen
from rendering.custom_uix.custom_alert import create_alert

from utils import observers

import game_code.game_data.constants.construction_constants as construction_constants


class IndustryWindow(Screen, observers.Observer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_load(self, *args):
        self.app.current_colony_changed.add_observer(self)
        self.app.current_system_changed.add_observer(self)

    def on_notify(self, object, event, data):
        # GAME EVENTS
        if event == "construction_project_change":
            pass

        # APP EVENTS
        elif event == "current_colony_changed":
            colony = self.app.current_colony
            for construction_project in colony.construction_projects.items():
                construction_project.construction_changed.add_observer(self)
        elif event == "current_system_changed":
            pass

    def submit_construction_project(self, building_type, building_runs, factories):
        try:
            if building_type.lower() not in construction_constants.building_costs:
                raise Exception()
            int_runs = int(building_runs)
            int_factories = int(factories)
        except ValueError:
            create_alert(
                title="Field Submission Error",
                message="Fields did not receive their desired type.",
                separator_color=[0.851, 0.325, 0.31, 1]  # Warning
            )
            print("ERROR: IndustryWindow|submit_construction_project Error: Ints not given for runs/factories")
        except Exception:
            create_alert(
                title="Field Submission Error",
                message="Invalid building name given.",
                separator_color=[0.851, 0.325, 0.31, 1]  # Warning
            )
            print("ERROR: IndustryWindow|submit_construction_project Error: Invalid building name given.")
        else:
            self.app.player_world.galaxy.create_new_construction_project(
                project_building=building_type,
                flags=None,
                project_runs=int_runs,
                num_of_factories=int_factories,
                colony_instance=self.app.current_colony
            )
