empire_flags = {
    'player_empire': False
}


class Empire:
    def __init__(self, empire_id, flags, name, galaxy, **kwargs):
        # Empire name and identification
        self.galaxy = galaxy
        self.name = name

        self.ids = {
            'self': empire_id
        }
        self.flags = empire_flags.copy()
        if flags is not None:
            self.flags.update(flags)

        # Empire modifiers and stats
        self.modifiers = {
            'building_modifiers': {
                'build_points': 10  # How much each factory is worth each year.
            }
        }

        # Empire entities
        self.colonies = {
            'capital': None
        }  # A dict of {ids: instances} for colonies.
        self.fleets = {}  # See above for fleets.

        self.__dict__.update(kwargs)

        galaxy.world_objects['empires'][self.ids['self']] = self
        if self.flags['player_empire']:
            galaxy.player_world.player_empire = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary
