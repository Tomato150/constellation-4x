class Empire:
    def __init__(self, empire_id, name, galaxy, **kwargs):
        # Empire name and identification
        self.galaxy = galaxy
        self.ids = {'self': empire_id}
        self.name = name

        # Empire modifiers and stats
        self.modifiers = {
            'building_modifiers': {
                'build_points': 10  # How much each factory is worth each year.
            }
        }

        # Empire entities
        self.colonies = {}  # A dict of {ids: instances} for colonies.
        self.fleets = {}  # See above for fleets.

        self.__dict__.update(kwargs)

        galaxy.world_objects['empires'][self.ids['self']] = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary
