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

        # Flags
        self.flags = colony_flags.copy()
        if flags is not None:
            self.flags.update(flags)

        # Colony Type information
        self.colony_type = 'mixed'  # Military, Mixed, Civilian

        # Colony buildings information
        self.buildings = {
            # Quantity buildings (Can keep expanding more facilities)
            'mines': 100,
            'factories': 100,
        }
        self.installations = {
            # The are buildings that have instances attached with special and unique stats for each building.
            # 'name': id
        }

        self.construction_projects = {}  # A dict of {id's: instance} of all construction projects assigned to the colony.

        # Colony Storage
        self.resource_storage = {
            'water': 999999999,
            'building_materials': 999999999999
        }

        self.__dict__.update(kwargs)

        if self.flags['capital'] == True:
            empire_instance.colonies['capital'] = self
        else:
            empire_instance.colonies[self.ids['self']] = self

        planet_instance.colonies[self.ids['self']] = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary

    def update_construction(self, galaxy, empire):
        for construction_project in self.construction_projects:
            galaxy.construction_projects[construction_project].tick_construction(empire, self)

    # SETTERS
    def add_buildings(self, building):
        if type(building) == str:
            self.buildings[building] += 1
        else:
            self.galaxy.add_objects({'installations': building})
            self.installations[building.name] = building.id
