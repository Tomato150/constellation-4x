from kivy.uix.screenmanager import Screen
from rendering.custom_uix.custom_alert import create_alert

import game_code.game_data.constants.construction_constants as construction_constants


class IndustryWindow(Screen):
    def submit_construction_project(self, building_type, building_runs, factories):
        try:
            if building_type.lower() not in construction_constants.building_costs:
                raise Exception()
            int_runs = int(building_runs)
            int_factories = int(factories)
        except ValueError:
            create_alert(
                title="Field Submission Error",
                message="Invalid numbers given for runs/factories",
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
