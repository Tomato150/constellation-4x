from utils import observers
import collections


colony_flags = {
    'capital': False
}


class Colony:
    def __init__(self, colony_id, name, flags, planet_instance, empire_instance, galaxy, **kwargs):
        # Colony Location and General information
        self.galaxy = galaxy
        self.name = name

        # Parents
        self.parent_empire = empire_instance
        self.parent_planet = planet_instance
        self.ids = {
            'self': colony_id,

            'star': planet_instance.ids['star'],
            'planet': planet_instance.ids['self'],

            'empire': empire_instance.ids['self']
        }

        # Flags and Subjects
        self.construction_project_created = observers.Subject('construction_project_created')

        self.flags = colony_flags.copy()
        if flags is not None:
            self.flags.update(flags)

        # Colony Type information
        self.colony_type = 'mixed'

        # Colony buildings information
        self.buildings = {
            'mines': 100,
            'factories': {
                'total': 100,
                'free': 100
            }
        }

        # Colony Storage
        self.resource_storage = {
            'total': 1999999998,
            'water': 999999999,
            'building_materials': 999999999
        }

        # Instance list
        self.installations = dict()
        self.construction_projects = collections.OrderedDict()
        self.remove_construction_project_list = list()

        self.__dict__.update(kwargs)

        if self.flags['capital']:
            empire_instance.colonies['capital'] = self
        else:
            empire_instance.colonies[self.ids['self']] = self

        planet_instance.colonies[self.ids['self']] = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary

    def update(self):
        if self.buildings['mines']:
            self.mine_resources()

    def mine_resources(self):
        pass

    def get_free_factories(self, max):
        if max <= self.buildings['factories']['free']:
            self.buildings['factories']['free'] -= max
            return max
        else:
            amount = self.buildings['factories']['free']
            self.buildings['factories']['free'] = 0
            return amount

    def unhook_all(self):
        """
        Unhooks any observer from self, and from all children.
        """
        self.construction_project_created.remove_all()
        for construction_project in self.construction_projects.items():
            construction_project.unhook_all()

    def delete_construction_projects(self):
        for construction_project in self.remove_construction_project_list:
            construction_project = self.construction_projects[construction_project]
            """:type: game_code.game_logic.faction_objects.construction_projects.ConstructionProject"""
            self.buildings['factories']['free'] += construction_project.num_of_factories['current']
            del self.construction_projects[construction_project]
        self.remove_construction_project_list = list()

        while self.buildings['factories']['free'] > 0:
            for construction_project in self.construction_projects.items():
                construction_project.get_free_factoires()

    # SETTERS
    def add_buildings(self, building):
        if type(building) == str:
            self.buildings[building] += 1
        else:
            self.galaxy.add_objects({'installations': building})
            self.installations[building.name] = building.id
