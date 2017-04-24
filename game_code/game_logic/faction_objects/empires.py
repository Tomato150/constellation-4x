class Empire:
    def __init__(self, empire_id, flags, name, galaxy, **kwargs):
        # Empire name and identification
        self.galaxy = galaxy
        self.name = name

        self.ids = {
            'self': empire_id
        }
        self.flags = dict() if flags is None else flags

        # Empire modifiers and stats
        self.modifiers = {
            'building_modifiers': {
                'build_points': 10  # How much each factory is worth each year.
            }
        }

        # Empire entities
        self.colonies = {}  # A dict of {ids: instances} for colonies. Colony '0' should always be the player's capital colony.
        self.fleets = {}  # See above for fleets.

        self.__dict__.update(kwargs)

        galaxy.world_objects['empires'][self.ids['self']] = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary
