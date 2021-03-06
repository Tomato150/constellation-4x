from game_code.game_logic.faction_objects import empires, colonies, construction_projects
from game_code.game_logic.stellar_objects import galaxies
from game_code.game_data.constants import construction_constants


#                                      Parent Colony of construction project
def start_construction_project(galaxy_instance: galaxies.Galaxy, target_object_ids, args):
    project_building = args['building']
    project_runs = args['runs']
    num_of_factories = args['num_of_factories']

    colony_instance = galaxy_instance.get_object_by_id('colony', target_object_ids, True)  # type: colonies.Colony

    construction_project = galaxy_instance.create_new_construction_project(project_building, project_runs,
                                                                           num_of_factories, colony_instance)

    return {
        'create': {
            'construction_projects': {construction_project.ids['self']: construction_project}
        }
    }
