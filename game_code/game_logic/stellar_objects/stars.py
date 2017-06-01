"""
The stars File

A file containing any relevant information about the star object
"""

import random

from game_code.game_data.constants import galaxy_generation_constants as constants
from game_code.game_logic import utility_functions

star_flags = {

}


class Star:
    """
    The Star Object. Used for stars within the galaxy
    """
    def __init__(self, star_id, flags, x, y, galaxy, **kwargs):
        """
        Initialize the star instance
        
        :param star_id: The ID of the star
        :param flags: Any additional flags for any specific use
        :param x: X coord for the star
        :param y: Y coord for hte star
        :param galaxy: Galaxy
        :param kwargs: Any Kwargs used to assign specific values computed below
        """
        self.galaxy = galaxy  # Reference to the galaxy
        self.name = utility_functions.name_creator(  # Name of the object (For game purposes)
            mini=random.randint(2, 3),
            maxi=random.randint(3, 5),
            syl=random.randint(1, 2)
        )

        self.ids = {
            'self': star_id  # ID of self
        }

        self.flags = star_flags.copy()  # Relevant flags for colonies
        if flags is not None:
            self.flags.update(flags)

        self.coordinates = [int(x), int(y)]  # System coordinates

        self.star_type = random.choice(constants.STARS)  # Star Type

        self.planets = dict()  # A dict of {id's: instances} of planet keys.

        self.__dict__.update(kwargs)  # Update any kwargs

        galaxy.world_objects['stars'][self.ids['self']] = self  # Assign to galaxy.

    def __getstate__(self):
        """
        Invoked whenever serializing self. Used to shed any issue with circularisation.
        
        :return dictionary: A dict of self, without pointers to parent object
        """
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        return dictionary

    def unhook_all(self):
        """
        Unhooks any observer from self, and from all children.
        """
        pass

    def generate_planets(self, amount=-1):
        """
        Generates planets for the system.
        
        :param amount: Defaults to -1, and will generate random amount of planets. Otherwise specifies the amount 
        intended to be created.  
        :return self.planets: A quick reference to all planets within the system 
        """
        if amount < 0:
            amount = random.randint(3, 8)
        for i in range(0, amount):
            self.galaxy.create_new_planet(self)
        return self.planets
