import random

from game_code.game_data.constants import galaxy_generation_constants as constants
from game_code.game_logic import utility_functions


class Star:
    def __init__(self, star_id, flags, x, y, galaxy, **kwargs):
        # System General information
        self.galaxy = galaxy
        self.name = utility_functions.name_creator(random.randint(2, 3), random.randint(3, 5), random.randint(1, 2))

        #Parents
        self.ids = {
            'self': star_id
        }
        self.flags = dict() if flags is None else flags

        # System Location Information
        self.coordinates = [int(x), int(y)]

        # Star type information
        self.star_type = random.choice(constants.STARS)

        # System Contents information:
        self.planets = {}  # A dict of {id's: instances} of planet keys.

        # Update kwargs
        self.__dict__.update(kwargs)

        galaxy.world_objects['stars'][self.ids['self']] = self

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary

    def generate_planets(self, amount=-1):
        if amount < 0:
            amount = random.randint(3, 8)
        for i in range(0, amount):
            self.galaxy.create_new_planet(self, self.name, len(self.planets))
        return self.planets
