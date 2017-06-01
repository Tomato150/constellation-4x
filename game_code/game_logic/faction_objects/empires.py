empire_flags = {
    'player_empire': False
}


class Empire:
    """
    The Empire Object.
    """
    def __init__(self, empire_id, name, flags, galaxy, **kwargs):
        """
        Initialize the empire instance.
        
        :param empire_id: The ID of the empire
        :param flags: Name of the empire
        :param galaxy: Galaxy
        :param kwargs: Any specific values to set for the empire.
        """
        self.galaxy = galaxy  # Reference to the galaxy object
        self.name = name  # Name of the empire

        self.ids = {'self': empire_id}  # ID of self.

        self.flags = empire_flags.copy()  # Relevant flags for empires
        if flags is not None:
            self.flags.update(flags)

        self.modifiers = {  # Stats and modifiers for the empire
            'building_modifiers': {
                'build_points': 10  # How much each factory is worth each year.
            }
        }

        # Empire entities
        self.colonies = {
            'capital': None
        }
        self.colonies_updates = dict()

        self.fleets = dict()  # A dict for the fleets in the empire
        self.fleets_updates = dict()

        self.__dict__.update(kwargs)  # Update any kwargs

        galaxy.world_objects['empires'][self.ids['self']] = self  # Assign to value on galaxy. Strong ref
        if self.flags['player_empire']:
            galaxy.player_world.player_empire = self

    def __getstate__(self):
        """
        Invoked whenever serializing self. Used to shed any issue with circularization.
        
        :return dictionary: A dict of self, without pointers to parent object
        """
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary

    def update(self):
        """Update method for the colony"""
        for colony_id, colony_update in self.colonies_updates.items():
            if colony_update:
                self.colonies[colony_id].update()

    def check_for_update(self):
        pass
