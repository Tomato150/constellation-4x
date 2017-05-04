from utils import observers


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
            'factories': 100,
        }

        # Colony Storage
        self.resource_storage = {
            'water': 999999999,
            'building_materials': 999999999999
        }

        # Instance list
        self.installations = dict()
        self.construction_projects = dict()
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

    def unhook_all(self):
        self.construction_project_created.remove_all()
        for construction_project in self.construction_projects.items():
            construction_project.unhook_all()

    def delete_construction_projects(self):
        for id in self.remove_construction_project_list:
            del self.construction_projects[id]
        self.remove_construction_project_list = list()

    # SETTERS
    def add_buildings(self, building):
        if type(building) == str:
            self.buildings[building] += 1
        else:
            self.galaxy.add_objects({'installations': building})
            self.installations[building.name] = building.id
